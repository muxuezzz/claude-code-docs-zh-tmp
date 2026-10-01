> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Checkpointing

> 跟踪、回溯和总结 Claude 的编辑和对话以管理会话状态。

Claude Code 自动跟踪 Claude 在工作时所做的文件编辑，允许您快速撤销更改并回溯到之前的状态，以防任何事情出现偏差。

<h2 id="how-checkpoints-work">
  checkpointing 如何工作
</h2>

当您与 Claude 合作时，checkpointing 会自动捕获每次您发送开始一个回合的提示前代码的状态。

<h3 id="automatic-tracking">
  自动跟踪
</h3>

Claude Code 跟踪其文件编辑工具所做的所有更改：

* 每个您发送的开始一个回合的提示都会创建一个新的 checkpoint
* Claude Code 在一个会话中保留最近 100 个 checkpoint 的文件快照。丢弃较旧的 checkpoint 会删除没有其他 checkpoint 引用的快照文件，除了每个文件的第一个快照，VS Code 扩展将其用作会话 diffs 的基线。
* Claude Code 将 checkpoints 与对话一起保存，因此您可以在恢复会话后仍然运行 `/rewind`
* Claude Code 在 [retention sweep](/docs/zh-CN/claude-directory#cleaned-up-automatically) 中删除会话的文件快照，默认情况下在会话最后一次保存后约 30 天。回溯到快照已消失的 checkpoint 可能会失败，出现 [`No files were restored`](/docs/zh-CN/errors#no-files-were-restored) 错误。要保留快照更长时间，请设置 [`cleanupPeriodDays`](/docs/zh-CN/settings-reference#cleanupperioddays)。

<h3 id="rewind-and-summarize">
  回溯和总结
</h3>

运行 `/rewind`，或在提示输入为空时按两次 `Esc`，打开回溯菜单。

<Note>
  如果提示输入包含文本，双 `Esc` 会清除它而不是打开菜单。清除的文本会保存到您的输入历史记录中，因此在您完成回溯菜单后，按 `Up` 可以调用它。
</Note>

回溯菜单列出了您在会话期间发送的每个提示，除了 [在回合中途发送的消息](#messages-sent-mid-turn-not-checkpointed)。选择您想要操作的点，然后选择一个操作：

* **恢复代码和对话**：将代码和对话都恢复到该点
* **恢复对话**：回溯到该消息，同时保持当前代码
* **恢复代码**：恢复文件更改，同时保持对话
* **从此处总结**：将此点之后的对话压缩为摘要，释放 context window 空间
* **到此处总结**：将此点之前的对话压缩为摘要，保持后续消息完整
* **算了**：返回消息列表而不做任何更改

两个代码恢复选项仅在所选 checkpoint 具有要恢复的跟踪文件更改时出现。如果该点之后没有捕获文件编辑，菜单仅提供 **恢复对话**、总结选项和 **算了**。

恢复对话或选择"从此处总结"后，所选消息的原始提示会恢复到输入字段中，以便您可以重新发送或编辑它。

选择"到此处总结"会让您留在对话末尾，输入字段为空。使用任一总结选项，**总结的对话** 标记会出现在对话中压缩消息的位置。

<h4 id="rewind-past-a-cleared-conversation">
  回溯过去已清除的对话
</h4>

如果您在同一 Claude Code 进程中较早运行了 `/clear`，回溯菜单会在列表顶部显示一个额外的条目，标记为 `/resume <session-id> (previous session)`。选择它可以恢复在 `/clear` 运行前活跃的对话。该条目在您退出 Claude Code 或恢复不同会话之前可用。

<h4 id="guide-a-summary">
  指导总结
</h4>

总结不会改变磁盘上的文件，原始消息保留在会话记录中，因此 Claude 仍然可以参考详细信息。要指导总结的重点，用箭头键突出显示 **总结** 选项，并在行显示 **add context (optional)** 的位置输入说明，然后按 `Enter`。用其数字键选择选项会立即总结，无需说明。

<Note>
  总结将您保持在同一会话中并压缩上下文，类似于有针对性的 `/compact`。要尝试不同的方法，同时保持原始会话完整，请改用 [`/branch`](/docs/zh-CN/sessions#branch-a-session) 或 `claude --continue --fork-session`。
</Note>

<h2 id="common-use-cases">
  常见用例
</h2>

Checkpoints 在以下情况下特别有用：

* **探索替代方案**：尝试不同的实现方法，而不会丢失起点
* **从错误中恢复**：快速撤销引入错误或破坏功能的更改
* **迭代功能**：进行变体实验，知道您可以恢复到工作状态
* **释放上下文空间**：从中点开始总结冗长的调试会话，保持初始说明完整

<h2 id="limitations">
  限制
</h2>

<h3 id="bash-command-changes-not-tracked">
  Bash 命令更改未跟踪
</h3>

Checkpointing 不跟踪由 Bash 命令修改的文件。例如，如果 Claude Code 运行：

```bash theme={null}
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

这些文件修改无法通过回溯撤销。只有通过 Claude 的文件编辑工具进行的直接文件编辑才会被跟踪。

<h3 id="subagent-edits-not-restored">
  子代理编辑未恢复
</h3>

[子代理](/docs/zh-CN/sub-agents)使用 Claude 的文件编辑工具进行编辑，但 Claude Code 通常不会在您的会话检查点中捕获这些编辑。回溯是否恢复这些编辑取决于子代理的运行方式：

* **前台分叉技能**：[具有 `context: fork` 的技能](/docs/zh-CN/skills#run-skills-in-a-subagent)在前台运行，在您自己的回合期间编辑您的工作树，因此回溯会照常恢复其编辑。设置 `background: false` 以在前台运行分叉；有几种情况（[列在技能页面上](/docs/zh-CN/skills#run-skills-in-a-subagent)）无论设置如何都会在那里运行。
* **任何其他子代理**：回溯不会恢复编辑。使用 git 来还原它们。这包括在后台运行的分叉技能（默认设置）和后台 [`/code-review --fix`](/docs/zh-CN/code-review) 运行。

<h3 id="external-changes-not-tracked">
  外部更改未跟踪
</h3>

Checkpointing 仅跟踪在当前会话中编辑过的文件。您在 Claude Code 外部对文件所做的手动更改以及来自其他并发会话的编辑通常不会被捕获，除非它们碰巧修改了与当前会话相同的文件。

<h3 id="messages-sent-mid-turn-not-checkpointed">
  中途发送的消息未检查点
</h3>

当您在 Claude 工作时[排队的消息](/docs/zh-CN/interactive-mode#queue-messages-while-claude-works)在运行的回合中到达 Claude 时，它会加入该回合而不是开始新的回合。该消息会出现在对话中，但 Claude Code 不会为其创建检查点，回溯菜单也不会列出它。Claude Code 作为其自己的回合发送的排队消息会照常获得检查点，包括当多个排队消息[共享该回合](/docs/zh-CN/interactive-mode#when-claude-code-sends-what-you-queued)时。

要删除此类消息或撤销 Claude 在其后所做的编辑，请回溯到启动该回合的提示。这会回溯整个回合，包括 Claude 在您的消息到达之前所做的工作。

<h3 id="symlinked-and-hard-linked-paths-not-restored">
  符号链接和硬链接路径未恢复
</h3>

Checkpointing 不会回溯符号链接或硬链接文件。当您从 `/rewind` 菜单中选择**恢复代码**或**恢复代码和对话**时，Claude Code 会跳过任何是符号链接或硬链接的跟踪路径，并显示 `已恢复代码，但跳过了 N 个文件` 警告。跳过的文件保持其当前内容。要撤销会话对其中一个文件的更改，请要求 Claude 反转编辑或自己编辑文件。配置文件（dotfile 管理器符号链接到您的项目中的文件）和 pnpm 硬链接到位的文件都属于此类别。

要查看恢复跳过的路径，请在恢复前使用 `/debug` 打开调试日志：`~/.claude/debug/<session-id>.txt` 中的调试日志会列出每个跳过的路径。有关每个跳过原因和恢复步骤，请参阅[错误参考中的 skipped-files 条目](/docs/zh-CN/errors#restored-the-code-but-skipped-files)。

<h3 id="not-a-replacement-for-version-control">
  不是版本控制的替代品
</h3>

Checkpoints 设计用于快速的会话级恢复。对于永久版本历史和协作，继续使用版本控制（例如 Git）进行提交、分支和长期历史。

<h2 id="see-also">
  另请参阅
</h2>

* [Interactive mode](/docs/zh-CN/interactive-mode) - 快捷键和会话控制
* [Commands](/docs/zh-CN/commands) - 使用 `/rewind` 访问 checkpoints
* [CLI reference](/docs/zh-CN/cli-reference) - 命令行选项
