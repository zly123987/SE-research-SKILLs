# Section 7: Conclusion

[← Back to Main](../SKILL.md) | [← Related Work](06-related-work.md)

The conclusion summarizes your contributions and points to future work. Keep it concise.

## Structure

```latex
\section{Conclusion}
\label{sec:conclusion}

% Summary paragraph (what you did)
...

% Results paragraph (what you found)
...

% Future work paragraph (what's next)
...
```

## Content Guidelines

### Summary Paragraph

Briefly restate the problem and your solution (2-3 sentences):

```latex
Dependency conflicts remain a significant challenge in Python development,
causing installation failures and wasting developer time. We presented
\tool{}, a hybrid approach combining static pattern matching, dynamic
pip validation, and LLM semantic analysis to detect and resolve conflicts
comprehensively.
```

### Results Paragraph

Highlight key findings (2-3 sentences):

```latex
Our evaluation on 50 real-world Python projects shows that \tool{}
achieves 80\% detection rate---14 percentage points higher than
state-of-the-art---while maintaining 100\% installation success rate
for generated repairs. The hierarchical design reduces LLM API costs
by 5$\times$ compared to LLM-only approaches.
```

### Future Work Paragraph

Identify concrete directions (1-2 items):

```latex
Future work includes extending \tool{} to handle optional dependencies
(\texttt{extras\_require}), which account for 8\% of our failures, and
supporting additional languages such as JavaScript (npm) and Java (Maven).
We also plan to conduct user studies to evaluate developer experience
with \tool{}'s repair suggestions.
```

### Data Availability
Just add the data availability section after conclusion with this new section:
```\section*{Data Availability} Our artifact and dataset can be accessed from \url{}~\cite{}.```

## Length Guidelines

- Total: 0.3 pages
- Summary: 1-2 sentences
- Results: 1-2 sentences
- Future work: 1 sentences


## What NOT to Include

- Don't introduce new information or results
- Don't repeat the abstract verbatim
- Don't discuss limitations (that's in Threats)
- Don't overclaim beyond what evaluation showed

## Common Mistakes

### 1. Too Long
Conclusion should be concise. If over 0.5 pages, trim.

### 2. New Results
Don't introduce findings not in the evaluation section.

### 3. Vague Future Work
**Bad**: "Future work includes further improvements."
**Good**: "Future work includes extending to optional dependencies (8% of failures)."

### 4. Missing Tool URL
If your tool is publicly available, mention it in the conclusion.

## Checklist

- [ ] Summary restates problem and solution (2-3 sentences)
- [ ] Results highlights key findings with numbers (2-3 sentences)
- [ ] Future work is concrete (specific directions, not vague)
- [ ] Tool availability URL included (if applicable)
- [ ] No new information introduced
- [ ] Length is ~0.5 pages
- [ ] Matches claims in introduction

[← Related Work](06-related-work.md) | [Next: Final Check →](08-final-check.md)
