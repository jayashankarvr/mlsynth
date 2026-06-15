# mlsynth

A permissive, rule-based Malayalam morphological synthesizer. It does forward
morphological generation: given a root and grammatical features, it produces the
inflected surface form (the counterpart to morphological analysis/segmentation).

```python
from mlsynth import synthesize_noun, Case, Number

synthesize_noun("മരം", Case.LOCATIVE).surface          # 'മരത്തിൽ'
synthesize_noun("മരം", Case.GENITIVE).surface          # 'മരത്തിന്റെ'
synthesize_noun("കുട്ടി", Case.GENITIVE).surface        # 'കുട്ടിയുടെ'
synthesize_noun("മരം", Case.NOMINATIVE, number=Number.PLURAL).surface  # 'മരങ്ങൾ'
```

## Why this exists

Existing Malayalam morphology tools are either copyleft (Apertium, libindic =
GPL/AGPL) or, in the case of the one permissive *generator* (`mlmorph`, MIT), built
on a GPL FST runtime. There is no permissive, dependency-clean, rule-based Malayalam
**synthesizer**. `mlsynth` aims to fill that gap with a small pure-Python rule engine
and no copyleft dependencies.

## Design

- **Declarative, provenance-tagged rules** (`mlsynth/rules.py`): each rule cites the
  source it was drawn from and carries a `verified` flag that is `True` only when the
  form has been ratified by a native reviewer. Adding or correcting a paradigm is a
  data edit, not a code change.
- **Inspectable results**: every `synthesize_noun(...)` returns a `SynthResult` with the
  `surface` form, the `morphemes` that compose it, the `stem_class`, the `provenance`
  key, and `verified`. Feature combinations that are not yet encoded raise rather than
  return a silently wrong form.
- **Akshara-correct joins**: suffixes are represented matra-initial so concatenation
  produces correct conjuncts/vowel signs; the genitive uses the canonical *nta* form
  (NA + virama + RRA).

## Status

Alpha. Five ending-conditioned noun classes: `am_neuter` (മരം) and `i_vowel` (കുട്ടി)
are complete across 11 cases (singular and plural); `vowel_anuswara` (കലാം), `u_vowel`
(പശു), and `ṭ_geminate` (വീട്) are partial. Includes differential object marking and a
synthetic/colloquial register for the instrumental. Most forms are native-ratified
(`verified=True`); a few are SMC-sourced pending sign-off (`verified=False`). See
[`LIMITATIONS.md`](LIMITATIONS.md) for exactly what is unsupported. Remaining noun
classes (a/e-stems, chillu), verbs, and pronouns are future work.

## Install

```bash
pip install mlsynth        # once published
# from source:
pip install -e ".[dev]"
```

## License

Apache-2.0. See `LICENSE` and `NOTICE`. Contributions are accepted under Apache-2.0
§5 (inbound = outbound); no separate CLA is required.

The implemented linguistic rules are **facts** restated in our own code; no source's
text, tables, code, or data is reproduced. Sources are credited in `REFERENCES.md` as
scholarship; that implies no endorsement and creates no license obligation.
