# Ralph Loop — DIY Autonomous Work Loops for Claude Code

Lightweight alternative to the broken `ralph-wiggum` plugin. Uses a Stop hook + skill file — no plugin infrastructure needed.

## How It Works

1. User types `/ralph-loop Fix all the bugs`
2. Skill instructs Claude to create a state file and start working
3. When Claude tries to stop, the Stop hook checks: done yet?
4. Not done → blocks exit, re-feeds the original prompt
5. Done (`<promise>COMPLETE</promise>` detected) or max iterations → allows exit

## Installation

### 1. Copy hook script

```bash
mkdir -p .claude/hooks
cp hooks/ralph-loop-stop.sh .claude/hooks/
chmod +x .claude/hooks/ralph-loop-stop.sh
```

### 2. Add hook to settings

Add to `.claude/settings.local.json` (or `.claude/settings.json`):

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/ralph-loop-stop.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

If the file already has content, merge the `hooks` key alongside existing keys.

### 3. Copy skill

```bash
cp -r . .claude/skills/ralph-loop/
# (or just copy SKILL.md into your skills directory)
```

### 4. Restart Claude Code

Hooks are loaded at session start. Restart to pick up the new Stop hook.

## Usage

```
/ralph-loop Implement feature X with tests
/ralph-loop max=20 Fix all linting errors
```

## Cancel

- Delete `.claude/ralph-loop.local.md`
- Or press Escape / Ctrl+C

## Dependencies

- `jq` (for JSON output in the stop hook)

## Files

```
ralph-loop/
├── SKILL.md                    # Skill file (copy to .claude/skills/ralph-loop/)
├── hooks/
│   └── ralph-loop-stop.sh      # Stop hook (copy to .claude/hooks/)
└── README.md                   # This file
```
