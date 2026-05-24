# DLT-Proof-Writing skill — dev / install Makefile.
#
# Usage:
#     make install     # symlink ~/.claude/skills/dlt-proof-writing → ./proof-writing-skill
#     make uninstall   # remove the symlink
#     make lint-self   # run lint.py on the eval_results fixtures
#     make test-evals  # run the eval harness
#
# The symlink approach matches Claude Code's documented dev workflow:
# edits in the source repo take effect within the current session
# without restart (file watcher on ~/.claude/skills/).

SKILL_NAME := dlt-proof-writing
SRC        := $(CURDIR)/proof-writing-skill
INSTALL    := $(HOME)/.claude/skills/$(SKILL_NAME)

.PHONY: install uninstall lint-self test-evals help

help:
	@echo "Targets:"
	@echo "  install     — symlink $(INSTALL) → $(SRC)"
	@echo "  uninstall   — remove symlink at $(INSTALL)"
	@echo "  lint-self   — lint the in-repo eval_results fixtures"
	@echo "  test-evals  — run the eval harness (if present)"

install:
	@if [ -L "$(INSTALL)" ]; then \
	  echo "Removing existing symlink at $(INSTALL)"; \
	  rm "$(INSTALL)"; \
	elif [ -e "$(INSTALL)" ]; then \
	  echo "ERROR: $(INSTALL) exists and is NOT a symlink."; \
	  echo "       Manually move or remove it first (it may contain"; \
	  echo "       user-edited data — back up before deleting)."; \
	  exit 1; \
	fi
	@mkdir -p "$(HOME)/.claude/skills"
	ln -s "$(SRC)" "$(INSTALL)"
	@echo "Installed: $(INSTALL) → $(SRC)"
	@echo "Edits to $(SRC) take effect immediately (no restart)."

uninstall:
	@if [ -L "$(INSTALL)" ]; then \
	  rm "$(INSTALL)"; \
	  echo "Removed symlink at $(INSTALL)."; \
	else \
	  echo "No symlink at $(INSTALL); nothing to do."; \
	fi

lint-self:
	@find "$(CURDIR)/eval_results" -name "*.tex" -print0 2>/dev/null | \
	  xargs -0 -r python3 "$(SRC)/scripts/lint.py" || true

test-evals:
	@if [ -x "$(SRC)/evals/run.py" ] || [ -f "$(SRC)/evals/run.py" ]; then \
	  python3 "$(SRC)/evals/run.py"; \
	else \
	  echo "No eval runner at $(SRC)/evals/run.py — adapt this target"; \
	  exit 1; \
	fi
