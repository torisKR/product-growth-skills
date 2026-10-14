<!-- docs-locale: zh -->
# Product Growth Skills

> 面向独立开发与产品增长的实用指南，涵盖 12 个智能体技能。

[返回仓库首页](../../README.md)

[한국어](../ko/README.md) · [English](../en/README.md) · [日本語](../ja/README.md) · [简体中文](../zh/README.md) · [Français](../fr/README.md)

**目录** · [简介](#overview) · [技能](#skills) · [快速开始](#quick-start) · [工作流程](#workflow) · [证据](#evidence) · [结构](#structure) · [验证](#validation) · [安全](#safety) · [贡献](#contributing)

<a id="overview"></a>
## 简介

本技能集将产品决策与范围明确的执行、可验证的结果连接起来，适用于需求验证、运营风险管理、用户获取、Flutter 与 Expo 应用优化，以及 Android 发布准备。

需要统筹任务时，从 **`toris-solo-founder`** 开始；问题已经明确时，直接选择对应的专项技能。仓库提供的是供智能体读取的指令和辅助文件，不是托管服务，也不是持续运行的自主后台系统。

五种语言的指南覆盖相同的核心内容。技能名称、路径和 Shell 命令保持不变，运行时的 `SKILL.md` 指令仍使用英语。除非目标市场需要其他语言，否则可以要求智能体用简体中文交付结果。

<a id="skills"></a>
## 技能目录

### 规划与运营

| 技能 | 用途 |
|---|---|
| [toris-solo-founder](../../toris-solo-founder/SKILL.md) | 明确目标、范围、证据、任务交接和可复用经验 |
| [toris-demand-validation](../../toris-demand-validation/SKILL.md) | 区分真实客户观察与假设，设计范围有限的试点 |
| [toris-cost-guardrails](../../toris-cost-guardrails/SKILL.md) | 梳理计费操作、额度覆盖范围、并发费用预留和剩余成本风险 |
| [toris-billing-reliability](../../toris-billing-reliability/SKILL.md) | 处理购买验证、重复事件、订阅访问权限与故障恢复 |
| [toris-small-sample-experiments](../../toris-small-sample-experiments/SKILL.md) | 定义指标，解读小样本、实验分流完整性与留存 |

### 用户获取与搜索

| 技能 | 用途 |
|---|---|
| [app-store-listing-creator](../../app-store-listing-creator/SKILL.md) | 准备商店描述、图标方向、截图方案和本地化说明 |
| [seo-geo-optimizer](../../seo-geo-optimizer/SKILL.md) | 检查技术 SEO、搜索意图、结构化数据、内部链接、GEO 和 `llms.txt` |

### 开发与发布

| 技能 | 用途 |
|---|---|
| [flutter-android-performance](../../flutter-android-performance/SKILL.md) | 测量 Flutter 启动、帧表现、CPU、内存、网络和应用体积 |
| [expo-android-performance](../../expo-android-performance/SKILL.md) | 根据 JavaScript、UI 与原生代码的维护边界诊断 Expo 性能 |
| [flutter-interactive-design](../../flutter-interactive-design/SKILL.md) | 构建响应式 Flutter 界面、手势、动效、受控的 3D 体验及无障碍替代方案 |
| [expo-interactive-design](../../expo-interactive-design/SKILL.md) | 构建 Expo 原生页面、路由、手势、动效和低性能设备的降级方案 |
| [toris-flutter-play-store-release](../../toris-flutter-play-store-release/SKILL.md) | 检查并管理基于 Fastlane、GitHub Actions 的 Flutter Android 发布；Firebase 与 Slack 操作单独限定范围 |

<a id="quick-start"></a>
## 快速开始与可选安装

### 直接读取本地仓库

首次获取仓库时：

```bash
git clone https://github.com/torisKR/product-growth-skills.git
cd product-growth-skills
```

如果以下位置已有仓库，请使用现有目录，不要重复克隆：

```bash
cd ~/projects/product-growth-skills
```

向当前具有本地文件访问权限的智能体发送：

```text
读取本仓库的 toris-solo-founder/SKILL.md，并应用到本次任务。
保留当前智能体和项目指令。
先明确目标、允许的修改、验收检查和费用边界。
执行已获授权的本地工作，分别报告已验证结果与未知事项。
只有实际工作提供证据时，才记录可复用的经验。
使用简体中文报告。
```

这是明确的文件读取请求，不会安装或重新配置智能体。对于无法访问本地文件的工具，只提供相关且可以共享的指令，不要提供个人运营记录。

### 保留同级目录引用

将完整仓库作为基准来源保留。技能可能引用同一父目录下的 `shared-references/`、`research/` 或其他技能目录。只复制一个技能目录而遗漏依赖项，可能导致链接失效。共享包中不得包含 `local-knowledge/`。

原生技能发现、安装位置，以及 `$skill-name` 或斜杠命令的调用方式取决于具体运行时，应在实际使用的工具中确认。不能仅凭存在 Markdown 文件，就认定与 Codex、OpenCodex、Hermes、Grok、agy 或 Claude 兼容。OpenCode 与 OpenCodex 也必须作为不同名称处理。

### 独立的 Android 发布包

下面的安装流程仅适用于发布包。在可信的仓库目录中，先预览拟执行的变更：

```bash
./toris-flutter-play-store-release/install.sh --dry-run
```

检查全局变更内容并决定安装后，再执行：

```bash
./toris-flutter-play-store-release/install.sh
```

更新、卸载，以及从旧名称 `flutter-play-store-release` 迁移时，请遵循[发布包指南](../../toris-flutter-play-store-release/README.md)。先验证新安装，再移除旧副本，不要手动删除全局目录。一般技能不会自动安装。

[单人运营手册](../../toris-solo-founder/references/solo-operator-playbook.md)细化了可用开发时间、客户支持、固定成本盈亏平衡与运营者收入目标、自动化时间回收以及故障恢复判断。[工具包](../../toris-solo-founder/README.md)提供只读计算工具和合成输入示例。请明确要求与原有技能一起阅读；这些资料不代表自动加载或已经取得真实业务成果。

<a id="workflow"></a>
## 工作模式与示例

```text
检查上下文 → 收集证据 → 确定范围 → 执行 → 验证 → 报告
```

| 模式 | 请求 | 结果 |
|---|---|---|
| `execute` | 实现、修复或改进 | 已获授权的本地修改及相关验证 |
| `review` | 只审查，不修改 | 不改变文件或外部系统，仅提供结论 |
| `plan` | 只规划，不实现 | 可执行但尚未实施的计划 |

实现类请求默认使用 `execute`。明确要求只审查或只规划时，以该要求为准。详见[执行策略](../../shared-references/execution-defaults.md)。

**需求与成本示例**

```text
读取 toris-demand-validation/SKILL.md，评估这个想法。
区分实际客户证据与假设，提出范围明确的试点。
然后使用 toris-cost-guardrails/SKILL.md，识别可能产生费用的操作。
不要联系客户、购买服务或修改生产环境的计费设置。
```

**发布示例**

```text
读取 toris-flutter-play-store-release/SKILL.md，检查这个 Flutter 应用。
在不上传的前提下，准备并验证最小且安全的 Android 发布流程。
准确报告已经执行的检查，以及剩余的商店、设备或账号操作。
```

交付说明应分别列出 **修改内容**、**已验证结果**、**未验证范围** 和 **需要用户执行的剩余操作**。实现、本地检查、实际交互、CI、部署、公开可用、支付与业务成果不能合并成一个“已完成”状态。

<a id="evidence"></a>
## 证据与个人知识

总控技能区分经过整理的工作记录、带日期的用户偏好、提案与未知事项。[来源说明](../../toris-solo-founder/references/agents-and-provenance.md)记录了六种工具的覆盖范围和限制，并不代表完整导出了所有工具的原始历史。

四个基于研究的专项技能共享 [2026-10-15 研究数据包](../../research/solo-developer-2026-10-15/README.md)，包含 **16 个一手来源、20 条条件化决策规则、4 条数值记录、12 个合成场景和 6 个算术示例**。另有 3 项冲突信息保持隔离排除状态。数值来自发布方的基准统计或示例，不是用户自己服务的指标。研究规则在获得真实项目证据前保持 `personal_validation: not_run`。

合成场景是编写的验收标准，不是智能体已经通过的测试。来源审阅、本地检查、运行时遵循指令、生产成功与商业成果属于不同的证据类别。[既有验证记录](../../research/solo-developer-2026-10-15/VERIFICATION.md)描述的是此前研究任务的范围，不保证当前工作目录的状态。

`local-knowledge/torisKR/knowledge-ledger.md` 是可选的本地个人运营记录，已被 Git 忽略。它不会包含在普通克隆中，也不得与技能一起重新分发。Git 忽略既不是加密，也不是备份。

现有深入说明保留原语言，包括[韩语总控指南](../ko/torisKR-solo-founder.md)、[韩语研究指南](../ko/research-backed-skills.md)，以及英语研究和运行时参考文档。本 README 的翻译不代表这些独立文档也已全部翻译。

<a id="structure"></a>
## 仓库结构

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
└── local-knowledge/                   # 仅限本地；Git 忽略
```

另外 11 个技能目录也位于仓库根目录。每个包中的 `SKILL.md` 描述调用条件与工作流程，`agents/openai.yaml` 提供展示信息和初始提示词，`references/` 存放详细指导。发布包还包括脚本、模板、测试和安装清单。

<a id="validation"></a>
## 本地验证

使用 Python 3，在仓库根目录执行。发布测试有单独的 Bash 与包依赖要求，请查阅专用指南，不能把 Python 检查视为发布测试已经完成。

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_research.py --as-of 2026-10-15
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_skills.py
git diff --check
bash toris-flutter-play-store-release/tests/run_tests.sh
```

| 检查 | 可以确认的内容 |
|---|---|
| Python 测试 | 回归用例、各语言指南结构一致性、公共命令与本地链接 |
| 研究验证器 | 来源引用、日期、证据类型、数值定义和算术结果 |
| 技能验证器 | 包结构、展示信息、链接、语言边界和既有内容检查 |
| Git diff 检查 | 受跟踪变更中的空白格式错误 |
| 发布测试 | 独立发布包规定的测试条件 |

清单中未声明的本地文件，例如 `.DS_Store`，可能使严格的发布清单检查停止。应报告实际失败与尚未运行的测试，而不是删除无关文件或降低验证要求。这些命令不会验证智能体的真实行为、付费交易、云费用上限、商店审核通过或业务表现。

<a id="safety"></a>
## 安全与范围

保留用户已有修改、当前智能体和项目指令。创建本地文件并不授权部署、公开上传、商店提交、修改线上 CMS、购买、变更账号或权限、破坏性操作，以及向他人发送消息。这些动作均需要明确授权。

不得将凭据、支付信息、客户记录或完整会话历史复制到共享技能中。价格、提供方行为、商店要求、搜索政策等可能变化的信息，应在实际任务需要时重新核对最新一手来源。任何技能都不保证收入、排名、商店批准、AI 回答引用或性能提升。

运行时指令保持英语。根目录 README、`docs/ko/`、`docs/en/`、`docs/ja/`、`docs/zh/`、`docs/fr/` 下的指南，以及个人使用的一般说明可以本地化。但即使位于这些目录，`SKILL.md`、`AGENTS.md`、`CLAUDE.md` 仍属于运行时指令。链接、路径、未完成标记与敏感信息检查继续生效。

<a id="contributing"></a>
## 贡献与许可证

请阅读 [CONTRIBUTING.md](../../CONTRIBUTING.md)。更新文档时，应同步五种语言的技能目录、章节锚点、Shell 命令、证据区分和授权边界。翻译说明与提示词，不要改变命令名称或文件路径。现有专项参考文档仍按各自范围维护。

仓库采用 [MIT License](../../LICENSE)。链接的第三方来源仍受原有条款约束，本许可证不会改变其内容的使用权。
