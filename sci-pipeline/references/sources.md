# 근거와 차용 출처

DOI는 2026-10-03 Crossref에서 해석 확인. 저장소는 같은 날 `gh api`로 SKILL.md·라이선스를 직접 확인.

## 체크리스트·방법론 (gates.md 약칭 → 원문)

| 약칭 | 원문 | 쓰는 게이트 |
|---|---|---|
| REFORMS | Kapoor et al. 2024, *Sci Adv*, 10.1126/sciadv.adk3452 | G1·G3·G8·G9 |
| Kapoor & Narayanan | Leakage and the reproducibility crisis, *Patterns* 2023, 10.1016/j.patter.2023.100804 | G3·G4 |
| TRIPOD+AI | Collins et al. 2024, *BMJ*, 10.1136/bmj-2023-078378 | G1·G8 |
| PROBAST+AI | Moons et al. 2025, *BMJ*, 10.1136/bmj-2024-082505 | G1·G3·리뷰 |
| Varoquaux 2017 | *NeuroImage*, 10.1016/j.neuroimage.2016.10.038 | G3 |
| Varoquaux 2018 | *NeuroImage*, 10.1016/j.neuroimage.2017.06.061 | G8 |
| Poldrack 2020 | Poldrack, Huckins & Varoquaux, *JAMA Psychiatry*, 10.1001/jamapsychiatry.2019.3671 | G1·G3 |
| Rosenblatt 2024 | *Nat Commun*, 10.1038/s41467-024-46150-w | G3 |
| Wilson & Collins 2019 | *eLife*, 10.7554/eLife.49547 | G6 |
| SBC | Modrák et al., *Bayesian Anal.*, 10.1214/23-BA1404 | G6 |
| Nosek 2018 | *PNAS*, 10.1073/pnas.1708274114 | G5 |
| van den Akker 2021 | 2차 자료 사전등록 템플릿, *Meta-Psychology*, 10.15626/MP.2020.2625 | G5 |
| Hosseini 2020 | Lockbox, *Neurosci Biobehav Rev*, 10.1016/j.neubiorev.2020.09.036 | G4 |

## AI 연구 에이전트 실패 근거

| 약칭 | 원문 | 반영 |
|---|---|---|
| SciIntegrity-Bench | arXiv:2605.10246 — 실자료 부재 시 시험한 7개 모델 모두 합성 자료 생성 | G2 조용한 대체 금지 |
| Luo et al. | arXiv:2509.08713 (NeurIPS 2025) — 부적절한 벤치마크·누수·지표 오용·사후 선택 | G3·G8, 리뷰어는 trace를 읽음 |
| METR | metr.org/blog/2025-06-05-recent-reward-hacking — 평가기 패치·타이머 덮어쓰기 | G7 평가 코드 해시 고정 |
| Agent Laboratory | arXiv:2501.04227 — 자동 리뷰 6.1 vs 인간 3.8 | 리뷰어 점수 금지·판정은 권고 |
| ResearchCodeBench | arXiv:2506.02314 — 실패의 58.6%가 돌지만 틀린 코드 | G6 정답 고정구 |
| Anthropic | anthropic.com/research/long-running-Claude · /claude-shaped-science | G6 매개변수 범위, G9 완료 증거 |

## 차용한 공개 스킬 (모두 MIT)

| 저장소 | 차용한 것 | 방식 |
|---|---|---|
| github.com/MagicalLiHua/conduct-deep-learning-research | 연구 모드 3분류, 계약 동결 필드, 실패 유형 분류, 멈춤 조건 구조 | 개념·구조 차용, 문장은 새로 씀. `freeze_card.py`는 `freeze_experiment_contract.py`의 "기존 스냅샷과 해시 불일치 시 거부" 구조를 참고해 새로 작성 |
| github.com/K-Dense-AI/claude-scientific-skills | `exploratory-data-analysis/scripts/missingness_leakage_audit.py`의 분할 간 개체·시간 중복 점검과 "중복 없음은 독립성 증명이 아님" 문구 | `group_overlap_audit.py`를 표준 라이브러리로 새로 작성(가족 단위 추가) |
| github.com/Orchestra-Research/AI-research-SKILLs | `0-autoresearch-skill`의 "프로토콜 커밋이 결과 커밋보다 먼저", `rigor-reviewer`의 탐색 무결성 차원 | G5 항목, 리뷰어 점검 항목 |
| github.com/austin-starks/Public-Portfolio-Challenge `skills/lockbox-holdout` | 본 락박스 = burned, 예외 시 기록 | G4 항목 |
| github.com/obra/superpowers `requesting-code-review` | 리뷰어에게 세션 기록 대신 큐레이션한 산출물 전달 | SKILL.md §6 |

## 코드 쪽 도구 권고

- 자료 계약 halt: pandera (10.25080/Majora-342d178e-010), pydantic
- 분할: scikit-learn `StratifiedGroupKFold`, nested CV
- 실행 기록: DataLad (10.21105/joss.03262), DVC, Snakemake (10.12688/f1000research.29032.2)
- Deepchecks는 행 단위 점검이라 참가자 단위 누수 판단에 쓰지 않는다.
