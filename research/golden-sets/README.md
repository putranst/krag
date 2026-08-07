# IsRAG Golden Set

## `israg-v1.jsonl`

Version 1 is a **synthetic evaluation scaffold** containing 200 bilingual reference items:

- 5 domains × 40 items: agriculture, Islamic finance, indigenous land rights, public health, digital governance
- 100 English + 100 Malay items
- 20 items per language in each domain
- JSONL, one object per line

Each item includes a query, reference answer, acceptable-answer points, domain/language labels, cultural context, and basic provenance fields. The current records are explicitly marked:

```text
annotation_status: reference_answer_pending_expert_review
```

They must not be presented as measured results or final human-authored ground truth. Before an academic submission, add citations, independent bilingual domain-expert annotations, adjudication, inter-annotator agreement, and relevant ethics/data-governance review.

## Rebuild

```bash
python3 research/golden-sets/build_israg_golden_set.py
```

The builder is deterministic and overwrites `israg-v1.jsonl`.

## Validation

```bash
python3 - <<'PY'
import json
from collections import Counter
from pathlib import Path
p = Path('research/golden-sets/israg-v1.jsonl')
rows = [json.loads(line) for line in p.read_text().splitlines()]
assert len(rows) == 200
assert Counter(r['language'] for r in rows) == {'en': 100, 'ms': 100}
assert all(v == 40 for v in Counter(r['domain'] for r in rows).values())
print('golden set valid')
PY
```

See `research/papers/paper-1-israg.md`, §4.1.

## License and release note

No external dataset is redistributed here. Treat the generated content as project research material pending project-level licensing, source citation, expert review, and release approval.
