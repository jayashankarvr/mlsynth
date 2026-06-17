# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jayashankar R
"""Clitics: the final agglutination layer, attached after the fully inflected case form.

A clitic attaches to the surface word, not the stem (Word = ... + case + clitic). Three
native-ratified clitics are modelled: the additive ``-ഉം`` and interrogative ``-ഓ``
(vowel-initial), and the emphatic ``-തന്നെ`` (consonant-initial, geminating).

Boundary sandhi for the vowel-initial clitics:
  * vowel-final form: Agama glide (front vowel -> യ, back vowel -> വ;
    കുട്ടിയെ + ഉം -> കുട്ടിയെയും, പശു + ഉം -> പശുവും);
  * chillu-final: revert the chillu (മരത്തിൽ + ഉം -> മരത്തിലും). ``ർ`` is split by origin:
    a lexical -ർ noun reverts to retroflex റ (കാർ -> കാറും), a plural marker or pronoun to
    dental ര (അമ്മമാർ -> അമ്മമാരും, അവർ -> അവരും);
  * virama-final: drop the virama (മരത്തിന് + ഉം -> മരത്തിനും);
  * anuswara (ം): -ഉം drops the ം and adds the വ glide (മരം -> മരവും); -ഓ keeps ം as the
    consonant മ (മരം -> മരമോ).

The emphatic ``-തന്നെ`` is written joined and geminates its initial ത -> ത്ത after a vowel
or chillu ending (കുട്ടിയെത്തന്നെ, വീട്ടിൽത്തന്നെ). Clitics stack in the order
Case + Postposition + emphatic + additive/interrogative; apply :func:`with_clitic` in that
order, and the inner boundary takes the same Agama glide (തന്നെ + ഓ -> തന്നെയോ).

Boundaries not covered by the ratified rules (e.g. -തന്നെ after a virama or anuswara) raise
``UnsupportedClitic`` rather than guess.
"""
from __future__ import annotations

from .nouns import _CHILLU_BASE, _attach, _is_base_consonant, _is_vowel_sign
from .types import Clitic, Number, NounFeatures, SynthResult

# Vowel-sign-initial form of the vowel-initial clitics (attach directly onto a consonant).
_VOWEL_CLITIC_MATRA = {Clitic.UM: "ും", Clitic.O: "ോ"}
# After an anuswara ending: -ഉം drops ം and adds the വ glide; -ഓ keeps ം as the consonant മ.
_ANUSWARA_FORM = {Clitic.UM: "വും", Clitic.O: "മോ"}

# Agama glide by the preceding vowel (ratified): front i/ī/e/ē -> യ, back u/ū -> വ.
_FRONT_SIGNS = frozenset("ിീെേ")
_BACK_SIGNS = frozenset("ുൂ")


class UnsupportedClitic(NotImplementedError):
    """The clitic-boundary sandhi for this form is not yet native-ratified."""


def _attach_vowel_clitic(surface: str, clitic: Clitic, dental_r: bool) -> str:
    matra = _VOWEL_CLITIC_MATRA[clitic]
    last = surface[-1]
    if last == "ം":                          # anuswara: clitic-specific (മരവും / മരമോ)
        return surface[:-1] + _ANUSWARA_FORM[clitic]
    if last == "്":                          # consonant-final: drop the virama
        return surface[:-1] + matra
    if last == "ർ":                          # dental ര for plural/pronoun, retroflex റ otherwise
        return surface[:-1] + ("ര" if dental_r else "റ") + matra
    if last in _CHILLU_BASE:                  # ൽ/ൺ/ൾ/ൻ: unambiguous reversion via _attach
        return _attach(surface, matra)
    if last in _FRONT_SIGNS or _is_base_consonant(last):   # front vowel or inherent -അ -> യ
        return surface + "യ" + matra
    if last in _BACK_SIGNS:                   # back vowel -> വ
        return surface + "വ" + matra
    raise UnsupportedClitic(
        f"clitic boundary not yet ratified for {surface!r} + {clitic.value!r}"
    )


def _attach_emphatic(surface: str) -> str:
    # -തന്നെ geminates its ത -> ത്ത after a vowel-sign or chillu ending (ratified). A
    # bare-consonant (inherent -അ) ending, a virama, or an anuswara is not ratified, so raise.
    last = surface[-1]
    if last in _CHILLU_BASE or _is_vowel_sign(last):
        return surface + "ത്തന്നെ"
    raise UnsupportedClitic(f"emphatic -തന്നെ boundary not yet ratified: {surface!r}")


def _attach_clitic(surface: str, clitic: Clitic, dental_r: bool) -> str:
    if clitic is Clitic.EMPHATIC:
        return _attach_emphatic(surface)
    return _attach_vowel_clitic(surface, clitic, dental_r)


def with_clitic(result: SynthResult, clitic: Clitic) -> SynthResult:
    """Attach a clitic to an inflected form, applying the boundary sandhi.

    For an analytic (multi-word) form the clitic attaches to the final token only (the
    postposition governs the phrase): മരം കൊണ്ട് + ഉം -> മരം കൊണ്ടും. Stack clitics by applying
    this in order (emphatic before the additive/interrogative). An unratified boundary raises
    :class:`UnsupportedClitic`.
    """
    # ർ reverts to dental ര for plural markers and pronouns, retroflex റ otherwise.
    dental_r = result.features.number is Number.PLURAL or result.stem_class == "pronoun"
    if result.analytic and " " in result.surface:
        head, _, last_token = result.surface.rpartition(" ")
        surface = head + " " + _attach_clitic(last_token, clitic, dental_r)
    else:
        surface = _attach_clitic(result.surface, clitic, dental_r)
    f = result.features
    features = NounFeatures(
        case=f.case, number=f.number, animacy=f.animacy, register=f.register,
        gender=f.gender, clitic=clitic,
    )
    return SynthResult(
        surface=surface, root=result.root, features=features,
        morphemes=list(result.morphemes) + [clitic.value],
        stem_class=result.stem_class, provenance="native-2026", verified=result.verified,
        analytic=result.analytic,
    )
