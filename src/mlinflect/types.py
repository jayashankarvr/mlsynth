# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jayashankar R
"""Typed feature inventory and result types for Malayalam noun synthesis.

Feature values match the mlmorph tagset (gitlab.com/smc/mlmorph) for interop, with
two features mlmorph leaves lexical: ``Animacy`` (drives differential object marking
and plural choice) and ``Register`` (synthetic vs analytic forms).
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Case(str, Enum):
    NOMINATIVE = "nominative"
    ACCUSATIVE = "accusative"
    DATIVE = "dative"
    GENITIVE = "genitive"
    SOCIATIVE = "sociative"
    LOCATIVE = "locative"
    INSTRUMENTAL = "instrumental"
    VOCATIVE = "vocative"
    ABLATIVE = "ablative"
    ALLATIVE = "allative"
    PERLATIVE = "perlative"


class Number(str, Enum):
    SINGULAR = "singular"
    PLURAL = "plural"


class Gender(str, Enum):
    MASCULINE = "masculine"
    FEMININE = "feminine"
    NEUTRAL = "neutral"


class Animacy(str, Enum):
    """Lexical animacy/humanness. Governs accusative marking (DOM) and plural choice."""

    HUMAN = "human"
    ANIMATE = "animate"  # animate, non-human (e.g. കിളി 'bird')
    INANIMATE = "inanimate"


class Register(str, Enum):
    FORMAL = "formal"        # synthetic forms (e.g. instrumental മരത്താൽ)
    COLLOQUIAL = "colloquial"  # analytic forms (e.g. മരം കൊണ്ട്)


class Clitic(str, Enum):
    """Post-inflectional clitics, attached after the case form (the final agglutination layer)."""

    UM = "ഉം"        # additive 'and / even'
    O = "ഓ"          # interrogative (yes/no)
    EMPHATIC = "തന്നെ"  # emphatic 'self / the very'


@dataclass(frozen=True)
class NounFeatures:
    case: Case
    number: Number = Number.SINGULAR
    animacy: Optional[Animacy] = None
    register: Register = Register.FORMAL
    gender: Optional[Gender] = None
    clitic: Optional["Clitic"] = None


@dataclass(frozen=True)
class SynthResult:
    """One synthesized inflected form.

    ``provenance`` is the citation key of the rule that produced it (see REFERENCES.md);
    ``verified`` is true only for native-ratified forms; ``analytic`` is true for
    multi-word forms (e.g. the colloquial instrumental മരം കൊണ്ട്).
    """

    surface: str
    root: str
    features: NounFeatures
    morphemes: List[str]
    stem_class: str
    provenance: str
    verified: bool
    analytic: bool = False


class VerbForm(str, Enum):
    """Finite verb forms (the foundational set; aspects/participles/voice come later)."""

    PRESENT = "present"
    FUTURE = "future"
    PAST = "past"
    PRESENT_NEGATIVE = "present_negative"
    PAST_NEGATIVE = "past_negative"
    FUTURE_NEGATIVE = "future_negative"
    IMPERATIVE_INFORMAL = "imperative_informal"
    IMPERATIVE_POLITE = "imperative_polite"
    CONDITIONAL = "conditional"
    HORTATIVE = "hortative"
    PROMISSIVE = "promissive"


@dataclass(frozen=True)
class VerbResult:
    """One synthesized verb form.

    ``provenance`` cites the rule (see REFERENCES.md); ``verified`` is true only for
    native-ratified forms; ``irregular`` flags a form taken from the exception lexicon.
    """

    surface: str
    infinitive: str
    form: VerbForm
    provenance: str
    verified: bool
    irregular: bool = False
