---
name: solarsplit-workbench
description: "SOLARSPLIT Workbench et son CLI wb pour les agents : builds et tests en file d'attente pour ne pas saturer la machine, worktree prêt à builder avec sa base et ses ports, serveur par worktree, ce qui tourne sur le Mac et quelle session l'a lancé, configuration réelle de chaque build, sujets qui regroupent les branches d'un même travail dans plusieurs repos. Charger au début de tout travail qui créera une branche ou buildera : la session dit d'abord à quel sujet son travail appartient (wb topic use, wb topic new, wb topic use --none), sinon wb et le hook refusent. Aussi avant tout swift build, swift test, xcodebuild, gradlew ou npm run build dans un repo produit, avant de créer ou de supprimer un worktree, et pour savoir ce que font les autres agents."
---

# solarsplit-workbench

SOLARSPLIT Workbench et son CLI wb pour les agents : builds et tests en file d'attente pour ne pas saturer la machine, worktree prêt à builder avec sa base et ses ports, serveur par worktree, ce qui tourne sur le Mac et quelle session l'a lancé, configuration réelle de chaque build, sujets qui regroupent les branches d'un même travail dans plusieurs repos. Charger au début de tout travail qui créera une branche ou buildera : la session dit d'abord à quel sujet son travail appartient (wb topic use, wb topic new, wb topic use --none), sinon wb et le hook refusent. Aussi avant tout swift build, swift test, xcodebuild, gradlew ou npm run build dans un repo produit, avant de créer ou de supprimer un worktree, et pour savoir ce que font les autres agents.

## Reference complete

Fichier source, 33 KB : `rule.md`, dans ce dossier de skill.
C'est un lien relatif vers `KrystianPawlowskiKnowledge/.cursor/rules/solarsplit-workbench.md`, valable sur toute machine.

Lire ce fichier quand la tache le demande.

## Sommaire des sections

- 1. Quand s'en servir
- 2. Le CLI
- 3. La file d'attente
- 4. Sortie pour un agent
- 5. Worktrees
- 6. Sujets
- 7. Ce que chaque run enregistre
- 8. Le hook d'état des sessions
- 9. Pièges
