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

## Creating Custom Skills & Agents

The fastest way to create well-structured skills and agents is with the meta skills from this library:

```
Use the skill-builder skill to create a custom skill for [your use case]
```

```
Use the agent-builder skill to create a custom agent for [your use case]
```

These generate skills/agents that follow the library's conventions automatically. See [skill-builder](../skills/meta/skill-builder) and [agent-builder](../skills/meta/agent-builder) for details.

## Manual Setup

### Adding a Skill

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

### Adding an Agent

Same pattern — create a folder in `custom/agents/` with an `AGENT.md`.

## Tips

- Keep project-specific logic here, reusable patterns in a PR to upstream
