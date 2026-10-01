> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code 如何使用 prompt caching

> Claude Code 自动管理 prompt caching。了解为什么模型切换会触发缓慢的未缓存回合、`/compact` 的成本、为什么 CLAUDE.md 编辑在会话中期不适用，以及如何检查缓存命中率。

Prompt caching 使 Claude Code 更快、更经济高效。没有缓存，API 会在每个回合重新处理您的完整历史记录。有了缓存，它会重用已经处理过的内容，按照[缓存令牌费率](https://platform.claude.com/docs/en/about-claude/pricing)对重新读取进行计费，并仅完全处理已更改的内容。

Claude Code 为您处理 prompt caching，除非您[禁用它](#disable-prompt-caching)。了解 prompt caching 的工作原理仍然很有用，因为某些操作会使缓存失效，使下一个响应更慢、更昂贵，同时它重建缓存。本页涵盖哪些操作会这样做、为什么某些设置等待重启才能应用，以及当使用量看起来很高时如何检查缓存性能。

<h2 id="how-the-cache-is-organized">
  缓存的组织方式
</h2>

每次在 Claude Code 中发送消息时，它都会发出一个新的 API 请求。模型在请求之间不会记住任何内容，因此 Claude Code 会重新发送完整的上下文：系统提示、你的项目上下文、所有之前的消息和工具结果，以及你的新消息。新内容被附加在末尾，这意味着每个请求的大部分内容与前一个请求相同。Prompt caching 是 API 避免重新处理未更改部分的方式。

API 通过将每个请求的开始部分（称为前缀）与最近处理的内容进行匹配来进行缓存。在正常的回合中，前缀是整个前一个请求，只有最新的交互是新的。匹配是精确的，因此前缀中任何地方的更改都会重新计算其后的所有内容。没有按文件或按段的缓存。有关底层机制，请参阅 API 参考中的 [how prompt caching works](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#how-prompt-caching-works)。

<img src="https://mintcdn.com/claude-code/VbDJw--l6T9a9Wvm/images/prompt-caching-prefix.svg?fit=max&auto=format&n=VbDJw--l6T9a9Wvm&q=85&s=f2e8f0b8298a50305fe428ca3f1d1594" className="dark:hidden" alt="Four turns shown as growing horizontal bars. Each turn's request contains everything from the previous turn plus the latest exchange appended at the end. On turns two and three, the unchanged prefix is read from cache and only the new exchange is processed. On turn four, the system prompt changed, so the prefix no longer matches and the entire request is reprocessed and written." width="720" height="454" data-path="images/prompt-caching-prefix.svg" />

<img src="https://mintcdn.com/claude-code/_xqph1dUOslCOwsj/images/prompt-caching-prefix-dark.svg?fit=max&auto=format&n=_xqph1dUOslCOwsj&q=85&s=297dc1c639f0915cae858d0c4b6f3be5" className="hidden dark:block" alt="Four turns shown as growing horizontal bars. Each turn's request contains everything from the previous turn plus the latest exchange appended at the end. On turns two and three, the unchanged prefix is read from cache and only the new exchange is processed. On turn four, the system prompt changed, so the prefix no longer matches and the entire request is reprocessed and written." width="720" height="454" data-path="images/prompt-caching-prefix-dark.svg" />

为了充分利用前缀匹配，Claude Code 对每个请求进行排序，使得在回合之间很少更改的内容首先出现：

| Layer | Content | Changes when |
| - | - | - |
| System prompt | Core instructions, tool definitions | The set of loaded tool definitions changes |
| Project context | CLAUDE.md, auto memory, unscoped rules | Session starts, or after `/clear` or `/compact` |
| Conversation | Your messages, Claude's responses, tool results | Every turn |

对对话层的更改会使系统提示和项目上下文保持缓存。对系统提示的更改会使所有内容失效，因为所有后续内容现在位于不同的前缀后面。第三列给出了常见的触发器，而不是详尽的列表，下面的部分涵盖了完整的集合。

前缀匹配规则解释了本页上的大多数行为。例如，[Plan mode](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode) 和 [skill loading](/docs/zh-CN/skills) 将其指令作为对话消息附加，因此缓存的前缀保持完整。

两个设置不在层表中出现，但仍然影响缓存的内容：

* **Model**：每个模型都有自己的缓存。切换模型会重新计算整个请求，即使内容相同。请参阅下面的 [Switching models](#switching-models)。
* **Effort level**：在大多数模型上，每个努力级别都有自己的缓存，因此在会话中途更改努力级别会重新计算整个请求。在具有 API 密钥或 Claude 订阅的 Opus 5.5、Sonnet 5.5 和 Fable 5.1 上，缓存默认保持完整。请参阅下面的 [Changing effort level](#changing-effort-level)。

<Tip>
  在会话顶部选择你的模型和努力级别，然后在任务之间的自然中断处保存 `/compact`。你在任务中途进行的更改越少，缓存命中率就越高。
</Tip>

<h3 id="where-the-cache-lives">
  缓存的位置
</h3>

缓存发生在服务器端，在为你的模型提供服务的任何基础设施中。位置取决于你的身份验证方式：

* **API key、Claude subscription 或 [Claude Platform on AWS](/docs/zh-CN/claude-platform-on-aws)**：缓存位于 Anthropic 的基础设施中，通过 [Claude API](https://platform.claude.com/docs) 访问
* **Amazon Bedrock 或 Google Cloud 的 Agent Platform**：缓存位于你的云提供商的服务基础设施中
* **Microsoft Foundry**：取决于部署的 [hosting option](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry#hosting-options)。在 Azure 上托管的部署在 Azure 基础设施上提供；在 Anthropic 上托管的部署在 Anthropic 的基础设施上提供
* **Custom `ANTHROPIC_BASE_URL` 或 [LLM gateway](/docs/zh-CN/llm-gateway)**：缓存位于你的请求被转发的地方，缓存是否有效取决于网关

Claude Code 还在对话中途附加系统上下文，例如文件更改通知，并在所有提供商和连接上标记该块以进行缓存，除非你设置了 [`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`](/docs/zh-CN/llm-gateway-protocol#disable-pre-release-capabilities)，在这种情况下该块被发送为未缓存。

在提供商自己的端点、Amazon Bedrock 及其 [Mantle endpoint](/docs/zh-CN/amazon-bedrock#use-the-mantle-endpoint)、Google Cloud 的 Agent Platform 和 Microsoft Foundry 上，缓存该块的方式与 Claude API 相同。

当你的请求通过 [LLM gateway](/docs/zh-CN/llm-gateway)、自定义 `ANTHROPIC_BASE_URL` 或云提供商基础 URL 覆盖（例如 [`ANTHROPIC_BEDROCK_BASE_URL`](/docs/zh-CN/env-vars)）时，缓存的内容取决于网关如何处理 Claude Code 发送的 [`cache_control` markers](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#explicit-cache-breakpoints)：

* **原样转发它们**：该块和你的对话缓存方式与在提供商自己的端点上相同。
* **使用命名 `cache_control` 的 `400` 错误拒绝标记的请求**：Claude Code 重新发送请求，将标记从块移到你的最后一条对话消息上，并在对话的其余部分保持在那里。该块作为未缓存的输入计费；你的对话保持缓存。
* **在返回成功时删除标记**：你的整个对话历史在每个回合上都作为未缓存的输入计费。将块形式的系统内容转换为纯字符串的网关以相同的方式删除标记。

有关每个提供商存储和处理的内容，请参阅 [data usage](/docs/zh-CN/data-usage)。无论缓存位于何处，条目在不活动期间后过期，下面的 [Cache lifetime](#cache-lifetime) 涵盖了 TTL 以及如何延长它。

<h2 id="actions-that-invalidate-the-cache">
  使缓存失效的操作
</h2>

这些操作可能导致下一个请求缓存未命中。您会看到一次速度较慢、成本更高的回合，之后新的前缀会被缓存。一旦您了解它们的成本，大多数操作都可以在任务中途避免。模型切换可能看起来没有成本，直到您注意到随后的速度较慢的回合。

* [切换模型](#switching-models)
* [更改工作量级别](#changing-effort-level)
* [启用快速模式](#turning-on-fast-mode)
* [连接或移除 MCP 服务器](#connecting-or-removing-an-mcp-server)
* [启用或禁用插件](#enabling-or-disabling-a-plugin)
* [拒绝整个工具](#denying-an-entire-tool)
* [压缩对话](#compacting-the-conversation)
* [积累许多图像](#accumulating-many-images)
* [升级 Claude Code](#upgrading-claude-code)

<h3 id="switching-models">
  切换模型
</h3>

每个模型都有自己的缓存。使用 [`/model`](/docs/zh-CN/model-config#setting-your-model) 切换意味着下一个请求会读取整个对话历史记录而没有缓存命中，即使内容相同。

当您在终端运行 `/model` 时，Claude Code 会要求您确认切换，但仅限于缓存仍然温暖且新模型不是产生最后一个响应的模型时。缓存在 Claude Code 在此对话中最后一次发送请求或 Claude 最后一次响应后的一个[缓存 TTL](#cache-lifetime) 内保持温暖。一旦该时间过去，缓存就会过期，因此 Claude Code 会在不询问的情况下进行切换。

在 v2.1.238 之前，Claude Code 不检查缓存 TTL，即使在缓存过期后也会询问。

您也可以通过 [PreModelSwitch hook](/docs/zh-CN/hooks#premodelswitch-decision-control) 要求此确认或跳过它。

[`opusplan` 模型设置](/docs/zh-CN/model-config#opusplan-model-setting)在计划模式下解析为 Opus，在执行期间解析为 Sonnet，因此每个计划模式切换都是一个模型切换并启动新的缓存。

[Fable 模型、Opus 5.5、Sonnet 5.5 和 Opus 5 上的自动模型回退](/docs/zh-CN/model-config#automatic-model-fallback)也是一个模型切换。当安全分类器在具有回退模型的类别中标记请求时，Claude Code 会在该模型上重新运行请求，会话继续进行。

当技能或命令的 frontmatter 命名一个[`model`](/docs/zh-CN/skills#frontmatter-reference)不同于会话当前模型的模型时，该回合也是一个模型切换：下一个请求读取整个对话历史记录而没有缓存命中。会话模型在您的下一个提示时恢复。`context: fork` 技能设置[分叉子代理的模型](/docs/zh-CN/skills#run-skills-in-a-subagent)。

<h3 id="changing-effort-level">
  更改工作量级别
</h3>

在大多数模型上，在会话中途更改[工作量级别](/docs/zh-CN/model-config#adjust-effort-level)意味着下一个请求会读取整个对话历史记录而没有缓存命中。当缓存仍然温暖时，Claude Code 会要求您先确认更改。

在 Opus 5.5、Sonnet 5.5 和 Fable 5.1 上使用 API 密钥或 Claude 订阅时，更改工作量会保持缓存，Claude Code 会在不询问的情况下应用新级别。这不适用于 Amazon Bedrock、Google Cloud 的 Agent Platform 或[Claude 应用网关](/docs/zh-CN/claude-apps-gateway)，或当您设置 [`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`](/docs/zh-CN/llm-gateway-protocol#disable-pre-release-capabilities) 或您的组织具有 HIPAA 配置时。

在 v2.1.260 之前，在 Fable 5.1 上使用 API 密钥或 Claude 订阅更改工作量也会使缓存失效。

<h3 id="turning-on-fast-mode">
  启用快速模式
</h3>

启用[快速模式](/docs/zh-CN/fast-mode)会添加一个请求标头，该标头是缓存键的一部分，因此 Claude Code 发送的启用快速模式的第一个请求会读取整个对话历史记录而没有缓存命中。Claude Code 在回合开始时设置该标头一次，并为整个回合保持它，因此当您在 Claude 工作时启用快速模式时，标头的缓存未命中发生在您下一个回合的第一个请求上。这些未缓存的输入令牌按[快速模式费率](/docs/zh-CN/fast-mode#understand-the-cost-tradeoff)计费，这就是为什么在会话开始时启用它的成本比在长会话深处启用它的成本要低。如果您当前的模型不支持快速模式，启用快速模式也会[切换您的模型](#switching-models)，该切换从运行回合中的下一个请求开始启动新的缓存。

成本每个对话应用一次。在第一个快速模式回合之后，Claude Code 继续发送标头，仅改变请求的速度设置，这不是缓存键的一部分。关闭快速模式、[速率限制后自动回退到标准速度](/docs/zh-CN/fast-mode#handle-rate-limits)以及稍后重新启用它都会保持缓存。如果您在会话中途[用完使用额度](/docs/zh-CN/fast-mode#handle-rate-limits)，Claude Code 会以相同的方式在标准速度下重试每个被拒绝的快速模式请求，因此此回退也会保持缓存。`/clear` 和 `/compact` 会重置此设置，因为它们无论如何都会在这些点重建缓存。

<h3 id="connecting-or-removing-an-mcp-server">
  连接或移除 MCP 服务器
</h3>

工具定义位于系统提示层，因此当请求中的工具定义集在回合之间发生变化时，缓存会失效。切换[顾问工具](/docs/zh-CN/advisor)是一个例外：其定义位于缓存断点之后，因此启用或禁用 `/advisor` 会保持缓存的前缀完整。[MCP 服务器](/docs/zh-CN/mcp)更改是否执行此操作取决于是否[工具搜索](/docs/zh-CN/mcp#scale-with-mcp-tool-search)延迟会话的 MCP 工具，这是支持的模型上的默认设置：

* **工具延迟**：Claude Code 为整个对话保持来自对话第一个请求的工具列表，因此服务器在会话中途连接或断开连接不会干扰已缓存的任何内容。在第一个请求后完成连接的服务器提供其工具作为 Claude 按需加载的延迟定义。
* **工具加载到前缀中**：添加定义会使缓存失效，移除定义也会。这适用于当[工具搜索低于其 `auto` 阈值、被禁用或不可用](/docs/zh-CN/mcp#configure-tool-search)时，例如在 Google Cloud 的 Agent Platform 模型早于 Claude 4.5 代、具有自定义 `ANTHROPIC_BASE_URL` 网关或在 Microsoft Foundry [部署在 Azure 上](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry#hosting-options)一旦 Claude Code 检测到部署拒绝工具搜索时。

没有工具搜索，中途服务器更改是否使缓存失效取决于更改的内容。对于每个更改，此表给出缓存是否保持以及下一个请求中工具定义发生的情况。

| 中途更改 | 缓存 | 下一个请求中的工具定义 |
| - | - | - |
| 服务器连接，或[动态工具更新](/docs/zh-CN/mcp#dynamic-tool-updates)添加工具 | 失效 | 添加新定义 |
| 服务器在您没有采取任何操作的情况下断开连接，例如 stdio 服务器的进程退出 | 保持 | 服务器的定义保持不变。对其工具之一的调用返回错误而不是运行 |
| 远程服务器在连接断开后[自动重新连接](/docs/zh-CN/mcp#automatic-reconnection) | 保持，除非在服务器重新连接时发送的请求添加了 `WaitForMcpServers` 工具，这会使缓存失效一次 | 服务器的定义保持不变。在服务器重新连接时发送的请求可以在对话尚未列出时添加 `WaitForMcpServers`，然后该工具对对话的其余部分保持列出 |
| 您故意移除工具，例如使用[拒绝规则](#denying-an-entire-tool)或通过在 `/mcp` 中禁用其服务器 | 失效 | 定义被移除 |

当您恢复其工具加载到前缀中的对话时，其中一个 MCP 服务器仍然可以在第一个请求发出时连接。如果记录的对话记录了该服务器的工具定义，该请求会按记录包含它们，因此当服务器以相同的工具完成连接时它不会改变。

编辑您的 MCP 配置本身不会改变缓存。新配置仅在重启后生效，这是服务器连接或断开连接的时候。

<h3 id="enabling-or-disabling-a-plugin">
  启用或禁用插件
</h3>

当您启用或禁用[插件](/docs/zh-CN/plugins/overview)时，更改的成本取决于插件提供的组件类型。下面的情况涵盖每个组件类型、Claude Code 何时应用更改以及在同一会话中再次禁用插件时发生的情况。

<h4 id="plugin-components-that-keep-the-cache">
  保持缓存的插件组件
</h4>

Claude Code 永远不会为插件的技能、命令、代理、hooks、监视器或主题使缓存失效。它在现有对话之后附加其内容，因此下一个请求为该内容付费，并仍然从缓存中读取其之前的所有内容。

<h4 id="plugins-that-provide-mcp-servers">
  提供 MCP 服务器的插件
</h4>

当您启用或禁用提供[MCP 服务器](/docs/zh-CN/plugins/components#mcp-servers)的插件时，Claude Code 遵循与[连接或移除 MCP 服务器](#connecting-or-removing-an-mcp-server)相同的规则。

<h4 id="code-intelligence-plugins">
  代码智能插件
</h4>

当您启用[代码智能插件](/docs/zh-CN/plugins/code-intelligence)时，Claude 会获得 [LSP 工具](/docs/zh-CN/tools-reference#lsp-tool-behavior)。

<h4 id="when-plugin-changes-apply">
  插件更改何时应用
</h4>

您在 `/plugin` 菜单中所做的更改会通过 [`/reload-plugins`](/docs/zh-CN/plugins/cli-reference#reload-plugins) 进行，Claude Code 在您关闭菜单时为您运行。您需要付费，无论是附加公告还是完整重新读取，都在更改应用后的第一个回合。Claude Code 也可以自行应用更改：

* 对于具有 `command` 源的插件，Claude Code [可以自行重新加载插件](/docs/zh-CN/plugins/loading#when-a-command-source-re-runs)。
* 当您[从 `/plugin` 界面安装插件](/docs/zh-CN/plugins/install#install-a-plugin)时，Claude Code 可以在安装期间激活它。安装摘要会告诉您它是否这样做了。
* 当您在 v2.1.246 或更高版本上使用 `/cd` [移动会话](/docs/zh-CN/permissions#move-the-session-to-another-directory)时，Claude Code 会在移动过程中应用新目录的设置启用的插件，而不会出现保持 `/reload-plugins` 的完整重新读取警告。
* 在交互式会话中，当您在使用 `--plugin-dir` 传递的[插件文件夹](/docs/zh-CN/plugins/create#load-a-directory-or-archive-for-one-session)中添加或移除插件时，更改会立即应用。如果应用它会触发完整重新读取，Claude Code 会保持更改并显示通知以运行 `/reload-plugins`。需要 Claude Code v2.1.265 或更高版本。

当 `/reload-plugins` 运行且重新加载会触发完整重新读取时，Claude Code 会显示警告并不应用重新加载。运行 `/reload-plugins --force` 以无论如何应用它。

`/reload-plugins` 也在没有交互式终端的会话中运行，例如桌面应用、Agent SDK 和[非交互式模式](/docs/zh-CN/headless)与 `-p`，当您直接将其输入到会话中时。需要 Claude Code v2.1.260 或更高版本。

在这些会话中，重新加载应用除了插件 MCP 服务器更改之外的所有内容，这些[在您的下一个会话中生效](/docs/zh-CN/plugins/cli-reference#reload-plugins)，因此永远不会在会话中途成本完整重新读取。

<h4 id="plugins-you-enable-and-then-disable-in-one-session">
  您在一个会话中启用然后禁用的插件
</h4>

当您禁用您在会话中较早启用的插件时，Claude Code 会恢复之前的请求形状。如果该前缀仍在其[缓存生命周期](#cache-lifetime)内，下一个请求会读取较旧的缓存条目而不是重建。

<h3 id="denying-an-entire-tool">
  拒绝整个工具
</h3>

如果您添加一个裸工具名称如 `Bash` 或 `WebFetch` 作为[拒绝规则](/docs/zh-CN/permissions#manage-permissions)，Claude 无法从您的下一个请求开始调用该工具，无论您是通过 `/permissions` 添加规则还是通过[直接编辑设置文件](/docs/zh-CN/settings#when-edits-take-effect)。这包括您在回合中途通过 `/permissions` 添加的规则。

当[工具搜索](/docs/zh-CN/mcp#scale-with-mcp-tool-search)处于活动状态时，这是支持的模型上的默认设置，请求的工具定义不会改变，缓存的前缀会存活。当工具搜索不可用或被禁用时，Claude Code 会从下一个请求中移除定义，这会使缓存失效，稍后移除规则也会。

只有在工具名称位置匹配的拒绝规则才会以这种方式阻止工具：裸工具名称、等效的 `Bash(*)` 形式或[工具名称 glob](/docs/zh-CN/permissions#tool-name-wildcards) 如 `"*"`。匹配仅 MCP 工具的 glob，例如 `"mcp__*"`，以相同的方式阻止这些工具。作用域拒绝规则如 `Bash(rm *)`，以及所有允许和询问规则，不会改变 Claude 看到的工具。Claude Code 在 Claude 尝试调用时检查它们，保持前缀完整。

<h3 id="compacting-the-conversation">
  压缩对话
</h3>

[压缩](/docs/zh-CN/context-window#what-survives-compaction)用摘要替换您的消息历史记录。根据设计，这会使对话层失效，因为下一个请求有一个新的、更短的历史记录，不与旧的共享前缀。Claude Code 重用系统提示层，除非对话是[在保持会以其他方式改变的系统提示的同时恢复的](#resuming-a-session)；在这种情况下，第一次压缩会切换到当前提示，该层重建一次。它从磁盘重新加载项目上下文，仅当 CLAUDE.md 和内存自会话开始以来未改变时才缓存命中。

为了生成摘要，Claude Code 发送一个单独的请求，其系统提示、工具和历史记录与您的对话相同，加上作为最终用户消息附加的摘要指令。当缓存温暖时，该请求从缓存中读取您的前缀，因此中途 `/compact` 的成本是上下文大小建议的一小部分，并花费大部分时间生成摘要。

在超过[缓存生命周期](#cache-lifetime)的中断后，没有缓存可读，因此摘要请求将重新处理完整历史记录作为未缓存的输入。这就是为什么当您[恢复旧会话](/docs/zh-CN/sessions#resume-from-a-summary)时 `/compact` 成本最高。在温暖和冷的情况下，压缩后的回合仅为更短的摘要重建对话缓存，因此该回合不是缓慢的部分。

<Tip>
  当您丢弃的上下文是您不再需要的内容时，压缩对您有利。要选择其开销发生的时间，请在工作中的自然中断处（例如任务之间）运行 `/compact`，而不是等待自动压缩在任务中途触发。如果您走上了一条想要完全放弃的路径，[`/rewind`](#rewinding-the-conversation)到较早的回合。重新绕回截断回到已缓存的前缀，而不是像压缩那样构建新的。
</Tip>

<h3 id="accumulating-many-images">
  积累许多图像
</h3>

API 限制每个请求可以携带多少图像和 PDF。有关当前数字，请参阅 API 文档中的[请求限制](https://platform.claude.com/docs/en/build-with-claude/vision#request-limits)。Claude Code 也限制请求中图像和 PDF 的总大小，因此大型屏幕截图比小型屏幕截图更快达到限制。

当下一个请求会超过任一限制时，Claude Code 会从它发送的内容中移除一批最旧的图像和 PDF，这为更多内容腾出空间，然后才需要再次移除任何内容。Claude 无法再看到移除的图像。如果 Claude 再次需要其中一个，请再次共享它。

移除图像会改变保存它们的消息，因此下一个请求会从这些消息中最早的开始重新处理对话。因为 Claude Code 一次移除一批，您会看到每批一个较慢的回合，而不是每个新屏幕截图一个。

<h3 id="upgrading-claude-code">
  升级 Claude Code
</h3>

新的 Claude Code 版本通常会更新系统提示或工具定义，因此升级后您启动的第一个对话从顶部构建其缓存。[自动更新](/docs/zh-CN/setup#auto-updates)在后台下载新版本，但在下一次启动时应用它们，从不在会话中途，因此您会看到这是重启后的未缓存第一个回合，而不是会话中的惊喜。设置 `DISABLE_AUTOUPDATER=1` 以控制何时应用升级。

<Note>
  有关恢复您在升级前启动的对话的成本，请参阅[恢复会话](#resuming-a-session)。
</Note>

<h2 id="actions-that-keep-the-cache">
  保持缓存的操作
</h2>

这些操作要么追加到对话的末尾，要么根本不触及请求。其中一些操作（例如编辑 CLAUDE.md）保持缓存的原因与该更改在运行会话中不会生效直到 `/clear`、`/compact` 或重启的原因相同。

* [编辑存储库中的文件](#editing-files-in-your-repository)
* [在会话中编辑 CLAUDE.md](#editing-claude-md-mid-session)
* [更改权限模式](#changing-permission-mode)
* [更改输出样式](#changing-output-style)
* [调用 skills 和命令](#invoking-skills-and-commands)
* [运行 `/recap`](#running-%2Frecap)
* [回溯对话](#rewinding-the-conversation)
* [生成子代理](#subagents-and-the-cache)

<h3 id="editing-files-in-your-repository">
  编辑存储库中的文件
</h3>

文件内容仅在 Claude 读取文件时进入上下文，而读取操作会追加到对话中。编辑 Claude 之前读过的文件不会追溯性地改变历史记录中的早期读取。相反，Claude Code 会追加一条 [`<system-reminder>`](/docs/zh-CN/glossary#system-reminder) 注明文件已更改，Claude 会在需要时重新读取该文件。

<h3 id="editing-claude-md-mid-session">
  在会话中编辑 CLAUDE.md
</h3>

您的项目根目录和用户级 CLAUDE.md 文件在会话开始时读取一次并保存在内存中。在会话中编辑它们不会使缓存失效，但编辑也不会应用。Claude 继续使用在会话开始时加载的版本。新内容在下一次 `/clear`、`/compact` 或重启时加载。

[子目录中的嵌套 CLAUDE.md 文件](/docs/zh-CN/memory)和[带有 `paths:` frontmatter 的规则](/docs/zh-CN/memory#path-specific-rules)稍后加载，当 Claude 首次读取匹配的文件时。在加载前编辑它确实会生效。加载后，内容成为对话历史的一部分，所以中途编辑不会追溯性地改变它。

<h3 id="changing-permission-mode">
  更改权限模式
</h3>

在[权限模式](/docs/zh-CN/permission-modes)之间切换，例如从手动模式切换到接受编辑，不会改变系统提示或工具定义，所以模式更改是缓存安全的。例外是使用 [`opusplan`](/docs/zh-CN/model-config#opusplan-model-setting) 模型设置的计划模式，它在您进入或离开计划模式时在 Opus 和 Sonnet 之间切换模型。这使得模式切换成为[模型切换](#switching-models)。

<h3 id="changing-output-style">
  更改输出样式
</h3>

当您在会话中使用 [`/output-style`](/docs/zh-CN/output-styles#change-your-output-style)、`/config` 或 `outputStyle` 设置切换[输出样式](/docs/zh-CN/output-styles)时，Claude 从您的下一条消息开始使用新样式。Claude Code 将新样式的指令作为对话中的消息传递，所以该请求仍然从缓存中读取系统提示和早期对话。

在 v2.1.251 之前，中途样式切换保持缓存但直到您运行 `/clear` 或启动新会话时才应用。

<h3 id="invoking-skills-and-commands">
  调用 skills 和命令
</h3>

[Skills](/docs/zh-CN/skills) 和[命令](/docs/zh-CN/commands)在调用点将其指令作为用户消息注入。对话中早期的任何内容都不会改变。frontmatter 中命名 `model` 的 skill 或命令可以是该轮的[模型切换](#switching-models)。

<h3 id="running-/recap">
  运行 `/recap`
</h3>

[`/recap`](/docs/zh-CN/interactive-mode#session-recap) 生成一个摘要以在您的终端中显示。与 `/compact` 不同，它将摘要作为命令输出追加而不是替换您的消息历史，所以缓存的前缀保持完整。

<h3 id="rewinding-the-conversation">
  回溯对话
</h3>

[`/rewind`](/docs/zh-CN/checkpointing) 将您的对话截断回到较早的轮次。剩余的历史是缓存在该点构建时的相同内容，系统提示和项目上下文层保持不变，所以下一个请求会命中较早的缓存条目。从那时起的每一轮都读过该前缀，即使原始轮次比 TTL 更久远，也保持了该条目的活跃。

恢复文件检查点与对话一起对缓存没有单独的影响。文件内容仅在 Claude 读取文件时进入上下文，与[编辑存储库中的文件](#editing-files-in-your-repository)相同。

<h2 id="resuming-a-session">
  恢复会话
</h2>

当你[恢复会话](/docs/zh-CN/sessions#resume-a-session)时，Claude Code 会重新发送整个对话，请求会从缓存中读取其前缀中未更改且仍在[缓存生命周期](#cache-lifetime)内的任何部分。本页顶部的层表说明了每一层的变化。

系统提示词会在[Claude Code 升级](#upgrading-claude-code)后或在恢复时使用不同的[`--append-system-prompt`](/docs/zh-CN/cli-reference#system-prompt-flags)文本时发生变化。默认情况下，恢复的对话会保持其启动时的系统提示词，因此其历史记录仍然位于相同的提示词后面，更改会在对话被压缩或在新对话中生效。[恢复的对话中的系统提示词标志](/docs/zh-CN/cli-reference#system-prompt-flags-in-resumed-conversations)涵盖了系统提示词标志在恢复的对话中的情况。

<h2 id="cache-lifetime">
  缓存生命周期
</h2>

缓存的前缀在不活动期间后过期。每个命中缓存的请求都会重置计时器，所以只要您继续工作，缓存就保持温暖。在足够长的间隙之后，下一个请求重新计算完整输入并重新建立缓存，这就是为什么步开后的第一个回合可能明显更慢。

在 Pro 或 Max 计划上，当您在长时间休息后恢复大型会话时，Claude Code [提供从摘要恢复](/docs/zh-CN/sessions#resume-from-a-summary)，以便后续请求不会携带完整历史记录。

生存时间 (TTL) 控制缓存存活的间隙有多长。API 提供两个：五分钟 TTL 和[一小时 TTL](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#1-hour-cache-duration)，它通过更长的中断保持缓存温暖，但[以更高的速率计费缓存写入](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pricing)。较长的 TTL 在您让会话空闲并返回到它时很有帮助，因为您跳过了过期前缀成本的重新处理。对于从不空闲超过五分钟的短工作突发，它成本更高，其中更高的写入速率适用，较长的缓存生命周期未被使用。

<h3 id="which-ttl-each-request-gets">
  每个请求获得哪个 TTL
</h3>

Claude Code 按请求决定 TTL，每个请求都属于以下两个固定桶之一：

* **主对话**：您的交互式回合、非交互式 `-p` 运行和 Agent SDK 回合，加上 Claude Code 与它们内联运行的助手
* **其他所有内容**：Claude Code 在该对话之外进行的请求，例如[子代理](/docs/zh-CN/sub-agents)、[工作流](/docs/zh-CN/workflows)、进程内[队友](/docs/zh-CN/agent-teams)、分支、压缩和会话标题

除非您自己选择 TTL，否则 Claude Code 仅在您计划包含的使用范围内的 Claude 订阅上请求一小时 TTL。在那里，它为主对话请求一小时，加上 Anthropic 在服务器端控制的一小组助手请求。此表给出了两种计费方式下每个桶的默认 TTL。

| 请求桶 | Claude 订阅，在计划使用范围内 | 使用额度、API 密钥或云提供商 |
| - | - | - |
| 主对话 | 一小时 | 五分钟 |
| 其他所有内容 | 五分钟，除了服务器控制的助手请求获得一小时 | 五分钟 |

一旦您超过计划的使用限制，Claude Code 使用[使用额度](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)，您需要为该使用付费，所以 Claude Code 将主对话降低到更便宜的五分钟 TTL。要在那里保持一小时 TTL，[自己选择 TTL](#choose-the-ttl-yourself)。

<h3 id="choose-the-ttl-yourself">
  自己选择 TTL
</h3>

您可以为任一桶设置 TTL。每个控制采用 `5m` 或 `1h`，Claude Code 忽略任何其他值。

* **主对话**：[`promptCacheTtl`](/docs/zh-CN/settings-reference#promptcachettl) 设置，或 `CLAUDE_CODE_PROMPT_CACHE_TTL` [环境变量](/docs/zh-CN/env-vars)
* **其他所有内容**：[`subagentPromptCacheTtl`](/docs/zh-CN/settings-reference#subagentpromptcachettl) 设置，或 `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL` 环境变量

两个设置和两个环境变量都需要 Claude Code v2.1.242 或更高版本。如果您使用 API 密钥登录或使用云提供商，将 `promptCacheTtl` 设置为 `1h` 以为主对话提供一小时缓存。其外的请求保持五分钟默认值，直到您也为该桶选择 TTL。

当多个控制适用时，Claude Code 按此顺序采用第一个匹配：

1. `FORCE_PROMPT_CACHING_5M=1`，为两个桶强制五分钟
2. 桶的环境变量
3. 桶的设置
4. 对于子代理的请求，子代理的 [`experimental` frontmatter 字段](/docs/zh-CN/sub-agents#supported-frontmatter-fields)中的 `cacheTtl` 值，需要 Claude Code v2.1.248 或更高版本。当您的 Claude 订阅使用使用额度时，Claude Code 忽略那里的 `1h`
5. `ENABLE_PROMPT_CACHING_1H=1`，为两个桶请求一小时
6. [请求桶的默认值](#which-ttl-each-request-gets)

当您调试缓存行为、比较两个 TTL 或覆盖在[托管设置](/docs/zh-CN/managed-settings)中设置的较长 TTL 时，设置 `FORCE_PROMPT_CACHING_5M=1`。

要确认您的主对话的缓存写入使用了哪个 TTL，运行 `claude -p "hello" --output-format json` 并读取结果中的 `usage.cache_creation`。Claude Code 在 `ephemeral_1h_input_tokens` 下报告一小时缓存写入，在 `ephemeral_5m_input_tokens` 下报告五分钟缓存写入。

通过您使用 `ANTHROPIC_BASE_URL` 设置的 LLM 网关，部分一小时请求在 `anthropic-beta` 标头中传输，所以配置网关以[原样转发该标头](/docs/zh-CN/llm-gateway-protocol#request-headers)。一小时 TTL 在[Claude 应用网关](/docs/zh-CN/claude-apps-gateway#availability-and-limitations)上不可用。在 Amazon Bedrock 上，prompt caching 支持、最小可缓存前缀长度和一小时 TTL 可用性都因模型而异。如果缓存令牌计数保持为零，请检查 Amazon Bedrock 文档中的[支持的模型、区域和限制](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html#prompt-caching-models)。

<h2 id="cache-scope">
  缓存范围
</h2>

在 Claude Code 中，缓存有效地限定在一台机器和目录。系统提示嵌入了您的自动内存路径，对话以工作目录、平台、shell 和 OS 版本的公告开始。因此，两个不同目录中的会话构建不同的前缀并错过彼此的缓存。

您在同一目录中并行运行的会话构建匹配的前缀并读取彼此的缓存。顺序会话仅当启动时的 git 状态快照匹配时才共享前缀，因为每个对话也携带该快照中的分支和最近的提交。

底层 API 缓存更广泛。缓存在组织之间隔离，在某些提供商上，[在组织内的工作区之间隔离](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#cache-storage-and-sharing)。在这些边界内，任何两个具有相同模型和前缀的请求读取相同的缓存。对于运行自动化流程队列的 Agent SDK 调用者，请参阅[改进跨用户和机器的 prompt caching](/docs/zh-CN/agent-sdk/modifying-system-prompts#improve-prompt-caching-across-users-and-machines)以将自动内存位置移出系统提示并跨用户和机器共享系统提示的缓存条目。

<h2 id="check-cache-performance">
  检查缓存性能
</h2>

缓存性能显示为 API 在每个响应上报告的两个令牌计数。实时观看它们的最直接方式是读取 `current_usage` 对象的[状态行脚本](/docs/zh-CN/statusline)：

| 字段 | 含义 |
| - | - |
| `cache_creation_input_tokens` | 在此回合写入缓存的令牌，按缓存写入速率计费 |
| `cache_read_input_tokens` | 在此回合从缓存提供的令牌，按模型的[缓存令牌速率](https://platform.claude.com/docs/en/about-claude/pricing)计费，低于标准输入速率 |

高读取与创建比率意味着缓存工作良好。如果创建在回合之间保持高位，您的前缀中有什么在改变。[使缓存失效的操作](#actions-that-invalidate-the-cache)部分列出了常见原因。

为了获得每个会话的摘要，运行 `/usage`。在主对话的第一个响应之后，Claude Code 会在会话块中添加一个[`Prompt cache (main)` 行](/docs/zh-CN/costs#prompt-cache-statistics)，显示会话的命中率、未命中计数以及缓存现在是否处于热状态。状态行脚本可以从[`prompt_cache` 对象](/docs/zh-CN/statusline#prompt-cache-fields)读取相同的数字。两者都需要 Claude Code v2.1.251 或更高版本。

当 Claude Code 能够识别时，`Prompt cache (main)` 行还会命名最后一次未命中的可能原因，例如 `likely cause: tool definitions changed`。可能原因文本需要 Claude Code v2.1.260 或更高版本。

为了在整个组织中获得可见性，OpenTelemetry 导出器报告每个用户和会话的缓存读取和创建令牌。有关指标和事件属性参考，请参阅[监控使用](/docs/zh-CN/monitoring-usage)。

<h2 id="subagents-and-the-cache">
  子代理和缓存
</h2>

[子代理](/docs/zh-CN/sub-agents)启动自己的对话，具有自己的系统提示和工具集，与父代的分开。它的第一个请求不读取父代的缓存，因为两个前缀不同，并在自己的回合中预热自己的缓存。子代理不在主对话[TTL 桶](#which-ttl-each-request-gets)之内，所以即使在订阅上也能获得五分钟，直到你[选择更长的时间](#choose-the-ttl-yourself)。

父代的缓存不受影响。从父代的一侧，子代理的调用和结果附加到对话，保留父代的前缀完整。

[分叉](/docs/zh-CN/sub-agents#fork-the-current-conversation)相比之下，完全继承父代的系统提示、工具和对话历史记录，所以其第一个请求读取父代的缓存。

其他请求也可以读取较早请求缓存的前缀：

* **会话副本**：你[使用 `/fork` 复制的会话](/docs/zh-CN/agent-view#copy-the-session-with-%2Ffork)在复制的对话末尾作为消息接收其隔离指令，所以原始对话构建的缓存保持完整。
* **压缩**：[压缩对话](#compacting-the-conversation)中描述的摘要调用使用相同的前缀共享方法。
* **恢复的子代理**：当 Claude [恢复子代理](/docs/zh-CN/sub-agents#resume-subagents)时，恢复运行的第一个请求可以读取原始运行预热的缓存。
* **工作流扇出**：在[工作流扇出](/docs/zh-CN/workflows#prompt-caching-in-a-fan-out)中，相同前缀的代理，Claude Code 默认将除第一个外的所有代理保留最多 5 秒，所以它们的第一个请求可以读取第一个代理缓存的前缀。

<h2 id="disable-prompt-caching">
  禁用 prompt caching
</h2>

禁用缓存在使用特定模型或提供商调试缓存行为时偶尔很有用。要关闭它，请将以下环境变量之一设置为 `1`：

| 变量 | 效果 |
| - | - |
| `DISABLE_PROMPT_CACHING` | 对所有模型禁用 |
| `DISABLE_PROMPT_CACHING_HAIKU` | 仅对默认 Haiku 模型禁用 |
| `DISABLE_PROMPT_CACHING_SONNET` | 仅对默认 Sonnet 模型禁用 |
| `DISABLE_PROMPT_CACHING_OPUS` | 仅对默认 Opus 模型禁用 |
| `DISABLE_PROMPT_CACHING_FABLE` | 仅对 Fable 禁用 |

`DISABLE_PROMPT_CACHING_HAIKU` 适用于默认 Haiku 模型，即 `haiku` 别名解析到的模型。它在该模型运行的任何地方禁用缓存，包括当它是您的主模型时的主对话。覆盖主对话需要 Claude Code v2.1.283 或更高版本。

该变量还涵盖您使用已弃用的 `ANTHROPIC_SMALL_FAST_MODEL` 变量设置的后台模型，当该模型与您的主模型不同时。

您固定为主模型的不同 Haiku 版本保持缓存；设置 `DISABLE_PROMPT_CACHING` 以禁用其缓存。

`DISABLE_PROMPT_CACHING_SONNET` 和 `DISABLE_PROMPT_CACHING_OPUS` 分别适用于 `sonnet` 或 `opus` 别名解析到的模型。如果您将任何其他 Sonnet 或 Opus 模型 ID 设置为主模型，该模型保持缓存。例如，`claude-sonnet-5` 上的会话保持缓存，而 `sonnet` 解析到 `claude-sonnet-5-5`。要禁用该模型的缓存，请设置 `DISABLE_PROMPT_CACHING`。

要在整个组织中设置缓存策略，请将这些或[TTL 变量](#cache-lifetime)中的任何一个放在[托管设置](/docs/zh-CN/managed-settings)的 `env` 块中。对于正常使用，保持缓存启用。

<h2 id="related-resources">
  相关资源
</h2>

* [从构建 Claude Code 中学到的经验：Prompt caching 就是一切](https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything)：Plan Mode、延迟工具加载和压缩的设计原理
* [探索上下文窗口](/docs/zh-CN/context-window)：什么加载到上下文中以及何时加载
* [减少令牌使用](/docs/zh-CN/costs#reduce-token-usage)：超越缓存的策略，用于管理上下文大小
* [跟踪和减少成本](/docs/zh-CN/agent-sdk/cost-tracking)：Agent SDK 调用者的缓存令牌跟踪和 TTL 配置
* [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)：底层 API 机制、断点和定价
