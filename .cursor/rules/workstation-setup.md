---
description: "Krystian's Mac: workspace map and which SOLARSPLIT repos are cloned, git identity, the GitHub account and how the gh CLI authenticates git, what Claude Code shells can and cannot reach, SSH and the GitHub key, the Android and Xcode toolchains, the Claude Code, Cursor and Codex context layers installed here and how to reinstall them, how to add a personal rule or skill. Load for any task about paths, git or GitHub access, CLI tooling, or the context setup on this machine."
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
| `~/solarsplit-dev/code/KrystianPawlowskiSessionLog` | Session journal, personal tier, created locally on 10.09.2026, no remote yet. One file per session under `sessions/`, conventions in its README. Low risk in the sense of `solarsplit-core` section 3: no auto-deploy, a single reader. The shared journal of SolarsplitKnowledge is not written from this machine, the personal dispatcher carries the rule |
| `~/solarsplit-dev/code/SolarsplitCapacitorShell` | Capacitor 8 shell opening web.solarsplit.com in a native Android app, Krystian's personal test of whether two mobile shells over the web app could replace the two native apps and the web client. Not an official SOLARSPLIT repo: no remote, not in the risk lists of `solarsplit-core` and not to be added there, personal tier in practice, commit freely and push nothing unless asked. Its build setup, Gradle 9.6.0 and AGP 9.4.0 on the bundled JBR 25 since 11.09.2026, is in its README |
| `~/solarsplit-dev/old/solarsplitWebFrontend[old]` | Former repo of the personal GitHub account, parked, not in use |

Cloned in `code/` on 09.09.2026: `SolarsplitKnowledge`, `KrystianPawlowskiKnowledge`, `SolarsplitWeb`, `SolarsplitWebClient`, `SOLARSPLITiOS`, `SolarsplitShared`, `SolarsplitAndroidApp`, `SolarsplitCapacitorShell`, `Clupi`. `KrystianPawlowskiSessionLog` was created locally on 10.09.2026, it is not a clone. Everything else in the shared workspace map (`solarsplit-web-landing`, the `Helvet*` and `Solarsplit*` Swift packages, `SOLARSPLITRoofMetrics`, `SOLARSPLIT_COMMUNITY`, `SOLARSPLIT_MONITORING`, `SolarsplitMedia`, `SolarsplitPrivate`, Wilfried's personal repos) is not on this machine. Re-check with `ls ~/solarsplit-dev/code`.

## 2. Git identity

`~/.gitconfig` sets `krystian-pawlowski`, k.pawlowski@solarsplit.com, for every repo on the machine. There is no `includeIf`, no `~/.gitconfig-solarsplit` and no personal-account identity any more. The git-lfs filter is configured globally. Check inside a repo with `git config user.email`.

## 3. GitHub access, through the gh CLI

Set up 09.09.2026.

- **Account.** `krystian-pawlowski`, the work account, member of the `SOLARSPLIT` and `HelveticApp` organisations with push rights. The personal account `omsomso` is not configured on this machine.
- **CLI.** `gh` 2.100.0 from Homebrew, logged in with `gh auth login` over HTTPS, scopes `repo`, `workflow`, `read:org` and `gist`. It keeps its own token. Nothing is exported in the shell, `GH_TOKEN` and `GITHUB_TOKEN` are unset, and no hand-managed token exists any more.
- **Git over HTTPS.** Remotes stay on `https://github.com/...`. The login also handed git the credential, served through the `osxkeychain` helper that Xcode's system git config declares, nothing to set up per repo. `printf 'protocol=https\nhost=github.com\n' | git credential fill | grep username` shows which identity git resolves.
- **From Claude Code shells.** `gh` works, sandbox included: `gh auth status`, `gh api`, `gh pr list`, `gh repo view` and `git push --dry-run` all verified on 09.09.2026. The Go dialer failure of the previous machine does not reproduce here.
- **SSH works from Claude Code since 14.09.2026, HTTPS stays the default for remotes.** The earlier finding that `~/.ssh` was unreachable came from a symlink of `~/.ssh` into `~/Documents/.ssh` made on 08.09.2026, and macOS blocks Documents for the desktop app even with the sandbox off. Since the folder is a real `~/.ssh` again (14.09.2026 14:45), `ssh -T git@github.com` answers with the work account from a sandboxed shell. The only GitHub key is `~/.ssh/id_ed25519`, ed25519 in OpenSSH format, passphrase-protected, registered on `krystian-pawlowski`. `~/.ssh/config` has a `Host github.com` block with `AddKeysToAgent yes`, `UseKeychain yes` and that identity, so the key loads on demand once its passphrase is in the keychain, which needs `ssh-add --apple-use-keychain ~/.ssh/id_ed25519` run once by hand. Until then the agent is empty after every reboot and every SSH use fails with `Permission denied (publickey)`. Check with `ssh-add -l`.
- **Re-login or rotation.** `gh auth refresh` or `gh auth login`, in a terminal, by hand: the browser flow cannot run from an agent session, and an agent never types a token.

## 4. Toolchains

- **Xcode** in `/Applications`, its bundled git is the system git and carries the `osxkeychain` credential helper.
- **Xcode and SSH packages.** `SolarsplitWorkspace.xcworkspace` merges SolarsplitWeb, SOLARSPLITiOS and SolarsplitShared into one package graph, and SOLARSPLITiOS declares SolarsplitAIPackage and SolarsplitInstallerMatchmakingPackage with `git@github.com:` URLs, so their mirrors in DerivedData fetch over SSH. Xcode's default package resolution uses its own SSH stack, libssh2 plus the Xcode SSH Authentication Agent, which cannot load an OpenSSH-format key and fails with `Server SSH Fingerprint Failed to Verify` then `Permission denied (publickey)`, which leaves the SolarsplitWeb scheme without any run destination. Since 14.09.2026 `defaults write com.apple.dt.Xcode IDEPackageSupportUseBuiltinSCM -bool YES` makes Xcode use the system git and ssh, hence the agent, for packages, verified by a full 93-package resolve in the IDE. Resolution logs: `~/Library/Developer/Xcode/DerivedData/SolarsplitWorkspace-*/Logs/Package/*.xcactivitylog`, gzip files, read them before suspecting platforms. A full resolve of this workspace takes about nine minutes. The GitHub account in Settings > Accounts keeps its key path in `com.apple.dt.Xcode.plist` under `IDESourceControlHostAccounts_10`, a moved key shows as none at every launch and re-picking it in the popup does not update the record, fix the path or remove and re-add the account.
- **Android.** No system JDK, `/usr/libexec/java_home` finds nothing. Android Studio 2026.1 bundles JBR 25 at `/Applications/Android Studio.app/Contents/jbr/Contents/Home`. The SDK is `~/Library/Android/sdk`, declared in `SolarsplitAndroid/local.properties` (gitignored). For CLI Gradle in `SolarsplitAndroidApp/SolarsplitAndroid/`, export `JAVA_HOME` to that JBR and `ANDROID_HOME` to the SDK. On 11.09.2026 the wrapper is Gradle 9.6.0 with AGP 9.4.0, and `gradle/gradle-daemon-jvm.properties` pins the daemon JVM to JetBrains 25 with foojay download URLs, so the bundled JBR is the one Gradle runs on. `~/.gradle/jdks/` also holds a Temurin 17 provisioned on 08.09.2026. Once the caches are warm, `./gradlew <task> --offline --console=plain` runs inside the Claude Code sandbox, a manifest merge or a module compile takes about 25 s.
- **Android emulator, on the host Mac, not here.** Verified 11.09.2026. This Mac is itself a virtual machine, `sysctl -n machdep.cpu.brand_string` says `Apple M2 (Virtual)`, 8 GB of RAM, and `sysctl kern.hv_support` is 0, so no emulator can run in it and `~/.android/avd` is empty. The emulator runs on the physical Mac that hosts this VM, reached as the ssh alias `android-host`, which is 192.168.64.1, the VM's default gateway (`netstat -rn -f inet | grep default`). A tunnel started outside Claude Code, `ssh -fNT -L 127.0.0.1:5037:127.0.0.1:5037 android-host`, forwards the host's adb server into this VM, so no adb server runs here and every `adb` command talks to the host's one: `adb devices` shows `emulator-5554`, AVD `Pixel_10a` on the API 37.1 Google Play arm64 16k image with 4 GB of guest RAM. `adb shell`, `adb install`, `adb logcat` and `adb exec-out screencap` all work from Claude Code shells, sandbox included. `adb emu` does not, the console port 5554 is not forwarded. The emulator's own logs and the macOS crash reports of its process are on the host, this VM never sees them. A second tunnel of the same shape, alias `minio-s3-host`, forwards ports 9000 and 9001, its purpose is not established in this file. Check both with `pgrep -fl "ssh -fNT"`.

  The emulator must run with hardware graphics, `-gpu host`. With software rendering, the guest reported `ANGLE ... SwiftShader` in `adb shell dumpsys SurfaceFlinger | grep ^GLES`, every page of the web client took seconds per frame in the Capacitor shell's WebView, and expanding a section of a project detail page killed the emulator process on the host every time, with nothing in the guest log but main-thread jank. Since Krystian relaunched it with `-gpu host` on 11.09.2026 the same line reads `Android Emulator OpenGL ES Translator (Apple M2), OpenGL ES 3.0 (4.1 Metal - 90.5)`, the crash is gone and the app is faster. That grep is the check.

## 5. Context layers installed on this machine

The same rules feed Claude Code, Cursor and, since 09.09.2026, Codex, as `agent-context-mechanics` describes. State on 10.09.2026.

**Claude Code, `~/.claude/`**

| Where | Points to | Loads |
|---|---|---|
| `rules/solarsplit-core.md` | SolarsplitKnowledge | every session |
| `rules/personal-dispatcher.md` | this repo | every session |
| `rules/swift-gotchas-index.md`, `fluent-migrations.md`, `simulator-navigation.md`, `solarsplit-android.md` | SolarsplitKnowledge | on matching files only |
| `skills/<name>`, the shared ones plus `workstation-setup` | `claude/skills/<name>` of each repo | on trigger or `/name` |
| `CLAUDE.md` | plain file written by the shared setup script | every session |

`~/solarsplit-dev/CLAUDE.md` loads on top of that in every session opened under the workspace root. Cap on the permanent layer: 50 KB cumulated. The personal setup script prints the current figure at the end of every run, the reference measurement is the script of `agent-context-mechanics` section 8, to run from `code/`.

**Hooks in Claude Code: none.** `~/.claude/settings.json` has no `hooks` key, so the shared guards (`hook-sync-skills-guard.sh`, `hook-journal-guard.py`, `hook-outbound-guard.py`) are not active in Claude Code sessions. After editing a rule, run the syncs by hand, or the personal setup script, which runs the Claude Code sync but not the Codex one. The same guards are active in Codex sessions through `~/.codex/hooks.json`, see below. Nothing on this machine redirects or captures shell output, checked on 10.09.2026 across settings, hooks, shell startup files and the session transcripts of both tools.

**Cursor, workspace root `~/solarsplit-dev/.cursor/rules/`.** One `.mdc` symlink per rule, shared and personal. Neither setup script links the shared rules for Cursor, the loop is in `~/solarsplit-dev/CLAUDE.md` and in the README of SolarsplitKnowledge. Cursor reads the frontmatter at window launch only, reload the window and open a new conversation after any change.

**Codex, `~/.codex/` and `~/.agents/skills/`.** Installed on 09.09.2026 with the ChatGPT desktop app (26.903.61454), which bundles Codex CLI 0.153.4 at `/Applications/ChatGPT.app/Contents/Resources/codex`. Nothing on the PATH, so `command -v codex` fails and that is expected. The layer was generated the same day by `python3 ~/solarsplit-dev/code/SolarsplitKnowledge/scripts/sync-codex-layer.py --write`, three derived artifacts never edited by hand: `~/.codex/AGENTS.md` carries the permanent layer deduced from `~/.claude/rules/`, personal dispatcher included, `~/.agents/skills/<name>` links every skill of both manifests, `workstation-setup` included, and `~/.codex/hooks.json` runs the shared guards through `codex-hook-adapter.py` on PreToolUse, UserPromptSubmit, SessionStart, PostToolUse and Stop. The personal setup script does not regenerate them, so after any change to a permanent rule or to a manifest run the Codex sync by hand, without `--write` first, it reports the drift and exits 2 when there is one. `~/.codex/config.toml` belongs to the app, trust level `trusted` on `~/solarsplit-dev`, no SOLARSPLIT content in it.

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
4. `sh scripts/setup-claude-code-personal.sh`. It links the dispatcher and the path-scoped rules into `~/.claude/rules/`, runs the shared sync that generates `SKILL.md` and the relative `rule.md`, links the skill into `~/.claude/skills/`, links the `.mdc` into the Cursor workspace root, checks the frontmatter and verifies that every link resolves to a `.md`. Then `python3 ~/solarsplit-dev/code/SolarsplitKnowledge/scripts/sync-codex-layer.py --write` for the `~/.agents/skills/` link, the personal script does not run it.
5. Add a row to the routing table of the dispatcher, commit, reload Cursor, open a new Claude Code session.

Frontmatter check by hand, the one Claude Code performs silently and fatally:

```bash
ruby -ryaml -e 'YAML.safe_load(File.read(ARGV[0], encoding: "utf-8")[/\A---\n(.*?)\n---/m, 1])' .cursor/rules/<name>.md
```

Never write an absolute path of this machine in a `SKILL.md` or `BODY.md`. The generated `rule.md` link is relative for that reason, and a regenerated skill must be byte-identical on every machine.

## 7. Open items, verify before acting

| Item | Where to check |
|---|---|
| This repo has its `origin` on the work account over HTTPS, `KrystianPawlowskiSessionLog` has no GitHub remote yet, `gh repo create` works from here | `git -C ~/solarsplit-dev/code/KrystianPawlowskiSessionLog remote -v` |
| Claude Code hooks not installed, Claude sync by the personal script, Codex sync by hand | `~/.claude/settings.json`, key `hooks`, and `python3 ~/solarsplit-dev/code/SolarsplitKnowledge/scripts/sync-codex-layer.py` |
| `swlogs` and `ssapi` not installed | `command -v swlogs`, `ls ~/.config/swlogs ~/.config/ssapi` |
| Personal setup script does not run `sync-codex-layer.py`, to add or keep by hand | `grep -n codex scripts/setup-claude-code-personal.sh` |
| Codex PostToolUse and Stop hooks run the shared journal guard, behaviour with the personal journal repo not yet observed in a Codex session | `~/.codex/hooks.json`, `SolarsplitKnowledge/scripts/hook-journal-guard.py` |
| Cursor not installed, `.cursor/rules/` links unused until then | `ls /Applications/Cursor.app` |
| Passphrase of `~/.ssh/id_ed25519` not in the keychain yet, the agent is empty after each reboot until `ssh-add --apple-use-keychain ~/.ssh/id_ed25519` is run once | `ssh-add -l` after a reboot |
| The two `git@` package URLs of SOLARSPLITiOS still force SSH in the workspace, switching them to HTTPS is the durable fix, high-risk repo, push on request only | `grep -n 'git@github.com' ~/solarsplit-dev/code/SOLARSPLITiOS/SOLARSPLITiOS.xcodeproj/project.pbxproj` |
| AppleScript to Xcode from a Claude Code shell answered -1743 not authorised on 14.09.2026 after one prompt, a graceful quit of Xcode from a shell needs the Automation permission | `osascript -e 'tell application "Xcode" to get name'`, System Settings > Privacy & Security > Automation |
| How the two ssh tunnels, `android-host` and `minio-s3-host`, are started and whether they survive a reboot. Checked 11.09.2026: no launch agent and no shell startup file mentions them, both processes are daemonized under PID 1 and were started within one second of each other, which points to a script run by hand | `pgrep -fl "ssh -fNT"`, `ls ~/Library/LaunchAgents`, `grep -n android-host ~/.zshrc ~/.zprofile` |
