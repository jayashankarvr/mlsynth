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


def _past(infinitive: str) -> tuple[str, bool]:
    """Return (past_surface, verified). ``verified`` is True for irregular-lexicon hits and
    the phonological ending-rules (-ിച്ചു/-ുത്തു/-ഞ്ഞു/-ട്ടു); it is False for the bare default
    -ഇ fallthrough, which is only a best guess and is wrong for unlisted irregulars
    (നടക്കുക -> *നടക്കി, really നടന്നു), as the native review noted the past is partly lexical."""
    if infinitive in _IRREGULAR_PAST:
        return _IRREGULAR_PAST[infinitive], True
    if infinitive.endswith("ിക്കുക"):
        return infinitive[:-6] + "ിച്ചു", True
    if infinitive.endswith("ുക്കുക"):
        return infinitive[:-6] + "ുത്തു", True
    if infinitive.endswith("യുക"):
        return infinitive[:-3] + "ഞ്ഞു", True
    if infinitive.endswith("ടുക"):
        prev = infinitive[:-3]
        if prev and prev[-1] in _SHORT_VOWELS:   # short vowel before ട -> geminate
            return prev + "ട്ടു", True            # ഇടുക -> ഇട്ടു, തൊടുക -> തൊട്ടു
        # long vowel / already-geminate cluster / consonant falls through to the default -ഇ
    return _stem(infinitive) + "ി", False         # default -ഇ: unconfirmed guess


def _past_plus(infinitive: str, matra_suffix: str) -> tuple[str, bool]:
    """Attach a matra-initial suffix to the past form (negative/conditional) and carry the
    past's ``verified`` through. A default -ഇ past takes the യ glide (ഓടി + ില്ല -> ഓടിയില്ല);
    a -ഉ past, or a past already ending in glide + ി (the irregular പോയി), drops its final
    vowel (വന്നു -> വന്നില്ല, പോയി -> പോയില്ല / പോയാൽ)."""
    past, verified = _past(infinitive)
    if past.endswith("ി"):
        if len(past) >= 2 and past[-2] in ("യ", "വ"):   # glide already present (പോയി)
            return past[:-1] + matra_suffix, verified
        return past + "യ" + matra_suffix, verified
    if past.endswith("ു"):
        return past[:-1] + matra_suffix, verified
    raise UnsupportedVerb(f"cannot attach {matra_suffix!r} to past {past!r}")


def synthesize_verb(infinitive: str, form: VerbForm) -> VerbResult:
    """Generate a finite verb form from its -ഉക infinitive.

    Unsupported infinitive shapes or unencoded forms raise :class:`UnsupportedVerb`. Forms
    that the rules cannot guarantee (a default-guess past, or an imperative of a verb in the
    irregular lexicon, which may be suppletive like വരുക -> വാ) carry ``verified=False`` rather
    than over-claim native ratification. Never a silently wrong, silently-verified form.
    """
    in_lexicon = infinitive in _IRREGULAR_PAST
    irregular = False

    if form is VerbForm.PAST:
        surface, verified = _past(infinitive)
        irregular = in_lexicon
    elif form is VerbForm.PAST_NEGATIVE:
        surface, verified = _past_plus(infinitive, "ില്ല")
        irregular = in_lexicon
    elif form is VerbForm.CONDITIONAL:
        surface, verified = _past_plus(infinitive, "ാൽ")
        irregular = in_lexicon
    else:
        stem = _stem(infinitive)
        verified = True
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
            verified = not in_lexicon   # suppletive risk (വരുക -> വാ, not വര്)
        elif form is VerbForm.IMPERATIVE_POLITE:
            surface = stem + "ൂ"
            verified = not in_lexicon
        elif form is VerbForm.HORTATIVE:
            surface = stem + "ട്ടെ"
        elif form is VerbForm.PROMISSIVE:
            surface = stem + "ാം"
        else:
            raise UnsupportedVerb(f"verb form {form!r} not encoded")

    return VerbResult(
        surface=surface, infinitive=infinitive, form=form,
        provenance="native-2026", verified=verified, irregular=irregular,
    )
