# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jayashankar R
"""Gender derivation: build a feminine stem from a masculine one (pre-inflection).

Malayalam marks gender on animate nouns only, and a feminine noun is *derived* from its
masculine base before any pluralization or case inflection. Two ratified patterns:
  * a masculine ending in the chillu -ൻ takes -ഇ (എഴുത്തുകാരൻ -> എഴുത്തുകാരി);
  * a masculine ending in -ഇ takes -ഇനി (വിദ്യാർത്ഥി -> വിദ്യാർത്ഥിനി).

``derive_feminine`` returns a plain root string, ready to feed back into
``synthesize_noun``. It is deliberately a separate step: derivation is lexical (it builds
a new lemma), inflection is grammatical. A base that fits neither pattern raises rather
than guess.
"""
from __future__ import annotations


class UnsupportedDerivation(ValueError):
    """The masculine base fits no known feminine-derivation pattern."""


def derive_feminine(masculine: str) -> str:
    """Derive the feminine lemma from a masculine animate base.

    ``-ൻ`` -> ``-ഇ`` (എഴുത്തുകാരൻ -> എഴുത്തുകാരി); ``-ഇ`` -> ``-ഇനി``
    (വിദ്യാർത്ഥി -> വിദ്യാർത്ഥിനി). The caller is responsible for passing a genuinely
    animate masculine noun; an unrecognised ending raises :class:`UnsupportedDerivation`.
    """
    if masculine.endswith("ൻ"):
        stem = masculine[:-1]            # drop the chillu; the bare consonant takes -ഇ
        if stem and "ക" <= stem[-1] <= "ഺ":
            return stem + "ി"
    elif masculine.endswith("ി"):
        if len(masculine) > 1 and "ക" <= masculine[-2] <= "ഺ":  # -ഇ on a real consonant
            return masculine + "നി"      # -ഇ -> -ഇനി
    raise UnsupportedDerivation(
        f"cannot derive a feminine form from {masculine!r}; expected a masculine base "
        f"ending in -ൻ (-> -ഇ) or -ഇ (-> -ഇനി)"
    )
