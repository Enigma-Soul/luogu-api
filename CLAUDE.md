# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Workflow Rules

- **Auto-commit**: commit after completing each distinct task
- **Auto-push**: push to `develop` branch every 5 commits
- **API issues**: when a test reveals a discrepancy between docs and actual API behavior, do NOT modify docs first — ask the user for confirmation before making changes
- **New API**: when the user provides a new/changed API, test it via luogutests first, then update docs
- **Doc updates**: always update ALL representations: `docs/*.md`, `openapi/paths/*.yaml` (+ `openapi/components/schemas.yaml` for shared schemas), `luogu-api.d.ts` TypeScript types, AND corresponding `luogutests/*.py` test file
- **Consistency checks**: when reviewing or adding APIs, cross-check `docs/*.md` ↔ `openapi/paths/*.yaml` ↔ `luogutests/*.py` for the same endpoints. If discrepancies are found, report them to the user with specific diffs (endpoint path, params, response fields) so the user can manually test against the live API — do NOT assume which representation is correct

## Commands

```bash
# Run all tests
uv run luogutest

# Run a single module
uv run python luogutests/problem.py

# Commit count before auto-push
git log --oneline origin/develop..HEAD | wc -l
```

## Architecture

This repo documents Luogu (luogu.com.cn) unofficial API. Three parallel representations must stay in sync:

| Representation | Path | Purpose |
|---|---|---|
| Human-readable docs | `docs/*.md` | Per-category API docs in Chinese |
| OpenAPI 3.1 spec | `openapi/openapi.yaml` → `openapi/paths/*.yaml` + `openapi/components/schemas.yaml` | Machine-readable spec |
| TypeScript types | `luogu-api.d.ts` | Type definitions for request/response params |
| Test suite | `luogutests/*.py` | Python tests against live API |

### File Mapping

Each API category has files across all representations:

| Test module | Docs | OpenAPI path |
|---|---|---|
| `problem.py` | `problems.md` | `problems.yaml` |
| `training.py` | `problem-sets.md` | `problem-sets.yaml` |
| `contest.py` | `contests.md` | `contests.yaml` |
| `record.py` | `records.md` | `records.yaml` |
| `discuss.py` | `discussions.md` | `discussions.yaml` |
| `feed.py` | `activities.md` | `activities.yaml` |
| `user.py` | `users.md` | `users.yaml` |
| `team.py` | `teams.md` | `teams.yaml` |
| `chat.py` | `chat.md` | `chat.yaml` |
| `article.py` | `articles.md` | `articles.yaml` |
| `blog.py` | `blog.md` | `blog.yaml` |
| `theme.py` | `themes.md` | `themes.yaml` |
| `image.py` | `images.md` | `images.yaml` |
| `ide.py` | `ide.md` | `ide.yaml` |
| `paste.py` | `pastes.md` | `pastes.yaml` |
| `auth.py` | `auth.md` | `auth.yaml` |
| `misc.py` | `misc.md` | `misc.yaml` |

### Test Suite (luogutests/)

- `base.py` is the only file that imports `requests`; all other modules do `from base import LuoguClient, log, confirm`
- `LuoguClient` auto-loads `cookie.json` (project root), prefetches CSRF token, handles `lentille` / `content` response formats
- Registered as `uv run luogutest` via `[project.scripts]` in `pyproject.toml`
- Write tests require manual confirmation (y/a/n/q, Ctrl+C)

### API Conventions

- Base URL: `https://www.luogu.com.cn`
- LentilleDataResponse: requires `x-lentille-request: content-only` header, data in `.data`
- DataResponse: requires `_contentOnly` query param or `x-luogu-type: content-only` header, data in `.currentData`
- Non-GET: requires `referer: https://www.luogu.com.cn/` and `x-csrf-token` header
- User-Agent must NOT contain `python-requests` and must NOT start with `mozilla/`
