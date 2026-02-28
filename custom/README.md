# Custom Skills & Agents

Your project-specific skills and agents go here. This folder is yours — upstream updates won't touch it.

## Structure

```
custom/
├── skills/          # Your custom skills
│   └── my-skill/
│       └── SKILL.md
└── agents/          # Your custom agents
    └── my-agent/
        └── AGENT.md
```

## Adding a Custom Skill

1. Create a folder in `custom/skills/`:

```
custom/skills/deploy-staging/
└── SKILL.md
```

2. Use the standard SKILL.md format:

```markdown
---
name: deploy-staging
description: |
  Staging deployment workflow for our specific infra.
  Recognizes: "deploy to staging", "staging deploy"
---

# Deploy to Staging

Your workflow steps here...
```

3. Copy it into your project:

```
Copy the skill from ~/skill-library/custom/skills/deploy-staging/SKILL.md into my project
```

## Adding a Custom Agent

Same pattern — create a folder in `custom/agents/` with an `AGENT.md`.

## Tips

- Use the **[skill-builder](../skills/meta/skill-builder)** skill to generate well-structured skills
- Use the **[agent-builder](../skills/meta/agent-builder)** skill to generate agents that follow the library's patterns
- Keep project-specific logic here, reusable patterns in a PR to upstream
