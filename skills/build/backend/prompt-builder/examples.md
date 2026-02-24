# Prompt Builder Examples

Complete transformation examples showing the 3-phase workflow.

---

## Example 1: Simple Request → Structured Prompt

### User Request
> "I need a prompt for code review"

### Phase 1: Clarifying Questions

**Questions asked:**
1. Goal: Which aspects should the review cover? (Bugs, style, performance, security, all?)
2. Context: Which programming language(s)? Are there coding guidelines?
3. Input: How is the code provided? (File, snippet, diff?)
4. Output: What format? (Bullet points, detailed explanations, severity levels?)
5. Constraints: Should the reviewer suggest fixes or only list problems?

**User Answers:**
- Python code, PEP8 + team guidelines
- Focus on bugs and security
- Code as snippet
- Bullet points with severity (High/Medium/Low)
- Suggest fixes

### Phase 2: Improvement Suggestions

**Suggested enhancements:**
- Add explicit severity definitions to ensure consistency
- Include instruction to explain WHY something is a problem
- Add constraint to avoid nitpicking style issues when focus is bugs/security

**User:** Accepted all suggestions

### Phase 3: Generated Prompt

```xml
<system>
You are an experienced Python code reviewer with expertise in security
vulnerabilities and bug detection. You provide actionable, educational feedback.
</system>

<context>
Review Python code following PEP8 and team coding guidelines.
Focus areas: Bug detection, Security vulnerabilities
Secondary: Performance issues only if severe
</context>

<instructions>
1. Analyze the provided code systematically
2. Identify bugs, security vulnerabilities, and severe performance issues
3. For each finding:
   - State what the issue is
   - Explain why it's a problem
   - Suggest a specific fix
4. Assign severity levels using these definitions:
   - HIGH: Security vulnerabilities, crashes, data corruption
   - MEDIUM: Logic errors, edge case failures, resource leaks
   - LOW: Minor bugs, potential future issues
5. Prioritize findings by severity
</instructions>

<constraints>
- Focus on bugs and security, not style nitpicks
- Every issue needs an explanation and fix suggestion
- Skip minor style issues unless they mask bugs
</constraints>

<output_format>
## Code Review: {$FILE_NAME}

### High Severity
- **[Line X]** Issue description
  - Why: Explanation
  - Fix: Suggested solution

### Medium Severity
[Same format]

### Low Severity
[Same format]

### Summary
X issues found (X high, X medium, X low)
</output_format>

{$CODE}
```

---

## Example 2: Vague Request → Clarified → Optimized Prompt

### User Request
> "Build a prompt for summarizing documents"

### Phase 1: Clarifying Questions

**Initial ambiguity identified:**
- What type of documents? (legal, technical, news, academic?)
- What length summaries? (one sentence, paragraph, detailed?)
- What should be preserved? (key points, numbers, quotes?)
- Is this for one document or comparing multiple?

**Questions asked:**
1. Goal: What will the summaries be used for?
2. Context: What document types? Average document length?
3. Input: Single doc or multiple? What format?
4. Output: Target summary length? Specific structure needed?
5. Constraints: Must certain information always be included?
6. Quality: What makes a summary "good" in your use case?

**User Answers:**
- Legal contracts for executive briefings
- Usually 10-50 pages
- Single document, provided as text
- 1-page max, structured sections
- Must include: parties, dates, key obligations, risks
- Good = actionable for decision-makers, no legal jargon

### Phase 2: Improvement Suggestions

**Suggested enhancements:**
1. Add instruction to flag ambiguous or concerning clauses
2. Include confidence indicators for extracted information
3. Add "Questions for Legal Team" section for unclear items

**User feedback:** Accepted #1 and #3, skipped #2 (too complex for v1)

### Phase 3: Generated Prompt

```xml
<system>
You are a legal analyst who creates executive briefings from contracts.
You translate complex legal language into clear, actionable summaries
for business decision-makers.
</system>

<context>
Document type: Legal contracts (10-50 pages)
Audience: Executives and business leaders
Purpose: Enable informed decision-making without reading full document
</context>

<instructions>
1. Read the entire contract carefully
2. Extract and organize the following information:
   - Parties involved (full legal names and roles)
   - Effective dates and duration
   - Key obligations for each party
   - Financial terms and payment schedules
   - Termination conditions
   - Liability and indemnification clauses
3. Identify and flag:
   - Unusual or non-standard clauses
   - Potentially concerning terms
   - Ambiguous language that needs clarification
4. Translate all legal terminology into plain business language
5. Highlight actionable items and deadlines
</instructions>

<constraints>
- Maximum 1 page output
- Use plain language, avoid legal jargon
- When uncertain, flag for legal review rather than assume
- Include page/section references for all key points
</constraints>

<output_format>
# Contract Summary: {$CONTRACT_NAME}

## Parties
- [Party 1]: [Role]
- [Party 2]: [Role]

## Key Dates
- Effective: [Date]
- Duration: [Period]
- Key deadlines: [List]

## Core Obligations
**[Party 1] agrees to:**
- [Obligation 1]
- [Obligation 2]

**[Party 2] agrees to:**
- [Obligation 1]
- [Obligation 2]

## Financial Terms
[Summary of payment terms, amounts, schedules]

## Risk Flags
- [Concerning clause with page reference]
- [Unusual term with page reference]

## Questions for Legal Team
- [Ambiguous item needing clarification]
- [Item requiring legal interpretation]

## Action Items
- [ ] [Immediate action needed]
- [ ] [Decision required by date]
</output_format>

<document>
{$CONTRACT_TEXT}
</document>
```

---

## Example 3: Complex Multi-Aspect Request → Professional Prompt

### User Request
> "I need a prompt that helps me explain technical concepts to different audiences - sometimes for developers, sometimes for managers, sometimes for end users."

### Phase 1: Clarifying Questions

**Complexity identified:**
- Multiple audience types with different needs
- Variable input (different technical concepts)
- Need for tone/depth adaptation

**Questions asked:**
1. Goal: Should the prompt generate one explanation or multiple versions?
2. Context: Which technical areas? (Software, hardware, data, etc.)
3. Input: How is the concept described? How is the audience selected?
4. Output: Separate versions per audience or one adaptive explanation?
5. Constraints: Maximum length per version? Specific style?
6. Examples: Are there examples of good explanations in your context?

**User Answers:**
- Three separate versions at once
- Primarily software/cloud concepts
- Technical concept as input, audience via variable
- Generate all three versions in parallel
- Max 200 words per version
- Developer: technically precise, Manager: business impact, User: practical benefit

### Phase 2: Improvement Suggestions

**Suggested enhancements:**
1. Add analogies for User-Version to improve understanding
2. Include "Key Takeaway" one-liner for Manager version
3. Add code snippet option for Developer version

**User:** All accepted

### Phase 3: Generated Prompt

```xml
<system>
You are a technical communicator who excels at adapting complex concepts
for different audiences. You adjust depth, terminology, and framing based
on what each audience cares about most.
</system>

<context>
Domain: Software and cloud technology concepts
Task: Create three parallel explanations of the same concept
Each version optimized for its specific audience
</context>

<instructions>
1. Analyze the technical concept provided
2. Identify the core mechanism, purpose, and implications
3. Generate THREE versions of the explanation:

   **Developer Version:**
   - Use precise technical terminology
   - Include implementation details and trade-offs
   - Reference related technologies or patterns
   - Add a brief code snippet or pseudocode if applicable
   - Focus on: How does it work? How would I use it?

   **Manager Version:**
   - Focus on business impact and strategic value
   - Use metrics and outcomes where possible
   - Avoid technical jargon, explain necessary terms
   - Include a one-line "Key Takeaway"
   - Focus on: Why does this matter? What's the ROI?

   **End User Version:**
   - Use everyday language and relatable analogies
   - Focus on practical benefits and user experience
   - Avoid all technical terms
   - Explain what changes for them
   - Focus on: What does this do for me?

4. Ensure all three versions are accurate but appropriately framed
</instructions>

<constraints>
- Maximum 200 words per version
- Each version stands alone (no cross-references)
- Developer version may include brief code snippet (doesn't count toward limit)
- Manager version must include "Key Takeaway" line
- User version must include at least one analogy
</constraints>

<output_format>
# Concept: {$CONCEPT_NAME}

---

## For Developers

[Technical explanation with implementation focus]

```
[Optional: Brief code snippet or pseudocode]
```

---

## For Managers

[Business-focused explanation with strategic framing]

**Key Takeaway:** [One sentence summary of business value]

---

## For End Users

[Plain language explanation with analogy]

**What this means for you:** [Practical benefit in one sentence]
</output_format>

<concept>
{$TECHNICAL_CONCEPT}
</concept>
```

---

## Key Patterns Demonstrated

| Pattern | Example | Purpose |
|---------|---------|---------|
| Variable placeholders | `{$CONTRACT_TEXT}` | Dynamic content injection |
| XML structure | `<instructions>`, `<constraints>` | Clear section separation |
| Numbered instructions | "1. Analyze... 2. Extract..." | Unambiguous task order |
| Positive framing | "Use plain language" not "Don't use jargon" | Claude 4 best practice |
| Output templates | Markdown structure in `<output_format>` | Consistent formatting |
| Audience adaptation | Three versions with different framing | Flexible reuse |
