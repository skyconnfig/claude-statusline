# Claude Code 状态栏 (Statusline)

> 一个漂亮、信息丰富的 [Claude Code](https://claude.ai/code) CLI 状态栏脚本。
>
> [![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
> [![bash](https://img.shields.io/badge/Shell-000000?style=flat&logo=gnu-bash&logoColor=white)](https://www.gnu.org/software/bash/)
> [![jq](https://img.shields.io/badge/jq-required-green)](https://jqlang.org/)

实时显示 3 行会话信息：

```
Claude 200K v2.1.92 | project (main) | +342 -87 lines | executor | NOR
●●●●●●●●●●○○○○○ 47% | $1.25 | 2m 05s | 5h 35% (2h 30m) | 7d 12% (5d 12h)
cache 37% | in: 202.1K out: 45.0K | api wait 1m 35s (76%) | cur 12.5K in 8.3K read 1.2K write
```

## 功能 & 输出格式

| 格式 | 命令 | 描述 |
|------|------|------|
| **Full** | (默认) | 3 行详细视图，包含所有指标 |
| **Compact** | `--format compact` | 单行紧凑视图，适合窄终端 |
| **ASCII** | `--format ascii` | 纯 ASCII 字符（无 Unicode 圆点）|
| **Bare** | `--format bare` | 纯文本，无颜色或转义序列 |

```
Full 模式:
Claude 200K (main) | +342 -87 lines | executor | NOR
●●●●●●●●●○○○○○○ 47% | $1.25 | 2m 05s | 5h 35% | 7d 12%
cache 37% | in: 202.1K out: 45.0K | api wait 1m 35s (76%)

Compact 模式:
Claude (main) | $1.25 | 2m 05s | 47% | +342 -87 | executor

ASCII 模式:
Claude 200K (main) | +342 -87 lines | executor | NOR
|||||||:::::::: 47% | $1.25 | 2m 05s | 5h 35% | 7d 12%
cache 37% | in: 202.1K out: 45.0K | api wait 1m 35s (76%)
```

### 颜色编码

- **绿色**（< 50%）：健康状态
- **黄色**（50%–80%）：中等——接近上限
- **红色**（> 80%）：偏高——建议压缩上下文

### Git 文件统计

- `3M` — 3 个已修改文件
- `2A` — 2 个新增/未跟踪文件
- `1D` — 1 个已删除文件

### 进度条颜色状态

```
低用量（绿色）:          ●●○○○○○○○○○○○○○ 15%
中等用量（黄色）:        ●●●●●●●○○○○○○○● 47%
高用量（红色）:          ●●●●●●●●●●●●●●● 92%
```

## 快速安装

```bash
curl -fsSL https://raw.githubusercontent.com/skyconnfig/claude-statusline/main/statusline.sh \
  -o ~/.claude/scripts/statusline.sh && \
mkdir -p ~/.claude/scripts && \
bash ~/.claude/scripts/statusline.sh --init
```

重启 Claude Code 即可！

## 手动安装

### 第一步：下载

```bash
git clone https://github.com/skyconnfig/claude-statusline.git
```

或直接复制 `statusline.sh` 到你喜欢的位置：

```bash
mkdir -p ~/.claude/scripts
cp statusline.sh ~/.claude/scripts/
```

Linux/macOS 赋予执行权限：

```bash
chmod +x ~/.claude/scripts/statusline.sh
```

### 第二步：配置

**自动配置（推荐）：**

```bash
bash statusline.sh --init
```

**手动配置：** 编辑 `~/.claude/settings.json`：

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/scripts/statusline.sh"
  }
}
```

**Windows（Git Bash）：**

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash /c/Users/你的用户名/.claude/scripts/statusline.sh"
  }
}
```

### 第三步：重启 Claude Code

重启会话后，状态栏会出现在终端底部。

## 工作原理

Claude Code 通过 stdin 传入 JSON 格式的会话元数据。脚本使用 `jq` 解析，加上 ANSI 颜色后输出 3 行。

```
Claude Code ──JSON──> statusline.sh ──ANSI 文本──> 终端状态栏
```

## 前置要求

- `bash`（Windows 使用 Git Bash）
- `jq` — JSON 解析器（Windows: `choco install jq`）
- `git` — 用于分支和文件统计
- `awk` — 用于 Token 格式化（大多数系统自带）

## 配置

### 使用不同的 Shell 路径

```json
{
  "statusLine": {
    "type": "command",
    "command": "/usr/bin/bash /path/to/statusline.sh"
  }
}
```

### 禁用状态栏

从 `settings.json` 中删除 `statusLine` 键，或设置：

```json
{
  "disableAllHooks": true
}
```

## 常见问题

### 状态栏不显示

1. 确认 `jq` 已安装：`which jq`
2. 手动测试脚本：
   ```bash
   echo '{"model":{"display_name":"测试"},"workspace":{"current_dir":"/tmp"},"cost":{"total_cost_usd":0,"total_duration_ms":0},"context_window":{"used_percentage":10}}' | bash statusline.sh
   ```
3. 检查 `settings.json` 的 JSON 语法是否正确

### 颜色不显示

确保终端支持 ANSI 转义序列，且 `TERM` 不是 `dumb`。尝试 `--format bare` 获取纯文本。

### 5h/7d 速率限制不显示

这些字段仅在 Claude Code 提供速率限制数据时出现，通常在接近使用上限时才会显示。

## JSON 输入格式

完整的数据结构如下：

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

## 许可

MIT

---

Made by [skyconnfig](https://github.com/skyconnfig)
