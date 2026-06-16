# mlsynth

A rule-based Malayalam morphological synthesizer. It does forward
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

Alpha. Eleven ending-conditioned noun classes across 11 cases, covering the major
Malayalam noun shapes, with every encoded form native-ratified (`verified=True`); shapes
outside the supported classes raise rather than guess. Five classes (`am_neuter` മരം,
`vowel_anuswara` കലാം, `i_vowel`
കുട്ടി/സ്ത്രീ, `u_vowel` പശു, `ṭ_geminate` വീട്) are complete in singular and plural;
`a_stem` (അമ്മ) and the chillu classes (`അവൻ`, `മകൾ`, `കാർ`, `കാൽ`, `തൂൺ`) are
singular-complete; their plurals are animacy-conditioned across the full paradigm
(inanimate `-കൾ`/`-ഉകൾ`, human `-മാർ`/`-ന്മാർ`/`-കാർ`, animate `-കൾ`). Suppletive personal
pronouns (ഞാൻ, നീ, അവർ, നാം, താൻ, ഇവൻ) are handled through an exception table rather than
the rule engine. A `derive_feminine` helper builds a feminine lemma from a masculine base
(എഴുത്തുകാരൻ → എഴുത്തുകാരി) before inflection. Includes differential object marking and a
synthetic/colloquial register for the instrumental. See [`LIMITATIONS.md`](LIMITATIONS.md)
for the precise gaps. Clitics/postpositions, stylistic variants, and verbs are future work.

## Install

```bash
pip install mlsynth
# from source:
pip install -e ".[dev]"
```

## License

Apache-2.0. See `LICENSE` and `NOTICE`. Contributions are accepted under Apache-2.0
§5 (inbound = outbound); no separate CLA is required.

Linguistic sources are credited in `REFERENCES.md`.
