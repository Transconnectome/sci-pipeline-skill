# CLAUDE.md — <레포 이름>

@AGENTS.md

## Claude Code 전용

- 세션을 시작하면 `WORKPLAN.md` §1 상태와 §4(d) 멈춤 조건부터 읽는다.
- 단계별 스킬: 설계·감사 = `sci-pipeline` · 독립 리뷰 = `pipeline-reviewer` 에이전트(요약이 아니라 원문 경로와 git diff를 준다, 리뷰 전후 `git status --porcelain` 동일 확인) · 아이디어→가설 = `sci-method` · 교차검증 = `trinity` · 인계 = `handoff-doc` · (레포 성격에 따라 추가 — 예: 문헌 KB = `nlmcreater`)
- 이 레포 고유 훅·권한·MCP: UNSET
