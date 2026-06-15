# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jayashankar R
"""Tests for mlsynth noun synthesis.

Expected surface forms are typed as independent literals (the forms attested in the
sources / native worksheet), and the engine constructs them from root + rules, so a
passing test confirms the rule encoding reproduces the attested paradigm rather than
being a tautology.
"""
import pytest

from mlsynth import (
    Animacy,
    Case,
    Number,
    Register,
    UnsupportedRoot,
    list_supported_classes,
    synthesize_noun,
)

# മരം 'tree', consonant + anuswara class.
AM = "മരം"
AM_SG = {
    Case.NOMINATIVE: "മരം", Case.ACCUSATIVE: "മരത്തെ", Case.DATIVE: "മരത്തിന്",
    Case.GENITIVE: "മരത്തിന്റെ", Case.SOCIATIVE: "മരത്തോട്", Case.LOCATIVE: "മരത്തിൽ",
    Case.INSTRUMENTAL: "മരത്താൽ", Case.VOCATIVE: "മരമേ", Case.ABLATIVE: "മരത്തിൽനിന്ന്",
    Case.ALLATIVE: "മരത്തിലേക്ക്", Case.PERLATIVE: "മരത്തിലൂടെ",
}
AM_PL = {
    Case.NOMINATIVE: "മരങ്ങൾ", Case.ACCUSATIVE: "മരങ്ങളെ", Case.DATIVE: "മരങ്ങൾക്ക്",
    Case.GENITIVE: "മരങ്ങളുടെ", Case.SOCIATIVE: "മരങ്ങളോട്", Case.LOCATIVE: "മരങ്ങളിൽ",
    Case.INSTRUMENTAL: "മരങ്ങളാൽ", Case.VOCATIVE: "മരങ്ങളേ",
}

# കുട്ടി 'child', vowel-final -ി class.
KUTTI = "കുട്ടി"
KUTTI_SG = {
    Case.NOMINATIVE: "കുട്ടി", Case.ACCUSATIVE: "കുട്ടിയെ", Case.DATIVE: "കുട്ടിക്ക്",
    Case.GENITIVE: "കുട്ടിയുടെ", Case.SOCIATIVE: "കുട്ടിയോട്", Case.LOCATIVE: "കുട്ടിയിൽ",
    Case.INSTRUMENTAL: "കുട്ടിയാൽ", Case.VOCATIVE: "കുട്ടിയേ",
}
KUTTI_PL = {
    Case.NOMINATIVE: "കുട്ടികൾ", Case.ACCUSATIVE: "കുട്ടികളെ", Case.DATIVE: "കുട്ടികൾക്ക്",
    Case.GENITIVE: "കുട്ടികളുടെ", Case.VOCATIVE: "കുട്ടികളേ",
}


@pytest.mark.parametrize("case,expected", list(AM_SG.items()))
def test_am_singular(case, expected):
    assert synthesize_noun(AM, case).surface == expected


@pytest.mark.parametrize("case,expected", list(AM_PL.items()))
def test_am_plural(case, expected):
    assert synthesize_noun(AM, case, number=Number.PLURAL).surface == expected


@pytest.mark.parametrize("case,expected", list(KUTTI_SG.items()))
def test_i_vowel_singular(case, expected):
    assert synthesize_noun(KUTTI, case).surface == expected


@pytest.mark.parametrize("case,expected", list(KUTTI_PL.items()))
def test_i_vowel_plural(case, expected):
    assert synthesize_noun(KUTTI, case, number=Number.PLURAL).surface == expected


# --- new classes ---

@pytest.mark.parametrize("root,case,expected", [
    ("കലാം", Case.ACCUSATIVE, "കലാമിനെ"),
    ("കലാം", Case.GENITIVE, "കലാമിന്റെ"),
    ("ടീം", Case.GENITIVE, "ടീമിന്റെ"),
    ("ഓം", Case.ACCUSATIVE, "ഓമിനെ"),      # independent vowel + anuswara
    ("ക്രീം", Case.ACCUSATIVE, "ക്രീമിനെ"),
    ("കലാം", Case.SOCIATIVE, "കലാമിനോട്"),
    ("കലാം", Case.VOCATIVE, "കലാമേ"),
    ("കലാം", Case.ABLATIVE, "കലാമിൽനിന്ന്"),
])
def test_vowel_anuswara(root, case, expected):
    assert synthesize_noun(root, case).surface == expected


@pytest.mark.parametrize("root,case,expected", [
    ("പശു", Case.GENITIVE, "പശുവിന്റെ"),
    ("പശു", Case.VOCATIVE, "പശുവേ"),
    ("മുത്തു", Case.VOCATIVE, "മുത്തുവേ"),
    ("പശു", Case.DATIVE, "പശുവിന്"),
    ("പശു", Case.ACCUSATIVE, "പശുവിനെ"),
    ("പശു", Case.SOCIATIVE, "പശുവിനോട്"),
    ("പശു", Case.INSTRUMENTAL, "പശുവിനാൽ"),
])
def test_u_vowel(root, case, expected):
    assert synthesize_noun(root, case).surface == expected


def test_u_vowel_plural_marker():
    assert synthesize_noun("പശു", Case.NOMINATIVE, number=Number.PLURAL).surface == "പശുക്കൾ"


@pytest.mark.parametrize("root,case,expected", [
    ("വീട്", Case.GENITIVE, "വീടിന്റെ"),       # plain stem
    ("വീട്", Case.DATIVE, "വീടിന്"),
    ("വീട്", Case.ACCUSATIVE, "വീടിനെ"),
    ("വീട്", Case.VOCATIVE, "വീടേ"),
    ("വീട്", Case.LOCATIVE, "വീട്ടിൽ"),         # geminated stem
    ("വീട്", Case.ALLATIVE, "വീട്ടിലേക്ക്"),
    ("വീട്", Case.ABLATIVE, "വീട്ടിൽനിന്ന്"),
    ("വീട്", Case.PERLATIVE, "വീട്ടിലൂടെ"),
    ("കാട്", Case.GENITIVE, "കാടിന്റെ"),
    ("കാട്", Case.LOCATIVE, "കാട്ടിൽ"),
])
def test_t_geminate(root, case, expected):
    assert synthesize_noun(root, case).surface == expected


def test_vocative():
    assert synthesize_noun("മരം", Case.VOCATIVE).surface == "മരമേ"
    assert synthesize_noun("മരം", Case.VOCATIVE, number=Number.PLURAL).surface == "മരങ്ങളേ"
    assert synthesize_noun("കുട്ടി", Case.VOCATIVE, number=Number.PLURAL).surface == "കുട്ടികളേ"


# --- differential object marking + register ---

def test_inanimate_accusative_defaults_bare():
    assert synthesize_noun(AM, Case.ACCUSATIVE, animacy=Animacy.INANIMATE).surface == "മരം"


def test_inanimate_accusative_marked_on_request():
    assert synthesize_noun(AM, Case.ACCUSATIVE, animacy=Animacy.INANIMATE, marked=True).surface == "മരത്തെ"


def test_animate_accusative_is_overt():
    assert synthesize_noun(KUTTI, Case.ACCUSATIVE, animacy=Animacy.HUMAN).surface == "കുട്ടിയെ"


def test_colloquial_instrumental_is_analytic():
    r = synthesize_noun(AM, Case.INSTRUMENTAL, register=Register.COLLOQUIAL)
    assert r.surface == "മരം കൊണ്ട്" and r.analytic is True


def test_dom_and_register_inherit_nominative_flags():
    # The DOM/register forms inherit verified/provenance from the nominative they are
    # built on, so they never over-claim relative to it.
    nom = synthesize_noun(KUTTI, Case.NOMINATIVE)
    bare = synthesize_noun(KUTTI, Case.ACCUSATIVE, animacy=Animacy.INANIMATE)
    assert (bare.surface, bare.verified, bare.provenance) == (nom.surface, nom.verified, nom.provenance)


# --- verified / provenance discipline ---

def test_native_ratified_forms_are_verified():
    assert synthesize_noun(AM, Case.ABLATIVE).verified is True            # worksheet C
    assert synthesize_noun(KUTTI, Case.GENITIVE).provenance == "native-14"
    assert synthesize_noun("വീട്", Case.LOCATIVE).verified is True


def test_extrapolated_forms_are_unverified():
    # u_vowel plural: only the -ക്കൾ marker is native-given; the oblique paradigm is extrapolated.
    r = synthesize_noun("പശു", Case.GENITIVE, number=Number.PLURAL)
    assert r.surface == "പശുക്കളുടെ" and r.verified is False


def test_morphemes_join_to_surface():
    r = synthesize_noun(AM, Case.LOCATIVE)
    assert "".join(r.morphemes) == r.surface


# --- soundness: raise, never silently wrong ---

@pytest.mark.parametrize("root", ["അമ്മ", "പുഴ", "അവൻ", "നായർ", "സ്ത്രീ", "ABC", "123", "ി", ""])
def test_unsupported_roots_raise(root):
    with pytest.raises(UnsupportedRoot):
        synthesize_noun(root, Case.GENITIVE)


def test_explicit_mismatched_class_raises():
    with pytest.raises(UnsupportedRoot):
        synthesize_noun(AM, Case.ACCUSATIVE, stem_class="i_vowel")


def test_unencoded_case_raises():
    with pytest.raises(NotImplementedError):
        synthesize_noun("കലാം", Case.INSTRUMENTAL)    # vowel_anuswara has no instrumental yet


def test_unencoded_plural_raises():
    with pytest.raises(NotImplementedError):
        synthesize_noun("കലാം", Case.GENITIVE, number=Number.PLURAL)  # no plural encoded


def test_supported_classes_listed():
    cls = list_supported_classes()
    assert {"am_neuter", "i_vowel", "vowel_anuswara", "u_vowel", "ṭ_geminate"} <= set(cls)
