# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jayashankar R
"""Clitic attachment (the post-case agglutination layer), native-ratified.

The additive -ഉം and interrogative -ഓ take an Agama glide / chillu reversion / virama drop;
anuswara and the emphatic -തന്നെ have their own ratified sandhi. Forms are verified=True.
"""
import pytest

from mlsynth import (
    Case,
    Clitic,
    Number,
    Register,
    Animacy,
    UnsupportedClitic,
    synthesize_noun,
    with_clitic,
)


def _w(root, case, clitic, **kw):
    return with_clitic(synthesize_noun(root, case, **kw), clitic)


# (root, case, clitic, expected surface) for the vowel-initial clitics.
FORMS = [
    # vowel-final + Agama glide
    ("കുട്ടി", Case.ACCUSATIVE, Clitic.UM, "കുട്ടിയെയും"),
    ("കുട്ടി", Case.ACCUSATIVE, Clitic.O, "കുട്ടിയെയോ"),
    ("കുട്ടി", Case.NOMINATIVE, Clitic.UM, "കുട്ടിയും"),     # -ഇ -> യ
    ("പശു", Case.NOMINATIVE, Clitic.UM, "പശുവും"),          # -ഉ -> വ
    ("അമ്മ", Case.GENITIVE, Clitic.UM, "അമ്മയുടെയും"),      # -െ -> യ
    # chillu-final reversion
    ("മരം", Case.LOCATIVE, Clitic.UM, "മരത്തിലും"),
    ("മരം", Case.INSTRUMENTAL, Clitic.UM, "മരത്താലും"),
    # virama-final: drop the virama
    ("മരം", Case.DATIVE, Clitic.UM, "മരത്തിനും"),
    ("മരം", Case.SOCIATIVE, Clitic.UM, "മരത്തോടും"),
    ("വീട്", Case.NOMINATIVE, Clitic.UM, "വീടും"),
    # anuswara: -ഉം drops ം + വ glide; -ഓ keeps ം as consonant മ
    ("മരം", Case.NOMINATIVE, Clitic.UM, "മരവും"),
    ("മരം", Case.NOMINATIVE, Clitic.O, "മരമോ"),
]


@pytest.mark.parametrize("root, case, clitic, expected", FORMS)
def test_clitic_surface(root, case, clitic, expected):
    r = _w(root, case, clitic)
    assert r.surface == expected
    assert r.features.clitic is clitic
    assert r.verified is True


def test_clitic_morphemes_record_citation_form():
    assert _w("കുട്ടി", Case.ACCUSATIVE, Clitic.UM).morphemes[-1] == "ഉം"


# The chillu ർ: lexical noun reverts to retroflex റ, plural/pronoun to dental ര.
def test_lexical_r_reverts_retroflex():
    assert _w("കാർ", Case.NOMINATIVE, Clitic.UM).surface == "കാറും"


def test_plural_r_reverts_dental():
    r = with_clitic(
        synthesize_noun("അമ്മ", Case.NOMINATIVE, number=Number.PLURAL, animacy=Animacy.HUMAN),
        Clitic.UM,
    )
    assert r.surface == "അമ്മമാരും"


def test_pronoun_r_reverts_dental():
    assert _w("അവർ", Case.NOMINATIVE, Clitic.UM).surface == "അവരും"


# Emphatic -തന്നെ: geminates ത -> ത്ത after a vowel or chillu ending.
@pytest.mark.parametrize("root, case, expected", [
    ("കുട്ടി", Case.ACCUSATIVE, "കുട്ടിയെത്തന്നെ"),
    ("വീട്", Case.LOCATIVE, "വീട്ടിൽത്തന്നെ"),
])
def test_emphatic(root, case, expected):
    r = _w(root, case, Clitic.EMPHATIC)
    assert r.surface == expected
    assert r.verified is True


def test_clitic_stacking_emphatic_then_interrogative():
    # Order: ... + emphatic + interrogative; the inner boundary takes the Agama glide.
    r = with_clitic(with_clitic(synthesize_noun("കുട്ടി", Case.ACCUSATIVE), Clitic.EMPHATIC), Clitic.O)
    assert r.surface == "കുട്ടിയെത്തന്നെയോ"


def test_clitic_on_analytic_form_attaches_to_last_token():
    analytic = synthesize_noun("മരം", Case.INSTRUMENTAL, register=Register.COLLOQUIAL)
    assert analytic.analytic is True  # മരം കൊണ്ട്
    assert with_clitic(analytic, Clitic.UM).surface == "മരം കൊണ്ടും"


# Emphatic -തന്നെ after a virama, anuswara, or a bare-consonant (inherent -അ) ending is not
# ratified yet (gemination after a bare stem is unconfirmed), so it must raise.
@pytest.mark.parametrize("root, case", [
    ("മരം", Case.DATIVE),       # virama
    ("മരം", Case.NOMINATIVE),   # anuswara
    ("അമ്മ", Case.NOMINATIVE),  # bare consonant (inherent -അ)
])
def test_emphatic_unratified_boundary_raises(root, case):
    with pytest.raises(UnsupportedClitic):
        _w(root, case, Clitic.EMPHATIC)
