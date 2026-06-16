# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jayashankar R
"""Suppletive pronoun paradigms and the soundness guarantees around them."""
import pytest

from mlsynth import Case, is_pronoun, list_pronouns, synthesize_noun

# (root, case, expected surface): native-ratified suppletive forms.
PRONOUN_FORMS = [
    ("ഞാൻ", Case.NOMINATIVE, "ഞാൻ"),
    ("ഞാൻ", Case.ACCUSATIVE, "എന്നെ"),
    ("ഞാൻ", Case.DATIVE, "എനിക്ക്"),
    ("ഞാൻ", Case.GENITIVE, "എന്റെ"),
    ("നീ", Case.ACCUSATIVE, "നിന്നെ"),
    ("നീ", Case.DATIVE, "നിനക്ക്"),
    ("നീ", Case.GENITIVE, "നിന്റെ"),
    ("അവർ", Case.ACCUSATIVE, "അവരെ"),
    ("അവർ", Case.DATIVE, "അവർക്ക്"),
    ("അവർ", Case.GENITIVE, "അവരുടെ"),
    ("നാം", Case.ACCUSATIVE, "നമ്മെ"),
    ("നാം", Case.DATIVE, "നമുക്ക്"),
    ("നാം", Case.GENITIVE, "നമ്മുടെ"),
    ("താൻ", Case.ACCUSATIVE, "തന്നെ"),
    ("താൻ", Case.DATIVE, "തനിക്ക്"),
    ("താൻ", Case.GENITIVE, "തന്റെ"),
    ("ഇവൻ", Case.ACCUSATIVE, "ഇവനെ"),
]


@pytest.mark.parametrize("root, case, expected", PRONOUN_FORMS)
def test_pronoun_surface(root, case, expected):
    result = synthesize_noun(root, case)
    assert result.surface == expected
    assert result.stem_class == "pronoun"
    assert result.verified is True
    assert result.provenance == "native-2026"


def test_pronoun_bypasses_chillu_rule():
    # Regression: ഞാൻ ends in the chillu ൻ, so the rule engine would otherwise
    # produce *ഞാനെ / *ഞാന്റെ. The suppletive table must win.
    assert synthesize_noun("ഞാൻ", Case.ACCUSATIVE).surface == "എന്നെ"
    assert synthesize_noun("ഞാൻ", Case.GENITIVE).surface == "എന്റെ"


def test_unencoded_pronoun_case_raises():
    # ഇവൻ has only nominative + accusative ratified; anything else must raise,
    # never fall through to the (wrong) chillu rule.
    with pytest.raises(NotImplementedError):
        synthesize_noun("ഇവൻ", Case.LOCATIVE)


def test_pronoun_plural_raises():
    # The pronoun table is singular-only; pronoun plurals are suppletive. A plural
    # request must raise, never return the singular form.
    from mlsynth import Number

    with pytest.raises(NotImplementedError):
        synthesize_noun("ഞാൻ", Case.ACCUSATIVE, number=Number.PLURAL)


def test_pronoun_helpers():
    assert is_pronoun("ഞാൻ") is True
    assert is_pronoun("മരം") is False
    assert "ഞാൻ" in list_pronouns()


def test_explicit_stem_class_overrides_pronoun_table():
    # An explicit stem_class is an escape hatch: the caller asked for rule-engine
    # behaviour, so the pronoun table is bypassed (no silent suppletion).
    result = synthesize_noun("ഞാൻ", Case.ACCUSATIVE, stem_class="chillu_n")
    assert result.stem_class == "chillu_n"
    assert result.surface != "എന്നെ"
