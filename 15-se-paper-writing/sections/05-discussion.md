# Section 5: Discussion

[← Back to Main](../SKILL.md) | [← Evaluation](04-evaluation.md)

This section consolidates post-evaluation interpretation. It must include
**Threats to Validity**, and may include **Limitations** and
**Lessons Learned** depending on paper type.

## Section Policy by Paper Type

- **All paper types**: include `Threats to Validity`.
- **Prototype/technique/tool papers**: include `Threats to Validity`; add
  `Limitations` if applicable; lessons learned are usually unnecessary.
- **Empirical studies**: include `Threats to Validity`; optionally add a
  brief `Lessons Learned` subsection when it contributes practical
  insights beyond RQ answers.

## Recommended Structure

```latex
\section{Discussion}
\label{sec:discussion}

\subsection{Threats to Validity}

\textbf{Internal Validity.}
% Confounding factors that might affect results
...

\textbf{External Validity.}
% Generalizability concerns
...

\textbf{Construct Validity.}
% Are metrics measuring what we claim?
...

\textbf{Conclusion Validity.}
% Statistical validity
...

% Optional for prototype/technique/tool papers
\subsection{Limitations}
...

% Optional, mainly for empirical studies
\subsection{Lessons Learned}
...
```

## Threats to Validity (Required)

Use the four standard validity types.

### Internal Validity

**Question**: Could confounding factors have affected the results?

Common threats:
- Implementation bugs in your system
- Bugs or mismatch in baseline implementations
- Data collection/labeling errors
- Experimenter bias in manual judgments

### External Validity

**Question**: Do results generalize beyond this study?

Common threats:
- Single language/ecosystem
- Single benchmark or narrow domains
- Limited scale or time window

### Construct Validity

**Question**: Are metrics measuring what you claim?

Common threats:
- Exact-match metrics penalize alternative correct outputs
- Benchmarks may contain imperfect ground truth
- Automated metrics may not fully capture developer utility

### Conclusion Validity

**Question**: Are statistical conclusions valid?

Common threats:
- Small sample sizes
- Test assumptions and repeated-measure concerns
- Random variation without confidence intervals/effect sizes

## Limitations (Recommended for Prototype Papers)

Keep this short and concrete (2-5 sentences). Focus on current scope
boundaries, not fixable engineering TODOs.

Good examples:
- Architectural paradigm shifts requiring large program restructuring
- Missing support for cross-language or multi-repo migration workflows
- Dependence on availability/quality of external documentation

## Lessons Learned (Optional, Mainly Empirical)

Include only if it adds insight that does not duplicate evaluation RQs. Always refer to the Existing sections or subsections for proofs.

Good use cases:
- Design implications derived from large-scale observational data
- Transferable practices for future dataset/tool builders

Avoid:
- Restating numeric results already covered in RQ summaries
- Generic claims without actionable implications

## Length Guidelines

- Total: 0.5-1 page typical
- `Threats to Validity`: 70-90% of this section
- `Limitations` / `Lessons Learned`: concise and selective

## Common Mistakes

1. Treating threats as optional.
2. Moving all limitations into evaluation instead of discussion.
3. Adding lessons learned to prototype papers without clear value.
4. Listing generic threats without mitigation or context.

## Checklist

- [ ] Section is named `Discussion`
- [ ] Threats must have some mitigation strategies.
- [ ] Includes `Threats to Validity` subsection
- [ ] Covers internal, external, construct, and conclusion validity
- [ ] Threats are study-specific and include mitigations/acknowledgments
- [ ] `Limitations` included when applicable
- [ ] `Lessons Learned` included only when warranted (mainly empirical)

[← Evaluation](04-evaluation.md) | [Next: Related Work →](06-related-work.md)
