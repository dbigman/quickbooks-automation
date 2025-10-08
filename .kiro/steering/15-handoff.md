---
inclusion: manual
---

# Rule: Produce a Quick Handoff (Knowledge-Transfer) Doc

## Objective
When asked to "create handoff", "make a KT doc", "summarize progress", or similar, gather just enough project context and write a small, actionable markdown file that lets a fresh LLM immediately continue the task without re-reading the whole repo.

## When to Use
- End of a work block or session
- Before switching modes/tools/agents
- When scope is clarified but execution will continue later

## Inputs to Collect (lightweight)
1. **Task scope & goal** (from the current chat + any plan/issue)
2. **State**: what’s done vs. remaining
3. **Key files & entrypoints** touched or created
4. **Decisions & constraints** (APIs, patterns, versions, non-goals)
5. **How to resume**: exact commands, env notes, test paths
6. **Links/artifacts** (PRs, tickets, docs)

> If unknowns block progress, ask up to **3 targeted questions** first; otherwise proceed and mark items as “Assumptions”.

## Process
1. **Derive scope** from the latest discussion and any available plan/notes.
2. **Skim for anchors**: README, package/project manifest, test runner config, primary app entry, and any files touched in this session.
3. **Summarize decisions** and constraints in bullets; avoid speculation.
4. **List work status** with checkboxes: Done / Remaining.
5. **Write a resume guide**: exact terminal commands, scripts, and test sequences to pick up from the next step.
6. **Name & save** the doc at `handoff/KT-<YYYY-MM-DD>-<task-slug>.md`.
7. **If supported**, show the diff and ask for approval before saving/committing.

## Output Requirements
- **One markdown file**, ≤ 200 lines, plain language.
- Use relative repo paths; include only essential snippets.
- No sensitive secrets; reference env var names instead.

## Template (fill all sections)
---
# Handoff: <Task Title>
**Date:** <YYYY-MM-DD>  
**Repo/Branch:** <repo>@<branch>  
**Last Commit (short):** <hash> – <message>  
**Status:** <Ready to Act | In Progress | Blocked(with reason)>

## Objective & Scope
- <1–3 bullets describing the goal and boundaries>

## Context & Decisions
- <APIs/SDKs/libraries chosen and why>
- <Key architectural notes or patterns>
- <Non-goals / out of scope>

## Files & Entry Points
- `<path/to/file>` – <purpose/what changed>
- `<path/to/entry>` – <how to run/call>

## What’s Done ✅
- [x] <step or change>
- [x] <tests/docs updated?>

## What’s Next ⏭️
- [ ] <very next action with file/function>
- [ ] <subsequent steps in order>

## How to Resume (Exact Commands)
```bash
# setup
<command to install / build>
# run / watch
<command>
# test
<command or test pattern>
