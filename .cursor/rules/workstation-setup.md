---
description: "Krystian's Mac: workspace map and which SOLARSPLIT repos are cloned, git identity, the GitHub account and how the gh CLI authenticates git, what Claude Code shells can and cannot reach (no ~/.ssh), the Android and Xcode toolchains, the Claude Code and Cursor context layers installed here and how to reinstall them, how to add a personal rule or skill. Load for any task about paths, git or GitHub access, CLI tooling, or the context setup on this machine."
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

Verified 09.09.2026 unless stated otherwise. The machine was re-set-up on 07.09.2026, which replaced the layout the previous version of this file described. macOS user `solarsplit`, macOS 26.6.2 (Darwin 25.6), Apple silicon. System Python 3.9.6, Ruby 2.6.10 (used by the frontmatter checks), `jq` 1.7.1, Homebrew in `/opt/homebrew`. Claude Code runs through the desktop app. Cursor is not in `/Applications` at this date, the Cursor links below are kept correct for when it is installed.

## 1. Workspace map

Everything SOLARSPLIT lives under `~/solarsplit-dev/`. There is no `~/Code/GitHub`, the path the shared rules use, and there is no intermediate `SolarsplitXcode/` folder any more: every repo is cloned flat in `code/`.

| Path | What |
|---|---|
| `~/solarsplit-dev` | Root opened in Claude Code and Cursor. Not a git repo. Carries `CLAUDE.md`, `.claude/settings.local.json` and `.cursor/rules/`, one `.mdc` symlink per rule, shared and personal |
| `~/solarsplit-dev/code` | Flat parent of every repo. This is the folder to pass, absolute, to the shared setup script, and the folder the sync scripts deduce from their own location |
| `~/solarsplit-dev/code/SolarsplitAndroidApp` | Android app. Its rule `solarsplit-android` lives in SolarsplitKnowledge like the iOS ones since 09.09.2026, the repo carries no rule of its own |
| `~/solarsplit-dev/code/SolarsplitWorkspace.xcworkspace` | Xcode workspace over the Swift repos |
| `~/solarsplit-dev/old/solarsplitWebFrontend[old]` | Former repo of the personal GitHub account, parked, not in use |

Cloned in `code/` on 09.09.2026: `SolarsplitKnowledge`, `KrystianPawlowskiKnowledge`, `SolarsplitWeb`, `SolarsplitWebClient`, `SOLARSPLITiOS`, `SolarsplitShared`, `SolarsplitAndroidApp`, `SolarsplitCapacitorShell`, `Clupi`. Everything else in the shared workspace map (`solarsplit-web-landing`, the `Helvet*` and `Solarsplit*` Swift packages, `SOLARSPLITRoofMetrics`, `SOLARSPLIT_COMMUNITY`, `SOLARSPLIT_MONITORING`, `SolarsplitMedia`, `SolarsplitPrivate`, Wilfried's personal repos) is not on this machine. Re-check with `ls ~/solarsplit-dev/code`.

## 2. Git identity

`~/.gitconfig` sets `krystian-pawlowski`, k.pawlowski@solarsplit.com, for every repo on the machine. There is no `includeIf`, no `~/.gitconfig-solarsplit` and no personal-account identity any more. The git-lfs filter is configured globally. Check inside a repo with `git config user.email`.

## 3. GitHub access, through the gh CLI

Set up 09.09.2026.

- **Account.** `krystian-pawlowski`, the work account, member of the `SOLARSPLIT` and `HelveticApp` organisations with push rights. The personal account `omsomso` is not configured on this machine.
- **CLI.** `gh` 2.100.0 from Homebrew, logged in with `gh auth login` over HTTPS, scopes `repo`, `workflow`, `read:org` and `gist`. It keeps its own token. Nothing is exported in the shell, `GH_TOKEN` and `GITHUB_TOKEN` are unset, and no hand-managed token exists any more.
- **Git over HTTPS.** Remotes stay on `https://github.com/...`. The login also handed git the credential, served through the `osxkeychain` helper that Xcode's system git config declares, nothing to set up per repo. `printf 'protocol=https\nhost=github.com\n' | git credential fill | grep username` shows which identity git resolves.
- **From Claude Code shells.** `gh` works, sandbox included: `gh auth status`, `gh api`, `gh pr list`, `gh repo view` and `git push --dry-run` all verified on 09.09.2026. The Go dialer failure of the previous machine does not reproduce here.
- **SSH is not an option from Claude Code.** macOS denies the desktop app any read of `~/.ssh`, even with the sandbox disabled, so the SSH key and `known_hosts` are unreachable and every SSH remote fails at host key verification. Keep remotes on HTTPS.
- **Re-login or rotation.** `gh auth refresh` or `gh auth login`, in a terminal, by hand: the browser flow cannot run from an agent session, and an agent never types a token.

## 4. Toolchains

- **Xcode** in `/Applications`, its bundled git is the system git and carries the `osxkeychain` credential helper.
- **Android.** No system JDK, `/usr/libexec/java_home` finds nothing. Android Studio 2026.1 bundles JBR 25 at `/Applications/Android Studio.app/Contents/jbr/Contents/Home`. The SDK is `~/Library/Android/sdk`, declared in `SolarsplitAndroid/local.properties` (gitignored). For CLI Gradle in `SolarsplitAndroidApp/SolarsplitAndroid/`, export `JAVA_HOME` to that JBR and `ANDROID_HOME` to the SDK; Gradle 9.1 then provisions Temurin 17 into `~/.gradle/jdks/` through foojay-resolver-convention 1.0.0. Once the caches are warm, `./gradlew <task> --offline --console=plain` runs inside the Claude Code sandbox, a manifest merge or a module compile takes about 25 s.

## 5. Context layers installed on this machine

The same rules feed Claude Code and Cursor, and could feed Codex, as `agent-context-mechanics` describes. State on 09.09.2026, after the reinstall of that day.

**Claude Code, `~/.claude/`**

| Where | Points to | Loads |
|---|---|---|
| `rules/solarsplit-core.md` | SolarsplitKnowledge | every session |
| `rules/personal-dispatcher.md` | this repo | every session |
| `rules/swift-gotchas-index.md`, `fluent-migrations.md`, `simulator-navigation.md`, `solarsplit-android.md` | SolarsplitKnowledge | on matching files only |
| `skills/<name>`, the shared ones plus `workstation-setup` | `claude/skills/<name>` of each repo | on trigger or `/name` |
| `CLAUDE.md` | plain file written by the shared setup script | every session |

`~/solarsplit-dev/CLAUDE.md` loads on top of that in every session opened under the workspace root. Cap on the permanent layer: 50 KB cumulated. The personal setup script prints the current figure at the end of every run, the reference measurement is the script of `agent-context-mechanics` section 8, to run from `code/`.

**Hooks: none.** `~/.claude/settings.json` has no `hooks` key, so the shared guards (`hook-sync-skills-guard.sh`, `hook-journal-guard.py`, `hook-outbound-guard.py`) are not active here. After editing a rule, run the sync by hand, or the personal setup script, which does it.

**Cursor, workspace root `~/solarsplit-dev/.cursor/rules/`.** One `.mdc` symlink per rule, shared and personal. Neither setup script links the shared rules for Cursor, the loop is in `~/solarsplit-dev/CLAUDE.md` and in the README of SolarsplitKnowledge. Cursor reads the frontmatter at window launch only, reload the window and open a new conversation after any change.

**Codex.** Not installed, no `codex` binary and no `~/.codex`. `python3 SolarsplitKnowledge/scripts/sync-codex-layer.py --write` would produce `AGENTS.md`, `hooks.json` and the skill links from the same sources, personal dispatcher included, since it deduces the permanent layer from `~/.claude/rules/`.

**Shared CLIs not installed here.** `swlogs` is not on the PATH and `~/.config/swlogs/` does not exist, `~/.local/bin` does not exist either, and there is no `~/.config/ssapi`. The skills `solarsplit-ops` and `solarsplit-api` describe their installation when needed.

### Reinstall or repair, idempotent

```bash
sh ~/solarsplit-dev/code/SolarsplitKnowledge/scripts/setup-claude-code.sh /Users/solarsplit/solarsplit-dev/code
sh ~/solarsplit-dev/code/KrystianPawlowskiKnowledge/scripts/setup-claude-code-personal.sh
```

The argument of the first script must be absolute, a relative path yields links that resolve from `~/.claude/rules/` and are all broken. Both scripts print a verification of every target at the end, read it rather than assume it passed.

## 6. Adding a personal rule or skill

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

## 7. Open items, verify before acting

| Item | Where to check |
|---|---|
| No GitHub remote for this repo yet, account to choose first; `gh repo create` works from here now | `git -C ~/solarsplit-dev/code/KrystianPawlowskiKnowledge remote -v` |
| Hooks not installed, sync scripts run by hand | `~/.claude/settings.json`, key `hooks` |
| `swlogs` and `ssapi` not installed | `command -v swlogs`, `ls ~/.config/swlogs ~/.config/ssapi` |
| Codex not installed, layer not generated | `command -v codex`, `ls ~/.codex` |
| Cursor not installed, `.cursor/rules/` links unused until then | `ls /Applications/Cursor.app` |
