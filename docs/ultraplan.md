> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用 ultraplan 在云端规划

> 从 CLI 启动计划，在网络上的 Claude Code 中草拟，然后远程执行或在终端中执行

<Note>
  Ultraplan 处于研究预览阶段。行为和功能可能会根据反馈而改变。
</Note>

Ultraplan 将规划任务从本地 CLI 交给在 [plan mode](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode) 中运行的 [网络上的 Claude Code](/docs/zh-CN/claude-code-on-the-web) 会话。Claude 在云端草拟计划，同时你可以继续在终端中工作。计划准备好后，你在浏览器中打开它来对特定部分进行评论、请求修订，并选择在何处执行。

当你需要比终端提供的更丰富的审查界面时，这很有用：

* **有针对性的反馈**：对计划的各个部分进行评论，而不是回复整个计划
* **无需干预的草拟**：计划在远程生成，所以你的终端可以自由用于其他工作
* **灵活的执行**：批准计划在网络上运行并打开拉取请求，或将其发送回终端

Ultraplan 需要 [网络上的 Claude Code](/docs/zh-CN/claude-code-on-the-web) 账户和 GitHub 仓库。由于它在 Anthropic 的云基础设施上运行，当使用 Amazon Bedrock、Google Cloud 的 Agent Platform 或 Microsoft Foundry 时不可用。云会话在你账户的默认 [云环境](/docs/zh-CN/claude-code-on-the-web#the-cloud-environment) 中运行。如果你还没有云环境，ultraplan 在首次启动时会自动创建一个。

<h2 id="launch-ultraplan-from-the-cli">
  从 CLI 启动 ultraplan
</h2>

从本地 CLI 会话，你可以通过三种方式启动 ultraplan：

* **命令**：运行 `/ultraplan` 后跟你的提示
* **关键字**：在普通提示中的任何地方包含单词 `ultraplan`
* **从本地计划**：当 Claude 完成本地计划并显示批准对话框时，选择 **No, refine with Ultraplan on Claude Code on the web** 将草稿发送到云端进行进一步迭代

例如，要使用命令规划服务迁移：

```
/ultraplan migrate the auth service from sessions to JWTs
```

命令和关键字路径在启动前打开确认对话框。本地计划路径跳过此对话框，因为该选择已作为确认。如果 [Remote Control](/docs/zh-CN/remote-control) 处于活动状态，当 ultraplan 启动时它会断开连接，因为两个功能都占用 claude.ai/code 界面，一次只能连接一个。

云会话启动后，CLI 的提示输入显示状态指示器，同时云会话工作：

| 状态                             | 含义                     |
| :----------------------------- | :--------------------- |
| `◇ ultraplan`                  | Claude 正在研究你的代码库并草拟计划  |
| `◇ ultraplan needs your input` | Claude 有澄清问题；打开会话链接以响应 |
| `◆ ultraplan ready`            | 计划已准备好在浏览器中审查          |

运行 `/tasks` 并选择 ultraplan 条目以打开详细视图，其中包含会话链接、代理活动和 **Stop ultraplan** 操作。停止会存档云会话并清除指示器；没有任何内容保存到终端。

<h2 id="review-and-revise-the-plan-in-your-browser">
  在浏览器中审查和修订计划
</h2>

当状态更改为 `◆ ultraplan ready` 时，打开会话链接以在 claude.ai 上查看计划。计划出现在专用审查视图中：

* **内联评论**：突出显示任何段落并留下评论供 Claude 处理
* **表情符号反应**：对部分进行反应以表示批准或关注，无需撰写完整评论
* **大纲侧边栏**：在计划的各个部分之间跳转

当你要求 Claude 处理你的评论时，它会修订计划并呈现更新的草稿。你可以根据需要迭代多次，然后选择在何处执行。

<h2 id="choose-where-to-execute">
  选择执行位置
</h2>

当计划看起来正确时，你在浏览器中选择 Claude 是在同一云会话中实现它，还是将其发送回等待的终端。

<h3 id="execute-on-the-web">
  在网络上执行
</h3>

在浏览器中选择 **Approve Claude's plan and start coding** 让 Claude 在同一 Claude Code on the web 会话中实现它。你的终端显示确认，状态指示器清除，工作继续在云端。实现完成后，[审查差异](/docs/zh-CN/claude-code-on-the-web#review-changes) 并从网络界面创建拉取请求。

<h3 id="send-the-plan-back-to-your-terminal">
  将计划发送回终端
</h3>

在浏览器中选择 **Approve plan and teleport back to terminal** 以在本地实现计划，完全访问你的环境。当会话从 CLI 启动且终端仍在轮询时，此选项出现。网络会话被存档，因此它不会继续并行工作。

你的终端在标题为 **Ultraplan approved** 的对话框中显示计划，有三个选项：

* **Implement here**：将计划注入到当前对话中，从你离开的地方继续
* **Start new session**：清除当前对话并仅以计划作为上下文重新开始
* **Cancel**：将计划保存到文件而不执行它；Claude 打印文件路径，以便你稍后可以返回到它

如果你启动新会话，Claude 会在顶部打印 `claude --resume` 命令，以便你稍后可以返回到之前的对话。

<h2 id="related-resources">
  相关资源
</h2>

* [网络上的 Claude Code](/docs/zh-CN/claude-code-on-the-web)：ultraplan 运行的云基础设施
* [Plan mode](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode)：本地会话中规划的工作方式
* [使用 ultrareview 查找错误](/docs/zh-CN/ultrareview)：ultraplan 的代码审查对应物，用于在合并前捕获问题
* [Remote Control](/docs/zh-CN/remote-control)：使用 claude.ai/code 界面与在自己机器上运行的会话
