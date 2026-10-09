> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 在 VS Code 中使用 Claude Code

> 安装和配置 VS Code 的 Claude Code 扩展。获得 AI 编码协助，包括内联差异、@-提及、计划审查和快捷键。

<img src="https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=300652d5678c63905e6b0ea9e50835f8" alt="VS Code 编辑器，右侧打开 Claude Code 扩展面板，显示与 Claude 的对话" width="2500" height="1155" data-path="images/vs-code-extension-interface.jpg" />

VS Code 扩展为 Claude Code 提供了原生图形界面，直接集成到您的 IDE 中。这是在 VS Code 中使用 Claude Code 的推荐方式。

使用该扩展，您可以在接受 Claude 的计划之前审查和编辑它们、在进行编辑时自动接受、@-提及具有特定行范围的文件、访问对话历史记录，以及在单独的选项卡或窗口中打开多个对话。

<h2 id="prerequisites">
  前置条件
</h2>

安装前，请确保您拥有：

* VS Code 1.94.0 或更高版本
* Anthropic 账户：任何付费 Claude 订阅（Pro、Max、Team 或 Enterprise）或 Claude Console 账户都可以使用，无需 API 密钥。首次打开扩展时，您将[使用此账户登录](/docs/zh-CN/authentication#log-in-to-claude-code)。如果您通过第三方提供商（如 Amazon Bedrock 或 Google Cloud 的 Agent Platform）访问 Claude，请参阅[使用第三方提供商](#use-third-party-providers)了解设置说明。

<Tip>
  该扩展包含其自己的 CLI（命令行界面）副本用于聊天面板。要在 VS Code 的集成终端中运行 `claude`，您还需要[独立 CLI 安装](/docs/zh-CN/setup)。有关详细信息，请参阅 [VS Code 扩展与 Claude Code CLI](#vs-code-extension-vs-claude-code-cli)。
</Tip>

<h2 id="install-the-extension">
  安装扩展
</h2>

点击您的 IDE 的链接以直接安装：

* [为 VS Code 安装](vscode:extension/anthropic.claude-code)
* [为 Cursor 安装](cursor:extension/anthropic.claude-code)

或在 VS Code 中，按 `Cmd+Shift+X`（Mac）或 `Ctrl+Shift+X`（Windows/Linux）打开扩展视图，搜索"Claude Code"，然后点击**安装**。

扩展的版本号即其捆绑的 Claude Code 版本。例如，需要 Claude Code v2.1.286 或更高版本的功能，需要 2.1.286 或更高版本的扩展，扩展视图中会显示该版本号。

该扩展也可以安装在其他 VS Code 分支中，如 Devin Desktop 或 Kiro。在编辑器的扩展视图中搜索"Claude Code"，或从 [Open VSX 注册表](https://open-vsx.org/extension/Anthropic/claude-code) 安装。如果您的编辑器无法安装该扩展，请[安装 CLI](/docs/zh-CN/quickstart) 并在其集成终端中运行 `claude`。CLI 可在任何终端中使用。

要在开发容器中运行 Claude Code，请参阅[开发容器](/docs/zh-CN/devcontainer)。

<Note>如果安装后扩展没有出现，请重启 VS Code 或从命令面板运行"Developer: Reload Window"。</Note>

<h2 id="get-started">
  开始使用
</h2>

安装后，您可以通过 VS Code 界面开始使用 Claude Code：

<Steps>
  <Step title="打开 Claude Code 面板">
    在整个 VS Code 中，Spark 图标表示 Claude Code：<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/vs-code-spark-icon.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=3ca45e00deadec8c8f4b4f807da94505" alt="Spark icon" style={{display: "inline", height: "0.85em", verticalAlign: "middle"}} width="16" height="16" data-path="images/vs-code-spark-icon.svg" />

    打开 Claude 的最快方法是点击编辑器右上角**编辑器工具栏**中的 Spark 图标。只有当您打开了文件时，该图标才会出现。

    <img src="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=eb4540325d94664c51776dbbfec4cf02" alt="VS Code 编辑器显示编辑器工具栏中的 Spark 图标" width="2796" height="734" data-path="images/vs-code-editor-icon.png" />

    打开 Claude Code 的其他方式：

    * **活动栏**：点击左侧边栏中的 Spark 图标以打开会话列表。点击任何会话以在您的[首选位置](#extension-settings)中打开它，或开始新的会话。此图标在活动栏中始终可见。
    * **命令面板**：`Cmd+Shift+P`（Mac）或 `Ctrl+Shift+P`（Windows/Linux），输入"Claude Code"，然后选择一个选项，如"在新选项卡中打开"
    * **状态栏**：点击窗口右下角的 **✻ Claude Code**。即使没有打开文件，这也有效。

    您可以拖动 Claude 面板以在 VS Code 中的任何位置重新定位它。有关详细信息，请参阅[自定义您的工作流](#customize-your-workflow)。
  </Step>

  <Step title="登录">
    第一次打开面板时，会出现登录屏幕。点击**登录**并在浏览器中完成授权。

    如果您稍后看到**未登录 · 请运行 /login**，扩展程序会自动重新打开登录屏幕。如果它没有出现，请从命令面板使用**开发者：重新加载窗口**重新加载窗口。

    如果您在 shell 中设置了 `ANTHROPIC_API_KEY` 但仍然看到登录提示，VS Code 可能没有继承您的 shell 环境。从终端使用 `code .` 启动 VS Code，以便它继承您的环境变量，或改为使用您的 Claude 账户登录。

    登录后，会出现**学习 Claude Code** 检查清单。通过点击**显示给我**来完成每一项，或使用 X 关闭它。要稍后重新打开它，请在 VS Code 设置中的扩展程序 → Claude Code 下取消选中**隐藏入门**。
  </Step>

  <Step title="发送提示">
    要求 Claude 帮助您处理代码或文件，无论是解释某些内容的工作原理、调试问题还是进行更改。

    <Tip>Claude 会自动看到您选择的文本。按 `Option+K`（Mac）/ `Alt+K`（Windows/Linux）也可以在您的提示中插入 @-mention 引用（如 `@file.ts#5-10`）。</Tip>

    以下是询问文件中特定行的示例：

    <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=ede3ed8d8d5f940e01c5de636d009cfd" alt="VS Code 编辑器，在 Python 文件中选择了第 2-3 行，Claude Code 面板显示关于这些行的问题，带有 @-mention 引用" width="3288" height="1876" data-path="images/vs-code-send-prompt.png" />
  </Step>

  <Step title="审查更改">
    您看到的内容取决于提示框底部显示的[权限模式](/docs/zh-CN/permission-modes#which-mode-a-session-starts-in)：

    * 在自动或自动编辑模式下，Claude 在不询问的情况下编辑工作区中的大多数文件。
    * 在手动模式下，当 Claude 想要编辑文件时，它会显示原始内容和建议更改的并排比较，然后要求权限。您可以接受、拒绝或告诉 Claude 改为做什么。如果您在接受之前直接在差异视图中编辑建议的内容，Claude 会被告知您修改了它，因此它不会假设文件与其原始建议相匹配。

          <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=e005f9b41c541c5c7c59c082f7c4841c" alt="VS Code 显示 Claude 建议更改的差异，以及询问是否进行编辑的权限提示" width="3292" height="1876" data-path="images/vs-code-edits.png" />

    要逐个审查建议的编辑，请使用差异中每个更改下的**接受此更改**和**拒绝此更改**按钮。拒绝更改会在建议的内容中还原它；接受会将其标记为已审查。接受或拒绝整个文件仍会完成审查。具有超过 100 个更改的差异会在没有按更改按钮的情况下打开，因此请将其作为整个文件进行审查。按更改审查需要 Claude Code v2.1.275 或更高版本。

    相同的操作可从编辑器的上下文菜单和命令面板中获得，分别为**Claude Code: Accept Change at Cursor** 和**Claude Code: Reject Change at Cursor**。
  </Step>
</Steps>

有关您可以使用 Claude Code 做什么的更多想法，请参阅[常见工作流](/docs/zh-CN/common-workflows)。

<Tip>
  从命令面板运行"Claude Code: Open Walkthrough"以获得基础知识的引导式教程。
</Tip>

<h2 id="use-the-prompt-box">
  使用输入框
</h2>

输入框支持以下几项功能：

* **权限模式**：点击输入框底部的模式指示器即可切换权限模式。在 Claude Code v2.1.283 或更高版本中，Auto 是内置的初始权限模式；在更早的版本中，仅 Pro、Max 和 Team 套餐如此。请参阅[扩展如何选择初始权限模式](/docs/zh-CN/permission-modes#switch-permission-modes)，了解哪些因素会改变这一点，以及指示器提供的所有权限模式。
  * **Auto**：由分类器审查大多数操作，而不是询问您。请参阅[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)，了解它会审查和阻止哪些操作。
  * **Manual**：Claude 在编辑文件和执行大多数 shell 命令之前会请求权限。
  * **Plan**：Claude 会描述它将要做什么，并在进行更改之前等待批准。VS Code 会自动将计划作为完整的 Markdown 文档打开，您可以在 Claude 开始之前添加行内评论来提供反馈。

    您也可以在输入框中输入 `/plan`。需要 Claude Code v2.1.280 或更高版本。

    * `/plan`：切换到计划模式。如果已处于计划模式，则改为显示当前计划。
    * 带任务的 `/plan`，例如 `/plan fix the auth bug`：切换到计划模式并开始为该任务制定计划。
    * `/plan open`：已处于计划模式时，在编辑器中打开计划文件。
  * **Edit automatically**：Claude 直接进行编辑，不再询问。
* **模型**：从命令菜单中选择 **Switch model…** 即可在会话中途更换模型。您也可以点击输入框底部的模型名称来打开同一个选择器。在 Claude Code v2.1.284 或更高版本中，在输入框中单独输入 `/model` 也会打开该选择器。

  当当前模型支持 [effort 级别](/docs/zh-CN/model-config#adjust-effort-level)时，选择器还会显示 **Effort** 行，模型名称按钮会显示所选级别。当您选择 `max` 以外的级别时，Claude Code 会将其保存为当前模型的默认值，存放在用户设置的 [`modelSettings`](/docs/zh-CN/settings-reference#modelsettings) 下；`max` 仅适用于当前会话。模型名称按钮和 **Effort** 行需要 Claude Code v2.1.257 或更高版本。

  当启用了[动态工作流](/docs/zh-CN/workflows)且当前模型支持时，**Effort** 行下方会出现 **Ultracode** 开关。打开它后，Claude 会以所选 effort 级别，为此会话中的每项实质性任务规划一个[工作流](/docs/zh-CN/workflows#let-claude-decide-with-ultracode)。开关打开期间，模型名称按钮会在级别后显示 `· Ultracode`。该开关需要 Claude Code v2.1.284 或更高版本。
* **命令菜单**：点击 `/` 或输入 `/` 即可打开命令菜单。选项包括附加文件、切换模型以及开关扩展思考。

  Customize 部分包含 MCP 服务器、命令、输出样式、hook、记忆、指令、权限和插件等条目。带有终端图标的条目会在集成终端中打开。

  * 要浏览 `/usage` 或 [`/remote-control`](/docs/zh-CN/remote-control) 等命令，请在 Customize 部分选择 **Slash commands**。对话框会列出这些命令并提供筛选框。选择其中一个即可运行。在输入框中输入 `/` 仍会以内联方式建议命令。需要 Claude Code v2.1.257 或更高版本。

    输入 `/skills` 也会打开此对话框。每个 [skill](/docs/zh-CN/skills) 行都会显示其[可见性](/docs/zh-CN/skills#override-skill-visibility-from-settings)，例如 **On** 或 **Name only**。点击可见性即可更改，但标记为 **locked** 的行（例如插件 skill）除外。`/skills` 快捷方式和可见性控件需要 Claude Code v2.1.280 或更高版本。
  * 在 Customize 部分选择 **Output styles** 即可选择[输出样式](/docs/zh-CN/output-styles)，包括您的自定义样式。需要 Claude Code v2.1.257 或更高版本。

    若要创建自定义样式，请从 **Output styles** 菜单中选择 **Build a custom style**。Claude Code 会在项目级或用户级为您编写[样式文件](/docs/zh-CN/output-styles#create-a-custom-output-style)。需要 Claude Code v2.1.261 或更高版本。
  * 在 Customize 部分选择 **Hooks** 即可查看会话中加载的 [hook](/docs/zh-CN/hooks)，按事件分组。您可以添加、编辑或删除保存在用户、项目和本地设置文件中的 hook。来自其他来源（例如托管设置或插件）的 hook 是只读的。需要 Claude Code v2.1.269 或更高版本。
  * 在 Customize 部分选择 **Permissions** 即可查看会话的[权限规则](/docs/zh-CN/permissions)，分为 Allow、Ask 和 Deny 三组。您可以向用户、项目或本地设置添加规则，并删除保存在其中的规则。来自其他来源的规则（例如托管设置或仅对本会话做出的批准）是只读的。需要 Claude Code v2.1.269 或更高版本。
  * 在 Customize 部分选择 **Memory** 即可打开或关闭[自动记忆](/docs/zh-CN/memory#auto-memory)。打开时，您还可以浏览 Claude 已保存的记忆，并在文件管理器中显示存储这些记忆的文件夹。需要 Claude Code v2.1.274 或更高版本。

    点击已保存的记忆即可在对话框中阅读，您可以在其中编辑文本、删除该记忆，或在编辑器中打开其文件。在对话框中查看、编辑和删除记忆需要 Claude Code v2.1.275 或更高版本。
  * 在 Customize 部分选择 **Instructions** 即可编辑 Claude 读取的 [CLAUDE.md 文件](/docs/zh-CN/memory#claude-md-files)。选择一个文件即可在编辑器中打开。如果该文件尚不存在，Claude Code 会先创建它。需要 Claude Code v2.1.274 或更高版本。
  * 在 Customize 部分选择 **Status**，或输入 `/status`，即可查看会话的 Claude Code 版本、账户、模型和 MCP 服务器详细信息。需要 Claude Code v2.1.280 或更高版本。
  * 在 Customize 部分选择 **Sandbox**，或输入 `/sandbox`，即可查看 Claude 的 Bash 命令是否在[沙箱中](/docs/zh-CN/sandboxing)运行。您可以在此切换沙箱模式并添加[排除的命令](/docs/zh-CN/settings-reference#sandbox-excludedcommands)。需要 Claude Code v2.1.280 或更高版本。
  * 在 Customize 部分选择 **Claude in Chrome**，或输入 `/chrome`，即可检查和管理 [Claude in Chrome](/docs/zh-CN/chrome) 连接。两者都需要使用 claude.ai 账户登录。需要 Claude Code v2.1.280 或更高版本。
  * 在 Context 部分选择 **Export conversation**，或输入 `/export`，即可将对话复制为纯文本或保存到文件。添加文件名（例如 `/export notes.txt`）可跳过对话框并选择文件的保存位置。需要 Claude Code v2.1.280 或更高版本。
  * Settings 部分包含 **Enable Remote Control for all sessions**，它会设置 [`remoteControlAtStartup`](/docs/zh-CN/settings-reference#remotecontrolatstartup)，用于控制[新的交互式会话是否自动连接到 Remote Control](/docs/zh-CN/remote-control#enable-remote-control-for-all-sessions)。需要 Claude Code v2.1.203 或更高版本。

    当您在某个 VS Code 窗口中打开或关闭此开关时，更改会应用于该 VS Code 窗口中已打开的会话，而不仅仅是之后启动的会话。如果关闭它，已打开的会话会断开连接。在 Claude Code v2.1.261 或更高版本中，更改还会同步到您其他 VS Code 窗口中打开的会话。
  * Settings 部分还包含 **Focus view**，它会将工具调用、工具结果和思考内容隐藏在可展开的行后面，只保留您的提示词和 Claude 的回复。您可以在此处切换，也可以使用 `Ctrl+Option+F`（Mac）/ `Ctrl+Alt+F`（Windows/Linux），或在命令面板中使用 **Claude Code: Toggle Focus view**。更改会应用于所有已打开的会话，并在会话之间保留。需要 Claude Code v2.1.221 或更高版本。

    Claude 最新的待办事项列表会保持可见，Claude 待回答问题所针对的文本也会保持可见；这需要 Claude Code v2.1.225 或更高版本。当 Claude 运行[子代理](/docs/zh-CN/sub-agents)时，显示其最新活动的实时进度行会出现在启动它们的工具调用组下方。这需要 Claude Code v2.1.269 或更高版本。
  * 要退出您的 Anthropic 账户，请在 Settings 部分选择 **Sign out**，或输入 `/logout`。使用[第三方提供商](#use-third-party-providers)时，菜单不提供这两种方式。需要 Claude Code v2.1.277 或更高版本。
  * 要报告 bug，请点击菜单底部的 **Report a problem**，或输入 `/bug` 或 `/feedback`，并可附带一段描述来预填报告。当您提交报告且通过第一方连接登录了 Anthropic 时，Claude Code 会将报告发送给 Anthropic。需要 Claude Code v2.1.229 或更高版本。

    使用第三方提供商或没有 Anthropic 凭据时，不会发送任何内容。对话框会在您填写之前说明这一点。提交后，报告会保存为[位于 `~/.claude/feedback-bundles/` 下的本地归档](/docs/zh-CN/data-usage#telemetry-services)，其中已知的 API 密钥和令牌模式会被遮盖。请将该文件发送给您的 Anthropic 客户代表，或将其附加到支持请求中。确认信息会显示文件名，并包含 **Show folder** 按钮。在您的计算机上保存报告需要 Claude Code v2.1.284 或更高版本。

    如果您组织的策略关闭了产品反馈，菜单中不会出现 **Report a problem**，并且 `/bug` 和 `/feedback` 会显示 `Feedback is turned off by your organization's policy or this environment's settings.` 提示，而不是打开报告。在 Claude Code v2.1.284 或更高版本中，如果您设置了 `DISABLE_FEEDBACK_COMMAND` 或 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 环境变量，反馈也会被关闭，打开报告时会改为显示该提示。
* **旁支问题**：输入 `/btw` 后跟一个问题，即可就会话提问，且[不会添加到对话中](/docs/zh-CN/interactive-mode#side-questions-with-%2Fbtw)。回答会在聊天旁边的面板中打开，您可以在其中继续追问。该线程在窗口重新加载后仍会保留。Claude Code 会保留最新的 20 次交流，并按照 [`cleanupPeriodDays`](/docs/zh-CN/settings-reference#cleanupperioddays) 的计划使已存储的线程过期，前提是 Claude Code 能够[安全地确定保留期限](/docs/zh-CN/claude-directory#cleaned-up-automatically)。要清除线程，请点击面板中的垃圾桶图标。需要 Claude Code v2.1.227 或更高版本。
* **复制回复**：将鼠标悬停在某条回复上并点击 **Copy response** 即可将其复制到剪贴板，或输入 `/copy` 复制最新的回复。`/copy 2` 会复制倒数第二条。需要 Claude Code v2.1.277 或更高版本。
* **书签**：将鼠标悬停在某条回复上并点击 **Bookmark response** 即可保存它，或在已保存的回复上点击 **Remove bookmark** 将其移除。

  要查看已保存的回复，请打开 Bookmarks 面板：点击 Claude Code 面板顶部的书签图标，在命令菜单的 Context 部分中选择 **Bookmarks**，或输入 `/bookmarks`。需要 Claude Code v2.1.286 或更高版本。
* **上下文指示器**：输入框会显示您已使用了 Claude 上下文窗口的多少。Claude 会在需要时自动压缩，您也可以手动运行 `/compact`。
* **提示缓存时钟**：上下文指示器旁边的时钟图标会估算对话的[提示缓存](/docs/zh-CN/prompt-caching)在过期前还剩多少时间。它会从缓存的五分钟或一小时[生命周期](/docs/zh-CN/prompt-caching#cache-lifetime)开始倒计时，每次使用缓存的响应都会重新开始倒计时。除压缩外，[使缓存失效的操作](/docs/zh-CN/prompt-caching#actions-that-invalidate-the-cache)不会重置时钟，因此在您切换模型后它仍可能显示剩余分钟数。
  * 在倒计时结束之前，图标会显示剩余分钟数，例如 **12m**。
  * 倒计时结束时，分钟数会消失，图标会变为红色（或您主题的错误颜色），直到下一次响应。此时缓存很可能已经过期，因此在缓存重建期间，您下一条消息的响应会更慢、更昂贵。如果五分钟的生命周期总是在您发送消息的间隔中耗尽，请参阅[自行选择 TTL](/docs/zh-CN/prompt-caching#choose-the-ttl-yourself)。
  * 在对话刚刚[压缩](/docs/zh-CN/prompt-caching#compacting-the-conversation)之后，图标也会变为红色且不显示分钟数，直到下一次响应，因为缓存尚未覆盖压缩后的对话。
* **Agent 地图**：当对话包含[子代理](/docs/zh-CN/sub-agents)时，输入框底部会出现 Agent 计数，例如 **2 agents**。其圆点显示是否有子代理正在工作或正在等待您授予权限。

  点击 Agent 计数即可打开 Agent 地图，它会将对话的子代理以树状形式绘制在主 Agent 之下，每个子代理都显示其状态、已用时间和 token 数。点击某个子代理即可查看其提示词和工具调用、打开其只读会话记录，或在其运行时停止它。需要 Claude Code v2.1.269 或更高版本。

  地图还会在 Agent 下方列出会话的其他[后台任务](/docs/zh-CN/tools-reference#background-commands)，例如后台 shell 命令和[监视器](/docs/zh-CN/tools-reference#monitor-tool)。点击某一行即可打开该任务的卡片并在其中停止它。

  当没有显示 Agent 计数时（例如 Claude 启动了后台 shell 但没有子代理），要打开地图，请在输入框中输入 `/tasks`。地图中的后台任务以及输入 `/tasks` 需要 Claude Code v2.1.277 或更高版本。

  在 Claude Code v2.1.286 或更高版本中，当您点击 **Stop** 或按 `Esc` 时，当前轮次会结束。后台 Agent 会继续运行，直到完成或您从地图中将其停止。
* **扩展思考**：让 Claude 花更多时间推理复杂问题。通过命令菜单（`/`）将其打开。Claude 的推理会以折叠块的形式出现在对话中：点击某个块即可阅读，或按 `Ctrl+O` 展开或折叠会话中的所有思考块。详情请参阅[扩展思考](/docs/zh-CN/model-config#extended-thinking)。
* **多行输入**：按 `Shift+Enter` 可添加新行而不发送。这同样适用于问题对话框中的“Other”自由文本输入。

<h3 id="reference-files-and-folders">
  引用文件和文件夹
</h3>

使用 @ 提及为 Claude 提供有关特定文件或文件夹的上下文。当您输入 `@` 后跟文件或文件夹名称时，Claude 会读取该内容，并可以回答有关它的问题或对其进行更改。Claude Code 支持模糊匹配，因此您可以输入部分名称来找到所需内容：

```text wrap theme={null}
Explain the logic in @auth (fuzzy matches auth.js, AuthService.ts, etc.)
What's in @src/components/ (include a trailing slash for folders)
```

对于大型 PDF，您可以让 Claude 读取特定页面而不是整个文件：单个页面、像第 1-10 页这样的范围，或像第 3 页及之后这样的开放范围。读取特定页面需要在运行 Claude Code 的机器上安装 [poppler-utils](/docs/zh-CN/tools-reference#read-tool-behavior)。

当您在编辑器中选择文本时，Claude 可以自动看到您高亮的代码。输入框底部会显示选中了多少行。按 `Option+K`（Mac）/ `Alt+K`（Windows/Linux）可插入带有文件路径和行号的 @ 提及（例如 `@app.ts#5-10`）。点击选区指示器上的 **X** 可将其移除，这样 Claude 就不会收到该选区。当您选择其他文本时，指示器会重新出现。

扩展会对某些文件隐瞒所选文本。当文件位于您的工作区内且匹配您的 `files.exclude` 或 `search.exclude` 设置时，Claude 最多只会收到该文件的路径，而不会收到您选择的文本。对于 git 忽略的文件也是如此，前提是 VS Code 的 `search.useIgnoreFiles` 设置和扩展的 [`respectGitIgnore` 设置](#extension-settings)都已打开（默认即为打开）。此过滤仅适用于聊天面板：当 Claude Code 在集成终端中运行时，无论是什么文件，CLI 都会发送您选择的文本，因此若要在那里阻止 Claude 获取某个文件的内容，请添加 [`Read` 拒绝规则](#the-built-in-ide-mcp-server)。

即使没有选择任何内容，Claude 也能看到您在编辑器中打开的是哪个文件，输入框会显示其名称。若只想添加您选择的文本，请关闭 [Attach Open File 设置](vscode://settings/claudeCode.attachOpenFile)。该设置需要 Claude Code v2.1.271 或更高版本。

您还可以在消息中附加图片和文件：

* 要附加图片，请将其从剪贴板粘贴到输入框中。
* 要附加文件，请按住 `Shift` 将其拖入输入框。
* 要从上下文中移除附件，请点击其上的 X。

<h3 id="paste-text">
  粘贴文本
</h3>

您粘贴的文本会在输入框中保持可见，而不会像[在终端中](/docs/zh-CN/terminal-config#paste-large-content)那样折叠为占位符。在 Claude Code [标记粘贴文本](/docs/zh-CN/terminal-config#how-claude-treats-pasted-text)的会话中，Claude 仍会将大段粘贴内容视为您粘贴的文本，而不是您输入的文本。

Claude Code 还会从您粘贴到输入框中的文本以及您发送的任何其他内容中移除[不可见的 Unicode 字符](/docs/zh-CN/interactive-mode#invisible-characters-in-prompts)：

* 如果粘贴时出现 `Removed 3 invisible characters from the pasted text` 之类的提示，说明文本已在去除这些字符后输入。
* 如果发送时出现有关已移除字符的提示，说明没有发送任何内容。清理后的文本已回到输入框中。再次发送即可按所示内容发送文本。

<h3 id="resume-past-conversations">
  恢复过去的对话
</h3>

点击 Claude Code 面板顶部的 **Session history** 按钮即可访问您的对话历史。您可以按关键字搜索或按时间浏览。

点击任意对话即可带着完整的消息历史恢复它。如果该对话已在当前窗口的另一个标签页中打开，点击它会切换到该标签页。有关恢复会话的更多信息，请参阅[管理会话](/docs/zh-CN/sessions)。

* **会话标题**：新会话会根据您的第一条消息获得 AI 生成的标题。
* **重命名和归档**：将鼠标悬停在会话上即可显示这些操作。重命名可为其设置描述性标题，归档则会将其移到列表底部的 **Archived sessions** 组中。

如果该对话在另一个 Claude Code 进程中打开（例如终端中的 `claude` 或另一个 VS Code 窗口），输入框的位置会显示一条提示：`This conversation is still open somewhere else. Using it in two places at once can mix up its messages.` 若要在此处继续，请先在另一处关闭该对话，然后点击 **Open here anyway**。如果不关闭就点击，该对话会在两处同时打开。设置了 [`claudeProcessWrapper`](#extension-settings) 时，扩展会跳过此检查并直接打开对话。

默认情况下，14 天内没有活动的会话会自动移到 **Archived sessions**，除非它处于打开状态、未读或位于某个[组](#organize-sessions-into-groups)中。自动归档需要 Claude Code v2.1.265 或更高版本。要更改期限或将其关闭，请打开 [Archive Inactive Sessions 设置](vscode://settings/claudeCode.archiveInactiveSessions)，然后选择天数或 **Never**。

要恢复已归档的会话，请展开 **Archived sessions** 并点击 **Unarchive session**。要一次性恢复所有已归档的会话，请将鼠标悬停在活动栏会话列表中的 **Archived sessions** 标题上，然后点击其取消归档图标，这需要 Claude Code v2.1.277 或更高版本。在 v2.1.257 之前，该操作是 **Delete session**，它会隐藏会话且无法恢复。升级后，您当时删除的会话会出现在 **Archived sessions** 下。

当您恢复的对话以计划模式结束时，Claude Code 会恢复计划模式。需要 Claude Code v2.1.246 或更高版本。在以下两种情况下，Claude Code 不会恢复计划模式：

* 扩展根据 `claudeCode.initialPermissionMode` 或从先前对话沿用的选择来[选择初始权限模式](/docs/zh-CN/permission-modes#switch-permission-modes)
* 您配置了 `claudeCode.claudeProcessWrapper`

<h3 id="resume-cloud-sessions-from-claude-ai">
  从 Claude.ai 恢复云端会话
</h3>

如果您运行[云端会话](/docs/zh-CN/claude-code-on-the-web)，可以直接在 VS Code 中恢复它们。这需要使用 **Claude.ai Subscription** 登录，而不是 Anthropic Console。

<Steps>
  <Step title="打开会话历史">
    点击 Claude Code 面板顶部的 **Session history** 按钮。
  </Step>

  <Step title="选择 Web 标签页">
    对话框显示两个标签页：Local 和 Web。点击 **Web** 即可查看来自 claude.ai 的会话。
  </Step>

  <Step title="选择要恢复的会话">
    浏览或搜索会话。点击其中一个即可在本地继续对话。
  </Step>
</Steps>

<Note>
  当您打开的文件夹是 GitHub 仓库时，Web 标签页仅显示来自该仓库的会话。

  当您恢复云端会话时，扩展会下载对话历史的副本；更改不会同步回 claude.ai。
</Note>

Web 标签页还会列出您的 [Remote Control](/docs/zh-CN/remote-control) 会话。如果您点击的会话曾在您当前打开的文件夹中运行，扩展会打开该本地对话而不是下载副本，并且如果已有标签页正在显示它，则会聚焦到该标签页。如果扩展无法排除另一个 Claude 进程已打开该对话的可能性，您将获得一份下载的副本。

如果对话的任何部分下载失败，会出现错误且不会保存副本。再次选择该会话即可重试。如果您选择的会话尚无可下载的对话，错误信息会告诉您应在何处继续该会话。

<h3 id="check-account-and-usage">
  查看账户和用量
</h3>

运行 `/usage` 即可打开 Account & usage 对话框。它会显示您已登录的账户，所报告的用量因登录方式而异：

* **claude.ai 套餐**：显示您套餐各项限额的用量条，例如当前会话和本周。每个用量条都会显示距离该限额重置还有多长时间。

  对话框还会细分哪些因素在消耗您的套餐限额。它会标出占近期用量 10% 或以上的行为，例如缓存未命中、长上下文以及大量使用子代理或高度并行的会话，并为每项提供降低用量的建议。归因表会显示每个 skill、子代理、插件和 MCP 服务器各自产生了多少用量。

  使用 Day 和 Week 切换按钮可在过去 24 小时和过去 7 天之间切换。这些数据是根据本机上的本地会话计算得出的近似值，因此不包括来自其他设备或 claude.ai 的用量。
* **其他登录方式**：当套餐限额不适用于您的登录方式时（例如使用[第三方提供商](#use-third-party-providers)或 API 密钥），Usage 部分会改为显示会话自身的费用和 token 用量。CLI 的 `/usage` 会在其 [Session 区块](/docs/zh-CN/costs#track-your-costs)中显示相同的总计。活动栏中的会话列表也会在其 **Account & usage** 标题下显示活动会话的总计。需要 Claude Code v2.1.277 或更高版本。

有关跟踪和降低用量的更多信息，请参阅[跟踪您的费用](/docs/zh-CN/costs#track-your-costs)。

<h2 id="customize-your-workflow">
  自定义您的工作流
</h2>

您可以重新定位 Claude 面板、运行多个对话、将会话列表组织成组或筛选会话列表，或切换到终端模式。

<h3 id="choose-where-claude-lives">
  选择 Claude 的位置
</h3>

您可以拖动 Claude 面板在 VS Code 中重新定位它。抓住面板的选项卡或标题栏并将其拖动到：

* **次级侧边栏**：窗口的右侧。在您编码时保持 Claude 可见。
* **主侧边栏**：左侧边栏，带有 Explorer、Search 等图标。
* **编辑器区域**：将 Claude 作为选项卡打开，与您的文件并排显示。适用于辅助任务。

当 Claude 在新编辑器组中打开选项卡时，该扩展会锁定该组，因此当 Claude 选项卡处于焦点时打开的文件会转到另一个组，而不是在其旁边。

要停止扩展锁定组，请关闭 [Lock Editor Groups setting](vscode://settings/claudeCode.lockEditorGroups)。已锁定的组将保持锁定状态，直到您解锁它们。该设置需要 Claude Code v2.1.274 或更高版本。

<Tip>
  将侧边栏用于您的主要 Claude 会话，并为辅助任务打开其他选项卡。Claude 会记住您首选的位置。Activity Bar 会话列表图标与 Claude 面板分开：会话列表始终在 Activity Bar 中可见，而 Claude 面板图标仅在面板停靠到左侧边栏时才出现在那里。
</Tip>

<h3 id="continue-conversations-after-a-reload">
  重新加载后继续对话
</h3>

运行 **Developer: Reload Window** 或重启 VS Code 后，聊天是否会返回其对话取决于它在哪里打开：

* **编辑器选项卡**：对话会随其选项卡返回。
* **侧边栏**：如果您在过去 10 分钟内发送了消息或 Claude 在其中做出了响应，对话会返回。如果它没有返回，请从 [Session history](#resume-past-conversations) 恢复对话。

如果另一个 Claude Code 进程仍打开着该对话，在此处打开之前会先询问您，显示的 **Open here anyway** 通知与您[从会话历史记录恢复对话](#resume-past-conversations)时相同。

如果重新加载中断了 Claude 的中间步骤，当对话返回时 Claude 会继续该步骤，聊天中的通知会标记该继续。需要 Claude Code v2.1.274 或更高版本。如果步骤在一小时前被中断或会话在其他地方打开，对话会返回为空闲状态。

要关闭继续功能，请打开 [Continue After Reload setting](vscode://settings/claudeCode.continueAfterReload) 并取消勾选它。在 VS Code 的环境中或在 [`environmentVariables` 设置](#extension-settings)中设置 [`CLAUDE_CODE_RESUME_INTERRUPTED_TURN`](/docs/zh-CN/env-vars#variables) 或任何其他 `CLAUDE_CODE_RESUME_` 变量在面板中不起作用，因为扩展会在启动面板的会话之前移除这些变量。

<h3 id="run-multiple-conversations">
  运行多个对话
</h3>

使用命令面板中的 **Open in New Tab** 或 **Open in New Window** 来启动其他对话。每个对话维护其自己的历史记录和上下文，允许您并行处理不同的任务。

使用选项卡时，spark 图标上的小彩色点表示状态：蓝色表示权限请求待处理，橙色表示 Claude 在选项卡隐藏时完成。

<h3 id="organize-sessions-into-groups">
  将会话组织成组
</h3>

在 Activity Bar 的会话列表中，您可以将相关会话收集到命名的、可折叠的组中。需要 Claude Code v2.1.229 或更高版本。

* **对会话进行分组或取消分组**：右键单击会话以从其创建组、将其移动到现有组或将其从其组中删除。每个会话一次只属于一个组，因此将其移动到另一个组会将其从第一个组中删除。
* **一次移动多个会话**：`Cmd`-单击（Mac）/ `Ctrl`-单击（Windows/Linux）每个会话，或 `Shift`-单击以选择范围，然后右键单击选择。
* **从其选项卡对会话进行分组**：从命令面板运行 **Claude Code: Add Session Tab to Group**，然后选择或创建组。需要 Claude Code v2.1.257 或更高版本。
* **重命名或删除组**：右键单击组标题。删除组仅删除组，其会话返回到未分组列表。

该扩展按工作区文件夹保存组，因此它们在窗口重新加载后仍然存在，并在您打开相同文件夹的每个窗口中出现。当您搜索列表时，该扩展在所有组中的一个平面列表中显示匹配项。

<h3 id="filter-the-sessions-list">
  筛选会话列表
</h3>

要缩小 Activity Bar 中的长会话列表，请使用列表顶部的两个筛选控件。需要 Claude Code v2.1.271 或更高版本。启用任一筛选器时，已归档的会话不会显示。

* **Active**：打开此切换开关以仅显示需要您输入、正在工作或未读的会话，以及您最后关注的 Claude 选项卡中的会话。
* **按状态筛选**：单击漏斗图标，然后勾选 **Needs input**、**Working** 或 **Completed** 以显示处于任何这些状态的会话。勾选 **Open** 或 **Closed** 以按会话是否打开来缩小范围。当会话在此窗口中有选项卡或在此计算机上的另一个 Claude Code 进程中运行（例如在终端中）时，会话计为打开。

当 **Active** 打开且您勾选状态、**Open** 或 **Closed** 时，列表还会显示与您的检查匹配的每个会话。您设置的筛选器在窗口重新加载后保持不变。

<h3 id="switch-to-terminal-mode">
  切换到终端模式
</h3>

默认情况下，该扩展打开图形聊天面板。如果您更喜欢 CLI 风格的界面，请打开 [Use Terminal setting](vscode://settings/claudeCode.useTerminal) 并勾选该框。

您也可以打开 VS Code 设置（Mac 上为 `Cmd+,` 或 Windows/Linux 上为 `Ctrl+,`），转到 Extensions → Claude Code，并勾选 **Use Terminal**。

<h2 id="manage-plugins">
  管理插件
</h2>

VS Code 扩展包含一个图形界面，用于安装和管理 [plugins](/docs/zh-CN/plugins/overview)。在提示框中输入 `/plugins` 以打开**管理插件**界面。

<h3 id="install-plugins">
  安装插件
</h3>

插件对话框显示两个选项卡：**Plugins** 和 **Marketplaces**。

在 Plugins 选项卡中：

* **已安装的插件**显示在顶部，带有切换开关以启用或禁用它们。
  * 如果您关闭项目的共享 `.claude/settings.json` 启用的插件，扩展会先询问：**为我禁用**仅为您关闭它，而**为所有人禁用**会更改共享文件。
  * 加载失败的插件会在其行上显示简短原因。点击该原因可查看您可以采取的措施，包括复制完整的错误消息以便在[插件故障排除](/docs/zh-CN/plugins/troubleshooting)中查找。
* **可用插件**来自您配置的市场，显示在下方
* 搜索以按名称或描述过滤插件
* 点击任何可用插件上的**安装**

安装插件时，选择安装范围：

* **为您安装**：在您的所有项目中可用（用户范围）
* **为此项目安装**：与项目协作者共享（项目范围）
* **本地安装**：仅供您使用，仅在此存储库中（本地范围）

安装完成后，表单会要求设置任何尚未设置的插件的 [configuration options](/docs/zh-CN/plugins/components#user-configuration)。要稍后查看或更改选项，请点击插件行上的齿轮图标。

敏感文本字段被掩盖，您之前保存的密钥显示 **(unchanged)**。将字段留空以保持保存的值。

保存更改后，打开的会话会重新加载其插件，对话框显示**重启 Claude 以应用插件更改**。

<h3 id="uninstall-plugins">
  卸载插件
</h3>

每个已安装的行都标明了它安装的 [scope](/docs/zh-CN/plugins/install#choose-an-install-scope)。要卸载该安装，请点击该行的垃圾桶图标。暗淡的垃圾桶图标标记您无法从此工作区卸载的行，例如您的组织管理的插件或为另一个项目安装的插件。

扩展在两种情况下会先询问：

* **项目的共享 `.claude/settings.json` 启用的插件**：选择**为我禁用**，这会为您的协作者保留插件安装，或**为所有人卸载**，这会使用 [`--keep-data`](/docs/zh-CN/plugins/cli-reference#what-an-uninstall-deletes-and-keeps) 删除项目的安装，因此插件的保存数据目录会保留。如果您已经为自己关闭了插件，垃圾桶图标会删除您自己的安装而不会提问。
* **否则，最后一个具有保存数据的插件安装**：选择是否保留或删除数据；**保留**是默认选项

<h3 id="share-a-plugin-install-link">
  分享插件安装链接
</h3>

要直接向某人发送特定插件的安装链接，请给他们扩展的 `install-plugin` URL。打开它会启动或聚焦 VS Code，打开 Claude Code 面板，并在该插件的范围选择上打开**管理插件**对话框。在该人选择范围之前，不会安装任何内容。如果该插件的市场在他们的 Claude Code 中尚未配置，对话框首先会要求他们添加它。

```text theme={null}
vscode://anthropic.claude-code/install-plugin?plugin=code-review&marketplace=anthropics/claude-plugins-official
```

该 URL 接受两个查询参数：

| 参数 | 描述 |
| - | - |
| `plugin` | 插件的名称，如其市场所列。必需。 |
| `marketplace` | 市场的[来源](/docs/zh-CN/plugins/install#add-a-marketplace)：GitHub `owner/repo`、`https://` URL 或 git SSH 地址，例如 `git@github.com:owner/repo.git`。省略时默认为 `anthropics/claude-plugins-official`。 |

扩展在打开任何内容之前会检查这两个值：

* **插件名称**：最多 100 个字符，以 ASCII 字母或数字开头，其余部分只能使用 ASCII 字母、数字、`.`、`_` 和 `-`。
* **市场来源**：只能是 `marketplace` 参数所列出的形式，因此不能是本地路径、`http://` 地址或市场的名称（例如 `claude-plugins-official`）。`https://` URL 不能包含用户名、密码或查询字符串。
* **Git ref**：要将市场固定到某个分支或标签，请在来源后附加 `%23`（`#` 的编码形式）再加上 ref，例如 `marketplace=owner/repo%23v1.0`。包含未编码 `#` 的链接会失败。`anthropics` GitHub 组织中的市场无法在链接中固定。

打开违反这些规则的链接时，用户会看到以 `Invalid plugin installation URL` 开头的错误。Claude Code 面板和对话框不会打开，也不会安装任何内容。如果您的插件名称或市场无法放入链接中，请告知用户在 **Marketplaces** 选项卡中添加该市场，然后从 **Plugins** 选项卡安装插件。

以下情况会在对话框中以消息结束，而不是作用域选择：

* **市场中没有列出该名称的插件**：对话框报告未找到该插件。根据市场的列表检查 `plugin` 值。
* **插件已安装**：对话框会说明这一点，不会发生任何更改。
* **已添加了另一个同名的市场**：对话框会说明链接中的市场未被添加，不会安装任何内容。

GitHub README、问题和某些其他 Markdown 主机会删除其方案不是 `http` 或 `https` 的链接，因此 `vscode://` 链接在那里呈现为纯文本。在这些主机上将 URL 放在代码块中，如 [链接呈现为纯文本而不是可点击的](/docs/zh-CN/deep-links#the-link-renders-as-plain-text-instead-of-being-clickable) 对 `claude-cli://` 链接所描述的那样。

<h3 id="manage-marketplaces">
  管理市场
</h3>

切换到 **Marketplaces** 选项卡以添加或删除插件源：

* 输入 GitHub 仓库、URL 或本地路径以添加新市场
* 点击刷新图标以更新市场的插件列表
* 点击垃圾桶图标以删除市场。删除它会 [卸载您从中安装的每个插件](/docs/zh-CN/plugins/install#manage-marketplaces)，因此确认会首先列出这些插件

您在对话框中所做的插件更改会立即应用到该 VS Code 窗口中打开的 Claude Code 会话。

如果您打开对话框的会话无法重新加载其插件，对话框会提供重试或在该会话中重启 Claude 的选项。

<Note>
  VS Code 中的插件管理在底层使用相同的 CLI 命令。您在扩展中配置的插件和市场也可在 CLI 中使用，反之亦然。
</Note>

有关插件系统的更多信息，请参阅 [Plugins](/docs/zh-CN/plugins/overview) 和 [Plugin marketplaces](/docs/zh-CN/plugins/overview)。

<h2 id="automate-browser-tasks-with-chrome">
  使用 Chrome 自动化浏览器任务
</h2>

将 Claude 连接到您的 Chrome 浏览器，以测试 Web 应用、使用控制台日志进行调试，以及在不离开 VS Code 的情况下自动化浏览器工作流。这需要 [Claude in Chrome 扩展](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) 版本 1.0.36 或更高版本。

在提示框中输入 `@browser`，然后输入您希望 Claude 执行的操作：

```text wrap theme={null}
@browser go to localhost:3000 and check the console for errors
```

您也可以打开附件菜单来选择特定的浏览器工具，例如打开新标签页或读取页面内容。

Claude 为浏览器任务打开新标签页并共享您浏览器的登录状态，因此它可以访问您已登录的任何网站。

如需让每个会话在启动时自动连接到您的浏览器，而无需输入 `@browser`，请参阅[默认启用 Chrome](/docs/zh-CN/chrome#enable-chrome-by-default)。关于在以这种方式连接的会话中，Claude Code 在执行浏览器操作前询问您的情况，请参阅 [VS Code 会话中的权限提示](/docs/zh-CN/chrome#permission-prompts-in-vs-code-sessions)。

有关设置说明、完整的功能列表和故障排除，请参阅 [在 Chrome 中使用 Claude Code](/docs/zh-CN/chrome)。

<h2 id="vs-code-commands-and-shortcuts">
  VS Code 命令和快捷键
</h2>

打开命令面板（Mac 上按 `Cmd+Shift+P` 或 Windows/Linux 上按 `Ctrl+Shift+P`），然后输入"Claude Code"以查看 Claude Code 扩展的所有可用 VS Code 命令。

某些快捷键取决于哪个面板处于"焦点"状态（接收键盘输入）。当光标在代码文件中时，编辑器处于焦点状态。当光标在 Claude 的提示框中时，Claude 处于焦点状态。使用 `Cmd+Esc` / `Ctrl+Esc` 在它们之间切换。

<Note>
  这些是用于控制扩展的 VS Code 命令。并非所有内置 Claude Code 命令都在扩展中可用。有关详细信息，请参阅 [VS Code 扩展与 Claude Code CLI](#vs-code-extension-vs-claude-code-cli)。
</Note>

| 命令 | 快捷键 | 描述 |
| - | - | - |
| Focus Input | `Cmd+Esc` (Mac) / `Ctrl+Esc` (Windows/Linux) | 在编辑器和 Claude 之间切换焦点 |
| Focus last message | - | 将键盘焦点移动到对话中的最新消息，或移动到等待权限提示，以便您可以使用键盘或屏幕阅读器从那里读取。在[终端模式](#switch-to-terminal-mode)中不可用。需要 Claude Code v2.1.268 或更高版本 |
| Open in Side Bar | - | 在侧边栏中打开 Claude |
| Open in Terminal | - | 在终端模式下打开 Claude |
| Open in New Tab | `Cmd+Shift+Esc` (Mac) / `Ctrl+Shift+Esc` (Windows/Linux) | 以编辑器选项卡形式打开新对话 |
| Open in New Window | - | 在单独的窗口中打开新对话 |
| New Conversation | `Cmd+N` (Mac) / `Ctrl+N` (Windows/Linux) | 开始新对话。需要 Claude 处于焦点状态且 `enableNewConversationShortcut` 设置为 `true` |
| Reopen Closed Session | `Cmd+Shift+T` (Mac) / `Ctrl+Shift+T` (Windows/Linux) | 重新打开最近关闭的 Claude 会话选项卡。当最后关闭的选项卡不是 Claude 会话时，会回退到 VS Code 的正常重新打开关闭编辑器功能。使用 `enableReopenClosedSessionShortcut` 禁用 |
| Insert @-Mention Reference | `Option+K` (Mac) / `Alt+K` (Windows/Linux) | 插入对当前文件和选择的引用（需要编辑器处于焦点状态） |
| Accept Change at Cursor | - | 在[审查建议编辑](#get-started)时，一次接受光标处的更改。需要 Claude Code v2.1.275 或更高版本 |
| Reject Change at Cursor | - | 在审查建议编辑时，一次拒绝光标处的更改。需要 Claude Code v2.1.275 或更高版本 |
| Toggle Focus view | `Ctrl+Option+F` (Mac) / `Ctrl+Alt+F` (Windows/Linux) | 隐藏或显示对话中的工具活动。在 Claude 面板或侧边栏可见时有效。需要 Claude Code v2.1.221 或更高版本 |
| Rename Session Tab | - | 重命名活动 Claude 选项卡中的会话。需要 Claude Code v2.1.257 或更高版本 |
| Add Session Tab to Group | - | 将活动 Claude 选项卡中的会话添加到您选择或创建的[会话组](#organize-sessions-into-groups)。需要 Claude Code v2.1.257 或更高版本 |
| Mark Session as Unread | - | 在会话列表中将活动 Claude 选项卡中的会话标记为未读。需要 Claude Code v2.1.257 或更高版本 |
| Show Logs | - | 查看扩展调试日志 |
| Logout | - | 登出您的 Anthropic 账户 |

<h3 id="launch-a-vs-code-tab-from-other-tools">
  从其他工具启动 VS Code 选项卡
</h3>

该扩展在 `vscode://anthropic.claude-code/open` 处注册了一个 URI 处理程序。使用它从您自己的工具（shell 别名、浏览器书签或任何可以打开 URL 的脚本）打开新的 Claude Code 选项卡。如果 VS Code 尚未运行，打开 URL 会先启动它。如果 VS Code 已在运行，URL 会在当前焦点的窗口中打开。

使用您的操作系统的 URL 打开程序调用处理程序。

<Tabs>
  <Tab title="macOS">
    ```bash theme={null}
    open "vscode://anthropic.claude-code/open"
    ```
  </Tab>

  <Tab title="Linux">
    ```bash theme={null}
    xdg-open "vscode://anthropic.claude-code/open"
    ```

    `xdg-open` 命令来自 `xdg-utils` 包。如果 shell 报告找不到它，请参阅 [xdg-open is not found on Linux](/docs/zh-CN/deep-links#xdg-open-is-not-found-on-linux)。
  </Tab>

  <Tab title="Windows">
    在 PowerShell 中：

    ```powershell theme={null}
    Start-Process "vscode://anthropic.claude-code/open"
    ```

    在 `cmd.exe` 中，`start` 将其第一个带引号的参数视为窗口标题，因此在 URL 之前传递一个空标题：

    ```cmd theme={null}
    start "" "vscode://anthropic.claude-code/open"
    ```
  </Tab>
</Tabs>

处理程序接受两个可选查询参数：

| 参数 | 描述 |
| - | - |
| `prompt` | 在提示框中预填充的文本。必须进行 URL 编码。提示框会被预填充但不会自动提交。 |
| `session` | 要恢复的会话 ID，而不是开始新对话。该会话必须属于 VS Code 中当前打开的工作区。如果找不到该会话，则改为开始新对话。如果该会话已在选项卡中打开，则该选项卡会获得焦点。要以编程方式捕获会话 ID，请参阅[继续对话](/docs/zh-CN/headless#continue-conversations)。 |

例如，要打开一个预填充了"review my changes"的选项卡：

```text theme={null}
vscode://anthropic.claude-code/open?prompt=review%20my%20changes
```

该扩展还处理 `vscode://anthropic.claude-code/install-plugin`，它[在一个插件上打开插件对话框](#share-a-plugin-install-link)。要启动终端会话而不是 VS Code 选项卡，请使用 CLI 的 `claude-cli://` 处理程序。请参阅[从链接启动会话](/docs/zh-CN/deep-links)。

<h2 id="configure-settings">
  配置设置
</h2>

该扩展有两种类型的设置：

* **VS Code 中的扩展设置**：控制扩展在 VS Code 中的行为。使用 `Cmd+,`（Mac）或 `Ctrl+,`（Windows/Linux）打开，然后转到扩展 → Claude Code。您也可以输入 `/` 并选择 **General config…** 来打开设置。
* **`~/.claude/settings.json` 中的 Claude Code 设置**：在扩展和 CLI 之间共享。用于允许的命令、环境变量、hooks 和 MCP 服务器。在 Claude Code v2.1.283 或更高版本中，它也是权限模式对话开始时的一个输入，在早期版本中仅在 Pro、Max 和 Team 计划上。[切换权限模式](/docs/zh-CN/permission-modes#switch-permission-modes)列出了顺序。有关详细信息，请参阅[设置](/docs/zh-CN/settings)。

<Tip>
  将 `"$schema": "https://json.schemastore.org/claude-code-settings.json"` 添加到您的 `settings.json` 中，以在 VS Code 中直接获得所有可用设置的自动完成和内联验证。
</Tip>

<h3 id="extension-settings">
  扩展设置
</h3>

VS Code 从您的用户设置中读取 `initialPermissionMode`，并忽略工作区值。在 v2.1.225 之前，VS Code 将该设置默认为 `default` 并应用工作区值。

| 设置 | 默认值 | 描述 |
| - | - | - |
| `useTerminal` | `false` | 在终端模式而不是图形面板中启动 Claude |
| `initialPermissionMode` | - | 控制新对话的批准提示：`default`、`plan`、`acceptEdits` 或 `bypassPermissions`。`manual` 是 `default` 的别名，选择模式指示器中标记为 **Manual** 的模式。当您将其留空时，扩展会选择起始权限模式，如[切换权限模式](/docs/zh-CN/permission-modes#switch-permission-modes)中所述。 |
| `preferredLocation` | `panel` | Claude 打开的位置：`sidebar`（右侧）或 `panel`（新标签页） |
| `lockEditorGroups` | `true` | [锁定 Claude 为其标签页启动的编辑器组](#choose-where-claude-lives)，以便您在 Claude 标签页获得焦点时打开的文件转到另一个组。关闭时，扩展永远不会锁定编辑器组。需要 Claude Code v2.1.274 或更高版本 |
| `autosave` | `true` | Claude 读取或写入文件前自动保存文件 |
| `attachOpenFile` | `true` | 将编辑器中打开的文件添加到您的消息中，并在提示框中显示它。关闭时，仅添加您选择的文本。需要 Claude Code v2.1.271 或更高版本 |
| `useCtrlEnterToSend` | `false` | 使用 Ctrl/Cmd+Enter 而不是 Enter 来发送提示 |
| `scrollToBottomOnSend` | `true` | 当您发送消息时，将对话滚动到底部。关闭时，对话保持在您离开的位置。需要 Claude Code v2.1.275 或更高版本 |
| `showMessageTimestamps` | `true` | 显示每条消息的发送时间。日期行会标记日期变更的位置。需要 Claude Code v2.1.284 或更高版本。在 v2.1.290 之前，默认值为 `false` |
| `enableNewConversationShortcut` | `false` | 启用 Cmd/Ctrl+N 来开始新对话 |
| `enableReopenClosedSessionShortcut` | `true` | 使用 Cmd/Ctrl+Shift+T 重新打开最近关闭的 Claude 会话标签页。当最后关闭的标签页不是 Claude 会话时，快捷键会运行 VS Code 的正常重新打开关闭编辑器命令。 |
| `archiveInactiveSessions` | `14` | 在无活动的这么多天后[自动存档会话](#resume-past-conversations)：`1`、`2`、`7` 或 `14`。设置为 `0` 以关闭。需要 Claude Code v2.1.265 或更高版本 |
| `continueAfterReload` | `true` | 窗口重新加载后，Claude [继续在恢复的会话中被中断的步骤](#continue-conversations-after-a-reload)。需要 Claude Code v2.1.274 或更高版本 |
| `hideOnboarding` | `false` | 隐藏入门清单（毕业帽图标） |
| `focusView` | `false` | 将工具调用、工具结果和思考隐藏在可展开的行后面，只留下您的提示和 Claude 的响应。Claude 的最新待办事项列表保持可见；这需要 Claude Code v2.1.225 或更高版本。您也可以从命令菜单切换焦点视图。需要 Claude Code v2.1.221 或更高版本 |
| `respectGitIgnore` | `true` | 从文件搜索和[选择上下文](#reference-files-and-folders)中排除 .gitignore 模式 |
| `usePythonEnvironment` | `true` | 运行 Claude 时激活工作区的 Python 环境。需要 Python 扩展。 |
| `environmentVariables` | `[]` | 为 Claude 进程设置环境变量。对于共享配置，请改用 Claude Code 设置。仅当值为绝对路径时，[`CLAUDE_CONFIG_DIR`](/docs/zh-CN/env-vars) 条目才会生效；扩展不会展开 `~`，并且会忽略相对路径值。 |
| `disableLoginPrompt` | `false` | 跳过身份验证提示（用于第三方提供商设置） |
| `allowDangerouslySkipPermissions` | `false` | 在模式选择器中添加绕过权限。仅在没有互联网访问的沙箱中使用。 |
| `claudeProcessWrapper` | - | 用于启动 Claude 进程的可执行文件。当存在时，捆绑的二进制路径作为参数传递。如果扩展构建不包含您的平台的二进制文件，请将其设置为单独安装的 `claude` 二进制文件。 |

<h2 id="use-a-screen-reader">
  使用屏幕阅读器
</h2>

该扩展的聊天面板可与屏幕阅读器配合使用。您无需打开任何设置：该扩展会为每个用户宣布对话活动，无需进行任何视觉更改。这与 CLI 的可选 [屏幕阅读器模式](/docs/zh-CN/accessibility) 不同，后者会调整终端界面。

聊天面板中的屏幕阅读器支持需要 Claude Code v2.1.236 或更高版本。

在对话期间，该扩展会宣布：

* **Claude 的回复**：该扩展在每条回复完成时宣布一次，在文本流入时保持沉默。您的屏幕阅读器将代码块读作行数摘要，按标签读取链接，逐个单元格读取表格；完整回复在记录中保持可读。
* **权限请求和问题**：当权限提示出现时，该扩展会宣布请求，并命名 Claude 想要使用的工具。当 Claude 向您提问以及当 Claude 完成计划并等待您审查时，它以相同方式宣布。
* **状态更改**：当 Claude 开始工作、Claude 准备好接收您的输入以及 Claude Code 开始压缩对话时，该扩展会宣布。
* **排队的消息**：当您在 Claude 工作时发送消息，该扩展会为该消息宣布"Message queued."。
* **错误和模型提示**：该扩展宣布对话中的错误，并在 [使用额度同意提示](/docs/zh-CN/model-config#fable-and-usage-credits) 或 [标记请求提示](/docs/zh-CN/model-config#ask-before-switching) 出现时宣布。

当 Claude 工作时，您的屏幕阅读器会读取一个文本标签来代替进度旋转器的动画。

当您重新打开会话或切换到另一个会话时，该扩展不会宣布任何内容：恢复的历史记录、待处理的权限提示和进行中的状态保持沉默，直到发生新的事情。

<h3 id="use-the-chat-panel-from-the-keyboard">
  从键盘使用聊天面板
</h3>

记录中的每个回合都以视觉隐藏的标题开头，标题标记为启动该回合的提示，因此您可以使用屏幕阅读器的标题导航在回合之间跳转。

在回合内，当您在其中移动时，您的屏幕阅读器会宣布您所在的消息来自谁：

* **您的消息**："您"
* **Claude 的消息**："Claude"
* **工具步骤**："Claude"加上工具名称，例如"Claude，Bash"
* **思考块**："Claude，思考"

因为该扩展将记录公开为标记的区域，您也可以使用 `Tab` 将焦点移动到记录本身，并按您自己的速度读取。要将焦点移动到最新消息或等待的权限提示，请从 [命令面板](#vs-code-commands-and-shortcuts) 运行 **Claude Code: Focus last message**。

当权限提示上的选项保存权限规则或目录访问时，其标签末尾会命名批准的保存位置，例如"所有项目"或"此会话"。当该选项获得焦点时，按 `Left` 或 `Right` 箭头键以更改目标，该扩展会在您移动到每个目标时宣布。您也可以单击标签中的目标。箭头键需要 Claude Code v2.1.268 或更高版本。

<h2 id="vs-code-extension-vs-claude-code-cli">
  VS Code extension vs. Claude Code CLI
</h2>

Claude Code 既可作为 VS Code extension（图形面板）使用，也可作为 CLI（终端中的命令行界面）使用。某些功能仅在 CLI 中可用。如果您需要仅限 CLI 的功能，请在 VS Code 的集成终端中运行 `claude`。这需要[独立 CLI 安装](/docs/zh-CN/setup)：extension 不会将 `claude` 添加到您的 PATH。请参阅[在 VS Code 中运行 CLI](#run-cli-in-vs-code)。

| 功能 | CLI | VS Code Extension |
| - | - | - |
| Commands and skills | [全部](/docs/zh-CN/commands) | 子集（输入 `/` 查看可用项） |
| MCP server config | 是 | 是（在聊天面板中使用 `/mcp` [添加和管理服务器](#connect-to-external-tools-with-mcp)） |
| Checkpoints | 是 | 是 |
| `!` Bash shortcut | 是 | 否 |
| Tab completion | 是 | 否 |

<h3 id="rewind-with-checkpoints">
  Rewind with checkpoints
</h3>

VS Code extension 支持 checkpoints，它可以跟踪 Claude 的文件编辑并让您回退到之前的状态。将鼠标悬停在任何消息上以显示回退按钮，然后从三个选项中选择：

* **Fork conversation from here**：从此消息开始新的对话分支，同时保持所有代码更改完整
* **Rewind code to here**：将文件更改恢复到对话中的此点，同时保持完整的对话历史记录
* **Fork conversation and rewind code**：开始新的对话分支并将文件更改恢复到此点

有关 checkpoints 如何工作及其限制的完整详情，请参阅 [Checkpointing](/docs/zh-CN/checkpointing)。

<h3 id="run-cli-in-vs-code">
  Run CLI in VS Code
</h3>

要在 VS Code 中使用 CLI，请打开集成终端（Windows/Linux 上为 `` Ctrl+` ``，Mac 上为 `` Cmd+` ``）并运行 `claude`。CLI 会自动与您的 IDE 集成，以支持 diff 查看和诊断共享等功能。

安装 extension 不会将 `claude` 放在您的 shell PATH 上。extension 为其聊天面板捆绑了 CLI 的私有副本，但在终端中输入 `claude` 需要[独立 CLI 安装](/docs/zh-CN/setup)。运行一次安装，此页面上的命令（包括 `claude mcp add` 和 `claude --resume`）将在任何终端中工作。如果安装后仍未找到 `claude`，请[验证您的 PATH](/docs/zh-CN/troubleshoot-install#verify-your-path)。

如果使用外部终端，请在 Claude Code 中运行 `/ide` 以将其连接到 VS Code。

<h3 id="switch-between-extension-and-cli">
  Switch between extension and CLI
</h3>

extension 和 CLI 共享相同的对话历史记录。要在 CLI 中继续 extension 对话，请在终端中运行 `claude --resume`。这将打开一个交互式选择器，您可以在其中搜索并选择您的对话。

<h3 id="include-terminal-output-in-prompts">
  Include terminal output in prompts
</h3>

使用 `@terminal:name` 在您的提示中引用终端输出，其中 `name` 是终端的标题。这让 Claude 可以看到命令输出、错误消息或日志，而无需复制粘贴。

<h3 id="move-a-running-command-or-subagent-to-the-background">
  Move a running command or subagent to the background
</h3>

当 Claude 正在等待某个命令或[子代理](/docs/zh-CN/sub-agents)，而其耗时超出您的预期时，请单击对话中其工具调用下方的 **Run in background**。该操作会在命令运行约两秒后出现，或在子代理启动后立即出现。Claude 会停止等待并继续当前轮次，而该命令或子代理则作为[后台任务](/docs/zh-CN/tools-reference#background-commands)继续运行，并在完成时通知 Claude。需要 Claude Code v2.1.287 或更高版本。

在此期间，若要查看任务状态或停止任务，请在输入框中输入 `/tasks` 以打开 [Agent 地图](#use-the-prompt-box)。子代理会在其中的 Agent 树中保留其位置，而命令则列在各 Agent 下方，其[卡片上显示最新输出](#monitor-background-processes)。

<h3 id="monitor-background-processes">
  Monitor background processes
</h3>

在提示框中输入 `/tasks` 以打开 [Agent 地图](#use-the-prompt-box)，它列出会话的后台任务，例如 Claude 作为后台 shell 命令留下运行的开发服务器。单击任务以打开其卡片，您可以在那里停止它。需要 Claude Code v2.1.277 或更高版本。

对于后台 shell 命令，或运行命令的[监视器](/docs/zh-CN/tools-reference#monitor-tool)，卡片还会显示该命令的最新输出，并在命令运行期间持续刷新。

<h3 id="connect-to-external-tools-with-mcp">
  Connect to external tools with MCP
</h3>

MCP（Model Context Protocol）服务器为 Claude 提供对外部工具、数据库和 API 的访问。

要在不离开 VS Code 的情况下管理 MCP 服务器，请在聊天面板中输入 `/mcp`。从打开的对话框中，您可以添加服务器、删除保存在本地、用户或项目[范围](/docs/zh-CN/mcp#mcp-installation-scopes)的服务器、启用或禁用服务器、重新连接到服务器以及管理 OAuth 身份验证。在对话框中添加和删除服务器需要 Claude Code v2.1.261 或更高版本。

您也可以在 VS Code 的集成终端中运行 `claude mcp add`（`` Ctrl+` `` 或 `` Cmd+` ``）。对话框和终端命令保存到相同的 MCP 配置，来自任一方的更改在您之后启动的对话中生效。下面的示例添加了 GitHub 的远程 MCP 服务器，该服务器使用作为标头传递的[个人访问令牌](https://github.com/settings/personal-access-tokens)进行身份验证：

```bash theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer YOUR_GITHUB_PAT"
```

将 `YOUR_GITHUB_PAT` 替换为您的个人访问令牌。`claude mcp add` 命令保存配置而不验证凭据，因此此处接受占位符值，但服务器稍后无法连接。要验证连接，请启动新对话，输入 `/mcp`，并检查服务器是否显示**已连接**。具有错误凭据的服务器显示**失败**。

配置后，要求 Claude 使用这些工具（例如，"Review PR #456"）。

要查找要连接的服务器，请参阅[查找和构建 MCP 服务器](/docs/zh-CN/mcp#find-and-build-mcp-servers)。

<h2 id="work-with-git">
  使用 git
</h2>

Claude Code 与 git 集成，帮助直接在 VS Code 中进行版本控制工作流。要求 Claude 提交更改、创建拉取请求或跨分支工作。要在具有自己的文件和分支的隔离 worktree 中启动 Claude，请参阅 [使用 worktrees 运行并行会话](/docs/zh-CN/worktrees)。

<h3 id="create-commits-and-pull-requests">
  创建提交和拉取请求
</h3>

Claude 可以暂存更改、编写提交消息，并根据您的工作创建拉取请求：

```text wrap theme={null}
commit my changes with a descriptive message
create a pr for this feature
summarize the changes I've made to the auth module
```

创建拉取请求时，Claude 会根据实际代码更改生成描述，并可以添加有关测试或实现决策的上下文。

<h2 id="use-third-party-providers">
  使用第三方提供商
</h2>

默认情况下，Claude Code 直接连接到 Anthropic 的 API。如果您的组织使用 Amazon Bedrock、Google Cloud 的 Agent Platform 或 Microsoft Foundry 来访问 Claude，请配置扩展以改用您的提供商：

<Steps>
  <Step title="禁用登录提示">
    打开[禁用登录提示设置](vscode://settings/claudeCode.disableLoginPrompt)并勾选该框。

    您也可以打开 VS Code 设置（Mac 上按 `Cmd+,` 或 Windows/Linux 上按 `Ctrl+,`），搜索"Claude Code login"，然后勾选**禁用登录提示**。
  </Step>

  <Step title="配置您的提供商">
    按照您的提供商的设置指南进行操作：

    * [Amazon Bedrock 上的 Claude Code](/docs/zh-CN/amazon-bedrock)
    * [Google Cloud 的 Agent Platform 上的 Claude Code](/docs/zh-CN/google-vertex-ai)
    * [Microsoft Foundry 上的 Claude Code](/docs/zh-CN/microsoft-foundry)

    这些指南涵盖在 `~/.claude/settings.json` 中配置您的提供商，这确保您的设置在 VS Code 扩展和 CLI 之间共享。
  </Step>
</Steps>

在第三方提供商上，扩展不提供需要 claude.ai 账户的功能，例如计划使用情况栏、[语音听写](/docs/zh-CN/voice-dictation)和用于[从 Claude.ai 恢复云会话](#resume-cloud-sessions-from-claude-ai)的 Web 标签页。有关这些登录时"账户和使用情况"对话框显示的内容，请参阅[检查账户和使用情况](#check-account-and-usage)。

来自早期 `/login` 的 claude.ai 登录会保留下来但未被使用：扩展不会在任何请求中发送它。

<h2 id="security-and-privacy">
  安全和隐私
</h2>

您的代码保持私密。Claude Code 处理您的代码以提供协助，但不会将其用于训练模型。有关数据处理的详细信息以及如何选择退出日志记录，请参阅[数据和隐私](/docs/zh-CN/data-usage)。

启用自动编辑权限后，Claude Code 可以修改 VS Code 配置文件（如 `settings.json` 或 `tasks.json`），VS Code 可能会自动执行这些文件。为了在处理不受信任的代码时降低风险：

* 为不受信任的工作区启用 [VS Code 受限模式](https://code.visualstudio.com/docs/editor/workspace-trust#_restricted-mode)
* 编辑时使用手动模式，而不是自动编辑模式或自动模式
* 在接受更改之前仔细审查更改

<h3 id="the-built-in-ide-mcp-server">
  内置 IDE MCP 服务器
</h3>

当扩展处于活动状态时，它运行一个本地 MCP 服务器，CLI 会自动连接到该服务器。这是 CLI 在 VS Code 的原生 diff 查看器中打开 diff、读取您当前的选择以用于 `@`-mentions，以及——当您在 Jupyter notebook 中工作时——要求 VS Code 执行单元格的方式。

服务器名为 `ide`，从 `/mcp` 中隐藏，因为没有什么需要配置的。但是，如果您的组织使用 `PreToolUse` hook 将 MCP 工具加入允许列表，您需要知道它的存在。

**选择和打开文件上下文。** 连接时，CLI 会在您发送的每个提示词中包含您当前的编辑器选择和活动文件的路径作为上下文。当发生这种情况时，会话记录会显示一行 `⧉ Selected N lines from <file>`。

如果您[在 Claude 工作时排队消息](/docs/zh-CN/interactive-mode#queue-messages-while-claude-works)，它会保留您按下 `Enter` 时的选择，无论您之后选择什么。

要排除敏感文件（如 `.env`），请为其路径添加 [`Read` 拒绝规则](/docs/zh-CN/permissions#read-and-edit)。匹配的拒绝规则可防止该文件的选定文本和打开文件通知到达 Claude。

如果您关闭[附加打开文件设置](#extension-settings)，CLI 仅在您在该文件中选择文本时接收活动文件的路径。

**传输和身份验证。** 服务器绑定到 `127.0.0.1` 上的随机端口，范围在 10000–65535，端口不可配置。传输是未加密的 `ws://`；因为套接字仅限于本地回环，任何可以捕获流量的进程也可以从锁文件中读取令牌，所以 TLS 不会增加保护。每次扩展激活都会生成一个新的随机身份验证令牌，将其写入 `~/.claude/ide/<port>.lock` 处的锁文件，CLI 必须将其作为 `X-Claude-Code-Ide-Authorization` 标头呈现才能连接。锁文件在 `0700` 目录中具有 `0600` 权限，因此只有运行 VS Code 的用户才能读取它。如果设置了 `CLAUDE_CONFIG_DIR`，锁文件将写入 `$CLAUDE_CONFIG_DIR/ide/` 目录。

**暴露给模型的工具。** 服务器托管十几个工具，但只有两个对模型可见。其余的是 CLI 用于自己的 UI 的内部 RPC，例如打开 diff、读取选择和保存文件。它们在工具列表到达 Claude 之前被过滤掉。

| 工具名称（如 hook 所见） | 功能 | 只读 |
| - | - | - |
| `mcp__ide__getDiagnostics` | 返回语言服务器诊断：VS Code 的问题面板中的错误和警告。可选地限定到一个文件。 | 是 |
| `mcp__ide__executeCode` | 在活动 Jupyter notebook 的内核中运行 Python 代码。请参阅下面的确认流程。 | 否 |

**聊天面板中的诊断。** 在聊天面板中，使用 Claude Code v2.1.285 或更高版本时，Claude 通过一个名为 `claude-vscode` 的独立内置服务器读取 VS Code 的问题面板。Claude 可以向它请求某个文件中的当前错误和警告，或者 VS Code 具有诊断信息的所有文件中的当前错误和警告。

hook 和权限规则将聊天面板的诊断工具视为 `mcp__claude-vscode__getDiagnostics`。要同时涵盖 CLI 和聊天面板中的诊断，请在您的 hook 或规则中同时指定 `mcp__ide__getDiagnostics` 和 `mcp__claude-vscode__getDiagnostics`。

以下 `settings.json` 示例拒绝这两个工具：

```json theme={null}
{
  "permissions": {
    "deny": [
      "mcp__ide__getDiagnostics",
      "mcp__claude-vscode__getDiagnostics"
    ]
  }
}
```

`Read` 拒绝规则不涵盖这两个工具中的任何一个，因此请像示例那样使用[拒绝规则](/docs/zh-CN/permissions#mcp)按名称阻止它们。

**Jupyter 执行始终先询问。** `mcp__ide__executeCode` 无法静默运行任何内容。在每次调用时，代码被插入为活动 notebook 末尾的新单元格，VS Code 将其滚动到视图中，原生快速选择器要求您**执行**或**取消**。取消或用 `Esc` 关闭选择器，会向 Claude 返回错误，不会运行任何内容。当没有活动 notebook、未安装 Jupyter 扩展 (`ms-toolsai.jupyter`) 或内核不是 Python 时，该工具也会直接拒绝。

<Note>
  快速选择器确认与 `PreToolUse` hook 分开。`mcp__ide__executeCode` 的允许列表条目让 Claude *提议*运行单元格；VS Code 内的快速选择器是让它*实际*运行的原因。
</Note>

<a id="troubleshooting" />

<h2 id="fix-common-issues">
  修复常见问题
</h2>

登录、网络和启动错误在安装故障排除页面和错误参考页面中有各自的条目。请在表格中找到您看到的内容，然后点击相应链接。

| 您看到的内容 | 前往位置 |
| - | - |
| 登录后出现 `API Error: 403 Request not allowed` | [登录后出现 403 Forbidden](/docs/zh-CN/troubleshoot-install#403-forbidden-after-login) |
| 已经登录后仍被要求再次登录 | [未登录或令牌已过期](/docs/zh-CN/troubleshoot-install#not-logged-in-or-token-expired) |
| 云提供商凭据在终端中可用，但在扩展程序中不可用 | [Bedrock、Agent Platform 或 Foundry 凭据未加载](/docs/zh-CN/troubleshoot-install#bedrock-agent-platform-or-foundry-credentials-not-loading) |
| `SSL certificate verification failed` 或 `Self-signed certificate detected` | [SSL 证书错误](/docs/zh-CN/errors#ssl-certificate-errors) |
| `Claude Code process exited with code 1` 或其他代码 | [Claude Code process exited with code N](/docs/zh-CN/errors#claude-code-process-exited-with-code-n) |
| `Could not locate the Claude CLI on PATH` | [Could not locate the Claude CLI on PATH](/docs/zh-CN/errors#could-not-locate-the-claude-cli-on-path) |
| `The connection to Claude Code ended before this message completed` | [The connection to Claude Code ended before this message completed](/docs/zh-CN/errors#the-connection-to-claude-code-ended-before-this-message-completed) |
| 在 VS Code 的集成终端中找不到 `claude` | [在 VS Code 中运行 CLI](#run-cli-in-vs-code) |

<h3 id="extension-won’t-install">
  扩展程序无法安装
</h3>

* 确保您拥有兼容的 VS Code 版本（1.94.0 或更高版本）
* 检查 VS Code 是否有权限安装扩展程序
* 尝试直接从 [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code) 安装

<h3 id="spark-icon-not-visible">
  Spark 图标不可见
</h3>

当您打开文件时，Spark 图标会出现在**编辑器工具栏**（编辑器右上角）。如果您看不到它：

1. **打开文件**：该图标需要打开文件。仅打开文件夹是不够的。
2. **检查 VS Code 版本**：需要 1.94.0 或更高版本（帮助 → 关于）
3. **重启 VS Code**：从命令面板运行"Developer: Reload Window"
4. **禁用冲突的扩展程序**：临时禁用其他 AI 扩展程序（Cline、Continue 等）
5. **检查工作区信任**：该扩展程序在受限模式下不起作用

或者，点击窗口右下角**状态栏**中的 **✻ Claude Code**。即使没有打开文件，这也能工作。您也可以使用**命令面板**（`Cmd+Shift+P` / `Ctrl+Shift+P`）并输入"Claude Code"。

<h3 id="cmd-esc-does-nothing-on-macos">
  Cmd+Esc 在 macOS 上无效
</h3>

在 macOS Tahoe 及更高版本上，系统游戏覆盖快捷键默认绑定到 `Cmd+Esc`，并在按键到达 VS Code 之前拦截它。要释放该快捷键：

1. 打开系统设置
2. 转到键盘，然后键盘快捷键，然后游戏控制器
3. 清除游戏覆盖复选框

或者，将扩展程序重新绑定到不同的键：打开 VS Code [键盘快捷键编辑器](https://code.visualstudio.com/docs/configure/keybindings)（`Cmd+K Cmd+S`），搜索 `Claude Code: Focus input`，并分配新的绑定。

<h3 id="claude-code-never-responds">
  Claude Code 从不响应
</h3>

如果 Claude Code 没有响应您的提示：

1. **检查您的互联网连接**：确保您有稳定的互联网连接
2. **开始新对话**：尝试开始新对话以查看问题是否仍然存在
3. **尝试 CLI**：从终端运行 `claude` 以查看是否获得更详细的错误消息

如果问题仍然存在，请[在 GitHub 上提交问题](https://github.com/anthropics/claude-code/issues)，并提供有关错误的详细信息。

<h2 id="uninstall-the-extension">
  卸载扩展
</h2>

要卸载 Claude Code 扩展：

1. 打开扩展视图（Mac 上按 `Cmd+Shift+X` 或 Windows/Linux 上按 `Ctrl+Shift+X`）
2. 搜索"Claude Code"
3. 点击**卸载**

如果你在 VS Code 集成终端中运行 `claude`，Claude Code 会自动重新安装扩展。要保持卸载状态，请在 `/config` 中关闭**自动安装 IDE 扩展**，或将 [`autoInstallIdeExtension`](/docs/zh-CN/settings-reference#autoinstallideextension) 设置为 `false`。你也可以将 [`CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`](/docs/zh-CN/env-vars) 环境变量设置为 `1`。

要同时删除扩展数据并重置所有设置，请删除你的平台对应的扩展存储目录。

在 macOS 上：

```bash theme={null}
rm -rf ~/Library/"Application Support"/Code/User/globalStorage/anthropic.claude-code
```

在 Linux 上：

```bash theme={null}
rm -rf ~/.config/Code/User/globalStorage/anthropic.claude-code
```

在 Windows 上，在 PowerShell 中：

```powershell theme={null}
Remove-Item -Recurse -Force "$env:APPDATA\Code\User\globalStorage\anthropic.claude-code"
```

如需更多帮助，请参阅[故障排除指南](/docs/zh-CN/troubleshooting)。

<h2 id="next-steps">
  后续步骤
</h2>

现在您已在 VS Code 中设置了 Claude Code：

* [探索常见工作流](/docs/zh-CN/common-workflows)以充分利用 Claude Code
* [设置 MCP 服务器](/docs/zh-CN/mcp)以使用外部工具扩展 Claude 的功能。在聊天面板中使用 `/mcp` 添加和管理它们。
* [配置 Claude Code 设置](/docs/zh-CN/settings)以自定义允许的命令、hooks 等。这些设置在扩展和 CLI 之间共享。
