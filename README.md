# KrystianPawlowskiKnowledge

Personal knowledge tier of Krystian Pawlowski, the counterpart of the "Personnel" tier that `solarsplit-core` describes for Wilfried. It holds what is mine or specific to my machine: preferences, accounts and token locations, workstation notes, and any personal rule or skill I want Claude Code and Cursor to load without touching the shared `SolarsplitKnowledge`.

Same mechanics as the shared repo, same scripts, one reader.

## Layout

| Path | Role |
|---|---|
| `.cursor/rules/personal-dispatcher.md` | Permanent layer. Loaded every session by Claude Code (linked into `~/.claude/rules/`, no `paths` field) and by Cursor (`alwaysApply: true`). Carries the personal routing table |
| `.cursor/rules/<name>.md` | One file per resource. Real file in `.md`, relative `.mdc` symlink next to it for Cursor |
| `claude/skills-manifest.json` | Declares which rules are exposed to Claude Code as skills. Discovered by the shared `sync-claude-skills.py` because this repo sits next to `SolarsplitKnowledge` |
| `claude/skills/<name>/` | Generated: `SKILL.md` summary and `rule.md` relative link. Never edited by hand |
| `scripts/setup-claude-code-personal.sh` | Installs and repairs the links, regenerates the skills, checks frontmatter and targets, prints the size of the permanent layer. Idempotent |

## Install

The shared layer first, then this one. The shared script needs the parent folder as an absolute argument, this one derives everything from its own location. Both print a verification at the end that is worth reading.

```bash
sh ~/solarsplit-dev/code/SolarsplitKnowledge/scripts/setup-claude-code.sh /Users/solarsplit/solarsplit-dev/code
sh ~/solarsplit-dev/code/KrystianPawlowskiKnowledge/scripts/setup-claude-code-personal.sh
```

Then open a new Claude Code session. In Cursor, reload the window and open a new conversation, it reads the rule frontmatter at launch only.

## Add a rule or a skill

1. Create `.cursor/rules/<name>.md` with a frontmatter carrying a quoted `description`. `alwaysApply: false` for a skill, `globs:` plus `paths:` for a path-scoped rule. Only the dispatcher is `alwaysApply: true`.
2. `cd .cursor/rules && ln -s <name>.md <name>.mdc`, relative.
3. For a skill, add `"<name>": "<name>"` to `claude/skills-manifest.json`. Key is the skill name, value the rule file name without extension.
4. `sh scripts/setup-claude-code-personal.sh`.
5. Add a row to the routing table of the dispatcher, commit.

The rules that protect against silent failures are the shared ones: quote `globs` and any `description` containing `: `, keep the real file in `.md`, never write an absolute machine path in a generated skill. The setup script checks the frontmatter and the link targets each time it runs. Diagnosis of anything that does not load: shared skill `agent-context-mechanics`.

## Session journal

Session entries go neither here nor in the shared journal of SolarsplitKnowledge. They live in a second personal-tier repo, `~/solarsplit-dev/code/KrystianPawlowskiSessionLog`, one file per session, conventions in its own README. The dispatcher carries the rule, this README only points to it.

## Confidentiality

This repo is never cloned by anyone else and is never referenced in a shared repo beyond its name, which the shared workspace map tolerates. The names of its rule files stay here, in a shared repo write "the personal dispatcher". Nothing here is copied into `SolarsplitKnowledge` or a product repo, and nothing from Wilfried's CEO or personal tiers exists on this machine.

## Remote

Local only for now. To back it up, create a private repository under the account of your choice and push. With the work account, the `gh` CLI does it in one step from this folder:

```bash
gh repo create KrystianPawlowskiKnowledge --private --source . --push
```
