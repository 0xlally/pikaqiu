# Vendor Posture — Patched Bugs, Framework Fingerprints, Cooldowns

> Kill-list of patched attack classes, fingerprint signatures for framework
> detection, and cooldown tables for takeover-style bugs. Agents consult this
> file when recon points at a vendor surface (cloud, IdP, CDN, managed DB) or
> when a chain relies on framework behavior.

Update this file whenever an engagement proves a vendor has closed a bug class
or a fingerprint signature drifts. Entries here prevent re-probing patched
vectors across future engagements.

---

## Patched — do not test

| Vector | Patched by | Evidence | Since |
|---|---|---|---|
| `*.azurewebsites.net` subdomain takeover | Microsoft reserves deprovisioned hostnames | `~/.claude/.../MEMORY.md`; multiple engagements | 2022-11 |
| AWS S3 "public bucket default" on new buckets | Block Public Access on by default | AWS docs, S3 console UX | 2023-04 |
| GCS uniform bucket-level access on new buckets | Google default | GCP docs | 2020 |
| GitHub Pages `*.github.io` takeover on deleted repos | 24h reservation + explicit CNAME check | GitHub security team | 2018 |

## Cloud subdomain-takeover cooldowns

Availability window after name release. Test only if cooldown is short AND
program permits third-party SaaS takeover (see `scope.yaml`, `policy.md`,
and `rules/hunting.md` Rule 1).

| Service | Cooldown | Notes |
|---|---|---|
| `*.azurewebsites.net` (App Service) | Indefinite reservation | Skip — patched. |
| `*.trafficmanager.net` | ~2 hours | Testable; still a dangling-CNAME bug when found. |
| `*.cloudapp.net` (classic VM DNS) | ~7 days | Testable but limited cloud surface remaining. |
| `*.blob.core.windows.net` | Immediate | Testable; requires storage-account-name collision. |
| `*.herokuapp.com` | Immediate after deletion | Program scope must explicitly permit. |
| `*.fastly.net` | Immediate | Requires service-config collision, not just name. |
| `*.github.io` | 24h then immediate | Test only when dangling CNAME is confirmed. |
| `s3://<bucket>` | Immediate | Region-scoped; test via `head-bucket` first. |

---

## Framework fingerprint signatures

Collect 5 signals before probing framework-specific CVEs. Partial matches are
ambiguous — run one safe differentiator before committing to a CVE list.

### Keycloak vs Spring Authorization Server

| Signal | Keycloak | Spring Authorization Server |
|---|---|---|
| OIDC discovery path | `/realms/<realm>/.well-known/openid-configuration` | `/.well-known/openid-configuration` at root |
| `issuer` in discovery | `https://.../realms/<realm>` | Equal to server base URL |
| Session cookie | `KEYCLOAK_SESSION`, `KEYCLOAK_IDENTITY` | `JSESSIONID` only |
| Admin surface | `/auth/admin/` | No built-in admin UI |
| Error body shape | Keycloak JSON envelope with `error`/`error_description` | Spring `OAuth2Error` shape |

Why it matters: Keycloak CVEs (SAML parser, account-console) do not apply to
Spring. Running them wastes probes and lights up WAFs.

### Azure App Service vs S3 static hosting

| Signal | Azure App Service | S3 static site |
|---|---|---|
| Headers | `x-powered-by: ASP.NET`, `Server: Microsoft-IIS/...`, `x-aspnet-version` | `Server: AmazonS3`, `x-amz-request-id`, `x-amz-id-2` |
| 404 body | HTML "The resource you are looking for has been removed" | `<Error><Code>NoSuchKey</Code>...` XML |

### Next.js vs Nuxt (client-rendered)

| Signal | Next.js | Nuxt |
|---|---|---|
| Hydration root | `__NEXT_DATA__` `<script>` tag | `__NUXT__` `<script>` tag |
| Asset path | `/_next/static/...` | `/_nuxt/...` |
| API conventions | `/api/*` collocated with pages | `/api/*` via Nitro server routes |

---

## Chrome CSP drift (re-verify every ~6 months)

CSP enforcement tightens roughly yearly. Before citing a CSP bypass in a chain,
re-run the PoC on the current stable channel — not a stale writeup.

| Feature | Current behavior (≥ Chrome 124) |
|---|---|
| `'unsafe-inline'` with `nonce-...` | Nonce wins; unsafe-inline ignored for that source. |
| `'strict-dynamic'` + legacy `'unsafe-inline'` | `strict-dynamic` takes precedence; `'unsafe-inline'` ignored. |
| Scheme source `https:` without host | Allowed in page context; restricted in extension contexts. |
| `script-src-attr 'unsafe-inline'` | Required for inline event handlers (`onclick=`, `onerror=`). |
| `trusted-types` enforced | Blocks DOM sinks that receive a plain string; must wrap via a trusted-type policy. |

Source: engagement findings on Snapchat and Coinmate flagged CSP drift as a
recurring false-positive source when citing old writeups.

---

## Managed-DB internal surface (Postgres catalogs)

On managed-Postgres platforms (Neon, Supabase, RDS with Postgres, Crunchy),
authenticated DB users can read per-tenant config via `pg_settings` GUCs and
catalog views. These leak internal hostnames usable as SSRF chain targets.

Low-privilege queries worth running on every managed-DB target:

```sql
SELECT name, setting FROM pg_settings
WHERE name NOT IN ('application_name','TimeZone','search_path');
SELECT * FROM pg_shadow;
SELECT * FROM pg_user;
SELECT * FROM pg_roles;
```

Vendor-prefixed GUCs (`neon.*`, `supabase.*`, `<vendor>.tenant_id`,
`<vendor>.console_url`) are the interesting rows — combine with any SSRF
primitive on the control plane.

Do NOT attempt `SET ROLE`, `ALTER ROLE`, `SECURITY DEFINER`, extension
escalation, or FDW outbound; managed platforms block these and the dead-end
wastes the session (see `rules/mistakes.md` KNOWLEDGE-GAPS).

---

## Adding new entries

New vendor hardening → append a row to the right table with first-seen date and
a pointer to the engagement or docs that proved it. Do not expand this file to
narrative lessons — those belong in `rules/mistakes.md`. Keep this file as a
lookup table the recon, subdomain-takeover, and hunter agents can grep in one
pass.
