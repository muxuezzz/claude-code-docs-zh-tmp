> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用 Claude Code 与屏幕阅读器

> 为 VoiceOver 和 NVDA 等屏幕阅读器设置 Claude Code，以及屏幕放大镜、减少动画和色盲友好主题的设置。

Claude Code 具有屏幕阅读器模式，可将其视觉终端界面替换为纯文本、线性文本。该模式不使用框、进度动画和原地重绘，而是打印带标签的行，屏幕阅读器（如 VoiceOver 或 NVDA）按顺序读取这些行，因此您可以进行完整对话、批准工具权限并从头到尾查看输出。

屏幕阅读器模式是可选的。如果您使用屏幕放大镜、减少动画或色盲友好主题而不是屏幕阅读器，请从[辅助功能设置](#accessibility-settings)表中设置 `CLAUDE_CODE_ACCESSIBILITY`、`prefersReducedMotion` 或 `theme`。屏幕阅读器模式仅调整终端界面，因此您不需要在 VS Code 扩展的聊天面板中使用它。在 Claude Code v2.1.236 或更高版本上，该扩展[在不需要任何设置的情况下向您的屏幕阅读器宣布对话活动](/docs/zh-CN/vs-code#use-a-screen-reader)。

<h2 id="turn-on-screen-reader-mode">
  打开屏幕阅读器模式
</h2>

选择与您使用屏幕阅读器频率相匹配的方法：

* 对于一个会话：运行 `claude --ax-screen-reader`。
* 对于从一个 shell 启动的会话：设置 `CLAUDE_AX_SCREEN_READER` 环境变量为 `1`。在 Bash 或 Zsh 中，运行 `export CLAUDE_AX_SCREEN_READER=1`。在 PowerShell 中，运行 `$env:CLAUDE_AX_SCREEN_READER = "1"`。将该行添加到您的 shell 配置文件以保持它用于未来的 shell。
* 对于机器上的每个会话：将 `"axScreenReader": true` 添加到您的用户[设置文件](/docs/zh-CN/settings)。该设置适用于任何终端，包括 VS Code 集成终端。

如果您组合方法，Claude Code 将 [`--ax-screen-reader`](/docs/zh-CN/cli-reference#cli-flags) 标志应用于 [`CLAUDE_AX_SCREEN_READER`](/docs/zh-CN/env-vars#variables) 环境变量，以及该变量应用于 [`axScreenReader`](/docs/zh-CN/settings-reference#axscreenreader) 设置。

如果您通过 SSH 使用 Claude Code，请在运行 Claude Code 的远程机器上设置环境变量或设置。

Claude Code 打印的第一行确认该模式：`[Screen Reader Mode: on via flag]`、`[Screen Reader Mode: on via env]` 或 `[Screen Reader Mode: on via settings]`。

<h2 id="turn-off-screen-reader-mode">
  关闭屏幕阅读器模式
</h2>

反转打开模式的任何方法：启动时不使用标志、取消设置环境变量或将 `axScreenReader` 设置为 `false`。如果将 `CLAUDE_AX_SCREEN_READER` 设置为 `0`，Claude Code 即使在设置为 `true` 时也会保持模式关闭。

<h2 id="accessibility-settings">
  无障碍设置
</h2>

该表列出了每个无障碍选项、您是将其设置为标志、环境变量还是设置，以及它改变的内容。

| 选项 | 类型 | 改变的内容 |
| :- | :- | :- |
| [`--ax-screen-reader`](/docs/zh-CN/cli-reference#cli-flags) | 标志 | 单个会话的屏幕阅读器模式。 |
| [`CLAUDE_AX_SCREEN_READER`](/docs/zh-CN/env-vars#variables) | 环境变量 | 从您设置它的 shell 启动的会话的屏幕阅读器模式。 |
| [`axScreenReader`](/docs/zh-CN/settings-reference#axscreenreader) | 设置 | 当为 `true` 时，每个会话的屏幕阅读器模式。 |
| [`CLAUDE_AX_STARTUP_QUIET_MS`](/docs/zh-CN/env-vars#variables) | 环境变量 | Claude Code 在确认行之后等待多长时间才能在屏幕阅读器模式下绘制第一个提示。需要 Claude Code v2.1.217 或更高版本。 |
| [`CLAUDE_AX_PREPARK_MS`](/docs/zh-CN/env-vars#variables) | 环境变量 | Claude Code 在屏幕阅读器模式下，光标位于行首时，等待多长时间才能写入新行或更改的行。需要 Claude Code v2.1.233 或更高版本。 |
| [`CLAUDE_CODE_ACCESSIBILITY`](/docs/zh-CN/env-vars#variables) | 环境变量 | 当您将其设置为 `1` 时，终端光标对屏幕放大镜（如 macOS Zoom）保持可见。光标跟随输入插入符号，在 Claude Code v2.1.218 或更高版本上，跟随菜单和面板（如 `/config` 和 `/plugin`）中的突出显示行。 |
| [`prefersReducedMotion`](/docs/zh-CN/settings-reference#prefersreducedmotion) | 设置 | 当为 `true` 时，减少或没有旋转器、闪烁和其他动画。 |
| [`theme`](/docs/zh-CN/settings-reference#theme) | 设置 | 界面颜色，包括色盲友好的 `dark-daltonized` 和 `light-daltonized` 主题。您也可以使用 [`/theme`](/docs/zh-CN/commands#all-commands) 选择一个。 |
| [`preferredNotifChannel`](/docs/zh-CN/settings-reference#preferrednotifchannel) | 设置 | 当值为 `"terminal_bell"` 时，在屏幕阅读器模式外，当 Claude 等待您时发出终端铃声。 |

<h2 id="what-your-screen-reader-hears">
  屏幕阅读器听到的内容
</h2>

在屏幕阅读器模式中，Claude Code 写入平面文本：

* 界面框架没有方框绘制字符
* 没有仅限颜色的提示
* 没有未更改内容的重绘。进度旋转器呈现为静态文本
* Claude 回复中的表格读作 `Header: value` 句子而不是方框字符网格

Claude Code 将其打印到终端滚动条中的所有内容都保留下来，因此您可以使用屏幕阅读器的审查命令或终端的搜索功能重新阅读之前的回合。Claude Code 在屏幕阅读器模式下忽略 [`tui` 设置](/docs/zh-CN/settings-reference#tui)。除了在[已知限制](#known-limitations)下列出的附加后台会话外，它打印滚动文本而不是[全屏渲染](/docs/zh-CN/fullscreen)。

Claude Code 还在两个点等待，以便屏幕阅读器能够跟上：

* Claude Code 打印确认行后，在绘制提示之前等待 3 秒，以便屏幕阅读器可以完成该行。按任意键结束等待。要更改等待的长度，请设置 [`CLAUDE_AX_STARTUP_QUIET_MS`](/docs/zh-CN/env-vars#variables)。
* 在 Claude Code 写入新行或更改的行（例如提示或更多 Claude 的回复）之前，它将光标移到行的开始处并等待 50 毫秒。然后屏幕阅读器从其第一个字符读取该行。您在输入行末尾键入或删除的字符立即出现。要更改等待的长度，请设置 [`CLAUDE_AX_PREPARK_MS`](/docs/zh-CN/env-vars#variables)。

成绩单中的每条消息都以屏幕阅读器宣布的标签开头，命名其内容：您的消息、Claude 的回复和思考、工具活动、错误和警告以及提示。这些标签也是可搜索的，因此您可以通过搜索终端的滚动条在成绩单的各个部分之间跳转：

| 标签 | 含义 |
| :- | :- |
| `you:` | 您的消息 |
| `claude:` | Claude 的回复 |
| `thinking:` | Claude 的思考 |
| `tool:` | 工具活动，例如文件编辑或命令运行 |
| `tool error:` | 失败的工具 |
| `error:` | 对话中的错误，例如失败的 API 请求 |
| `warning:` | Claude Code 的警告，例如切换到备用模型 |
| `Permission Required:` | 等待您的答案的权限提示 |
| `Cost:` | Claude Code 退出时的会话成本摘要，如果您的帐户[显示成本](/docs/zh-CN/costs) |

Claude Code 将终端光标保持在输入插入符上，因此屏幕阅读器的读取当前行命令读取您正在编辑的提示。

当您在输入行末尾键入时，或在那里按 `Backspace`，Claude Code 仅写入更改的字符。您的屏幕阅读器仅回显这些字符。

当您使用[文本编辑快捷键](/docs/zh-CN/interactive-mode#text-editing)之一删除单词或行时，Claude Code 宣布删除的文本：

* 使用 `Ctrl+W` 或 `Alt+D` 删除单词，或在 macOS 上使用 `Option+Delete` 或在 Windows 上使用 `Ctrl+Backspace`
* 使用 `Ctrl+U` 或 `Cmd+Backspace` 删除到行的开始
* 使用 `Ctrl+K` 删除到行的末尾

当您使用 `Shift+Tab` 循环[权限模式](/docs/zh-CN/permission-modes)时，Claude Code 宣布您登陆的权限模式，例如 `[plan mode on]` 或 `[accept edits on]`。Claude Code 打印公告一次，不会在以后的重绘中重复。

<h3 id="jump-between-turns">
  在回合之间跳转
</h3>

Claude Code 在回合边界处发出 OSC 133 shell-integration 标记，因此您的终端的跳转到上一个提示键在回合之间移动，而无需阅读整个成绩单：

* iTerm2：Cmd+Shift+Up
* VS Code 终端：Windows 上的 Ctrl+Up，macOS 上的 Cmd+Up
* Windows Terminal：默认情况下没有键；在其设置中绑定 `scrollToMark` 操作
* Kitty 和 Ghostty：检查终端的文档以获取其跳转到提示键

macOS Terminal 不对标记进行操作，Claude Code 在 WezTerm 中不发出它们。在这些终端中，搜索滚动条中的 `you:` 标签。

<h2 id="answer-menus-and-prompts">
  回答菜单和提示
</h2>

在屏幕阅读器模式中，您通常使用箭头键导航的菜单（包括权限提示）会变成编号列表。Claude Code 将每个选项宣布为编号行，然后是一个 `Select with numbers` 提示，该提示命名有效范围。输入您想要的选项的编号，然后按 Enter。

* 按 Escape 键取消提示以 `or Escape to cancel` 结尾的菜单。
* 如果您输入的数字不在列表中，Claude Code 会宣布有效范围，让您重试。

[`/effort`](/docs/zh-CN/model-config#adjust-effort-level) 选择器在屏幕阅读器模式外是一个滑块，在屏幕阅读器模式中变成相同类型的编号列表。

是或否提示要求输入类型的答案，而不是两选项菜单。回答 `y` 或 `n` 并按 Enter。`yes` 和 `no` 也可以。

<h2 id="hear-when-claude-code-needs-you">
  听取 Claude Code 何时需要你
</h2>

在屏幕阅读器模式下，当 Claude Code 需要你的注意时，它会响起终端铃声，这样你就不必一直检查记录。铃声在以下情况下响起：

* Claude 完成回复
* 提示或对话框需要你的答案，例如权限提示
* 运行时间超过 5 秒的工具完成

铃声是你的终端的标准警报。要使其静音，请更改你的终端应用程序中的铃声设置。在屏幕阅读器模式之外，设置 [`preferredNotifChannel`](/docs/zh-CN/settings-reference#preferrednotifchannel) 为 `"terminal_bell"` 以在 Claude 等待你时获得[类似的铃声](/docs/zh-CN/terminal-config#get-a-terminal-bell-or-notification)。

<h2 id="known-limitations">
  已知限制
</h2>

某些行为不适应屏幕阅读器模式：

* 屏幕阅读器模式在屏幕阅读器运行时不会自动打开。
* Claude Code 不会宣布通过除了使用 `Shift+Tab` 循环以外的任何方式进行的权限模式更改，例如从命令进入[计划模式](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode)。
* 使用 `claude attach` 或从代理视图附加到[后台会话](/docs/zh-CN/agent-view)会进入终端的备用屏幕，该屏幕没有本机滚动缓冲区。这与[其他附加会话的行为相同](/docs/zh-CN/fullscreen)。要退出，请在空提示上按左箭头，或如果对话框有焦点，请按 Ctrl+Z。
* Claude Code 在退出时打印的摘要中宣布成本，而不是每轮。
* 屏幕阅读器模式不改变带有 `-p` 标志的[非交互模式](/docs/zh-CN/headless)。非交互模式已经写入纯文本，并且仍然是脚本编写的替代方案。

<h2 id="report-an-issue">
  报告问题
</h2>

如果屏幕阅读器、放大镜或终端出现问题，请在 [Claude Code 问题跟踪器](https://github.com/anthropics/claude-code/issues)上打开问题，并在标题中提及您的辅助技术。在报告中包括您的操作系统、终端应用程序以及辅助技术名称和版本。
