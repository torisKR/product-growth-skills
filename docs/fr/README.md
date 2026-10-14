<!-- docs-locale: fr -->
# Product Growth Skills

> Un guide pratique de 12 compétences pour agents IA, au service du développement indépendant et de la croissance produit.

[Accueil du dépôt](../../README.md)

[한국어](../ko/README.md) · [English](../en/README.md) · [日本語](../ja/README.md) · [简体中文](../zh/README.md) · [Français](../fr/README.md)

**Sommaire** · [Présentation](#overview) · [Compétences](#skills) · [Démarrage](#quick-start) · [Méthode de travail](#workflow) · [Éléments probants](#evidence) · [Structure](#structure) · [Validation](#validation) · [Sécurité](#safety) · [Contribution](#contributing)

<a id="overview"></a>
## Présentation

Cette collection relie les décisions produit à un travail au périmètre défini et à des résultats vérifiables. Elle couvre la validation de la demande, les risques d'exploitation, l'acquisition d'utilisateurs, l'amélioration d'applications Flutter ou Expo et la préparation d'une distribution Android.

Commencez par **`toris-solo-founder`** pour coordonner une tâche, ou choisissez une compétence spécialisée lorsque le problème est déjà identifié. Il s'agit d'instructions et de fichiers de référence pour un agent, et non d'un service hébergé ou d'un système autonome fonctionnant en arrière-plan.

Les cinq guides linguistiques couvrent le même contenu essentiel. Les noms de compétences, chemins et commandes shell ne sont pas traduits ; les instructions d'exécution `SKILL.md` restent en anglais. Demandez des livrables en français, sauf si le marché visé exige une autre langue.

<a id="skills"></a>
## Catalogue des compétences

### Planifier et exploiter

| Compétence | Rôle |
|---|---|
| [toris-solo-founder](../../toris-solo-founder/SKILL.md) | Définir l'objectif, le périmètre, les preuves, la transmission du travail et les enseignements réutilisables |
| [toris-demand-validation](../../toris-demand-validation/SKILL.md) | Distinguer observations clients et hypothèses, puis concevoir un pilote limité |
| [toris-cost-guardrails](../../toris-cost-guardrails/SKILL.md) | Cartographier les opérations facturables, la couverture des plafonds, les réservations concurrentes et le risque résiduel |
| [toris-billing-reliability](../../toris-billing-reliability/SKILL.md) | Traiter la vérification des achats, les événements dupliqués, les droits d'abonnement et la récupération après échec |
| [toris-small-sample-experiments](../../toris-small-sample-experiments/SKILL.md) | Définir les indicateurs et interpréter les petits échantillons, l'intégrité de l'affectation et la rétention |

### Acquérir des utilisateurs

| Compétence | Rôle |
|---|---|
| [app-store-listing-creator](../../app-store-listing-creator/SKILL.md) | Préparer descriptions de boutique, orientations d'icône, plans de captures d'écran et consignes de localisation |
| [seo-geo-optimizer](../../seo-geo-optimizer/SKILL.md) | Examiner le SEO technique, l'intention de recherche, les données structurées, les liens internes, le GEO et `llms.txt` |

### Développer et livrer

| Compétence | Rôle |
|---|---|
| [flutter-android-performance](../../flutter-android-performance/SKILL.md) | Mesurer le démarrage, les images rendues, le CPU, la mémoire, le réseau et la taille d'une application Flutter |
| [expo-android-performance](../../expo-android-performance/SKILL.md) | Diagnostiquer les performances Expo selon les responsabilités des couches JavaScript, UI et native |
| [flutter-interactive-design](../../flutter-interactive-design/SKILL.md) | Créer des interfaces Flutter adaptatives, des gestes, des animations et une 3D maîtrisée avec des alternatives accessibles |
| [expo-interactive-design](../../expo-interactive-design/SKILL.md) | Construire des écrans Expo natifs, la navigation, les gestes, les animations et des solutions de repli pour les appareils limités |
| [toris-flutter-play-store-release](../../toris-flutter-play-store-release/SKILL.md) | Examiner et gérer la distribution Flutter Android avec Fastlane et GitHub Actions ; les actions Firebase et Slack gardent un périmètre distinct |

<a id="quick-start"></a>
## Démarrage et installation facultative

### Lire depuis une copie locale

Pour obtenir une nouvelle copie :

```bash
git clone https://github.com/torisKR/product-growth-skills.git
cd product-growth-skills
```

Si le dépôt existe déjà à l'emplacement suivant, utilisez-le au lieu de le cloner à nouveau :

```bash
cd ~/projects/product-growth-skills
```

Adressez cette demande à l'agent actuel disposant d'un accès aux fichiers locaux :

```text
Lis toris-solo-founder/SKILL.md dans ce dépôt et applique-le à ma tâche.
Conserve l'agent actuel et les instructions du projet.
Définis l'objectif, les modifications autorisées, les vérifications et la limite de coût.
Effectue le travail local autorisé et distingue les résultats vérifiés des inconnues.
Ne consigne un enseignement réutilisable que si le travail apporte des preuves.
Réponds en français.
```

Il s'agit d'une demande explicite de lecture de fichiers, pas d'une installation ou d'une reconfiguration de l'agent. Sans accès local, fournissez uniquement les instructions pertinentes et partageables, jamais les notes personnelles d'exploitation.

### Conserver les références relatives

Gardez le dépôt complet comme source de référence. Les compétences peuvent dépendre des dossiers voisins `shared-references/`, `research/` ou d'autres compétences. Copier un seul dossier sans ses dépendances peut casser les liens. N'incluez jamais `local-knowledge/` dans un paquet partagé.

La découverte native des compétences, les répertoires d'installation et l'invocation par `$skill-name` ou commande précédée d'une barre oblique dépendent de l'environnement. Vérifiez ces détails pour l'outil utilisé. La présence d'un fichier Markdown ne démontre pas la compatibilité avec Codex, OpenCodex, Hermes, Grok, agy ou Claude. OpenCode et OpenCodex restent deux noms distincts.

### Paquet autonome de distribution Android

Les commandes suivantes concernent uniquement le paquet de distribution. Depuis une copie de confiance du dépôt, commencez par prévisualiser les modifications :

```bash
./toris-flutter-play-store-release/install.sh --dry-run
```

Après examen des changements globaux et décision d'installer :

```bash
./toris-flutter-play-store-release/install.sh
```

Pour les mises à jour, la désinstallation et la migration depuis `flutter-play-store-release`, suivez le [guide du paquet de distribution](../../toris-flutter-play-store-release/README.md). Vérifiez la nouvelle installation avant de retirer l'ancienne ; ne supprimez pas manuellement les répertoires globaux. Les autres compétences ne s'installent pas automatiquement.

Le [guide d'exploitation en solo](../../toris-solo-founder/references/solo-operator-playbook.md) détaille la capacité de développement, le support, le seuil de couverture des coûts, l'objectif de revenu personnel, le temps nécessaire pour amortir une automatisation et la reprise après incident. La [boîte à outils](../../toris-solo-founder/README.md) fournit un calculateur en lecture seule et des données fictives. Consultez-la explicitement avec le skill existant : ni chargement automatique ni résultat commercial réel ne sont attestés.

<a id="workflow"></a>
## Modes de travail et exemples

```text
Examiner le contexte → réunir les preuves → définir le périmètre → agir → vérifier → rendre compte
```

| Mode | Demande | Résultat |
|---|---|---|
| `execute` | Implémenter, corriger ou améliorer | Modifications locales autorisées et vérifications pertinentes |
| `review` | Examiner uniquement, sans modifier | Constats sans changement de fichiers ni de systèmes externes |
| `plan` | Planifier uniquement, sans implémenter | Plan exploitable, mais non exécuté |

Les demandes d'implémentation utilisent `execute` par défaut. Une demande explicite de revue ou de planification prévaut. Consultez la [politique d'exécution](../../shared-references/execution-defaults.md).

**Exemple : demande et coûts**

```text
Lis toris-demand-validation/SKILL.md et évalue cette idée.
Sépare les observations clients réelles des hypothèses et propose un pilote limité.
Utilise ensuite toris-cost-guardrails/SKILL.md pour repérer les opérations payantes possibles.
Ne contacte pas de clients, n'achète aucun service et ne modifie pas la facturation en production.
```

**Exemple : préparation d'une livraison**

```text
Lis toris-flutter-play-store-release/SKILL.md et examine cette application Flutter.
Prépare et vérifie le chemin de distribution Android minimal et sûr, sans téléversement.
Indique les contrôles exécutés et les actions restantes sur la boutique, les appareils ou les comptes.
```

La restitution distingue les **modifications**, les **résultats vérifiés**, les **éléments non vérifiés** et les **actions restant à l'utilisateur**. Ne confondez pas implémentation, tests locaux, interactions réelles, CI, déploiement, disponibilité publique, paiements et résultats commerciaux.

<a id="evidence"></a>
## Éléments probants et connaissances privées

La compétence de coordination distingue les comptes rendus de travail consolidés, les préférences datées, les propositions et les inconnues. Sa [référence de provenance](../../toris-solo-founder/references/agents-and-provenance.md) précise la couverture des six outils et ses limites ; elle ne constitue pas un export intégral de tous leurs historiques bruts.

Les quatre compétences issues de recherches partagent le [dossier du 2026-10-15](../../research/solo-developer-2026-10-15/README.md) : **16 sources primaires, 20 règles conditionnelles, 4 enregistrements numériques, 12 scénarios synthétiques et 6 exemples arithmétiques**. Trois éléments contradictoires restent en quarantaine. Les chiffres sont des références ou exemples publiés, pas des indicateurs du service de l'utilisateur. Les règles conservent `personal_validation: not_run` tant qu'une application réelle n'apporte pas les preuves nécessaires.

Les scénarios synthétiques sont des critères d'acceptation rédigés, pas des tests déjà réussis par un agent. Lecture des sources, contrôles locaux, respect des instructions, réussite en production et résultats commerciaux sont des catégories de preuves différentes. Le [compte rendu de vérification](../../research/solo-developer-2026-10-15/VERIFICATION.md) décrit le périmètre de la tâche de recherche antérieure, sans garantir l'état de la copie actuelle.

`local-knowledge/torisKR/knowledge-ledger.md` est un registre personnel local facultatif, ignoré par Git. Il n'est pas inclus dans un clone normal et ne doit pas être redistribué avec les compétences. L'exclusion Git n'est ni un chiffrement ni une sauvegarde.

Les documents détaillés existants conservent leur langue d'origine : [guide de coordination en coréen](../ko/torisKR-solo-founder.md), [guide de recherche en coréen](../ko/research-backed-skills.md), références de recherche et instructions d'exécution en anglais. La traduction de ce README n'implique pas celle de ces documents indépendants.

<a id="structure"></a>
## Structure du dépôt

```text
product-growth-skills/
├── README.md
├── docs/
│   ├── ko/README.md
│   ├── en/README.md
│   ├── ja/README.md
│   ├── zh/README.md
│   └── fr/README.md
├── toris-solo-founder/
├── shared-references/
├── research/solo-developer-2026-10-15/
├── scripts/
└── local-knowledge/                   # Local uniquement ; ignoré par Git
```

Les 11 autres dossiers de compétences se trouvent également à la racine. Chaque paquet contient `SKILL.md` pour les conditions d'activation et la méthode, `agents/openai.yaml` pour les métadonnées d'affichage et une demande initiale, et `references/` pour les consignes détaillées. Le paquet de distribution contient aussi des scripts, modèles, tests et un manifeste d'installation.

<a id="validation"></a>
## Validation locale

Exécutez les commandes à la racine du dépôt avec Python 3. La suite de distribution possède ses propres prérequis Bash et dépendances : consultez son guide, sans supposer que les tests Python la couvrent.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_research.py --as-of 2026-10-15
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_skills.py
git diff --check
bash toris-flutter-play-store-release/tests/run_tests.sh
```

| Contrôle | Ce qu'il vérifie |
|---|---|
| Tests Python | Régressions, cohérence entre langues, commandes communes et liens locaux |
| Validateur de recherche | Références, dates, catégories de preuves, définitions numériques et calculs |
| Validateur de compétences | Structure des paquets, métadonnées, liens, limites linguistiques et contrôles de contenu existants |
| Contrôle Git diff | Erreurs d'espacement dans les modifications suivies |
| Suite de distribution | Contrat de test déclaré par le paquet autonome de distribution |

Un fichier local non déclaré, tel que `.DS_Store`, peut bloquer le contrôle strict du manifeste. Signalez l'échec réel et les tests non exécutés au lieu de supprimer des fichiers sans rapport ou d'affaiblir les contrôles. Ces commandes ne vérifient ni le comportement réel des agents, ni les transactions payantes, les plafonds cloud, l'approbation des boutiques ou les performances commerciales.

<a id="safety"></a>
## Sécurité et périmètre

Préservez les modifications existantes de l'utilisateur, l'agent sélectionné et les instructions du projet. Créer des fichiers locaux n'autorise pas un déploiement, une publication, une soumission en boutique, une modification du CMS en production, un achat, un changement de compte ou de permissions, une opération destructive ou un message à autrui. Ces actions nécessitent une autorisation explicite.

Ne copiez jamais d'identifiants secrets, de données de paiement, de dossiers clients ou d'historiques complets de conversation dans les compétences partagées. Vérifiez les prix, comportements des fournisseurs, exigences des boutiques et politiques de recherche susceptibles d'évoluer auprès de sources primaires à jour lorsqu'une tâche réelle en dépend. Aucune compétence ne garantit un revenu, un classement, une approbation, une citation dans une réponse IA ou un gain de performance.

Les instructions d'exécution restent en anglais. Le README racine, les guides dans `docs/ko/`, `docs/en/`, `docs/ja/`, `docs/zh/`, `docs/fr/` et les notes personnelles destinées à une lecture humaine peuvent être localisés. Même dans ces dossiers, `SKILL.md`, `AGENTS.md` et `CLAUDE.md` restent des instructions d'exécution. Les contrôles de liens, chemins, marqueurs d'inachèvement et secrets continuent de s'appliquer.

<a id="contributing"></a>
## Contribution et licence

Consultez [CONTRIBUTING.md](../../CONTRIBUTING.md). Lors d'une mise à jour, alignez les catalogues, ancres de sections, commandes shell, distinctions de preuves et limites d'autorisation des cinq guides. Traduisez les explications et les demandes, pas les noms de commandes ni les chemins. Les références spécialisées existantes conservent leur propre périmètre de maintenance.

Le dépôt utilise la [MIT License](../../LICENSE). Les sources tierces liées conservent leurs conditions d'origine ; cette licence ne modifie pas les droits sur leur contenu.
