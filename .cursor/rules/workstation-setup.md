---
description: "Krystian's Mac: workspace map and which SOLARSPLIT repos are cloned, git identities, the two GitHub accounts, token storage in the Keychain and its rotation, why the gh CLI fails from Claude Code shells and what to use instead, the Claude Code and Cursor context layers installed here and how to reinstall them, how to add a personal rule or skill. Load for any task about paths, git or GitHub access, tokens, CLI tooling, or the context setup on this machine."
alwaysApply: false
---

<!--
GIT-TRACKED in KrystianPawlowskiKnowledge/.cursor/rules/
Real file in .md, relative .mdc symlink next to it for Cursor.
Exposed to Claude Code as the skill `workstation-setup` through claude/skills-manifest.json.
Personal tier. Never named in a repo shared with the dev team.

Facts only, each verified on this machine on the date given. A statement without a way to
re-verify it does not belong here, the shared rule about state tables applies.
-->

# Workstation setup, Krystian's Mac

Verified 04.09.2026 unless stated otherwise. macOS user `omso`, Darwin 25.2, Apple silicon. System Python 3.9.6, Ruby 2.6.10 (used by the frontmatter checks), `jq` 1.7.1, Cursor in `/Applications`, Claude Code through the desktop app.

## 1. Workspace map

Everything SOLARSPLIT lives under `~/dev/solarsplit/`. There is no `~/Code/GitHub`, the path the shared rules use.

| Path | What |
|---|---|
| `~/dev/solarsplit/code` | Root opened in Cursor and Claude Code. Not a git repo. Carries `CLAUDE.md`, `.claude/` (local permissions and the hand-written `solarsplit-android` skill) and `.cursor/rules/` (symlinks to every rule, shared and personal) |
| `~/dev/solarsplit/code/SolarsplitXcode/` | Parent of the Swift-side repos and of both knowledge repos. This is the folder to pass, absolute, to the shared setup script, and the folder the sync scripts deduce from their own location |
| `~/dev/solarsplit/code/SolarsplitAndroidApp` | Android app. Its rule is `solarsplit-android.mdc` at the repo root, exposed as a local skill in `code/.claude/skills/` |
| `~/dev/solarsplit/code/SolarsplitWorkspace.xcworkspace` | Xcode workspace over the Swift repos |
| `~/dev/solarsplit/solarsplitWebFrontend` | Repo owned by the personal GitHub account, see section 3 |
| `~/dev/solarsplit/Docs`, `~/dev/solarsplit/builds` | Documents and build outputs, not repos |

Cloned in `SolarsplitXcode/` on 04.09.2026: `SolarsplitKnowledge`, `KrystianPawlowskiKnowledge`, `SolarsplitWeb`, `SolarsplitWebClient`, `solarsplit-web-landing`, `SOLARSPLITiOS`, `SolarsplitShared`, `SolarsplitAIPackage`, `SolarsplitInstallerMatchmakingPackage`, `HelvetFoundation`, `HelvetLocationPackage`, `HelvetSwiftUI`. Everything else in the shared workspace map (`SOLARSPLITRoofMetrics`, `SOLARSPLIT_COMMUNITY`, `SOLARSPLIT_MONITORING`, `SolarsplitMedia`, `SolarsplitPrivate`, Wilfried's personal repos) is not on this machine. Re-check with `ls ~/dev/solarsplit/code/SolarsplitXcode`.

## 2. Git identity

`~/.gitconfig` sets Krystian Pawlowski, krypaw@ik.me, and an `includeIf "gitdir:~/dev/solarsplit/"` that loads `~/.gitconfig-solarsplit`, which switches the email to k.pawlowski@solarsplit.com. Every repo under `~/dev/solarsplit/`, this one included, therefore commits with the work address. Check inside a repo with `git config user.email`.

Credential helper for github.com and gist.github.com: `/opt/homebrew/bin/gh auth git-credential`, which hands git the token of section 3. The git-lfs filter is configured globally.

## 3. GitHub accounts and token

Set up 03.09.2026.

- **Accounts.** `krystian-pawlowski` is the work account, member of the `SOLARSPLIT` and `HelveticApp` organisations with push rights. `omsomso` is the personal account and owns `solarsplitWebFrontend`.
- **Token.** A classic personal access token of the work account, scopes `repo` and `workflow`, no `user:email`. Stored in the macOS login Keychain as the generic password service `claude-gh-token`. Nothing in plain text on disk.
- **Loading.** `~/.zshenv` reads it with `security find-generic-password` and exports `GH_TOKEN` and `GITHUB_TOKEN`, so every shell has it, Claude Code's included. The credential helper turns it into HTTPS git auth.
- **Personal-account repos.** The work token gets a 404 on `solarsplitWebFrontend`. Run git there with the token removed from the environment: `env -u GH_TOKEN -u GITHUB_TOKEN git ...`.
- **Rotation.** Run the command below, then open a new shell, nothing else changes.

```bash
security add-generic-password -U -a "$USER" -s claude-gh-token -w '<new PAT>'
```

### The gh CLI does not work from Claude Code shells

`gh` fails with `connect: bad file descriptor` on every network call from a Claude Code shell on this machine, while `curl`, Python and `git` reach the same hosts. It is the Go dialer against the desktop app's network layer, and it persists with the sandbox disabled. Consequences:

- `gh auth status` reporting an invalid token is a false negative. Do not rotate the token on that basis.
- `gh pr create`, `gh pr view`, `gh issue`, `gh run` are unavailable. Use the REST API, for example:

```bash
curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github+json" https://api.github.com/repos/SOLARSPLIT/SolarsplitWebClient/pulls
```

- Plain `git` over HTTPS (clone, fetch, pull, push) works normally.

## 4. Context layers installed on this machine

The same rules feed Claude Code and Cursor, and could feed Codex, as `agent-context-mechanics` describes. State on 04.09.2026:

**Claude Code, `~/.claude/`**

| Where | Points to | Loads |
|---|---|---|
| `rules/solarsplit-core.md` | SolarsplitKnowledge | every session |
| `rules/personal-dispatcher.md` | this repo | every session |
| `rules/swift-gotchas-index.md`, `fluent-migrations.md`, `simulator-navigation.md` | SolarsplitKnowledge | on matching files only |
| `skills/<name>`, 16 shared plus those of this repo | `claude/skills/<name>` of each repo | on trigger or `/name` |
| `CLAUDE.md` | plain file written by the shared setup script, with a personal-tier section appended | every session |

Cap on the permanent layer: 50 KB cumulated. The personal setup script prints the current figure at the end of every run, the reference measurement is the script of `agent-context-mechanics` section 8, to run from `SolarsplitXcode/`.

**Hooks: none.** `~/.claude/settings.json` has no `hooks` key, so the shared guards (`hook-sync-skills-guard.sh`, `hook-journal-guard.py`) are not active here. After editing a rule, run the sync by hand, or the personal setup script, which does it.

**Cursor, workspace root `~/dev/solarsplit/code/.cursor/rules/`.** One `.mdc` symlink per rule, shared and personal. Cursor reads the frontmatter at window launch only, reload the window and open a new conversation after any change.

**Codex.** `~/.codex` exists but no `AGENTS.md`, `hooks.json` or `~/.agents/skills/` were generated. `python3 SolarsplitKnowledge/scripts/sync-codex-layer.py --write` would produce them from the same sources, personal dispatcher included, since it deduces the permanent layer from `~/.claude/rules/`.

**Shared CLIs not installed here.** `swlogs` is not on the PATH and `~/.config/swlogs/` does not exist, `~/.local/bin` does not exist either, and there is no `~/.config/ssapi`. The skills `solarsplit-ops` and `solarsplit-api` describe their installation when needed.

### Reinstall or repair, idempotent

```bash
sh ~/dev/solarsplit/code/SolarsplitXcode/SolarsplitKnowledge/scripts/setup-claude-code.sh /Users/omso/dev/solarsplit/code/SolarsplitXcode
sh ~/dev/solarsplit/code/SolarsplitXcode/KrystianPawlowskiKnowledge/scripts/setup-claude-code-personal.sh
```

The argument of the first script must be absolute, a relative path yields links that resolve from `~/.claude/rules/` and are all broken. Both scripts print a verification of every target at the end, read it rather than assume it passed.

## 5. Adding a personal rule or skill

This repo mirrors SolarsplitKnowledge: `.cursor/rules/*.md` with `.mdc` symlinks, `claude/skills-manifest.json`, generated `claude/skills/<name>/`, `scripts/`. The shared `sync-claude-skills.py` discovers this repo through its manifest because both repos share a parent folder, so no shared file has to know this repo exists.

1. Write `.cursor/rules/<name>.md` with a quoted `description` in the frontmatter. `alwaysApply: false` for a skill, `globs:` plus `paths:` for a path-scoped rule, `alwaysApply: true` only for the dispatcher.
2. `cd .cursor/rules && ln -s <name>.md <name>.mdc`, relative.
3. For a skill, add `"<name>": "<name>"` to `claude/skills-manifest.json`. Key is the skill name, value the rule file name without extension.
4. `sh scripts/setup-claude-code-personal.sh`. It links the dispatcher and the path-scoped rules into `~/.claude/rules/`, runs the shared sync that generates `SKILL.md` and the relative `rule.md`, links the skill into `~/.claude/skills/`, links the `.mdc` into the Cursor workspace root, checks the frontmatter and verifies that every link resolves to a `.md`.
5. Add a row to the routing table of the dispatcher, commit, reload Cursor, open a new Claude Code session.

Frontmatter check by hand, the one Claude Code performs silently and fatally:

```bash
ruby -ryaml -e 'YAML.safe_load(File.read(ARGV[0], encoding: "utf-8")[/\A---\n(.*?)\n---/m, 1])' .cursor/rules/<name>.md
```

Never write an absolute path of this machine in a `SKILL.md` or `BODY.md`. The generated `rule.md` link is relative for that reason, and a regenerated skill must be byte-identical on every machine.

## 6. Open items, verify before acting

| Item | Where to check |
|---|---|
| No GitHub remote for this repo yet, account to choose first | `git -C ~/dev/solarsplit/code/SolarsplitXcode/KrystianPawlowskiKnowledge remote -v` |
| Hooks not installed, sync scripts run by hand | `~/.claude/settings.json`, key `hooks` |
| `swlogs` and `ssapi` not installed | `command -v swlogs`, `ls ~/.config/swlogs ~/.config/ssapi` |
| Codex layer not generated | `ls ~/.codex/AGENTS.md ~/.agents/skills` |
