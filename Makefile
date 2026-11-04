.PHONY: start

start:
	cd codex-hooks-workshop/presentation && \
		{ test -d node_modules || npm ci --ignore-scripts; } && \
		npm run dev
