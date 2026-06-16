# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jayashankar R
"""Declarative, provenance-tagged noun-inflection rules, conditioned on stem ending.

A noun class is selected by the root's ending (anuswara `ം`, vowel signs `ി`/`ു`, the
`ട്` cluster, a chillu, or a bare consonant for -അ stems) plus an optional `pre`
constraint. Each class supplies an oblique-stem transform and a matra-initial suffix
per case; a case may override the stem (e.g. `ട്` geminates only for spatial cases).
Suffixes attach via ``nouns._attach``, which reverts a trailing chillu to its base
consonant before a vowel sign (so plural മരങ്ങൾ + `ുടെ` → മരങ്ങളുടെ).

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
    pre: str = ""               # "" | "consonant" | "vowel" (what precedes the ending)
    ends_consonant: bool = False  # match roots ending in a bare consonant (-അ stems)


_GEMINATE_T = StemTransform("ട്", "ട്ട")  # ട് -> ട്ട for the ṭ_geminate spatial cases


def _plural_cases(provenance: str, verified: bool) -> Dict[Case, CaseRule]:
    """Standard plural case markers, attached to a plural stem ending in the chillu ൾ
    (which reverts to ള before a vowel sign). Used by every class whose plural ends in ൾ."""
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
    # Consonant + anuswara (മരം); oblique augment -ത്ത-; vocative on a -മ- stem (മരമേ).
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
    # Vowel + anuswara (കലാം, ടീം); -മ- stem with -ഇന- linker; plural -ഉകൾ (കലാമുകൾ).
    "vowel_anuswara": NounClass(
        name="vowel_anuswara",
        description="Vowel + anuswara nouns (e.g. കലാം, ടീം); -മ- stem with -ഇന- linker.",
        endings=("ം",),
        pre="vowel",
        oblique=StemTransform("ം", "മ"),
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
        plural_marker=StemTransform("ം", "മുകൾ"),
        plural_cases=_plural_cases("native-2026", True),
    ),
    # Vowel-final -ി (കുട്ടി); glide -യ-, dative on root.
    "i_vowel": NounClass(
        name="i_vowel",
        description="Vowel-final nouns ending in -ി or -ീ (e.g. കുട്ടി, സ്ത്രീ); glide -യ-.",
        endings=("ി", "ീ"),
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
    # Vowel-final -ഉ/-ഊ (പശു); glide -വ-; plural -ക്കൾ (പശുക്കൾ), ratified.
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
        plural_marker=StemTransform("", "ക്കൾ"),
        plural_cases=_plural_cases("native-2026", True),
    ),
    # -ട് final (വീട്); geminate ട്->ട്ട for spatial cases, plain stem (-ഇന-) otherwise;
    # plural -ഉകൾ without gemination (വീടുകൾ).
    "ṭ_geminate": NounClass(
        name="ṭ_geminate",
        description="-ട് final nouns (e.g. വീട് 'house'); geminate ട്->ട്ട for spatial cases.",
        endings=("ട്",),
        oblique=StemTransform("്", ""),  # plain oblique: വീട്->വീട
        cases={
            Case.NOMINATIVE: CaseRule("", False, "native-2026", True),
            Case.ACCUSATIVE: CaseRule("ിനെ", True, "native-2026", True),
            Case.DATIVE: CaseRule("ിന്", True, "native-2026", True),
            Case.GENITIVE: CaseRule("ിന്റെ", True, "native-2026", True),
            Case.SOCIATIVE: CaseRule("ിനോട്", True, "native-2026", True),
            Case.INSTRUMENTAL: CaseRule("ിനാൽ", True, "native-2026", True),
            Case.VOCATIVE: CaseRule("േ", True, "native-2026", True),
            Case.LOCATIVE: CaseRule("ിൽ", True, "native-2026", True, oblique=_GEMINATE_T),
            Case.ALLATIVE: CaseRule("ിലേക്ക്", True, "native-2026", True, oblique=_GEMINATE_T),
            Case.ABLATIVE: CaseRule("ിൽനിന്ന്", True, "native-2026", True, oblique=_GEMINATE_T),
            Case.PERLATIVE: CaseRule("ിലൂടെ", True, "native-2026", True, oblique=_GEMINATE_T),
        },
        plural_marker=StemTransform("്", "ുകൾ"),  # വീട്->വീടുകൾ (no gemination)
        plural_cases=_plural_cases("native-2026", True),
    ),
    # -അ stems (അമ്മ, പുഴ); glide -യ-; vocative -ഏ on the root (അമ്മേ); dative -യ്ക്ക്.
    "a_stem": NounClass(
        name="a_stem",
        description="Bare-consonant (-അ) stems (e.g. അമ്മ 'mother'); glide -യ-.",
        endings=(),
        ends_consonant=True,
        oblique=StemTransform("", "യ"),
        cases={
            Case.NOMINATIVE: CaseRule("", False, "native-2026", True),
            Case.ACCUSATIVE: CaseRule("െ", True, "native-2026", True),       # അമ്മയെ
            Case.GENITIVE: CaseRule("ുടെ", True, "native-2026", True),        # അമ്മയുടെ
            Case.DATIVE: CaseRule("യ്ക്ക്", False, "native-2026", True),       # അമ്മയ്ക്ക് (on root)
            Case.VOCATIVE: CaseRule("േ", False, "native-2026", True),          # അമ്മേ (on root, not glide)
            Case.SOCIATIVE: CaseRule("ോട്", True, "native-2026", True),
            Case.LOCATIVE: CaseRule("ിൽ", True, "native-2026", True),
            Case.INSTRUMENTAL: CaseRule("ാൽ", True, "native-2026", True),
            Case.ABLATIVE: CaseRule("ിൽനിന്ന്", True, "native-2026", True),
            Case.ALLATIVE: CaseRule("ിലേക്ക്", True, "native-2026", True),
            Case.PERLATIVE: CaseRule("ിലൂടെ", True, "native-2026", True),
        },
        plural_marker=StemTransform("", ""),
        plural_cases={},
    ),
    # Chillu-final classes. The chillu reverts to its base consonant for vowel suffixes;
    # each chillu takes a different suffix set (native worksheet).
    # ൻ/ൾ take -ഓട് sociative and -ആൽ instrumental (on the reverted stem);
    # ർ/ൽ/ൺ take the -ഇന- linker (sociative -ഇനോട്, instrumental -ഇനാൽ). Plurals deferred.
    "chillu_n": NounClass(
        name="chillu_n",
        description="-ൻ final nouns (e.g. അവൻ, നടൻ).",
        endings=("ൻ",),
        oblique=StemTransform("ൻ", "ന"),
        cases={
            Case.NOMINATIVE: CaseRule("", False, "native-2026", True),
            Case.ACCUSATIVE: CaseRule("െ", True, "native-2026", True),    # അവനെ
            Case.DATIVE: CaseRule("്", True, "native-2026", True),         # അവന്
            Case.GENITIVE: CaseRule("്റെ", True, "native-2026", True),     # നടന്റെ
            Case.VOCATIVE: CaseRule("േ", True, "native-2026", True),       # മകനേ
            Case.SOCIATIVE: CaseRule("ോട്", True, "native-2026", True),    # അവനോട്
            Case.LOCATIVE: CaseRule("ിൽ", True, "native-2026", True),      # അവനിൽ
            Case.INSTRUMENTAL: CaseRule("ാൽ", True, "native-2026", True),  # അവനാൽ
            Case.ABLATIVE: CaseRule("ിൽനിന്ന്", True, "native-2026", True),
            Case.ALLATIVE: CaseRule("ിലേക്ക്", True, "native-2026", True),
            Case.PERLATIVE: CaseRule("ിലൂടെ", True, "native-2026", True),
        },
        plural_marker=StemTransform("", ""),
        plural_cases={},
    ),
    "chillu_ll": NounClass(
        name="chillu_ll",
        description="-ൾ final nouns (e.g. മകൾ).",
        endings=("ൾ",),
        oblique=StemTransform("ൾ", "ള"),
        cases={
            Case.NOMINATIVE: CaseRule("", False, "native-2026", True),
            Case.ACCUSATIVE: CaseRule("െ", True, "native-2026", True),    # മകളെ
            Case.DATIVE: CaseRule("ക്ക്", False, "native-2026", True),     # മകൾക്ക് (on root)
            Case.GENITIVE: CaseRule("ുടെ", True, "native-2026", True),     # മകളുടെ
            Case.VOCATIVE: CaseRule("േ", True, "native-2026", True),       # മകളേ
            Case.SOCIATIVE: CaseRule("ോട്", True, "native-2026", True),    # മകളോട്
            Case.LOCATIVE: CaseRule("ിൽ", True, "native-2026", True),      # മകളിൽ
            Case.INSTRUMENTAL: CaseRule("ാൽ", True, "native-2026", True),  # മകളാൽ
            Case.ABLATIVE: CaseRule("ിൽനിന്ന്", True, "native-2026", True),
            Case.ALLATIVE: CaseRule("ിലേക്ക്", True, "native-2026", True),
            Case.PERLATIVE: CaseRule("ിലൂടെ", True, "native-2026", True),
        },
        plural_marker=StemTransform("", ""),
        plural_cases={},
    ),
    "chillu_r": NounClass(
        name="chillu_r",
        description="-ർ final nouns (e.g. കാർ).",
        endings=("ർ",),
        oblique=StemTransform("ർ", "റ"),
        cases={
            Case.NOMINATIVE: CaseRule("", False, "native-2026", True),
            Case.ACCUSATIVE: CaseRule("ിനെ", True, "native-2026", True),   # ഡോക്ടറിനെ
            Case.DATIVE: CaseRule("ിന്", True, "native-2026", True),       # കാറിന്
            Case.GENITIVE: CaseRule("ിന്റെ", True, "native-2026", True),   # കാറിന്റെ
            Case.VOCATIVE: CaseRule("േ", True, "native-2026", True),       # കാറേ
            Case.SOCIATIVE: CaseRule("ിനോട്", True, "native-2026", True),  # കാറിനോട്
            Case.LOCATIVE: CaseRule("ിൽ", True, "native-2026", True),      # കാറിൽ
            Case.INSTRUMENTAL: CaseRule("ിനാൽ", True, "native-2026", True),
            Case.ABLATIVE: CaseRule("ിൽനിന്ന്", True, "native-2026", True),
            Case.ALLATIVE: CaseRule("ിലേക്ക്", True, "native-2026", True),
            Case.PERLATIVE: CaseRule("ിലൂടെ", True, "native-2026", True),
        },
        plural_marker=StemTransform("", ""),
        plural_cases={},
    ),
    "chillu_l": NounClass(
        name="chillu_l",
        description="-ൽ final nouns (e.g. കാൽ).",
        endings=("ൽ",),
        oblique=StemTransform("ൽ", "ല"),
        cases={
            Case.NOMINATIVE: CaseRule("", False, "native-2026", True),
            Case.ACCUSATIVE: CaseRule("ിനെ", True, "native-2026", True),   # കാലിനെ
            Case.DATIVE: CaseRule("ിന്", True, "native-2026", True),        # കാലിന്
            Case.GENITIVE: CaseRule("ിന്റെ", True, "native-2026", True),    # കാലിന്റെ
            Case.VOCATIVE: CaseRule("േ", True, "native-2026", True),        # കാലേ
            Case.SOCIATIVE: CaseRule("ിനോട്", True, "native-2026", True),  # കാലിനോട്
            Case.LOCATIVE: CaseRule("ിൽ", True, "native-2026", True),      # കാലിൽ
            Case.INSTRUMENTAL: CaseRule("ിനാൽ", True, "native-2026", True),
            Case.ABLATIVE: CaseRule("ിൽനിന്ന്", True, "native-2026", True),
            Case.ALLATIVE: CaseRule("ിലേക്ക്", True, "native-2026", True),
            Case.PERLATIVE: CaseRule("ിലൂടെ", True, "native-2026", True),
        },
        plural_marker=StemTransform("", ""),
        plural_cases={},
    ),
    "chillu_nn": NounClass(
        name="chillu_nn",
        description="-ൺ final nouns (e.g. തൂൺ).",
        endings=("ൺ",),
        oblique=StemTransform("ൺ", "ണ"),
        cases={
            Case.NOMINATIVE: CaseRule("", False, "native-2026", True),
            Case.ACCUSATIVE: CaseRule("ിനെ", True, "native-2026", True),   # തൂണിനെ
            Case.DATIVE: CaseRule("ിന്", True, "native-2026", True),        # തൂണിന്
            Case.GENITIVE: CaseRule("ിന്റെ", True, "native-2026", True),    # തൂണിന്റെ
            Case.VOCATIVE: CaseRule("േ", True, "native-2026", True),        # തൂണേ
            Case.SOCIATIVE: CaseRule("ിനോട്", True, "native-2026", True),  # തൂണിനോട്
            Case.LOCATIVE: CaseRule("ിൽ", True, "native-2026", True),      # തൂണിൽ
            Case.INSTRUMENTAL: CaseRule("ിനാൽ", True, "native-2026", True),
            Case.ABLATIVE: CaseRule("ിൽനിന്ന്", True, "native-2026", True),
            Case.ALLATIVE: CaseRule("ിലേക്ക്", True, "native-2026", True),
            Case.PERLATIVE: CaseRule("ിലൂടെ", True, "native-2026", True),
        },
        plural_marker=StemTransform("", ""),
        plural_cases={},
    ),
}
