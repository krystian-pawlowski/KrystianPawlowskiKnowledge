---
description: "SOLARSPLIT Workbench et son CLI wb pour les agents : builds et tests en file d'attente pour ne pas saturer la machine, worktree prêt à builder avec sa base et ses ports, serveur par worktree, ce qui tourne sur le Mac et quelle session l'a lancé, configuration réelle de chaque build, sujets qui regroupent les branches d'un même travail dans plusieurs repos. Charger au début de tout travail qui créera une branche ou buildera : la session dit d'abord à quel sujet son travail appartient (wb topic use, wb topic new, wb topic use --none), sinon wb et le hook refusent. Aussi avant tout swift build, swift test, xcodebuild, gradlew ou npm run build dans un repo produit, avant de créer ou de supprimer un worktree, et pour savoir ce que font les autres agents."
alwaysApply: false
---

<!--
PERSONAL COPY, temporary. The team version of this resource sits on branch
docs/workbench-wb-261001 of SolarsplitKnowledge, unmerged on purpose while Krystian is the only
one with the Workbench (decision of 01.10.2026). This copy activates it on this Mac only.
Keep everything below this paragraph identical to the branch version. When the branch merges,
delete this file, its .mdc link, its manifest entry and its dispatcher row in one commit, or the
two skills clash by name.

Créé le 01.10.2026 : plusieurs sessions d'agents lançaient leurs builds en même temps sur la VM
de Krystian, charge moyenne au-delà de 200 sur quatre cœurs, et rejouaient les mêmes pièges de
worktree. Krystian veut que le développement passe par la Workbench, lisible par les
développeurs comme par les agents, et que la coordination soit prévisible.

CROSS-REFERENCE:
- SolarsplitWorkbench/README.md -> l'app, le panneau Activity, wb en détail
- SolarsplitWorkbench/scripts/wb.py -> le CLI
- SolarsplitWorkbench/scripts/wb-hook.py -> le hook d'état des sessions
- swift-vapor-patterns.md -> gotchas #28, #123, #137, #138 et #157, que wb worktree create évite
-->

# SOLARSPLIT Workbench et `wb`, pour les agents

La Workbench est l'app macOS qui build et lance le backend, les apps et le web. `wb` en est la face pour les terminaux et les agents : les mêmes scripts, plus une file d'attente, un registre des runs et des worktrees prêts à l'emploi. Le panneau **Activity** de l'app montre tout ce que `wb` enregistre.

## 1. Quand s'en servir

- **Toute build ou tout test d'un repo produit** : `wb build <app>`, `wb test backend`, plutôt que `swift build`, `swift test`, `xcodebuild`, `./gradlew` ou `npm run build`. Sur une machine partagée par plusieurs sessions, c'est ce qui évite les builds empilées.
- **Avant de créer ou de supprimer un worktree** : `wb worktree create`, `wb worktree remove`.
- **Pour un serveur dans un worktree** : `wb run backend|webclient|landing`, `wb stop …`.
- **Pour savoir ce qui tourne, où, et quelle session l'a lancé** : `wb ps`.
- **Pour un travail qui touche plusieurs repos, ou qui en prolonge un** : `wb topic`, section 6.
- **Non** pour les tests d'un package Swift seul (SolarsplitShared, Helvet*) : `swift test` dans le package, après un `wb ps` pour ne pas tomber au milieu d'une build lourde.
- **Non** pour l'app iOS ou Android lancée sur le simulateur ou l'émulateur : il n'y en a qu'un par machine, `run-ios.py` et `run-android.py` restent le chemin, `wb build ios|android` pour seulement compiler.

## 2. Le CLI

Pas sur le PATH par défaut : `python3 <dossier des repos>/SolarsplitWorkbench/scripts/wb.py <commande>`, soit `~/Code/GitHub/…` chez Wilfried, `~/solarsplit-dev/code/…` chez Krystian. `--help` sur chaque commande.

| Commande | Fait |
|---|---|
| `wb build backend\|ios\|android\|webclient\|landing\|workbench` | build du checkout du dossier courant, sinon `--worktree DIR`, sinon le checkout principal. `workbench` : la Workbench elle-même, `--release` pour celle que `make-app.sh` empaquette, qui passe aussi par là |
| `wb run workbench [--harness DIR]`, `wb stop workbench` | la Workbench d'un checkout buildée à son tour puis ouverte, à la place de celle qu'il avait ouverte, arrêtée par le pid enregistré. Jamais un `kill` par nom : il atteint aussi le compilateur d'une autre session |
| `wb test backend [--filter REGEX] [--skip-build]` | les suites XCTest, résultats par test |
| `wb run backend\|webclient\|landing`, `wb stop …` | serveur du checkout sur son port, le backend buildé d'abord dans la file |
| `wb worktree create <app\|repo> <branche>` | worktree prêt à builder, voir section 5 |
| `wb worktree remove <worktree>`, `wb worktree list` | suppression gardée, liste avec base et ports |
| `wb ps`, `wb runs`, `wb logs <run>` | ce qui tourne et la file, sous chaque session de l'app Claude le lien qui l'y ouvre, les runs récents, la sortie entière d'un run |
| `wb config [--slots N\|auto]` | combien de builds à la fois |
| `wb topic list\|new\|use\|show\|add` | les sujets, le travail d'un thème dans plusieurs repos, voir section 6 |
| `wb topic plan [sujet]` | ses vérifications et ce qui reste à fusionner dans l'ordre, ce qui retient chaque branche, `--json` pour un agent |
| `wb topic tidy <sujet>` | supprime sur ce Mac ses branches fusionnées extraites nulle part, gardées au sujet comme fusionnées, origin intact |
| `wb topic describe <sujet>` | une ou deux phrases sur le sujet par Codex ou Claude Code, gardées tant que ses branches ne changent pas, l'app les demande seule |
| `wb topic setup\|build\|run\|stop\|clean <sujet>` | ses worktrees liés dans son dossier, buildés dans l'ordre, servis ensemble, retirés une fois poussés |

Les options que `wb` ne connaît pas vont au script : `wb build backend --tests` (`swift build --build-tests`), `wb build ios --env staging`, `--clean`, `--shared <dossier>`.

Le backend se builde par `xcodebuild` par défaut depuis le 02.10.2026 : il passe l'arrêt sur `_NumericsShims` de `swift build` (gotcha #28), et le script remet `Package.resolved` comme avant la build quand Xcode n'a fait qu'en retirer le pin SolarsplitShared et le reformater. `--builder swift` pour SwiftPM. Les builds de tests restent sur `swift build`.

## 3. La file d'attente

- Une build ou un test prend une place libre, dans l'ordre des demandes, et attend aussi les builds lancées hors de la file (Xcode, un agent qui lance `swift build` lui-même). L'attente dit ce qu'elle attend et à quelle session c'est.
- **Les scripts `run-*.py` rejoignent la file d'eux-mêmes** dès qu'ils compilent : les boutons Start, Run et Build de l'app, les tests du backend, un script lancé dans un terminal ou par un agent attendent leur tour comme `wb`, enregistrés comme ses runs. `wb` leur passe `WB_RUN` pour dire qu'il tient déjà le tour. Un lint part tout de suite.
- Nombre de places : réglage **Builds at a time** de l'app ou `wb config --slots N|auto`, `WB_SLOTS` pour une commande. Automatique : une place par quatre cœurs et par 8 Go de mémoire, le plus petit des deux, de 1 à 4. Une place sur une VM à 4 cœurs et 10 Go, trois sur un MacBook Pro à 12 cœurs et 36 Go.
- **Lancer `wb`, ou un script `run-*.py` qui builde, en arrière-plan** (Claude Code : `run_in_background`) : une attente dépasse facilement le délai d'un appel d'outil. L'arrêter (Ctrl-C, SIGTERM) sort proprement la build de la file, ou l'arrête si elle tourne.
- `--no-wait` saute la file, `WB_NO_WAIT=1` pour un script, seulement à la demande explicite de l'utilisateur. Dans l'app, **Start now** fait de même, dans l'en-tête d'un service en attente et sur une ligne en file du panneau Activity.
- Chaque panneau de service de l'app montre sous ses options ce qui tourne ailleurs sur son repo : les builds, tests et serveurs des autres worktrees ou des agents, et les builds en file.

## 4. Sortie pour un agent

- Les erreurs seulement, comme les scripts les filtrent, `--output warnings|all` pour plus, `wb logs <run>` pour tout.
- `--json` : la dernière ligne est un résumé, état, durée, erreurs avec fichier et ligne, ou comptes et échecs des tests, et la configuration du run.
- Code de sortie : celui de la build ou des tests, 0 si réussi, 130 si interrompu, 2 pour une erreur d'usage de `wb`.

## 5. Worktrees

`wb worktree create` met le checkout à côté des autres (`$WB_WORKTREES`, sinon un dossier `worktrees` à côté du dossier des repos), sur une branche neuve depuis `origin/develop` (`origin/main` pour SolarsplitShared, qui fusionne sur main) ou `--from`, **sans upstream** jusqu'au premier push, pour qu'un `git push` nu ne vise jamais `develop`. Il copie depuis le checkout principal les fichiers ignorés dont une build a besoin, seulement là où git les ignore aussi dans le worktree, puisqu'ils portent des secrets : `.env.development` et `.env.testing` du backend, `Configurations/` d'iOS, `local.properties`, `google-services.json` et `.env` d'Android, `.env` du WebClient.

- **Backend : une base à lui**, `ss_wt_<dossier>`, copie de la base de développement par `pg_dump | psql`, écrite dans le `.env.development` du worktree (gotcha #137). Les migrations et les suites de la branche ne touchent jamais la base partagée. `--shared-database` pour s'en passer. Une copie de données réelles (`ss_clone_*`) est refusée comme source, ses fusibles sortants vont par le nom.
- **Ports à lui** pour `wb run` : 8081, 5174, 4322 et au-delà. `wb run webclient --backend <worktree>` pointe le proxy du WebClient sur le backend de ce worktree.
- `wb worktree remove` refuse un worktree avec des modifications, des commits sur aucune branche distante ou quelque chose qui y tourne, sauf `--force`, supprime la base qu'il a créée, puis `git worktree remove` emporte les dossiers de build. La branche reste.
- Ne jamais copier un `.build` d'un checkout à l'autre (gotcha #28) : le worktree se builde proprement, une première build backend prend une vingtaine de minutes sur une VM à 4 cœurs, une build incrémentale une minute.

## 6. Sujets

Un sujet regroupe le travail d'un même thème dans plusieurs repos, une fonctionnalité, un correctif ou un simple changement : les branches du backend, de Shared, du WebClient et des apps qui vont ensemble, même quand leurs noms diffèrent, plusieurs par repo, les fusionnées gardées comme historique. Le panneau Topics de l'app les montre avec, pour chaque branche, son worktree, sa pull request et les sessions qui y travaillent, quel que soit l'agent.

- **Le sujet d'abord, avant tout travail** : une session de Claude Code, Codex, Cursor ou VS Code dit à quel sujet son travail appartient avant de créer une branche ou un worktree, de builder, tester ou servir : `wb topic use <sujet>` pour un sujet existant (`wb topic list`), `wb topic new "<Nom lisible>" --task "<la demande, en une phrase>"` pour un nouveau, `wb topic use --none` pour un travail hors sujet. Sinon `wb` refuse (code 3) et le hook de la Workbench refuse `git worktree add`, `git checkout -b` et `git switch -c`, chacun en donnant ces trois commandes et la liste des sujets. Demander à la personne en cas de doute. Une session lancée dans le dossier d'un sujet, `worktrees/topics/<sujet>/` (ce que fait Start work dans le panneau Topics), ou avec `WB_TOPIC`, a déjà dit le sien. Une session qui builde une branche déjà classée rejoint son sujet, une branche de tronc n'en demande pas. Plus de sujet deviné d'après le titre d'une session. `wb topic merge` réunit deux sujets voisins. La liste donne chaque sujet avec ses repos et sa dernière activité, le plus récent d'abord : si plusieurs peuvent convenir, même repo ou sujet proche, demander à la personne plutôt que choisir ou ouvrir un sujet de plus pour le même travail. Un sujet archivé depuis ne compte plus, le hook le dit à l'invite suivante : demander alors s'il faut le ressortir (`wb topic archive <sujet> --undo`), jamais en ouvrir un second. La personne peut déplacer une session vers un autre sujet depuis la Workbench, ses branches avec elle (`wb topic use <sujet> --session claude:<id> --branches`), ou fusionner son sujet dans un autre, et le hook le dit aussi à l'invite suivante.
- **Une demande sans rapport, dans la même session** : quand la personne demande autre chose que le sujet de la session, `wb topic new "<titre>" --task "<la demande>"` avant de créer une branche : la session travaille alors sur ce nouveau sujet, ses branches d'avant restent dans l'ancien. Pour une branche déjà classée à tort : `wb topic add <sujet> <repo> <branche> --move`. wb et le hook le rappellent chaque fois qu'une branche rejoint le sujet de la session.
- **Des problèmes trouvés, pour plus tard** : `wb topic new "<titre>" --todo --task "<la tâche, comme un prompt>"` les met dans la liste à faire du panneau Topics, d'où ils se lancent, ensemble ou en parallèle. `wb topic start <sujet>` en démarre un et donne son dossier.
- **Ensuite, rien à faire** : chaque branche que la session crée par `wb worktree create`, builde, teste ou sert par `wb` rejoint le sujet seule, et chaque run porte son sujet. Un worktree créé pour le sujet arrive dans son dossier, nommé comme son repo. Une branche faite par `git checkout -b` ou `git switch -c` dans une session Claude Code sur un sujet le rejoint aussi, par le hook. En rattrapage, wb lit la conversation des sessions du sujet (transcript Claude Code, rollout Codex) pour les branches faites par git, poussées par `git push` ou dont la pull request est ouverte par `gh pr create`. Une branche faite autrement, par l'éditeur ou sans push : `wb topic add` depuis son checkout, ou `wb topic add <repo> <branche>`. Une branche retirée par `wb topic remove` n'y revient pas seule. Les branches de tronc et de release n'y entrent jamais.
- **Pour un travail qui touche plusieurs repos dès le départ** : `wb topic setup <sujet> shared backend webclient` crée un worktree par repo dans le dossier du sujet, `worktrees/topics/<sujet>/`, chacun nommé comme son repo, le backend sur sa propre base. Ils sont liés : le backend et iOS buildent contre le Shared du sujet, `wb run webclient` vise son backend, quel que soit celui qui lance la build. `wb topic build <sujet>` builde le backend puis les clients, chacun à son tour dans la file, `wb topic run <sujet>` sert le backend puis le web client, `--clean` pour builder le backend depuis un dossier vide quand `swift build` bute sur `_NumericsShims` (gotcha #28), `wb topic stop` les arrête. Un `--shared` ou un `--backend` donné en ligne de commande l'emporte. Avec xcodebuild, le builder par défaut, le lien au Shared passe par un workspace et le checkout reste propre. Avec `--builder swift`, il passe par `swift package edit`, qui réécrit le `Package.resolved` du backend : ne jamais committer cette version (gotcha #138).
- **Avant de fusionner** : `wb topic plan <sujet>` donne ses branches dans l'ordre de fusion, Shared d'abord, que les apps résolvent sur main, puis le backend, puis les clients, chacune avec sa pull request, son état et ce qui la retient. Il signale un backend ou un iOS dont le `Package.resolved` commité pinne SolarsplitShared sans le travail Shared du sujet, ou sur un commit absent du main de Shared : une fois Shared fusionné, mettre le pin à la tête de main à la main (gotcha #35). Ses vérifications disent aussi une build qui n'a pas pris le Shared du sujet, une build plus ancienne que les derniers commits, un web client branché sur un autre backend que celui du sujet. `wb topic show` finit par ces vérifications.
- **Quand l'app demande de corriger** : le bouton Ask to fix du panneau Topics liste les échecs (CI, build ou tests locaux, conflits, pin Shared) avec leurs liens. Une session Claude Code au travail le reçoit à la fin de son tour par le hook de la Workbench (`wb topic send`), comme un message de la personne : trouver la cause, corriger dans le worktree, builder et tester par wb, pousser, s'arrêter pour demander sur une décision.
- **Pour suivre une build** : l'app ouvre chaque build, test ou serveur dans une fenêtre, sa progression, son log et ses erreurs, depuis Activity, le bandeau Also on… d'un service ou le bloc Builds and servers d'un sujet. En ligne de commande, `wb logs <run> -f`.
- **Quand le travail est poussé** : `wb topic clean <sujet>` retire les worktrees de son dossier comme `wb worktree remove`, branches et sujet gardés.
- **Quand tout est fusionné** : une branche compte comme fusionnée quand sa pull request l'est, squash compris, ou quand elle est entrée dans son tronc en fast-forward sans pull request (tous ses commits dans le tronc, et son reflog montre des commits à elle depuis sa création). `wb topic show` et le panneau replient les branches fusionnées en une ligne, `wb topic tidy <sujet>` les supprime sur ce Mac, puis `wb topic archive <sujet>`, refusé tant qu'une autre session y travaille, sauf `--force`.
- **Pour reprendre un sujet** : `wb topic show <sujet>` donne ses branches dans chaque repo, leurs worktrees, pull requests et checks, les sessions et les derniers runs. C'est le point de départ d'une session qui prend la suite d'une autre.
- **La session est reconnue sans rien faire** : `CLAUDE_CODE_SESSION_ID` dans Claude Code, `CODEX_THREAD_ID` dans Codex, sinon le shell sous Cursor, VS Code ou l'onglet du terminal. `WB_TOPIC=<sujet>` fixe le sujet d'une commande ou d'un shell.
- Les sujets sont propres au Mac, dans `topics.json` à côté des runs. L'app les crée, les renomme, les fusionne et les archive par les mêmes commandes.

## 7. Ce que chaque run enregistre

Le registre est dans `~/Library/Application Support/solarsplit-workbench/wb/`, les 200 derniers runs. Pour chacun : la session Claude Code qui l'a lancé, par `CLAUDE_CODE_SESSION_ID`, qui nomme son transcript, son titre et, pour une session de l'app Claude, le lien qui l'y ouvre, le checkout, la branche, le commit et les modifications, et **ce avec quoi il builde** : pour le backend la base par son nom et sa nature (sa propre copie, la base de développement, une copie de données réelles, ou **partagée avec le checkout principal**, signalée), le bucket, le builder, le SolarsplitShared utilisé et un `Package.resolved` réécrit. Pour iOS et Android l'environnement et Shared, pour le WebClient Node et le backend visé. Aucun mot de passe. Le panneau Activity déplie chaque run et chaque serveur lancé par un script.

## 8. Le hook d'état des sessions

`scripts/wb-hook.py` de la Workbench, déclaré dans `~/.claude/settings.json` sur SessionStart, UserPromptSubmit, PreToolUse et PostToolUse (matcher `Bash`), Stop, Notification et SessionEnd, avec la commande `/usr/bin/python3 <dossier des repos>/SolarsplitWorkbench/scripts/wb-hook.py`. Il garde un petit fichier par session : état (au travail, en attente de toi, a besoin de toi, terminée), première ligne du dernier prompt, commande en cours, et l'identifiant de la session dans l'app Claude, `CLAUDE_CODE_HOST_SESSION_ID`, seule variable d'environnement qu'il lit, qui rattache ce fichier à sa session même renommée. Le panneau Activity ouvre chaque session de l'app par le lien que l'app lui donne, `claude://claude.ai/epitaxy/<identifiant>`. Mots de passe masqués, rien ne quitte la machine, toujours le code 0, environ 50 ms par appel, jamais sur les lectures de fichiers.

**Les refus du hook, depuis le 02.10.2026, sur décision de Krystian.** Avant une commande shell, le hook refuse (`permissionDecision: deny` de PreToolUse) un build, un test ou un serveur de dev direct d'un repo produit ou de la Workbench elle-même (`swift build`, `swift test`, `xcodebuild` hors `-list` et consorts, `gradlew`, `npm run build` ou `dev`), en donnant la commande `wb` équivalente, et une nouvelle branche par git tant que la session n'a pas dit son sujet (section 6). `WB_DIRECT=1` dans la commande laisse passer un build direct voulu. Après une branche faite par git dans une session sur un sujet, il la classe sous ce sujet. Au premier prompt d'une session qui n'a rien dit, il ajoute une courte note sur la façon de dire son sujet. À la fin d'un tour, il remet le message laissé par Ask to fix (section 6). Il s'applique aux sessions déjà ouvertes dès que le fichier change sur main.

**Dans Codex, les refus seulement.** Son adaptateur relaie bien les groupes de `~/.claude/settings.json`, mais il rejoue PostToolUse sous la forme des seuls chemins de fichier, sans la commande ni le nom de l'événement, et Stop sans ce nom, deux appels que le hook ignore. Seul PreToolUse lui parvient, et avec lui les deux refus, que l'adaptateur rend à Codex : ni classement d'une branche faite par git (la lecture des conversations le rattrape), ni note au premier prompt, ni message de fin de tour. Il note l'outil en cours d'une session Codex, jamais sa fin. Le panneau Activity montre la session Codex par son processus, sans ce relevé. Vérifié le 01.10.2026 en rejouant des événements par l'adaptateur.

## 9. Pièges

- **Un worktree créé à la main partage la base du checkout principal** : ses migrations et ses suites changent les données de développement de tout le monde. `wb` le signale dans la configuration du run. Le recréer avec `wb worktree create`, ou suivre la recette du gotcha #137.
- **La build de la landing page réécrit des fichiers suivis** : `npm run build` commence par `scripts/fetch-landing-manifest.mjs`, qui lit `https://app.solarsplit.com` et réécrit `src/data/network-data.json` et `public/images/installers/`. Une build de la landing laisse donc des modifications dans le checkout dès que le manifeste de production a changé.
- **La file attend aussi une build Xcode de l'IDE** en cours : `wb ps` dit laquelle.
- **Un job lancé en arrière-plan par un shell ignore Ctrl-C**, et ses enfants en héritent : `wb` installe ses propres gestionnaires avant de lancer le script pour que l'arrêt atteigne la build. Un script qui lance une build sans `wb` doit faire de même.
