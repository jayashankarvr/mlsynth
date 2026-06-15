# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jayashankar R
"""Declarative, provenance-tagged noun-inflection rules, conditioned on stem ending.

A noun class is selected by the root's ending (anuswara `ം`, vowel sign `ി`/`ു`, the
`ട്` cluster, ...) plus an optional `pre` constraint (whether a consonant or a vowel
precedes the ending). Each class supplies an oblique-stem transform and a matra-initial
suffix per case; a case may override the stem (e.g. `ട്` geminates only for the spatial
cases). Suffixes attach via ``nouns._attach``, which reverts a trailing chillu to its
base consonant before a vowel sign (so plural മരങ്ങൾ + `ുടെ` → മരങ്ങളുടെ).

Provenance keys (see REFERENCES.md): ``native-2026`` (native-ratified), ``smc-morph``
(SMC docs, pending native sign-off), ``native-14`` (genitive #14). Editing a paradigm
is a data edit here; flip ``verified`` after native sign-off.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from .types import Case


@dataclass(frozen=True)
class StemTransform:
    strip: str
    append: str

    def apply(self, root: str) -> str:
        if self.strip and root.endswith(self.strip):
            root = root[: -len(self.strip)]
        return root + self.append


@dataclass(frozen=True)
class CaseRule:
    suffix: str        # matra-initial; "" for the bare nominative
    use_oblique: bool  # attach to the class oblique stem (True) or the bare root (False)
    provenance: str
    verified: bool = False
    oblique: Optional[StemTransform] = None  # per-case stem override (e.g. ട് gemination)


@dataclass(frozen=True)
class NounClass:
    name: str
    description: str
    endings: Tuple[str, ...]
    oblique: StemTransform
    cases: Dict[Case, CaseRule]
    plural_marker: StemTransform
    plural_cases: Dict[Case, CaseRule]
    # "" = match on ending alone; "consonant"/"vowel" = also require that kind of
    # character before the ending (disambiguates മരം consonant+anuswara from കലാം
    # vowel+anuswara, both ending in ം).
    pre: str = ""


# ട് gemination, shared by the spatial cases of the ṭ_geminate class.
_GEMINATE_T = StemTransform("ട്", "ട്ട")


# Plural case markers attach to the plural stem (its trailing chillu ൾ reverts to ള
# before a vowel sign). Includes vocative -ഏ (worksheet Part B). Provenance/verified
# are per-class.
def _plural_cases(provenance: str, verified: bool) -> Dict[Case, CaseRule]:
    v = verified
    return {
        Case.NOMINATIVE: CaseRule("", False, provenance, v),
        Case.ACCUSATIVE: CaseRule("െ", True, provenance, v),
        Case.DATIVE: CaseRule("ക്ക്", True, provenance, v),
        Case.GENITIVE: CaseRule("ുടെ", True, provenance, v),
        Case.SOCIATIVE: CaseRule("ോട്", True, provenance, v),
        Case.LOCATIVE: CaseRule("ിൽ", True, provenance, v),
        Case.INSTRUMENTAL: CaseRule("ാൽ", True, provenance, v),
        Case.VOCATIVE: CaseRule("േ", True, provenance, v),
        Case.ABLATIVE: CaseRule("ിൽനിന്ന്", True, provenance, v),
        Case.ALLATIVE: CaseRule("ിലേക്ക്", True, provenance, v),
        Case.PERLATIVE: CaseRule("ിലൂടെ", True, provenance, v),
    }


CLASSES: Dict[str, NounClass] = {
    # Consonant + anuswara (e.g. മരം); oblique augment -ത്ത-. Vocative uses a -മ- stem
    # (മരം -> മരമേ). Core cases native-ratified; abl/all/perl ratified in worksheet C.
    "am_neuter": NounClass(
        name="am_neuter",
        description="Consonant + anuswara nouns (e.g. മരം 'tree'); oblique augment -ത്ത-.",
        endings=("ം",),
        pre="consonant",
        oblique=StemTransform("ം", "ത്ത"),
        cases={
            Case.NOMINATIVE: CaseRule("", False, "native-2026", True),
            Case.ACCUSATIVE: CaseRule("െ", True, "native-2026", True),
            Case.DATIVE: CaseRule("ിന്", True, "native-2026", True),
            Case.GENITIVE: CaseRule("ിന്റെ", True, "native-2026", True),
            Case.SOCIATIVE: CaseRule("ോട്", True, "native-2026", True),
            Case.LOCATIVE: CaseRule("ിൽ", True, "native-2026", True),
            Case.INSTRUMENTAL: CaseRule("ാൽ", True, "native-2026", True),
            Case.VOCATIVE: CaseRule("േ", False, "native-2026", True, oblique=StemTransform("ം", "മ")),
            Case.ABLATIVE: CaseRule("ിൽനിന്ന്", True, "native-2026", True),
            Case.ALLATIVE: CaseRule("ിലേക്ക്", True, "native-2026", True),
            Case.PERLATIVE: CaseRule("ിലൂടെ", True, "native-2026", True),
        },
        plural_marker=StemTransform("ം", "ങ്ങൾ"),
        plural_cases=_plural_cases("native-2026", True),
    ),
    # Vowel + anuswara (e.g. കലാം, ടീം); anuswara behaves as -മ- and suffixes take the
    # -ഇന- linker. acc/gen native-ratified (worksheet A); dative extrapolated.
    "vowel_anuswara": NounClass(
        name="vowel_anuswara",
        description="Vowel + anuswara nouns (e.g. കലാം, ടീം); -മ- stem with -ഇന- linker.",
        endings=("ം",),
        pre="vowel",
        oblique=StemTransform("ം", "മ"),
        cases={
            Case.NOMINATIVE: CaseRule("", False, "native-2026", True),
            Case.ACCUSATIVE: CaseRule("ിനെ", True, "native-2026", True),
            Case.GENITIVE: CaseRule("ിന്റെ", True, "native-2026", True),
            Case.DATIVE: CaseRule("ിന്", True, "native-2026", True),
            Case.SOCIATIVE: CaseRule("ിനോട്", True, "native-2026", True),
            Case.LOCATIVE: CaseRule("ിൽ", True, "native-2026", True),
            Case.VOCATIVE: CaseRule("േ", True, "native-2026", True),
            Case.ABLATIVE: CaseRule("ിൽനിന്ന്", True, "native-2026", True),
            Case.ALLATIVE: CaseRule("ിലേക്ക്", True, "native-2026", True),
            Case.PERLATIVE: CaseRule("ിലൂടെ", True, "native-2026", True),
        },
        plural_marker=StemTransform("", ""),
        plural_cases={},
    ),
    # Vowel-final -ി nouns (e.g. കുട്ടി); glide -യ-, dative on root. Singular core +
    # abl/all/perl native-ratified (worksheet); genitive #14.
    "i_vowel": NounClass(
        name="i_vowel",
        description="Vowel-final nouns ending in -ി (e.g. കുട്ടി 'child'); glide -യ-.",
        endings=("ി",),
        oblique=StemTransform("", "യ"),
        cases={
            Case.NOMINATIVE: CaseRule("", False, "native-2026", True),
            Case.ACCUSATIVE: CaseRule("െ", True, "native-2026", True),
            Case.DATIVE: CaseRule("ക്ക്", False, "native-2026", True),
            Case.GENITIVE: CaseRule("ുടെ", True, "native-14", True),
            Case.SOCIATIVE: CaseRule("ോട്", True, "native-2026", True),
            Case.LOCATIVE: CaseRule("ിൽ", True, "native-2026", True),
            Case.INSTRUMENTAL: CaseRule("ാൽ", True, "native-2026", True),
            Case.VOCATIVE: CaseRule("േ", True, "native-2026", True),
            Case.ABLATIVE: CaseRule("ിൽനിന്ന്", True, "native-2026", True),
            Case.ALLATIVE: CaseRule("ിലേക്ക്", True, "native-2026", True),
            Case.PERLATIVE: CaseRule("ിലൂടെ", True, "native-2026", True),
        },
        plural_marker=StemTransform("", "കൾ"),
        plural_cases=_plural_cases("native-2026", True),
    ),
    # Vowel-final -ഉ/-ഊ nouns (e.g. പശു, മുത്തു); glide -വ-. gen/vocative native-
    # ratified (worksheet A); acc/dat/loc extrapolated from the -ഇന- linker pattern.
    "u_vowel": NounClass(
        name="u_vowel",
        description="Vowel-final nouns ending in -ഉ/-ഊ (e.g. പശു 'cow'); glide -വ-.",
        endings=("ു", "ൂ"),
        oblique=StemTransform("", "വ"),
        cases={
            Case.NOMINATIVE: CaseRule("", False, "native-2026", True),
            Case.ACCUSATIVE: CaseRule("ിനെ", True, "native-2026", True),
            Case.DATIVE: CaseRule("ിന്", True, "native-2026", True),
            Case.GENITIVE: CaseRule("ിന്റെ", True, "native-2026", True),
            Case.SOCIATIVE: CaseRule("ിനോട്", True, "native-2026", True),
            Case.LOCATIVE: CaseRule("ിൽ", True, "native-2026", True),
            Case.INSTRUMENTAL: CaseRule("ിനാൽ", True, "native-2026", True),
            Case.VOCATIVE: CaseRule("േ", True, "native-2026", True),
            Case.ABLATIVE: CaseRule("ിൽനിന്ന്", True, "native-2026", True),
            Case.ALLATIVE: CaseRule("ിലേക്ക്", True, "native-2026", True),
            Case.PERLATIVE: CaseRule("ിലൂടെ", True, "native-2026", True),
        },
        plural_marker=StemTransform("", "ക്കൾ"),  # പശു -> പശുക്കൾ (marker native-given)
        plural_cases=_plural_cases("smc-morph", False),
    ),
    # -ട് final nouns (e.g. വീട്, കാട്); geminate ട്->ട്ട for the spatial cases, plain
    # stem (-ഇന- linker) for gen/dat. Worksheet A native-ratified; perlative extrapolated.
    "ṭ_geminate": NounClass(
        name="ṭ_geminate",
        description="-ട് final nouns (e.g. വീട് 'house'); geminate ട്->ട്ട for spatial cases.",
        endings=("ട്",),
        oblique=StemTransform("്", ""),  # plain oblique for gen/dat/acc/soc/voc: വീട്->വീട
        cases={
            Case.NOMINATIVE: CaseRule("", False, "native-2026", True),
            Case.ACCUSATIVE: CaseRule("ിനെ", True, "native-2026", True),
            Case.DATIVE: CaseRule("ിന്", True, "native-2026", True),
            Case.GENITIVE: CaseRule("ിന്റെ", True, "native-2026", True),
            Case.SOCIATIVE: CaseRule("ിനോട്", True, "native-2026", True),
            Case.VOCATIVE: CaseRule("േ", True, "native-2026", True),
            Case.LOCATIVE: CaseRule("ിൽ", True, "native-2026", True, oblique=_GEMINATE_T),
            Case.ALLATIVE: CaseRule("ിലേക്ക്", True, "native-2026", True, oblique=_GEMINATE_T),
            Case.ABLATIVE: CaseRule("ിൽനിന്ന്", True, "native-2026", True, oblique=_GEMINATE_T),
            Case.PERLATIVE: CaseRule("ിലൂടെ", True, "native-2026", True, oblique=_GEMINATE_T),
        },
        plural_marker=StemTransform("", ""),
        plural_cases={},
    ),
}
