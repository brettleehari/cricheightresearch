# Agent Prompt: Update Research Paper

## Instructions
You are updating an academic research paper on cricket anthropometric evolution. Do not ask questions—make reasonable choices based on the CLAUDE.md context and these specific instructions.

## Current Task
Update the paper at `paper/cricket_paper.md` with the following changes:

### 1. Abstract Section
**Problem:** The abstract jumps into statistics too quickly.
**Solution:** Add 2-3 sentences of plain-language context before any numbers.

Structure should be:
1. Plain English: What we studied and why it matters (2 sentences)
2. Plain English: What we found in simple terms (1-2 sentences)  
3. Then: Statistical details (current content)
4. Plain English: Why this matters (1 sentence conclusion)

Example opening:
> "Are elite cricketers getting taller because teams are specifically selecting for height, or simply because the general population is getting taller? This question matters for talent identification and understanding how the sport is evolving."

### 2. Section 1.2 (Literature Review / Background)
**Problem:** Lacks concrete player examples spanning different eras and styles.
**Solution:** Add references to these players as illustrative examples:

| Player | Era | Height | Style | Use For |
|--------|-----|--------|-------|---------|
| Viv Richards | 1970s-80s | 178 cm | Dominant stroke-maker | Classic era baseline |
| Brian Lara | 1990s-2000s | 173 cm | Elegant left-hander | Skill over height |
| Matthew Hayden | 2000s | 193 cm | Power opener | Modern tall batter |
| Kevin Pietersen | 2000s-10s | 193 cm | Aggressive stroke-player | English/South African example |
| Joe Root | 2010s-present | 183 cm | Technical anchor | Current generation |

Weave these naturally into the narrative about height-performance debates, e.g.:
> "The success of relatively compact batsmen like Brian Lara (173 cm) and Sachin Tendulkar (165 cm) alongside taller power hitters like Matthew Hayden (193 cm) and Kevin Pietersen (193 cm) suggests height alone does not determine batting excellence."

### 3. Country-Wise Analysis (New Subsection)
**Location:** Add as Section 4.X in Results
**Content:** Present nation-specific height trends for the 8 primary nations.

Include:
- Mean heights by nation across eras
- Which nations show strongest/weakest temporal trends
- ICC coefficient (variance explained by nation)
- Table: Nation × Era mean heights

### 4. Regional Analysis (New Subsection)
**Location:** Add as Section 4.Y in Results (after country-wise)
**Content:** Group nations into cricket regions and analyze patterns.

Regions:
- **South Asian:** India, Pakistan, Sri Lanka, Bangladesh
- **Oceanian:** Australia, New Zealand  
- **Caribbean:** West Indies
- **European:** England, Ireland
- **African:** South Africa, Zimbabwe

Analysis should include:
- Regional mean heights and temporal slopes
- Whether regional trends differ from global trend
- Discussion of potential confounds (population demographics, playing styles)

### 5. Discussion Updates
Add brief discussion of:
- Nation-specific findings and what they suggest
- Regional patterns and potential explanations
- Caveats about smaller sample sizes when disaggregated

## Style Requirements
- Maintain active voice where possible
- Use past tense for methods and results
- Use present tense for established facts and implications
- Include 95% confidence intervals for all estimates
- Round statistics consistently (2 decimal places for coefficients, 3 for p-values)

## Output
Save the updated paper to `paper/cricket_paper_v2.md`

Do not ask for clarification. Make reasonable choices based on context. Begin immediately.
