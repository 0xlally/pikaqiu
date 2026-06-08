# Platform Identities — Canonical Env Var Map

ALL agents, skills, and orchestrators that need a username, handle, email,
password, token, or cookie for a bug bounty platform MUST read it from these
env vars at runtime.

> NEVER hardcode a username, email alias, password, token, or cookie in source,
> markdown, scope.yaml, reports, or PoCs. NEVER guess or hallucinate one. NEVER
> use a placeholder like `<your-h1-handle>` and assume the user will fill it in.
> If a needed env var is unset, FAIL LOUDLY with a message naming the missing
> variable — DO NOT substitute a default and DO NOT fall back to a different
> platform's identity.
>
> This file lists var **names** only. Values live in the user's shell env and
> never in this repo (public).

## HackerOne

| Env var | Holds | Use for |
|---------|-------|---------|
| `HACKERONE_USERNAME` | Researcher handle on `hackerone.com` | Reporter field, @-mentions, "who is this report from" |
| `HACKERONE_TOKEN` | API token paired with the username | REST API auth (`Authorization: Basic`) |
| `H1_API_KEY` | Combined `username:token` form | Clients/scripts that want a single secret |
| `HACKERONE_EMAIL_ALIAS` | `<handle>@wearehackerone.com` forwarder | Any target form / PoC signup that asks for "an email" |

## Bugcrowd

| Env var | Holds | Use for |
|---------|-------|---------|
| `BUGCROWD_USERNAME` | Researcher handle on `bugcrowd.com` | Reporter field, @-mentions |
| `BUGCROWD_EMAIL` | Real account login email | **Bugcrowd login flow only.** Never expose to a target program, never put in a PoC, never paste into a third-party form. |
| `BUGCROWD_PASSWORD` | Account password | Auth flow only |
| `BUGCROWD_TOTP_SECRET` | Base32 TOTP secret | 2FA codes during auth |
| `BUGCROWD_EMAIL_ALIAS` | `<handle>@bugcrowdninja.com` forwarder | Any target form / PoC signup that asks for "an email" |
| `BUGCROWD_TOKEN` | API token | REST API auth (when applicable) |

## Intigriti

| Env var | Holds | Use for |
|---------|-------|---------|
| `INTIGRITI_USERNAME` | Researcher handle on `intigriti.com` | Reporter field, @-mentions |
| `INTIGRITI_TOKEN` | API token | REST API auth |
| `INTIGRITI_SPA_COOKIE` | SPA session cookie | Used when REST API is not viable |
| `INTIGRITI_EMAIL_ALIAS` | `<handle>@intigriti.me` forwarder | Any target form / PoC signup that asks for "an email" |

## YesWeHack

| Env var | Holds | Use for |
|---------|-------|---------|
| `YESWEHACK_EMAIL` | `<scoped>@yeswehack.ninja` forwarder | The **only** YesWeHack identity. Used as both reporter and contact email. |
| `YESWEHACK_TOKEN` | API token (when issued) | REST API auth |

YesWeHack has **no separate username field**. Do not invent one.

## Rules

1. **Handle vs alias are not interchangeable.** Three platforms (HackerOne /
   Bugcrowd / Intigriti) have a *handle* (`*_USERNAME`) AND a separate
   *email alias* (`*_EMAIL_ALIAS`). The handle is the reporter / identity
   field on the platform; the alias is what you give to a *target program*
   when its form asks for an email. Never put the handle in an email field
   and never put the alias in a username field.
2. **Cross-platform isolation.** A HackerOne alias only routes mail through
   HackerOne; same for Bugcrowd, Intigriti, YesWeHack. Never reuse one
   platform's identity (handle OR alias) when interacting with another
   platform.
3. **Personal email is reserved.** `BUGCROWD_EMAIL` is the only env var that
   holds the real personal login email, and it is used only by the Bugcrowd
   auth flow (`mcp-bounty-server/providers/bugcrowd_auth.py`). Never expose
   it to a program, in a PoC, in a screenshot, or in a report.
4. **Read at runtime.** Read every variable at runtime via the platform-native
   accessor:
   - Python: `os.environ.get("HACKERONE_USERNAME")`
   - Node: `process.env.HACKERONE_USERNAME`
   - Shell: `"$HACKERONE_USERNAME"`
   - Skill / agent prompt: pass the symbol through, do not resolve it.
5. **Fail loudly when unset.** If an operation needs `HACKERONE_USERNAME` and
   it is unset, abort with a message like:
   `error: HACKERONE_USERNAME is not set; refusing to guess`.
   Do NOT pick a different env var, do NOT use a placeholder, do NOT prompt
   the model to invent one.
6. **Reports & PoCs reference the symbol, never the value.** When a generated
   report, PoC, or sign-up script needs to embed the researcher's identity,
   write the env-var symbol (e.g. `${HACKERONE_EMAIL_ALIAS}`) into the saved
   artifact. Substitute the actual value only at submit/run time, never at
   draft/commit time. Committed artifacts must stay free of personal
   identifiers because this repo is public.
7. **Forwarded by MCP.** The `bounty-platforms` MCP server has these names in
   its `forwardEnv` list (`.mcp.json`). If you add a new platform-identity
   var, add the name to `forwardEnv` too, otherwise the MCP server will not
   see it.

## Quick lookup: "What identity goes here?"

| Need | HackerOne | Bugcrowd | Intigriti | YesWeHack |
|------|-----------|----------|-----------|-----------|
| Reporter handle / @-mention | `$HACKERONE_USERNAME` | `$BUGCROWD_USERNAME` | `$INTIGRITI_USERNAME` | (n/a) |
| Email field on target signup / PoC | `$HACKERONE_EMAIL_ALIAS` | `$BUGCROWD_EMAIL_ALIAS` | `$INTIGRITI_EMAIL_ALIAS` | `$YESWEHACK_EMAIL` |
| API auth | `$H1_API_KEY` *or* `$HACKERONE_USERNAME` + `$HACKERONE_TOKEN` | `$BUGCROWD_TOKEN` | `$INTIGRITI_TOKEN` | `$YESWEHACK_TOKEN` |
| Web/SPA auth | (use API) | `$BUGCROWD_EMAIL` + `$BUGCROWD_PASSWORD` + `$BUGCROWD_TOTP_SECRET` | `$INTIGRITI_SPA_COOKIE` | (use API) |
