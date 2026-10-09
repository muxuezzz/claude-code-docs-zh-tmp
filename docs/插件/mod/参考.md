> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# mod 参考

> Claude Code mod 的完整参考：hook 模块布局、事件、mods API 方法、渲染位置、按使用入口划分的元素、限制和设置。

查阅 [mod](/docs/zh-CN/plugins/mods/overview) 可以处理的任何事件、可以调用的任何 mods API 方法，或可以在其中绘制的任何渲染位置，适用于 v2.1.290 起的 Claude Code CLI 和 Desktop 应用。每个条目给出名称和一行描述，如有相应的指南章节，还会链接到该章节。

<Note>
  完整的参考是 Claude Code 的 [mod TypeScript 声明](https://github.com/anthropics/claude-code/blob/main/mods/types/claude-code.d.ts)，其中描述了每个事件、方法和元素，并附有示例。GitHub 上的副本可能比您安装的 Claude Code 版本更旧。两者不一致时，请以 [Claude Code 为您的版本写入的副本](/docs/zh-CN/plugins/mods/create#get-the-types-for-your-build)为准。
</Note>

<h2 id="files">
  文件
</h2>

mod 是一个包含以下文件的插件目录：

| 文件 | 必需 | 内容 |
| :- | :- | :- |
| `.claude-plugin/plugin.json` | 是 | 插件[清单](/docs/zh-CN/plugins/manifest-reference)。mod 不会添加任何必需字段。 |
| `hooks/hooks.json` | 是 | `modules`：一个数组，包含一个指向 hook 模块的路径（相对于此文件），如 `"modules": ["./register.js"]`。也可以在 `hooks` 下包含[设置 hook](/docs/zh-CN/hooks)。 |
| hook 模块，例如 [`hooks/register.js`](/docs/zh-CN/plugins/mods/create#write-a-mod-yourself) | 是 | mod 的入口点。导出 `register(on, options)`。文件名以 `.js`、`.mjs`、`.cjs`、`.jsx`、`.ts`、`.mts`、`.cts` 或 `.tsx` 结尾。是一个 ES 模块。 |
| [`types/index.d.ts`](/docs/zh-CN/plugins/mods/interface#declare-the-values)，由清单中的 `types` 指定 | 当 mod 使用 `$.state` 或向 mods API 添加命名空间时 | 声明 `PluginState` 值以及 mod 添加的任何命名空间 |
| 名称以 `.test.ts` 或 `.test.tsx` 结尾的文件 | 否 | [`claude plugin test`](/docs/zh-CN/plugins/mods/test#write-a-test) 运行的测试 |

`register` 接收 `on` 和 `options`。`options` 包含清单所声明的 [`userConfig`](/docs/zh-CN/plugins/components#user-configuration) 字段的值，并已填入默认值。

<h2 id="the-hook-function">
  hook 函数
</h2>

mod 通过在 `register` 内调用 `on` 来注册它的每个 hook（即事件处理程序）。`on` 接受事件名称、一个可选的[匹配器](/docs/zh-CN/plugins/mods/events#filter-which-events-a-hook-handles)（即对事件字段的过滤条件）以及 hook，如 `on('tool.call', { tool: 'Bash' }, async ($, e, next) => next(e))`。`on` 返回一个注册对象，它只有一个方法 `.catch(handler)`，用于设置该 hook 的[错误处理程序](/docs/zh-CN/plugins/mods/events#handle-a-hook-that-fails)。

| 参数 | 说明 |
| :- | :- |
| [`$`](/docs/zh-CN/plugins/mods/events#how-a-hook-handles-an-event) | mods API：[mods API 方法](#mods-api-methods)中的所有方法。每次调用都要完整写出，先写命名空间再写方法，如 `$.fs.read('notes.md')`。 |
| [`e`](/docs/zh-CN/plugins/mods/events#how-a-hook-handles-an-event) | 事件的输入，为深度冻结的纯数据。要更改它，请将副本传给 `next`。 |
| [`next(e)`](/docs/zh-CN/plugins/mods/events#how-a-hook-handles-an-event) | 下一个处理程序，类似中间件。先运行此 hook 之后的 hook，再运行 Claude Code 的行为。解析为事件的结果。 |
| [`next.signal`](/docs/zh-CN/plugins/mods/api#stop-background-work) | 一个 `AbortSignal`，在事件被放弃时中止 |
| `next.origin` | 触发该事件者的 `{ plugin, tier }`。Claude Code 自身为 `{ plugin: 'engine', tier: 'core' }`。mod 的 `tier` 是它在 [mod 运行顺序](/docs/zh-CN/plugins/mods/events#the-order-mods-run-in)中的优先级组：`prepend`、`user`、`append` 或 `builtin`。 |
| `next.budget` | hook 的时间限制（以毫秒为单位）：`next.budget.ms` 是总限制，`next.budget.remainingMs` 是当前剩余时间 |
| `next.to(e, tier)` | 跳到后面的层级，即 `append`、`builtin` 或 `core`。`next.to(e, 'append')` 会跳过用户安装的 mod。只有 `prependPlugins` 或 `appendPlugins` 中的 mod 才能调用它。 |
| `next.error` | 仅在 `.catch` 处理程序中可用。hook 失败时，`kind` 为 `throw` 或 `timeout`，`message` 是错误文本。当 hook 因事件来自其自身某个 mods API 调用内部而被跳过时，`kind` 为 `re-entry`；如果触发该事件的是另一个 mod 添加到 mods API 的方法，则 `cause` 为 `lent`。`re-entry` 和 `cause` 需要 Claude Code v2.1.292 或更高版本。 |
| `next.called` | 仅在 `.catch` 处理程序中可用。当 hook 已调用 `next` 时为 `true`。 |

<h2 id="events">
  事件
</h2>

事件按其涉及的内容分组，每个事件都列出了触发时机以及其上的 hook 可以返回的内容。`turn.step` 和 `process.spawn` 上的 hook 是异步生成器，其他 hook 是异步函数。

每个表格的最后一列使用简写。`next(e)` 原样传递事件。`next({ ...e, text })` 传递一个更改了指定字段的副本，如 `next({ ...e, text: e.text.trim() })`。对象表示不调用 `next` 而直接应答该事件，而 `reason` 之类的词代表您编写的字符串，如 `{ deny: 'Use the file tools.' }`。

<h3 id="tools">
  工具
</h3>

工具事件围绕 Claude 发出的每个工具调用触发，涵盖从 Claude 读取的描述到是否运行该调用的决定：

| 事件 | 触发时机 | hook 可以返回 |
| :- | :- | :- |
| [`tool.call`](/docs/zh-CN/plugins/mods/events#guard-or-change-a-tool-call) | 工具即将运行 | `next(e)`、`{ deny: reason }` 或 `{ result }` |
| [`tool.check`](/docs/zh-CN/plugins/mods/events#where-settings-hooks-run-in-the-order) | Claude Code 在 `tool.call` 和 `PreToolUse` hook 之后决定是否允许运行某个工具调用。`next(e)` 解析为规则、权限模式和这些 hook 得出的决定。 | `{ decision }`，其值为 `allow`、`ask` 或 `deny` |
| `tool.describe` | 每个工具一次，在其描述首次发送给 Claude 时 | `{ description }`，可选择将 `isDeferred` 设为 `true` 以将该工具置于[工具搜索](/docs/zh-CN/mcp#scale-with-mcp-tool-search)之后，或设为 `false` 以预先加载它 |

<h4 id="agent-and-organization-fields-on-tool-check">
  `tool.check` 上的 Agent 和组织字段
</h4>

在 `tool.check` hook 中，读取以下字段可区分子代理的调用与主对话的调用，并查看您的组织是否要求对某个连接器工具进行批准：

* **`e.agentId`**：当[子代理](/docs/zh-CN/sub-agents)或[进程内队友](/docs/zh-CN/agent-teams#choose-a-display-mode)发出调用时设置，由主对话发出调用时则不存在
* **`e.ceiling`**：对于您的组织设为 `ask` 的连接器工具，其值为 `ask`，适用于[该设置能传达到 Claude Code 的会话](/docs/zh-CN/mcp#organization-controls-on-connector-tools)

在 `tool.check` 上，`e.agentId` 和 `e.ceiling` 需要 Claude Code v2.1.290 或更高版本。

<h3 id="prompts-and-what-claude-reads">
  提示词以及 Claude 读取的内容
</h3>

提示词事件涵盖用户输入的文本，以及 Claude Code 自行发送给 Claude 的文本，例如系统提示词和提醒：

| 事件 | 触发时机 | hook 可以返回 |
| :- | :- | :- |
| [`prompt.submit`](/docs/zh-CN/plugins/mods/events#rewrite-or-add-to-a-prompt) | 提交提示词时 | `next({ ...e, text })`、`next({ ...e, context })` 或 `{ drop: reason }` |
| `prompt.fill`, `prompt.suggest` | 文本即将作为草稿或暗色建议进入输入框 | 更改了文本的 `next(e)` |
| `prompt.edit` | 用户编辑输入框 | `next(e)` |
| `prompt.compose` | Claude Code 渲染系统提示词 | `{ sections }`，一个按发送顺序排列的 `{ id, text, scope }` 列表 |
| [`prompt.section`](/docs/zh-CN/plugins/mods/events#rewrite-or-add-to-a-prompt) | 系统提示词的每个命名部分一次。`e.name` 是该部分在 `prompt.compose` 中的 `id`。 | `{ text }`，或 `{ text: null }` 以省略该部分 |
| [`prompt.context`](/docs/zh-CN/plugins/mods/events#rewrite-or-add-to-a-prompt) | 每个对话一次，用于随第一条消息发送的上下文 | `{ blocks }` |
| `prompt.attachment` | Claude Code 为 Claude 添加一条它自己的消息，例如提醒。`e.type` 指明消息类型；对于类型声明中已声明的类型，`e.detail` 包含编写该文本所依据的事实。 | `{ text }`，或 `{ text: null }` 以省略它 |
| `prompt.mention` | Claude Code 即将读取提示词中 @ 提及的文件。需要 Claude Code v2.1.290 或更高版本。 | `next({ ...e, path })` 以读取其他文件，或 `{ deny: reason }` |
| [`skill.prompt`](/docs/zh-CN/plugins/mods/events#rewrite-or-add-to-a-prompt) | skill 的文本为 Claude 展开时 | `{ text }` |
| `attribution.text` | Claude Code 撰写提交或 Pull Request 的署名文本时 | `{ text }` |

<h3 id="commands-and-configuration">
  命令和配置
</h3>

命令和配置事件在命令运行或被列出时，以及 `/config` 行显示或更改时触发：

| 事件 | 触发时机 | hook 可以返回 |
| :- | :- | :- |
| [`command.run`](/docs/zh-CN/plugins/mods/api#add-a-command) | 命令即将运行 | `{ text }`、`{}` 或 `next(e)` |
| `command.describe` | 每个命令一次，用于命令列表 | `{ description, argumentHint, isHidden }` |
| `config.set` | `/config` 行即将更改 | `next({ ...e, value })` 或 `{ deny: reason }` |
| `config.describe` | 每个 `/config` 行一次 | `{ label, description, isHidden }` |

<h3 id="turns">
  轮次
</h3>

轮次事件从头到尾跟踪一次回答，包括其中每个发往模型的请求：

| 事件 | 触发时机 | hook 可以返回 |
| :- | :- | :- |
| [`turn.start`](/docs/zh-CN/plugins/mods/events#follow-a-turn) | 轮次开始 | `next(e)` |
| [`turn.step`](/docs/zh-CN/plugins/mods/events#follow-a-turn) | 一个请求即将发往模型 | `yield* next(e)`，或 `next({ ...e, model })`、`next({ ...e, effort })` |
| [`turn.complete`](/docs/zh-CN/plugins/mods/events#follow-a-turn) | 轮次结束 | `next(e)`，或 `{ text }` 以在回答下方显示一行 |

<h3 id="session">
  会话
</h3>

会话事件标记会话的开始、结束、压缩，以及与其他会话交换消息：

| 事件 | 触发时机 | hook 可以返回 |
| :- | :- | :- |
| [`session.start`](/docs/zh-CN/plugins/mods/api#add-a-command-or-a-tool) | 每个已加载的 mod 一次，在第一个提示词之前触发，并在该 mod 重新加载后再次触发。`/clear`、`/resume` 或 `/branch` 之后不会触发。 | `next(e)` |
| `session.end` | 会话结束，或运行 `/clear`、`/resume` 或 `/branch` 时。`e.reason` 为 `clear`、`resume`、`logout`、`prompt_input_exit` 或 `other`。`/branch` 报告为 `resume`。 | `next(e)` |
| `session.compact` | 对话即将被压缩 | `{ skip: reason }` |
| [`session.receive`](/docs/zh-CN/plugins/mods/api#send-and-receive-messages-between-sessions), [`session.send`](/docs/zh-CN/plugins/mods/api#send-and-receive-messages-between-sessions) | 一条消息从另一个 Agent 或会话到达，或即将发往另一个 Agent 或会话。请参阅[在会话之间发送和接收消息](/docs/zh-CN/plugins/mods/api#send-and-receive-messages-between-sessions)。 | `receive` 返回 `{ consumed: reason }`，`send` 返回 `{ isDelivered: false, reason }` |
| `session.append` | 对话保留的每一行一次，例如提示词、响应块、工具结果或通知，在存储之前触发 | `next({ ...e, message })` 以重写该行的 `content` |
| `session.attach`, `session.detach` | 另一个应用连接到会话或从会话断开 | `next(e)` |
| `session.measure` | 每个轮次之后，以及套餐限制的已用百分比发生变化时 | `next(e)` |

<h3 id="subagents">
  子代理
</h3>

子代理事件在向 Claude 提供某个子代理类型时，以及子代理或 agent team 队友即将启动时触发：

| 事件 | 触发时机 | hook 可以返回 |
| :- | :- | :- |
| `agent.offer` | 向 Claude 提供某个子代理类型 | `{ isOffered: false }` 以不提供它 |
| `agent.spawn` | 子代理或 [agent team](/docs/zh-CN/agent-teams) 队友即将启动。对于队友，`e.isTeammate` 为 `true`。 | `next({ ...e, model })` 以选择其模型，或 `{ deny: reason }` |

<h3 id="interface">
  界面
</h3>

界面事件在 Claude Code 绘制渲染位置时，以及用户使用 mod 绘制的控件时触发。[在界面中绘制](/docs/zh-CN/plugins/mods/interface)展示了 `ui.render` hook 返回的内容：

| 事件 | 触发时机 |
| :- | :- |
| [`ui.render`](/docs/zh-CN/plugins/mods/interface#pick-where-to-draw) | 某个[渲染位置](#render-sites)即将被绘制 |
| `ui.resolve` | mod 加载时，每个应用、渲染位置和 mod 各一次。其结果是 `$.ui.resolve(e)` 读取的元素表。 |
| [`ui.press`](/docs/zh-CN/plugins/mods/interface#respond-to-presses-and-typing), [`ui.input`](/docs/zh-CN/plugins/mods/interface#respond-to-presses-and-typing), [`ui.select`](/docs/zh-CN/plugins/mods/interface#respond-to-presses-and-typing) | mod 绘制的 `Button`、`Input` 或 `Select` 被使用 |
| `ui.focus`, `ui.scroll` | 获得焦点的控件，或窗格或横栏的滚动位置即将更改 |
| `ui.close` | 窗格即将关闭。`e.id` 是该窗格，`e.origin.kind` 为 `plugin`、`person` 或 `unload`。 |
| [`ui.message`](/docs/zh-CN/plugins/mods/interface#build-a-tree-from-elements) | `Client` 元素向其 mod 发送数据 |
| [`ui.fault`](/docs/zh-CN/plugins/mods/interface#redraw-when-something-changes) | 您的 mod 绘制的 `Client` 元素加载、绘制或运行失败。`e.phase` 为 `load`、`render` 或 `run`，`e.reason` 是错误消息。需要 Claude Code v2.1.289 或更高版本。 |

<h3 id="other-mods">
  其他 mod
</h3>

这些事件让 mod 在其他 mod 加载时对其进行操作，以拒绝某个 mod 或更改它收到的 mods API：

| 事件 | 触发时机 | hook 可以返回 |
| :- | :- | :- |
| [`plugin.register`](/docs/zh-CN/plugins/mods/admin#enforce-a-policy-with-a-mod-of-your-own) | hook 模块即将加载。`e.uses` 列出它的事件、mods API 调用、环境变量和状态，与 `claude plugin validate` 打印的内容一致。每个调用都不带 `$.` 前缀，如 `fs.read`。 | `{ refuse: reason }` |
| `engine.create` | 正在为此 mod 构建 mods API | 更改后的 mods API，用于添加某个命名空间。`user` [层级](#the-hook-function)之外的 mod 还可以隐藏某个命名空间。 |

<h3 id="telemetry">
  遥测
</h3>

遥测事件针对 Claude Code 记录的使用情况记录触发：

| 事件 | 触发时机 | hook 可以返回 |
| :- | :- | :- |
| `telemetry.log`, `telemetry.mark` | 一条遥测记录即将被记录，或标记某项功能的一次使用。在您安装的 mod 中，请为遥测 hook 设置过滤条件 `{ to: 'collector' }`，如 `on('telemetry.log', { to: 'collector' }, hook)`。如果没有该过滤条件，mod 将无法通过 `claude plugin validate`。`*` 不匹配这些事件。 | `next(e)` 或 `{ deny: reason }` |

<h3 id="settings-hook-events">
  设置 hook 事件
</h3>

每个[设置 hook 事件](/docs/zh-CN/hooks#hook-events)都是一个名为 `classic.<Event>` 的事件，如 `classic.Stop` 或 `classic.PostToolUse`。`e` 是该 hook 的 stdin JSON。

<h3 id="mods-api-calls">
  mods API 调用
</h3>

每个 [mods API 方法](#mods-api-methods)也是一个事件，以其命名空间和方法命名，如 `fs.read`、`model.complete` 或 `ui.open`。其上的 hook 会拦截在它之后运行的 mod 发出的调用，并可以返回 `next(e)`、`{ deny: reason }` 或 `{ value }`。

<h2 id="mods-api-methods">
  mods API 方法
</h2>

mods API 是每个 hook 接收的 `$` 参数。它的方法按命名空间分组，例如 `$.ui`。此表按名称列出每个命名空间的方法，因此 `$.ui` 行中的 `open` 就是调用 `$.ui.open(...)`。指南展示了常用方法的用法，而[您的构建版本的类型](/docs/zh-CN/plugins/mods/create#get-the-types-for-your-build)记录了每个方法并附有示例。

| 命名空间 | 方法 |
| :- | :- |
| `$.plugin` | `name`、`root`：此插件的名称和目录 |
| [`$.ui`](/docs/zh-CN/plugins/mods/interface#pick-where-to-draw) | `resolve`、`invalidate`、`open`、`close`、`panes`、`focus`、`scroll`、`toast`、`status`、`log`、`notice`、`ask`、`copy`、`selection`、`blit` |
| [`$.command`](/docs/zh-CN/plugins/mods/api#add-a-command) | `register`、`run`、`list` |
| [`$.tool`](/docs/zh-CN/plugins/mods/api#add-a-tool) | `register`、`call`、`check`、`list` |
| `$.agent` | `register`、`spawn`、`list`。`list()` 返回此会话的子代理和队友，每项都带有 `status`，其值为 `pending`、`running`、`waiting`、`idle`、`completed`、`failed` 或 `killed` 之一，其中 `idle` 和 `waiting` 需要 Claude Code v2.1.289 或更高版本。 |
| [`$.model`](/docs/zh-CN/plugins/mods/api#call-a-model) | `complete`、`fork`、`classify` |
| [`$.prompt`](/docs/zh-CN/plugins/mods/api#start-a-turn-from-a-background-job) | `submit`、`read`、`fill`、`suggest`、`compose`。Claude 读取来自 `submit({ text })` 的文本时，前面会有一句指明您的 mod 为发送者的话。`submit({ text, asUser: true })` 将文本作为用户自己的话发送，不带那句话。 |
| `$.turn` | `abort` |
| [`$.session`](/docs/zh-CN/plugins/mods/api#send-and-receive-messages-between-sessions) | `messages`、`cwd`、`root`、`model`、`turns`、`id`、`repo`、`surfaces`、`usage`、`version`、`compact`、`send`、`append`、`authorize`。`usage()` 返回 `{ startedAt, context, rateLimits, cost }`：`context` 包含 `tokens`、`window` 和 `percent`，`rateLimits` 是由 `{ kind, percentUsed, resetsAt }` 组成的列表。 |
| `$.config` | `list`、`set` |
| [`$.settings`](/docs/zh-CN/plugins/mods/api#reach-files-processes-and-the-network) | `read` |
| [`$.env`](/docs/zh-CN/plugins/mods/api#reach-files-processes-and-the-network) | `get`、`set` |
| [`$.fs`](/docs/zh-CN/plugins/mods/api#reach-files-processes-and-the-network) | `read`、`write`、`list`、`exists`、`stat`、`ancestors`。`write` 不是原子操作：它会原地替换文件内容，因此另一个进程可能读到只写了一部分的文件。请将多个会话都会更改的数据保存在 `$.store` 中。 |
| [`$.store`](/docs/zh-CN/plugins/mods/interface#keep-state) | `get`、`set`、`delete`、`keys`。一个由本机所有会话共享的键值存储。请参阅[从多个会话保存](/docs/zh-CN/plugins/mods/interface#save-from-more-than-one-session)。 |
| [`$.state`](/docs/zh-CN/plugins/mods/interface#keep-a-value-in-\$-state) | 响应式状态：`get`、`set`，以及从 `claude-code` 导入的辅助函数 `atom`、`read`、`update`、`derive` 和 `memberOf` |
| [`$.clock`](/docs/zh-CN/plugins/mods/api#run-work-in-the-background) | `now`、`sleep`、`after`、`every` |
| [`$.http`](/docs/zh-CN/plugins/mods/api#reach-files-processes-and-the-network) | `fetch` |
| [`$.process`](/docs/zh-CN/plugins/mods/api#reach-files-processes-and-the-network) | `run`、`spawn` |
| [`$.mcp`](/docs/zh-CN/plugins/mods/api#reach-files-processes-and-the-network) | `call`、`connect`。`connect(server)` 连接您自己的插件清单中列出的 MCP 服务器。 |
| `$.audio` | `play`、`speak` |
| `$.telemetry` | `log`、`mark`。仅当由 Claude Code 或内置 mod 发出调用时，才会发送记录。 |

<h2 id="render-sites">
  渲染位置
</h2>

渲染位置是 Claude Code 界面中的扩展点。每一行是 `ui.render` hook 中 `e.component` 的一个值，并列出了 `e.props` 的字段以及渲染它的应用。`e.surface` 为 `terminal` 或 `desktop`。[更改 Claude Code 已绘制的内容](/docs/zh-CN/plugins/mods/interface#change-what-claude-code-already-draws)展示了 hook 在某个位置可以做什么，并为每种选择提供了示例。

| 位置 | `e.props` | `e.requestId` | 渲染于 |
| :- | :- | :- | :- |
| [`Pane`](/docs/zh-CN/plugins/mods/interface#pick-where-to-draw) | `title`、`isFocused`、`bodyColumns`、`placement`、`scroll`、`view` | 窗格的 `id` | 终端、Desktop |
| [`AbovePrompt`](/docs/zh-CN/plugins/mods/interface#pick-where-to-draw) | `hasSurvey`、`isWorking`、`maxRows`、`bodyColumns`、`scroll`、`view` | 单一实例 | 终端、Desktop |
| `UserMessage` | `text`、`origin`、`isExpanded`，以及视来源而定的 `task` 或 `from` | 消息 id | 终端、Desktop |
| `AssistantMessage` | 回复的文本 | 消息 id | 终端、Desktop |
| `ToolUse`, `ToolResult`, `ToolGroup` | 工具的名称、输入和结果 | 工具调用 id | 终端、Desktop |
| `CommandOutput` | `command`、`text` | 消息 id | 终端、Desktop |
| [`AskUserQuestion`](/docs/zh-CN/plugins/mods/interface#change-what-claude-code-already-draws) | 问题和选项 | 工具调用 id | 终端、Desktop |
| `ToolProgress` | `kind` | 工具调用 id | 终端 |
| [`Spinner`](/docs/zh-CN/plugins/mods/interface#change-what-claude-code-already-draws) | `word`、`message`、`suffix`、`mode` | Agent id | 终端、Desktop |
| `TurnDuration` | `word`、`durationMs` | 消息 id | 终端 |
| `InfoNotice` | `text`、`command` | 消息 id | 终端 |
| `SessionMode` | `modes` | 单一实例 | 终端、Desktop |
| `PromptHint` | `isDraft`、`isWorking`、`hint` | 单一实例 | 终端、Desktop |

`e.viewport` 包含 `columns`、`rows` 和 `isFullscreen`。在应用测量其窗口之前，它不存在。它的 `rows` 是整个窗口的高度，而不是您的窗格的高度。

要使树适配其所在位置，请在 hook 中读取以下 prop：

* **`Pane` 或横栏的宽度**：按 `e.props.bodyColumns` 绘制
* **会话记录旁的 `Pane` 的高度**：当 `e.props.placement` 为 `'dock'` 时，`e.props.scroll.bodyRows` 是该窗格可供您的树使用的行数
* **输入框上方的 `Pane` 的高度**：当 `e.props.placement` 为 `'inline'` 时，窗格会随您的树增高，直到达到上限，而 `bodyRows` 就是该上限。[`$.ui.open` 的 `rows` 字段](/docs/zh-CN/plugins/mods/interface#open-a-pane-at-the-right-time)可请求不同的上限。

比窗格更高的树会整体滚动。

<h2 id="elements">
  元素
</h2>

元素是 `ui.render` hook 所返回的树的构建块，您可以从 `$.ui.resolve(e)` 获取它们。[用元素构建树](/docs/zh-CN/plugins/mods/interface#build-a-tree-from-elements)展示了常用元素以及终端如何绘制它们，[界面图库](/docs/zh-CN/plugins/mods/gallery)提供了大多数元素的截图。对勾表示该应用可以绘制该元素。

| 元素 | 主要 prop | 终端 | Desktop |
| :- | :- | :-: | :-: |
| [`Box`](/docs/zh-CN/plugins/mods/interface#build-a-tree-from-elements) | `key`、flex 布局、`gap`、`padding`、`margin`、`width`、`height`、[`borderStyle`](#box-border-styles)、`backgroundColor`、`position`、`hover` | ✓ | ✓ |
| [`Text`](/docs/zh-CN/plugins/mods/interface#build-a-tree-from-elements) | `color`、`backgroundColor`、`bold`、`italic`、`underline`、`dimColor`、`inverse`、`wrap` | ✓ | ✓ |
| [`Button`](/docs/zh-CN/plugins/mods/interface#respond-to-presses-and-typing) | `key`、`label`、`onPress`、`hotkey`、`plain`、`dimColor`、`autoFocus`、`action` | ✓ | ✓ |
| [`Link`](/docs/zh-CN/plugins/mods/interface#link-in-the-desktop-app) | `href`、`label`。请参阅[限制](#limits)。 | ✓ | ✓ |
| [`Code`](/docs/zh-CN/plugins/mods/gallery#show-code-and-changes) | `source`、`language`、`path`、`startLine`、`format`、`wrap` | ✓ | ✓ |
| `Markdown` | `text`、`key`、`dimColor`、`onLinkPress`、`pressableLinks` | ✓ | ✓ |
| [`Input`](/docs/zh-CN/plugins/mods/interface#take-typed-input-and-draw-a-row-for-each-item) | `key`、`label`、`placeholder`、`value`、`submitLabel`、`onSubmit`、`onInput`、`autoFocus` | ✓ | ✓ |
| `Select` | `key`、`label`、`options`、`value`、`onSelect`、`autoFocus` | ✓ | ✓ |
| `Svg` | 一个 SVG 文档，最多 131,072 个字符 | | ✓ |
| [`Client`](/docs/zh-CN/plugins/mods/interface#build-a-tree-from-elements) | `module`、`key` | ✓ | ✓ |
| [`Raster`](/docs/zh-CN/plugins/mods/interface#draw-a-grid-of-colored-cells) | `key`、`columns`（最多 512）、`rows`（最多 256）、`cells`。请参阅[绘制彩色单元格网格](/docs/zh-CN/plugins/mods/interface#draw-a-grid-of-colored-cells)。 | ✓ | |
| `Image` | 最多 2 MiB 的 PNG 或 RGBA 字节，或文件路径，`columns` 和 `rows`（最多 255），以及 `alt` 文本。 | ✓ | |

更多 `Button` 规则：`action` 指定 Claude Code 自身的某个[快捷键操作](/docs/zh-CN/keybindings)，当用户为该操作设置的绑定是组合键或带修饰键的按键时，该绑定会按下此按钮。当用户在空的输入框中只输入某个数字并停顿时，横栏中设置了该数字 `hotkey` 的按钮也会触发。当同一次绘制中的两个按钮指定相同的 `hotkey` 时，由后一个按钮获得它。`autoFocus` 在任何控件上都只接受 `true`，因此要关闭它，请省略该 prop。

<h3 id="box-border-styles">
  `Box` 边框样式
</h3>

要在 `Box` 周围绘制边框，请将其 `borderStyle` 设置为以下名称之一，例如 `borderStyle: 'round'`。每一行说明终端针对该名称绘制的内容，并展示边框的上边缘。

| `borderStyle` | 终端绘制的内容 | 上边缘 |
| :- | :- | :- |
| `'single'` | 直角细线 | `┌──┐` |
| `'double'` | 双线 | `╔══╗` |
| `'round'` | 圆角细线 | `╭──╮` |
| `'bold'` | 粗线 | `┏━━┓` |
| `'singleDouble'` | 上下为细线，左右两侧为双线 | `╓──╖` |
| `'doubleSingle'` | 上下为双线，左右两侧为细线 | `╒══╕` |
| `'classic'` | ASCII 字符 `+`、`-` 和 `\|` | `+--+` |
| `'arrow'` | 指向 `Box` 内部的箭头 | `↘↓↓↙` |
| `'dashed'` | 虚线，四角留空 | `╌╌` |
| `'quote'` | 左侧一条竖条 `▎`，其他三边为空白单元格 | 空白 |

如果 `Box` 的 `borderStyle` 指定的是其他名称（例如 `'rounded'`），则绘制时不带边框。

<h2 id="limits">
  限制
</h2>

hook 和 mods API 调用受时间和大小限制。Claude Code 会跳过超出时间限制的 hook。

| 限制 | 值 |
| :- | :- |
| 单个事件中 hook 自身的执行时间，不计入在 `next` 内或在除 `$.clock.sleep` 之外的 mods API 调用中花费的时间 | 10 秒；对于 `prompt.edit` hook 为 50 毫秒 |
| `.catch` 处理程序的执行时间 | 1 秒 |
| 所有 `session.end` hook 合计 | 与 [SessionEnd hook 预算](/docs/zh-CN/hooks#sessionend-input)相同，除非您更改，否则为 1.5 秒，从您设置中的 `SessionEnd` hook 完成时开始计算 |
| `$.process.run` 超时时间 | 默认 30 秒，最长 10 分钟 |
| `$.model.complete` `maxTokens` | 默认 1024，最多 64,000 或模型的输出上限 |
| `$.fs.read` 和 `$.fs.write` | 单个文件 4 MiB |
| hook 的 `drop` 原因或 `config.set` 的 `deny` 原因 | 4,096 个字符。更长的原因会被截去末尾部分，drop 或 deny 仍然生效。截断需要 Claude Code v2.1.292 或更高版本；在更早的版本中，该 hook 会改为[失败](/docs/zh-CN/plugins/mods/events#handle-a-hook-that-fails)。 |
| 单个树中的文本 | 仅绘制前 100,000 个字符 |
| `Code` 的 `language` 或 `path`、`Select` 选项的 `value`，或 `Client` 的 `module` | 10,000 个字符。如果其中任何一项超出此长度，Claude Code 会[在该位置绘制其自身的版本](/docs/zh-CN/plugins/mods/interface#build-a-tree-from-elements)。 |
| `Link` 的 `href` | 2,048 个字符。更长的 `href` 会导致整个树无法绘制。 |
| `$.store` | JSON 总计 4 MiB |
| `$.session.messages()` | 最新的 4,096 个条目 |
| `$.ui.invalidate('ui.render')` 重绘 | 限制为每秒 10 次；在终端中，对于可见窗格、展开区域以及输入框下方的提示行，限制为每秒 30 次。更早到达的调用会被合并。 |
| `$.ui.toast` | 显示 4 秒，除非您传入 `{ timeoutMs }` |
| 非用户主动打开的窗格 | 从终端第 144 列起放置；用户打开过一次后，从第 110 列起放置 |
| 命令、工具、子代理类型和窗格名称 | 字母、数字、`_` 和 `-`，最多 64 个字符 |
| 单个 `claude plugin test` 测试 | 5 秒，除非该测试设置了 `timeoutMs` |

<h2 id="settings-and-environment-variables">
  设置和环境变量
</h2>

以下是影响 mod 的设置和环境变量。“位置”列说明每一项从哪个设置文件或环境中读取：

| 名称 | 位置 | 作用 |
| :- | :- | :- |
| `CLAUDE_CODE_PLUGIN_DIRS` | 环境变量，或 `~/.claude/settings.json` 中的 `env` | 要像 `--plugin-dir` 那样加载的插件目录，用于无法传递标志的应用。以 `:` 分隔的绝对路径，在 Windows 上以 `;` 分隔。 |
| `CLAUDE_CODE_PLUGIN_DIR_WATCH` | 环境变量 | `1` 使长时间运行的非交互式会话在保存时重新加载 `--plugin-dir` mod |
| `prependPlugins`, `appendPlugins` | 托管设置。仅在没有托管设置的机器上、且用户未使用 Team 或 Enterprise 套餐登录时，才可在用户设置中使用。 | 插件 id 列表，例如 `acme-guard@acme-tools`。`prependPlugins` 中的 mod 在用户安装的每个 mod 之前运行，`appendPlugins` 中的 mod 在之后运行，均按列出的顺序。请参阅 [mod 运行顺序](/docs/zh-CN/plugins/mods/events#the-order-mods-run-in)。 |
| `allowManagedModsOnly` | 托管设置，作为[内置守卫的选项](/docs/zh-CN/plugins/mods/admin#set-options-on-the-built-in-guard) | 只有[算作您组织的](/docs/zh-CN/plugins/mods/admin#install-your-organizations-mods) mod 以及 Claude Code 内置的 mod 会运行其 hook。用户的设置 hook 会继续运行。 |
| `allowModsToOverrideDenyRules` | 托管设置，作为[内置守卫的选项](/docs/zh-CN/plugins/mods/admin#set-options-on-the-built-in-guard) | 允许用户安装的 mod 批准被 `deny` 规则拒绝的工具调用 |
| `allowManagedHooksOnly` | 托管设置 | 阻止不属于您组织的 hook 和已安装的 mod。请参阅[哪些会继续运行](/docs/zh-CN/settings-reference#what-runs-under-allowmanagedhooksonly)。 |
| `disableAllHooks` | 任何设置文件 | 在托管设置中，来自已安装插件的任何 mod 或 hook 都不会运行。在您自己的设置中，您组织管理的内容会继续运行。请参阅 [`disableAllHooks`](/docs/zh-CN/settings-reference#disableallhooks)。 |
| `disableSideloadFlags` | 托管设置 | 在启动时拒绝 `--plugin-dir` 和 `--plugin-url` |
| `pluginConfigs` | 用户设置或托管设置 | 保存 mod 的 `userConfig` 值，以插件 id 为键，例如 `acme-guard@acme-tools`；对于使用 `--plugin-dir` 加载的 mod，则以其名称加 `@inline` 为键，例如 `first-mod@inline` |

`sec-default@builtin` 是 Claude Code 内置的守卫，在 `/plugin` 和调试日志中显示为 `cc-plugin-sec-default`。在有托管设置的机器上，或对于使用 Team 或 Enterprise 套餐登录的用户，它会在用户安装的每个 mod 之前加载。如果设置了托管的 `prependPlugins`，则只有当该列表指定了该守卫时它才会加载，并位于列出的位置。其源代码位于 [Claude Code 仓库的 `mods/sec-default` 目录](https://github.com/anthropics/claude-code/tree/main/mods/sec-default)中。

<h2 id="commands">
  命令
</h2>

这些命令和标志用于加载、检查和测试 mod。`claude` 命令在您的 shell 中运行，`/` 命令在 Claude Code 输入框中运行。表中的 `<directory>` 代表您输入的路径，如 `claude plugin validate ./first-mod`。方括号表示可选参数。

| 命令 | 作用 |
| :- | :- |
| [`/plugin`](/docs/zh-CN/plugins/mods/overview#see-which-mods-a-session-loaded) | 当有非内置的 mod 加载时，在其标签页下方显示一行，例如 `1 mod active · first-mod` |
| [`claude plugin validate <directory>`](/docs/zh-CN/plugins/mods/create#check-what-claude-code-reads-from-your-mod) | 读取插件的清单和 hook 模块，并报告错误、它处理的事件以及它发出的 mods API 调用。`--strict` 将警告视为错误，`--json` 打印机器可读的报告。 |
| [`claude plugin test [directory]`](/docs/zh-CN/plugins/mods/test#write-a-test) | 运行该目录（如果未指定目录，则为当前目录）下名称以 `.test.ts` 或 `.test.tsx` 结尾的每个文件。有测试失败时以状态 1 退出。 |
| [`claude --plugin-dir <directory>`](/docs/zh-CN/plugins/mods/create#write-a-mod-yourself) | 为一个会话加载插件目录，并在您保存时重新加载其 hook 模块。重复该标志可加载多个目录。 |
| `/reload-plugins` | 在您运行时重新加载插件 |
