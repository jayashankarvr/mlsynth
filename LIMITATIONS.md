# Limitations

mlsynth never emits a wrong form. When it cannot produce a form it has not verified,
it raises instead. Two exception types:

- **`UnsupportedRoot`**: the root's shape is not in a supported noun class.
- **`NotImplementedError`**: a supported class, but that case/number is not encoded.

This document is generated from the current rules.

## Supported noun classes

| Class | Shape | Example | Coverage |
|-------|-------|---------|----------|
| `am_neuter` | consonant + anuswara | `മരം` | complete (11 cases, sg + pl) |
| `i_vowel` | `-ി` vowel-final | `കുട്ടി` | complete (11 cases, sg + pl) |
| `u_vowel` | `-ഉ` / `-ഊ` vowel-final | `പശു` | complete singular; plural extrapolated |
| `vowel_anuswara` | vowel + anuswara | `കലാം`, `ടീം` | singular minus instrumental; no plural |
| `ṭ_geminate` | `-ട്` final (geminating) | `വീട്` | singular minus instrumental; no plural |

## A. Root shapes that raise `UnsupportedRoot`

These classes are not encoded yet:

| Root shape | Examples | Planned class |
|------------|----------|---------------|
| `-അ` / `-എ` vowel stems | `അമ്മ`, `പുഴ` | a/e-stem (`യ` glide) |
| chillu final | `അവൻ`, `നായർ`, `പാൽ`, `മകൾ` | chillu classes (per-chillu) |
| long `-ീ` vowel stems | `സ്ത്രീ` | a/e/ī-stem (`യ` glide) |
| no Malayalam base letter, or empty | `ABC`, `123`, bare signs, `""` | rejected by design |

The a/e-stem class needs predicate-based matching (those roots end in a bare consonant,
not a fixed suffix); the chillu classes need per-chillu handling. Both are specced and
deferred to the next release.

## B. Case/number combinations that raise `NotImplementedError`

- **`vowel_anuswara`** (`കലാം`): instrumental and the whole plural are not encoded.
- **`ṭ_geminate`** (`വീട്`): instrumental and the whole plural are not encoded.

`am_neuter`, `i_vowel`, and `u_vowel` (singular) have no such gaps.

## C. Produced but not native-ratified (`verified=False`)

- **`u_vowel` plural**: the `-ക്കൾ` marker is native-given (`പശുക്കൾ`), but the plural
  oblique paradigm (`പശുക്കളുടെ`, ...) is extrapolated. Gate on `result.verified` for
  ratified output only.

## D. Known matching caveat

`u_vowel` matches any root ending in `-ു` / `-ൂ`. A non-standard input that writes a
final samvruthokaram (half-u) as a bare `-ു` instead of `-്` could be mis-routed here.
Standard orthography writes samvruthokaram with the virama, so genuine `-ഉ`-final nouns
(`പശു`, `ഗുരു`) inflect correctly; the risk is limited to non-standard/transliterated input.

## E. Out of scope in this release

- **Verbs**: noun synthesis only; verb synthesis is the next major addition.
- **Pronouns**: irregular; deferred.
- **Derivation, compounding, and external sandhi** (word + word) are out of scope.

## Roadmap

Next: the a/e-stem and chillu classes (section A), the instrumental + plural of the
two partial classes (section B), and native ratification of the `u_vowel` plural.
Verbs follow as 0.1.0.
