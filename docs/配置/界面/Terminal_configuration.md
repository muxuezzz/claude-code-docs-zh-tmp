> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 为 Claude Code 配置您的终端

> 修复 Shift+Enter 以插入新行、在 Claude 完成时获得终端铃声、配置 tmux、匹配颜色主题，以及在 Claude Code CLI 中启用 Vim 模式。

Claude Code 可以在任何终端中工作，无需配置。此页面适用于某些特定功能的行为不符合您预期的情况。在下方找到您的症状。如果一切都已按预期工作，您不需要此页面。

* [Shift+Enter 提交而不是插入新行](#enter-multiline-prompts)
* [macOS 上的 Option 键快捷键无效](#enable-option-key-shortcuts-on-macos)
* [Claude 完成时没有声音或警报](#get-a-terminal-bell-or-notification)
* [您在 tmux 内运行 Claude Code](#configure-tmux)
* [Windows 上的退格键删除整个单词](#fix-backspace-deleting-a-whole-word-on-windows)
* [显示闪烁或滚动条跳跃](#switch-to-fullscreen-rendering)
* [您想在提示符中使用 Vim 快捷键](#edit-prompts-with-vim-keybindings)

此页面是关于让您的终端向 Claude Code 发送正确的信号。要更改 Claude Code 本身响应的快捷键，请参阅 [快捷键](/docs/zh-CN/keybindings) 代替。

<h2 id="enter-multiline-prompts">
  输入多行提示
</h2>

按 Enter 键提交您的消息。要添加换行符而不提交，请按 Ctrl+J，或输入 `\` 然后按 Enter。两种方法在每个终端中都可以工作，无需任何设置。

在大多数终端中，您也可以按 Shift+Enter，但支持因终端模拟器而异：

| 终端 | Shift+Enter 换行 |
| :- | :- |
| Ghostty、Kitty、iTerm2、WezTerm、Warp、Apple Terminal、Windows Terminal | 无需设置即可工作 |
| 支持 kitty 键盘协议的其他终端，例如 foot 和 Alacritty 0.16 或更高版本 | 无需设置即可工作。需要 Claude Code v2.1.269 或更高版本 |
| VS Code、Cursor、Devin Desktop、Alacritty 0.16 之前版本、Zed | 运行一次 `/terminal-setup` |
| gnome-terminal、JetBrains IDE（如 PyCharm 和 Android Studio） | 不可用；使用 Ctrl+J 或 `\` 然后 Enter |

对于 VS Code、Cursor、Devin Desktop、Alacritty 0.16 之前版本和 Zed，`/terminal-setup` 会将 Shift+Enter 快捷键写入终端的配置文件。在第一次运行时，您会看到确认消息，例如 `Installed VSCode terminal Shift+Enter key binding`。现有绑定保持不变；如果您看到类似 `VSCode terminal Shift+Enter key binding already configured` 的消息，则未进行任何更改。在主机终端中直接运行 `/terminal-setup`，而不是在 tmux 或 screen 内运行，因为它需要写入主机终端的配置。

在 VS Code、Cursor 和 Devin Desktop 中，`/terminal-setup` 还会更新两个编辑器设置：它将 `terminal.integrated.gpuAcceleration` 设置为 `"off"` 以防止集成终端中的文本乱码，并设置 `terminal.integrated.mouseWheelScrollSensitivity` 以在[全屏模式](/docs/zh-CN/fullscreen)中实现更平滑的滚动。要撤销 GPU 加速更改，请将其设置回 `"auto"` 并重新加载编辑器窗口。

在 Zed 中，`/terminal-setup` 会就地更新您的 `keymap.json`：

* 如果 keymap 已有绑定且其中没有 Terminal `shift-enter`，Claude Code 首先会将其备份到同一目录中的副本，例如 `keymap.json.1a2b3c4d.bak`，然后将 Shift+Enter 绑定合并到您的 keymap 中，保留您的其他快捷键和注释
* 如果 Claude Code 无法读取或解析 keymap、无法备份或无法验证合并结果，它会[保持文件不变并打印快捷键块供您自己添加](/docs/zh-CN/errors#terminal-setup-left-your-zed-keymap-unchanged)

如果您在 tmux 内运行，即使外部终端支持，Shift+Enter 也需要下面的 [tmux 配置](#configure-tmux)。

要将换行绑定到不同的键，或交换行为使 Enter 插入换行而 Shift+Enter 提交，请在您的[快捷键文件](/docs/zh-CN/keybindings)中映射 `chat:newline` 和 `chat:submit` 操作。

<h2 id="enable-option-key-shortcuts-on-macos">
  在 macOS 上启用 Option 键快捷键
</h2>

某些 Claude Code 快捷键使用 Option 键，例如 Option+Enter 用于换行或 Option+P 用于切换模型。在 macOS 上，大多数终端默认不会将 Option 作为修饰符发送，因此这些快捷键在启用之前不会起作用。终端设置通常标记为"Use Option as Meta Key"；Meta 是现在标记为 Option 或 Alt 的键的历史 Unix 名称。

<Tabs>
  <Tab title="Apple Terminal">
    打开"设置"→"配置文件"→"键盘"并勾选"Use Option as Meta Key"。

    如果您接受了 Claude Code 的首次运行终端设置提示，这已经完成。该提示为您运行 `/terminal-setup`，它启用 Option 作为 Meta 并在您的 Apple Terminal 配置文件中关闭可听见的铃声。

    在[屏幕阅读器模式](/docs/zh-CN/accessibility)中，`/terminal-setup` 保持铃声设置不变，以便终端铃声保持可听见。在 v2.1.211 之前，`/terminal-setup` 即使在屏幕阅读器模式下也会关闭铃声。如果较早的运行关闭了铃声，请在"设置"→"配置文件"→"高级"→"可听见的铃声"下将其重新打开。
  </Tab>

  <Tab title="iTerm2">
    打开"设置"→"配置文件"→"键"→"常规"并将"Left Option key"和"Right Option key"设置为"Esc+"。

    在 iTerm2 中运行 `/terminal-setup` 会在"设置"→"常规"→"选择"下启用"Applications in terminal may access clipboard"，以便 `/copy` 命令可以写入您的系统剪贴板。该命令即使在 tmux 内运行时也能检测到 iTerm2。重启 iTerm2 以使更改生效。
  </Tab>

  <Tab title="VS Code">
    将 `"terminal.integrated.macOptionIsMeta": true` 添加到您的 VS Code 设置中。
  </Tab>
</Tabs>

对于 Ghostty、Kitty 和其他终端，请在终端的配置文件中查找 Option-as-Alt 或 Option-as-Meta 设置。

<h2 id="get-a-terminal-bell-or-notification">
  获取终端铃声或通知
</h2>

当 Claude 完成任务或暂停以等待权限提示，且您似乎离开了终端时，它会触发通知事件。请参阅[每种通知类型何时触发](/docs/zh-CN/hooks#notification)以了解确切的时间。将其显示为终端铃声或桌面通知可让您在长任务运行时切换到其他工作。

默认情况下，Claude Code 仅在 Ghostty、Kitty 和 iTerm2 中发送桌面通知。在其他终端中，将 [`preferredNotifChannel`](/docs/zh-CN/settings-reference#preferrednotifchannel) 设置为 `"terminal_bell"` 以改为响铃终端铃声，或配置[通知 hook](#play-a-sound-with-a-notification-hook) 以获得自定义声音或命令。以下设置条目打开终端铃声：

```json ~/.claude/settings.json theme={null}
{
  "preferredNotifChannel": "terminal_bell"
}
```

桌面通知通过 SSH 到达您的本地计算机，因此远程会话仍然可以提醒您。Ghostty 和 Kitty 将其转发到您的操作系统通知中心，无需进一步设置。iTerm2 要求您启用转发：

<Steps>
  <Step title="打开 iTerm2 通知设置">
    转到"设置"→"配置文件"→"终端"。
  </Step>

  <Step title="启用警报">
    勾选"通知中心警报"，然后单击"筛选警报"并启用"发送转义序列生成的警报"。
  </Step>
</Steps>

如果通知仍未出现，请确认您的终端应用程序在操作系统设置中具有通知权限，如果您在 tmux 内运行，请[启用传递](#configure-tmux)。

<h3 id="play-a-sound-with-a-notification-hook">
  使用通知 hook 播放声音
</h3>

在任何终端中，您可以配置[通知 hook](/docs/zh-CN/hooks-guide#get-notified-when-claude-needs-input) 以在 Claude 需要您的注意时播放声音或运行自定义命令。Hook 与内置通知一起运行，而不是替换它，因此不接收桌面通知的终端（如 Warp 或 VS Code 集成终端）可以使用 hook 或将 `preferredNotifChannel` 设置为 `"terminal_bell"`。

下面的示例在 macOS 上播放系统声音。链接的指南包含 macOS、Linux 和 Windows 的桌面通知命令。

```json ~/.claude/settings.json theme={null}
{
  "hooks": {
    "Notification": [
      {
        "hooks": [{ "type": "command", "command": "afplay /System/Library/Sounds/Glass.aiff" }]
      }
    ]
  }
}
```

<h2 id="configure-tmux">
  配置 tmux
</h2>

当 Claude Code 在 tmux 中运行时，默认情况下 Shift+Enter 提交而不是插入换行符，桌面通知和[进度条](/docs/zh-CN/settings-reference#terminalprogressbarenabled)永远无法到达外部终端。将这些行添加到 `~/.tmux.conf`，然后运行 `tmux source-file ~/.tmux.conf` 将其应用到运行中的服务器：

```bash ~/.tmux.conf theme={null}
set -g allow-passthrough on
set -s extended-keys on
set -as terminal-features 'xterm*:extkeys'
```

`allow-passthrough` 行允许通知和进度更新到达外部终端，而不是被 tmux 吞掉。`extended-keys` 行让 tmux 区分 Shift+Enter 和普通 Enter，这样换行快捷键就能工作。

<h2 id="fix-backspace-deleting-a-whole-word-on-windows">
  修复 Windows 上 Backspace 删除整个单词的问题
</h2>

在 Windows 上，Claude Code 将到达的 Backspace 读取为 `^H`，将其解释为 Ctrl+Backspace，这会[删除前一个单词](/docs/zh-CN/interactive-mode#text-editing)，除非 `TERM_PROGRAM` 是 `mintty` 或 `TERM` 是 `cygwin`。在 macOS 和 Linux 上，Claude Code 将其读取为普通 Backspace。

如果每次按 Backspace 都会删除整个单词，说明你的终端为普通 Backspace 发送了 `^H`。设置 [`CLAUDE_CODE_BS_AS_CTRL_BACKSPACE=0`](/docs/zh-CN/env-vars)。此时 Backspace 和 Ctrl+H 将各删除一个字符。如果在 macOS 或 Linux 上 Ctrl+Backspace 仅删除一个字符，因为你的终端为它发送了 `^H`，则改为将变量设置为 `1`。

<h2 id="match-the-color-theme">
  匹配颜色主题
</h2>

使用 `/theme` 命令或 `/config` 中的主题选择器，选择与您的终端相匹配的 Claude Code 主题。选择自动选项可检测您的终端的浅色或深色背景，因此主题会在您的终端跟随操作系统外观更改时进行更改。Claude Code 不控制终端本身的配色方案，该方案由终端应用程序设置。

要自定义界面底部显示的内容，请配置一个[自定义状态行](/docs/zh-CN/statusline)，显示当前模型、工作目录、git 分支或其他上下文。

<h3 id="create-a-custom-theme">
  创建自定义主题
</h3>

除了内置预设外，`/theme` 还列出您定义的任何自定义主题以及由已安装的[插件](/docs/zh-CN/plugins/components#themes-and-output-styles)贡献的任何主题。选择列表末尾的\*\*新建自定义主题…\*\*以交互方式创建一个：您命名主题，然后选择要覆盖的各个颜色令牌。当自定义主题突出显示时，按 `Ctrl+E` 可编辑它。

每个自定义主题都是 `~/.claude/themes/` 中的一个 JSON 文件。不带 `.json` 扩展名的文件名是主题的 slug，选择主题会将 `custom:<slug>` 存储为您的主题偏好设置。该文件有三个可选字段：

| 字段 | 类型 | 描述 |
| :- | :- | :- |
| `name` | string | 在 `/theme` 中显示的标签。默认为文件名 slug |
| `base` | string | 主题开始的内置预设：`dark`、`light`、`dark-daltonized`、`light-daltonized`、`dark-ansi` 或 `light-ansi`。默认为 `dark` |
| `overrides` | object | 颜色令牌名称到颜色值的映射。此处未列出的令牌会回退到基础预设 |

颜色值接受 `#rrggbb`、`#rgb`、`rgb(r,g,b)`、`ansi256(n)` 或 `ansi:<name>`，其中 `<name>` 是 16 个标准 ANSI 颜色名称之一，例如 `red` 或 `cyanBright`。未知令牌和无效颜色值会被忽略，因此拼写错误不会破坏渲染。

以下示例定义了一个主题，该主题保留深色预设但重新着色提示符强调、错误文本和成功文本：

```json ~/.claude/themes/dracula.json theme={null}
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}
```

Claude Code 监视 `~/.claude/themes/` 并在添加或更改文件时重新加载，因此在编辑器中所做的编辑会应用到正在运行的会话，无需重启。如果 Claude Code 启动时 `~/.claude/themes/` 文件夹本身不存在，请在创建第一个主题文件后重启一次。之后，更改会应用而无需重启。

下面的参考涵盖了您可以在 `overrides` 中设置的令牌。`/theme` 中的交互式编辑器显示相同的令牌以及实时预览，加上一些单一用途的强调，例如此处省略的入门屏幕颜色。

<Accordion title="颜色令牌参考">
  以下示例结合了下面几个组中的令牌：品牌强调、Plan Mode 边框、diff 背景和消息背景。

  ```json ~/.claude/themes/midnight.json theme={null}
  {
    "name": "Midnight",
    "base": "dark",
    "overrides": {
      "claude": "#a78bfa",
      "planMode": "#38bdf8",
      "diffAdded": "#14532d",
      "diffRemoved": "#7f1d1d",
      "userMessageBackground": "#1e1b4b"
    }
  }
  ```

  <h4 id="text-and-accent-colors">
    文本和强调颜色
  </h4>

  控制整个界面中使用的主要品牌强调和前景文本阴影。

  | 令牌 | 控制 |
  | :- | :- |
  | `claude` | 主要品牌强调，用于微调器和助手标签 |
  | `text` | 默认前景文本 |
  | `inverseText` | 绘制在彩色背景顶部的文本，例如状态徽章 |
  | `inactive` | 次要文本，例如提示、时间戳和禁用项 |
  | `subtle` | 淡色边框和去强调的次要文本 |
  | `suggestion` | 自动完成建议和选择器中的选择突出显示 |
  | `permission` | 对话框边框，包括权限提示和选择器 |
  | `remember` | 内存和 `CLAUDE.md` 指示器 |

  <h4 id="status-colors">
    状态颜色
  </h4>

  在消息和指示器中发出成功、失败和警告状态的信号。

  | 令牌 | 控制 |
  | :- | :- |
  | `success` | 成功消息和通过的检查 |
  | `error` | 错误消息和失败 |
  | `warning` | 警告、注意消息和自动模式指示器 |
  | `merged` | 合并的拉取请求状态 |

  <h4 id="input-box-and-mode-indicators">
    输入框和模式指示器
  </h4>

  设置输入框边框颜色和权限模式或指示器处于活动状态时显示的强调。

  | 令牌 | 控制 |
  | :- | :- |
  | `promptBorder` | 输入框边框 |
  | `planMode` | Plan Mode 强调、Plan Mode 消息和 Plan Mode 对话框 |
  | `autoAccept` | Accept-edits mode 强调 |
  | `bashBorder` | 输入 `!` shell 命令时的输入框边框 |
  | `ide` | IDE 连接指示器 |
  | `fastMode` | Fast mode 指示器 |
  | `effortUltra` | 当[ultracode](/docs/zh-CN/model-config#adjust-effort-level)打开时输入框边框上的 `ultracode` 标签。您对此颜色的覆盖在 Claude Code v2.1.239 或更高版本上生效 |

  <h4 id="diff-rendering">
    Diff 渲染
  </h4>

  在文件编辑和审查中着色添加和删除的代码。

  | 令牌 | 控制 |
  | :- | :- |
  | `diffAdded` | 添加行的背景 |
  | `diffRemoved` | 删除行的背景 |
  | `diffAddedDimmed` | 您拒绝编辑后显示的变暗 diff 中添加行的背景 |
  | `diffRemovedDimmed` | 您拒绝编辑后显示的变暗 diff 中删除行的背景 |
  | `diffAddedWord` | 添加行内的字级突出显示 |
  | `diffRemovedWord` | 删除行内的字级突出显示 |

  <h4 id="fullscreen-mode">
    全屏模式
  </h4>

  Claude Code 在默认和全屏渲染器中都绘制 `userMessageBackground`、`bashMessageBackgroundColor` 和 `memoryBackgroundColor`。它仅在[全屏渲染模式](/docs/zh-CN/fullscreen)中使用 `userMessageBackgroundHover` 和 `selectionBg`。

  | 令牌 | 控制 |
  | :- | :- |
  | `userMessageBackground` | 成绩单中您的消息后面的背景 |
  | `userMessageBackgroundHover` | 悬停或展开消息时消息后面的背景 |
  | `bashMessageBackgroundColor` | 成绩单中 `!` shell 命令条目后面的背景 |
  | `memoryBackgroundColor` | 成绩单中 `#` 内存条目后面的背景 |
  | `selectionBg` | 用鼠标选择的文本的背景 |

  <h4 id="usage-meter-and-speaker-labels">
    使用量计量表和说话者标签
  </h4>

  调整 `/usage` 视图中显示的条形图和区分您的消息与 Claude 消息的标签。

  | 令牌 | 控制 |
  | :- | :- |
  | `rate_limit_fill` | 使用量计量表的填充部分 |
  | `rate_limit_empty` | 使用量计量表的未填充部分 |
  | `briefLabelYou` | 您的消息上 `You` 标签的颜色 |
  | `briefLabelClaude` | 助手消息上 `Claude` 标签的颜色 |

  <h4 id="shimmer-variants-and-subagent-colors">
    微光变体和子代理颜色
  </h4>

  几个令牌有一个配对的微光变体，提供微调器的动画梯度中使用的较浅颜色。如果动画看起来不匹配，请与其基础令牌一起覆盖微光。

  * `claude` 和 `claudeShimmer`
  * `warning` 和 `warningShimmer`
  * `permission` 和 `permissionShimmer`
  * `promptBorder` 和 `promptBorderShimmer`
  * `inactive` 和 `inactiveShimmer`
  * `fastMode` 和 `fastModeShimmer`

  每个[子代理](/docs/zh-CN/sub-agents)和并行任务以八个命名颜色之一显示，以便您可以在成绩单中区分它们。令牌名称遵循 `<color>_FOR_SUBAGENTS_ONLY` 的模式，其中 `<color>` 是 `red`、`blue`、`green`、`yellow`、`purple`、`orange`、`pink` 或 `cyan`。覆盖这些以更改每个命名颜色的外观。例如，定义中具有 `color: blue` 的子代理使用 `blue_FOR_SUBAGENTS_ONLY` 值绘制。

  Claude Code 在提示输入中使用七色彩虹梯度渲染[`ultrathink`](/docs/zh-CN/model-config#use-ultrathink-for-one-off-deep-reasoning)关键字。令牌名称遵循 `rainbow_<color>` 和 `rainbow_<color>_shimmer` 的模式，其中 `<color>` 是 `red`、`orange`、`yellow`、`green`、`blue`、`indigo` 或 `violet`。
</Accordion>

<h2 id="switch-to-fullscreen-rendering">
  切换到全屏渲染
</h2>

在[屏幕阅读器模式](/docs/zh-CN/accessibility)中，本部分不适用。Claude Code 始终呈现为纯滚动文本，除非在附加的[后台会话](/docs/zh-CN/agent-view)中，如果您在任何其他会话中运行 `/tui fullscreen`，Claude Code 会打印说明而不是切换。

如果显示闪烁或在 Claude 工作时滚动位置跳跃，请切换到[全屏渲染模式](/docs/zh-CN/fullscreen)。在此模式下，您可以使用鼠标或 PageUp 在 Claude Code 内滚动，而不是使用终端的原生回滚；请参阅[全屏页面](/docs/zh-CN/fullscreen#search-and-review-the-conversation)了解如何搜索和复制。

如果闪烁是唯一的问题，且您的终端支持同步输出但未被自动检测（例如 Emacs `eat`），请设置 [`CLAUDE_CODE_FORCE_SYNC_OUTPUT=1`](/docs/zh-CN/env-vars) 以停止闪烁而不更改渲染器。

运行 `/tui fullscreen` 以切换并保存偏好设置。您的对话将完整重新启动，未来的会话将以全屏启动，除非[全屏启动失败](/docs/zh-CN/fullscreen#fullscreen-renderer-didnt-finish-starting)。您也可以在启动 Claude Code 之前设置 `CLAUDE_CODE_NO_FLICKER` 环境变量：

<CodeGroup>
  ```bash Bash and Zsh theme={null}
  CLAUDE_CODE_NO_FLICKER=1 claude
  ```

  ```powershell PowerShell theme={null}
  $env:CLAUDE_CODE_NO_FLICKER = "1"; claude
  ```

  ```json ~/.claude/settings.json theme={null}
  {
    "env": {
      "CLAUDE_CODE_NO_FLICKER": "1"
    }
  }
  ```
</CodeGroup>

<h2 id="cap-response-width-in-wide-terminals">
  在宽终端中限制响应宽度
</h2>

在宽终端中，Claude 响应中的每一行文本都会占据窗口的全部宽度。要改为在设定的列数处换行，请在您的设置中设置 [`maxProseWidth`](/docs/zh-CN/settings-reference#maxprosewidth)。

<h2 id="paste-large-content">
  粘贴大型内容
</h2>

当您粘贴超过 800 个字符或超过三行的内容到提示框时，Claude Code 会将输入折叠为占位符，例如 `[Pasted text #1 +120 lines]`，以保持输入框的可用性，并在您提交时仍会发送完整内容。对于非常大的输入（如整个文件或长日志），将内容写入文件并要求 Claude 读取它，而不是粘贴。对话记录保持可读性，Claude 可以在后续轮次中按路径引用文件。VS Code 集成终端也可能在非常大的粘贴到达 Claude Code 之前丢弃字符，因此在那里使用文件。

如果粘贴包含[不可见的 Unicode 字符](/docs/zh-CN/interactive-mode#invisible-characters-in-prompts)，Claude Code 会在您按 Enter 时移除它们，并将清理后的提示放回输入框供您再次按 Enter 发送。

<h3 id="how-claude-treats-pasted-text">
  Claude 如何处理粘贴的文本
</h3>

当您提交时，Claude 会看到每个 `[Pasted text #N]` 占位符后面的内容，标记为您从其他地方粘贴而不是输入的文本。Claude 被告知粘贴可能包含您没有写的指令，并且仅在您输入的消息要求时才遵循其中的指令。在不[获取功能标志](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)的会话中，粘贴不会被标记。

<h3 id="delete-and-restore-a-collapsed-paste">
  删除和恢复折叠的粘贴
</h3>

当您使用单词或行快捷键（如 `Ctrl+W` 或 `Ctrl+K`）删除，或通过 vim 删除（如 `df]` 这样的 `f`/`t` 动作），且删除范围到达 `[Pasted text #N]` 占位符内部时，Claude Code 会完全移除占位符。要恢复它，在单词或行快捷键后使用 [`Ctrl+Y`](/docs/zh-CN/interactive-mode#text-editing) 粘贴删除的内容，或在 vim 删除后使用 [`p` 在 NORMAL 模式下](/docs/zh-CN/interactive-mode#editing-normal-mode)。

<h3 id="recall-a-prompt-that-had-pasted-text">
  调用包含粘贴文本的提示
</h3>

Claude Code 将每个 `[Pasted text #N]` 占位符后面的内容保存在 `~/.claude/paste-cache/` 下，因此当您从[命令历史](/docs/zh-CN/interactive-mode#command-history)中调用提示并重新提交时，完整的粘贴内容会再次发送，包括在后续会话中。

早于 [`cleanupPeriodDays`](/docs/zh-CN/settings-reference#cleanupperioddays) 的缓存文件会根据[保留扫描规则](/docs/zh-CN/claude-directory#cleaned-up-automatically)被删除，因此调用的提示可能引用不再存在的粘贴文本。当您提交这样的提示时，Claude Code 永远不会发送字面上的 `[Pasted text #N]` 字符串，而是显示一个通知，命名缺失的粘贴：

* 在包含剩余文本的纯提示中，Claude Code 移除占位符并发送剩余文本。
* 在[shell 模式](/docs/zh-CN/interactive-mode#shell-mode-with-prefix)命令或 `/` 命令中，其中移除会改变运行内容，以及在任何移除会留下空白的提示中，Claude Code 取消提交并在输入中保留原始文本，占位符仍在其中。删除占位符或编辑命令，然后重新提交。

<h2 id="edit-prompts-with-vim-keybindings">
  使用 Vim 快捷键编辑提示词
</h2>

Claude Code 包含用于提示词输入的 Vim 风格编辑模式。通过 `/config` → Editor mode 启用它，或在 `~/.claude/settings.json` 中将 [`editorMode`](/docs/zh-CN/settings-reference#editormode) 设置为 `"vim"`。将 Editor mode 设置回 `normal` 以关闭它。

Vim 模式支持 NORMAL 和 VISUAL 模式动作和操作符的子集，例如 `hjkl` 导航、`v`/`V` 选择以及 `d`/`c`/`y` 与文本对象。有关完整的快捷键表，请参阅 [Vim 编辑器模式参考](/docs/zh-CN/interactive-mode#vim-editor-mode)。

Vim 动作无法通过快捷键文件重新映射。要将两个按键的 INSERT 模式序列（例如 `jj`）映射到 Escape，请在用户设置中设置 [`vimInsertModeRemaps`](/docs/zh-CN/interactive-mode#remap-insert-mode-key-sequences)。

在 INSERT 模式下按 Enter 仍会提交您的提示词，这与标准 Vim 不同。在 NORMAL 模式下使用 `o` 或 `O`，或使用 Ctrl+J 来插入新行。

<h2 id="related-resources">
  相关资源
</h2>

* [交互模式](/docs/zh-CN/interactive-mode)：完整的键盘快捷键参考和 Vim 快捷键表
* [快捷键](/docs/zh-CN/keybindings)：重新映射任何 Claude Code 快捷键，包括 Enter 和 Shift+Enter
* [全屏渲染](/docs/zh-CN/fullscreen)：全屏模式下滚动、搜索和复制的详细信息
* [钩子指南](/docs/zh-CN/hooks-guide)：Linux 和 Windows 的更多通知钩子示例
* [故障排除](/docs/zh-CN/troubleshooting)：修复终端配置之外的问题
