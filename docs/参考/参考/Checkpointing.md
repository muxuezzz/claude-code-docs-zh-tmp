> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Checkpointing

> 跟踪、回溯和总结 Claude 的编辑和对话以管理会话状态。

Claude Code 自动跟踪 Claude 在工作时所做的文件编辑，允许您快速撤销更改并回溯到之前的状态，以防任何事情出现偏差。

## checkpointing 如何工作

当您与 Claude 合作时，checkpointing 会自动捕获每次您发送开始一个回合的提示前代码的状态。

### 自动跟踪

Claude Code 跟踪其文件编辑工具所做的所有更改：

* 每个您发送的开始一个回合的提示都会创建一个新的 checkpoint
* Claude Code 在一个会话中保留最近 100 个 checkpoint 的文件快照。丢弃较旧的 checkpoint 会删除没有其他 checkpoint 引用的快照文件，除了每个文件的第一个快照，VS Code 扩展将其用作会话 diffs 的基线。
* Claude Code 将 checkpoints 与对话一起保存，因此您可以在恢复会话后仍然运行 `/rewind`
* Claude Code 在 [retention sweep](https://code.claude.com/docs/zh-CN/claude-directory.md#cleaned-up-automatically) 中删除会话的文件快照，默认情况下在会话最后一次保存后约 30 天。回溯到快照已消失的 checkpoint 可能会失败，出现 [`No files were restored`](https://code.claude.com/docs/zh-CN/errors#no-files-were-restored) 错误。要保留快照更长时间，请设置 [`cleanupPeriodDays`](https://code.claude.com/docs/zh-CN/settings-reference#cleanupperioddays)。

### 回溯和总结

运行 `/rewind`，或在提示输入为空时按两次 `Esc`，打开回溯菜单。

> [!NOTE]
>
> 如果提示输入包含文本，双 `Esc` 会清除它而不是打开菜单。清除的文本会保存到您的输入历史记录中，因此在您完成回溯菜单后，按 `Up` 可以调用它。

回溯菜单列出了您在会话期间发送的提示词。选择您想要操作的点，然后选择一个操作：

* **恢复代码和对话**：将代码和对话都恢复到该点
* **恢复对话**：回溯到该消息，同时保持当前代码
* **恢复代码**：恢复文件更改，同时保持对话
* **从此处总结**：将此点之后的对话压缩为摘要，释放 context window 空间
* **到此处总结**：将此点之前的对话压缩为摘要，保持后续消息完整
* **算了**：返回消息列表而不做任何更改

两个代码恢复选项仅在所选 checkpoint 具有要恢复的跟踪文件更改时出现。如果该点之后没有捕获文件编辑，菜单仅提供 **恢复对话**、总结选项和 **算了**。

恢复对话或选择"从此处总结"后，所选消息的原始提示会恢复到输入字段中，以便您可以重新发送或编辑它。

选择"到此处总结"会让您留在对话末尾，输入字段为空。使用任一总结选项，**总结的对话** 标记会出现在对话中压缩消息的位置。

#### 如果您在发送下一个提示词之前退出，已回溯的消息可能会重新出现

要再次移除重新出现的消息，请在该会话中运行 `/rewind` 并选择相同的提示词，然后选择 **恢复对话**。在退出之前，请向 Claude 发送一个提示词，因为 Claude Code 会将回溯后的对话与该提示词一起保存。您已恢复的文件会保持回溯后的状态。

#### 回溯过去已清除的对话

如果您在同一 Claude Code 进程中较早运行了 `/clear`，回溯菜单会在列表顶部显示一个额外的条目，标记为 `/resume <session-id> (previous session)`。选择它可以恢复在 `/clear` 运行前活跃的对话。该条目在您退出 Claude Code 或恢复不同会话之前可用。

#### 指导总结

总结不会改变磁盘上的文件，原始消息保留在会话记录中，因此 Claude 仍然可以参考详细信息。要指导总结的重点，用箭头键突出显示 **总结** 选项，并在行显示 **add context (optional)** 的位置输入说明，然后按 `Enter`。用其数字键选择选项会立即总结，无需说明。

> [!NOTE]
>
> 总结将您保持在同一会话中并压缩上下文，类似于有针对性的 `/compact`。要尝试不同的方法，同时保持原始会话完整，请改用 [`/branch`](https://code.claude.com/docs/zh-CN/sessions#branch-a-session) 或 `claude --continue --fork-session`。

## 常见用例

Checkpoints 在以下情况下特别有用：

* **探索替代方案**：尝试不同的实现方法，而不会丢失起点
* **从错误中恢复**：快速撤销引入错误或破坏功能的更改
* **迭代功能**：进行变体实验，知道您可以恢复到工作状态
* **释放上下文空间**：从中点开始总结冗长的调试会话，保持初始说明完整

## 限制

### Bash 命令更改未跟踪

一旦 Claude 在您的对话中使用其文件编辑工具编辑过某个文件，`/rewind` 就会撤销之后 Bash 命令对该文件所做的更改。仅由 Bash 命令更改过的文件不会被跟踪，并保持原样。要还原此类文件，请使用版本控制，例如 Git。

在每条提示词下，回溯菜单会统计对 Claude 已编辑过的文件所做的更改，无论这些更改由什么产生。如果某条提示词中有 shell 命令更改了此类文件，该提示词同样会列出文件更改。

### 子代理编辑未恢复

[子代理](https://code.claude.com/docs/zh-CN/sub-agents.md)使用 Claude 的文件编辑工具进行编辑，但 Claude Code 通常不会在您的会话检查点中捕获这些编辑。回溯是否恢复这些编辑取决于子代理的运行方式：

* **前台分叉技能**：[具有 `context: fork` 的技能](https://code.claude.com/docs/zh-CN/skills#run-skills-in-a-subagent)在前台运行，在您自己的回合期间编辑您的工作树，因此回溯会照常恢复其编辑。设置 `background: false` 以在前台运行分叉；有几种情况（[列在技能页面上](https://code.claude.com/docs/zh-CN/skills.md#run-skills-in-a-subagent)）无论设置如何都会在那里运行。
* **任何其他子代理**：回溯只会恢复 Claude 已在您的对话中编辑过的文件。子代理对其他文件的编辑会保留，因此请使用版本控制（例如 Git）来还原它们。这包括在后台运行的分叉 skill（默认设置）和后台 [`/code-review --fix`](https://code.claude.com/docs/zh-CN/code-review-local) 运行。

### 外部更改未跟踪

Checkpointing 仅跟踪在当前会话中编辑过的文件。您在 Claude Code 外部对文件所做的手动更改以及来自其他并发会话的编辑通常不会被捕获，除非它们碰巧修改了与当前会话相同的文件。

### 中途发送的消息未检查点

在回溯菜单中，您[在 Claude 仍在工作时输入的](https://code.claude.com/docs/zh-CN/interactive-mode.md#queue-messages-while-claude-works)消息可能会被标记为 **No code restore**。Claude 在其轮次结束之前读取了该消息。[检查点是为启动轮次的提示词创建的](#how-checkpoints-work)，因此该消息没有属于自己的检查点。Claude 在读取该消息之后所做的编辑会计入启动该轮次的提示词。

您无需对该消息本身做任何处理。要撤销会话中那部分的文件更改，请选择启动该轮次的提示词，然后选择 **Restore code** 或 **Restore code and conversation**。这会还原 Claude 在整个轮次中所做的文件编辑，包括您的消息到达之前所做的编辑。选择被标记的消息时仍会提供 **Restore conversation**，它会将对话回溯到该消息，并保持您的文件不变。

### 符号链接和硬链接路径未恢复

检查点功能不会回溯符号链接或硬链接文件。当您从 `/rewind` 菜单中选择 **Restore code** 或 **Restore code and conversation** 时，Claude Code 会跳过任何是符号链接或硬链接的跟踪路径，并显示 `Restored the code, but skipped N files` 警告。跳过的文件保持其当前内容。要撤销会话对其中一个文件的更改，请要求 Claude 反转编辑或自己编辑文件。dotfile 管理器符号链接到您项目中的配置文件，以及 pnpm 硬链接到位的文件，都属于此类别。

要查看恢复跳过的路径，请在恢复前使用 `/debug` 打开调试日志：`~/.claude/debug/<session-id>.txt` 中的调试日志会列出每个跳过的路径。有关每个跳过原因和恢复步骤，请参阅[错误参考中的 skipped-files 条目](https://code.claude.com/docs/zh-CN/errors.md#restored-the-code-but-skipped-files)。

### 不是版本控制的替代品

Checkpoints 设计用于快速的会话级恢复。对于永久版本历史和协作，继续使用版本控制（例如 Git）进行提交、分支和长期历史。

## 另请参阅

* [Interactive mode](https://code.claude.com/docs/zh-CN/interactive-mode.md) - 快捷键和会话控制
* [Commands](https://code.claude.com/docs/zh-CN/commands.md) - 使用 `/rewind` 访问 checkpoints
* [CLI reference](https://code.claude.com/docs/zh-CN/cli-reference.md) - 命令行选项
