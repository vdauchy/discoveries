# Verification record

Checked 2026-11-04 against local codex-cli 0.166.0.

- `python3 -m unittest discover -s codex-hooks-workshop/tests -v`: 8 tests passed, including 43 isolated fixture cases and launcher selection for all 18 labs.
- `sh -n codex-hooks-workshop/demo.sh`: passed.
- `make -n start`: retains the existing single start target.
- `npm run build` from presentation/: passed.
- Slidev PDF export: 49 pages rendered; all pages visually reviewed via rendered contact sheets, with individual code slides also inspected.
- Generated app-server schema: all 14 documented event names found in installed ManagedHooksRequirements; support snapshot saved in reference/.

These checks do not invoke a Codex model session. Trust, matcher dispatch, permission policy, tool enforcement, compaction scheduling, child-agent lifecycle, background output delivery, spilling, and session closure have not been live-rehearsed. LIVE-CHECKLIST.md remains unmarked. Synthetic replay of the MCP exchange is not Codex callback integration evidence.

Temporary rendered PDFs and review images are QA artifacts in /tmp, not repository deliverables.
