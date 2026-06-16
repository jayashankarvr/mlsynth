# Limitations

mlsynth never emits a form it has not verified; when it cannot, it raises
`NotImplementedError` (a supported class, but that case or number is not encoded) or
`UnsupportedRoot` (the root fits no class). The items below are genuine constraints.
Planned-but-unbuilt features (gender derivation, clitics, postpositions, stylistic
variants) are tracked as future work in the README, not here.

## Plurals: partial coverage

- The classes `am_neuter`, `vowel_anuswara`, `i_vowel`, `u_vowel`, and `ṭ_geminate` have
  plurals. `a_stem` and the chillu classes do not yet: their plurals are
  animacy-conditioned (`-മാർ` human versus `-കൾ` inanimate, with irregulars like `മക്കൾ`),
  which is not predictable from the stem shape and is not yet modelled. Requesting one
  raises `NotImplementedError`.

## Distinctions the input does not carry

- **`u_vowel` and `a_stem` match broadly.** A malformed lemma (a samvruthokaram half-u
  written as a bare `-ു` instead of `-്`, or truncated text) is inflected rather than
  rejected, so callers must pass well-formed lemmas.
- Without an `animacy` argument the accusative defaults to the overt form; the zero-marked
  inanimate accusative needs `animacy=INANIMATE`.

## Out of scope

- **Verbs** (this package synthesizes nouns only).
- **Noun compounding and external sandhi**: joining two lemmas (e.g. ആന + കുട്ടി →
  ആനക്കുട്ടി, with gemination) is a separate problem from single-lemma inflection.
