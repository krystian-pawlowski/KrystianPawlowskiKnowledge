---
description: "Personal context of Krystian Pawlowski: who I am, language and working preferences, where my session journal lives, how this Mac differs from the workspace the shared rules describe, GitHub accounts, confidentiality of this tier, and the routing table of personal resources. Always loaded."
alwaysApply: true
---

<!--
GIT-TRACKED in KrystianPawlowskiKnowledge/.cursor/rules/
Real file in .md, relative .mdc symlink next to it for Cursor.
Linked from ~/.claude/rules/ (Claude Code: no `paths` field, so it loads every session)
and from the Cursor workspace root .cursor/rules/ (alwaysApply: true).

This is the PERSONAL DISPATCHER that solarsplit-core refers to, for this machine and its
one user. Its file name and the names of the other rules of this repo must never appear
in a repo shared with the dev team. Over there, write "the personal dispatcher".

Keep it small. It shares the 50 KB permanent-layer cap with solarsplit-core (about 26 KB)
and ~/.claude/CLAUDE.md. Only what is true for almost every task belongs here. The rest
goes into a rule of this repo, exposed as a skill through claude/skills-manifest.json.
-->

# Personal context, Krystian Pawlowski

Loaded on top of `solarsplit-core`. The shared rules describe the workspace, the tiers and the writing style as seen from Wilfried's machine. This file translates them to this machine and adds what is personal. When the two disagree on a path or an account, this file wins, on everything else the shared rules win.

## 1. Who I am

Krystian Pawlowski, developer on the SOLARSPLIT team, k.pawlowski@solarsplit.com. I work across SolarsplitWebClient, SolarsplitWeb and the mobile apps, and I review pull requests on the iOS and Android repos.

## 2. How to work with me

- Talk to me in English. SOLARSPLIT deliverables follow the shared writing style, in whatever language the deliverable needs.
- Commit messages, comments and identifiers follow the conventions of the repo they land in.
- The deployment convention of `solarsplit-core` section 3 applies unchanged: on high-risk repos, commit when useful, push, tag or merge `main` only when I ask.

## 3. Session journal

The closing routine of `solarsplit-core` section 6 sends the session entry to the shared journal of SolarsplitKnowledge. On this machine it goes to `~/solarsplit-dev/code/KrystianPawlowskiSessionLog` instead, a personal-tier repo: one file per session under `sessions/YYYY-MM-DD-<slug>.md`, conventions in its README, written and committed there at session close. No Knowledge branch or pull request for a journal entry, no `Code Session` number, no line in the shared state table. Risk level in the sense of `solarsplit-core` section 3: low, no auto-deploy and a single reader, so commit without asking, and push too once a remote exists.

Only the fourth gesture stays shared: a rule of SolarsplitKnowledge that the session has made false is fixed through a pull request reviewed by Wilfried, and the journal entry names that pull request. The journal never enters a shared repo and a shared repo never learns its file names, same rule as the confidentiality section below.

## 4. This Mac is not Wilfried's

The shared rules assume `~/Code/GitHub`, which does not exist here. Translate every such path:

| Shared rules say | Here |
|---|---|
| `~/Code/GitHub/<repo>`, whatever the repo | `~/solarsplit-dev/code/<repo>`, every repo cloned flat, no intermediate folder |
| workspace root carrying `.cursor/rules/` | `~/solarsplit-dev`, not a git repo, also carries `CLAUDE.md` and `.claude/` |
| parent folder passed to the setup and sync scripts | `/Users/solarsplit/solarsplit-dev/code`, absolute |

A repo from the shared workspace map that is not in `code/` is not cloned here, not misplaced. `SolarsplitPrivate`, Wilfried's personal repos and their journals are not on this machine and a shared rule that points to them leads nowhere. The full list of what is cloned, and everything else about this machine, is in `workstation-setup`.

## 5. GitHub and git identity

One account on this machine, `krystian-pawlowski`, the work account, member of the SOLARSPLIT and HelveticApp organisations. The `gh` CLI is logged in with it and works from Claude Code shells, sandbox included: `gh pr`, `gh api`, `gh repo` are available, and git authenticates over HTTPS through the same login, no token to manage by hand and none exported in the shell. `~/.ssh` is unreachable from Claude Code, so remotes stay on HTTPS. Every repo commits as k.pawlowski@solarsplit.com through `~/.gitconfig`. Details and checks in `workstation-setup`.

## 6. Confidentiality of this tier

This repo is my personal tier, the counterpart of the "Personnel" row of `solarsplit-core` section 4. It holds what is mine or specific to this machine: preferences, accounts, where tokens live, personal notes. Nothing here is copied into a shared repo, and a shared repo never learns the names of the files in here. Wilfried's CEO and personal tiers are separate repos that I do not have, and this repo never receives their content either. The session journal repo of section 3 belongs to this same tier.

## 7. Personal routing table

Same mechanics as `solarsplit-core` section 6. Claude Code: a skill, triggered by its description or invoked by `/name`. Cursor: read `KrystianPawlowskiKnowledge/.cursor/rules/<name>.md` directly, do not wait for it to attach.

| Resource | Load when the task touches |
|---|---|
| `workstation-setup` | Paths and cloned repos on this Mac, git identity, the GitHub account and how `gh` authenticates git, what Claude Code shells cannot reach, the Android and Xcode toolchains, the Claude Code and Cursor layers installed here and how to reinstall them, how to add a personal rule or skill |

## 8. Maintaining this repo

Repo: `~/solarsplit-dev/code/KrystianPawlowskiKnowledge`, same conventions as SolarsplitKnowledge, full procedure in `workstation-setup` section 6. Risk level in the sense of `solarsplit-core` section 3: low, no auto-deploy and a single reader, so commit and push without asking once a remote exists. The short form:

1. Edit or create the real `.md` in `.cursor/rules/`, with its relative `.mdc` symlink next to it.
2. Permanent content goes in this file. Path-scoped content gets `globs:` and `paths:`. Everything else becomes a skill through `claude/skills-manifest.json`.
3. Run `sh scripts/setup-claude-code-personal.sh`. It links, regenerates the skills through the shared sync script, checks the frontmatter and verifies every target.
4. Add the row to the table above, commit, reload the Cursor window, open a new Claude Code session.
