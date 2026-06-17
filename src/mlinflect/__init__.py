# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jayashankar R
"""A rule-based Malayalam morphological synthesizer.

Forward morphological generation (root + features -> inflected surface form),
starting with noun inflection. Rules are declarative and provenance-tagged; see
REFERENCES.md for the linguistic sources and the project's native-ratification
workflow.
"""
from .clitics import UnsupportedClitic, with_clitic
from .gender import UnsupportedDerivation, derive_feminine
from .nouns import UnsupportedRoot, list_supported_classes, synthesize_noun
from .pronouns import is_pronoun, list_pronouns
from .types import (
    Animacy,
    Case,
    Clitic,
    Gender,
    NounFeatures,
    Number,
    Register,
    SynthResult,
    VerbForm,
    VerbResult,
)
from .verbs import UnsupportedVerb, synthesize_verb

__version__ = "0.1.1"
__all__ = [
    "Animacy",
    "Case",
    "Clitic",
    "Gender",
    "Number",
    "NounFeatures",
    "Register",
    "SynthResult",
    "VerbForm",
    "VerbResult",
    "synthesize_noun",
    "synthesize_verb",
    "with_clitic",
    "list_supported_classes",
    "is_pronoun",
    "list_pronouns",
    "derive_feminine",
    "UnsupportedClitic",
    "UnsupportedDerivation",
    "UnsupportedRoot",
    "UnsupportedVerb",
    "__version__",
]
