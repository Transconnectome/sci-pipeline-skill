# 레포 진입 문서 4종 — 생성·갱신 프롬프트 (도구 중립)

Claude Code · Codex CLI · Antigravity 어디에나 아래 `---` 사이를 붙여 쓴다. `<레포 경로>`만 바꾼다.

---
`<레포 경로>`에서 sci-pipeline 진입 문서 4종 — `AGENTS.md` · `CLAUDE.md` · `WORKPLAN.md` · `README.md` — 를 만들거나 갱신한다.

1. **실측부터 한다.** `git status`, `git log --oneline -5`, 디렉토리 목록, 기존 4종 문서 · `HANDOFF.md` · 데이터 사전 · 테스트 명령을 읽는다. 상태는 지금 실행한 명령 결과로만 적고, 상태 문장마다 측정 시각과 근거(명령·파일)를 붙인다.
2. **있으면 고치고, 없을 때만 만든다.** 같은 역할 문서가 이미 있으면(예: `docs/PLAN.md`가 작업 계획 역할) 그것을 그 역할로 쓰고 새로 만들지 않는다. 위치가 레포 관례와 다르면(예: `docs/WORKPLAN.md`) 관례를 따른다.
3. **정본은 한 곳.** 도구 중립 규칙(읽는 순서·멈추는 규칙·명령) = `AGENTS.md` / Claude 전용(스킬·리뷰 에이전트·훅) = `CLAUDE.md`, 첫 줄 `@AGENTS.md` / 측정 상태·게이트 진행표·멈춤 조건·다음 계획 = `WORKPLAN.md` / 사람용 입구 = `README.md`(게이트는 링크만). 같은 내용을 두 문서에 쓰지 않는다.
4. **템플릿**: sci-pipeline `assets/agents_md.template.md` · `claude_md.template.md` · `workplan.template.md` · `readme.template.md`.
5. **지어내지 않는다.** 모르는 값은 `UNSET` + `fixed_when`. 수치·날짜·인물·결정을 만들지 않는다. 1차 질문 · δ · 주지표 · 봉인 여부는 PI 결정으로 남긴다. 자료 형식·접근은 질문이 아니라 실측 과제로 적는다.
6. **게이트 판정은 UNSET / 미확인 / N/A까지만** 적는다. 작성자가 자기 게이트를 PASS로 적지 않는다(통과 결정은 PI, 리뷰어 판정은 권고).
7. **G9**: "최초" 같은 선점 표현 금지. 수치는 DOI/PMID 또는 `[확인 필요]`.
8. **보고**: 4개 파일 경로, 새로 만든 것 / 고친 것, 남은 UNSET 목록, 지금 걸린 멈춤 조건. 커밋은 요청이 있을 때만 한다.
---

실례: `~/git/dolittle` (2026-10-06) — `docs/WORKPLAN.md` §4가 다음 계획의 정본, `CLAUDE.md`는 `@AGENTS.md` + 단계별 스킬 표.
