# Limitations

mlsynth never emits a form it has not verified; when it cannot, it raises
`NotImplementedError` (a supported class, but that case or number is not encoded) or
`UnsupportedRoot` (the root fits no class). The items below are genuine constraints:
distinctions the orthography does not carry, and problems outside this package's scope.
Planned-but-unbuilt features (postpositions, stylistic variants) are tracked as
future work in the README, not here.

## Distinctions the input does not carry

- **Animacy is not recoverable from spelling.** `a_stem` and chillu plurals therefore
  require an explicit `animacy` and raise without it, since `-മാർ` (human) versus `-കൾ`
  (inanimate) is not predictable from the stem. For the same reason the accusative
  defaults to the overt form; the zero-marked inanimate accusative needs
  `animacy=INANIMATE`.
- **`u_vowel` and `a_stem` match broadly.** A malformed lemma (a samvruthokaram half-u
  written as a bare `-ു` instead of `-്`, or truncated text) is inflected rather than
  rejected, so callers must pass well-formed lemmas.

## Out of scope

- **Verbs** (this package synthesizes nouns only).
- **Noun compounding and external sandhi**: joining two lemmas (e.g. ആന + കുട്ടി →
  ആനക്കുട്ടി, with gemination) is a separate problem from single-lemma inflection.
