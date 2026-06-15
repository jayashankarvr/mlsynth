# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jayashankar R
"""Rule-based Malayalam noun synthesis: (root + features) -> inflected surface form.

The forward (generation) counterpart to morphological analysis, applying the
ending-conditioned rules in :mod:`mlsynth.rules`. Every result carries the rule's
provenance and a ``verified`` flag (true only for native-ratified forms).

Two cross-cutting rules from the native review / SMC docs:
  * Differential object marking (DOM): an inanimate noun's accusative defaults to the
    bare form (മരം), the overt form (മരത്തെ) only on request; an animate noun's
    accusative is always overt.
  * Register: the instrumental is synthetic by default (മരത്താൽ) but analytic in the
    colloquial register (മരം കൊണ്ട്).
"""
from __future__ import annotations

from typing import List, Optional

from .rules import CLASSES, NounClass
from .types import Animacy, Case, Gender, NounFeatures, Number, Register, SynthResult

# Chillu -> base consonant (a chillu reverts before a following vowel sign).
_CHILLU_BASE = {
    "ൺ": "ണ", "ൻ": "ന", "ർ": "ര", "ൽ": "ല", "ൾ": "ള", "ൿ": "ക",
}


def _is_vowel_sign(ch: str) -> bool:
    o = ord(ch)
    return 0x0D3E <= o <= 0x0D4C or o in (0x0D57, 0x0D62, 0x0D63)


def _is_independent_vowel(ch: str) -> bool:
    o = ord(ch)
    return 0x0D05 <= o <= 0x0D14 or o in (0x0D60, 0x0D61)


def _attach(stem: str, suffix: str) -> str:
    """Join a matra-initial suffix to a stem, reverting a trailing chillu to its base."""
    if not suffix:
        return stem
    if stem and _is_vowel_sign(suffix[0]) and stem[-1] in _CHILLU_BASE:
        stem = stem[:-1] + _CHILLU_BASE[stem[-1]]
    return stem + suffix


class UnsupportedRoot(ValueError):
    """No noun class matches the root and none was given explicitly."""


def list_supported_classes() -> List[str]:
    return sorted(CLASSES)


def _has_base_letter(s: str) -> bool:
    # Reject input made only of signs/virama/anusvara or non-Malayalam text.
    return any("അ" <= ch <= "ഺ" for ch in s)


def _class_matches(cls: NounClass, root: str) -> bool:
    for e in cls.endings:
        if root.endswith(e):
            if cls.pre:
                pre = root[: -len(e)]
                if not pre:
                    return False
                is_vowel = _is_vowel_sign(pre[-1]) or _is_independent_vowel(pre[-1])
                # consonant+anuswara (മരം) vs vowel+anuswara (കലാം, ഓം): same ending,
                # disambiguated by what precedes it.
                if cls.pre == "consonant" and is_vowel:
                    return False
                if cls.pre == "vowel" and not is_vowel:
                    return False
            return True
    return False


def _resolve_class(root: str, stem_class: Optional[str]) -> NounClass:
    if stem_class is not None:
        try:
            cls = CLASSES[stem_class]
        except KeyError:
            raise UnsupportedRoot(
                f"unknown stem_class {stem_class!r}; supported: {list_supported_classes()}"
            ) from None
        if not _class_matches(cls, root):
            raise UnsupportedRoot(
                f"root {root!r} does not fit class {cls.name!r} (endings {cls.endings}"
                + (f", {cls.pre}-stem only)" if cls.pre else ")")
            )
        return cls
    for cls in sorted(
        CLASSES.values(), key=lambda c: max(len(e) for e in c.endings), reverse=True
    ):
        if _class_matches(cls, root):
            return cls
    raise UnsupportedRoot(
        f"cannot infer a noun class for root {root!r}; pass stem_class= explicitly "
        f"(supported: {list_supported_classes()})"
    )


def synthesize_noun(
    root: str,
    case: Case,
    number: Number = Number.SINGULAR,
    *,
    animacy: Optional[Animacy] = None,
    register: Register = Register.FORMAL,
    gender: Optional[Gender] = None,
    stem_class: Optional[str] = None,
    marked: bool = False,
) -> SynthResult:
    """Generate the inflected surface form of ``root`` for the given features.

    ``animacy`` drives DOM (accusative) and is recorded on the result; with it unknown,
    the accusative defaults to the overt form. ``marked=True`` forces the overt
    accusative for an inanimate noun. ``gender`` is recorded but unused by current
    classes. Unencoded feature combinations raise :class:`NotImplementedError`;
    unresolvable/ill-formed roots raise :class:`UnsupportedRoot`. Never a silently
    wrong form.
    """
    if not root:
        raise UnsupportedRoot("root must be a non-empty string")
    if not _has_base_letter(root):
        raise UnsupportedRoot(f"root {root!r} contains no Malayalam base letter")
    cls = _resolve_class(root, stem_class)
    features = NounFeatures(
        case=case, number=number, animacy=animacy, register=register, gender=gender
    )

    def _result(surface, morphemes, provenance, verified, analytic=False):
        return SynthResult(
            surface=surface, root=root, features=features, morphemes=morphemes,
            stem_class=cls.name, provenance=provenance, verified=verified, analytic=analytic,
        )

    table = cls.plural_cases if number is Number.PLURAL else cls.cases
    try:
        rule = table[case]
    except KeyError:
        raise NotImplementedError(
            f"case {case.value!r} ({number.value}) not yet encoded for class {cls.name!r}"
        ) from None

    # The nominative form of the requested number (used by DOM and the analytic register).
    nom_rule = table[Case.NOMINATIVE]
    nom_stem = (cls.plural_marker.apply(root) if number is Number.PLURAL else root)
    nominative = _attach(nom_stem, nom_rule.suffix) if nom_rule.use_oblique else nom_stem

    # Colloquial instrumental is analytic (nominative + കൊണ്ട്); verified/provenance
    # track the nominative, so non-ratified inputs aren't over-claimed (worksheet Q2).
    if case is Case.INSTRUMENTAL and register is Register.COLLOQUIAL:
        return _result(nominative + " കൊണ്ട്", [nominative, "കൊണ്ട്"],
                       nom_rule.provenance, nom_rule.verified, analytic=True)

    # DOM: inanimate accusative is the bare nominative (worksheet Q1); inherits its flags.
    if case is Case.ACCUSATIVE and animacy is Animacy.INANIMATE and not marked:
        return _result(nominative, [nominative], nom_rule.provenance, nom_rule.verified)

    if number is Number.PLURAL:
        stem = cls.plural_marker.apply(root)
        surface = _attach(stem, rule.suffix)
        morphemes = [stem, rule.suffix] if rule.suffix else [stem]
        return _result(surface, morphemes, rule.provenance, rule.verified)

    if rule.oblique is not None:
        stem = rule.oblique.apply(root)       # per-case stem (e.g. ട് gemination)
    elif rule.use_oblique:
        stem = cls.oblique.apply(root)
    else:
        stem = root
    surface = _attach(stem, rule.suffix)
    morphemes = [stem, rule.suffix] if rule.suffix else [stem]
    return _result(surface, morphemes, rule.provenance, rule.verified)
