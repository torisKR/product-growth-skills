<!-- docs-locale: ja -->
# Product Growth Skills

> 個人開発とプロダクトの成長を支える、12のエージェントスキルの実践ガイド。

[リポジトリのホーム](../../README.md)

[한국어](../ko/README.md) · [English](../en/README.md) · [日本語](../ja/README.md) · [简体中文](../zh/README.md) · [Français](../fr/README.md)

**目次** · [概要](#overview) · [スキル](#skills) · [使い始める](#quick-start) · [作業の進め方](#workflow) · [根拠](#evidence) · [構成](#structure) · [検証](#validation) · [安全性](#safety) · [コントリビューション](#contributing)

<a id="overview"></a>
## 概要

プロダクトに関する判断を、範囲の明確な作業と検証可能な結果につなげるスキル集です。需要の検証、運用リスクの管理、ユーザー獲得、Flutter・Expoアプリの改善、Androidの配信準備に利用できます。

作業全体を整理する場合は **`toris-solo-founder`** から始め、課題が明確な場合は専門スキルを選んでください。このリポジトリはエージェントが読む指示と補助ファイルであり、ホスティングサービスや常時稼働する自律システムではありません。

5言語のガイドは同じ基本事項を扱います。スキル名、パス、シェルコマンドは翻訳せず、実行時の指示となる `SKILL.md` は英語のまま維持します。対象市場に別の言語が必要な場合を除き、成果物は日本語で依頼できます。

<a id="skills"></a>
## スキル一覧

### 企画と運用

| スキル | 役割 |
|---|---|
| [toris-solo-founder](../../toris-solo-founder/SKILL.md) | 目的、作業範囲、根拠、引き継ぎ、再利用できる教訓を整理 |
| [toris-demand-validation](../../toris-demand-validation/SKILL.md) | 顧客の実際の行動と仮定を区別し、小規模な試行を設計 |
| [toris-cost-guardrails](../../toris-cost-guardrails/SKILL.md) | 課金される処理、上限の適用範囲、同時実行の予約コスト、残存リスクを確認 |
| [toris-billing-reliability](../../toris-billing-reliability/SKILL.md) | 購入検証、重複イベント、サブスクリプションの利用権限、復旧を扱う |
| [toris-small-sample-experiments](../../toris-small-sample-experiments/SKILL.md) | 指標を定義し、少数標本、実験の割り当ての整合性、継続利用率を解釈 |

### ユーザー獲得と検索

| スキル | 役割 |
|---|---|
| [app-store-listing-creator](../../app-store-listing-creator/SKILL.md) | ストア説明、アイコンの方向性、スクリーンショット構成、ローカライズ方針を準備 |
| [seo-geo-optimizer](../../seo-geo-optimizer/SKILL.md) | 技術SEO、検索意図、構造化データ、内部リンク、GEO、`llms.txt` を点検 |

### 開発とリリース

| スキル | 役割 |
|---|---|
| [flutter-android-performance](../../flutter-android-performance/SKILL.md) | Flutterの起動、フレーム、CPU、メモリ、通信、アプリサイズを測定 |
| [expo-android-performance](../../expo-android-performance/SKILL.md) | JavaScript・UI・ネイティブコードの管理境界を踏まえてExpoの性能を診断 |
| [flutter-interactive-design](../../flutter-interactive-design/SKILL.md) | レスポンシブなFlutter UI、ジェスチャー、モーション、限定的な3Dとアクセシブルな代替表現を実装 |
| [expo-interactive-design](../../expo-interactive-design/SKILL.md) | Expoの画面、ルーティング、ジェスチャー、モーション、低性能端末向けの代替処理を実装 |
| [toris-flutter-play-store-release](../../toris-flutter-play-store-release/SKILL.md) | Fastlane・GitHub Actionsを使うFlutter Android配信の点検と運用。Firebase・Slack操作は別の範囲で管理 |

<a id="quick-start"></a>
## 使い始める・任意のインストール

### チェックアウトから直接読む

新しく取得する場合:

```bash
git clone https://github.com/torisKR/product-growth-skills.git
cd product-growth-skills
```

次の場所に既存のチェックアウトがある場合は、再度クローンせずにそのフォルダーを使います。

```bash
cd ~/projects/product-growth-skills
```

ローカルファイルを読める現在のエージェントに、次のように依頼します。

```text
このリポジトリの toris-solo-founder/SKILL.md を読み、今回の作業に適用して。
現在のエージェントとプロジェクトの指示を維持して。
目的、許可された変更、検証基準、費用の上限を先に整理して。
許可されたローカル作業を行い、確認済みの結果と未確認事項を分けて報告して。
実際の作業で根拠を得た場合に限り、再利用できる教訓を記録して。
日本語で報告して。
```

これはファイルを読む明示的な依頼であり、エージェントのインストールや設定変更ではありません。ファイルにアクセスできないツールには、共有可能な必要部分だけを渡し、個人用の運用記録は渡さないでください。

### 相対パスを維持する

リポジトリ全体を基準となる原本として保持してください。スキルは同じ親フォルダーにある `shared-references/`、`research/`、他のスキルを参照する場合があります。依存ファイルを含めずに1フォルダーだけコピーすると、リンクが切れることがあります。共有パッケージに `local-knowledge/` を含めないでください。

スキルの自動検出、インストール先、`$skill-name` やスラッシュコマンドでの呼び出し方法はランタイムによって異なります。実際に使うツールで確認してください。Markdownファイルの存在だけで、Codex・OpenCodex・Hermes・Grok・agy・Claudeとの互換性を断定してはいけません。OpenCodeとOpenCodexも別の名前として扱います。

### 独立したAndroid配信パッケージ

以下のインストール手順は配信パッケージにのみ適用されます。信頼できるチェックアウトから、まず変更予定を確認します。

```bash
./toris-flutter-play-store-release/install.sh --dry-run
```

グローバルな変更内容を確認し、インストールを選択した場合に限り実行します。

```bash
./toris-flutter-play-store-release/install.sh
```

更新、アンインストール、旧名 `flutter-play-store-release` からの移行は、[配信パッケージのガイド](../../toris-flutter-play-store-release/README.md)に従ってください。旧版を取り除く前に新版を検証し、グローバルディレクトリを手動で削除しないでください。一般のスキルが自動インストールされることはありません。

[一人運営のプレイブック](../../toris-solo-founder/references/solo-operator-playbook.md)では、開発に使える時間、問い合わせ対応、固定費の損益分岐と運営者の収入目標、自動化の時間回収、障害復旧を扱う。[ツールキット](../../toris-solo-founder/README.md)には読み取り専用の計算ツールと架空の入力例がある。既存スキルと明示的に併読する資料であり、自動読み込みや実際の事業成果を保証するものではない。

<a id="workflow"></a>
## 作業モードと依頼例

```text
状況の確認 → 根拠の収集 → 範囲の決定 → 実行 → 検証 → 報告
```

| モード | 依頼 | 結果 |
|---|---|---|
| `execute` | 実装、修正、改善 | 許可されたローカル変更と関連する検証 |
| `review` | レビューのみ、変更しない | ファイルや外部システムを変更せずに所見を報告 |
| `plan` | 計画のみ、実装しない | 未実行の具体的な作業計画 |

実装依頼の既定は `execute` です。レビューのみ、計画のみという明示的な依頼が優先されます。[実行ポリシー](../../shared-references/execution-defaults.md)も参照してください。

**需要と費用の確認**

```text
toris-demand-validation/SKILL.md を読んで、このアイデアを評価して。
実際の顧客の根拠と仮定を分け、範囲の明確な試行を提案して。
続いて toris-cost-guardrails/SKILL.md で課金が発生し得る処理を調べて。
顧客への連絡、サービスの購入、本番の課金設定変更は行わないで。
```

**リリース準備**

```text
toris-flutter-play-store-release/SKILL.md を読み、このFlutterアプリを点検して。
アップロードせずに、最小限で安全なAndroid配信手順を準備し、検証して。
実行した検査と、残っているストア・実機・アカウント作業を正確に報告して。
```

最終報告では **変更内容**、**検証済みの結果**、**未検証の範囲**、**利用者に残された操作**を区別します。実装、ローカル検査、実際の操作、CI、デプロイ、公開反映、決済、事業成果を1つの完了状態にまとめないでください。

<a id="evidence"></a>
## 根拠と個人の知識

総括スキルでは、整理済みの作業記録、日付付きの利用者の選好、提案、未確認事項を区別します。[出典に関する文書](../../toris-solo-founder/references/agents-and-provenance.md)には6ツールの確認範囲と限界があり、すべての生ログを完全にエクスポートした資料ではありません。

4つの調査ベースの専門スキルは、[2026-10-15の調査データ](../../research/solo-developer-2026-10-15/README.md)を共有します。**一次資料16件、条件付きの判断規則20件、数値記録4件、仮想シナリオ12件、算術例6件**を含み、矛盾する3項目は除外状態で保管しています。数値は公表されたベンチマークや例であり、利用者自身のサービス指標ではありません。実際のプロジェクトで根拠を得るまでは `personal_validation: not_run` を維持します。

仮想シナリオは作成した受け入れ基準であり、エージェントが実際に合格したテストではありません。資料確認、ローカル検査、指示への追従、本番の成功、事業成果はそれぞれ別の根拠です。[既存の検証記録](../../research/solo-developer-2026-10-15/VERIFICATION.md)は前回の調査作業の範囲を記録しており、現在のチェックアウトの状態を保証するものではありません。

`local-knowledge/torisKR/knowledge-ledger.md` は任意のローカル専用運用記録で、Gitの追跡対象外です。通常のクローンには含まれず、スキルとともに再配布してはいけません。Gitでの除外は暗号化でもバックアップでもありません。

既存の詳細文書は原文の言語を維持しています。[韓国語の総括ガイド](../ko/torisKR-solo-founder.md)、[韓国語の調査ガイド](../ko/research-backed-skills.md)、英語の調査資料とランタイム参考文書を利用できます。このREADMEの翻訳は、それらの独立した文書まで翻訳したという意味ではありません。

<a id="structure"></a>
## リポジトリ構成

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
└── local-knowledge/                   # ローカル専用、Git対象外
```

残り11個のスキルフォルダーもリポジトリのルート直下に並びます。各パッケージの `SKILL.md` は呼び出し条件と作業手順、`agents/openai.yaml` は表示情報と開始用プロンプト、`references/` は詳細な指針を保持します。配信パッケージにはスクリプト、テンプレート、テスト、インストール用マニフェストも含まれます。

<a id="validation"></a>
## ローカル検証

Python 3を使い、リポジトリのルートで実行します。配信テストには別途Bashとパッケージ固有の前提条件があります。Pythonの検査だけで配信テストまで完了したと判断せず、専用ガイドを確認してください。

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_research.py --as-of 2026-10-15
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_skills.py
git diff --check
bash toris-flutter-play-store-release/tests/run_tests.sh
```

| 検査 | 確認できること |
|---|---|
| Pythonテスト | 回帰ケース、言語間の構成の一致、共通コマンド、ローカルリンク |
| 調査データ検証 | 出典参照、日付、根拠の分類、数値定義、算術結果 |
| スキル検証 | パッケージ構造、表示情報、リンク、言語の適用範囲、既存の内容検査 |
| Git diff検査 | 追跡対象の変更に含まれる空白の問題 |
| 配信テスト | 独立した配信パッケージの所定のテスト条件 |

`.DS_Store` のような未登録のローカルファイルがあると、厳密なマニフェスト検査が停止する場合があります。無関係なファイルを削除したり検査を弱めたりせず、実際のエラーと未実行のテストを報告してください。これらのコマンドは、エージェントの実際の動作、有料取引、クラウドの支出上限、ストア承認、事業成果を検証しません。

<a id="safety"></a>
## 安全性と作業範囲

利用者の既存の変更、選択したエージェント、プロジェクトの指示を維持します。ローカルファイルの作成は、デプロイ、公開アップロード、ストア申請、本番CMSの変更、購入、アカウントや権限の変更、破壊的な操作、他者への連絡を許可するものではありません。これらには明示的な承認が必要です。

認証情報、支払情報、顧客記録、会話履歴全体を共有スキルにコピーしてはいけません。料金、提供者の動作、ストア要件、検索ポリシーなど変化する情報は、実際の作業時に最新の一次資料で確認します。売上、検索順位、ストア承認、AI回答への引用、性能改善を保証するスキルはありません。

ランタイム指示は英語で維持します。ルートREADME、`docs/ko/`、`docs/en/`、`docs/ja/`、`docs/zh/`、`docs/fr/` のガイドと個人向けの一般文書は翻訳できます。ただし、その中にあっても `SKILL.md`、`AGENTS.md`、`CLAUDE.md` はランタイム指示として扱います。リンク、パス、未完成の記述、機密情報の検査は引き続き適用されます。

<a id="contributing"></a>
## コントリビューションとライセンス

[CONTRIBUTING.md](../../CONTRIBUTING.md)を参照してください。文書の更新時には、5言語のスキル一覧、セクションのアンカー、シェルコマンド、根拠の区別、承認の範囲をそろえてください。説明やプロンプトは翻訳しても、コマンド名やパスは変更しません。既存の専門参考文書は、それぞれの管理範囲を維持します。

リポジトリには [MIT License](../../LICENSE) が適用されます。リンク先の外部資料には元の利用条件が適用され、このライセンスによってその内容の権利が変更されることはありません。
