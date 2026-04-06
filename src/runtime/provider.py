from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib import error as urllib_error
from urllib import request as urllib_request

from core.models import AgentRuntimeRequest, AgentRuntimeResponse


class ProviderAgentRuntime:
    """直连 provider 的运行时，不依赖 claude CLI 登录态。"""

    def __init__(
        self,
        *,
        cwd: str | Path | None = None,
        model: str,
        base_url: str,
        auth_token: str | None = None,
        api_key: str | None = None,
        max_tokens: int = 1024,
        timeout_seconds: float = 60.0,
    ) -> None:
        self.cwd = Path(cwd).resolve() if cwd else None
        self.model = model.strip()
        self.base_url = base_url.strip()
        self.auth_token = auth_token.strip() if auth_token else None
        self.api_key = api_key.strip() if api_key else None
        self.max_tokens = max_tokens
        self.timeout_seconds = timeout_seconds
        self.messages_urls = _build_candidate_messages_urls(self.base_url)

        if not self.model:
            raise ValueError("provider runtime 缺少 model。")
        if not self.base_url:
            raise ValueError("provider runtime 缺少 base_url。")
        if not (self.auth_token or self.api_key):
            raise ValueError("provider runtime 缺少认证信息（auth_token 或 api_key）。")

    def run(self, request: AgentRuntimeRequest) -> AgentRuntimeResponse:
        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "system": request.system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self._prompt_text(request),
                        }
                    ],
                }
            ],
        }

        try:
            response_json, status_code, used_url = self._post(payload)
        except RuntimeError as exc:
            message = f"[provider_error] {exc}"
            return AgentRuntimeResponse(
                agent_name=request.agent_name,
                content=message,
                raw={
                    "provider": "direct_provider",
                    "error": str(exc),
                },
            )

        extracted_text = _extract_text(response_json)
        if not extracted_text:
            extracted_text = "[provider_warning] empty content in provider response"

        return AgentRuntimeResponse(
            agent_name=request.agent_name,
            content=extracted_text,
            raw={
                "provider": "direct_provider",
                "status_code": status_code,
                "messages_url": used_url,
                "response": response_json,
            },
        )

    def _post(self, payload: dict[str, Any]) -> tuple[dict[str, Any], int, str]:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        last_error: Exception | None = None
        auth_attempts = self._auth_header_candidates()

        for messages_url in self.messages_urls:
            for auth_name, auth_headers in auth_attempts:
                request = urllib_request.Request(messages_url, data=body, method="POST")
                for key, value in self._base_headers().items():
                    request.add_header(key, value)
                for key, value in auth_headers.items():
                    request.add_header(key, value)

                try:
                    with urllib_request.urlopen(request, timeout=self.timeout_seconds) as response:
                        status_code = response.getcode()
                        response_text = response.read().decode("utf-8", errors="replace")
                except urllib_error.HTTPError as exc:
                    error_body = exc.read().decode("utf-8", errors="replace")
                    if exc.code in {401, 404}:
                        last_error = RuntimeError(
                            f"provider 请求失败: HTTP {exc.code} ({auth_name}) - {messages_url} - {error_body}"
                        )
                        continue
                    raise RuntimeError(
                        f"provider 请求失败: HTTP {exc.code} ({auth_name}) - {error_body}"
                    ) from exc
                except urllib_error.URLError as exc:
                    raise RuntimeError(f"provider 网络错误: {exc.reason}") from exc

                try:
                    parsed = json.loads(response_text)
                except json.JSONDecodeError as exc:
                    raise RuntimeError(f"provider 返回非 JSON 响应: {response_text}") from exc

                if not isinstance(parsed, dict):
                    raise RuntimeError(f"provider 返回格式非法: {parsed!r}")
                if isinstance(parsed.get("error"), dict):
                    error_message = parsed["error"].get("message") or parsed["error"]
                    raise RuntimeError(f"provider 返回错误 ({auth_name}): {error_message}")
                return parsed, int(status_code), messages_url

        if last_error is not None:
            raise last_error
        raise RuntimeError("provider 请求失败：没有可用的消息端点。")

    def _base_headers(self) -> dict[str, str]:
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "anthropic-version": "2023-06-01",
        }
        return headers

    def _auth_header_candidates(self) -> list[tuple[str, dict[str, str]]]:
        if self.api_key:
            return [("x-api-key", {"x-api-key": self.api_key})]

        token = self.auth_token or ""
        if not token:
            return [("none", {})]

        if token.lower().startswith("sk-"):
            return [
                ("x-api-key", {"x-api-key": token}),
                ("authorization", {"authorization": f"Bearer {token}"}),
            ]

        return [
            ("authorization", {"authorization": f"Bearer {token}"}),
            ("x-api-key", {"x-api-key": token}),
        ]

    def _prompt_text(self, request: AgentRuntimeRequest) -> str:
        prompt = f"当前agent：{request.agent_name}\n\n当前任务：\n{request.user_prompt}"
        if not request.context:
            return prompt
        return (
            f"{prompt}\n\n上下文（JSON）：\n"
            f"{json.dumps(request.context, ensure_ascii=False, indent=2)}"
        )


def _build_candidate_messages_urls(base_url: str) -> list[str]:
    cleaned = base_url.strip().rstrip("/")
    lowered = cleaned.lower()
    candidates: list[str] = []

    if lowered.endswith("/v1/messages"):
        candidates.append(cleaned)
    elif lowered.endswith("/v1"):
        candidates.append(f"{cleaned}/messages")
    elif lowered.endswith("/messages"):
        candidates.append(cleaned)
    else:
        candidates.append(f"{cleaned}/v1/messages")
        candidates.append(f"{cleaned}/messages")

    if "/anthropic" in lowered:
        removed = cleaned[: lowered.rfind("/anthropic")]
        removed = removed.rstrip("/")
        if removed:
            candidates.append(f"{removed}/v1/messages")
            candidates.append(f"{removed}/messages")

    uniq: list[str] = []
    for item in candidates:
        if item not in uniq:
            uniq.append(item)
    return uniq


def _extract_text(payload: dict[str, Any]) -> str:
    content = payload.get("content")
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if not isinstance(block, dict):
                continue
            text = _extract_block_text(block)
            if text:
                parts.append(text)
        if parts:
            return "\n".join(parts)

    choices = payload.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            message = first.get("message")
            if isinstance(message, dict):
                message_content = message.get("content")
                if isinstance(message_content, str) and message_content.strip():
                    return message_content.strip()
                if isinstance(message_content, list):
                    parts = []
                    for item in message_content:
                        if not isinstance(item, dict):
                            continue
                        text = _extract_block_text(item)
                        if text:
                            parts.append(text)
                    if parts:
                        return "\n".join(parts)

    reasoning_content = payload.get("reasoning_content")
    if isinstance(reasoning_content, str) and reasoning_content.strip():
        return reasoning_content.strip()

    output_text = payload.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    return ""


def _extract_block_text(block: dict[str, Any]) -> str:
    text = block.get("text")
    if isinstance(text, str) and text.strip():
        return text.strip()

    thinking = block.get("thinking")
    if isinstance(thinking, str) and thinking.strip():
        return thinking.strip()

    reasoning = block.get("reasoning_content")
    if isinstance(reasoning, str) and reasoning.strip():
        return reasoning.strip()

    return ""
