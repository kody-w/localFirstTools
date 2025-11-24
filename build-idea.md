<idea> prompt compressor              

taking very long prompts, like 7000 lines, aka 75k tokens

and compressing them by a set %, such as 35%, without losing essential context </ idea>

‹problem> the fact that when i just tried this, with GPT-5-high, that has 400k context window, and told it very clearly what i want, and to achieve a 30% length reduction, it managed to turn 7000 lines into 266 lines

which is more like 96% reduction </problem>

‹approach> you cannot do this in one shot.

you have to first split the long prompt into chunks, rate each chunk in terms of relevance, and then run an LLM on each chunk separately, one by one, starting with the least-relevant chunk

and constnatly checking the total token counnt 




Six-step implementation plan 1. Structured Chunking: Markdown-aware chunker (headings, code fe lists) with stable IDs and token counts; never split code or seman 2. Hybrid Relevance Scoring: Combine heuristics (rules/constraints/ schema/identifiers) with GPT-4.1 ratings; maintain a priority queue re-rate neighbors on change. 3. Budget Orchestration: Set strict global token target (tiktoken) with

margin; allocate dynamic per-chunk budgets; gate progress on measured tokens. 4. Iterative Compression: Compress least-relevant largest chunks first via GPT-4.1 with strict prompts; tighten via a small binary-search loop to fit budgets. 5. Dedup + Stitch: Detect cross-chunk redundancy; canonicalize repeats; run a brief global cohesion pass with GPT-4.1 to adjust connectors without increasing tokens. 6. Validation + UX: Provide CLI with dry-run/metrics and deterministic settings (temp=0); safety rails (min-chunk size, rollback); unit tests for chunking/scoring/budgeting.

Simplified Six-Step Plan
1. Chunk Input: Split into Markdown-aware chunks with stable IDs; never split code; compute token counts; mark must-keep spans.
2. Score Relevance: Rate each chunk with simple heuristics (must-keep, keywords, headings, references); optionally one GPT-4.1 pass to break ties; order least-to-most relevant.
3. Set Target & Track: Use the user’s desired length/percent to compute a token target; maintain a running total from current chunks.
4. Compress Iteratively: Starting with the least-relevant chunks, ask GPT-4.1 to shorten while preserving facts/code; replace the chunk and update its token count each time.
5. Check & Stop: After each change, recompute total tokens; stop when at or under target; on bad outputs, revert that chunk and move on.
6. Output & Verify: Reassemble in original order; quick checks: must-keep spans unchanged and links intact; output compressed text plus before/after token metrics.
