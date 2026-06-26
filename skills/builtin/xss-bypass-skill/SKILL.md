---
name: xss-bypass-skill
description: Focused XSS bypass skill for authorized CTF, lab, and pentest targets. Use for reflected, stored, and DOM XSS; HTML, attribute, JavaScript, URL, CSS, DOM sink, file upload, and admin bot contexts; and cases involving filters, WAFs, blocked tags/events/alert/parentheses/spaces, CSP, sandbox, Trusted Types, DOMPurify/mXSS, framework sinks, postMessage, restricted character sets, or bot delivery constraints. Use when Codex needs minimal-difference probes, browser/runtime verification, DOM source-sink tracing, or payload construction without broad external payload dictionaries.
---

# xss-bypass-skill

Goal: bypass filters and environment constraints, build XSS that executes in a browser or bot, and collect reproducible runtime evidence. Do not spray large payload lists. Use small representative probes to classify the blocker, then retest one variable at a time.

## Shortest Loop

1. Locate the context: confirm whether input reaches HTML text, an attribute, a JavaScript string/expression, URL, CSS, DOM sink, upload preview, or admin bot.
2. Identify constraints with 3-5 representative probes: blocked `<`, `>`, quotes, spaces, tags, events, protocols, CSP, Trusted Types, sanitizers, or bot behavior.
3. Generate the smallest payload: keep the allowed context fixed and replace only the missing piece, such as the escape, execution carrier, trigger event, or success signal.
4. Verify in a browser: for DOM, events, CSP, Trusted Types, sandbox, mXSS, upload preview, admin bot, or page success branches, use Playwright to capture dialog/console/DOM/request/state changes.
5. Stop after strong evidence: once the payload changes page state, text, navigation, session, bot callback, or flag path, stop expanding and make a minimal differential proof.

## References

- Read `references/bypass-playbook.md` when the context or blocker is known and you need a bypass construction.
- Read `references/playwright-verification.md` when you need to prove browser execution, DOM mutation, event triggering, CSP/TT/sandbox effects, upload preview behavior, or bot-like behavior.

## Notes

On failure, record the exact blocker instead of writing "XSS failed". Example: entry confirmed; reflection lands in an HTML attribute; `>` can escape but spaces are stripped; `/` separation is untested; `onload` is preserved but has no runtime signal; next step is to compare final DOM and event triggering with Playwright.
