# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jayashankar R
"""Verb synthesis: tenses, past allomorphy + irregulars, negation, imperative, moods.

Expected forms are the native-ratified answers from the verb worksheet (Parts 1-4).
"""
import pytest

from mlinflect import VerbForm, UnsupportedVerb, synthesize_verb as v


# --- Part 1: present and future (regular) ---
@pytest.mark.parametrize("inf, present, future", [
    ("ഓടുക", "ഓടുന്നു", "ഓടും"),
    ("അടിക്കുക", "അടിക്കുന്നു", "അടിക്കും"),
    ("പറയുക", "പറയുന്നു", "പറയും"),
    ("ചിരിക്കുക", "ചിരിക്കുന്നു", "ചിരിക്കും"),
])
def test_present_future(inf, present, future):
    assert v(inf, VerbForm.PRESENT).surface == present
    assert v(inf, VerbForm.FUTURE).surface == future


# --- Part 2/3: past (allomorphy by ending + irregular lexicon) ---
REGULAR_PAST = [
    ("ഓടുക", "ഓടി"),            # default -ഇ
    ("കലങ്ങുക", "കലങ്ങി"),       # -ങ്ങുക default
    ("പണിയുക", "പണിഞ്ഞു"),       # -യുക -> -ഞ്ഞു
    ("ഇടുക", "ഇട്ടു"),           # short vowel + ടുക -> -ട്ടു
    ("തൊടുക", "തൊട്ടു"),         # short vowel + ടുക -> -ട്ടു
    ("ചാടുക", "ചാടി"),           # long vowel + ടുക -> default
    ("ഞെട്ടുക", "ഞെട്ടി"),       # already-geminate -ട്ടുക -> default (not -ട്ട്ടു)
    ("മുട്ടുക", "മുട്ടി"),        # already-geminate -ട്ടുക -> default
    ("പറിക്കുക", "പറിച്ചു"),      # -ിക്കുക -> -ിച്ചു
    ("കൊടുക്കുക", "കൊടുത്തു"),    # -ുക്കുക -> -ുത്തു
    ("നോക്കുക", "നോക്കി"),        # vowel + ക്കുക -> default
    ("അടിക്കുക", "അടിച്ചു"),
    ("പറയുക", "പറഞ്ഞു"),
    ("കുടിക്കുക", "കുടിച്ചു"),
]

IRREGULAR_PAST = [
    ("വരുക", "വന്നു"), ("പോകുക", "പോയി"), ("കാണുക", "കണ്ടു"), ("ചെയ്യുക", "ചെയ്തു"),
    ("തിന്നുക", "തിന്നു"), ("ചാവുക", "ചത്തു"), ("നിൽക്കുക", "നിന്നു"),
    ("കൊല്ലുക", "കൊന്നു"), ("വീഴുക", "വീണു"), ("കാക്കുക", "കാത്തു"),
]


@pytest.mark.parametrize("inf, past", REGULAR_PAST)
def test_regular_past(inf, past):
    r = v(inf, VerbForm.PAST)
    assert r.surface == past
    assert r.irregular is False


@pytest.mark.parametrize("inf, past", IRREGULAR_PAST)
def test_irregular_past(inf, past):
    r = v(inf, VerbForm.PAST)
    assert r.surface == past
    assert r.irregular is True
    assert r.verified is True  # lexicon hits are ratified


# verified gating: the ending-rules and lexicon are confident; the bare default -ഇ is a guess
# (wrong for unlisted irregulars like നടക്കുക -> really നടന്നു), so it must NOT claim verified.
@pytest.mark.parametrize("inf, verified", [
    ("പറിക്കുക", True),    # -ിക്കുക rule
    ("കൊടുക്കുക", True),   # -ുക്കുക rule
    ("പണിയുക", True),      # -യുക rule
    ("ഇടുക", True),        # short -ടുക rule
    ("ഓടുക", False),       # default -ഇ: unconfirmed
    ("നോക്കുക", False),    # default -ഇ: unconfirmed
    ("നടക്കുക", False),    # default -ഇ guess that is actually irregular (നടന്നു)
])
def test_past_verified_gating(inf, verified):
    assert v(inf, VerbForm.PAST).verified is verified


def test_suppletive_imperative_not_verified():
    # An irregular/suppletive verb's imperative may be wrong (വരുക -> വാ, not വര്), so the
    # rule-generated imperative must not claim verified; a regular verb's imperative does.
    assert v("ഓടുക", VerbForm.IMPERATIVE_INFORMAL).verified is True
    assert v("വരുക", VerbForm.IMPERATIVE_INFORMAL).verified is False
    assert v("പോകുക", VerbForm.IMPERATIVE_POLITE).verified is False


# --- Part 4: negation, imperative, moods (ഓടുക) ---
@pytest.mark.parametrize("form, expected", [
    (VerbForm.PRESENT_NEGATIVE, "ഓടുന്നില്ല"),
    (VerbForm.PAST_NEGATIVE, "ഓടിയില്ല"),
    (VerbForm.FUTURE_NEGATIVE, "ഓടില്ല"),
    (VerbForm.IMPERATIVE_INFORMAL, "ഓട്"),
    (VerbForm.IMPERATIVE_POLITE, "ഓടൂ"),
    (VerbForm.CONDITIONAL, "ഓടിയാൽ"),
    (VerbForm.HORTATIVE, "ഓടട്ടെ"),
    (VerbForm.PROMISSIVE, "ഓടാം"),
])
def test_oduka_forms(form, expected):
    assert v("ഓടുക", form).surface == expected


# Negation/conditional built on an irregular or -ഉ past.
@pytest.mark.parametrize("inf, form, expected", [
    ("വരുക", VerbForm.PAST_NEGATIVE, "വന്നില്ല"),
    ("വരുക", VerbForm.CONDITIONAL, "വന്നാൽ"),
    ("അടിക്കുക", VerbForm.PAST_NEGATIVE, "അടിച്ചില്ല"),
    ("അടിക്കുക", VerbForm.CONDITIONAL, "അടിച്ചാൽ"),
    ("കാണുക", VerbForm.PAST_NEGATIVE, "കണ്ടില്ല"),
    ("ചെയ്യുക", VerbForm.PAST_NEGATIVE, "ചെയ്തില്ല"),
    # പോകുക's past പോയി already ends in a glide+ി; must NOT double-glide.
    ("പോകുക", VerbForm.PAST_NEGATIVE, "പോയില്ല"),
    ("പോകുക", VerbForm.CONDITIONAL, "പോയാൽ"),
])
def test_past_derived_forms(inf, form, expected):
    assert v(inf, form).surface == expected


# Present/future of an irregular verb stay regular (only the past is irregular).
def test_irregular_present_is_regular():
    assert v("വരുക", VerbForm.PRESENT).surface == "വരുന്നു"
    assert v("വരുക", VerbForm.FUTURE).surface == "വരും"


# --- soundness ---
def test_non_uka_infinitive_raises():
    with pytest.raises(UnsupportedVerb):
        v("ABC", VerbForm.PRESENT)
    with pytest.raises(UnsupportedVerb):
        v("മരം", VerbForm.PRESENT)
