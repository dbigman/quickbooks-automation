---
inclusion: fileMatch
fileMatchPattern: ['**/*.*']
---

# AI Collaboration & Prompting

1. **Clarity is Key:** Provide clear, specific, and unambiguous instructions to the AI. Define the desired outcome, constraints, and context.
2. **Context Referencing:** If a task spans multiple interactions, explicitly remind the AI of relevant previous context, decisions, or code snippets.
3. **Suggest vs. Apply:** Clearly state whether the AI should *suggest* a change for human review or *apply* a change directly (use only when high confidence and task is well-defined). Use prefixes like "Suggestion:" or "Applying fix:."
4. **Question AI Output:** Critically review AI-generated code. Verify logic and don’t blindly trust confident-sounding but potentially incorrect suggestions.
5. **Focus the AI:** Guide the AI to specific, focused parts of the task. Avoid overly broad requests.
6. **Leverage Strengths:** Use the AI for boilerplate generation, refactoring specific patterns, syntax checks, and test case generation, while maintaining human oversight for complex logic.
7. **Incremental Interaction:** Break down complex tasks into smaller steps. Review and confirm each step before proceeding.
8. **Standard Check-in:** Before significant code suggestions, confirm understanding by summarizing context, goals, and planned steps.
9. **Domain-Specific Guides:** For QuickBooks qbXML code generation, **ALWAYS** reference and follow `QuickBooks_Desktop_qbXML_ Report_Query_Guide.md` to ensure SDK compatibility.
