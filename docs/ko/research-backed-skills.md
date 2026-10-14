# 리서치 기반 1인 개발·사업 스킬

조사 기준일: 2026-10-15. 개인 실전 경험이 아니라 **공개 1차 자료에서 도출한 실행 지식**이다. 실제 프로젝트에서 적용·검증한 뒤에만 개인 암묵지로 승격한다.

## 무엇을 추가했는가

| 스킬 | 해결할 문제 | 주요 산출물 |
|---|---|---|
| [toris-demand-validation](../../toris-demand-validation/SKILL.md) | 만들기는 쉬운데 누가 왜 쓸지 불명확한 상황 | 수요 근거표, 최소 파일럿 계약, 지속·수정·중단 판단 |
| [toris-cost-guardrails](../../toris-cost-guardrails/SKILL.md) | AI·메시지·클라우드 사용료가 예상 밖으로 늘어나는 상황 | 과금 경계 목록, 알림·차단 구분, 동시 작업 예약 비용·실패 처리 설계 |
| [toris-billing-reliability](../../toris-billing-reliability/SKILL.md) | 중복 결제 알림, 순서가 뒤바뀐 이벤트, 구독 권한 불일치 | 구매·접근 권한 상태 모델, 중복 방지 키, 복구·검증 시나리오 |
| [toris-small-sample-experiments](../../toris-small-sample-experiments/SKILL.md) | 사용자가 적어 작은 수치 변화에 과도한 결론을 내리는 상황 | 지표 정의서, 표본·배정 상태 점검, 성숙 코호트 분석, 불확실성을 포함한 판단 |

기존 `toris-solo-founder`는 전체 작업의 총괄 기준으로 유지한다. 앱스토어 소재, SEO, Flutter·Expo 성능·디자인, 배포 스킬을 중복 구현하지 않고 이번 네 영역을 전문화했다.

## 조사 데이터의 구성

[연구 묶음](../../research/solo-developer-2026-10-15/README.md)을 시작점으로 읽는다.

| 파일 | 내용 | 해석 시 주의 |
|---|---|---|
| [evidence.json](../../research/solo-developer-2026-10-15/evidence.json) | 1차 출처 16개, 조건부 판단 20개, 숫자 기록 4개, 제외 항목 3개 | 출처의 관찰과 작성자가 도출한 판단을 분리했다. 모든 판단의 개인 실전 검증 상태는 `not_run`이다. |
| [evaluations.json](../../research/solo-developer-2026-10-15/evaluations.json) | 실패 압박 상황 12개와 산술 예제 6개 | 상황은 가상 검증 입력이다. 고객 대화나 실제 모델 실행 로그가 아니다. |
| `scripts/validate_research.py` | 식별자·참조·출처 유형·날짜·수치 정의·산술 결과 검사 | 실제 통계 판정, 결제 처리, 분산 비용 통제, 에이전트 행동을 실행하는 도구가 아니다. |
| `scripts/test_research_bundle.py` | 누락·잘못된 출처 연결·미래 날짜·비정상 숫자·거짓 실전 검증 표시 등에 대한 회귀 테스트 | 구조적 오류를 잡는 검사이며 연구 내용 전체의 진실성을 자동 증명하지 않는다. |

숫자 기록 4개 중 2개는 RevenueCat 보고서의 공개 벤치마크이고, 2개는 PostHog 문서의 표본 계산 예제다. 개인 서비스의 사용자·매출·전환율을 만들어 넣지 않았다. 산술 예제 6개 중 1개는 출판된 계산 예제, 나머지 5개는 명시적으로 표시한 가상 입력이다.

조사는 필요한 판단을 중심으로 선별한 자료 검토이며, 모든 관련 연구를 빠짐없이 조사한 체계적 문헌고찰은 아니다. 링크의 조회일과 문서의 발행일·통계 대상 기간도 구분한다.

## 이번에 도출한 중요한 판단

### 1. 긍정적인 반응보다 실제 문제와 행동을 확인한다

중립적인 질문으로 최근의 구체적인 상황, 현재의 해결 방법, 실패의 결과를 확인한다. AI가 만든 페르소나와 칭찬을 고객 수요로 집계하지 않는다. 사용할 수 있는 화면과 기꺼이 비용을 지불할 서비스도 다르다. [인터뷰 지침](https://www.gov.uk/service-manual/user-research/using-in-depth-interviews)과 [사용성 평가 지침](https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing)을 바탕으로, 문제·사용성·약속·결제·반복 사용을 별도 단계로 정리했다.

작은 수작업 파일럿으로 충분히 확인할 수 있는 가설이라면 먼저 그 경계를 정하는 방법을 제안한다. 이것은 작성자의 운영 제안이지, Toris가 이미 해당 방식으로 매출을 검증했다는 주장이 아니다.

### 2. 예산 알림, 제공자의 지출 차단, 앱의 작업 허용 판단은 다르다

Google Cloud의 [알림 전용 예산](https://docs.cloud.google.com/billing/docs/how-to/budgets)은 사용을 직접 차단하지 않는다. 그러나 [지출 차단 예산](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps)은 별도 기능이므로 ‘클라우드는 예산 차단 기능이 없다’라고 일반화하지 않는다. 적용 서비스, 지연, 이미 실행 중인 작업, 계속 청구되는 비용을 확인해야 한다. [Supabase 비용 통제](https://supabase.com/docs/guides/platform/cost-control#spend-cap)도 적용 제외 항목이 있으므로 전체 청구액 상한과 같다고 보지 않는다.

앱 안에서는 이미 쓴 비용뿐 아니라 동시 실행 중인 작업이 예약한 비용도 고려한다. `사용 비용 + 예약 비용 + 새 작업 최대 비용`을 하나의 원자적 처리로 확인하는 구조를 제안했다. 단순 산술 검사가 실제 동시성 통제를 증명하지는 않는다.

### 3. 결제 알림을 받는 것과 권리를 한 번만 지급하는 것은 다르다

[Paddle 이벤트 전달](https://developer.paddle.com/webhooks/about/how-webhooks-work/)은 중복과 순서 역전을 고려해야 한다. 전달 알림의 식별자, 구매·구독의 식별자, 실제 포인트·권한 지급의 식별자를 분리한다. 인증된 이벤트를 복구 가능한 저장소에 남긴 뒤 접수를 응답하고, 실제 지급은 트랜잭션 또는 멱등적인 복구 구조로 처리하도록 했다.

[Google Play 구매 검증](https://developer.android.com/google/play/billing/security)에서는 결제 대기와 구매 완료를 구분한다. 이미 본 구매 토큰은 중복 지급을 막는 데 사용하되, 구독 상태의 이후 갱신까지 모두 무시해서는 안 된다. [RTDN](https://developer.android.com/google/play/billing/rtdn-reference)은 완전한 구매 상태가 아닌 변경 신호이므로 확인 절차가 따로 필요하다.

### 4. 사용자가 적다면 결론의 강도도 낮춰야 한다

[PostHog의 표본 계획 예제](https://posthog.com/docs/experiments/sample-size-running-time)는 기준 전환율 10%, 상대 최소 감지 효과 20%에서 근사식으로 집단당 3,600회, 두 집단 합계 7,200회를 산출한다. 이를 독립적으로 재계산하는 예제를 넣었지만, 모든 실험의 최소 표본이나 정확한 검정력 계산으로 일반화하지 않는다.

설정한 배정 비율과 관측 노출 비율이 크게 다르면 성과보다 데이터 무결성을 먼저 확인한다. 아직 7일이 지나지 않은 사용자의 7일 유지율은 0이 아니라 미관측이다. [SRM 연구 초록](https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/)과 [코호트 유지율 정의](https://posthog.com/docs/product-analytics/retention)를 참고했다. 전체 논문을 읽거나 실제 고객 분석을 실행한 것은 아니다.

## 충돌한 자료를 처리한 방식

RevenueCat 보고서의 일부 스토어별 수치는 본문의 특정 항목과 다른 요약 항목이 일치하지 않았다. Google Cloud 지출 차단의 복원·초기화 설명도 검색 결과와 열어 본 본문 사이에 차이가 있었다. 이 세 항목은 `excluded`에 **quarantined**로 보존하고 수치 비교·매출 예측·자동화 규칙에서 제외했다. 불일치 원인을 확인한 것처럼 쓰지 않는다.

채택한 RevenueCat 숫자도 2025년 대상 기간의 일정 조건을 충족한 연동 앱에 관한 관측 통계다. [보고서](https://www.revenuecat.com/state-of-subscription-apps)의 접근 방식별 전환율 차이를 내 앱에 유료벽을 넣었을 때의 인과적 상승률로 해석하지 않는다. 실제 적용 때는 최신 문서와 현재 프로젝트 조건을 다시 확인한다.

## 바로 사용하는 요청 예시

로컬 파일 접근이 가능한 현재 에이전트에 아래처럼 전달한다. 전역 스킬 설치나 다른 에이전트 위임이 완료됐다는 의미는 아니다.

```text
~/projects/product-growth-skills/toris-demand-validation/SKILL.md를 읽고,
이 아이디어의 고객 문제·현재 대안·수요 근거를 구분해.
추가 결제 없이 할 수 있는 최소 검증과 지속·수정·중단 조건을 작성해.
실행하지 않은 고객 인터뷰나 결제를 실제 결과로 기록하지 마.
```

```text
~/projects/product-growth-skills/toris-cost-guardrails/SKILL.md를 읽고,
현재 프로젝트의 유료 호출·동시 작업·재시도를 점검해.
알림과 실제 차단을 구분하고, 허용된 로컬 코드만 수정·검증해.
운영 서비스의 요금제·계정·차단 설정은 바꾸지 마.
```

```text
~/projects/product-growth-skills/toris-billing-reliability/SKILL.md를 읽고,
현재 결제 연동의 중복 지급·이벤트 순서·결제 대기·만료 처리를 검토해.
실제 결제·환불 없이 로컬 회귀 테스트와 복구 설계를 만들어.
```

```text
~/projects/product-growth-skills/toris-small-sample-experiments/SKILL.md를 읽고,
제공한 데이터의 분모·기간·배정·코호트 성숙도를 먼저 확인해.
관측된 변화와 통계적으로 판단할 수 있는 범위를 구분해서 보고해.
데이터가 없거나 부족하면 수치를 만들거나 승자를 강제로 정하지 마.
```

## 설치·공유 경계

각 스킬은 같은 저장소의 `shared-references/`와 `research/`를 참조한다. 폴더 하나만 따로 복사하면 참조가 빠질 수 있으므로 원본 저장소의 상대 구조를 유지한다. 설치 경로·호출 방식은 사용하는 런타임에서 별도 확인해야 한다.

개인 원장의 경험과 이번 공개 연구 데이터는 분리했다. 과금·계정 변경, 커밋·푸시, 전역 설치, 외부 게시, 자동화 생성은 이 문서 작성에 포함되지 않는다.

## 로컬 검증

[실행 결과 기록](../../research/solo-developer-2026-10-15/VERIFICATION.md)에 검사 범위와 결과를 남겼다. Python 테스트 28개와 전체 스킬 12개 구조 검사는 통과했다. 기존 릴리스 테스트는 기존 `.DS_Store` 파일을 예상 밖 항목으로 감지해 중단됐고, 이후 테스트는 미실행이다. 기존 파일을 삭제하거나 검사를 완화하지 않았다.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_research.py --as-of 2026-10-15
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_skills.py
git diff --check
```

실제 에이전트별 행동 검증, 운영 결제, 비용 차단, 사용자 실험은 미실행이다. 가상 상황이 문서에 있다는 사실과 해당 상황을 실제로 통과했다는 주장은 별개다.
