# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jayashankar R
"""A permissive, rule-based Malayalam morphological synthesizer.

Forward morphological generation (root + features -> inflected surface form),
starting with noun inflection. Rules are declarative and provenance-tagged; see
REFERENCES.md for the linguistic sources and the project's native-ratification
workflow.
"""
from .nouns import UnsupportedRoot, list_supported_classes, synthesize_noun
from .pronouns import is_pronoun, list_pronouns
from .types import Animacy, Case, Gender, NounFeatures, Number, Register, SynthResult

__version__ = "0.0.2"
__all__ = [
    "Animacy",
    "Case",
    "Gender",
    "Number",
    "NounFeatures",
    "Register",
    "SynthResult",
    "synthesize_noun",
    "list_supported_classes",
    "is_pronoun",
    "list_pronouns",
    "UnsupportedRoot",
    "__version__",
]
