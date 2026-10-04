#!/usr/bin/env bash
# Link the skill into Claude Code / Codex / Antigravity skill dirs and render the reviewer agent.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$REPO/sci-pipeline"
SKILL_DIR="${SKILL_DIR:-$HOME/.agents/skills/sci-pipeline}"   # canonical shared location

mkdir -p "$(dirname "$SKILL_DIR")"
if [ -e "$SKILL_DIR" ] && [ ! -L "$SKILL_DIR" ]; then
  echo "refusing: $SKILL_DIR exists and is not a symlink (move it first)" >&2; exit 1
fi
ln -sfn "$SKILL_SRC" "$SKILL_DIR"

for d in "$HOME/.claude/skills" "$HOME/.codex/skills" "$HOME/.gemini/skills"; do
  [ -d "$d" ] || continue
  ln -sfn "$SKILL_DIR" "$d/sci-pipeline"
  echo "linked $d/sci-pipeline -> $SKILL_DIR"
done

if [ -d "$HOME/.claude/agents" ]; then
  sed "s#{{SKILL_DIR}}#$SKILL_DIR#g" "$REPO/agents/pipeline-reviewer.md" > "$HOME/.claude/agents/pipeline-reviewer.md"
  echo "rendered $HOME/.claude/agents/pipeline-reviewer.md"
fi
