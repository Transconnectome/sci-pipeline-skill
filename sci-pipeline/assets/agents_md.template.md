# AGENTS.md — <레포 이름> (도구 중립 에이전트 안내)

> Claude Code · Codex CLI · Antigravity가 함께 읽는다. 도구별 추가 사항은 `CLAUDE.md` 등에 두고 여기에 복제하지 않는다.
> 상태·게이트 판정은 여기에 적지 않는다 — 정본은 `WORKPLAN.md`.

## 읽는 순서

1. 이 파일 → 2. `CLAUDE.md`(Claude Code만) → 3. `WORKPLAN.md` §1 상태 · §4(c) 게이트 · §4(d) 멈춤 조건 → 4. `HANDOFF.md`(있으면)
5. 시작 전에 `git status`·`git worktree list`를 본다. 이 레포의 규칙이 sci-pipeline 스킬보다 우선한다.

## 이 레포의 질문

- 핵심 목표 한 문장: UNSET (fixed_when: G1 / PI) — 확장 과제로 강등하지 않는다
- 연구 모드: UNSET (`EXPLORATORY` / `CONFIRMATORY` / `REPLICATION`)
- 독립 단위: UNSET (fixed_when: G1 / 통계)

## 멈추는 규칙 (sci-pipeline 게이트)

- G2 자료 계약 위반은 halt한다. 자동 교정·재정렬·합성 자료로 조용히 대체하지 않는다.
- G3 분할은 <독립 단위> 단위. 전처리·특징 선택·튜닝은 전부 fold 안.
- G4 확인 자료는 봉인하고 저장소에는 해시만 둔다. 한 번 보면 burned로 기록한다.
- G5 동결 카드 없이 확인 실험을 하지 않는다. 카드 커밋이 결과 커밋보다 먼저다.
- G6 implement는 합성 고정구부터. 실패하면 기준을 낮추지 않고 실패로 남긴다.
- G7 실패 포함 모든 run을 장부에 남긴다. G8 판정 어휘는 keep/modify/stop/inconclusive/no_candidate.
- G9 상태 문장에는 측정 시각과 근거 파일을 붙인다. 수치는 DOI/PMID 또는 `[확인 필요]`. "최초" 금지. 작성자가 자기 게이트를 PASS로 적지 않는다.

## 명령

| 목적 | 명령 |
|---|---|
| 테스트 | UNSET |
| 카드 동결·검증 | `python3 <sci-pipeline>/scripts/freeze_card.py freeze|verify <card>` |
| 분할 중복 점검 | `python3 <sci-pipeline>/scripts/group_overlap_audit.py ...` |

## 다루지 말 것

- 원자료·식별자 위치: UNSET (Git 밖 승인 위치)
- 비밀값이 든 설정 파일을 읽거나 출력하지 않는다.
