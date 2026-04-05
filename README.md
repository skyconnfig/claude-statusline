# Claude Code Statusline

A beautiful, information-rich statusline script for [Claude Code](https://claude.ai/code) CLI.

Displays 3 lines of real-time session information:

```
Claude 200K v2.1.92 | project (main) | +342 -87 lines | 3A | executor | NOR
●●●●●●●●●●●●●●● 47% | $1.25 | 2m 05s | 5h 35% (2h 30m) | 7d 12% (5d 12h)
cache 37% | in: 202.1K out: 45.0K | api wait 1m 35s (76%) | cur 12.5K in 8.3K read 1.2K write
```

## Features

| Line | Content |
|------|---------|
| **Line 1** | Model name, context window size, version, repo name, git branch, lines added/removed, git file stats (Modified/Added/Deleted), active agent, vim mode |
| **Line 2** | Context usage progress bar (color-coded), session cost, duration, 5-hour & 7-day rate limit usage with countdown timers |
| **Line 3** | Cache hit rate, total input/output tokens, API wait time, current request token detail (input, cache read, cache write) |

### Color Coding

- **Green** (< 50%): Healthy usage
- **Yellow** (50%–80%): Moderate usage — getting close
- **Red** (> 80%): High usage — consider compacting

### Git Stats

- `3M` — 3 modified files
- `2A` — 2 added/untracked files
- `1D` — 1 deleted file

## Prerequisites

- `bash` (Git Bash on Windows)
- `jq` — JSON parser (`choco install jq` on Windows)
- `git` — for branch and file stats
- `awk` — for token formatting (included in most systems)

## Installation

### Step 1: Download the script

```bash
git clone https://github.com/skyconnfig/claude-statusline.git
```

Or simply copy `statusline.sh` to your preferred location, e.g.:

```bash
mkdir -p ~/.claude/scripts
cp statusline.sh ~/.claude/scripts/
```

Make it executable (Linux/macOS):

```bash
chmod +x ~/.claude/scripts/statusline.sh
```

### Step 2: Configure Claude Code

Edit your Claude Code `settings.json` (`~/.claude/settings.json`):

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/scripts/statusline.sh"
  }
}
```

**Windows (Git Bash):**

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash /c/Users/YourName/.claude/scripts/statusline.sh"
  }
}
```

### Step 3: Restart Claude Code

The statusline will appear at the bottom of the terminal after restarting the session.

## Screenshot

Below is an example of what the statusline looks like in action:

```
Line 1 ──────────────────────────────────────────────────────────────
Claude 200K v2.1.92 | claude-statusline (main) | +342 -87 lines | 3A | executor | NOR

Line 2 ──────────────────────────────────────────────────────────────
●●●●●●●●●●●●●●● 47% | $1.25 | 2m 05s | 5h 35% (2h 30m) | 7d 12% (5d 12h)
[Green dots = healthy       ]

Line 3 ──────────────────────────────────────────────────────────────
cache 37% | in: 202.1K out: 45.0K | api wait 1m 35s (76%) | cur 12.5K in 8.3K read 1.2K write
```

### Context Bar Progressions

```
Low usage (green):          ●●○○○○○○○○○○○○● 15%
Moderate usage (yellow):    ●●●●●●●○○○○○○○● 47%
High usage (red):           ●●●●●●●●●●●●●●● 92%
```

## How It Works

Claude Code passes session metadata as JSON on stdin. The script parses it with `jq`, formats it with ANSI colors, and outputs 3 lines.

```
Claude Code ──JSON──> statusline.sh ──ANSI text──> Terminal status bar
```

The JSON input includes:

- `model.display_name` — Model name
- `workspace.current_dir` — Current working directory
- `cost.total_cost_usd` — Accumulated cost
- `context_window.used_percentage` — Context window usage
- `rate_limits.five_hour.*` / `rate_limits.seven_day.*` — Rate limit info
- `context_window.total_input_tokens` — Total token counts
- And more...

## Configuration

### Using a different shell path

If `bash` is not in your `PATH`, use the full path:

```json
{
  "statusLine": {
    "type": "command",
    "command": "/usr/bin/bash /path/to/statusline.sh"
  }
}
```

### Disabling the statusline

Remove the `statusLine` key from `settings.json`, or set:

```json
{
  "disableAllHooks": true
}
```

## Troubleshooting

### Statusline not showing

1. Verify `jq` is installed: `which jq`
2. Test the script manually:
   ```bash
   echo '{"model":{"display_name":"Test"},"workspace":{"current_dir":"/tmp"},"cost":{"total_cost_usd":0,"total_duration_ms":0},"context_window":{"used_percentage":10}}' | bash statusline.sh
   ```
3. Check `settings.json` for valid JSON syntax

### `bc: command not found`

This script uses `awk` instead of `bc` for token formatting. If you see `bc` errors, your version may be outdated — pull the latest.

### Colors not rendering

Ensure your terminal supports ANSI escape sequences and is not set to `TERM=dumb`.

### Rate limits / 5h / 7d not showing

These fields are only present when rate limit data is provided by Claude Code. They appear when you are approaching your usage limits.

## JSON Schema

The full JSON schema received from Claude Code on stdin:

```json
{
  "model": { "display_name": "Claude" },
  "workspace": { "current_dir": "/path/to/project" },
  "cost": {
    "total_cost_usd": 1.25,
    "total_duration_ms": 125000,
    "total_api_duration_ms": 95000,
    "total_lines_added": 342,
    "total_lines_removed": 87
  },
  "context_window": {
    "used_percentage": 47,
    "context_window_size": 200000,
    "total_input_tokens": 202100,
    "total_output_tokens": 45000,
    "current_usage": {
      "input_tokens": 12500,
      "cache_read_input_tokens": 8300,
      "cache_creation_input_tokens": 1200
    }
  },
  "rate_limits": {
    "five_hour": { "used_percentage": 35, "resets_at": 1743915600 },
    "seven_day": { "used_percentage": 12, "resets_at": 1744174800 }
  },
  "version": "2.1.92",
  "vim": { "mode": "NORMAL" },
  "agent": { "name": "executor" }
}
```

## License

MIT

---

Made by [skyconnfig](https://github.com/skyconnfig)
