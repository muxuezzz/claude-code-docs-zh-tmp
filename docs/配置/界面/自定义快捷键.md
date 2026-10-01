> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 自定义快捷键

> 使用快捷键配置文件在 Claude Code 中自定义快捷键。

Claude Code 支持可自定义的快捷键。运行 `/keybindings` 来创建或打开位于 `~/.claude/keybindings.json` 的配置文件。

<h2 id="configuration-file">
  配置文件
</h2>

快捷键配置文件是一个包含 `bindings` 数组的对象。每个块指定一个上下文和一个按键映射到操作的映射。

<Note>快捷键文件的更改会自动检测并应用，无需重启 Claude Code。</Note>

| 字段 | 描述 |
| :- | :- |
| `$schema` | 可选的 JSON Schema URL，用于编辑器自动完成 |
| `$docs` | 可选的文档 URL |
| `bindings` | 按上下文分组的绑定块数组 |

此示例将 `Ctrl+E` 绑定到在聊天上下文中打开外部编辑器，并取消绑定 `Ctrl+S`：

```json theme={null}
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "$docs": "https://code.claude.com/docs/en/keybindings",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+s": null
      }
    }
  ]
}
```

<h2 id="contexts">
  上下文
</h2>

每个绑定块指定一个**上下文**，其中绑定适用：

| 上下文 | 描述 |
| :- | :- |
| `Global` | 在应用程序的任何地方应用 |
| `Chat` | 主聊天输入区域 |
| `Autocomplete` | 自动完成菜单打开 |
| `Settings` | 设置菜单 |
| `Confirmation` | 权限和确认对话框 |
| `Tabs` | 选项卡导航组件 |
| `Help` | 帮助菜单可见 |
| `Transcript` | 记录查看器 |
| `HistorySearch` | 历史记录搜索模式 (Ctrl+R) |
| `Task` | 任务在前台运行 |
| `ThemePicker` | 主题选择器对话框 |
| `Attachments` | 选择对话框中的图像附件导航 |
| `Footer` | 页脚指示器导航（任务、团队、差异、工件） |
| `MessageSelector` | 回退和总结对话框消息选择 |
| `DiffDialog` | 差异查看器导航 |
| `DiffPanel` | [差异面板](/docs/zh-CN/interactive-mode#diff-panel)打开 |
| `ModelPicker` | 模型选择器工作量级别 |
| `EffortSlider` | 由 `/effort` 打开的工作量滑块 |
| `Select` | 通用选择/列表组件 |
| `Plugin` | Plugin 对话框（浏览、发现、管理） |
| `Agents` | [Agent 视图](/docs/zh-CN/agent-view)（`claude agents`） |
| `Scroll` | 对话滚动和全屏模式下的文本选择 |

在 v2.1.205 之前，`/doctor` 诊断屏幕存在 `Doctor` 上下文和 `doctor:fix` 操作。

<h2 id="available-actions">
  可用操作
</h2>

操作遵循 `namespace:action` 格式，例如 `chat:submit` 用于发送消息或 `app:toggleTodos` 用于显示任务列表。每个上下文都有特定的可用操作。

<h3 id="app-actions">
  App 操作
</h3>

在 `Global` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `app:interrupt` | Ctrl+C | 取消当前操作 |
| `app:exit` | Ctrl+D | 退出 Claude Code。在 800ms 内按两次以确认 |
| `app:redraw` | (未绑定) | 强制终端重绘 |
| `app:toggleTodos` | Ctrl+T | 切换 Claude 待办事项清单的可见性。这不是 [`/tasks`](/docs/zh-CN/commands) 后台任务视图 |
| `app:toggleTranscript` | Ctrl+O | 切换详细记录 |

<h3 id="history-actions">
  History 操作
</h3>

用于导航命令历史的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `history:search` | Ctrl+R | 打开历史搜索 |
| `history:previous` | Up | 上一个历史项 |
| `history:next` | Down | 下一个历史项 |

<h3 id="chat-actions">
  Chat 操作
</h3>

在 `Chat` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `chat:cancel` | Escape | 取消当前输入 |
| `chat:clearInput` | Ctrl+L | 强制全屏重绘，保留输入和对话 |
| `chat:clearScreen` | Cmd+K | 与 `chat:clearInput` 相同。请参阅 [清除对话](/docs/zh-CN/fullscreen#clear-the-conversation) 了解 Cmd+K 在 iTerm2 和 Terminal.app 上的行为 |
| `chat:killAgents` | Ctrl+X Ctrl+K | 停止此会话中所有运行的 [后台子代理](/docs/zh-CN/sub-agents#run-subagents-in-foreground-or-background)，并在会话的其余部分关闭 [artifact 自动回复](/docs/zh-CN/artifacts#let-claude-reply-to-comments-on-its-own) |
| `chat:cycleMode` | Shift+Tab\* | 循环权限模式 |
| `chat:modelPicker` | Meta+P | 打开模型选择器 |
| `chat:fastMode` | Meta+O | 切换快速模式 |
| `chat:thinkingToggle` | Meta+T | 切换扩展思考 |
| `chat:submit` | Enter | 提交消息 |
| `chat:queueSubmit` | Ctrl+X Enter | 提交消息，标记为等待其轮次：当 Claude 工作时，Claude Code [将其排队](/docs/zh-CN/interactive-mode#queue-messages-while-claude-works)，永远不会中断轮次。与 `chat:submit` 不同，即使自动完成建议被突出显示，它也会提交草稿。需要 v2.1.247 或更高版本 |
| `chat:sendNow` | Ctrl+Enter, Ctrl+X Ctrl+S | 发送您的 [排队消息](/docs/zh-CN/interactive-mode#queue-messages-while-claude-works) 和您的草稿，立即一起发出。[Claude Code 发送您排队的内容](/docs/zh-CN/interactive-mode#when-claude-code-sends-what-you-queued) 涵盖了 Claude 正在处理的轮次会发生什么。当没有任何内容运行时，该键提交草稿，在 [shell 模式](/docs/zh-CN/interactive-mode#shell-mode-with-prefix) 中，它仅排队命令。不报告扩展键的终端将 `Ctrl+Enter` 传递为纯 `Enter`，因此 `Ctrl+X Ctrl+S` 是在任何终端中都有效的绑定。需要 v2.1.275 或更高版本 |
| `chat:newline` | Ctrl+J | 插入换行符而不提交 |
| `chat:undo` | Ctrl+\_, Ctrl+Shift+- | 撤销上一个操作 |
| `chat:externalEditor` | Ctrl+G, Ctrl+X Ctrl+E | 在外部编辑器中打开。[agent 视图调度输入](/docs/zh-CN/agent-view#keyboard-shortcuts) 也遵循此操作的单键击绑定 |
| `chat:stash` | Ctrl+S | 隐藏当前提示 |
| `chat:imagePaste` | Ctrl+V (Windows 和 WSL 上为 Alt+V) | 从剪贴板粘贴图像。在 WSL 上，默认绑定两个快捷键 |

\*在没有 VT 模式的 Windows 上 (Node \<24.2.0/\<22.17.0, Bun \<1.2.23)，默认为 Meta+M。

<h3 id="autocomplete-actions">
  Autocomplete 操作
</h3>

在 `Autocomplete` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `autocomplete:accept` | Tab | 接受建议 |
| `autocomplete:dismiss` | Escape | 关闭菜单 |
| `autocomplete:previous` | Up | 上一个建议 |
| `autocomplete:next` | Down | 下一个建议 |

<h3 id="confirmation-actions">
  Confirmation 操作
</h3>

在 `Confirmation` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `confirm:yes` | Enter | 确认操作 |
| `confirm:no` | Escape | 拒绝操作 |
| `confirm:previous` | Up | 上一个选项 |
| `confirm:next` | Down | 下一个选项 |
| `confirm:nextField` | Tab | 下一个字段 |
| `confirm:previousField` | (未绑定) | 上一个字段 |
| `confirm:toggle` | Space | 切换选择 |
| `confirm:cycleMode` | Shift+Tab\* | 循环权限模式。在文件权限提示上，关闭打开的 [注释字段](/docs/zh-CN/permissions#add-a-comment-when-you-answer-a-permission-prompt)；没有打开的字段时，选择允许会话其余部分操作的选项（当提示提供该选项时） |

\*在没有 VT 模式的 Windows 上 (Node \<24.2.0/\<22.17.0, Bun \<1.2.23)，默认为 Meta+M。

在 v2.1.257 之前，`confirm:toggleExplanation` 操作绑定到默认的 `Ctrl+E`，在 Bash 和 PowerShell 权限提示上显示模型生成的命令说明。

对话框使用 `confirm:yes` 和 `confirm:no` 来接受和取消，即使它们不提出是或否的问题。如果您在此上下文中绑定裸字母（例如 `y` 或 `n`），该字母也会作用于从不将其显示为键的对话框。显示 `y` 和 `n` 作为其键的对话框会自己读取这些字母，不需要绑定。

在大多数对话框中，按 `Ctrl+C` 或 `Ctrl+D` 两次会关闭对话框而不是退出 Claude Code。第一次按下后的提示会说明第二次按下是关闭对话框还是退出。两个键都是 [保留的](#reserved-shortcuts)，无法重新绑定。

此示例将 `y` 绑定到 `confirm:yes`，将 `n` 绑定到 `confirm:no`：

```json theme={null}
{
  "bindings": [
    {
      "context": "Confirmation",
      "bindings": {
        "y": "confirm:yes",
        "n": "confirm:no"
      }
    }
  ]
}
```

使用这些绑定，当 [文本字段](#text-fields) 有焦点时，`y` 和 `n` 仍然作为字母输入。

在 v2.1.280 之前，`y` 也默认绑定到 `confirm:yes`，`n` 绑定到 `confirm:no`。如果您在 v2.1.280 之前使用 `/keybindings` 创建了 `keybindings.json`，该文件会列出两个绑定，它们会保持有效，直到您删除这两行。

<h3 id="permission-actions">
  Permission 操作
</h3>

在 `Confirmation` 上下文中可用的权限对话框操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `permission:toggleDebug` | (未绑定) | 切换权限调试信息。之前的 Ctrl+D 默认值在 v2.1.146 中被移除，因为它与 `app:exit` 冲突 |

<h3 id="transcript-actions">
  Transcript 操作
</h3>

在 `Transcript` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `transcript:toggleShowAll` | Ctrl+E | 切换显示所有内容 |
| `transcript:exit` | q, Ctrl+C, Escape | 退出记录视图 |

`transcript:toggleShowAll` 仅在经典渲染器中应用；在 [全屏渲染](/docs/zh-CN/fullscreen) 中，记录查看器不提供显示全部切换。

<h3 id="history-search-actions">
  History search 操作
</h3>

在 `HistorySearch` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `historySearch:next` | Ctrl+R | 下一个匹配项 |
| `historySearch:accept` | Escape, Tab | 接受选择 |
| `historySearch:cancel` | Ctrl+C | 取消搜索 |
| `historySearch:execute` | Enter | 执行选定的命令 |
| `historySearch:cycleScope` | Ctrl+S | 循环范围：会话、项目、任何地方 |

`historySearch:next`、`historySearch:accept`、`historySearch:cancel` 和 `historySearch:execute` 默认值适用于经典渲染器中的内联历史搜索，它始终搜索来自所有项目的提示。`historySearch:cycleScope` 仅在 [全屏渲染](/docs/zh-CN/fullscreen) 中生效，其中 `Ctrl+R` 打开搜索对话框，`Ctrl+S` 循环其范围。对话框的其他键是固定的，无法重新绑定：`Enter` 或 `Tab` 将突出显示的匹配项放在提示输入中，`Esc` 取消。

<h3 id="task-actions">
  Task 操作
</h3>

在 `Task` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `task:background` | Ctrl+B, Ctrl+X Ctrl+B | 后台当前任务。Ctrl+X Ctrl+B 弦避免 tmux 前缀冲突 |

<h3 id="theme-actions">
  Theme 操作
</h3>

在 `ThemePicker` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `theme:toggleSyntaxHighlighting` | Ctrl+T | 切换语法高亮 |

<h3 id="help-actions">
  Help 操作
</h3>

在 `Help` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `help:dismiss` | Escape | 关闭帮助菜单 |

<h3 id="tabs-actions">
  Tabs 操作
</h3>

在 `Tabs` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `tabs:next` | Tab, Right | 下一个标签页 |
| `tabs:previous` | Shift+Tab, Left | 上一个标签页 |

在选项卡式对话框中，当选项卡行有焦点时，`tabs:next` 和 `tabs:previous` 会切换选项卡。在某些对话框中，例如 `/help` 和 `/sandbox`，选项卡切换键也可以从选项卡的内容中工作。

`Up` 和 `Down` 在选项卡行和选项卡的内容之间移动焦点，内容中的列表仅在有焦点时才响应键。

<h3 id="attachments-actions">
  Attachments 操作
</h3>

在 `Attachments` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `attachments:next` | Right | 下一个附件 |
| `attachments:previous` | Left | 上一个附件 |
| `attachments:remove` | Backspace, Delete | 移除选定的附件 |
| `attachments:exit` | Down, Escape | 退出附件导航 |

<h3 id="footer-actions">
  Footer 操作
</h3>

在 `Footer` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `footer:next` | Right | 下一个页脚项 |
| `footer:previous` | Left | 上一个页脚项 |
| `footer:up` | Up | 在页脚中向上导航（在顶部取消选择） |
| `footer:down` | Down | 在页脚中向下导航 |
| `footer:openSelected` | Enter | 打开选定的页脚项 |
| `footer:clearSelection` | Escape | 清除页脚选择 |
| `footer:dismiss` | (未绑定) | 绑定键到此操作没有效果，命名它的 `keybindings.json` 保持有效。在 v2.1.281 之前，Backspace 和 Delete 被绑定到它，并从页脚中关闭选定的 artifact 链接。 |

选定页脚项时（例如提示下方的代理面板中的一行），即使您在 `Chat` 上下文中将 `Enter` 重新绑定到 `chat:queueSubmit` 或 `chat:newline`，`Enter` 也会打开它。

`Chat` 绑定在 `Footer` 上下文未绑定的键上（例如 `Shift+Tab` 用于 `chat:cycleMode`）在选定项时继续工作。

<h3 id="message-selector-actions">
  Message selector 操作
</h3>

在 [rewind 菜单](/docs/zh-CN/checkpointing) 的消息列表中，您可以通过 [Select 操作](#select-actions) 及其默认键在消息中移动并选择一条。您的 `Select` 绑定对这些操作也适用于那里。`MessageSelector` 上下文没有自己的操作或默认绑定。使用它通过在 `MessageSelector` 块中绑定 Select 操作（例如 `select:accept`）来仅为此列表更改键。

此示例将 `o` 绑定到在 rewind 菜单中选择突出显示的消息，而不更改任何其他列表：

```json theme={null}
{
  "bindings": [
    {
      "context": "MessageSelector",
      "bindings": {
        "o": "select:accept"
      }
    }
  ]
}
```

在 v2.1.283 之前，此列表忽略 `Select` 绑定，并有自己的操作：`messageSelector:up`、`messageSelector:down`、`messageSelector:top`、`messageSelector:bottom` 和 `messageSelector:select`。如果您的 `keybindings.json` 绑定了其中一个名称，绑定在此列表中继续工作作为执行相同操作的 Select 操作。`Home` 和 `End` 跳到列表的任一端；在 v2.1.283 之前，`Shift+K` 和 `Shift+J` 等键默认执行此操作。

<h3 id="diff-actions">
  Diff 操作
</h3>

在 `DiffDialog` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `diff:dismiss` | Escape | 关闭 diff 查看器；从详细视图返回到文件列表 |
| `diff:previousSource` | Left | 上一个 diff 源 |
| `diff:nextSource` | Right | 下一个 diff 源 |
| `diff:previousFile` | Up, K | 文件列表中的上一个文件；在详细视图中向上滚动一行 |
| `diff:nextFile` | Down, J | 文件列表中的下一个文件；在详细视图中向下滚动一行 |
| `diff:back` | (未绑定) | 在 diff 查看器中返回。Escape 通过 `diff:dismiss` 执行返回操作。之前在详细视图中的 Left 默认值在 v2.1.203 中被移除 |

文件列表也响应 [Select 操作](#select-actions)，通过它们的默认键和您的 `Select` 绑定。`select:previous` 和 `select:next` 移动到上一个和下一个文件，`Enter` 通过 `select:accept` 打开选定文件的 diff。要仅为文件列表更改其中一个键，在 `DiffDialog` 块中绑定 Select 操作。

在 v2.1.283 之前，文件列表忽略 `Select` 绑定，`Enter` 通过单独的 `diff:viewDetails` 操作打开选定文件的 diff。如果您的 `keybindings.json` 绑定了 `diff:viewDetails`，绑定在文件列表中继续工作作为 `select:accept`。

diff 详细视图也将寻呼机样式的键绑定到标准 [滚动操作](#scroll-actions)。这些绑定是 `DiffDialog` 上下文的一部分，仅在详细视图中应用；[滚动操作](#scroll-actions) 下列出的 `Scroll` 上下文默认值保持不变。

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `scroll:pageUp` | PageUp | 向上滚动半个视口 |
| `scroll:pageDown` | PageDown | 向下滚动半个视口 |
| `scroll:fullPageUp` | Shift+Space, B | 向上滚动整个视口 |
| `scroll:fullPageDown` | Space | 向下滚动整个视口 |
| `scroll:top` | G, Home | 跳到顶部 |
| `scroll:bottom` | Shift+G, End | 跳到底部 |

<h3 id="diff-panel-actions">
  Diff panel 操作
</h3>

用于 [diff 面板](/docs/zh-CN/interactive-mode#diff-panel) 的操作，`/diff` 在全屏渲染中打开。`app:cycleDiffBase` 在 `DiffPanel` 上下文中，在面板打开时处于活动状态；其他的在 `Global` 中。该面板需要 Claude Code v2.1.260 或更高版本。

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `app:toggleReplTab` | (未绑定) | 打开或关闭 diff 面板，与运行 `/diff` 相同 |
| `app:cycleDiffBase` | Ctrl+X B | 循环面板的比较基础：此会话、未提交、然后分支 |
| `app:diffFileListUp` | Ctrl+Up, Meta+Up | 当面板的文件列表溢出时向上滚动 |
| `app:diffFileListDown` | Ctrl+Down, Meta+Down | 当面板的文件列表溢出时向下滚动 |
| `app:toggleDiffNoiseFilter` | (未绑定) | 在面板中显示或隐藏测试和生成的文件 |
| `app:toggleDiffPreSession` | (未绑定) | 展开或折叠此会话之前的更改 |

<h3 id="model-picker-actions">
  Model picker 操作
</h3>

在 `ModelPicker` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `modelPicker:decreaseEffort` | Left | 降低努力级别 |
| `modelPicker:increaseEffort` | Right | 提高努力级别 |
| `modelPicker:thisSessionOnly` | s | 仅将突出显示的模型应用于此会话 |

<h3 id="effort-slider-actions">
  Effort slider 操作
</h3>

在 `EffortSlider` 上下文中可用的操作，当您运行不带参数的 `/effort` 时打开的滑块。滑块的 Enter 和 Escape 键无法重新绑定。

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `effortSlider:decreaseEffort` | Left | 将滑块移动到下一个较低的努力级别。需要 v2.1.284 或更高版本 |
| `effortSlider:increaseEffort` | Right | 将滑块移动到下一个较高的努力级别。需要 v2.1.284 或更高版本 |
| `effortSlider:toggleUltracode` | Tab | 为此会话打开或关闭 [ultracode](/docs/zh-CN/workflows#let-claude-decide-with-ultracode)，当滑块 [提供它](/docs/zh-CN/model-config#when-ultracode-is-available) 时。需要 v2.1.284 或更高版本 |
| `effortSlider:thisSessionOnly` | s | 仅将焦点 [努力级别](/docs/zh-CN/model-config#adjust-effort-level) 应用于此会话。需要 v2.1.257 或更高版本 |

<h3 id="select-actions">
  Select 操作
</h3>

在 `Select` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `select:next` | Down, J, Ctrl+N | 下一个选项 |
| `select:previous` | Up, K, Ctrl+P | 上一个选项 |
| `select:pageUp` | PageUp | 向上移动一页选项 |
| `select:pageDown` | PageDown | 向下移动一页选项 |
| `select:first` | Home | 第一个选项 |
| `select:last` | End | 最后一个选项 |
| `select:accept` | Enter | 接受选择 |
| `select:cancel` | Escape | 取消选择 |

在列表面板中，例如 `/skills`、`/mcp` 和 `/tasks`，Claude Code 应用您的 `select:pageUp`、`select:pageDown`、`select:first` 和 `select:last` 绑定。在大多数其他列表中，例如 `/model` 选择器，您的 `select:first` 和 `select:last` 绑定适用。PageUp 和 PageDown 在这些列表中进行分页，无论您的绑定如何。

在 v2.1.280 之前，这些其他列表忽略 Home、End 和您的 `select:first` 和 `select:last` 绑定。

在 v2.1.283 之前，`/mcp` 工具列表使用固定的 PageUp 和 PageDown 键进行分页，无论您的绑定如何。

<h3 id="plugin-actions">
  Plugin 操作
</h3>

在 `Plugin` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `plugin:toggle` | Space | 切换插件选择 |
| `plugin:install` | I | 安装选定的插件 |
| `plugin:favorite` | F | 收藏选定的插件，使其在"已安装"标签页附近排序 |

<h3 id="settings-actions">
  Settings 操作
</h3>

在 `Settings` 上下文中可用的操作。`select:accept` 和 `confirm:no` 操作从 [Select](#select-actions) 和 [Confirmation](#confirmation-actions) 上下文重用，具有特定于设置的行为：更改在您更改时立即应用于每个设置，因此 Escape 关闭面板并保存您的更改，而不是拒绝。

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `settings:search` | / | 进入搜索模式 |
| `settings:retry` | R | 在错误时重试加载使用数据 |
| `select:accept` | Enter, Space | 更改选定的设置或打开其子菜单 |
| `confirm:no` | Escape | 关闭面板。更改已保存 |

<h3 id="agents-actions">
  Agents 操作
</h3>

在 `Agents` 上下文中可用的操作，适用于 [agent 视图](/docs/zh-CN/agent-view)，使用 `claude agents` 打开。需要 v2.1.257 或更高版本。

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `agents:switchView` | Ctrl+S | 在状态和目录之间切换 [会话分组](/docs/zh-CN/agent-view#organize-the-list) |
| `agents:togglePin` | Ctrl+T | [固定或取消固定](/docs/zh-CN/agent-view#organize-the-list) 选定的会话 |

当 agent 视图打开时，Claude Code 对 `Agents` 上下文绑定的任何键使用 `Agents` 绑定，并忽略同一键上的 `Chat` 或 `Global` 绑定。例如，在 agent 视图中按 Ctrl+S 会切换会话分组，而不是触发默认的 `chat:stash`。

调度输入的外部编辑器快捷键不是 `Agents` 操作。Agent 视图遵循 `Chat` 上下文的 `chat:externalEditor` 绑定，默认为 Ctrl+G。

绑定在 agent 视图中的单个按键上触发，因此绑定到 `chat:externalEditor` 的 Ctrl+X Ctrl+E 弦不会在那里打开编辑器。

<h3 id="voice-actions">
  Voice 操作
</h3>

当 [语音听写](/docs/zh-CN/voice-dictation) 启用时，在 `Chat` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `voice:pushToTalk` | Space | 听写提示。根据 `/voice` 模式按住或点击 |

<h3 id="scroll-actions">
  Scroll 操作
</h3>

当 [全屏渲染](/docs/zh-CN/fullscreen) 启用时，在 `Scroll` 上下文中可用的操作：

| 操作 | 默认 | 描述 |
| :- | :- | :- |
| `scroll:lineUp` | `wheelup` | 向上滚动一行。鼠标滚轮滚动触发此操作 |
| `scroll:lineDown` | `wheeldown` | 向下滚动一行。鼠标滚轮滚动触发此操作 |
| `scroll:pageUp` | PageUp | 向上滚动半个视口高度 |
| `scroll:pageDown` | PageDown | 向下滚动半个视口高度 |
| `scroll:top` | Ctrl+Home | 跳到对话的开始 |
| `scroll:bottom` | Ctrl+End | 跳到最新消息并重新启用自动跟随 |
| `scroll:halfPageUp` | (未绑定) | 向上滚动半个视口高度。与 `scroll:pageUp` 相同的行为，为 vi 样式重新绑定提供 |
| `scroll:halfPageDown` | (未绑定) | 向下滚动半个视口高度。与 `scroll:pageDown` 相同的行为，为 vi 样式重新绑定提供 |
| `scroll:fullPageUp` | (未绑定) | 向上滚动整个视口高度 |
| `scroll:fullPageDown` | (未绑定) | 向下滚动整个视口高度 |
| `selection:copy` | Ctrl+Shift+C / Cmd+C | 将选定的文本复制到剪贴板 |
| `selection:clear` | (未绑定) | 清除活动的文本选择。需要 v2.1.234 或更高版本 |
| `selection:extendLeft` | Shift+Left | 将活动选择向左扩展一列 |
| `selection:extendRight` | Shift+Right | 将活动选择向右扩展一列 |
| `selection:extendUp` | Shift+Up | 将活动选择向上扩展一行。当选择到达顶部边缘时滚动视口 |
| `selection:extendDown` | Shift+Down | 将活动选择向下扩展一行。当选择到达底部边缘时滚动视口 |
| `selection:extendLineStart` | Shift+Home | 将活动选择扩展到行的开始 |
| `selection:extendLineEnd` | Shift+End | 将活动选择扩展到行的结束 |

<h2 id="keystroke-syntax">
  按键语法
</h2>

<h3 id="modifiers">
  修饰符
</h3>

使用修饰符键和 `+` 分隔符：

* `ctrl` 或 `control` - Control 键
* `shift` - Shift 键
* `alt`、`opt`、`option` 或 `meta` - Windows 和 Linux 上的 Alt 键，macOS 上的 Option 键
* `cmd`、`command`、`super` 或 `win` - macOS 上的 Command 键，Windows 上的 Windows 键，Linux 上的 Super 键

`cmd` 组仅在报告 Super 修饰符的终端中被检测到，例如支持 Kitty 键盘协议或 xterm 的 `modifyOtherKeys` 模式的终端。大多数终端不会发送它，因此对于希望在任何地方都能工作的绑定，请使用 `ctrl` 或 `meta`。

例如：

```text theme={null}
ctrl+k          Ctrl + K
shift+tab       Shift + Tab
meta+p          macOS 上的 Option + P，其他地方的 Alt + P
ctrl+shift+c    多个修饰符
```

<h3 id="uppercase-letters">
  大写字母
</h3>

Claude Code 不区分大小写地解析按键名称，因此 `K` 与 `k` 的绑定相同，`ctrl+K` 与 `ctrl+k` 相同。要绑定 Shift 和一个字母，请写 `shift+k`。

<h3 id="non-us-keyboard-layouts">
  非美国键盘布局
</h3>

即使您的活动键盘布局输入其他字符，也要将 Ctrl 快捷键的按键名称写成拉丁字符。

Claude Code 如何将您按下的按键与绑定匹配取决于布局的类型：

* 在非拉丁布局（如西里尔字母）下，当终端使用 Kitty 键盘协议并报告该位置时，Claude Code 通过按键的美国布局位置来匹配 Ctrl 快捷键。在这样的终端中，使用俄语布局时，按下 Ctrl 和物理 W 键会触发 `ctrl+w`。在不报告位置的终端中，Claude Code 匹配终端为按键发送的任何内容：ASCII 控制代码触发拉丁快捷键，作为西里尔字符到达的按键不匹配任何绑定
* 在重新排列拉丁字母的布局（如 AZERTY）下，Claude Code 匹配按键输入的字母，因此按下 Ctrl 和标记为 A 的按键会触发 `ctrl+a`

在 v2.1.247 之前，在使用 Kitty 键盘协议的终端（如 Ghostty、Kitty、WezTerm 和 iTerm2）中，在非拉丁布局下按下 Ctrl 快捷键不会触发其绑定。

<h3 id="chords">
  和弦
</h3>

和弦是由空格分隔的按键序列：

```text theme={null}
ctrl+k ctrl+s   按 Ctrl+K，释放，然后按 Ctrl+S
```

在前一个按键的 3 秒内按下每个按键。如果您等待更长时间，Claude Code 会取消和弦并显示一条简短通知。

<h3 id="special-keys">
  特殊键
</h3>

* `escape` 或 `esc` - Escape 键
* `enter` 或 `return` - Enter 键
* `tab` - Tab 键
* `space` - 空格键
* `up`、`down`、`left`、`right` - 箭头键
* `pageup`、`pagedown` - Page Up 和 Page Down 键
* `home`、`end` - Home 和 End 键
* `backspace`、`delete` - 删除键
* `wheelup`、`wheeldown` - 鼠标滚轮滚动事件

<h2 id="unbind-default-shortcuts">
  取消绑定默认快捷键
</h2>

将操作设置为 `null` 以取消绑定默认快捷键：

```json theme={null}
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+s": null
      }
    }
  ]
}
```

这也适用于和弦绑定。取消绑定共享前缀的每个和弦会释放该前缀以用作单键绑定。任何活跃上下文中的和弦都会保留其前缀，因此您必须在定义该和弦的上下文中取消绑定每个和弦。

Claude Code 在 `ctrl+x` 前缀上绑定这些默认和弦：`Chat` 中的 `ctrl+x ctrl+k`、`ctrl+x ctrl+e`、`ctrl+x enter`、`ctrl+x ctrl+a`、`ctrl+x ctrl+s` 和 `ctrl+x tab`，`Task` 中的 `ctrl+x ctrl+b`，以及 `DiffPanel` 中的 `ctrl+x b`。`ctrl+x enter` 和弦需要 v2.1.247 或更高版本，`ctrl+x b`、`ctrl+x ctrl+a` 和 `ctrl+x tab` 需要 v2.1.260 或更高版本，以及 `ctrl+x ctrl+s` 需要 v2.1.275 或更高版本。

要将 `ctrl+x` 本身回收为单键绑定，请取消绑定所有这些：

```json theme={null}
{
  "bindings": [
    {
      "context": "Task",
      "bindings": {
        "ctrl+x ctrl+b": null
      }
    },
    {
      "context": "DiffPanel",
      "bindings": {
        "ctrl+x b": null
      }
    },
    {
      "context": "Chat",
      "bindings": {
        "ctrl+x ctrl+k": null,
        "ctrl+x ctrl+e": null,
        "ctrl+x enter": null,
        "ctrl+x ctrl+a": null,
        "ctrl+x ctrl+s": null,
        "ctrl+x tab": null,
        "ctrl+x": "chat:newline"
      }
    }
  ]
}
```

如果您取消绑定前缀上的某些但不是全部和弦，按下前缀仍会进入和弦等待模式以处理剩余的绑定。

<h2 id="reserved-shortcuts">
  保留的快捷键
</h2>

这些快捷键无法重新绑定：

| 快捷键 | 原因 |
| :- | :- |
| Ctrl+C | 硬编码的中断/取消 |
| Ctrl+D | 硬编码的退出 |
| Ctrl+M | Claude Code 始终将其接收为 Enter |
| Ctrl+\[ | Claude Code 始终将其接收为 Escape。在使用 Kitty 键盘协议的终端中，这需要 v2.1.242 或更高版本 |
| Ctrl+I | Claude Code 始终将其接收为 Tab |
| Ctrl+H | 发送 ASCII 退格字节。[Claude Code 在 Windows 上如何读取它](/docs/zh-CN/terminal-config#fix-backspace-deleting-a-whole-word-on-windows)取决于您的终端和 [`CLAUDE_CODE_BS_AS_CTRL_BACKSPACE`](/docs/zh-CN/env-vars) 环境变量 |
| Caps Lock | 不传递到终端应用程序 |

<h2 id="terminal-conflicts">
  终端冲突
</h2>

某些快捷键可能与终端多路复用器冲突：

| 快捷键 | 冲突 |
| :- | :- |
| Ctrl+B | tmux 前缀（按两次发送） |
| Ctrl+A | GNU screen 前缀 |
| Ctrl+Z | Unix 进程暂停（SIGTSTP） |

<h2 id="text-fields">
  文本字段
</h2>

如果你绑定一个裸字母、数字或空格，你仍然可以在对话框或面板内的文本字段中输入该字符。其中一个字段是 Claude 提出问题的 `Other` 答案。当该字段获得焦点时，你按下的不带 Ctrl、Alt 或 Cmd 的可打印键会进入该字段，Claude Code 不会根据你的绑定来匹配它。

这些键在字段获得焦点时仍然会运行其绑定：

* 不输入字符的键，例如 Enter、Escape、Tab 和箭头键
* 任何与 Ctrl、Alt 或 Cmd 一起按下的键
* 已在进行中的[和弦](#chords)的第二个按键

在主提示符处，Claude Code 根据活跃的上下文（例如 `Chat`）匹配每个键，仅当没有绑定接受该键时才输入该键。

<h2 id="vim-mode-interaction">
  Vim 模式交互
</h2>

启用 vim 模式（通过 `/config` → 编辑器模式）时，快捷键和 vim 模式独立运行：

* **Vim 模式**在文本输入级别处理输入（光标移动、模式、动作）
* **快捷键**在组件级别处理操作（切换待办事项、提交等）
* vim 模式中的 Escape 键从 INSERT 切换到 NORMAL 模式；它不触发 `chat:cancel`
* 大多数 Ctrl+key 快捷键通过 vim 模式传递到快捷键系统
* Vim 键不能通过快捷键文件重新映射。要映射两键 INSERT 模式序列（如 `jj`）到 Escape，请使用 [`vimInsertModeRemaps`](/docs/zh-CN/interactive-mode#remap-insert-mode-key-sequences) 设置
* 在 vim NORMAL 模式中，`?` 显示帮助菜单（vim 行为）
* 在 vim NORMAL 模式中，`/` 打开历史搜索，与标准模式中的 Ctrl+R 相同

<h2 id="validation">
  验证
</h2>

Claude Code 验证您的快捷键并向调试日志写入以下警告：

* 解析错误（无效的 JSON 或结构）
* 拼写错误的修饰符，例如 `ctl+k`。Claude Code 会删除它无法识别的部分，并将绑定应用于剩余的按键，在此示例中为 `k`。
* 无效的上下文名称
* 无效的操作值，例如不是字符串或 `null` 的操作
* 未知的操作名称，例如注册操作的拼写错误。Claude Code 跳过该绑定并保持该键的任何默认绑定有效。在 v2.1.246 之前，具有未知操作名称的绑定会静默禁用该键
* 保留快捷键冲突
* 同一上下文中的重复绑定

使用 [`--debug`](/docs/zh-CN/cli-reference#cli-flags) 启动 Claude Code 以查看详细信息。
