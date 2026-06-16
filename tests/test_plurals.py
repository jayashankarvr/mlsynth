# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jayashankar R
"""Animacy-conditioned plurals for a_stem + chillu classes (0.0.3).

Inanimate plurals (-കൾ / -ഉകൾ) have the full case paradigm; human plurals
(-മാർ / -ന്മാർ / -കാർ) and irregulars expose only the nominative; an unknown animacy
raises rather than guess -മാർ vs -കൾ.
"""
import pytest

from mlsynth import Animacy, Case, Number, synthesize_noun

PL = Number.PLURAL


def _pl(root, case, **kw):
    return synthesize_noun(root, case, number=PL, **kw)


# --- Inanimate plurals: full paradigm ---------------------------------------

# (root, case, expected) for the inanimate full paradigm.
INANIMATE_FORMS = [
    ("പുഴ", Case.NOMINATIVE, "പുഴകൾ"),
    ("പുഴ", Case.GENITIVE, "പുഴകളുടെ"),
    ("പുഴ", Case.DATIVE, "പുഴകൾക്ക്"),
    ("പുഴ", Case.LOCATIVE, "പുഴകളിൽ"),
    ("പുഴ", Case.SOCIATIVE, "പുഴകളോട്"),
    # chillu: the lexical base is restored (retroflex റ, not the dental ര of -മാർ).
    ("കാർ", Case.NOMINATIVE, "കാറുകൾ"),
    ("കാർ", Case.GENITIVE, "കാറുകളുടെ"),
    ("കാൽ", Case.NOMINATIVE, "കാലുകൾ"),
    ("കാൽ", Case.GENITIVE, "കാലുകളുടെ"),
    ("തൂൺ", Case.NOMINATIVE, "തൂണുകൾ"),
    ("തൂൺ", Case.GENITIVE, "തൂണുകളുടെ"),
]


@pytest.mark.parametrize("root, case, expected", INANIMATE_FORMS)
def test_inanimate_plural_paradigm(root, case, expected):
    r = _pl(root, case, animacy=Animacy.INANIMATE)
    assert r.surface == expected
    assert r.verified is True
    assert r.provenance == "native-2026"


def test_inanimate_plural_accusative_is_dom_bare():
    # DOM: the inanimate accusative defaults to the bare plural nominative.
    assert _pl("പുഴ", Case.ACCUSATIVE, animacy=Animacy.INANIMATE).surface == "പുഴകൾ"
    assert _pl("കാർ", Case.ACCUSATIVE, animacy=Animacy.INANIMATE).surface == "കാറുകൾ"


def test_inanimate_plural_accusative_marked_is_overt():
    assert _pl(
        "പുഴ", Case.ACCUSATIVE, animacy=Animacy.INANIMATE, marked=True
    ).surface == "പുഴകളെ"


# --- Human plurals: nominative only -----------------------------------------

# (root, expected nominative plural) per the agentive-aware rule.
HUMAN_NOMINATIVES = [
    ("അമ്മ", "അമ്മമാർ"),            # -അ stem -> -മാർ
    ("അധ്യാപകൻ", "അധ്യാപകന്മാർ"),  # -ൻ -> -ന്മാർ
    ("എഴുത്തുകാരൻ", "എഴുത്തുകാർ"),  # agentive -കാരൻ -> -കാർ
    ("ഡോക്ടർ", "ഡോക്ടർമാർ"),        # -ർ human -> -മാർ
]


@pytest.mark.parametrize("root, expected", HUMAN_NOMINATIVES)
def test_human_plural_nominative(root, expected):
    r = _pl(root, Case.NOMINATIVE, animacy=Animacy.HUMAN)
    assert r.surface == expected
    assert r.verified is True


# The full human-plural oblique paradigm (ർ -> ര before a vowel suffix), native-ratified.
HUMAN_OBLIQUE = [
    (Case.ACCUSATIVE, "അമ്മമാരെ"),
    (Case.GENITIVE, "അമ്മമാരുടെ"),
    (Case.DATIVE, "അമ്മമാർക്ക്"),     # consonant suffix: chillu stays intact
    (Case.LOCATIVE, "അമ്മമാരിൽ"),
    (Case.SOCIATIVE, "അമ്മമാരോട്"),
    (Case.INSTRUMENTAL, "അമ്മമാരാൽ"),
    (Case.VOCATIVE, "അമ്മമാരേ"),
]


@pytest.mark.parametrize("case, expected", HUMAN_OBLIQUE)
def test_human_plural_oblique(case, expected):
    r = _pl("അമ്മ", case, animacy=Animacy.HUMAN)
    assert r.surface == expected
    assert r.verified is True


def test_human_plural_accusative_is_overt():
    # Humans take the overt accusative (DOM zero-marks inanimates only).
    assert _pl("അമ്മ", Case.ACCUSATIVE, animacy=Animacy.HUMAN).surface == "അമ്മമാരെ"


# --- Irregular / suppletive plurals (no animacy needed) ----------------------

IRREGULARS = [
    ("മകൾ", "മക്കൾ"),
    ("മകൻ", "മക്കൾ"),
    ("അവൻ", "അവർ"),
    ("മനുഷ്യൻ", "മനുഷ്യർ"),  # -അൻ -> -അർ lexical; not the *മനുഷ്യന്മാർ default
]


@pytest.mark.parametrize("root, expected", IRREGULARS)
def test_irregular_plural(root, expected):
    r = _pl(root, Case.NOMINATIVE)  # irregulars are unambiguous; no animacy required
    assert r.surface == expected
    assert r.verified is True


# Irregular oblique cases: ർ-final reverts to ര (അവർ), ൾ-final to ള (മക്കൾ).
IRREGULAR_OBLIQUE = [
    ("അവൻ", Case.ACCUSATIVE, "അവരെ"),
    ("അവൻ", Case.GENITIVE, "അവരുടെ"),
    ("അവൻ", Case.DATIVE, "അവർക്ക്"),
    ("മനുഷ്യൻ", Case.ACCUSATIVE, "മനുഷ്യരെ"),
    ("മനുഷ്യൻ", Case.GENITIVE, "മനുഷ്യരുടെ"),
    ("മകൾ", Case.GENITIVE, "മക്കളുടെ"),
    ("മകൾ", Case.DATIVE, "മക്കൾക്ക്"),
    ("മകൾ", Case.LOCATIVE, "മക്കളിൽ"),
]


@pytest.mark.parametrize("root, case, expected", IRREGULAR_OBLIQUE)
def test_irregular_plural_oblique(root, case, expected):
    r = _pl(root, case)
    assert r.surface == expected
    assert r.verified is True


def test_irregular_accusative_stays_overt_under_contradictory_animacy():
    # Irregulars are human/animate; a contradictory animacy=INANIMATE must NOT DOM
    # zero-mark them (അവർ -> overt അവരെ, never the bare അവർ).
    assert _pl("അവൻ", Case.ACCUSATIVE, animacy=Animacy.INANIMATE).surface == "അവരെ"


# --- ANIMATE (non-human) plurals: -കൾ like inanimate, but overt accusative ---

ANIMATE_FORMS = [
    (Case.NOMINATIVE, "ആനകൾ"),
    (Case.ACCUSATIVE, "ആനകളെ"),   # overt: DOM zero-marks inanimates only
    (Case.GENITIVE, "ആനകളുടെ"),
    (Case.DATIVE, "ആനകൾക്ക്"),
    (Case.SOCIATIVE, "ആനകളോട്"),
]


@pytest.mark.parametrize("case, expected", ANIMATE_FORMS)
def test_animate_nonhuman_plural(case, expected):
    r = _pl("ആന", case, animacy=Animacy.ANIMATE)
    assert r.surface == expected
    assert r.verified is True


# --- Soundness: animacy is still required -----------------------------------

@pytest.mark.parametrize("root", ["അമ്മ", "കാർ", "അധ്യാപകൻ", "തൂൺ"])
def test_plural_without_animacy_raises(root):
    with pytest.raises(NotImplementedError):
        _pl(root, Case.NOMINATIVE)


def test_done_classes_plurals_unaffected():
    # The five already-complete classes keep their animacy-blind plurals.
    assert synthesize_noun("മരം", Case.NOMINATIVE, number=PL).surface == "മരങ്ങൾ"
    assert synthesize_noun("കുട്ടി", Case.NOMINATIVE, number=PL).surface == "കുട്ടികൾ"
    assert synthesize_noun("വീട്", Case.GENITIVE, number=PL).surface == "വീടുകളുടെ"
