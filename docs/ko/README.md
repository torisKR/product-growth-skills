<!-- docs-locale: ko -->
# Product Growth Skills

> 1인 개발과 제품 성장을 위한 에이전트 스킬 12개를 사용하는 실전 가이드.

[저장소 홈](../../README.md)

[한국어](../ko/README.md) · [English](../en/README.md) · [日本語](../ja/README.md) · [简体中文](../zh/README.md) · [Français](../fr/README.md)

**목차** · [소개](#overview) · [스킬](#skills) · [빠른 시작](#quick-start) · [작업 흐름](#workflow) · [근거](#evidence) · [구조](#structure) · [검증](#validation) · [안전](#safety) · [기여](#contributing)

<a id="overview"></a>
## 소개

제품의 다음 결정을 명확한 작업 범위와 검증 가능한 결과로 연결하는 스킬 모음입니다. 수요 검증, 운영 위험 관리, 사용자 유입, Flutter·Expo 앱 개선, Android 배포 준비에 사용할 수 있습니다.

전체 작업을 정리할 때는 **`toris-solo-founder`**부터 읽고, 해결할 문제가 명확하면 해당 전문 스킬을 선택하세요. 이 저장소는 에이전트가 읽는 지침과 보조 파일이며, 호스팅 서비스나 상시 실행되는 자동화 시스템이 아닙니다.

다섯 언어의 가이드는 같은 핵심 내용을 다룹니다. 스킬 이름·파일 경로·셸 명령은 번역하지 않으며, 에이전트가 실행 지침으로 읽는 `SKILL.md`는 영어로 유지합니다. 대상 시장 때문에 다른 언어가 필요한 경우를 제외하고 결과물은 한국어로 요청할 수 있습니다.

<a id="skills"></a>
## 스킬 목록

### 기획과 운영

| 스킬 | 역할 |
|---|---|
| [toris-solo-founder](../../toris-solo-founder/SKILL.md) | 목적·수정 범위·검증 근거·작업 인계·재사용할 교훈 정리 |
| [toris-demand-validation](../../toris-demand-validation/SKILL.md) | 실제 고객 관찰과 가정을 구분하고 작은 파일럿 설계 |
| [toris-cost-guardrails](../../toris-cost-guardrails/SKILL.md) | 과금 지점·상한 적용 범위·동시 작업의 예약 비용·잔여 위험 점검 |
| [toris-billing-reliability](../../toris-billing-reliability/SKILL.md) | 구매 검증·중복 이벤트·구독 접근 권한·실패 복구 처리 |
| [toris-small-sample-experiments](../../toris-small-sample-experiments/SKILL.md) | 지표 정의와 소규모 표본·실험 배정 무결성·유지율 해석 |

### 사용자 유입과 검색 노출

| 스킬 | 역할 |
|---|---|
| [app-store-listing-creator](../../app-store-listing-creator/SKILL.md) | 스토어 설명·아이콘 방향·스크린샷 구성·현지화 지침 준비 |
| [seo-geo-optimizer](../../seo-geo-optimizer/SKILL.md) | 기술 SEO·검색 의도·구조화 데이터·내부 링크·GEO·`llms.txt` 점검 |

### 개발과 출시

| 스킬 | 역할 |
|---|---|
| [flutter-android-performance](../../flutter-android-performance/SKILL.md) | Flutter 시작 시간·프레임·CPU·메모리·네트워크·앱 크기 측정 |
| [expo-android-performance](../../expo-android-performance/SKILL.md) | JavaScript·UI·네이티브 코드의 관리 범위를 구분해 Expo 성능 진단 |
| [flutter-interactive-design](../../flutter-interactive-design/SKILL.md) | 반응형 Flutter UI·제스처·모션·제한된 3D와 접근성 대안 구현 |
| [expo-interactive-design](../../expo-interactive-design/SKILL.md) | Expo 화면·라우팅·제스처·모션과 저사양 기기용 대안 구현 |
| [toris-flutter-play-store-release](../../toris-flutter-play-store-release/SKILL.md) | Fastlane·GitHub Actions 기반 Flutter Android 배포 점검과 운영. Firebase·Slack 작업은 별도 범위로 관리 |

<a id="quick-start"></a>
## 빠른 시작과 선택적 설치

### 저장소에서 직접 읽기

새로 내려받는 경우:

```bash
git clone https://github.com/torisKR/product-growth-skills.git
cd product-growth-skills
```

아래 위치에 이미 저장소가 있다면 다시 복제하지 않고 기존 폴더를 사용합니다.

```bash
cd ~/projects/product-growth-skills
```

로컬 파일을 읽을 수 있는 현재 에이전트에 다음과 같이 요청합니다.

```text
이 저장소의 toris-solo-founder/SKILL.md를 읽고 이번 작업에 적용해.
현재 선택한 에이전트와 프로젝트 지침을 유지해.
목표·허용된 수정·검증 기준·비용 한도를 먼저 정리해.
허용된 로컬 작업을 실행하고 확인한 결과와 미검증 범위를 구분해.
실제 작업에서 근거를 얻었을 때만 재사용할 교훈을 기록해.
한국어로 보고해.
```

이는 파일을 읽어 적용하는 요청이며, 에이전트 설치나 설정 변경을 의미하지 않습니다. 파일 접근이 없는 도구에는 필요한 공개 가능 지침만 전달하고 개인 운영 원장은 전달하지 않습니다.

### 상대 경로를 유지하기

전체 저장소를 기준 원본으로 보관하세요. 스킬은 같은 상위 폴더의 `shared-references/`, `research/`, 다른 스킬을 참조할 수 있습니다. 의존 파일 없이 스킬 폴더 하나만 복사하면 링크가 깨질 수 있습니다. 공유용 묶음에 `local-knowledge/`를 포함하지 않습니다.

자동 스킬 탐색, 설치 위치, `$skill-name` 또는 슬래시 명령 호출 방식은 런타임마다 다릅니다. 실제 사용하는 도구에서 확인해야 합니다. Markdown 파일이 있다는 이유로 Codex·OpenCodex·Hermes·Grok·agy·Claude에서의 호환성을 단정하지 않습니다. OpenCode와 OpenCodex도 서로 다른 이름으로 유지합니다.

### 독립형 Android 배포 패키지

아래 설치 절차는 배포 패키지에만 해당합니다. 신뢰할 수 있는 저장소에서 먼저 변경 예정 사항을 확인합니다.

```bash
./toris-flutter-play-store-release/install.sh --dry-run
```

전역 변경 내용을 검토하고 설치하기로 결정한 경우에만 실행합니다.

```bash
./toris-flutter-play-store-release/install.sh
```

업데이트·제거·기존 `flutter-play-store-release`에서의 이전은 [배포 패키지 가이드](../../toris-flutter-play-store-release/README.md)를 따릅니다. 새 설치를 검증한 뒤 기존 설치를 제거하며, 전역 폴더를 수동으로 삭제하지 않습니다. 일반 스킬은 자동 설치되지 않습니다.

[1인 운영 플레이북](../../toris-solo-founder/references/solo-operator-playbook.md)은 개발 가능 시간, 고객 지원, 고정비 손익분기와 운영자 소득, 자동화 시간 회수, 장애 복구 판단을 구체화한다. [한국어 해설](solo-operator-playbook.md)과 [읽기 전용 계산 도구](../../toris-solo-founder/README.md)를 함께 제공한다. 기존 스킬과 명시적으로 함께 읽는 자료이며, 자동 로딩이나 실제 사업 성과를 주장하지 않는다.

<a id="workflow"></a>
## 작업 모드와 요청 예시

```text
맥락 확인 → 근거 수집 → 범위 결정 → 실행 → 검증 → 보고
```

| 모드 | 요청 | 결과 |
|---|---|---|
| `execute` | 구현·수정·개선 | 허용된 로컬 변경과 관련 검증 |
| `review` | 검토만 하고 수정하지 않기 | 파일·외부 시스템 변경 없이 진단 결과 제공 |
| `plan` | 계획만 세우고 구현하지 않기 | 실행하지 않은 구체적인 작업 계획 |

구현 요청은 `execute`가 기본입니다. 검토나 계획만 요청한 경우 그 지시가 우선합니다. 자세한 기준은 [실행 정책](../../shared-references/execution-defaults.md)을 참고하세요.

**수요와 비용 점검**

```text
toris-demand-validation/SKILL.md를 읽고 이 아이디어를 평가해.
실제 고객 근거와 가정을 구분하고 범위가 명확한 파일럿을 제안해.
이어서 toris-cost-guardrails/SKILL.md로 잠재적인 유료 작업을 찾아줘.
고객 연락·서비스 구매·운영 결제 설정 변경은 하지 마.
```

**출시 준비**

```text
toris-flutter-play-store-release/SKILL.md를 읽고 이 Flutter 앱을 점검해.
업로드 없이 가장 작은 안전한 Android 배포 경로를 준비하고 검증해.
실행한 검사와 남은 스토어·기기·계정 작업을 정확히 보고해.
```

최종 보고는 **변경 내용**, **검증 결과**, **미검증 범위**, **사용자에게 남은 작업**으로 구분합니다. 구현·로컬 검사·실제 조작·CI·배포·공개 반영·결제·사업 성과를 하나의 완료 상태로 묶지 않습니다.

<a id="evidence"></a>
## 근거와 개인 지식

총괄 스킬은 정제된 작업 기록, 날짜가 있는 사용자 선호, 제안, 미확인 사항을 구분합니다. [출처 문서](../../toris-solo-founder/references/agents-and-provenance.md)에 여섯 도구의 확인 범위와 한계가 있습니다. 모든 도구의 원본 이력을 완전히 추출한 자료는 아닙니다.

네 가지 리서치 전문 스킬은 [2026-10-15 연구 묶음](../../research/solo-developer-2026-10-15/README.md)을 공유합니다. **1차 출처 16개, 조건부 판단 20개, 숫자 기록 4개, 가상 상황 12개, 산술 예제 6개**로 구성되며 충돌한 항목 3개는 별도 제외 상태로 남겨 두었습니다. 숫자는 출처가 발표한 벤치마크나 예제이지 개인 서비스의 지표가 아닙니다. 연구 규칙은 실제 프로젝트 근거가 생기기 전까지 `personal_validation: not_run`을 유지합니다.

가상 상황은 작성한 수용 기준이지 에이전트가 실제로 통과한 테스트가 아닙니다. 자료 확인, 로컬 검사, 런타임 지침 준수, 운영 성공, 사업 성과는 각각 다른 근거입니다. [기존 검증 기록](../../research/solo-developer-2026-10-15/VERIFICATION.md)은 앞선 연구 작업의 범위를 기록하며 현재 작업 폴더의 상태를 보증하지 않습니다.

`local-knowledge/torisKR/knowledge-ledger.md`는 선택적으로 사용하는 로컬 전용 원장이며 Git 추적에서 제외됩니다. 일반적인 저장소 복제에는 포함되지 않고 스킬과 함께 배포해서도 안 됩니다. Git 제외는 암호화나 백업이 아닙니다.

기존 상세 문서는 원래 언어로 보존했습니다. [한국어 총괄 운영 가이드](../ko/torisKR-solo-founder.md), [한국어 리서치 가이드](../ko/research-backed-skills.md), 영어 연구·런타임 참고 문서를 함께 활용할 수 있습니다. 이번 README 번역이 별도 상세 문서까지 모두 번역했다는 의미는 아닙니다.

<a id="structure"></a>
## 저장소 구조

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
└── local-knowledge/                   # 로컬 전용; Git 제외
```

나머지 스킬 폴더 11개도 저장소 최상위에 나란히 위치합니다. 각 패키지의 `SKILL.md`는 호출 조건과 작업 흐름, `agents/openai.yaml`은 표시 정보와 시작 프롬프트, `references/`는 상세 지침을 담습니다. 배포 패키지에는 추가로 스크립트·템플릿·테스트·설치 매니페스트가 있습니다.

<a id="validation"></a>
## 로컬 검증

Python 3를 사용해 저장소 최상위에서 실행합니다. 배포 테스트는 별도의 Bash·패키지 실행 조건이 있으므로 해당 가이드를 확인하세요. Python 검사로 배포 테스트까지 검증됐다고 판단하지 않습니다.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_research.py --as-of 2026-10-15
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_skills.py
git diff --check
bash toris-flutter-play-store-release/tests/run_tests.sh
```

| 검사 | 확인하는 내용 |
|---|---|
| Python 테스트 | 회귀 사례, 언어별 구성 일치, 공통 명령, 로컬 링크 |
| 연구 검증기 | 출처 참조·날짜·근거 유형·수치 정의·산술 결과 |
| 스킬 검증기 | 패키지 구조·표시 정보·링크·언어 구분·기존 콘텐츠 검사 |
| Git diff 검사 | 추적 중인 변경 내용의 공백 오류 |
| 배포 테스트 | 독립형 배포 패키지에 정의된 테스트 조건 |

`.DS_Store`처럼 매니페스트에 없는 로컬 파일이 있으면 엄격한 배포 파일 목록 검사가 중단될 수 있습니다. 관련 없는 파일을 삭제하거나 검사를 약화하지 말고 실제 오류와 미실행 테스트를 보고합니다. 이 명령들은 에이전트의 실제 행동, 유료 거래, 클라우드 상한, 스토어 승인, 사업 성과를 검증하지 않습니다.

<a id="safety"></a>
## 안전과 작업 범위

사용자의 기존 변경, 선택한 에이전트, 프로젝트 지침을 보존합니다. 로컬 파일 생성은 배포·공개 업로드·스토어 제출·운영 CMS 변경·구매·계정 및 권한 변경·파괴적인 작업·외부 연락의 승인이 아닙니다. 해당 행동에는 명시적인 승인이 필요합니다.

인증 정보, 결제 정보, 고객 기록, 전체 대화 이력을 공유 스킬에 복사하지 않습니다. 요금·제공자 동작·스토어 요구사항·검색 정책처럼 변할 수 있는 사실은 실제 작업 때 최신 1차 출처로 확인합니다. 어떤 스킬도 매출·검색 순위·스토어 승인·AI 답변 인용·성능 향상을 보장하지 않습니다.

런타임 지침은 영어로 유지합니다. 최상위 README, `docs/ko/`, `docs/en/`, `docs/ja/`, `docs/zh/`, `docs/fr/`의 안내와 개인용 일반 문서는 현지화할 수 있습니다. 다만 그 안에서도 `SKILL.md`, `AGENTS.md`, `CLAUDE.md`는 런타임 지침으로 취급합니다. 링크·경로·미완성 표시·비밀정보 검사는 그대로 적용됩니다.

<a id="contributing"></a>
## 기여와 라이선스

[CONTRIBUTING.md](../../CONTRIBUTING.md)를 참고하세요. 문서를 갱신할 때 다섯 언어의 스킬 목록·목차 앵커·셸 명령·근거 구분·승인 범위를 함께 맞춥니다. 설명과 프롬프트는 번역하되 명령 이름이나 경로는 바꾸지 않습니다. 기존 전문 참고 문서는 각 문서의 관리 범위를 유지합니다.

저장소에는 [MIT License](../../LICENSE)가 적용됩니다. 링크된 외부 자료는 원래 제공자의 이용 조건을 따르며 이 라이선스로 재배포 권한이 바뀌지 않습니다.
