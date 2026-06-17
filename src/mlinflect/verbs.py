# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jayashankar R
"""Rule-based Malayalam verb synthesis: (infinitive + form) -> inflected surface form.

Verbs are cited by their -ഉക infinitive (ഓടുക 'to run'). Present and future are regular
(replace -ഉക with -ഉന്നു / -ഉം). The past is allomorphic, selected by the infinitive
ending, with an irregular-verb lexicon checked first (native worksheet, Part 2/3):

  * -ിക്കുക -> -ിച്ചു   (അടിക്കുക -> അടിച്ചു)
  * -ുക്കുക -> -ുത്തു   (കൊടുക്കുക -> കൊടുത്തു)
  * -ടുക   -> -ട്ടു    (ഇടുക -> ഇട്ടു), but -ാടുക takes the default -ഇ (ചാടുക -> ചാടി)
  * -യുക   -> -ഞ്ഞു    (പണിയുക -> പണിഞ്ഞു)
  * default -> -ഇ      (ഓടുക -> ഓടി; also നോക്കുക -> നോക്കി, കലങ്ങുക -> കലങ്ങി)

Negation, imperative, and a few moods build on the stem or the past form (Part 4). Forms
not covered by the ratified rules raise :class:`UnsupportedVerb`.
"""
from __future__ import annotations

from .types import VerbForm, VerbResult

# Irregular past forms, checked before the allomorphy rules (native worksheet, Part 3).
_IRREGULAR_PAST = {
    "വരുക": "വന്നു",          # come
    "പോകുക": "പോയി",         # go
    "കാണുക": "കണ്ടു",         # see
    "ചെയ്യുക": "ചെയ്തു",       # do
    "തിന്നുക": "തിന്നു",       # eat
    "ചാവുക": "ചത്തു",         # die
    "ഉണ്ണുക": "ഉണ്ടു",        # eat (formal)
    "തരിക": "തന്നു",          # give (to me)
    "കാക്കുക": "കാത്തു",       # wait/guard
    "നിൽക്കുക": "നിന്നു",      # stand
    "തോൽക്കുക": "തോറ്റു",      # lose
    "നോവുക": "നൊന്തു",       # ache
    "കൊല്ലുക": "കൊന്നു",      # kill
    "വീഴുക": "വീണു",         # fall
    "എഴുന്നേൽക്കുക": "എഴുന്നേറ്റു",  # get up
}


# Short vowel nuclei (matras + independent). A -ടുക verb geminates (-ട്ടു) only after a SHORT
# vowel right before the ട (ഇടുക -> ഇട്ടു, തൊടുക -> തൊട്ടു); a long vowel (ഓടുക -> ഓടി,
# ചാടുക -> ചാടി) or an already-geminate cluster (ഞെട്ടുക, where a virama precedes -> ഞെട്ടി)
# takes the default -ഇ. Requiring an explicit short-vowel nucleus (not just "not long") keeps a
# virama or bare consonant before ട from triggering a spurious second gemination.
_SHORT_VOWELS = frozenset("ിുെൊ" + "അഇഉഎഒ")


class UnsupportedVerb(ValueError):
    """The infinitive shape is not supported, or the form is not encoded."""


def _stem(infinitive: str) -> str:
    """The bare stem: the -ഉക infinitive minus its -ഉക ending (ഓടുക -> ഓട)."""
    if not infinitive.endswith("ുക"):
        raise UnsupportedVerb(
            f"infinitive {infinitive!r} does not end in -ഉക; only -ഉക verbs are supported"
        )
    return infinitive[:-2]


def _past(infinitive: str) -> str:
    """The past form: irregular lexicon first, then ending-conditioned allomorphy."""
    if infinitive in _IRREGULAR_PAST:
        return _IRREGULAR_PAST[infinitive]
    if infinitive.endswith("ിക്കുക"):
        return infinitive[:-6] + "ിച്ചു"
    if infinitive.endswith("ുക്കുക"):
        return infinitive[:-6] + "ുത്തു"
    if infinitive.endswith("യുക"):
        return infinitive[:-3] + "ഞ്ഞു"
    if infinitive.endswith("ടുക"):
        prev = infinitive[:-3]
        if prev and prev[-1] in _SHORT_VOWELS:   # short vowel before ട -> geminate
            return prev + "ട്ടു"                  # ഇടുക -> ഇട്ടു, തൊടുക -> തൊട്ടു
        # long vowel / already-geminate cluster / consonant falls through to the default -ഇ
    return _stem(infinitive) + "ി"            # default -ഇ (ഓടി, നോക്കി, കലങ്ങി, ഞെട്ടി)


def _past_plus(infinitive: str, matra_suffix: str) -> str:
    """Attach a matra-initial suffix to the past form (for the negative and conditional):
    a default -ഇ past takes the യ glide (ഓടി + ില്ല -> ഓടിയില്ല); a -ഉ past, or a past that
    already ends in a glide + ി (the irregular പോയി), drops its final vowel (വന്നു -> വന്നില്ല,
    പോയി -> പോയില്ല / പോയാൽ)."""
    past = _past(infinitive)
    if past.endswith("ി"):
        if len(past) >= 2 and past[-2] in ("യ", "വ"):   # glide already present (പോയി)
            return past[:-1] + matra_suffix
        return past + "യ" + matra_suffix
    if past.endswith("ു"):
        return past[:-1] + matra_suffix
    raise UnsupportedVerb(f"cannot attach {matra_suffix!r} to past {past!r}")


def synthesize_verb(infinitive: str, form: VerbForm) -> VerbResult:
    """Generate a finite verb form from its -ഉക infinitive.

    Unsupported infinitive shapes or unencoded forms raise :class:`UnsupportedVerb`.
    Never a silently wrong form.
    """
    irregular = infinitive in _IRREGULAR_PAST

    if form is VerbForm.PAST:
        surface = _past(infinitive)
    elif form is VerbForm.PAST_NEGATIVE:
        surface = _past_plus(infinitive, "ില്ല")
    elif form is VerbForm.CONDITIONAL:
        surface = _past_plus(infinitive, "ാൽ")
    else:
        stem = _stem(infinitive)
        if form is VerbForm.PRESENT:
            surface = stem + "ുന്നു"
        elif form is VerbForm.FUTURE:
            surface = stem + "ും"
        elif form is VerbForm.PRESENT_NEGATIVE:
            surface = stem + "ുന്നില്ല"
        elif form is VerbForm.FUTURE_NEGATIVE:
            surface = stem + "ില്ല"
        elif form is VerbForm.IMPERATIVE_INFORMAL:
            surface = stem + "്"
        elif form is VerbForm.IMPERATIVE_POLITE:
            surface = stem + "ൂ"
        elif form is VerbForm.HORTATIVE:
            surface = stem + "ട്ടെ"
        elif form is VerbForm.PROMISSIVE:
            surface = stem + "ാം"
        else:
            raise UnsupportedVerb(f"verb form {form!r} not encoded")
        irregular = False  # present/future/imperative/moods are regular even for irregulars

    return VerbResult(
        surface=surface, infinitive=infinitive, form=form,
        provenance="native-2026", verified=True, irregular=irregular,
    )
