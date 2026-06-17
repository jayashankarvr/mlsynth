# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jayashankar R
"""Feminine derivation (pre-inflection) and its composition with case inflection."""
import pytest

from mlinflect import (
    Case,
    UnsupportedDerivation,
    derive_feminine,
    synthesize_noun,
)

# (masculine base, feminine derivation)
PAIRS = [
    ("എഴുത്തുകാരൻ", "എഴുത്തുകാരി"),   # -ൻ -> -ഇ (agentive writer)
    ("വിദ്യാർത്ഥി", "വിദ്യാർത്ഥിനി"),  # -ഇ -> -ഇനി (student)
]


@pytest.mark.parametrize("masc, fem", PAIRS)
def test_derive_feminine(masc, fem):
    assert derive_feminine(masc) == fem


def test_derive_then_inflect():
    # Derivation is pre-inflection: the feminine lemma feeds straight back in and
    # inflects as an ordinary -ഇ (i_vowel) stem.
    fem = derive_feminine("എഴുത്തുകാരൻ")          # എഴുത്തുകാരി
    assert synthesize_noun(fem, Case.GENITIVE).surface == "എഴുത്തുകാരിയുടെ"


@pytest.mark.parametrize("bad", ["മരം", "പശു", "വീട്", "അമ്മ", "ൻ", "ി"])
def test_underivable_base_raises(bad):
    # A bare chillu ("ൻ") or a bare matra ("ി") must raise, not emit a lone-matra non-word.
    with pytest.raises(UnsupportedDerivation):
        derive_feminine(bad)
