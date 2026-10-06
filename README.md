# sci-pipeline-skill

과학·ML 연구 파이프라인(자료 → 분할 → 모델 → 평가 → 판정)을 **설계·구현·감사**할 때 쓰는 에이전트 스킬과 읽기 전용 리뷰 에이전트.
Claude Code, Codex CLI, Antigravity에서 같은 스킬 폴더를 공유한다.

이 스킬은 문서를 만드는 도구가 아니라, **결과를 보기 전에 정할 것을 정하게 하고 정하지 않았으면 멈추게 하는 얇은 게이트 절차**다.

## 게이트 9개

| # | 게이트 | 핵심 |
|---|---|---|
| G1 | 목표·추정량 | 1차 질문 1개, 성과는 기준선 대비 증분으로만 |
| G2 | 자료 계약 | 위반 시 halt, 자동 교정·합성 자료로 조용한 대체 금지 |
| G3 | 분할·누수 | 참가자(가족·기관) 단위, 모든 적합은 fold 안 |
| G4 | 봉인 확인 분할 | 사전등록 후 한 번만, 본 적 있으면 burned |
| G5 | 동결 카드 | 한 요소만 변경, 미정은 `UNSET`, sha256 동결 + 커밋 고정 |
| G6 | 합성 고정구 | 정답을 아는 입력을 매개변수 범위에서 회수, 합성으로 전망 금지 |
| G7 | 실행 기록·환경 | 실패 포함 장부, 평가 코드 해시 고정, 환경별 수치 동작 |
| G8 | 판정 분류 | keep / modify / stop / inconclusive / no_candidate, 소프트웨어 실패 ≠ null |
| G9 | 상태 분리·주장 | 문서·합성·구현·실자료·재현·임상을 따로, 작성자 ≠ 리뷰어 |

모드는 `design`(카드 동결 전 구현 금지), `implement`(고정구 먼저, TDD), `audit`(새 파일 0개) 세 가지다.

레포 안에서 설계를 시작하면 **진입 문서 4종**(`AGENTS.md` 도구 중립 규칙 · `CLAUDE.md` = `@AGENTS.md` + Claude 전용 · `WORKPLAN.md` 측정 상태와 게이트 진행표 · `README.md` 사람용 입구)을 없을 때만 만들고 있으면 고친다. 정본은 한 곳에만 두고, 모르는 값은 `UNSET`으로 남긴다. 생성 프롬프트는 [`sci-pipeline/references/repo_docs_prompt.md`](sci-pipeline/references/repo_docs_prompt.md).

## 구성

```
sci-pipeline/          스킬 본체 (SKILL.md, references/, assets/ — 카드·자료 계약·진입 문서 4종 템플릿, scripts/, evals/)
agents/                Claude Code용 pipeline-reviewer 서브에이전트 템플릿
install.sh             세 도구에 symlink + 리뷰어 에이전트 렌더
```

`scripts/`는 표준 라이브러리만 쓴다.
- `freeze_card.py freeze|verify|unset <card>` — 실험 카드 sha256 동결·검증(`--strict`, `--expect <커밋된 해시>`)
- `group_overlap_audit.py` — 분할 간 참가자·가족·시간 중복, 공백·대소문자만 다른 id 탐지

## 설치

```bash
git clone https://github.com/Transconnectome/sci-pipeline-skill.git
cd sci-pipeline-skill && ./install.sh
```

## 근거

체크리스트는 REFORMS, Kapoor & Narayanan 누수 분류, TRIPOD+AI, PROBAST+AI, 신경영상 교차검증 문헌, Wilson & Collins 회수 시험 등에서, 사고 사례는 세 비공개 연구 프로젝트에서 왔다. 공개 스킬(conduct-deep-learning-research, K-Dense claude-scientific-skills, Orchestra AI-research-SKILLs, lockbox-holdout, superpowers)에서 구조·개념을 차용했다(모두 MIT). 목록과 DOI는 [`sci-pipeline/references/sources.md`](sci-pipeline/references/sources.md).

## 한계

- 리뷰 에이전트는 Write·Edit 도구가 없지만 Bash 쓰기는 지시로만 막는다.
- 리뷰어 판정은 권고이고 게이트 통과는 사람이 결정한다.
