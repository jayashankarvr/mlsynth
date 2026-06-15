# References

`mlsynth` implements Malayalam morphological **facts** (case-marker allomorphy,
oblique-stem augments, glide insertion) restated in our own rule engine. **No text,
tables, code, or datasets from any source below are reproduced or redistributed.**
These citations are scholarly credit; they imply no endorsement and create no license
obligation.

Each rule in `mlsynth/rules.py` carries a `provenance` key from this list. Forms are
ratified through a native-reviewer workflow; a rule's `verified` flag is `True` only
after native sign-off.

## Provenance keys

- **`vinod-2012`**: Vinod P. M., Jayan V., Bhadran V. K. *Implementation of Malayalam
  Morphological Analyzer Based on Hybrid Approach.* Proc. ROCLING 2012 (ACL Anthology
  O12-1028). Source of the `am_neuter` (-ം, oblique -ത്ത-) singular paradigm.
- **`krishnan-2021`**: Krishnan G. G., Raghunathan A., Sarma V. M. *Acquisition of
  Malayalam inflections: Complexity of morphosyntactic rules and its impact on
  developing grammars.* First Language. Case inventory and allomorphy for the
  `i_vowel` class.
- **`native-14`**: Native-reviewer ratification (project correctness log, item #14):
  the modern genitive form കുട്ടിയുടെ (over the archaic FST form).
- **`native-2026`**: Native-reviewer worksheet ratification of the മരം and കുട്ടി
  singular/plural paradigms, the differential-object-marking rule (inanimate accusative
  defaults bare), and the synthetic/analytic instrumental register.
- **`smc-morph`**: SMC's Malayalam morphology documentation, covering nominal inflection rules
  (https://morph.smc.org.in/ninfl/cases.html) and the mlmorph tagset
  (https://gitlab.com/smc/mlmorph). Used for cases pending native sign-off
  (ablative, allative, perlative, vocative). Rules restated as facts, no data copied.

## Additional background consulted (facts only)

- Gayathri G. Krishnan. *Malayalam Morphosyntax: Inflectional Features and their
  Acquisition.* PhD thesis, IIT Bombay, 2019.
- Premjith B., Soman K. P. *Deep Learning Approach for the Morphological Synthesis in
  Malayalam and Tamil at the Character Level.* ACM TALLIP 20(6), 2021. (Framing of
  synthesis as morpheme-boundary transformation.)
- Kunjamma S. *Lexical and Grammatical Meaning in Malayalam.* Language in India, 2019.
  (Case-role semantics; positive/negative verb opposition.)
