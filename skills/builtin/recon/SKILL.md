---
name: recon
description: Fast reconnaissance - discover assets, entry points, attack surface, and hypotheses
tags: [pentest, recon, discovery]
---

# 侦察 (Recon)

## 工作流
1. 验证 `scope.md` 和 `run-policy.json`。
2. 为每个可触达的暴露面建立基准：包括 HTTP 响应头、框架线索、可见流、角色模型和状态转换。
3. 映射攻击者可控的输入：表单、JSON 字段、查询参数、Header、上传点、WebSocket 消息、postMessage 通道、GraphQL 操作以及 AI 提示词或文件输入。
4. 映射隐藏表面：JS 路由、旧版本 API、同级端点、备用方法、调试行为、内部标识符、功能开关（feature flags）等。
5. 对比信任边界：客户端与服务端检查的差异、角色转换、工作流跳过、对象所有权、缓存层、重定向和第三方集成。
6. 将观察结果转化为可测试的假设。每个假设必须针对一个入口点、一个可能的漏洞类别以及一个后续测试。
7. 报告覆盖范围缺口（coverage gaps）以及某些表面未能被观察到的原因。

## 首轮建模问题
- 真实边界是什么：纯浏览器端、纯后端、混合应用，还是认证流？
- 敏感结果更可能落在哪里：浏览器、API 响应、本地文件、数据库记录，还是内部服务？
- 应用是否在模板、重定向、文件路径、Header、序列化对象或后台任务中信任用户输入？
- 是否存在多个解析器或执行层的分歧：代理与应用、URL 解析器与 fetcher、过滤器与浏览器、序列化器与校验器？

## 高价值表面检查
- 在猜 API 之前，先读 HTML、内联脚本和打包后的 JS。
- 对比前端提交的字段和后端实际接受的字段；可选 JSON 字段、隐藏参数和备用内容类型经常打开隐藏路径。
- 尽早检查明显的元数据或辅助路径：`/robots.txt`、`/sitemap.xml`、`/.well-known/`、`/admin`、`/debug`、`/.git/`、`/.env`。
- 对有价值的路由做发现层面的变体观察：替换 HTTP 方法、内容类型和编码方式，但不要进入利用验证。

## 入口分类
- 尝试在侦察阶段先把功能归到一个主类别：注入、鉴权/授权、解析器差异、上传/解析、代理/边界信任、状态机或客户端执行。
- 如果一个功能同时触发多个类别，仍然优先写成单入口、单主假设，把其余方向留作 `coverage_gap` 或后续候选。

## 侦察心态
- 以攻击场景的角度思考，但止步于发现阶段。
- 关注异常而非数量：如命名漂移、错误差异、版本差异、缺失的同级项、非预期参数以及状态矛盾。
- 将每个功能视为一组对象、角色、转换和副作用的集合。
- 利用失败的测试结果来完善模型，而不是重复相同的角度。
- 范围（Scope）来源于本地策略文件。

## 漏洞覆盖
在映射功能或某个表面提示存在漏洞类别时，请参阅 `references/vuln-class-matrix.md`。

利用它来回答三个问题：
1. 侦察阶段应该在此收集什么信号？
2. 现在应该保存什么证据？
3. `targeted-pentest`（针对性渗透测试）的 `next_test` 该如何措辞？

该矩阵是以发现为导向的。请勿将漏洞利用载荷（payloads）、提权链或报告用语复制到侦察输出中。

## 假设规范 (Hypothesis Discipline)
- 确保 `statement`（描述）具体且具有可证伪性。
- 保持 `entry_point`（入口点）精细：单一路径、路由、变更、文件处理器或工作流步骤。
- `kind` 使用可能的漏洞类别，而非完整的利用链。
- 在 `why_plausible`（合理性说明）中放入机制详情。
- 在 `next_test` 中放入最小化的确认动作。
- 如果证据不足，应降低 `confidence`（置信度）而不是扩大假设范围。
- 保持 `candidate_findings`（候选发现）仅作为观察结果；其状态必须保持为 `candidate`。

## 证据规范 (Evidence Discipline)
- 将可重现的请求、响应、截图、路由图和代码片段保存至 `evidence/` 目录下。
- 记录观察每种行为时所使用的角色、账号状态和前提条件。
- 区分已确认的资产与第三方的观察结果。
- 注明未观察到的内容：缺失的角色对比、未测试的备用方法、受限状态或不可用的账号。

## 提交约定 (Submission Contract)
仅调用一次 `submit_sub_agent_output`。
- `assets`: 已确认的主机、路径、端点、参数、角色或工作流节点。
- `hypotheses`: 包含 `hypothesis_id`、`kind`、`entry_point`、`statement`、`why_plausible`、`next_test`、`priority` 和 `confidence` 的具体记录。
- `candidate_findings`: 仅限有证据支撑的观察结果；状态必须保持为 `candidate`。
- `evidence_refs`: 仅限可追溯的文件或捕获的工件。
- `coverage_gaps`: 具体的未观察表面或对比，用于驱动下一轮循环。
