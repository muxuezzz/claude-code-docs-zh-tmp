> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 将会话输出作为 artifacts 共享

> Artifacts 将 Claude Code 的工作转化为 claude.ai 上的实时交互式页面，您可以将其保持私密、与您的组织共享或发布到公开链接。

<Note>
  Artifacts 在 Pro、Max、Team 和 Enterprise 计划中可用，需要使用 [`/login`](/docs/zh-CN/setup#authenticate) 登录的会话。有关完整的要求集，请参阅 [可用性](#availability)。
</Note>

[Artifact](https://claude.com/features/artifacts) 是一个实时交互式网页，Claude Code 从您的会话发布到 claude.ai 上的私密 URL。您在浏览器中打开它，随着会话的继续，它会实时更新。当您希望其他人也看到它时，可以从页面标题中共享它。

<Frame>
  <img src="https://mintcdn.com/claude-code/kaHIYYMIYMYPxQg9/images/artifacts-viewer.png?fit=max&auto=format&n=kaHIYYMIYMYPxQg9&q=85&s=dbfd671cdb0d15f49f808b9e89778fe1" alt="一个 artifact 在浏览器中打开，位于 claude.ai/code/artifact。查看器标题显示 artifact 标题 acme-funnel-fix、一个共享按钮和作者头像。共享菜单已打开，显示&#x22;始终共享最新版本&#x22;切换、显示&#x22;共享版本 2&#x22;的版本选择器、&#x22;Acme 中的所有人&#x22;受众选择器和复制链接按钮。标题下方，artifact 页面显示两个并排的移动设备模型、一个漏斗图表和一行指标卡片。" width="2511" height="1890" data-path="images/artifacts-viewer.png" />
</Frame>

<h2 id="when-to-use-an-artifact">
  何时使用 artifact
</h2>

当终端文本不是 Claude 生成内容的合适媒介时，请使用 artifact：输出内容更容易查看和交互，而不是逐行阅读。Claude 从您的会话可以访问的任何内容构建页面，包括您的代码库和通过您的[连接工具](/docs/zh-CN/mcp)拉取的数据，因此页面可以显示需要段落才能描述的内容。例如，要求 Claude：

* 通过带注释的 diff 向审查者讲解拉取请求
* 从会话已拉取的数据呈现仪表板
* 并排展示多个设计或实现选项
* 保持在长任务运行时填充的调查时间线
* 向团队成员发送链接，而不是将输出粘贴到 Slack
* 发布状态板，[每次有人打开时通过 MCP 连接器拉取新数据](#pull-live-data-with-mcp-connectors)

有关与这些相匹配的提示，请参阅[您可以构建的内容](#what-you-can-build)，有关连接器支持的板的提示，请参阅[使用 MCP 连接器拉取实时数据](#pull-live-data-with-mcp-connectors)。

<h3 id="what-an-artifact-is-not">
  artifact 不是什么
</h3>

artifact 是工作的捕获：一个自包含的页面，没有后端，因此无法提供多个路由。对于具有后端的托管内部工具，请改为在您自己的基础设施上部署它。有关完整的限制集，请参阅[页面约束](#page-constraints)。

<h2 id="create-an-artifact">
  创建工件
</h2>

Claude 可能会在输出适合作为页面时自动发布工件，或者你可以直接请求创建一个。要请求创建，请用简洁的语言命名该功能或描述你想要的视觉输出。任何比以文本形式阅读更容易看到的内容都是很好的候选，例如带有内联注释的 diff、图表或一组选项的比较。下面的提示是两个示例；有关更多模式，请参阅[你可以构建的内容](#what-you-can-build)。

```text wrap theme={null}
Make an artifact that walks through this PR with the diff annotated inline.
```

```text wrap theme={null}
Build a dashboard artifact of last week's deploy failures by service and keep it updated as you investigate.
```

除非你指定位置，否则 Claude 会将页面写入项目外的临时目录中的 HTML 或 Markdown 文件，然后发布它。在[计划模式](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode)之外，Claude 发布的响应你输入的提示的新工件会直接通过，无需权限提示或分类器审查，除非该发布声明了页面的运行时功能，例如[连接器调用](#pull-live-data-with-mcp-connectors)或[文件下载](#offer-a-file-download)。在计划模式下，Claude Code 会在每个工件的首次发布前询问你。

工件对你保持私密，直到你[共享它](#share-an-artifact)。在你公开共享后，Claude Code 会在每次对话中要求你的批准一次后再更改它，或在[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)下让分类器审查更改。

如果你关闭了[功能标志获取](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)，Claude Code 会在每个工件的首次发布前询问，或在自动模式下让分类器审查它。

首次发布后，Claude 会打印 URL，你的浏览器会打开到新页面。如果你通过[远程控制](/docs/zh-CN/remote-control)从 claude.ai、Claude Desktop 或 Claude 移动应用发送提示，运行会话的机器上不会打开标签页。下次 Claude 从你在终端输入的提示发布工件时，浏览器会在那里打开。随时按 `Ctrl+]` 可以重新打开会话的最近工件。

Claude 会选择工件的标题和一个表情符号，两者都会出现在你在 claude.ai 上的[工件库](#share-an-artifact)和共享链接中。Claude 还可以选择与页面内容相匹配的浏览器标签页图标，例如图表或日历。如果你想要特定的标题、表情符号或标签页图标，请告诉 Claude。

要停止在发布新工件时自动打开浏览器，请在你的环境中设置 `CLAUDE_CODE_ARTIFACT_AUTO_OPEN=0`。

如果 Claude 回复说无法发布，或写入本地 HTML 文件而没有链接，则该工具未为你的会话启用。检查[可用性](#availability)要求。

<h2 id="update-an-artifact">
  更新一个 artifact
</h2>

要求 Claude 修改页面，或让长时间运行的任务在进行过程中重新发布。Claude 编辑底层文件并重新发布到相同的 URL。

```text wrap theme={null}
在摘要图表下方添加按地区的细分，然后重新发布。
```

任何打开该页面的人都会看到就地更新。每次发布都会成为一个版本，从页面标题中的 **Share** 控件，你可以选择查看者看到哪个版本。

要从不同的会话更新 artifact，请给 Claude 其 URL，或使用 [`/artifacts`](#find-an-artifact-again) 附加它。如果两者都没有，新会话会创建新的 artifact 而不是更新现有的。

```text wrap theme={null}
使用今天的数字更新 https://claude.ai/code/artifact/5fbea6f3-...
```

<h2 id="find-an-artifact-again">
  再次查找一个artifact
</h2>

在Claude Code中运行`/artifacts`以列出您拥有的每个artifact和与您共享的每个artifact。选择一个并按`o`在浏览器中打开它，或按`c`复制其链接。按`Enter`将其附加到当前会话；在v2.1.216之前，`Enter`在浏览器中打开它。Claude Code从您的claude.ai账户读取列表，因此它在新会话中工作，在`/clear`之后工作，当链接已从终端滚出时也能工作。需要Claude Code v2.1.208或更高版本。

<h2 id="share-an-artifact">
  分享一个artifact
</h2>

新创建的artifact只有你能看到。要分享它，请在浏览器中打开该artifact，并使用页面标题中的**分享**控件。标题还链接到你的库，位置在[claude.ai/code/artifacts](https://claude.ai/code/artifacts)，其中列出了你创建的每个artifact。

你组织中的查看者可以看到谁发布了该页面：在组织内共享的artifact上，你的名字在标题菜单中；在公开artifact上，对于组织内已登录的查看者，你的名字在页面标题中。打开公开链接但未登录的查看者，或来自组织外的查看者，会看到标签`内容由用户生成且未经验证。`而不是你的名字。

你可以与谁分享取决于你的计划：

* **在你的组织内**：在Team和Enterprise计划上，向组织中的特定人员或所有人授予访问权限。查看者以组织成员身份登录claude.ai以查看该页面。
* **公开**：分享一个链接，互联网上的任何人都可以打开，无需claude.ai登录。在Team和Enterprise计划上，公开分享处于关闭状态，直到所有者[为组织启用它](#control-public-sharing)。

<h3 id="let-someone-edit-with-you">
  让某人与你一起编辑
</h3>

与你分享的人默认是查看者：他们可以看到你发布的每个版本，但无法更改页面。在Team和Enterprise计划上，你也可以让某人成为编辑者。在分享对话框中，添加一个人并将其角色从**查看者**切换到**编辑者**。

编辑者发布新版本的方式与你[从另一个会话更新artifact](#update-an-artifact)的方式相同：他们向Claude提供artifact的URL，或从[`/artifacts`](#find-an-artifact-again)附加它，Claude会拉取当前内容并用他们的更改重新发布。打开该页面的每个人都会实时看到每个更新。

<h2 id="read-an-artifact-shared-with-you">
  阅读与你共享的工件
</h2>

当有人与你共享一个工件时，你可以让 Claude 阅读它：给 Claude 提供其 URL，或从 [`/artifacts`](#find-an-artifact-again) 附加它。

Claude 读取他人编写的页面的方式与它读取网页的方式相同，使用 [WebFetch](/docs/zh-CN/tools-reference#webfetch-tool-behavior)：它获得关于所询问内容的摘要，而不是原始页面，摘要报告写入页面的说明，而不是转达它们。Claude Code 还将页面的完整源代码保存到本地文件，当 Claude 需要确切内容时可以打开该文件，例如将工件重新发布为 [编辑器](#let-someone-edit-with-you)。

<h2 id="collect-comments-on-an-artifact">
  收集工件上的评论
</h2>

当您在组织内共享工件时，与您共享的人可以在页面上留下评论，您可以让 Claude 读取这些评论并回复。您需要 Claude Code v2.1.221 或更高版本。Claude 在两种情况下读取评论：

* **您要求 Claude 读取评论**：向 Claude 提供工件的 URL 并要求查看评论。Claude 列出每个线程，并标记可以编辑工件的人发送给它的评论。
* **可以编辑工件的人向 Claude 发送评论**：在页面上的线程中，他们使用**发送给 Claude**发送评论，或在其中提及 `@claude`。无论哪种方式，他们都会激活该线程。

Claude 只能回复或解决已激活的线程。其他线程保持打开状态，直到某人在页面上解决它们。查看者会看到每条回复都归属于 Claude，通过您。

如果您公开共享工件，只有其公开链接访问权限的人看不到其评论，也无法添加任何评论。现有评论线程保留在工件上，您和其编辑者仍然可以读取和回复它们。

要自己要求查看评论，请向 Claude 提供 URL：

```text wrap theme={null}
读取 https://claude.ai/code/artifact/5fbea6f3-... 上的评论，并进行评论者要求的更改。
```

如果 Claude 告诉您它无法读取评论，请确认您的版本、您的会话和您的功能标志设置：

* 您运行的是 Claude Code v2.1.221 或更高版本。
* 您不在安装 Claude Code 或从 v2.1.221 之前的版本升级后的第一个会话中。在[安装或升级后的第一个会话](/docs/zh-CN/env-vars#first-session-after-an-install-or-upgrade)中，Claude 可能还无法读取评论；启动新会话并再次询问。
* 您没有关闭功能标志获取。

<h3 id="let-claude-reply-to-comments-on-its-own">
  让 Claude 自动回复评论
</h3>

在您的会话发布工件后，Claude Code 会在会话运行期间监视该工件的评论。当可以编辑工件的人向 Claude 发送评论时，它会立即到达您的会话，Claude 可以读取线程并回复，而无需您询问。

您需要 Claude Code v2.1.228 或更高版本。如果您关闭了[功能标志获取](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)，Claude Code 不会监视评论。

您的[权限模式](/docs/zh-CN/permission-modes)决定了当发送的评论到达时 Claude 的行为：

* **Claude 自动回复**：当您的权限模式允许 Claude 在不询问您的情况下发布回复时，Claude 读取线程并回复，并在评论要求更改时编辑工件。您会看到`自动回复了工件上的评论线程：<name>`或`自动编辑了工件：<name>以响应评论线程`。
* **Claude 等待您**：在计划模式之外，当发布回复需要您的批准时，您会看到`评论正在等待工件：<name>`。Claude 然后要求您批准读取线程，再次批准发布回复。
* **Claude 在计划模式中暂停**：您会看到`评论正在等待工件：<name>`，Claude 不会回复，直到您离开计划模式并要求它读取和回复。

Claude 还会在处理该工件上的 60 条已发送评论或线程激活后的一小时内停止自动回复该工件。您会看到`评论正在等待工件：<name>`一次，当该小时的评论过期时，Claude 会重新开始。

运行 `/tasks` 查看您的会话正在监视的每个工件，列为实时更新任务。您可以通过以下任何方式停止 Claude 自动回复：

* **在空闲提示符处按一次 Ctrl+C**：Claude 暂停回复您的会话正在监视的每个工件。在您发送下一条消息后，回复会重新开始。
* **在 `/tasks` 中停止任务**：Claude 停止回复该工件，直到您要求它在那里恢复回复。重新发布工件不会再次启动回复，当您稍后恢复会话时，停止仍然适用。
* **在 3 秒内按两次 `Ctrl+X Ctrl+K`**：[停止每个运行的后台子代理](/docs/zh-CN/interactive-mode#general-controls)的和弦也会停止 Claude 为会话的其余部分回复每个工件。要求 Claude 恢复回复不会撤销此停止。

如果传递评论的服务变得不可用或停止响应，Claude Code 会尝试重新连接一段时间，然后停止监视您的会话正在监视的每个工件。

<h2 id="pull-live-data-with-mcp-connectors">
  使用 MCP 连接器拉取实时数据
</h2>

artifact 可以在每次有人查看它时调用 [MCP 连接器](/docs/zh-CN/mcp#use-mcp-servers-from-claude-ai)，因此页面显示的是当前数据而不是构建它的会话中的快照。来自 artifact 的连接器调用在 Pro、Max、Team 和 Enterprise 计划上可用，需要 Claude Code v2.1.209 或更高版本。在早期版本上，Claude 会发布该页面，其中包含会话在构建时收集的任何数据。

要创建一个由连接器支持的页面，请在提示中命名连接器和您想要的数据：

```text wrap theme={null}
构建一个我们开放拉取请求的 dashboard artifact，当页面加载时通过我的 GitHub 连接器拉取实时列表。
```

Claude 声明该页面可能调用哪些连接器作为发布的一部分，该页面无法调用该声明之外的连接器。只有来自您 claude.ai 账户的连接器符合条件：Claude 在声明中命名它们，当有人查看页面时，每个调用都会[通过查看账户自己的连接](#how-connector-calls-work-for-viewers)运行到该连接器。您在 Claude Code 中配置的本地 MCP 服务器（例如来自 `.mcp.json` 的服务器）可以在 Claude 构建页面时提供数据，但已发布的页面无法调用它们。

页面在加载时获取数据，可以按间隔刷新或当查看者在页面上使用刷新控件时刷新。响应缓存在查看者的浏览器中，因此重新打开的页面会立即从缓存的响应呈现，然后使用新结果更新。

<h3 id="how-connector-calls-work-for-viewers">
  连接器调用如何为查看者工作
</h3>

当已发布的页面调用连接器时，该调用使用查看页面的人的账户，而不是发布它的人的账户：

* **每个查看者使用他们自己的连接器**：调用通过查看账户的已连接工具进行，因此两个打开同一 dashboard 的人可能会看到不同的数据，具体取决于他们的账户可以访问什么。该页面永远看不到任何人的凭证；claude.ai 代表页面进行调用。
* **查看者首先批准访问**：claude.ai 在页面的第一个连接器调用之前向每个查看者请求权限。拒绝的查看者或未连接页面使用的连接器的查看者仍然可以看到页面，但没有其实时部分。
* **操作也使用查看者的账户**：页面可以提供控件，调用具有副作用的连接器工具，例如发布消息或更新问题。该操作通过选择控件的任何人的账户进行。

当您计划共享一个由连接器支持的页面时，请要求 Claude 在每个实时部分中包含一条后备消息，该消息命名它需要的连接器。缺少连接的查看者随后会看到要连接的内容，而不是空部分。

您可以在您的组织内或公开[共享一个由连接器支持的页面](#share-an-artifact)，如您的计划和组织设置所允许的那样。连接器调用不会为未登录 claude.ai 的查看者或来自您组织外部的查看者运行。该查看者看到的页面没有其实时部分。

<h3 id="the-page-shows-no-live-data-for-a-viewer">
  页面对查看者显示没有实时数据
</h3>

当由连接器支持的页面呈现但其实时部分对您组织中的查看者保持为空时，请解决这些原因：

* **查看者未连接连接器**：连接器是按账户的，因此每个查看者都需要自己连接到页面调用的每个连接器。他们可以在 claude.ai 上的**设置 > 连接器**下添加一个，然后重新加载页面。
* **查看者拒绝了权限请求**：拒绝在该页面加载的其余部分持续。重新加载页面会再次显示权限请求。
* **为组织关闭了连接器调用**：所有者控制管理设置中的[**启用 artifact 连接器**切换](#control-connector-calls-from-artifacts)。
* **页面调用连接器不公开的工具名称**：受影响的部分对所有人（包括您）保持为空。当页面命名网关风格连接器后面的单个工具，而该连接器仅公开其自己的几个工具时，可能会发生这种情况。要求 Claude 修复页面调用的工具名称并再次发布它。

  当 Claude 发布页面且该连接器的工具在您的会话中可用时，Claude Code 会检查页面声明的工具名称与它们的对比，警告 Claude 不匹配的名称，并在没有任何名称匹配时拒绝发布。在 v2.1.265 之前，它会在不检查它们的情况下发布页面。

<h2 id="offer-a-file-download">
  提供文件下载
</h2>

artifact 可以向查看者提供页面生成的文件，例如表格的 CSV 导出或图表的 PNG。查看者通过页面上的下载控制（例如按钮）保存文件。文件下载是 claude.ai 启用的运行时功能，按账户提供，因此 Claude 在构建控制之前会检查您的账户是否具有此功能。

查看者无法从普通下载链接或页面上的脚本保存文件，因为 claude.ai 上的 artifact 查看器会阻止页面本身启动的任何下载，包括指向 `data:` 或 `blob:` URL 的链接。如果页面具有以这种方式构建的下载按钮，请要求 Claude 使用下载功能重新构建它们。

要提供文件，请在您的提示中要求控制和文件格式：

```text wrap theme={null}
Add a button that downloads this table as a CSV file.
```

Claude 将下载功能声明为发布的一部分，与[声明连接器](#pull-live-data-with-mcp-connectors)的方式相同。

<h2 id="what-you-can-build">
  您可以构建的内容
</h2>

Artifact 是单个 HTML 页面，因此您可以用 HTML、CSS 和内联 JavaScript 表达的任何内容都在范围内。下面的模式最常出现。

<h3 id="walk-through-a-change">
  逐步讲解更改
</h3>

要求一个页面，在相关行旁边呈现 diff 或设计更改并带有注释，以便审阅者可以在代码旁边阅读您的推理，而不是从描述中重建它。

```text wrap theme={null}
Make an artifact that walks through this PR. Render the diff with margin annotations and color-code findings by severity.
```

<h3 id="compare-alternatives">
  比较替代方案
</h3>

要求在一个页面上有多个变体，以便您可以相互评估它们。这适用于布局、文案、API 形状或实现计划。

```text wrap theme={null}
Make an artifact with four distinctly different layouts for the settings panel. Vary density and grouping, and lay them out as a grid with a one-line tradeoff under each.
```

<h3 id="tune-with-interactive-controls">
  使用交互式控件进行调整
</h3>

要求滑块、切换或输入字段绑定到您正在调整的任何内容，以便您可以直接探索值，而不是描述它们。

```text wrap theme={null}
Build an artifact with sliders for the easing curve, duration, and delay so I can try values on this transition. Show the animation live as I move them.
```

<h3 id="bring-the-result-back-to-your-session">
  将结果带回您的会话
</h3>

Artifact 可以充当您随后交给 Claude 的决定的轻量级编辑器。要求一个导出控件，生成您可以粘贴到终端的文本，以便与页面交互的结果流回会话，而不是停留在页面上。

```text wrap theme={null}
Make a triage board artifact with each open issue as a draggable card across Now, Next, Later, and Cut columns. Add a "Copy as prompt" button that gives me the final ordering to paste back here.
```

<h3 id="track-work-in-progress">
  跟踪进行中的工作
</h3>

要求 Claude 在长任务运行时保持 artifact 最新，以便任何拥有链接的人都可以跟随，而无需阅读终端。

```text wrap theme={null}
Turn this migration plan into a checklist artifact. Check items off as you complete them and add a note for anything you skip.
```

<h2 id="improve-the-visual-design">
  改进视觉设计
</h2>

Claude 在构建工件时应用内置设计技能，因此页面获得精心设计的调色板、排版和布局，无需额外提示。该技能还会在选择自己的设计之前查找项目中是否存在现有设计系统。设计令牌是设计系统重复使用的命名颜色、排版和间距值。为了保持工件与产品品牌的一致性，请将它们记录在 Claude 可以找到的地方，例如项目的 [CLAUDE.md](/docs/zh-CN/memory) 或存储库中的主题文件：

```markdown theme={null}
## Design system

- Colors: primary #1a4d8f, accent #f59e0b, surface #f8fafc
- Typography: Inter for body, JetBrains Mono for code
- Spacing: 8px scale, 6px border radius
```

Claude 将您的设计系统视为比其自己的选择更高的优先级，您的提示比两者都更高的优先级。上面的标题和格式是一个示例；任何清晰的颜色、字体和间距列表都可以。

对于排版，Claude 可以从 Google Fonts 加载字体，这是工件页面可以加载的唯一外部字体源。Claude 将任何其他字体内联为 `@font-face` 数据 URI，并为每个字体提供后备堆栈，因此即使字体未加载，页面仍会呈现。要使用特定字体，请在提示或设计系统中命名它。

<h2 id="start-from-a-slides-design-or-docs-template">
  从幻灯片、设计或文档模板开始
</h2>

Claude 可以从您的 claude.ai 账户上的模板开始创建工件，而不是从头开始构建页面：[Claude Slides](https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them#h_11d5a9a5fa) 用于演示文稿，[Claude Design](https://support.claude.com/en/articles/14604416-get-started-with-claude-design) 用于视觉设计，或 [Claude Docs](https://support.claude.com/en/articles/16923645-get-started-with-claude-docs) 用于其他人将阅读和编辑的文档。每个都在 claude.ai 上的自己的编辑器中打开，您和您的团队成员可以直接更改它或要求 Claude 更改，并将其导出为 PowerPoint、PDF 或 Word 等格式。

要从模板开始，请描述您想要的内容，例如"将迁移说明转换为周四审查的演示文稿"或"将此计划作为文档写给团队"。Claude 选择匹配的模板，从您的请求和会话已有的内容填充它，并给您链接。对于演示文稿或设计，您也可以运行 `/slides` 或 `/design` 并提供简要说明。

<Note>
  模板处于测试阶段。它们在 Pro、Max 和 Team 计划上默认启用。在 Enterprise 计划上，所有者在**组织设置 > 工件**下[启用每个模板](https://support.claude.com/en/articles/16994751-artifacts-admin-guide-for-team-and-enterprise-plans)。如果您的组织关闭了 Slides 模板，`/slides` 不会出现；如果关闭了 Design 模板，`/design` 不会草拟设计。两个命令都需要 Claude Code v2.1.265 或更高版本以及一个[工件可用](#availability)的会话。
</Note>

<h3 id="make-a-slide-deck">
  制作幻灯片演示文稿
</h3>

运行 `/slides` 并提供简要说明，说明演示文稿涵盖的内容以及针对的对象：

```text wrap theme={null}
/slides a quarterly review of the platform team's reliability work, for the engineering all-hands
```

Claude 创建一个 Claude Slides 工件并给您链接。在桌面浏览器中打开它以编辑或演示演示文稿。如果您运行 `/slides` 而不提供简要说明，Claude 会在创建任何内容之前询问演示文稿应该是关于什么的。

<h3 id="draft-a-design-canvas">
  草拟设计画布
</h3>

要模拟 UI、屏幕流、登陆页面或海报，而不是构建页面，请运行 `/design` 并提供简要说明。Claude 将设计作为一个画布上的画板草拟，并将画布发布为一个 Claude Design 工件。简要说明命名您想要绘制的内容：

```text wrap theme={null}
/design a settings screen for a mobile banking app
```

在桌面浏览器中打开已发布的工件以查看画板。在画板上选择一个元素并更改它，您的编辑会自动保存。您可以将每个画板导出为 PNG 或 PDF。

<h3 id="write-a-document-with-claude-docs">
  使用 Claude Docs 编写文档
</h3>

Claude Docs 作为 claude.ai [连接器](/docs/zh-CN/mcp#use-mcp-servers-from-claude-ai)而不是命令到达 Claude Code。连接后，`/mcp` 将其列为 `claude.ai Claude Docs`。针对供其他人使用的文档的请求随后转到 Claude Docs 而不是工件页面：规范、提案或您在会话中完成的计划的写入。Claude 在草拟文档时给您文档的链接。

属于代码库的文档（例如 README）保持为文件。要为 Claude 否则会放在 Claude Docs 中的内容获取文件，请命名格式，例如 `.docx` 或存储库中的 Markdown 文件。

要关闭连接器，请将 `claude.ai Claude Docs` 添加到 `deniedMcpServers` 或使用 `/mcp` 切换，两者都在[禁用 claude.ai 连接器](/docs/zh-CN/mcp#disable-claude-ai-connectors)中描述。

<h2 id="page-constraints">
  页面约束
</h2>

每个工件都是一个独立的页面。Claude Code 将您发布的文件包装在 HTML 文档外壳中，并在严格的内容安全策略 (CSP) 下提供服务，这决定了页面可以执行的操作。

| 约束 | 效果 |
| :- | :- |
| 外部请求 | 页面可以从 Google Fonts 加载字体，以及从[五个公共 CDN 主机](#allowlist-the-viewer-domain)加载脚本：cdnjs、unpkg、Tailwind 和 jQuery CDN，以及 jsDelivr 上的选定路径，例如 `/npm/`。CSP 阻止所有外部图像和所有其他外部脚本、样式表和字体，并让 `fetch`、XHR 和 WebSocket 调用仅到达页面自身的源和 Google Fonts 主机。因此，Claude 从这些 CDN 之一加载页面需要的任何库，内联所有其他 CSS 和 JavaScript，并将图像嵌入为数据 URI。[连接器调用](#pull-live-data-with-mcp-connectors)通过 claude.ai 进行，它自己进行网络调用。 |
| 无后端 | 工件是一个静态页面。它无法自行对查看者进行身份验证。 |
| 下载 | 页面无法自行启动下载。为了让查看者保存页面生成的文件，Claude 声明下载功能。请参阅[提供文件下载](#offer-a-file-download)。 |
| 单页面 | 相对链接无法解析，因为页面旁边没有部署任何内容。对于多部分内容，Claude 使用页面内锚点而不是单独的文件。 |
| 源文件类型 | 发布的文件必须是 `.html`、`.htm` 或 `.md`，并且必须解码为 UTF-8，或通过其字节顺序标记解码为小端 UTF-16。Markdown 文件呈现为样式化的文档页面，带有语法突出显示的代码。无法解码或包含替换字符 `U+FFFD` 的文件会被[拒绝并显示要修复的行和列](/docs/zh-CN/errors#the-source-file-is-not-valid-utf-8-text)。 |
| 呈现大小 | 呈现的页面必须为 16 MiB 或更小。大型嵌入图像通常是发布因大小而失败的原因。 |

生成工件使用输出令牌，就像任何其他响应一样，样式化页面比相同内容作为终端文本更耗费令牌。内联 CSS、用于交互控制的 JavaScript，尤其是嵌入为数据 URI 的图像是主要贡献者。要减少工件的令牌成本：

* 对于图表，优先使用 SVG 或 HTML 和 CSS，而不是嵌入的光栅图像
* 省略您不需要的交互性
* 让页面汇总大型数据集，而不是完整地内联它们

<h2 id="availability">
  可用性
</h2>

Artifacts 需要以下所有条件。当不满足其中一个时，Claude 写入本地 HTML 文件或说它无法发布。

| 要求 | 可用时间 |
| :- | :- |
| 计划 | Pro、Max、Team 或 Enterprise。在 Pro 和 Max 计划上，artifacts 仅对您私有，直到您共享它们，不适用任何管理员管理。在 Team 和 Enterprise 计划上，artifacts 默认启用，Owner 可以在 claude.ai 管理设置中 [关闭它们](#manage-artifacts-for-your-organization)。 |
| 身份验证 | 会话由 claude.ai 账户支持：在 CLI 或桌面应用中使用 `/login` 登录。Claude Tag 会话通过代理的身份登录，因此不需要任何步骤。使用 API 密钥、[网关令牌](/docs/zh-CN/llm-gateway) 或云提供商凭证的会话无法发布。 |
| 模型提供商 | Anthropic API。在 [Amazon Bedrock](/docs/zh-CN/amazon-bedrock)、[Google Cloud 的 Agent Platform](/docs/zh-CN/google-vertex-ai) 或 [Microsoft Foundry](/docs/zh-CN/microsoft-foundry) 上不可用。 |
| 组织策略 | 客户管理的加密密钥 (CMEK)、HIPAA 和 [零数据保留](/docs/zh-CN/zero-data-retention) 未为组织启用。 |
| 表面 | Claude Code CLI，或 Claude 桌面应用版本 1.13576.0 或更高版本。当 Claude Tag 和 artifacts 都为组织启用时，[Claude Tag](https://claude.com/docs/claude-tag/overview) 会话也可以发布 artifacts。在 [Agent SDK](/docs/zh-CN/agent-sdk/overview)、GitHub Action 和 MCP-server 上下文中默认关闭，以及当设置 [`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`](/docs/zh-CN/env-vars) 时。 |

您的组织是否允许 artifacts 来自您的组织策略，Claude Code 从 `api.anthropic.com` 加载。当 Claude Code 无法加载策略时，artifacts 不可用。当您请求一个时，Claude 会说明原因。

如果涉及代理、VPN 或网络过滤器，请要求您的 IT 管理员允许 `api.anthropic.com` 通过。Claude Code 会在后台继续重试，一旦策略加载并允许，artifacts 就会变得可用。

<h2 id="disable-artifacts">
  禁用 artifacts
</h2>

要为您自己的会话关闭 artifacts，无论您的组织设置如何，请使用以下任何一种方法：

| 位置 | 操作 |
| :- | :- |
| [`/config`](/docs/zh-CN/commands) | 关闭 **Artifacts** 行，这会将 [`"enableArtifact": false`](/docs/zh-CN/settings-reference#enableartifact) 写入您的用户设置 |
| [Settings 文件](/docs/zh-CN/settings) | 设置 `"enableArtifact": false`。已弃用的 `"disableArtifact": true` 也会关闭 artifacts |
| [环境变量](/docs/zh-CN/env-vars) | 设置 `CLAUDE_CODE_DISABLE_ARTIFACT=1` |
| [权限规则](/docs/zh-CN/permissions) | 将 `Artifact` 添加到 `permissions.deny` |

一旦您在 [`--settings`](/docs/zh-CN/cli-reference#cli-flags) 文件中或使用 `CLAUDE_CODE_DISABLE_ARTIFACT` 关闭 artifacts，或您的管理员在[托管设置](/docs/zh-CN/server-managed-settings)中关闭它们，任何设置文件都无法将其重新打开。在 v2.1.242 之前，[优先级堆栈](/docs/zh-CN/settings#settings-precedence)中较高位置的文件可能会重新打开 artifacts，即使较低优先级的文件设置了 `"enableArtifact": false`。

您也可以在项目的 `.claude/settings.json` 或 `.claude/settings.local.json` 中设置 `"enableArtifact": false` 来为该项目中的会话关闭 artifacts。任何文件中的 `"enableArtifact": true` 都不会将其重新打开。在项目和本地设置中支持此键需要 Claude Code v2.1.242 或更高版本。

如果您添加了没有 `domain:` 部分的 `WebFetch` deny 或 ask 规则，它不会关闭 artifacts 或阻止 artifact 读取。[`permissions` 中 `deny` 或 `ask` 中的 `WebFetch(domain:claude.ai)` 规则确实适用于 artifact 读取](/docs/zh-CN/permissions#allow-or-deny-every-fetch)。

<h2 id="manage-artifacts-for-your-organization">
  为您的组织管理 artifacts
</h2>

Team 和 Enterprise 计划上的所有者从 [claude.ai 管理设置](https://claude.ai/admin-settings/artifacts) 控制 artifacts。Artifact 内容存储在 Anthropic 运营的基础设施上，仅对发布组织的经过身份验证的成员可见，除非该 artifact 是[公开共享](#control-public-sharing)的。

<h3 id="enable-or-disable-artifacts">
  启用或禁用 artifacts
</h3>

要为整个组织启用或禁用 artifacts，请转到 [**Organization settings > Artifacts**](https://claude.ai/admin-settings/artifacts) 并使用 **Artifacts** 切换。在具有基于角色的访问控制的 Enterprise 计划上，您还可以将 artifacts 限制到特定角色：转到 [**Organization settings > Roles**](https://claude.ai/admin-settings/roles)，编辑角色，并设置 **Artifacts** 权限。

<h3 id="control-connector-calls-from-artifacts">
  控制来自 artifacts 的连接器调用
</h3>

[来自 artifacts 的连接器调用](#pull-live-data-with-mcp-connectors)有自己的切换，与打开或关闭 artifacts 的 **Artifacts** 切换分开。转到 [**Organization settings > Capabilities**](https://claude.ai/admin-settings/capabilities) 并使用 **Enable artifact connectors** 切换。同一切换控制在 claude.ai 对话中创建的 artifacts 的连接器调用。

<h3 id="control-public-sharing">
  控制公开共享
</h3>

在 Team 和 Enterprise 计划上，公开共享默认处于关闭状态。要让成员将 artifacts 发布到任何人都可以查看而无需登录的公开链接，请转到 [**Organization settings > Artifacts**](https://claude.ai/admin-settings/artifacts) 并在 **Artifacts** 切换下打开 **External sharing**。将其关闭会阻止通过现有公开链接的访问，而不会更改每个 artifact 的受众；如果您重新启用它，访问将恢复。

<h3 id="set-a-retention-policy">
  设置保留策略
</h3>

要设置在自动删除之前保留 artifacts 的时间长度，请转到 [**Organization settings > Data and privacy**](https://claude.ai/admin-settings/data-privacy-controls)。您可以为仍然对其作者私有的 artifacts 和已共享的 artifacts 设置单独的保留期。

<h3 id="review-the-audit-log">
  查看审计日志
</h3>

发布、共享和删除 artifact 各自出现在您组织的审计日志中，位于 `claude_artifact_*` 事件类型下，这是用于在 claude.ai 对话中创建的 artifacts 的同一系列。

<h3 id="allowlist-the-viewer-domain">
  将查看器域列入允许列表
</h3>

claude.ai 上的查看器从沙箱 `*.claudeusercontent.com` 源加载每个 artifact。如果您的组织限制出站网络访问，请将该域添加到您的允许列表中，与 `claude.ai` 一起。有关完整列表，请参阅 [网络访问要求](/docs/zh-CN/network-config#network-access-requirements)。

从 [Google Fonts](#improve-the-visual-design) 加载字体的 artifact 也会请求 `fonts.googleapis.com` 和 `fonts.gstatic.com`。两个主机都是可选的。如果您阻止它们，artifacts 将以备用字体呈现。使用快速拒绝而不是静默丢弃来阻止，以便字体请求立即失败，而不是延迟页面的首次呈现。

Artifacts 还可以从 `cdnjs.cloudflare.com`、`cdn.jsdelivr.net`、`cdn.tailwindcss.com`、`code.jquery.com` 和 `unpkg.com` 加载 JavaScript 库（如 React 或图表包），而不能从任何其他外部主机加载。如果您阻止这些主机，artifact 中依赖库的部分将无法工作，与被阻止的字体不同，被阻止的库没有备用方案。在这里也使用快速拒绝，以便被阻止的库请求立即失败，而不是挂起直到超时。

<h3 id="list-and-delete-artifacts-with-the-compliance-api">
  使用 Compliance API 列出和删除 artifacts
</h3>

[Compliance API](https://docs.claude.com/en/api/compliance) 提供端点来列出组织的 artifacts、检索特定版本的内容和删除 artifact：

| 方法 | 端点 |
| :- | :- |
| `GET` | `/v1/compliance/code/artifacts` |
| `GET` | `/v1/compliance/code/artifacts/{artifact_id}/versions/{version_id}` |
| `DELETE` | `/v1/compliance/code/artifacts/{artifact_id}` |

有关请求和响应架构，请参阅 [Compliance API 参考](https://docs.claude.com/en/api/compliance/code/artifacts)。

<h2 id="related-resources">
  相关资源
</h2>

* 浏览与 artifacts 配对的 [提示模式和工作流](/docs/zh-CN/prompt-library)
* 将您重复使用的 artifact 提示转换为 [skill](/docs/zh-CN/skills)，以便您可以将其作为命令调用
* [连接 MCP 服务器](/docs/zh-CN/mcp)，以便 Claude 可以在构建页面时将数据拉入 artifact
