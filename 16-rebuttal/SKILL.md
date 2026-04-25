---
name: paper-rebuttal
description: Use when drafting, shortening, or revising academic paper rebuttals to reviewers, especially for conference/journal reviews with tight word limits, mixed praise/concerns, methodology challenges, novelty disputes, or requests for clearer positioning.
---

# Paper Rebuttal

Use this skill for academic review responses and rebuttal files such as `rebuttal.md`.

## Goal

Write responses that are:

- short,
- directly responsive to the reviewer’s actual question,
- careful about claims,
- and aligned with the evidence already available in the paper, artifact, or local files.

## Workflow

1. Identify the reviewer’s real concern.
   Common categories:
   - novelty or “not surprising”
   - unclear definition or measurement
   - missing related work
   - sampling or scope justification
   - evaluation weakness
   - artifact / anonymity / reproducibility
   - practical impact or security risk

2. Choose the response posture.
   Use one of these:
   - concede and narrow the claim
   - clarify the definition or scope
   - distinguish setting / unit of analysis / contribution
   - point to existing validation
   - admit limitation and say it will be clarified in revision

3. Draft the shortest response that actually answers the question.
   Good default structure:
   - acknowledge the point
   - answer it directly
   - say what will be clarified or toned down in revision

4. If editing a rebuttal file, keep the existing format unless the user asks to change it.
   For explicit reviewer questions, use a heading like `Q: ...` only when it improves scanability.

## Rebuttal Template

Use this structure when creating a fresh `rebuttal.md` or when normalizing a messy draft:

```md
# For Reviewer-A

*****Issue heading*****
Short direct response.

*****Q: Explicit reviewer question*****
Short direct response.

# For Reviewer-B

*****Issue heading*****
Short direct response.

# For Reviewer-C

*****Q: Explicit reviewer question*****
Short direct response.

[1] Standard reference if needed.
[2] Standard reference if needed.
```

Follow these template rules:

- Use one short block per issue.
- Keep reviewer grouping explicit.
- Use `Q:` only for explicit questions for authors' response.
- Keep headings short and concrete.
- Put references at the end only if the rebuttal text cites them.
- Do not turn every comment into a long paragraph; default to 2-4 sentences.

Good heading examples:

- `*****How CER is computed*****`
- `*****Sample selection rationale*****`
- `*****Q: Clarifying the lag definition*****`
- `*****Artifact anonymity*****`

## Default Rules

- Do not defend weak claims just because they are in the paper.
- If the reviewer is right, say so briefly and narrow the claim.
- Do not introduce extra methodology, pipelines, or metrics unless they help the exact question.
- Do not promise new experiments, tests, or statistics unless they already exist or can be produced now.
- Do not cite papers that do not actually support the point.
- Distinguish:
  - what the metric measures,
  - what it does not measure,
  - and what limitation follows from that.
- Prefer “dataset-specific” over “generalizable” unless strong support exists.
- Prefer “conservative lower bound” over overclaiming completeness.
- For artifact/anonymity issues, avoid absolute claims like “anonymity is assured.”
- For practitioner-evaluation concerns, do not argue that the authors count as practitioners; distinguish precision validation from practitioner validation.

## Useful Response Patterns

### When the reviewer says a finding is not novel

- Do not argue the high-level lesson is new.
- Reframe the value as:
  - implication in this setting,
  - large-scale evidence,
  - finer granularity,
  - or operationalization.

Good move:
- “We agree that this is not new as general OSS advice; our contribution is to quantify/operationalize it in the fork-synchronization setting.”

### When the reviewer says two findings overlap

- Agree and merge them conceptually.
- Emphasize the implication, not the duplicated observation.

### When the reviewer questions a metric

- State exactly how it is computed.
- Confirm the limitation if correct.
- Say whether it should be read as:
  - PR exposure,
  - conservative lower bound,
  - history-visible propagation,
  - etc.

### When the reviewer questions sample selection

- State what population the sample is meant to represent.
- Explain why that criterion is observable and reproducible.
- If the reviewer proposes a criterion only knowable after crawling the data, say so.

### When the reviewer asks about asymmetry

- Explain that the mechanisms differ by direction.
- Say why the same metric is meaningful in one direction but not the other.

### When the reviewer points to related work

- Admit the omission.
- Distinguish scope, ecosystem, unit of analysis, and added insight.
- Do not over-acknowledge overlap if the paper still has a clear edge.

## Style

- Prefer short paragraphs over long ones.
- Remove throat-clearing.
- Avoid speculative future-work language unless needed.
- Keep wording factual and plain.
- If the user asks for more compression, shorten the longest responses first.

## Editing a Rebuttal File

When patching a rebuttal file:

- preserve reviewer grouping,
- keep one response per issue,
- shorten conservatively,
- and check for mismatches between the reviewer’s actual question and the drafted answer.

Prioritize these failure modes:

- answering a nearby question instead of the exact one,
- using the wrong citation,
- overstating novelty,
- introducing a new attack surface,
- or claiming broader evidence than you have.
