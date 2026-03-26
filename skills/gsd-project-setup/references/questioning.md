# Deep Questioning Techniques

## Core Principles

The goal is to extract enough context to write a clear, actionable PROJECT.md. Ask questions that reveal what the user actually needs, not just what they say they want.

## Techniques

### Challenge Vagueness
When users use imprecise language, ask for specifics:
- "When you say 'scalable', what scale? 100 users or 100,000?"
- "What does 'fast' mean here? Sub-100ms API response? Page load under 2s?"
- "You said 'simple' — simple for whom? The developer or the end user?"

### Make Abstract Concrete
Turn concepts into observable behavior:
- "Walk me through what a user would actually do, step by step"
- "If I were watching someone use this, what would I see?"
- "Show me what the output would look like for a real example"

### Surface Assumptions
Identify hidden beliefs driving the design:
- "You mentioned using React — is that decided, or open to alternatives?"
- "Are you assuming users will be technical?"
- "Is there an existing system this needs to integrate with?"

### Find Edges
Explore boundary conditions and failure modes:
- "What happens when the network is down?"
- "What if two users try to edit the same thing?"
- "What's the worst case scenario if this feature breaks?"

### Reveal Motivation
Understand the why behind the what:
- "What problem sparked this project?"
- "Who's asking for this and why?"
- "What would happen if you didn't build this?"

## Context Checklist

Before declaring "ready to create PROJECT.md", mentally verify:

- [ ] Core purpose is clear (what it does, who it's for)
- [ ] Key features are identified (must-have vs nice-to-have)
- [ ] Technical constraints are known (stack, hosting, integrations)
- [ ] User types are defined (who uses it, how)
- [ ] Success criteria exist (how to know it's working)
- [ ] Scope boundaries are set (what it's NOT)
- [ ] Timeline/budget constraints are known (if any)
