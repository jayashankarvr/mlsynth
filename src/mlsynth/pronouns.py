# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jayashankar R
"""Suppletive personal-pronoun paradigms.

Pronouns bypass the rule engine: their oblique stems are suppletive (ഞാൻ 'I' →
എന്നെ / എനിക്ക് / എന്റെ), so standard agglutination would emit a wrong form (the
class engine would treat ഞാൻ as a -ൻ chillu and produce *ഞാനെ). The forms below are
the canonical (first-listed) variant per case; ratified spoken/written alternates are
noted alongside each entry but not generated. A case absent from a pronoun's map is
not encoded: the caller gets ``NotImplementedError``, never a guessed form.
"""
from __future__ import annotations

from typing import Dict, List

from .types import Case

# root -> {case: canonical surface}. Forms are native-ratified facts (verified=True).
PRONOUN_FORMS: Dict[str, Dict[Case, str]] = {
    # ഞാൻ 'I'. alt: dative എനിയ്ക്ക് / എനിക്കു; genitive എന്നുടെ
    "ഞാൻ": {
        Case.NOMINATIVE: "ഞാൻ",
        Case.ACCUSATIVE: "എന്നെ",
        Case.DATIVE: "എനിക്ക്",
        Case.GENITIVE: "എന്റെ",
    },
    # നീ 'you' (sg). alt: dative നിനക്കു; genitive നിന്നുടെ
    "നീ": {
        Case.NOMINATIVE: "നീ",
        Case.ACCUSATIVE: "നിന്നെ",
        Case.DATIVE: "നിനക്ക്",
        Case.GENITIVE: "നിന്റെ",
    },
    # അവർ 'they'. alt: dative അവർക്കു; genitive അവർതൻ (poetic)
    "അവർ": {
        Case.NOMINATIVE: "അവർ",
        Case.ACCUSATIVE: "അവരെ",
        Case.DATIVE: "അവർക്ക്",
        Case.GENITIVE: "അവരുടെ",
    },
    # നാം 'we' (inclusive). alt: dative നമുക്കു; genitive നമ്മളുടെ
    "നാം": {
        Case.NOMINATIVE: "നാം",
        Case.ACCUSATIVE: "നമ്മെ",
        Case.DATIVE: "നമുക്ക്",
        Case.GENITIVE: "നമ്മുടെ",
    },
    # താൻ 'oneself' (reflexive). alt: dative തനിയ്ക്ക്
    "താൻ": {
        Case.NOMINATIVE: "താൻ",
        Case.ACCUSATIVE: "തന്നെ",
        Case.DATIVE: "തനിക്ക്",
        Case.GENITIVE: "തന്റെ",
    },
    # ഇവൻ 'he / this one'. Only the accusative is ratified so far.
    "ഇവൻ": {
        Case.NOMINATIVE: "ഇവൻ",
        Case.ACCUSATIVE: "ഇവനെ",
    },
}


def is_pronoun(root: str) -> bool:
    return root in PRONOUN_FORMS


def list_pronouns() -> List[str]:
    return sorted(PRONOUN_FORMS)
