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

## Concept-focused presentation revision — 2026-11-05

The main deck now has 34 slides focused on hook behavior and contracts; the short deck has 9. A brief launcher introduction precedes the event examples in both decks. Workshop routes, replay instructions, and detailed setup remain in the guides. Event slides show the matching ./demo.sh NN launcher command, its working directory, a scenario prompt, and any explicit trigger action. Matcher semantics now have dedicated examples showing tool-name filtering, command inspection in the handler, and the field matched by each event. Official contract links remain visible.

The full deck builds and exports; the rendered slides were visually reviewed. This documentation-only revision does not change hook implementations or claim additional live CLI verification.

## Manifest discovery revision — 2026-11-05

- Migrated all 18 scenario descriptions into per-directory manifest.json files.
- Launcher, list, replay, and reset discover scenario directories without a central registry.
- 19 unit tests passed, including automatic new-case discovery/launch, duplicate IDs, malformed metadata, directory/event mismatches, aliases, per-manifest launch settings, and reset of a newly discovered case.
- All 43 synthetic hook fixture cases passed through standalone replay. Both ID and directory-name replay selectors were checked.
- Both slide decks build. The updated launcher-introduction slide was exported and visually reviewed.

Launcher tests use a fake Codex executable to verify arguments. These checks do not add live Codex hook-delivery evidence.
