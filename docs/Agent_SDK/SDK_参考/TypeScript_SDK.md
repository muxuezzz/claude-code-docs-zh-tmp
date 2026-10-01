> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Agent SDK 参考 - TypeScript

> TypeScript Agent SDK 的完整 API 参考，包括所有函数、类型和接口。

<script src="/docs/components/typescript-sdk-type-links.js" defer />

<h2 id="installation">
  安装
</h2>

```bash theme={null}
npm install @anthropic-ai/claude-agent-sdk
```

<Note>
  SDK 为您的平台捆绑了一个本地 Claude Code 二进制文件，作为可选依赖项，例如 `@anthropic-ai/claude-agent-sdk-darwin-arm64`。大多数安装无需单独安装 Claude Code。SDK 版本跟踪捆绑的 Claude Code 版本。SDK v0.3.191 捆绑 Claude Code v2.1.191，因此本页面上需要特定 Claude Code 版本的功能需要具有相同补丁号或更高版本的 SDK 版本。如果您的包管理器跳过可选依赖项，SDK 会抛出 `Native CLI binary for <platform>-<arch> not found`；改为将 [`pathToClaudeCodeExecutable`](#options) 设置为单独安装的 `claude` 二进制文件。

  如果您的包管理器不应用 npm 的 `libc` 字段（如 Yarn 1.x 不应用），您会在 Linux 上同时获得 glibc 和 musl 平台包，大约使安装大小翻倍。在 Agent SDK v0.2.141 或更高版本上，SDK 仍然会启动正确的变体。要在容器镜像中回收空间，请删除与您的应用运行的 libc 不匹配的平台包；对于 x64 上的 glibc 运行时，即 `rm -rf node_modules/@anthropic-ai/claude-agent-sdk-linux-x64-musl`。在开发机器上删除是临时的，因为 Yarn 会在下一次依赖项更改时重新安装该包。
</Note>

<h3 id="compile-to-a-single-executable">
  编译为单个可执行文件
</h3>

当您使用 `bun build --compile` 将应用程序编译为单文件可执行文件时，SDK 无法在运行时解析捆绑的 CLI 二进制文件。`require.resolve` 在编译后的可执行文件的 `$bunfs` 虚拟文件系统内不起作用，因此 SDK 会抛出 `Native CLI binary for <platform>-<arch> not found`。

要解决此问题，请将平台二进制文件作为文件资产嵌入，在启动时使用 `extractFromBunfs()` 将其提取到真实路径，然后将该路径传递给 [`pathToClaudeCodeExecutable`](#options)。

`extractFromBunfs()` 辅助函数需要 `@anthropic-ai/claude-agent-sdk` v0.3.144 或更高版本。下面的示例为 Apple Silicon 上的 macOS 构建：

```typescript theme={null}
import binPath from "@anthropic-ai/claude-agent-sdk-darwin-arm64/claude" with { type: "file" };
import { extractFromBunfs } from "@anthropic-ai/claude-agent-sdk/extract";
import { query } from "@anthropic-ai/claude-agent-sdk";

const cliPath = extractFromBunfs(binPath);

for await (const message of query({
  prompt: "Hello",
  options: { pathToClaudeCodeExecutable: cliPath },
})) {
  console.log(message);
}
```

`extractFromBunfs()` 将嵌入的二进制文件从编译后的可执行文件的虚拟文件系统复制到每个用户的临时目录，并返回真实路径。在编译后的可执行文件之外，它返回输入路径不变，因此相同的代码在开发中无需修改即可运行。

每个编译后的可执行文件都嵌入了单个平台的二进制文件。将导入中的平台包与您的 `--target` 匹配：

* 要进行交叉编译，请安装不匹配的平台包，例如 `npm install @anthropic-ai/claude-agent-sdk-linux-x64 --force`。
* 在 Windows 上，二进制文件子路径是 `claude.exe`，例如 `@anthropic-ai/claude-agent-sdk-win32-x64/claude.exe`。

<h3 id="import-the-/core-entry-when-you-bundle-the-agent-sdk">
  在捆绑 Agent SDK 时导入 `/core` 入口
</h3>

如果您的应用程序将 Agent SDK 与其自己的依赖项一起捆绑，请从 `@anthropic-ai/claude-agent-sdk/core` 而不是包根目录导入。`/core` 入口需要 TypeScript Agent SDK v0.3.282 或更高版本，其类型需要 TypeScript 5.0 或更高版本。

`/core` 入口导出与根入口相同的 `query()`、`startup()`、`tool()`、`createSdkMcpServer()` 和 `resolveSettings()`，以及重命名、标记和删除会话的函数、`AbortError`、运行时常量和每种类型。它不添加自己的名称。为了保持应用程序加载的代码较小，`/core` 省略了一些根导出，包括 `prewarm()`、`InMemorySessionStore` 类以及列出、读取、分叉、导入和总结会话的辅助函数。如果您需要其中之一，请改用根入口。

根入口内联了自己的 `zod` 和 `@modelcontextprotocol/sdk` 副本。`/core` 入口从您的 `node_modules` 按照 Agent SDK 的 `peerDependencies` 声明的范围导入它们，因此已经包含它们的捆绑包不会携带第二个副本。在给定的进程中从根或 `/core` 导入，而不是两者：它们是单独的捆绑包，加载两者会给您两个 Agent SDK 类和状态的副本。

<h2 id="functions">
  函数
</h2>

<h3 id="query">
  `query()`
</h3>

与 Claude Code 交互的主要函数。创建一个异步生成器，在消息到达时流式传输消息。

```typescript theme={null}
function query({
  prompt,
  options
}: {
  prompt: string | AsyncIterable<SDKUserMessage>;
  options?: Options;
}): Query;
```

<h4 id="parameters">
  参数
</h4>

| 参数 | 类型 | 描述 |
| :- | :- | :- |
| `prompt` | `string \| AsyncIterable<`[`SDKUserMessage`](#sdkusermessage)`>` | 输入提示，可以是字符串或异步可迭代对象（用于流式模式） |
| `options` | [`Options`](#options) | 可选配置对象（请参阅下面的 Options 类型） |

<h4 id="returns">
  返回值
</h4>

返回一个 [`Query`](#query-object) 对象，该对象扩展 `AsyncGenerator<`[`SDKMessage`](#sdkmessage)`, void>`，并具有其他方法。

<h3 id="startup">
  `startup()`
</h3>

通过生成 CLI 子进程并在提示可用之前完成初始化握手来预热 CLI 子进程。返回的 [`WarmQuery`](#warmquery) 句柄稍后接受提示并将其写入已准备好的进程，因此第一个 `query()` 调用解析时无需支付子进程生成和初始化成本。如果您还不知道会话的工作目录，请改用 [`prewarm()`](#prewarm)。

```typescript theme={null}
function startup(params?: {
  options?: Options;
  initializeTimeoutMs?: number;
}): Promise<WarmQuery>;
```

<h4 id="parameters-2">
  参数
</h4>

| 参数 | 类型 | 描述 |
| :- | :- | :- |
| `options` | [`Options`](#options) | 可选配置对象。与 `query()` 的 `options` 参数相同 |
| `initializeTimeoutMs` | `number` | 等待子进程初始化的最长时间（毫秒）。默认为 `60000`。如果初始化未在规定时间内完成，promise 将以超时错误拒绝 |

<h4 id="returns-2">
  返回值
</h4>

返回一个 `Promise<`[`WarmQuery`](#warmquery)`>`，在子进程生成并完成其初始化握手后解析。

<h4 id="example">
  示例
</h4>

早期调用 `startup()`，例如在应用程序启动时，然后在提示准备好后在返回的句柄上调用 `.query()`。这会将子进程生成和初始化移出关键路径。

```typescript theme={null}
import { startup } from "@anthropic-ai/claude-agent-sdk";

// 提前支付启动成本
const warm = await startup({ options: { maxTurns: 3 } });

// 稍后，当提示准备好时，这是立即的
for await (const message of warm.query("What files are here?")) {
  console.log(message);
}
```

<h3 id="prewarm">
  `prewarm()`
</h3>

*Alpha。* 在您知道它将服务哪个会话之前启动 Claude Code 进程作为备用，以便您稍后可以使用 [`claim()`](#spareprocess) 将其绑定到会话。在应用程序启动之前用户选择文件夹的应用程序中使用它。需要 TypeScript Agent SDK v0.3.282 或更高版本。

`prewarm()` 完成与 [`startup()`](#startup) 相同的初始化握手，当您设置 `options.cwd` 时进程在其中等待，否则在 Claude Code 配置目录下的私有临时目录中等待。会话的工作目录、其 `SessionStart` hooks、其 stdio MCP 服务器以及其 CLAUDE.md 和 git 上下文等待声明。备用进程在等待时占用大约 230 到 260 MB 的内存。如果您的 [`spawnClaudeCodeProcess`](#options) 在另一台机器或容器中运行 Claude Code，请将 `options.cwd` 设置为存在于那里的目录，以便备用进程在其中等待。

```typescript theme={null}
function prewarm(params?: {
  options?: Options;
  initializeTimeoutMs?: number;
}): Promise<SpareProcess>;
```

`options` 和 `initializeTimeoutMs` 的含义与 `startup()` 相同，除了 `options.cwd` 仅设置备用进程等待的目录。promise 在进程完成其初始化握手后使用 [`SpareProcess`](#spareprocess) 解析。如果 `options` 设置 `resume`、`continue` 或 `forkSession`，`prewarm()` 会抛出错误，因为备用进程还没有会话。声明无法设置的所有内容，例如 `mcpServers`、`hooks`、`canUseTool`、`settingSources`、`systemPrompt` 和 `plugins`，在备用进程的生命周期内是固定的，因此为每个不同的选项集保留一个备用进程，并在它们更改时再次预热。

<h4 id="example-2">
  示例
</h4>

在应用程序启动时预热，然后在用户启动会话时声明备用进程：

```typescript theme={null}
import { prewarm } from "@anthropic-ai/claude-agent-sdk";

// 在应用程序启动时，在会话的文件夹已知之前
const spare = await prewarm({ options: { maxTurns: 3 } });

// 稍后，当用户在文件夹中启动会话时
const claimedQuery = spare.claim({
  prompt: "What files are here?",
  options: { cwd: "/path/to/project" },
});

spare.claimed.catch((error: Error) => {
  // 除非消息以 "option_not_applied" 开头，否则提示未运行：
  // 改为使用 query() 启动此会话
  console.error("Claim failed:", error.message);
});

for await (const message of claimedQuery) {
  console.log(message);
}
```

<h3 id="tool">
  `tool()`
</h3>

为与 SDK MCP 服务器一起使用创建类型安全的 MCP 工具定义。

```typescript theme={null}
function tool<Schema extends AnyZodRawShape>(
  name: string,
  description: string,
  inputSchema: Schema,
  handler: (args: InferShape<Schema>, extra: unknown) => Promise<CallToolResult>,
  extras?: { annotations?: ToolAnnotations; searchHint?: string; alwaysLoad?: boolean }
): SdkMcpToolDefinition<Schema>;
```

<h4 id="parameters-3">
  参数
</h4>

| 参数 | 类型 | 描述 |
| :- | :- | :- |
| `name` | `string` | 工具的名称 |
| `description` | `string` | 工具功能的描述 |
| `inputSchema` | `Schema extends AnyZodRawShape` | 定义工具输入参数的 Zod 架构（支持 Zod 3 和 Zod 4） |
| `handler` | `(args, extra) => Promise<`[`CallToolResult`](#calltoolresult)`>` | 执行工具逻辑的异步函数 |
| `extras` | `{ annotations?: `[`ToolAnnotations`](#toolannotations)`; searchHint?: string; alwaysLoad?: boolean }` | 可选的 extras。`annotations` 为客户端提供 MCP 行为提示。`searchHint` 是当[工具搜索](/docs/zh-CN/agent-sdk/tool-search)处于活动状态时在延迟工具列表中显示的单行功能短语。`alwaysLoad: true` 将此工具的完整架构保留在初始提示中，而不是延迟它 |

<h4 id="toolannotations">
  `ToolAnnotations`
</h4>

从 `@modelcontextprotocol/sdk/types.js` 重新导出。所有字段都是可选提示；客户端不应依赖它们做出安全决策。

| 字段 | 类型 | 默认值 | 描述 |
| :- | :- | :- | :- |
| `title` | `string` | `undefined` | 工具的人类可读标题 |
| `readOnlyHint` | `boolean` | `false` | 如果为 `true`，工具不会修改其环境 |
| `destructiveHint` | `boolean` | `true` | 如果为 `true`，工具可能执行破坏性更新（仅在 `readOnlyHint` 为 `false` 时有意义） |
| `idempotentHint` | `boolean` | `false` | 如果为 `true`，使用相同参数的重复调用没有额外效果（仅在 `readOnlyHint` 为 `false` 时有意义） |
| `openWorldHint` | `boolean` | `true` | 如果为 `true`，工具与外部实体交互（例如，网络搜索）。如果为 `false`，工具的域是封闭的（例如，内存工具） |

```typescript theme={null}
import { tool } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

const searchTool = tool(
  "search",
  "Search the web",
  { query: z.string() },
  async ({ query }) => {
    return { content: [{ type: "text", text: `Results for: ${query}` }] };
  },
  { annotations: { readOnlyHint: true, openWorldHint: true } }
);
```

<h3 id="createsdkmcpserver">
  `createSdkMcpServer()`
</h3>

创建在与应用程序相同的进程中运行的 MCP 服务器实例。

```typescript theme={null}
function createSdkMcpServer(options: {
  name: string;
  version?: string;
  instructions?: string;
  tools?: Array<SdkMcpToolDefinition<any>>;
  alwaysLoad?: boolean;
  timeout?: number;
}): McpSdkServerConfigWithInstance;
```

<h4 id="parameters-4">
  参数
</h4>

| 参数 | 类型 | 描述 |
| :- | :- | :- |
| `options.name` | `string` | MCP 服务器的名称 |
| `options.version` | `string` | 可选版本字符串 |
| `options.instructions` | `string` | 可选服务器说明，从 `initialize` 返回并作为 MCP 说明块呈现给模型 |
| `options.tools` | `Array<SdkMcpToolDefinition>` | 使用 [`tool()`](#tool) 创建的工具定义数组 |
| `options.alwaysLoad` | `boolean` | 当为 `true` 时，来自此服务器的每个工具都保留在初始提示中，永远不会在[工具搜索](/docs/zh-CN/agent-sdk/tool-search)后延迟。与 [`tool()`](#tool) 中的每个工具 `alwaysLoad` 结合 |
| `options.timeout` | `number` | 此服务器的工具调用超时（毫秒）。Claude Code 将其应用于此服务器以代替 [`MCP_TOOL_TIMEOUT`](/docs/zh-CN/env-vars)。传递至少 1000 的整数。Claude Code 忽略其他值。需要 TypeScript Agent SDK v0.3.248 或更高版本 |

<h3 id="listsessions">
  `listSessions()`
</h3>

发现并列出具有轻量级元数据的过去会话。按项目目录筛选或列出所有项目中的会话。

```typescript theme={null}
function listSessions(options?: ListSessionsOptions): Promise<SDKSessionInfo[]>;
```

<h4 id="parameters-5">
  参数
</h4>

| 参数 | 类型 | 默认值 | 描述 |
| :- | :- | :- | :- |
| `options.dir` | `string` | `undefined` | 列出会话的目录。省略时，返回所有项目中的会话 |
| `options.limit` | `number` | `undefined` | 要返回的最大会话数 |
| `options.includeWorktrees` | `boolean` | `true` | 当 `dir` 在 git 存储库内时，包括来自所有 worktree 路径的会话 |

<h4 id="return-type-sdksessioninfo">
  返回类型：`SDKSessionInfo`
</h4>

| 属性 | 类型 | 描述 |
| :- | :- | :- |
| `sessionId` | `string` | 唯一会话标识符 (UUID) |
| `summary` | `string` | 显示标题：自定义标题、最近的提示、自动生成的摘要或第一个提示 |
| `lastModified` | `number` | 上次修改时间（自纪元以来的毫秒数） |
| `fileSize` | `number \| undefined` | 会话文件大小（字节）。仅对本地 JSONL 存储进行填充 |
| `customTitle` | `string \| undefined` | 会话的自定义标题（当设置了一个时），例如通过 `--name`、`/rename`、hook 的 `sessionTitle` 输出或 [`renameSession()`](#renamesession)。否则为 AI 生成的会话标题（如果会话有的话） |
| `firstPrompt` | `string \| undefined` | 会话中的第一个有意义的用户提示 |
| `gitBranch` | `string \| undefined` | 会话结束时的 git 分支 |
| `cwd` | `string \| undefined` | 会话的工作目录 |
| `tag` | `string \| undefined` | 用户设置的会话标签（请参阅 [`tagSession()`](#tagsession)） |
| `createdAt` | `number \| undefined` | 创建时间（自纪元以来的毫秒数），来自第一个条目的时间戳 |

<h4 id="example-3">
  示例
</h4>

打印项目的 10 个最近会话。结果按 `lastModified` 降序排序，因此第一项是最新的。省略 `dir` 以搜索所有项目。

```typescript theme={null}
import { listSessions } from "@anthropic-ai/claude-agent-sdk";

const sessions = await listSessions({ dir: "/path/to/project", limit: 10 });

for (const session of sessions) {
  console.log(`${session.summary} (${session.sessionId})`);
}
```

<h3 id="getsessionmessages">
  `getSessionMessages()`
</h3>

从过去的会话记录中读取用户和助手消息。

```typescript theme={null}
function getSessionMessages(
  sessionId: string,
  options?: GetSessionMessagesOptions
): Promise<SessionMessage[]>;
```

<h4 id="parameters-6">
  参数
</h4>

| 参数 | 类型 | 默认值 | 描述 |
| :- | :- | :- | :- |
| `sessionId` | `string` | 必需 | 要读取的会话 UUID（请参阅 `listSessions()`） |
| `options.dir` | `string` | `undefined` | 查找会话的项目目录。省略时，搜索所有项目 |
| `options.limit` | `number` | `undefined` | 要返回的最大消息数 |
| `options.offset` | `number` | `undefined` | 从开始跳过的消息数 |

<h4 id="return-type-sessionmessage">
  返回类型：`SessionMessage`
</h4>

| 属性 | 类型 | 描述 |
| :- | :- | :- |
| `type` | `"user" \| "assistant"` | 消息角色 |
| `uuid` | `string` | 唯一消息标识符 |
| `session_id` | `string` | 此消息所属的会话 |
| `message` | `unknown` | 来自记录的原始消息有效负载 |
| `parent_tool_use_id` | `string \| null` | 对于子代理消息，生成 `Agent` 或 `Skill` 工具调用的 `tool_use_id`，该调用启动了子代理。对于主会话消息和较旧的会话为 `null` |
| `parent_agent_id` | `string \| null` | 对于来自[嵌套子代理](/docs/zh-CN/sub-agents#let-subagents-spawn-their-own-subagents)的消息，生成该消息的子代理的 `agentId`。对于主会话消息、来自顶级子代理的消息和较旧的会话为 `null`。需要 Claude Code v2.1.202 或更高版本 |

<h4 id="example-4">
  示例
</h4>

```typescript theme={null}
import { listSessions, getSessionMessages } from "@anthropic-ai/claude-agent-sdk";

const [latest] = await listSessions({ dir: "/path/to/project", limit: 1 });

if (latest) {
  const messages = await getSessionMessages(latest.sessionId, {
    dir: "/path/to/project",
    limit: 20
  });

  for (const msg of messages) {
    console.log(`[${msg.type}] ${msg.uuid}`);
  }
}
```

<h3 id="getsessioninfo">
  `getSessionInfo()`
</h3>

按 ID 读取单个会话的元数据，无需扫描完整项目目录。

```typescript theme={null}
function getSessionInfo(
  sessionId: string,
  options?: GetSessionInfoOptions
): Promise<SDKSessionInfo | undefined>;
```

<h4 id="parameters-7">
  参数
</h4>

| 参数 | 类型 | 默认值 | 描述 |
| :- | :- | :- | :- |
| `sessionId` | `string` | 必需 | 要查找的会话 UUID |
| `options.dir` | `string` | `undefined` | 项目目录路径。省略时，搜索所有项目目录 |

返回 [`SDKSessionInfo`](#return-type-sdksessioninfo)，如果找不到会话，则返回 `undefined`。

<h3 id="renamesession">
  `renameSession()`
</h3>

通过附加自定义标题条目来重命名会话。重复调用是安全的；最新的标题获胜。

```typescript theme={null}
function renameSession(
  sessionId: string,
  title: string,
  options?: SessionMutationOptions
): Promise<void>;
```

<h4 id="parameters-8">
  参数
</h4>

| 参数 | 类型 | 默认值 | 描述 |
| :- | :- | :- | :- |
| `sessionId` | `string` | 必需 | 要重命名的会话 UUID |
| `title` | `string` | 必需 | 新标题。修剪空格后必须非空 |
| `options.dir` | `string` | `undefined` | 项目目录路径。省略时，搜索所有项目目录 |

<h3 id="tagsession">
  `tagSession()`
</h3>

标记会话。传递 `null` 以清除标签。重复调用是安全的；最新的标签获胜。

```typescript theme={null}
function tagSession(
  sessionId: string,
  tag: string | null,
  options?: SessionMutationOptions
): Promise<void>;
```

<h4 id="parameters-9">
  参数
</h4>

| 参数 | 类型 | 默认值 | 描述 |
| :- | :- | :- | :- |
| `sessionId` | `string` | 必需 | 要标记的会话 UUID |
| `tag` | `string \| null` | 必需 | 标签字符串，或 `null` 以清除 |
| `options.dir` | `string` | `undefined` | 项目目录路径。省略时，搜索所有项目目录 |

<h3 id="resolvesettings">
  `resolveSettings()`
</h3>

使用与 CLI 相同的合并引擎为给定目录解析有效的 Claude Code 设置，无需生成 Claude CLI。在调用 `query()` 之前使用它来检查 `query()` 调用将看到的配置。

<Note>
  此函数处于 alpha 阶段，其 API 在稳定之前可能会更改。
</Note>

快照与实时 `query()` 会话应用的内容不同：

* **`policyHelper`**：`resolveSettings()` 读取 MDM 源，包括 macOS plist 和 Windows HKLM/HKCU，但不执行管理员配置的 `policyHelper` 子进程。
* **服务器管理的设置**：`resolveSettings()` 不获取[服务器管理的设置](/docs/zh-CN/server-managed-settings#fetch-and-caching-behavior)。将它们作为 `options.serverManagedSettings` 传递以包含它们。
* **`defaultMode`**：快照从每个层级按原样返回 `permissions.defaultMode`，因此它可以包括项目和本地设置中的 `'auto'` 和 `'bypassPermissions'` 值，[实时会话忽略](/docs/zh-CN/permission-modes#which-mode-a-session-starts-in)这些值。

```typescript theme={null}
function resolveSettings(
  options?: ResolveSettingsOptions
): Promise<ResolvedSettings>;
```

<h4 id="parameters-10">
  参数
</h4>

`resolveSettings()` 接受单个选项对象。所有字段都是可选的。

| 参数 | 类型 | 默认值 | 描述 |
| :- | :- | :- | :- |
| `options.cwd` | `string` | `process.cwd()` | 用于解析项目和本地设置的相对目录 |
| `options.settingSources` | [`SettingSource`](#settingsource)`[]` | 所有源 | 要加载的文件系统源。传递 `[]` 以跳过用户、项目和本地设置。[端点管理的策略](/docs/zh-CN/managed-settings#delivery-mechanisms)在所有情况下都会加载。`resolveSettings()` 仅当您传递 `options.serverManagedSettings` 时才包括服务器管理的设置 |
| `options.managedSettings` | `Settings` | `undefined` | 由嵌入主机提供的策略层设置。遵循与 [`managedSettings` in `Options`](#options) 相同的规则，除了 `resolveSettings()` 不执行配置的 [`policyHelper`](/docs/zh-CN/settings-reference#policyhelper)，因此快照可以包括实时会话删除的设置 |
| `options.serverManagedSettings` | `Settings` | `undefined` | 来自 `/api/claude_code/settings` 的服务器管理设置有效负载。非限制性密钥不经过滤地通过 |

<h4 id="return-type-resolvedsettings">
  返回类型：`ResolvedSettings`
</h4>

`resolveSettings()` 返回一个对象，描述合并的设置和为每个密钥提供的源。

| 属性 | 类型 | 描述 |
| :- | :- | :- |
| `effective` | `Settings` | 在按优先级顺序应用所有启用的源后合并的设置 |
| `provenance` | `Partial<Record<keyof Settings, ProvenanceEntry>>` | 对于 `effective` 中的每个顶级密钥，哪个源提供了该值 |
| `sources` | `Array<{ source, settings, path?, policyOrigin? }>` | 每个源的原始设置，按从最低到最高优先级排序 |

<h4 id="example-5">
  示例
</h4>

下面的示例为项目目录解析设置并打印控制清理周期的源。在没有设置文件设置 `cleanupPeriodDays` 的机器上，两条打印的行都显示 `undefined` 作为值，这是预期的输出而不是错误。

```typescript theme={null}
import { resolveSettings } from "@anthropic-ai/claude-agent-sdk";

const { effective, provenance } = await resolveSettings({
  cwd: "/path/to/project",
  settingSources: ["user", "project", "local"],
});

console.log(`Cleanup period: ${effective.cleanupPeriodDays} days`);
console.log(`Set by: ${provenance.cleanupPeriodDays?.source}`);
```

<h2 id="types">
  类型
</h2>

<h3 id="options">
  `Options`
</h3>

`query()` 函数的配置对象。

| 属性 | 类型 | 默认值 | 描述 |
| :- | :- | :- | :- |
| `abortController` | `AbortController` | `new AbortController()` | 用于取消操作的控制器 |
| `additionalDirectories` | `string[]` | `[]` | Claude 可以访问的其他目录。SDK 将每个条目作为 `--add-dir` 传递给 Claude Code，因此使用 `project` 设置源时，Claude Code 也会[加载目录的 skills、commands 和 subagents](/docs/zh-CN/permissions#additional-directories-grant-file-access-not-configuration) |
| `agent` | `string` | `undefined` | 主线程的代理名称。代理必须在 `agents` 选项或设置中定义 |
| `agents` | `Record<string, [`AgentDefinition`](#agentdefinition)>` | `undefined` | 以编程方式定义 subagents |
| `agentProgressSummaries` | `boolean` | `false` | 当为 `true` 时，为 subagents 生成单行进度摘要，并通过 `summary` 字段在 [`task_progress`](#sdktaskprogressmessage) 事件上转发它们。适用于前台和后台 subagents |
| `allowDangerouslySkipPermissions` | `boolean` | `false` | 启用绕过权限。使用 `permissionMode: 'bypassPermissions'` 时需要，在启动时或稍后通过 `setPermissionMode()` 进行。请参阅 [plan mode](/docs/zh-CN/agent-sdk/permissions#plan-mode-plan) 了解它如何与 `permissionMode: 'plan'` 交互 |
| `allowedTools` | `string[]` | `[]` | 无需提示即可自动批准的工具。这不会将 Claude 限制为仅这些工具。如果您在此处命名[任务跟踪工具](/docs/zh-CN/agent-sdk/todo-tracking#model-availability)之一，Claude Code 也会选择加入会话。其他未列出的工具会通过 `permissionMode` 和 `canUseTool` 进行处理。使用 `disallowedTools` 阻止工具。请参阅[权限](/docs/zh-CN/agent-sdk/permissions#allow-and-deny-rules) |
| `betas` | [`SdkBeta`](#sdkbeta)`[]` | `[]` | 启用测试功能 |
| `canUseTool` | [`CanUseTool`](#canusetool) | `undefined` | 自定义权限函数，仅在[权限流](/docs/zh-CN/agent-sdk/permissions#how-permissions-are-evaluated)落到提示时调用。不会为 `allowedTools`、allow 规则或 `permissionMode` 自动批准的调用调用。allow 规则不会预先批准[任何模式都不自动批准的操作](/docs/zh-CN/permission-modes#actions-no-mode-auto-approves)；请参阅 [`CanUseTool`](#canusetool) 了解详情 |
| `continue` | `boolean` | `false` | 继续最近的对话 |
| `cwd` | `string` | `process.cwd()` | 当前工作目录 |
| `debug` | `boolean` | `false` | 为 Claude Code 进程启用调试模式 |
| `debugFile` | `string` | `undefined` | 将调试日志写入特定文件路径。隐式启用调试模式 |
| `disallowedTools` | `string[]` | `[]` | 要拒绝的工具。裸名称如 `"Bash"` 会从 Claude 的上下文中移除该工具。作用域规则如 `"Bash(rm *)"` 会保留该工具可用，并在每个权限模式（包括 `bypassPermissions`）中拒绝匹配的调用，针对[按照书写方式](/docs/zh-CN/permissions#bash-rule-limits)的命令。请参阅[权限](/docs/zh-CN/agent-sdk/permissions#allow-and-deny-rules) |
| `effort` | `'low' \| 'medium' \| 'high' \| 'xhigh' \| 'max'` | `undefined` | 控制 Claude 在其响应中投入的努力程度。与自适应思考一起工作以指导思考深度。请参阅[调整努力级别](/docs/zh-CN/model-config#adjust-effort-level) |
| `enableFileCheckpointing` | `boolean` | `false` | 启用文件更改跟踪以进行回滚。请参阅[文件 checkpointing](/docs/zh-CN/agent-sdk/file-checkpointing) |
| `env` | `Record<string, string \| undefined>` | `process.env` | 环境变量。设置此选项时，这会替换子进程环境而不是与 `process.env` 合并，因此请传递 `{ ...process.env, YOUR_VAR: 'value' }` 以保留继承的变量如 `PATH`。请参阅[处理缓慢或停滞的 API 响应](#handle-slow-or-stalled-api-responses)了解此模式的示例，以及[环境变量](/docs/zh-CN/env-vars)了解底层 CLI 读取的变量。设置 `CLAUDE_AGENT_SDK_CLIENT_APP` 以在 User-Agent 标头中标识您的应用 |
| `executable` | `'bun' \| 'deno' \| 'node'` | 自动检测 | 要使用的 JavaScript 运行时 |
| `executableArgs` | `string[]` | `[]` | 传递给可执行文件的参数 |
| `extraArgs` | `Record<string, string \| null>` | `{}` | 其他参数 |
| `fallbackModel` | `string` | `undefined` | 主模型失败时使用的模型。接受逗号分隔的列表。有关顺序和上限，请参阅[备用模型链](/docs/zh-CN/model-config#fallback-model-chains)。有关指导，请参阅[选择模型](/docs/zh-CN/agent-sdk/configuration#choose-a-model) |
| `forkSession` | `boolean` | `false` | 使用 `resume` 恢复时，分叉到新会话 ID 而不是继续原始会话 |
| `forwardSubagentText` | `boolean` | `false` | 转发 subagent 文本和思考块作为助手和用户消息，并设置 `parent_tool_use_id`，以便消费者可以呈现嵌套记录。没有此选项，Claude Code 会发出 subagent `tool_use` 和 `tool_result` 块，但不会发出文本或思考。来自每个嵌套深度的 subagents 的消息在 Claude Code v2.1.219 及更高版本上转发；在 v2.1.219 之前，仅出现来自深度 1 subagents 的消息。来自分叉 skill 生成的 subagents 的消息，以及嵌套分叉 skills 的消息，需要 v2.1.275 或更高版本 |
| `hooks` | `Partial<Record<`[`HookEvent`](#hookevent)`, `[`HookCallbackMatcher`](#hookcallbackmatcher)`[]>>` | `{}` | 事件的 Hook 回调 |
| `includeHookEvents` | `boolean` | `false` | 在消息流中包括 hook 生命周期事件，作为 [`SDKHookStartedMessage`](#sdkhookstartedmessage)、[`SDKHookProgressMessage`](#sdkhookprogressmessage) 和 [`SDKHookResponseMessage`](#sdkhookresponsemessage)。`SessionStart` 和 `Setup` hooks 的生命周期事件始终包括在内，不需要此选项。某些 hook 事件，如 `Notification`、`SessionEnd`、`PreCompact` 和 `PostCompact`，即使使用此选项也永远不会产生 `SDKHookStartedMessage`。对于这些事件，Claude Code 仍会在运行超过一秒的命令 hook 产生输出时发出 `SDKHookProgressMessage`，并仅在[在后台运行](/docs/zh-CN/hooks#run-hooks-in-the-background)的 hook 完成时发出 `SDKHookResponseMessage` |
| `includePartialMessages` | `boolean` | `false` | 包括部分消息事件 |
| `loadTimeoutMs` | `number` | `60000` | *Alpha.* 每个 `sessionStore.load()` 和 `sessionStore.listSubkeys()` 调用在恢复物化期间的超时时间（以毫秒为单位）。如果适配器未在此窗口内解决，查询将失败而不是挂起。未设置 `sessionStore` 时忽略 |
| `managedSettings` | `Settings` | `undefined` | 您的主机进程提供给生成的会话的策略层设置。在具有管理员部署的托管设置的机器上，Claude Code 会忽略这些，除非管理员的最高优先级托管源设置 `parentSettingsBehavior: 'merge'`，并且当 [`policyHelper`](/docs/zh-CN/settings-reference#policyhelper) 提供托管设置时永远不会合并它们。合并的值通过仅限制性过滤器；[限制父设置](/docs/zh-CN/claude-apps-gateway#restrict-parent-settings)涵盖过滤器允许的内容和 `allowManaged*Only` 锁。设置 [`CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST`](/docs/zh-CN/env-vars) 的主机有三个键直接从此有效负载读取：其在 Claude Code v2.1.222 或更高版本上的[模型配置](/docs/zh-CN/model-config#restrict-model-selection)、当没有托管源在 v2.1.246 或更高版本上设置它时的 [`modelPricing`](/docs/zh-CN/settings-reference#modelpricing)，以及其在 v2.1.247 或更高版本上的 `ENABLE_TOOL_SEARCH` env 条目 |
| `maxBudgetUsd` | `number` | `undefined` | 当客户端成本估计达到此 USD 值时停止查询。仅计算调用自身的支出；从恢复的会话恢复的总计不计算。有关准确性注意事项和重置行为，请参阅[跟踪成本和使用情况](/docs/zh-CN/agent-sdk/cost-tracking) |
| `maxThinkingTokens` | `number` | `undefined` | *已弃用：* 改用 `thinking`。思考过程的最大令牌数 |
| `maxTurns` | `number` | `undefined` | 最大代理轮次（工具使用往返） |
| `mcpServers` | `Record<string, [`McpServerConfig`](#mcpserverconfig)>` | `{}` | MCP 服务器配置 |
| `model` | `string` | CLI 的默认值 | Claude 模型别名或完整模型名称。请参阅[接受的值和特定于提供商的 ID](/docs/zh-CN/model-config#available-models) |
| `onElicitation` | `(request: ElicitationRequest, options: { signal: AbortSignal }) => Promise<ElicitationResult>` | `undefined` | 用于处理 MCP 引出请求的回调。当 MCP 服务器请求用户输入且没有 hook 首先处理它时调用。未提供时，未处理的引出请求会自动被拒绝 |
| `outputFormat` | `{ type: 'json_schema', schema: JSONSchema }` | `undefined` | 为代理结果定义输出格式。请参阅[结构化输出](/docs/zh-CN/agent-sdk/structured-outputs)了解详情 |
| `outputStyle` | `string` | `undefined` | 不是 `Options` 字段。改为在内联 [`settings`](/docs/zh-CN/settings) 对象或设置文件中设置 `outputStyle`。请参阅[激活输出样式](/docs/zh-CN/agent-sdk/modifying-system-prompts#activate-an-output-style) |
| `pathToClaudeCodeExecutable` | `string` | 从捆绑的本地二进制文件自动解析 | Claude Code 可执行文件的路径。仅在安装期间跳过可选依赖项或您的平台不在支持的集合中时需要 |
| `permissionMode` | [`PermissionMode`](#permissionmode) | `'default'` | 会话的权限模式 |
| `permissionPromptToolName` | `string` | `undefined` | 权限提示的 MCP 工具名称 |
| `permissionPrompts` | `'host' \| 'none'` | `'host'` | 谁回答权限提示：`'host'` 将它们路由到您的 [`canUseTool`](#canusetool) 回调或 `permissionPromptToolName` 工具，`'none'` [拒绝会提示的调用](/docs/zh-CN/agent-sdk/permissions#how-permissions-are-evaluated)。需要 Claude Code v2.1.259 或更高版本 |
| `persistSession` | `boolean` | `true` | 当为 `false` 时，禁用会话持久化到磁盘。会话之后无法恢复 |
| `planModeInstructions` | `string` | `undefined` | Plan Mode 的自定义工作流说明。当 `permissionMode` 为 `'plan'` 时，此字符串替换默认 Plan Mode 工作流正文。CLI 仍然使用只读强制前导和 ExitPlanMode 协议页脚包装它 |
| `plugins` | [`SdkPluginConfig`](#sdkpluginconfig)`[]` | `[]` | 从本地路径加载自定义 plugins。请参阅[Plugins](/docs/zh-CN/agent-sdk/plugins)了解详情 |
| `projectConfigRoot` | `string` | `undefined` | `cwd` 是 worktree 的受信任检出的绝对路径。Claude Code 从此目录而不是 `cwd` 读取项目设置、`.mcp.json` 和项目的 `.claude/` commands、agents、skills、workflows、routines 和 output styles，并将 `CLAUDE_PROJECT_DIR` 设置为它。Hooks、helper scripts 如 `apiKeyHelper` 和 stdio MCP 服务器以此目录作为其工作目录启动。`CLAUDE.md` 文件和 `.claude/rules/` 仍然从 `cwd` 加载。需要 Claude Code v2.1.275 或更高版本 |
| `promptSuggestions` | `boolean` | `false` | 启用提示建议。在每个轮次后，Claude Code 发出 `prompt_suggestion` 消息，包含预测的下一个用户提示。Claude Code 不会为某些轮次生成建议，例如当您的帐户接近或达到其使用限制时。请参阅[Claude Code 何时跳过建议](/docs/zh-CN/interactive-mode#when-claude-code-skips-suggestions) |
| `resume` | `string` | `undefined` | 要恢复的会话 ID |
| `resumeDropsTurn` | `string` | `undefined` | 使用 `resumeSessionAt`：截断恢复打算丢弃的轮次的提示 UUID。当丢弃的范围包含任何不可归因于该轮次的内容（例如吸收的排队消息或任务通知）时，Claude Code 会拒绝恢复，并在拒绝消息中命名 `--resume-drops-turn` 标志。仅 Agent SDK 和打印模式恢复读取该对。需要 Claude Code v2.1.223 或更高版本 |
| `resumeSessionAt` | `string` | `undefined` | 在特定消息 UUID 处恢复会话 |
| `sandbox` | [`SandboxSettings`](#sandboxsettings) | `undefined` | 以编程方式配置 sandbox 行为。请参阅[Sandbox 设置](#sandboxsettings)了解详情 |
| `sessionId` | `string` | 自动生成 | 为会话使用特定的 UUID 而不是自动生成一个 |
| `sessionStore` | [`SessionStore`](/docs/zh-CN/agent-sdk/session-storage#the-sessionstore-interface) | `undefined` | 将会话记录镜像到外部后端，以便另一个主机可以恢复它们。请参阅[将会话持久化到外部存储](/docs/zh-CN/agent-sdk/session-storage) |
| `sessionStoreFlush` | `'batched' \| 'eager'` | `'batched'` | *Alpha.* `sessionStore` 的刷新模式。未设置 `sessionStore` 时忽略 |
| `settings` | `string \| Settings` | `undefined` | 内联[设置](/docs/zh-CN/settings)对象、设置文件路径或内联 JSON 字符串。填充[优先级顺序](/docs/zh-CN/settings#settings-precedence)中的标志设置层。使用 [`applyFlagSettings()`](#applyflagsettings) 在运行时更改 |
| `settingSources` | [`SettingSource`](#settingsource)`[]` | CLI 默认值（所有源） | 控制加载哪些文件系统设置。传递 `[]` 以禁用用户、项目和本地设置。[端点管理的策略](/docs/zh-CN/managed-settings#delivery-mechanisms)无论如何都会加载；当会话使用组织凭证在[符合条件的配置](/docs/zh-CN/server-managed-settings#platform-availability)上进行身份验证时，会获取服务器管理的设置。请参阅[使用 Claude Code 功能](/docs/zh-CN/agent-sdk/claude-code-features#what-settingsources-does-not-control) |
| `skills` | `string[] \| 'all'` | `undefined` | 会话可用的 skills。传递 `'all'` 以启用每个发现的 skill，或传递 skill 名称列表。仅传递确切名称。在 Agent SDK v0.3.221 或更高版本上，SDK 在启动 Claude Code 进程之前会以错误拒绝格式错误和通配符形式的名称。设置后，SDK 会自动将 Skill 工具添加到 `allowedTools`。如果您也传递 `tools`，请在该列表中包含 `'Skill'`。请参阅[Skills](/docs/zh-CN/agent-sdk/skills) |
| `spawnClaudeCodeProcess` | `(options: SpawnOptions) => SpawnedProcess` | `undefined` | 用于生成 Claude Code 进程的自定义函数。用于在 VM、容器或远程环境中运行 Claude Code |
| `stderr` | `(data: string) => void` | `undefined` | stderr 输出的回调 |
| `strictMcpConfig` | `boolean` | `false` | 仅使用在 `mcpServers` 中传递的服务器，并忽略项目 `.mcp.json`、用户设置、plugin 提供的 MCP 服务器和[claude.ai connectors](/docs/zh-CN/mcp#use-mcp-servers-from-claude-ai) |
| `systemPrompt` | `string \| string[] \| { type: 'custom'; prompt: string \| string[]; snapshot?: boolean } \| { type: 'preset'; preset: 'claude_code'; append?: string; excludeDynamicSections?: boolean; snapshot?: boolean }` | `undefined`（最小提示） | 系统提示配置。传递字符串以获取自定义提示，或 `{ type: 'preset', preset: 'claude_code' }` 以使用 Claude Code 的系统提示。传递一个字符串数组，其中包含导出的 `SYSTEM_PROMPT_DYNAMIC_BOUNDARY` 常量在静态和每个请求部分之间，以[缓存自定义提示的静态部分](/docs/zh-CN/agent-sdk/modifying-system-prompts#cache-the-static-part-of-a-custom-prompt)。使用预设对象形式时，添加 `append` 以使用其他说明扩展它，并设置 `excludeDynamicSections: true` 以将每个会话上下文移到第一条用户消息中，以便[更好地跨机器重用提示缓存](/docs/zh-CN/agent-sdk/modifying-system-prompts#improve-prompt-caching-across-users-and-machines)。设置 `snapshot: false` 以在每个请求上重建提示，而不是[重用会话在其第一个请求上记录的提示](/docs/zh-CN/agent-sdk/modifying-system-prompts#change-the-prompt-of-an-existing-session)。要在自定义提示上设置 `snapshot`，请传递 `{ type: 'custom', prompt }` 形式。`{ type: 'custom' }` 形式和 `snapshot` 字段需要 TypeScript Agent SDK v0.3.257 或更高版本 |
| `taskBudget` | `{ total: number }` | `undefined` | *Alpha.* API 端任务预算（以令牌为单位）。设置后，模型会被告知其剩余令牌预算，以便它可以调整工具使用速度并在达到限制前完成 |
| `thinking` | [`ThinkingConfig`](#thinkingconfig) | 支持的模型为 `{ type: 'adaptive' }` | 控制 Claude 的思考/推理行为。请参阅 [`ThinkingConfig`](#thinkingconfig) 了解选项 |
| `title` | `string` | `undefined` | 会话的显示标题。通过 `resume` 或 `continue` 恢复时，恢复的会话的持久化标题优先；使用 [`renameSession()`](#renamesession) 重新标题现有会话 |
| `toolAliases` | `Record<string, string>` | `undefined` | 将内置工具名称映射到 MCP 工具名称，以便 Claude 调用您的 MCP 实现而不是内置工具。例如，`{ Bash: 'mcp__workspace__bash' }` |
| `toolConfig` | [`ToolConfig`](#toolconfig) | `undefined` | 内置工具行为的配置。请参阅 [`ToolConfig`](#toolconfig) 了解详情 |
| `tools` | `string[] \| { type: 'preset'; preset: 'claude_code' }` | `undefined` | 工具配置。传递工具名称数组或使用预设获取 Claude Code 的默认工具 |
| `verbatimPrompts` | `boolean` | `false` | 按照书写方式传递每个提示。SDK 使用 `client_composed: true` 发送每条用户消息。请参阅 [`client_composed`](#sdkusermessage) 了解 Claude Code 在这些消息上跳过的内容。当您的提示文本包含最终用户未输入的内容时使用此选项。对于每轮控制，请将其关闭并改为在各个流式消息上设置 `client_composed`。需要 TypeScript Agent SDK v0.3.280 或更高版本和 Claude Code v2.1.248 或更高版本；这些 SDK 版本捆绑的 Claude Code 版本满足 Claude Code 要求 |

<h4 id="handle-slow-or-stalled-api-responses">
  处理缓慢或停滞的 API 响应
</h4>

CLI 子进程读取多个环境变量，这些变量控制 API 超时和停滞检测。通过 `env` 选项传递它们：

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

const result = query({
  prompt: "Analyze this code",
  options: {
    env: {
      ...process.env,
      API_TIMEOUT_MS: "120000",
      CLAUDE_CODE_MAX_RETRIES: "2",
      CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS: "120000",
    },
  },
});
```

* `API_TIMEOUT_MS`：Anthropic 客户端上的每个请求超时，以毫秒为单位。默认 `600000`。适用于主循环和所有 subagents。
* `CLAUDE_CODE_MAX_RETRIES`：最大 API 重试次数。默认 `10`，上限为 `15`。每次重试都有自己的 `API_TIMEOUT_MS` 窗口，因此最坏情况下的实际时间大约是 `API_TIMEOUT_MS × (CLAUDE_CODE_MAX_RETRIES + 1)` 加上退避。对于需要等待更长时间中断的无人值守运行，设置 [`CLAUDE_CODE_RETRY_WATCHDOG=1`](/docs/zh-CN/errors#tune-retry-behavior)：它无限期重试瞬时容量错误，从 Claude Code v2.1.199 开始，为其他瞬时错误提高默认值至 `300` 并移除此变量的上限。
* `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS`：subagents 的停滞监视程序。当流监视程序打开时，默认值为 `CLAUDE_STREAM_IDLE_TIMEOUT_MS` 加 5 分钟，即 `600000`，除非您提高该变量。当流监视程序关闭时，默认值为 `600000`。在 v2.1.257 之前，默认值始终为 `600000`。

  计时器在每个流事件上重置。在停滞时，Claude Code 中止 subagent 并向父级报告停滞。对于后台 subagent，它也会将任务标记为失败并附加任何部分结果。
* `CLAUDE_ENABLE_STREAM_WATCHDOG` 与 `CLAUDE_STREAM_IDLE_TIMEOUT_MS`：当标头已到达但响应正文停止流式传输时中止请求的流监视程序。监视程序对所有提供商默认启用；设置 `CLAUDE_ENABLE_STREAM_WATCHDOG=0` 以禁用它。`CLAUDE_STREAM_IDLE_TIMEOUT_MS` 默认为 `300000` 并被限制为该最小值。中止后，[自动重试](/docs/zh-CN/errors#automatic-retries)涵盖 Claude Code 根据响应进度的程度所做的事情。

  当监视程序等待 `ANTHROPIC_BASE_URL` 后面的网关用保活 ping 保持打开的响应时，设置 `includePartialMessages` 的主机继续接收 `ping` [流事件](#sdkpartialassistantmessage)，因此将这些帧读作活跃性而不是在沉默时超时会话。在 v2.1.257 之前，帧在最后一个真实流事件后 5 分钟停止。

<h3 id="query-object">
  `Query` 对象
</h3>

由 `query()` 函数返回的接口。

```typescript theme={null}
interface Query extends AsyncGenerator<SDKMessage, void> {
  interrupt(): Promise<SDKControlInterruptResponse | undefined>;
  rewindFiles(
    userMessageId: string,
    options?: { dryRun?: boolean }
  ): Promise<RewindFilesResult>;
  setPermissionMode(mode: PermissionMode): Promise<void>;
  setModel(model?: string): Promise<void>;
  setMaxThinkingTokens(maxThinkingTokens: number | null): Promise<void>;
  applyFlagSettings(settings: {
    [K in keyof Settings]?: K extends 'effortLevel'
      ? 'low' | 'medium' | 'high' | 'xhigh' | 'max' | null
      : Settings[K] | null;
  }): Promise<void>;
  updateSettings(
    source: 'localSettings' | 'userSettings',
    settings: Record<string, unknown>,
  ): Promise<void>;
  initializationResult(): Promise<SDKControlInitializeResponse>;
  reinitialize(): Promise<SDKControlInitializeResponse>;
  supportedCommands(): Promise<SlashCommand[]>;
  supportedModels(): Promise<ModelInfo[]>;
  supportedAgents(): Promise<AgentInfo[]>;
  mcpServerStatus(): Promise<McpServerStatus[]>;
  getContextUsage(opts?: {
    detail?: 'summary' | 'full';
  }): Promise<SDKControlGetContextUsageResponse>;
  readFile(
    path: string,
    options?: { maxBytes?: number; encoding?: 'utf-8' | 'base64' }
  ): Promise<SDKControlReadFileResponse | null>;
  reloadPlugins(options?: {
    holdOnCacheImpact?: boolean;
  }): Promise<SDKControlReloadPluginsResponse>;
  reloadSkills(): Promise<SDKControlReloadSkillsResponse>;
  reloadOutputStyles(): Promise<SDKControlReloadOutputStylesResponse>;
  accountInfo(): Promise<AccountInfo>;
  reconnectMcpServer(serverName: string): Promise<void>;
  toggleMcpServer(serverName: string, enabled: boolean): Promise<void>;
  setMcpServers(servers: Record<string, McpServerConfig>): Promise<McpSetServersResult>;
  readMcpResource(serverName: string, uri: string): Promise<SDKControlMcpReadResourceResponse>;
  streamInput(stream: AsyncIterable<SDKUserMessage>): Promise<void>;
  stopTask(taskId: string): Promise<void>;
  close(): void;
}
```

<h4 id="methods">
  方法
</h4>

| 方法 | 描述 |
| :- | :- |
| `interrupt()` | 中断查询。仅在流式输入模式下可用。当 CLI 在 [`SDKSystemMessage.capabilities`](#sdksystemmessage) 中通告 `interrupt_receipt_v1` 功能时，使用列出中断时待处理的消息的 [`SDKControlInterruptResponse`](#sdkcontrolinterruptresponse) 进行解决。在 v2.1.205 之前的 CLI 上解决为 `undefined` |
| `rewindFiles(userMessageId, options?)` | 将文件恢复到指定用户消息时的状态。传递 `{ dryRun: true }` 以预览更改。需要 `enableFileCheckpointing: true`。请参阅[文件 checkpointing](/docs/zh-CN/agent-sdk/file-checkpointing) |
| `setPermissionMode()` | 更改权限模式（仅在流式输入模式下可用） |
| `setModel()` | 更改模型（仅在流式输入模式下可用）。传递 `undefined` 或字符串 `"default"` 重置为[Claude Code 的默认模型](/docs/zh-CN/model-config) |
| `setMaxThinkingTokens()` | *已弃用：* 改用 `thinking` 选项。更改最大思考令牌数。传递 `null` 会将思考重置为会话默认值：清除中期覆盖，对于禁用思考的会话思考保持关闭 |
| `applyFlagSettings(settings)` | 在运行时将设置合并到会话的标志设置层中（仅在流式输入模式下可用）。请参阅 [`applyFlagSettings()`](#applyflagsettings) |
| `updateSettings(source, settings)` | 将一个允许列表键写入项目的本地设置文件或您的用户设置文件，以便该值对后续会话持久化。请参阅 [`updateSettings()`](#updatesettings)。需要 TypeScript SDK v0.3.257 或更高版本，它捆绑 Claude Code v2.1.257 |
| `initializationResult()` | 返回完整的初始化结果，包括支持的命令、模型、帐户信息和输出样式配置 |
| `reinitialize()` | 重新发送 `initialize` 控制请求到运行的 CLI，并返回新的结果而不是缓存的首次连接结果。在传输间隙后使用它，例如在断开连接后重新连接到会话，以便待处理的权限请求再次到达您的 `canUseTool` 回调。使回调对每个请求 ID 幂等，因为响应丢失的请求会再次分派。需要 Claude Code v2.1.195 或更高版本 |
| `supportedCommands()` | 返回可用的 slash commands。从 Agent SDK v0.3.216 开始，列表反映中期命令更改；请参阅 [`SDKCommandsChangedMessage`](#sdkcommandschangedmessage) |
| `supportedModels()` | 返回具有显示信息的可用模型 |
| `supportedAgents()` | 返回可用的 subagents 作为 [`AgentInfo`](#agentinfo)`[]` |
| `mcpServerStatus()` | 返回连接的 MCP 服务器的状态作为 [`McpServerStatus`](#mcpserverstatus)`[]` |
| `getContextUsage(opts?)` | 返回 [`SDKControlGetContextUsageResponse`](#sdkcontrolgetcontextusageresponse)，按类别、skill 和工具分解会话的上下文窗口使用情况。使用默认 `detail`，它与 `/context` 在交互式会话中显示的数据相同。[`detail` 选项](#sdkcontrolgetcontextusageresponse)需要 Agent SDK v0.3.257 或更高版本 |
| `readFile(path, options?)` | 从会话的文件系统读取文件。Claude Code 根据 `cwd` 解析路径；[`readFile()` 可以读取什么](#what-readfile-can-read)列出它提供的文件。传递 `{ maxBytes }` 以更改读取上限（默认 1 MB，上限 10 MB）和 `{ encoding: 'base64' }` 用于二进制文件，如图像。使用 [`SDKControlReadFileResponse`](#sdkcontrolreadfileresponse) 进行解决，或在权限拒绝、文件丢失或传输错误时使用 `null`。需要 TypeScript SDK v0.2.121 或更高版本 |
| `reloadPlugins(options?)` | 从磁盘重新加载 plugins，以便您在会话中期安装或编辑的 plugins 到达运行的会话。使用 [`SDKControlReloadPluginsResponse`](#sdkcontrolreloadpluginsresponse) 进行解决，列出会话的 commands、subagents、plugins 和 MCP 服务器状态。需要 Agent SDK v0.2.85 或更高版本。[`holdOnCacheImpact` 选项](#sdkcontrolreloadpluginsresponse)需要 Agent SDK v0.3.268 或更高版本 |
| `reloadSkills()` | 从磁盘重新加载 skills，以便您在会话中期添加或编辑的 skills 对运行的会话可用。使用 [`SDKControlReloadSkillsResponse`](#sdkcontrolreloadskillsresponse) 进行解决，列出重新加载后可用的 skills。需要 Agent SDK v0.3.163 或更高版本 |
| `reloadOutputStyles()` | 重新读取[输出样式](/docs/zh-CN/output-styles)从磁盘，以便您在会话中期添加或编辑的样式文件对运行的会话可用。使用 [`SDKControlReloadOutputStylesResponse`](#sdkcontrolreloadoutputstylesresponse) 进行解决，列出重新加载后可用的样式名称。需要 Agent SDK v0.3.261 或更高版本 |
| `accountInfo()` | 返回帐户信息 |
| `reconnectMcpServer(serverName)` | 按名称重新连接 MCP 服务器。如果名称也匹配设置文件（如 `.mcp.json` 或 `~/.claude.json`）中的条目，Claude Code 会重新连接您通过 [`mcpServers`](#options) 或 `setMcpServers()` 配置的服务器，而不是设置文件条目。该解析顺序需要 Claude Code v2.1.257 或更高版本 |
| `toggleMcpServer(serverName, enabled)` | 按名称启用或禁用 MCP 服务器，名称解析与 `reconnectMcpServer()` 相同。禁用会断开 stdio、SSE 或 HTTP 服务器的连接并移除其工具；对于您使用 `setMcpServers()` 在会话中期添加的服务器，工具移除需要 Claude Code v2.1.285 或更高版本 |
| `setMcpServers(servers)` | 动态替换此会话的 MCP 服务器集。使用 [`McpSetServersResult`](#mcpsetserversresult) 进行解决，命名添加和删除的服务器以及任何错误 |
| `readMcpResource(serverName, uri)` | *Alpha.* 从连接的 MCP 服务器读取一个 MCP Apps `ui://` 资源，以便您的应用程序可以呈现工具的小部件。使用 [`SDKControlMcpReadResourceResponse`](#sdkcontrolmcpreadresourceresponse) 进行解决。需要 TypeScript Agent SDK v0.3.280 或更高版本 |
| `streamInput(stream)` | 将输入消息流式传输到查询以进行多轮对话 |
| `stopTask(taskId)` | 按 ID 停止运行的后台任务 |
| `close()` | 关闭查询并终止底层进程。强制结束查询并清理所有资源 |

<h4 id="applyflagsettings">
  `applyFlagSettings()`
</h4>

在运行的会话上更改[设置](/docs/zh-CN/settings)而无需重新启动查询。当没有专用设置器的设置需要在会话中期更改时使用它，例如在代理读取不受信任的输入后收紧 `permissions`。`setModel()` 和 `setPermissionMode()` 是这两个键的专用设置器；`applyFlagSettings()` 是接受任何设置键子集的通用形式，在此处传递 `model` 的行为与 `setModel()` 相同。

仅某些键在会话中期生效：

* **在下一个轮次应用**：`effortLevel`、`ultracode`、`permissions`、`hooks`、`skillOverrides`、`fastMode`、`agent`。切换 `agent` 也会在下一个轮次应用该代理的模型覆盖和 hooks。其系统提示在下一个轮次应用，或在[重用记录的系统提示](/docs/zh-CN/agent-sdk/modifying-system-prompts#change-the-prompt-of-an-existing-session)的会话中，一旦会话被压缩。
* **在当前轮次应用**：`model`。如果您在 Claude 处理轮次时切换 `model`，Claude 已在生成的响应在旧模型上完成，轮次的其余部分（从 Claude Code 对模型进行的下一个调用开始）使用新模型。Subagents 保持自己的模型。在 v2.1.212 之前，中期切换等待下一个轮次。
* **会话中期无效**：系统提示选项。这些在启动时解决一次，因此运行的会话保持原始值，即使调用成功。要更改它们，请启动新会话。

`effortLevel` 接受一个[努力级别](/docs/zh-CN/model-config#adjust-effort-level)名称。它也接受 `"ultracode"`，它请求 `xhigh` 努力与[ultracode](/docs/zh-CN/workflows#let-claude-decide-with-ultracode)打开。`applyFlagSettings()` 声明 `effortLevel` 不包含该值，因此在 TypeScript 中传递 `{ ultracode: true, effortLevel: "xhigh" }` 以获得相同的结果，或仅 [`ultracode`](/docs/zh-CN/settings-reference#ultracode) 键以在会话的当前努力级别打开 ultracode。`ultracode` 值需要 Claude Code v2.1.203 或更高版本，仅由 `applyFlagSettings()` 接受，不由设置文件中的 `effortLevel` 键接受。在 v2.1.284 之前，仅 `ultracode` 键也将级别设置为 `xhigh`。

这些值被写入标志设置层，这是内联 `query()` 的 `settings` 选项在启动时填充的同一层。这与[优先级部分](#settings-precedence)称为编程选项的层相同。

连续调用浅合并顶级键。第二次调用 `{ permissions: {...} }` 会替换先前调用中的整个 `permissions` 对象，而不是深度合并到其中。

要清除您使用 `applyFlagSettings()` 设置的键，请为该键传递 `null`。大多数键然后回退首先到 `query()` 的 `settings` 选项在启动时设置的值，然后到较低优先级源。清除的 `model` 重置为[Claude Code 的默认模型](/docs/zh-CN/model-config)，即使设置文件设置 `model`。传递 `undefined` 无效，因为 JSON 序列化会将其删除。

除了 `model` 的三个键重置会话状态而不是回退：

* `effortLevel: null` 将会话返回到模型的默认努力级别，而不是 `query()` 的 `effort` 选项或设置文件中的 `effortLevel`。
* `agent: null` 从下一个轮次开始在没有代理的情况下运行主线程，而不是恢复 `query()` 的 `agent` 选项或设置文件中的 `agent`。如果清除的代理应用了自己的模型，会话返回到在启动时解决的模型。
* `ultracode: null` 关闭 ultracode，如 `false` 一样，而不是恢复设置文件中的 `ultracode` 值。会话保持其当前努力级别，因此在同一调用中传递 `effortLevel` 以更改它。

仅在流式输入模式下可用，与 `setModel()` 和 `setPermissionMode()` 的约束相同。

下面的示例在会话中期切换活动模型，然后清除覆盖，以便模型重置为[Claude Code 的默认模型](/docs/zh-CN/model-config)。

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

const q = query({ prompt: messageStream });

// 覆盖会话其余部分的模型
await q.applyFlagSettings({ model: "claude-opus-4-6" });

// 稍后：清除覆盖；模型重置为 Claude Code 的默认模型
await q.applyFlagSettings({ model: null });
```

<Note>
  `applyFlagSettings()` 仅适用于 TypeScript。Python SDK 不公开等效方法。
</Note>

<h4 id="updatesettings">
  `updateSettings()`
</h4>

将一个允许列表键写入设置文件，以便该值对加载该源的后续会话持久化。每个源接受一个键，具有字符串值：

* **`"localSettings"`**：接受 `outputStyle` 并将其合并到项目的本地设置文件 `.claude/settings.local.json` 中。新样式在会话的下一个请求时生效。
* **`"userSettings"`**：接受 `effortLevel` 并将其保存为会话当前模型的默认[努力级别](/docs/zh-CN/model-config#adjust-effort-level)，在您的用户设置文件中的 [`modelSettings`](/docs/zh-CN/settings-reference#modelsettings) 下。传递 `max` 不写任何内容，因为 `max` 仅限会话。运行的会话无论如何都保持其当前努力级别，因此当您也想更改它时调用 [`applyFlagSettings()`](#applyflagsettings)。此源需要 TypeScript SDK v0.3.277 或更高版本，它捆绑 Claude Code v2.1.277。

当请求携带任何其他键、会话通过远程传输运行以及会话的 [`settingSources`](#options) 排除您命名的源时，调用会拒绝。不支持删除键。

<h3 id="warmquery">
  `WarmQuery`
</h3>

由 [`startup()`](#startup) 返回的句柄。子进程已生成并初始化，因此在此句柄上调用 `query()` 会直接将提示写入准备好的进程，无需启动延迟。

```typescript theme={null}
interface WarmQuery extends AsyncDisposable {
  query(prompt: string | AsyncIterable<SDKUserMessage>): Query;
  close(): void;
}
```

<h4 id="methods-2">
  方法
</h4>

| 方法 | 描述 |
| :- | :- |
| `query(prompt)` | 向预热的子进程发送提示并返回 [`Query`](#query-object)。每个 `WarmQuery` 只能调用一次 |
| `close()` | 关闭子进程而不发送提示。使用此方法丢弃不再需要的预热查询 |

`WarmQuery` 实现 `AsyncDisposable`，因此可以与 `await using` 一起使用以进行自动清理。

<h3 id="spareprocess">
  `SpareProcess`
</h3>

*Alpha.* 由 [`prewarm()`](#prewarm) 返回的句柄：一个已启动的 Claude Code 进程，尚未绑定到会话，可以声明一次。需要 TypeScript Agent SDK v0.3.282 或更高版本。

```typescript theme={null}
interface SpareProcess extends AsyncDisposable {
  claim(params: {
    prompt: string | AsyncIterable<SDKUserMessage>;
    options: ClaimOptions;
  }): Query;
  readonly claimed: Promise<{ cwd: string; sessionId: string; parkedMs?: number; sdkMcpSettled: boolean }>;
  readonly exited: Promise<void>;
  close(): void;
}
```

<h4 id="members">
  成员
</h4>

| 成员 | 描述 |
| :- | :- |
| `claim({ prompt, options })` | 将备用进程绑定到 `options.cwd` 中的会话并发送其第一条消息。同步返回 [`Query`](#query-object)，如 `query()` 一样。每个 `SpareProcess` 只能调用一次 |
| `claimed` | 一旦 Claude Code 接受声明，就使用会话的工作目录和 ID 进行解决。当 Claude Code 拒绝声明、进程在声明前退出或关闭，以及当会话运行时不带您请求的 `model` 或 `maxThinkingTokens` 时拒绝，消息以 `option_not_applied` 开头。 |
| `exited` | 当进程退出时解决，无论是否声明。替换在您声明前退出的备用进程 |
| `close()` | 终止进程。在声明前，这会丢弃备用进程并拒绝 `claimed` |

`options.cwd` 是必需的。声明也可以设置 `additionalDirectories`、`model`、`permissionMode`、`maxThinkingTokens`、`settings` 中的标志设置覆盖、`appendSystemPrompt`、`title`、`agents` 和 `env` 中的每个会话令牌。

Claude Code 可以拒绝声明，例如对于不存在的文件夹或其项目设置设置 `env`、`agent` 或 `model` 的文件夹。当 `claimed` 拒绝消息以 `option_not_applied` 开头时，会话运行时不带您请求的 `model` 或 `maxThinkingTokens`。在任何其他拒绝后，您的提示尚未运行，因此改用 `query()` 启动会话。

<h3 id="sdkcontrolinitializeresponse">
  `SDKControlInitializeResponse`
</h3>

`initializationResult()` 的返回类型。包含会话初始化数据。

```typescript theme={null}
type SDKControlInitializeResponse = {
  commands: SlashCommand[];
  agents: AgentInfo[];
  output_style: string;
  available_output_styles: string[];
  models: ModelInfo[];
  account: AccountInfo;
  fast_mode_state?: "off" | "cooldown" | "on";
  fast_mode_disabled_reason?: FastModeDisabledReason;
  hooks_applied?: boolean;
};
```

`hooks_applied` 报告 Claude Code 是否注册了 `initialize` 请求携带的 `hooks`。SDK 在会话启动时发送该请求一次，并在每个 [`reinitialize()`](#query-object) 调用上再次发送。该字段需要 Agent SDK v0.3.238 或更高版本。

当请求不携带 hooks 时，Claude Code 会省略该字段。当请求携带 hooks 时，该值取决于请求是否是会话的第一个初始化，以及对于重复的请求，它如何到达会话：

* `true`：Claude Code 注册了 hooks。会话的第一个初始化返回此值。通过 CLI 的 stdin 发送的重复初始化也返回 `true`。在这种情况下，新请求中的 hooks 替换之前注册的 hooks。
* `false`：Claude Code 忽略了 hooks。发送到远程会话的重复初始化返回此值，因此加入会话的第二个客户端无法替换第一个客户端注册的 hooks。

在 Agent SDK v0.3.238 之前，响应从不携带该字段，Claude Code 在每个重复初始化上忽略 `hooks`。

响应始终报告 `fast_mode_state`，当某些东西阻止[快速模式](/docs/zh-CN/fast-mode)时，`fast_mode_disabled_reason` 携带原因代码，以便您可以解释阻止的状态而不是重新推导可用性。两种行为都需要 Claude Code v2.1.219 或更高版本。在 v2.1.219 之前，当快速模式不可用时响应会省略 `fast_mode_state`，并且从不携带原因。有关原因代码及其含义，请参阅结果消息上的 [`fast_mode_disabled_reason`](#sdkresultmessage)。

成功 `initialize` 的控制响应包装器也携带 `pending_permission_requests` 数组。该字段位于响应包装器本身，而不是上面的 `SDKControlInitializeResponse` 有效负载中。每个条目都是一个完整的 `control_request` 消息，具有与会话在运行时为权限请求流式传输的相同 `{ type: "control_request", request_id, request }` 形状。

该数组列出此 Claude Code 进程已发出且尚未解决的权限请求。SDK 为您读取数组并将每个条目分派到您的 [`canUseTool`](#canusetool) 回调，这与 [`reinitialize()`](#query-object) 在传输间隙后触发的相同重新发送。使用重复的请求 ID 幂等地处理，因为条目可以重复回调已在连接断开前收到的请求。

该数组在成功 `initialize` 响应上始终存在，当此进程没有未解决的权限请求时为空。需要 Claude Code v2.1.268 或更高版本。较早的版本可能会省略该字段，因此如果您自己解析线路协议，请将缺失的字段视为较旧的 CLI，而不是没有待处理的证明。

<h3 id="sdkcontrolinterruptresponse">
  `SDKControlInterruptResponse`
</h3>

中断收据：[`interrupt()`](#query-object) 在通告 [`SDKSystemMessage.capabilities`](#sdksystemmessage) 中的 `interrupt_receipt_v1` 功能的 CLI 上解决的值。需要 Claude Code v2.1.205 或更高版本。较早的 CLI 使用空成功有效负载回答中断，因此 `interrupt()` 解决为 `undefined`。

```typescript theme={null}
type SDKControlInterruptResponse = {
  still_queued: string[];
  cancelled?: string[];
};
```

`still_queued` 列出中断时待处理的用户消息的 UUID：仍在队列中的消息，加上 Claude Code 已从队列中取出用于下一个轮次的任何消息。除非您首先取消它，否则每个都在中断后作为其自己的轮次运行。如果您在第一个轮次启动之前中断，Claude Code 会在轮次启动时立即中止该轮次，该轮次中列出的消息不会获得响应。

使用收据来决定是否重新发送任何内容。列出的消息如果您不取消它会进入对话，因此重新发送它会向 Claude 传递两次。

使用这些注意事项解释列表：

* 仅出现已使用 UUID 入队的消息。空数组并不意味着没有其他内容会运行。
* 仅列出主线程消息。寻址到 subagent 的消息超出范围。
* 列表可以包括您的客户端从未发送的 UUID，例如[计划任务](/docs/zh-CN/scheduled-tasks)触发器。忽略您不识别的 UUID，而不是将其视为错误。

直接驱动 CLI 控制协议的客户端（而不是通过 `interrupt()`）可以在 `interrupt` 控制请求上设置 `cancel_queued: true`。Claude Code v2.1.219 及更高版本在 [`SDKSystemMessage.capabilities`](#sdksystemmessage) 中通告 `interrupt_cancel_queued_v1` 功能的支持；较早的 CLI 忽略该字段并让排队的消息照常运行。这样的中断也会取消每条否则会在 `still_queued` 下列出的消息：收据在 `cancelled` 下列出它们，`still_queued` 为空，它们都不运行。

`cancelled` 列表与 `still_queued` 具有相同的注意事项。`interrupt()` 方法从不发送 `cancel_queued`，因此它解决的收据不携带 `cancelled`。

收据是在处理中断时拍摄的快照，在干净中断时，它在中断轮次的 [`SDKResultMessage`](#sdkresultmessage) 之前到达。在该结果之后读取收据而不是检查队列：循环立即启动下一个排队的轮次，因此您在结果后检查的队列已经改变。

<h3 id="sdkcontrolgetcontextusageresponse">
  `SDKControlGetContextUsageResponse`
</h3>

[`getContextUsage()`](#query-object) 的返回类型。使用默认 `detail`，这是 Claude Code 在交互式会话中为 `/context` 命令呈现的相同有效负载，因此除了令牌计数外，它还携带显示字段，如 `color` 和 `gridRows`，Claude Code 使用这些字段来绘制 `/context` 使用情况网格。

该方法的可选 `detail` 参数选择 Claude Code 如何计算每个类别。使用默认值 `'full'`，Claude Code 使用令牌计数 API 请求计算每个类别。传递 `{ detail: 'summary' }` 以从最后一个响应的使用情况和本地估计获取答案。没有令牌计数请求出去，每个类别的数字是近似的。`detail` 参数需要 Agent SDK v0.3.257 或更高版本。

当您发送 `/context` 作为提示而不是调用该方法时，Claude Code 会将 [`SDKContextUsage`](#sdkcontextusage) 有效负载附加到传递结果的助手消息的 `context_usage` 字段。该字段需要 Agent SDK v0.3.232 或更高版本。

```typescript theme={null}
type SDKControlGetContextUsageResponse = {
  categories: {
    name: string;
    tokens: number;
    color: string;
    isDeferred?: boolean;
    kind: "used" | "free" | "buffer" | "deferred";
  }[];
  totalTokens: number;
  maxTokens: number;
  rawMaxTokens: number;
  percentage: number;
  gridRows: {
    color: string;
    isFilled: boolean;
    categoryName: string;
    tokens: number;
    percentage: number;
    squareFullness: number;
  }[][];
  model: string;
  memoryFiles: {
    path: string;
    type: string;
    tokens: number;
  }[];
  mcpTools: {
    name: string;
    serverName: string;
    tokens: number;
    isLoaded?: boolean;
  }[];
  deferredBuiltinTools?: {
    name: string;
    tokens: number;
    isLoaded: boolean;
  }[];
  systemTools?: {
    name: string;
    tokens: number;
  }[];
  systemPromptSections?: {
    name: string;
    tokens: number;
  }[];
  agents: {
    agentType: string;
    source: string;
    tokens: number;
  }[];
  slashCommands?: {
    totalCommands: number;
    includedCommands: number;
    tokens: number;
  };
  skills?: {
    totalSkills: number;
    includedSkills: number;
    tokens: number;
    skillFrontmatter: {
      name: string;
      source: string;
      tokens: number;
    }[];
  };
  autoCompactThreshold?: number;
  isAutoCompactEnabled: boolean;
  messageBreakdown?: {
    toolCallTokens: number;
    toolResultTokens: number;
    attachmentTokens: number;
    assistantMessageTokens: number;
    userMessageTokens: number;
    redirectedContextTokens: number;
    unattributedTokens: number;
    toolCallsByType: {
      name: string;
      callTokens: number;
      resultTokens: number;
    }[];
    attachmentsByType: {
      name: string;
      tokens: number;
    }[];
  };
  apiUsage: {
    input_tokens: number;
    output_tokens: number;
    cache_creation_input_tokens: number;
    cache_read_input_tokens: number;
  } | null;
};
```

从集合字段读取令牌归属：

* `categories` 保存每个类别的总计。每个条目的 `kind` 使用与 [`SDKContextUsageCategory`](#sdkcontextusagecategory) 相同的值对行进行分类。在其上对行进行分类，而不是在显示 `name` 上。该字段需要 Agent SDK v0.3.268 或更高版本。
* `mcpTools` 和 `agents` 将令牌归属于各个 MCP 工具和 subagents。
* `memoryFiles` 列出每个加载的内存文件及其成本。
* `skills.skillFrontmatter` 将 skill 列表的令牌归属于每个包含的 skill。每个 skill 的计数测量每个 skill 的列表条目，因为 Claude Code 实际发送它，这可能比 skill 的完整 frontmatter 更短。比较 `skills.totalSkills` 与 `skills.includedSkills` 以查看每个发现的 skill 是否进入列表。

`totalTokens` 是会话的当前上下文使用情况，`maxTokens` 是针对该使用情况测量的窗口。该窗口是模型的上下文窗口，或当应用一个时的较低自动压缩窗口。`rawMaxTokens` 携带与 `maxTokens` 相同的值，`percentage` 是 `totalTokens` 作为该窗口的四舍五入百分比。

Claude Code 保留可选的 `deferredBuiltinTools`、`systemTools` 和 `systemPromptSections` 诊断未设置，因此即使类型声明它们，也应该期望它们不存在。

<h3 id="sdkcontrolreadfileresponse">
  `SDKControlReadFileResponse`
</h3>

[`readFile()`](#query-object) 的返回类型。

```typescript theme={null}
type SDKControlReadFileResponse = {
  contents: string;
  absPath: string;
  truncated?: boolean;
  encoding?: 'base64';
};
```

`contents` 保存文件文本，或当您请求 `encoding: 'base64'` 时的 base64 数据；响应的 `encoding` 字段在这种情况下设置为 `'base64'`。`absPath` 是解析的绝对路径。当文件长于 `maxBytes` 上限且内容在该限制处被切割时，`truncated` 被设置。

<h4 id="what-readfile-can-read">
  `readFile()` 可以读取什么
</h4>

`readFile()` 提供的文件集比 Read 工具更窄：

* 会话的工作目录之一内的常规文件，如 `cwd` 和 `additionalDirectories`
* Claude Code 自己的一些文件用于会话，如工具结果

Read deny 和 ask 规则仍然阻止匹配的路径，广泛的 Read allow 规则不会向 `readFile()` 打开文件系统的其余部分。对于任何其他内容，调用使用 `null` 进行解决。

<h3 id="sdkcontrolreloadpluginsresponse">
  `SDKControlReloadPluginsResponse`
</h3>

[`reloadPlugins()`](#query-object) 的返回类型。

```typescript theme={null}
type SDKControlReloadPluginsResponse = {
  commands: SlashCommand[];
  agents: AgentInfo[];
  plugins: {
    name: string;
    path: string;
    source?: string;
    version?: string;
  }[];
  mcpServers: McpServerStatus[];
  error_count: number;
  held?: boolean;
  cache_impact?: {
    mcp_servers_added: string[];
    mcp_servers_removed: string[];
    lsp_tool_change: ("adds" | "may-add" | "removes" | "may-remove") | null;
  };
};
```

集合字段描述调用后的会话：

* `commands`、`agents` 和 `mcpServers`：会话的 commands、subagents 和 MCP 服务器状态，采用 `supportedCommands()`、`supportedAgents()` 和 `mcpServerStatus()` 返回的相同形状。`supportedAgents()` 继续返回在初始化时捕获的列表，因此在此处读取 `agents` 以获取重新加载后的集合
* `plugins`：每个加载的 plugin，其 `name` 和安装 `path`。`version` 重复 plugin 的 manifest 声明的内容，是 plugin 作者控制的，因此在信任之前验证它。当 manifest 未声明任何内容时省略
* `error_count`：加载 plugins 的错误数

将 `{ holdOnCacheImpact: true }` 传递给 `reloadPlugins()` 以保持会使对话的提示缓存失效的重新加载，而不是应用它。Claude Code 运行交互式 `/reload-plugins` 命令在[警告缓存成本](/docs/zh-CN/prompt-caching#enabling-or-disabling-a-plugin)之前进行的检查。该选项需要 Agent SDK v0.3.268 或更高版本。比 v2.1.268 更旧的 Claude Code 可执行文件（例如您通过 `pathToClaudeCodeExecutable` 指向的）会忽略该选项并应用重新加载。

当您传递该选项时，读取 `held` 以了解发生了什么：

* `true`：重新加载未被应用，集合字段描述会话仍然是什么样子。`cache_impact` 说明应用会改变什么。要应用，请再次调用 `reloadPlugins()` 而不使用该选项。
* `false`：检查未发现缓存影响，重新加载已被应用。
* 不存在：您未传递该选项，或 Claude Code 可执行文件比 v2.1.268 更旧并应用了重新加载。

`cache_impact` 仅在 `held: true` 旁边存在。`mcp_servers_added` 和 `mcp_servers_removed` 命名重新加载会注册或删除的 plugin MCP 服务器，作为作用域 `plugin:<plugin>:<server>` 名称。名称是 plugin 作者编写的，因此在显示之前验证它们。`lsp_tool_change` 说明应用是否会添加或删除 LSP 工具，或 `null` 当它都不做时。`may-` 形式意味着检查无法完全看到待处理的 plugin 集。

<h3 id="sdkcontrolreloadskillsresponse">
  `SDKControlReloadSkillsResponse`
</h3>

[`reloadSkills()`](#query-object) 的返回类型。

```typescript theme={null}
type SDKControlReloadSkillsResponse = {
  skills: SlashCommand[];
};
```

`skills` 列出重新加载后可用的 skills，采用 `supportedCommands()` 返回的相同 [`SlashCommand`](#slashcommand) 形状。

<h3 id="sdkcontrolreloadoutputstylesresponse">
  `SDKControlReloadOutputStylesResponse`
</h3>

[`reloadOutputStyles()`](#query-object) 的返回类型。

```typescript theme={null}
type SDKControlReloadOutputStylesResponse = {
  available_output_styles: string[];
};
```

`available_output_styles` 列出重新加载后可用的内置和自定义输出样式的名称。

<h3 id="sdkcontrolmcpreadresourceresponse">
  `SDKControlMcpReadResourceResponse`
</h3>

[`readMcpResource()`](#query-object) 的返回类型，携带 MCP 服务器的 `resources/read` 结果。需要 TypeScript Agent SDK v0.3.280 或更高版本。

```typescript theme={null}
type SDKControlMcpReadResourceResponse = {
  contents: {
    uri: string;
    mimeType?: string;
    text?: string;
    blob?: string;
    _meta?: Record<string, unknown>;
  }[];
};
```

将 `readMcpResource()` 的服务器名称作为 `mcpServerStatus()` 报告的名称和 `ui://` URI（例如工具在其 [`_meta`](#mcpserverstatus) 中声明的 `ui.resourceUri`）传递。对于任何其他 URI 方案、您的应用程序自己托管的 [SDK MCP 服务器](#createsdkmcpserver) 以及未连接的服务器，调用会拒绝。当初始化消息的 [`capabilities`](#sdksystemmessage) 包含 `mcp_read_resource_v1` 时可用。

每个 `contents` 条目是服务器发送的一个内容项。`blob` 为二进制项保存 base64 数据，`_meta` 是项目自己的 `_meta`，其中 MCP Apps 服务器放置资源的 `ui.csp` 和 `ui.permissions`。内容是不受信任的第三方 HTML，因此在沙箱中呈现它们。

<h3 id="agentdefinition">
  `AgentDefinition`
</h3>

以编程方式定义的 subagent 的配置。

```typescript theme={null}
type AgentDefinition = {
  description: string;
  tools?: string[];
  disallowedTools?: string[];
  prompt: string;
  model?: string;
  mcpServers?: AgentMcpServerSpec[];
  skills?: string[];
  initialPrompt?: string;
  maxTurns?: number;
  background?: boolean;
  omitClaudeMd?: boolean;
  memory?: "user" | "project" | "local";
  effort?: "low" | "medium" | "high" | "xhigh" | "max" | number;
  permissionMode?: PermissionMode;
  criticalSystemReminder_EXPERIMENTAL?: string;
};
```

| 字段 | 必需 | 描述 |
| :- | :- | :- |
| `description` | 是 | 何时使用此代理的自然语言描述 |
| `tools` | 否 | 允许的工具名称数组。如果省略，继承[可用于 subagents 的每个工具](/docs/zh-CN/sub-agents#available-tools)。要将 Skills 预加载到代理的上下文中，请使用 `skills` 字段而不是在此处列出 `'Skill'` |
| `disallowedTools` | 否 | 要为此代理明确禁止的工具名称数组。也接受 MCP 服务器级别的模式：`mcp__server` 或 `mcp__server__*` 移除该服务器的每个工具，`mcp__*` 移除任何服务器的每个 MCP 工具 |
| `prompt` | 是 | 代理的系统提示 |
| `model` | 否 | 此代理的模型覆盖。接受别名，如 `'fable'`、`'opus'`、`'sonnet'`、`'haiku'`、`'inherit'`，或完整的模型 ID。`'inherit'` 使用主模型。当您省略它时，Claude Code 在[subagent 模型顺序](/docs/zh-CN/sub-agents#choose-a-model)中选择模型 |
| `mcpServers` | 否 | 此代理的 MCP 服务器规范 |
| `skills` | 否 | 要预加载到代理上下文中的 skill 名称数组 |
| `initialPrompt` | 否 | 当此代理作为主线程代理运行时，自动提交为第一个用户轮次 |
| `maxTurns` | 否 | 停止前的最大代理轮次数（API 往返） |
| `background` | 否 | 调用时将此代理作为非阻塞后台任务运行 |
| `omitClaudeMd` | 否 | 当此代理作为 subagent 运行时，在没有用户、项目和本地 CLAUDE.md 文件的情况下运行此代理；托管策略文件仍然加载。将其用于从 Agent 工具提示中获取所需内容的代理。当此代理作为主线程代理运行时忽略。需要 TypeScript Agent SDK v0.3.271 或更高版本 |
| `memory` | 否 | 此代理的内存源：`'user'`、`'project'` 或 `'local'` |
| `effort` | 否 | 此代理的推理努力级别。接受命名级别或整数 |
| `permissionMode` | 否 | 此代理内工具执行的权限模式。[subagent 继承规则](/docs/zh-CN/agent-sdk/permissions#available-modes)决定何时应用。请参阅 [`PermissionMode`](#permissionmode) |
| `criticalSystemReminder_EXPERIMENTAL` | 否 | 实验性：添加到系统提示的关键提醒 |

<h3 id="agentmcpserverspec">
  `AgentMcpServerSpec`
</h3>

指定 subagent 可用的 MCP 服务器。可以是服务器名称（字符串，引用父级 `mcpServers` 配置中的服务器）或内联服务器配置记录，将服务器名称映射到配置。

```typescript theme={null}
type AgentMcpServerSpec = string | Record<string, McpServerConfigForProcessTransport>;
```

其中 `McpServerConfigForProcessTransport` 是 `McpStdioServerConfig | McpSSEServerConfig | McpHttpServerConfig | McpSdkServerConfig`。

<h3 id="settingsource">
  `SettingSource`
</h3>

控制 SDK 从哪些基于文件系统的配置源加载设置。

```typescript theme={null}
type SettingSource = "user" | "project" | "local";
```

| 值 | 描述 | 位置 |
| :- | :- | :- |
| `'user'` | 全局用户设置 | `~/.claude/settings.json` |
| `'project'` | 共享项目设置（版本控制） | `.claude/settings.json` |
| `'local'` | 本地项目设置，当 Claude Code 将设置保存到其中时被 gitignored | `.claude/settings.local.json` |

<h4 id="default-behavior">
  默认行为
</h4>

当 `settingSources` 被省略或 `undefined` 时，`query()` 加载与 Claude Code CLI 相同的文件系统设置：用户、项目和本地。请参阅[settingSources 不控制的内容](/docs/zh-CN/agent-sdk/claude-code-features#what-settingsources-does-not-control)了解无论此选项如何都会读取的输入，以及如何禁用它们。

<h4 id="why-use-settingsources">
  为什么使用 settingSources
</h4>

**禁用文件系统设置：**

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

// 不从磁盘加载用户、项目或本地设置
const result = query({
  prompt: "Analyze this code",
  options: { settingSources: [] }
});
```

**仅加载特定设置源：**

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

// 仅加载项目设置，忽略用户和本地
const result = query({
  prompt: "Run CI checks",
  options: {
    settingSources: ["project"] // 仅 .claude/settings.json
  }
});
```

要加载 CLAUDE.md 项目说明，请在 `settingSources` 中包含 `"project"`。请参阅[修改系统提示](/docs/zh-CN/agent-sdk/modifying-system-prompts#claude-md-files-for-project-level-instructions)了解 CLAUDE.md 加载如何与系统提示选项交互。

<h4 id="settings-precedence">
  设置优先级
</h4>

加载多个源时，设置按此优先级合并（从高到低）：

1. 本地设置（`.claude/settings.local.json`）
2. 项目设置（`.claude/settings.json`）
3. 用户设置（`~/.claude/settings.json`）

编程选项（如 `agents`、`allowedTools` 和 `settings`）覆盖用户、项目和本地文件系统设置。托管策略设置优先于编程选项。

<h3 id="permissionmode">
  `PermissionMode`
</h3>

```typescript theme={null}
type PermissionMode =
  | "default" // 标准权限行为
  | "acceptEdits" // 自动接受文件编辑
  | "bypassPermissions" // 绕过权限检查；显式 ask 规则仍然提示
  | "plan" // Plan Mode - 仅读取工具
  | "dontAsk" // 不提示权限，如果未预先批准则拒绝
  | "auto"; // 模型分类器批准或拒绝权限提示
```

<h3 id="canusetool">
  `CanUseTool`
</h3>

用于控制工具使用的自定义权限函数类型。

该函数是 SDK 替代交互式权限提示：仅当[权限评估流](/docs/zh-CN/agent-sdk/permissions#how-permissions-are-evaluated)解决为提示时才调用它。已由 `allowedTools` 条目、设置 allow 规则或权限模式（如 `acceptEdits` 或 `bypassPermissions`）批准的工具调用永远不会调用它。要限制每个工具调用，请改用 [`PreToolUse` hook](/docs/zh-CN/agent-sdk/hooks)。

[任何模式都不自动批准的操作](/docs/zh-CN/permission-modes#actions-no-mode-auto-approves)不会被 allow 规则预先批准；请参阅[权限如何被评估](/docs/zh-CN/agent-sdk/permissions#how-permissions-are-evaluated)了解哪些到达回调以及在 `dontAsk` 和 `auto` 模式下会发生什么。

```typescript theme={null}
type CanUseTool = (
  toolName: string,
  input: Record<string, unknown>,
  options: {
    signal: AbortSignal;
    suggestions?: PermissionUpdate[];
    blockedPath?: string;
    mcpServer?: { name: string; source: string };
    decisionReason?: string;
    defaultToNo?: boolean;
    suppressAlwaysAllowRule?: boolean;
    toolUseID: string;
    agentID?: string;
    requestId: string;
  }
) => Promise<PermissionResult | null>;
```

| 选项 | 类型 | 描述 |
| :- | :- | :- |
| `signal` | `AbortSignal` | 如果应中止操作，则发出信号 |
| `suggestions` | [`PermissionUpdate`](#permissionupdate)`[]` | 建议的权限更新，以便用户不会再次被提示此工具。Bash 提示包括一个建议，其中包含 `localSettings` [目标](#permissionupdatedestination)，因此在 `updatedPermissions` 中返回它会将规则写入 `.claude/settings.local.json` 并在会话中持久化。 |
| `blockedPath` | `string` | 触发权限请求的文件路径（如果适用） |
| `mcpServer` | `{ name: string; source: string }` | 对于 `mcp__*` 工具，提供该工具的 MCP 服务器及其定义来源，具有 [`McpServerProvenance`](#mcpserverprovenance) 的字段。对于其他工具不存在。需要 Agent SDK v0.3.274 或更高版本 |
| `decisionReason` | `string` | 解释为什么触发此权限请求 |
| `defaultToNo` | `boolean` | 当 `true` 时，单个杂散按键不得批准此请求：在其拒绝选项上打开您的提示，不要预先选择批准，并且不提供单键批准快捷方式。需要 Agent SDK v0.3.268 或更高版本 |
| `suppressAlwaysAllowRule` | `boolean` | 当 `true` 时，不为此请求提供持久的始终允许选择，因为它会写入的规则授予超过请求自身操作的权限。需要 Agent SDK v0.3.268 或更高版本 |
| `toolUseID` | `string` | 此特定工具调用在助手消息中的唯一标识符 |
| `agentID` | `string` | 如果在 subagent 中运行，subagent 的 ID |
| `requestId` | `string` | `control_request` 信封的 `request_id`。您的应用程序在其自己的通道上发送的 `control_response`（例如签名的 HTTP POST）必须回显此值，以便 Claude Code 进程可以将回复与请求匹配 |

回调通常通过返回 [`PermissionResult`](#permissionresult) 来解决请求，SDK 将其写回其传输作为 `control_response`。仅当您的应用程序已通过其自己的通道为此请求发送 `control_response`（回显 `requestId`）时才返回 `null`；SDK 然后跳过将响应写入其传输。在任何其他情况下返回 `null` 会使工具调用无限期被阻止，因为永远不会发送 `control_response` 且权限提示不会超时。

`requestId` 选项和 `null` 返回值需要 Claude Code v2.1.199 或更高版本。

<h3 id="permissionresult">
  `PermissionResult`
</h3>

权限检查的结果。

```typescript theme={null}
type PermissionResult =
  | {
      behavior: "allow";
      updatedInput?: Record<string, unknown>;
      updatedPermissions?: PermissionUpdate[];
      toolUseID?: string;
    }
  | {
      behavior: "deny";
      message: string;
      interrupt?: boolean;
      toolUseID?: string;
    };
```

<h3 id="toolconfig">
  `ToolConfig`
</h3>

内置工具行为的配置。

```typescript theme={null}
type ToolConfig = {
  askUserQuestion?: {
    previewFormat?: "markdown" | "html";
  };
};
```

| 字段 | 类型 | 描述 |
| :- | :- | :- |
| `askUserQuestion.previewFormat` | `'markdown' \| 'html'` | 选择加入 [`AskUserQuestion`](/docs/zh-CN/agent-sdk/user-input#question-format) 选项上的 `preview` 字段并设置其内容格式。未设置时，Claude 不发出预览 |

<h3 id="mcpserverconfig">
  `McpServerConfig`
</h3>

MCP 服务器的配置。

```typescript theme={null}
type McpServerConfig =
  | McpStdioServerConfig
  | McpSSEServerConfig
  | McpHttpServerConfig
  | McpSdkServerConfigWithInstance;
```

<h4 id="mcpstdioserverconfig">
  `McpStdioServerConfig`
</h4>

```typescript theme={null}
type McpStdioServerConfig = {
  type?: "stdio";
  command: string;
  args?: string[];
  env?: Record<string, string>;
};
```

<h4 id="mcpsseserverconfig">
  `McpSSEServerConfig`
</h4>

```typescript theme={null}
type McpSSEServerConfig = {
  type: "sse";
  url: string;
  headers?: Record<string, string>;
};
```

<h4 id="mcphttpserverconfig">
  `McpHttpServerConfig`
</h4>

```typescript theme={null}
type McpHttpServerConfig = {
  type: "http";
  url: string;
  headers?: Record<string, string>;
};
```

<h4 id="mcpsdkserverconfigwithinstance">
  `McpSdkServerConfigWithInstance`
</h4>

```typescript theme={null}
type McpSdkServerConfigWithInstance = {
  type: "sdk";
  name: string;
  timeout?: number;
  instance: McpServer;
};
```

<h4 id="mcpclaudeaiproxyserverconfig">
  `McpClaudeAIProxyServerConfig`
</h4>

```typescript theme={null}
type McpClaudeAIProxyServerConfig = {
  type: "claudeai-proxy";
  url: string;
  id: string;
};
```

<h3 id="sdkpluginconfig">
  `SdkPluginConfig`
</h3>

SDK 中加载 plugins 的配置。

```typescript theme={null}
type SdkPluginConfig = {
  type: "local";
  path: string;
  skipMcpDiscovery?: boolean;
};
```

| 字段 | 类型 | 描述 |
| :- | :- | :- |
| `type` | `'local'` | 必须为 `'local'`（目前仅支持本地 plugins） |
| `path` | `string` | 插件目录的绝对或相对路径 |
| `skipMcpDiscovery` | `boolean` | 当为 `true` 时，SDK 从此 plugin 加载 skills、hooks、agents 和 commands，但不读取其 `.mcp.json` 或 manifest `mcpServers`。当您的应用程序拥有 plugin 的 MCP 连接时设置此选项。 |

**示例：**

```typescript theme={null}
plugins: [
  { type: "local", path: "./my-plugin" },
  { type: "local", path: "/absolute/path/to/plugin" }
];
```

有关创建和使用 plugins 的完整信息，请参阅[Plugins](/docs/zh-CN/agent-sdk/plugins)。

<h2 id="message-types">
  消息类型
</h2>

<h3 id="sdkmessage">
  `SDKMessage`
</h3>

查询返回的所有可能消息的联合类型。

```typescript theme={null}
type SDKMessage =
  | SDKAssistantMessage
  | SDKUserMessage
  | SDKUserMessageReplay
  | SDKResultMessage
  | SDKSystemMessage
  | SDKPartialAssistantMessage
  | SDKCompactBoundaryMessage
  | SDKStatusMessage
  | SDKLocalCommandOutputMessage
  | SDKHookStartedMessage
  | SDKHookProgressMessage
  | SDKHookResponseMessage
  | SDKPluginInstallMessage
  | SDKToolProgressMessage
  | SDKAuthStatusMessage
  | SDKTaskNotificationMessage
  | SDKTaskStartedMessage
  | SDKTaskProgressMessage
  | SDKTaskUpdatedMessage
  | SDKBackgroundTasksChangedMessage
  | SDKThinkingTokensMessage
  | SDKSessionStateChangedMessage
  | SDKWorkerShuttingDownMessage
  | SDKCommandsChangedMessage
  | SDKNotificationMessage
  | SDKFilesPersistedEvent
  | SDKToolUseSummaryMessage
  | SDKMemoryRecallMessage
  | SDKRateLimitEvent
  | SDKElicitationCompleteMessage
  | SDKPermissionDeniedMessage
  | SDKPromptSuggestionMessage
  | SDKAPIRetryMessage
  | SDKMirrorErrorMessage
  | SDKInformationalMessage
  | SDKConversationResetMessage;
```

<h3 id="sdkassistantmessage">
  `SDKAssistantMessage`
</h3>

助手响应消息。

```typescript theme={null}
type SDKAssistantMessage = {
  type: "assistant";
  uuid: UUID;
  session_id: string;
  message: BetaMessage; // From Anthropic SDK
  parent_tool_use_id: string | null;
  error?: SDKAssistantMessageError;
  aborted?: true;
  timestamp?: string;
  context_usage?: SDKContextUsage;
  user_message_uuid?: string;
  user_message_uuids?: string[];
  resume_reason?: string;
};
```

`message` 字段是来自 Anthropic SDK 的 [`BetaMessage`](https://platform.claude.com/docs/en/api/messages/create)。它包含 `id`、`content`、`model`、`stop_reason` 和 `usage` 等字段。

`SDKAssistantMessageError` 是以下之一：`'authentication_failed'`、`'oauth_org_not_allowed'`、`'account_on_hold'`、`'billing_error'`、`'rate_limit'`、`'overloaded'`、`'invalid_request'`、`'model_not_found'`、`'server_error'`、`'max_output_tokens'`、`'cloud_credential_error'` 或 `'unknown'`。其中四个值的含义超出了它们的名称：

* `'model_not_found'`：选定的模型不存在或对您的账户或部署不可用
* `'overloaded'`：API 返回 529，因为服务器处于容量限制，与 `'rate_limit'` 不同，后者是针对您配额的 429
* `'account_on_hold'`：[您的账户被冻结](/docs/zh-CN/errors#your-account-is-on-hold)
* `'cloud_credential_error'`：Claude Code 无法在其运行的机器上获取可用的 AWS 或 Google Cloud 凭证，因此没有请求到达云提供商。通常原因是云登录已过期或从未在该机器上完成，但暂时无法访问的凭证服务会报告相同的值。请参阅[无法加载 AWS 或 Google Cloud 凭证](/docs/zh-CN/errors#could-not-load-aws-or-google-cloud-credentials)。需要 TypeScript Agent SDK v0.3.267 或更高版本，其中包含 Claude Code v2.1.267

当中断或中止在流完成前截断助手消息时，`aborted` 为 `true`：消息没有 `stop_reason`，内容可能在单词中间结束。该字段在正常完成的消息上不存在。它需要 Agent SDK v0.3.214 或更高版本。

Claude Code 在该轮的第一条助手消息上设置 `user_message_uuid` 和 `user_message_uuids`，条件在 [`user_message_uuid`](#user_message_uuid) 中。当 Claude Code 重新运行被重启中断的轮时，重新运行的携带这些字段的助手消息也携带 [`resume_reason`](#resume_reason)。

`timestamp` 是消息内容在生成它的进程上完成生成的 ISO 8601 时间。该值来自该机器的时钟，因此仅用于显示，不要按它排序消息。一个 API 轮可以产生多条共享 `message.id` 的助手消息，每条都有自己的 `timestamp`。当字段不存在时，回退到您收到消息的时间。

`context_usage` 是 `/context` 报告的结构化副本，类型为 [`SDKContextUsage`](#sdkcontextusage)，需要 Agent SDK v0.3.232 或更高版本。当您发送 `/context` 作为提示时，Claude Code 将报告作为助手消息传递，其 `message.content` 包含 markdown 表格，并将 `context_usage` 附加到同一消息。Claude Code 不在任何其他助手消息上设置该字段，早期版本在没有它的情况下传递 `/context` 表格，因此当字段存在时从字段读取分解，当不存在时回退到 markdown 文本。

<h3 id="sdkusermessage">
  `SDKUserMessage`
</h3>

用户输入消息。

```typescript theme={null}
type SDKUserMessage = {
  type: "user";
  uuid?: UUID;
  session_id?: string;
  message: MessageParam; // From Anthropic SDK
  pasted_content?: MessageParam["content"][];
  parent_tool_use_id: string | null;
  isSynthetic?: boolean;
  shouldQuery?: boolean;
  client_composed?: true;
  tool_use_result?: unknown;
  origin?: SDKMessageOrigin;
  inline_pastes?: string[];
};
```

设置 `pasted_content` 以发送用户粘贴到您的提示 UI 中而不是输入的内容，每个粘贴一个条目，每个条目是字符串或内容块数组。Claude Code 按顺序在输入的文本后追加每个条目的文本，并可能将每个粘贴包装在 `<pasted_content>` 标签中。除文本外的块被忽略，因此在 `message.content` 中发送图像和文档。需要 Agent SDK v0.3.277 或更高版本。

设置 `shouldQuery` 或 `client_composed` 以改变 Claude Code 处理您发送的消息的方式：

* `shouldQuery`：设置为 `false` 以将消息附加到记录中而不触发助手轮。消息被保留并合并到下一条触发轮的用户消息中。使用此方法注入上下文，例如您在带外运行的命令的输出，而无需在模型调用上花费。
* `client_composed`：设置为 `true` 以让 Claude Code 按原样传递消息文本。Claude Code 然后不展开 `@path` 或 [`@server:resource`](/docs/zh-CN/mcp#use-mcp-resources) 提及，也不运行以 `/` 开头的文本作为命令。当 [`verbatimPrompts`](#options) 选项打开时，SDK 在每条消息上设置该字段。需要 TypeScript Agent SDK v0.3.280 或更高版本和 Claude Code v2.1.248 或更高版本。

在携带 `tool_result` 块的消息上，`tool_use_result` 是工具的结构化输出对象，而不是发送给模型的文本。其形状取决于匹配 `tool_use` 块命名的工具，因此该字段的类型为 `unknown`；内置形状列在[工具输出类型](#tool-output-types)下。

对于 `Agent` 工具，`tool_use_result` 是 [`AgentOutput`](#agent-2)。在 `completed` 结果上，`content` 包含子代理的报告，不包含 Claude Code 附加到 `tool_result` 文本的代理 ID 和使用情况尾部，因此从 `tool_use_result` 渲染而不是解析该文本。

对于结果包含 `resource_link` 块的 MCP 工具，`tool_use_result` 是一个对象，其中包含 [`SDKMcpResourceLink`](#sdkmcpresourcelink) 条目的 `resourceLinks` 数组。Claude 将每个链作为 `tool_result` 块中的一行文本接收，因此读取 `resourceLinks` 以渲染服务器返回的文件，而不是解析该文本。Claude Code 在结果没有链时省略 `resourceLinks`，在来自子代理的结果上省略，每个结果最多保留 50 个链，并在数组达到 64 KiB 序列化 JSON 后停止添加链。`resourceLinks` 需要 Agent SDK v0.3.257 或更高版本。

设置 `inline_pastes` 以告诉 Claude Code `message.content` 的哪些部分用户粘贴而不是输入，每个粘贴一个字符串。提示文本保留在用户放置的位置。Claude Code 可能会在其所在位置将每个列出的粘贴包装在 `<pasted_content>` 标签中，以便 Claude 可以区分粘贴的材料和用户自己的话。只有提示最后一个文本块中的粘贴被包装。需要 TypeScript Agent SDK v0.3.280 或更高版本。

<h3 id="sdkusermessagereplay">
  `SDKUserMessageReplay`
</h3>

带有必需 UUID 的重放用户消息。

```typescript theme={null}
type SDKUserMessageReplay = {
  type: "user";
  uuid: UUID;
  session_id: string;
  message: MessageParam;
  parent_tool_use_id: string | null;
  isSynthetic?: boolean;
  client_composed?: true;
  tool_use_result?: unknown;
  origin?: SDKMessageOrigin;
  isReplay: true;
};
```

从会话外部注入的用户轮，其 [`origin`](#sdkmessageorigin) 类型为 `peer` 或 `channel`，无论是在活跃轮期间传递还是在会话空闲时启动新轮，都作为重放到达流。在 v2.1.207 之前，在会话空闲时传递的注入轮在流上不产生消息，仅在您重新读取记录时出现。

<h3 id="sdkresultmessage">
  `SDKResultMessage`
</h3>

最终结果消息。

```typescript theme={null}
type SDKResultMessage =
  | {
      type: "result";
      subtype: "success";
      uuid: UUID;
      session_id: string;
      duration_ms: number;
      duration_api_ms: number;
      is_error: boolean;
      api_error_status?: number | null;
      num_turns: number;
      result: string;
      stop_reason: string | null;
      ttft_ms?: number;
      ttft_stream_ms?: number;
      user_message_uuid?: string;
      user_message_uuids?: string[];
      resume_reason?: string;
      local_command?: string;
      request_sent_wall_ms?: number;
      first_content_frame_ms?: number;
      first_stream_post_ms?: number;
      first_stream_post_ack_ms?: number;
      first_stream_post_wall_ms?: number;
      total_cost_usd: number;
      usage: NonNullableUsage;
      modelUsage: { [modelName: string]: ModelUsage };
      permission_denials: SDKPermissionDenial[];
      queued_turn_count?: number;
      structured_output?: unknown;
      deferred_tool_use?: { id: string; name: string; input: Record<string, unknown> };
      terminal_reason?: TerminalReason;
      result_index?: number;
      fast_mode_state?: FastModeState;
      fast_mode_disabled_reason?: FastModeDisabledReason;
      origin?: SDKMessageOrigin;
    }
  | {
      type: "result";
      subtype:
        | "error_max_turns"
        | "error_during_execution"
        | "error_max_budget_usd"
        | "error_max_structured_output_retries";
      uuid: UUID;
      session_id: string;
      duration_ms: number;
      duration_api_ms: number;
      is_error: boolean;
      num_turns: number;
      stop_reason: string | null;
      total_cost_usd: number;
      usage: NonNullableUsage;
      modelUsage: { [modelName: string]: ModelUsage };
      permission_denials: SDKPermissionDenial[];
      queued_turn_count?: number;
      errors: string[];
      startup_failure_reason?: SDKStartupFailureReason;
      user_message_uuid?: string;
      user_message_uuids?: string[];
      resume_reason?: string;
      terminal_reason?: TerminalReason;
      result_index?: number;
      fast_mode_state?: FastModeState;
      fast_mode_disabled_reason?: FastModeDisabledReason;
      origin?: SDKMessageOrigin;
    };
```

结果上的多个字段除了 `subtype` 之外还提供诊断详情：

* `api_error_status`：终止对话的 API 错误的 HTTP 状态码。当轮在没有 API 错误的情况下结束时不存在或为 `null`。
* `ttft_ms`：首个令牌的时间（毫秒），在第一条完整助手消息到达时测量。仅在成功分支上存在。
* `ttft_stream_ms`：直到第一个 `message_start` 流事件（响应流打开时）的时间（毫秒）。低于 `ttft_ms`；两者之间的差距是流传输第一条消息所花费的时间。仅在成功分支上存在。
* `user_message_uuid`：您发送的消息的 `uuid`，该轮回答了该消息。请参阅 [`user_message_uuid`](#user_message_uuid) 了解哪些结果携带它。
* `user_message_uuids`：您发送的每条消息的 `uuid`，Claude Code 在该轮中回答了这些消息。请参阅 [`user_message_uuids`](#user_message_uuids)。
* `resume_reason`：Claude Code 重新运行该轮的原因，在重启中断后。请参阅 [`resume_reason`](#resume_reason)。
* `local_command`：轮分派的命令的名称，在轮由命令完成而不进入代理循环的成功结果上，例如 `/compact`。名称折叠为小写字母和下划线，因此 `/reload-plugins` 报告 `reload_plugins`。MCP 服务器提供的命令和内置 `/mcp` 报告 `mcp`。您自己定义的命令报告 `custom`。参数从不包含。在进入代理循环的每个轮上不存在，在运行无命令的发送上不存在。需要 Agent SDK v0.3.268 或更高版本。
* `request_sent_wall_ms`：Claude Code 分派 API 请求的纪元毫秒，用于与服务器端时间戳的连接。仅与 [`user_message_uuid`](#user_message_uuid) 一起存在，在成功结果上，其中 `is_error` 为 false，且轮发送了 API 请求。
* `first_content_frame_ms`：直到第一个 `content_block_start` 或 `content_block_delta` 流事件的时间（毫秒），计算思考块作为内容。仅在成功分支上存在，当 `is_error` 为 false 时。需要 Agent SDK v0.3.260 或更高版本。
* `first_stream_post_ms`、`first_stream_post_ack_ms`、`first_stream_post_wall_ms`：上传轮的第一个流事件的时间。Claude Code 仅在它流传输到 claude.ai 的会话中记录它们，例如[云会话](/docs/zh-CN/claude-code-on-the-web)，`query()` 产生的结果不携带它们。需要 Agent SDK v0.3.260 或更高版本。
* `usage`：仅主代理循环。排除子代理和辅助模型调用，在流式输入会话中按轮计算。对于令牌/成本会计，优先使用 `modelUsage`。
* `modelUsage`：在此 `query()` 调用期间通过查询管道进行的每个模型调用的每模型总计，包括主循环、子代理和内部调用（如压缩和 Workflow 代理）。该管道外的辅助调用（如权限分类器和令牌计数请求）被排除。恢复会话的调用也计算[从会话早期调用恢复的每模型总计](/docs/zh-CN/agent-sdk/cost-tracking#accumulate-costs-across-multiple-calls)。在流式输入会话中，总计在轮中是累积的，因此读取最新结果而不是跨结果求和。请参阅[在流式输入模式中跟踪成本](/docs/zh-CN/agent-sdk/cost-tracking#track-costs-in-streaming-input-mode)了解重置，以及[在会话崩溃后恢复总计](/docs/zh-CN/agent-sdk/cost-tracking#recover-totals-after-a-session-crash)了解零化结果。
* `total_cost_usd`：累积估计成本（美元），涵盖与 `modelUsage` 相同的调用并在相同点重置。恢复会话的调用也计算[从会话早期调用恢复的总计](/docs/zh-CN/agent-sdk/cost-tracking#accumulate-costs-across-multiple-calls)。这是一个估计值，不是账单声明。请参阅[跟踪成本和使用情况](/docs/zh-CN/agent-sdk/cost-tracking)了解准确性注意事项。
* `queued_turn_count`：您发送的带有 `origin: { kind: "human" }` 的消息数，在 Claude Code 产生结果时仍在等待。请参阅 [`queued_turn_count`](#queued_turn_count) 了解 `0` 和缺失字段告诉您什么。
* `result_index`：此结果在运行的传递顺序中的位置，从 0 开始计算，跨越进程写入的每个结果。在两个分支上存在。写入失败的结果仍然消耗其编号，因此序列中的间隙意味着结果丢失。需要 Agent SDK v0.3.268 或更高版本。
* `startup_failure_reason`：Claude Code 拒绝启动的原因，在它在已知启动失败时退出前写入的 `error_during_execution` 结果上。请参阅 [`startup_failure_reason`](#startup_failure_reason) 了解值以及哪些失败携带它。需要 Agent SDK v0.3.274 或更高版本。
* `terminal_reason`：循环结束的原因。`"completed"`、`"max_turns"`、`"tool_deferred"`、`"aborted_streaming"`、`"aborted_tools"`、`"hook_stopped"`、`"stop_hook_prevented"`、`"background_requested"`、`"blocking_limit"`、`"rapid_refill_breaker"`、`"prompt_too_long"`、`"image_error"`、`"model_error"`、`"api_error"`、`"malformed_tool_use_exhausted"`、`"budget_exhausted"`、`"structured_output_retry_exhausted"`、`"tool_deferred_unavailable"` 或 `"turn_setup_failed"` 之一。
* `fast_mode_state`：`"on"`、`"off"` 或 `"cooldown"` 之一。
* `fast_mode_disabled_reason`：[快速模式](/docs/zh-CN/fast-mode)现在不可用的原因。当没有任何东西阻止快速模式时不存在，尽管请求仍可能以标准速度运行。在快速模式速率限制后的冷却期间，Claude Code 报告 `fast_mode_state: "cooldown"` 且没有原因代码，并在冷却期过期时重新启用快速模式。需要 Claude Code v2.1.219 或更高版本。

使用原因代码在您自己的 UI 中解释为什么快速模式关闭，而不是重新推导可用性。每个代码命名阻止快速模式的检查：

| 原因代码 | 含义 |
| - | - |
| `free` | 账户没有快速模式需要的付费订阅或使用额度 |
| `preference` | 组织已禁用快速模式 |
| `extra_usage_disabled` | 账户的使用额度已关闭 |
| `network_error` | [可用性检查](/docs/zh-CN/fast-mode#use-fast-mode-behind-proxies-and-llm-gateways)无法到达 `api.anthropic.com` |
| `unknown` | Claude Code 无法确定可用性 |
| `not_first_party` | 会话使用 Anthropic API 以外的提供商 |
| `disabled_by_env` | [`CLAUDE_CODE_DISABLE_FAST_MODE`](/docs/zh-CN/env-vars) 已设置 |
| `model_not_allowed` | 快速模式 Opus 模型不在组织的 [`availableModels`](/docs/zh-CN/model-config#restrict-model-selection) 允许列表中 |
| `sdk_opt_in_required` | 会话未选择加入快速模式：在 [`settings`](#options) 选项中或通过 [`applyFlagSettings()`](#applyflagsettings) 传递 `fastMode: true` |
| `pending` | 可用性检查尚未完成 |

相同的字段对出现在 [`SDKSystemMessage`](#sdksystemmessage) 和 [`SDKControlInitializeResponse`](#sdkcontrolinitializeresponse) 上，因此您可以在第一轮之前读取快速模式状态。

`origin` 字段转发触发此结果的用户消息的 [`SDKMessageOrigin`](#sdkmessageorigin)。当 SDK 注入合成后续轮（例如对于完成的后台任务）时，生成的 `SDKResultMessage` 携带 `origin: { kind: "task-notification" }`。触发器触发和服务器验证的来自您其他会话的消息到达时也带有此类型，每个都带有[任务通知子类型](#task-notification-subkinds)中描述的 `subkind`。检查 `kind` 以区分回答您提示的结果和注入的后续，然后在路由或抑制它们之前进行区分。如果您的应用程序[声明计划运行](#declare-a-scheduled-run)，它们的结果也携带 `kind: "task-notification"`，因此不要仅在 `kind` 上抑制。

当多个后台任务完成一起排队时，Claude Code 可以在一轮中回答它们，而不是每个一轮。每个完成仍然产生自己的结果与此来源。Claude Code 一起回答的完成中除最后一个外的所有完成产生空结果，其中 `num_turns: 0`，按顺序，最后一个的结果携带回答它们全部的轮。

该字段在任何用户轮之前发出的结果上不存在，例如启动错误。

当 `PreToolUse` 钩子返回 `permissionDecision: "defer"` 时，结果具有 `stop_reason: "tool_deferred"` 和 `deferred_tool_use` 携带待处理工具的 `id`、`name` 和 `input`。读取此字段以在您自己的 UI 中显示请求，然后使用相同的 `session_id` 恢复以继续。请参阅[延迟工具调用以供稍后使用](/docs/zh-CN/hooks#defer-a-tool-call-for-later)了解完整往返。

<h4 id="user_message_uuid">
  `user_message_uuid`
</h4>

轮回答的 [`SDKUserMessage`](#sdkusermessage) 的 `uuid`，回显以便您可以将 Claude Code 的回复与您发送的消息匹配。Claude Code 仅在您在消息上设置 uuid 时回显 `uuid`。该字段在 `SDKUserMessage` 上是可选的，传递给 `query()` 的字符串提示不携带任何。

轮回答的消息取决于轮如何启动：

* **您发送的常规消息**，意思是没有 `isSynthetic: true` 的消息：轮在其整个运行中回答该消息。当您一起发送多条消息时，Claude Code 可以将它们合并为一轮，该字段然后仅携带最后一条消息的 `uuid`。要将回复与任何合并的消息匹配，请使用 [`user_message_uuids`](#user_message_uuids)。
* **您发送的带有 `isSynthetic: true` 的消息**：轮最初回答该消息。如果 Claude Code 在工具调用之间拾取您的常规消息，轮从那时起回答拾取的消息。回显合成消息的 `uuid` 需要 Agent SDK v0.3.265 或更高版本；早期版本在合成轮上不回显任何内容。
* **Claude Code 生成的提示以重新运行被重启中断的轮**（在 [`CLAUDE_CODE_RESUME_INTERRUPTED_TURN`](/docs/zh-CN/env-vars) 下）：当被中断轮的最后一个提示是您发送的常规消息时，无论它是打开轮还是 Claude Code 在轮期间拾取它，重新运行最初回答该消息。[`resume_reason`](#resume_reason) 告诉重新运行的帧来自被中断尝试的。当最后一个提示不是您的常规消息时，重新运行最初不回答您的任何消息。如果 Claude Code 在工具调用之间拾取您的常规消息，轮从那时起回答拾取的消息。回显被中断轮的提示需要 Agent SDK v0.3.268 或更高版本。
* **Claude Code 自己生成的任何其他提示**：轮最初不回答您的任何消息，其帧不携带回显。如果 Claude Code 在工具调用之间拾取您的常规消息，轮从那时起回答该消息。拾取回显需要 Agent SDK v0.3.265 或更高版本；早期版本在这些轮上不回显任何内容。

Claude Code 在三种帧上回显回答的消息的 `uuid`：

* **结果**：回答您发送的消息的轮的每个结果。在 Agent SDK v0.3.265 或更高版本上，每个这样的结果都携带它。在 v0.3.265 之前，常规消息启动的轮的成功结果在轮未发送 API 请求或以延迟工具调用结束时缺少它。在 v0.3.246 之前，错误结果也缺少它，在 v0.3.216 之前每个结果都缺少它。
* **轮的第一个回复**：第一条[助手消息](#sdkassistantmessage)，或使用 `includePartialMessages` 时第一条[流事件](#sdkpartialassistantmessage)，其 `event.type` 不是 `ping`，因此您可以在结果到达之前绑定回复。当轮流传输任何内容时，Claude Code 改为在第一条助手消息上设置它。第一个回复回显需要 Agent SDK v0.3.246 或更高版本。当轮回答的消息在轮中间改变时，改变后的第一个回复携带该字段，在 Agent SDK v0.3.265 或更高版本上；早期版本在每轮一个回复帧上设置它。
* **轮的每个 [`thinking_tokens`](#sdkthinkingtokensmessage) 帧**：以便您可以将思考进度归因于您发送的消息，而无需等待轮的第一个回复。需要 Agent SDK v0.3.260 或更高版本。

Claude Code 在这些情况下省略该字段：

* 除了那些第一个回复之外的回复帧
* 子代理帧
* 回答没有消息的轮，或回答您发送的没有 `uuid` 的消息的轮
* 回答您未发送的消息的结果，例如崩溃的工作进程后的零化结果

<h4 id="user_message_uuids">
  `user_message_uuids`
</h4>

Claude Code 在该轮中回答的您发送的每条消息的 `uuid`。当您一起发送多条消息时，Claude Code 可以将它们合并为一轮，`user_message_uuid` 然后仅命名其中的最后一个。要将回复与任何合并的消息匹配，在此列表中的任何位置查找该消息的 `uuid`。需要 Agent SDK v0.3.259 或更高版本。

Claude Code 在携带该字段的每个回复帧和结果上一起设置列表与 `user_message_uuid`。对于携带 `user_message_uuid` 的完整帧集以及每个需要的版本，请参阅 [`user_message_uuid`](#user_message_uuid)。列表始终包含 `user_message_uuid` 并最多包含 64 个条目。

当 Claude Code 在轮运行时拾取您发送的常规消息时，它将该消息的 `uuid` 添加到结果的列表中。

当第一个回复或结果携带 `user_message_uuid` 而没有列表时，它来自早期的 Claude Code 版本，因此回退到单个字段。

<h4 id="resume_reason">
  `resume_reason`
</h4>

Claude Code 重新运行该轮的原因，在重启后。Claude Code 在它在 [`CLAUDE_CODE_RESUME_INTERRUPTED_TURN`](/docs/zh-CN/env-vars) 下重新运行的轮上设置此字段，以便您可以将重新运行的回复和结果与被中断尝试的区分开。需要 Agent SDK v0.3.268 或更高版本。

Claude Code 在两种帧上设置该字段：

* **重新运行的结果**：在成功和错误分支上，无论结果是否携带 `user_message_uuid`。
* **重新运行的回复帧**：那些携带 [`user_message_uuid`](#user_message_uuid) 的帧。

该值是一个短小写令牌，命名轮被重新运行的原因，例如 `interrupted_turn`。该字段在所有其他轮上不存在。

<h4 id="queued_turn_count">
  `queued_turn_count`
</h4>

您发送的带有 [`origin: { kind: "human" }`](#sdkmessageorigin) 的消息数，在 Claude Code 产生结果时仍在命令队列中等待。需要 Agent SDK v0.3.242 或更高版本。

`0` 和缺失字段告诉您什么：

* **`0`**：Claude Code 不计算您发送的没有该 `origin` 的消息，也不计算任务通知，因此轮仍然可以跟随。
* **缺失**：Claude Code 在崩溃或致命启动错误后发出的最终结果省略该字段，并[可能携带零化总计](/docs/zh-CN/agent-sdk/cost-tracking#recover-totals-after-a-session-crash)。

<h4 id="startup_failure_reason">
  `startup_failure_reason`
</h4>

Claude Code 拒绝启动的原因，以便您的应用程序可以提供修复而不是重试。Claude Code 在它在已知启动失败时退出前写入的 `error_during_execution` 结果上设置它。该结果携带零化总计，其 `errors` 数组携带与 stderr 相同的文本。该字段在所有其他结果上不存在。需要 Agent SDK v0.3.274 或更高版本。

在 [`env`](#options) 中设置 `CLAUDE_CODE_STARTUP_FAILURE_RESULTS` 为 `1` 以接收每个 `SDKStartupFailureReason` 值的此结果。没有该变量，Claude Code 仅为这些失败写入结果，其余的以 stderr 输出、非零退出和无结果消息结束：

* Claude Code 停止的恢复，因为它[无法将会话返回到其工作树](/docs/zh-CN/worktrees#the-session-resumes-outside-its-worktree)，带有 `worktree_unverified` 或 `worktree_resume_refused`。该部分说明哪个错误携带哪个值。
* 拒绝后台会话持有的对话的 [`continue`](#options)，带有 `session_held_by_background`。对于这样的对话的拒绝 [`resume`](#options)，Claude Code 仅在设置了变量时写入结果。

```typescript theme={null}
type SDKStartupFailureReason =
  | "org_pin_api_key_conflict"
  | "provider_not_allowed"
  | "org_verify_failed"
  | "org_pin_mismatch"
  | "managed_settings_invalid"
  | "remote_settings_required_unavailable"
  | "gateway_signin_required"
  | "gateway_access_denied"
  | "proxy_invalid"
  | "temp_dir_unusable"
  | "cwd_unavailable"
  | "shell_tool_missing"
  | "session_held_by_background"
  | "worktree_resume_refused"
  | "worktree_unverified"
  | "cli_version_too_old"
  | "bypass_root";
```

每个值命名一个拒绝：

| 值 | 停止会话的原因 |
| :- | :- |
| `org_pin_api_key_conflict` | 托管设置[需要第一方或 Cloud 网关登录](/docs/zh-CN/authentication#restrict-login-to-your-organization)，并配置了 Anthropic API 密钥、身份验证令牌或 `apiKeyHelper` |
| `provider_not_allowed` | 托管设置[列出此机器可能使用的 API 提供商](/docs/zh-CN/settings-reference#allowedproviders)，会话设置为不在列表中的提供商，或设置未固定的端点。需要 Claude Code v2.1.285 或更高版本 |
| `org_verify_failed` | 登录的组织无法针对 pin 进行验证，例如由于网络故障或已撤销的令牌 |
| `org_pin_mismatch` | 登录属于 pin 不允许的组织 |
| `managed_settings_invalid` | 无法读取托管策略设置，pin 未命名任何组织，或[托管模型限制](/docs/zh-CN/errors#managed-settings-block-the-default-model)为默认选项留下没有允许的模型 |
| `remote_settings_required_unavailable` | 组织需要的托管设置无法加载 |
| `gateway_signin_required` | [Cloud 网关](/docs/zh-CN/claude-apps-gateway)结束了此登录 |
| `gateway_access_denied` | 对 Cloud 网关的托管设置请求返回 403，网关的[故障排除表](/docs/zh-CN/claude-apps-gateway-deploy#troubleshooting)涵盖了这一点 |
| `proxy_invalid` | 代理设置不是完整的 URL |
| `temp_dir_unusable` | 每用户临时目录不安全或无法创建 |
| `cwd_unavailable` | 工作目录被删除、移动或无法读取 |
| `shell_tool_missing` | 在 Windows 上，没有可用的 shell 工具：Git Bash 缺失，PowerShell 缺失或使用 `CLAUDE_CODE_USE_POWERSHELL_TOOL` 关闭 |
| `session_held_by_background` | 要恢复或继续的对话作为[后台会话](/docs/zh-CN/agent-view)运行 |
| `worktree_resume_refused` | 会话的工作树未通过其安全检查，或恢复是从其内部启动的。`errors` 说明运行相同恢复是否继续而不使用工作树 |
| `worktree_unverified` | 会话的工作树现在无法验证，重试可能成功 |
| `cli_version_too_old` | 此 Claude Code 版本低于 Anthropic 需要的最低版本 |
| `bypass_root` | 在以 root 身份运行时请求了绕过权限模式 |

<h3 id="sdksystemmessage">
  `SDKSystemMessage`
</h3>

系统初始化消息。

```typescript theme={null}
type SDKSystemMessage = {
  type: "system";
  subtype: "init";
  uuid: UUID;
  session_id: string;
  agents?: string[];
  apiKeySource: ApiKeySource;
  betas?: string[];
  claude_code_version: string;
  cwd: string;
  tools: string[];
  mcp_servers: {
    name: string;
    status: string;
    source?: string;
  }[];
  model: string;
  permissionMode: PermissionMode;
  slash_commands: string[];
  terminal_slash_commands?: string[];
  output_style: string;
  skills: string[];
  plugins: { name: string; path: string }[];
  plugin_errors?: {
    plugin: string;
    type: string;
    message: string;
    path?: string;
  }[];
  fast_mode_state?: FastModeState;
  fast_mode_disabled_reason?: FastModeDisabledReason;
  effort?: "low" | "medium" | "high" | "xhigh" | "max" | null;
  capabilities?: string[];
};
```

`fast_mode_state` 报告会话的[快速模式](/docs/zh-CN/fast-mode)状态。当某些东西阻止快速模式时，`fast_mode_disabled_reason` 命名阻止它的检查；该字段需要 Claude Code v2.1.219 或更高版本。对于原因代码及其含义，请参阅结果消息上的 [`fast_mode_disabled_reason`](#sdkresultmessage)。

`terminal_slash_commands` 命名 `slash_commands` 中的条目，其接口绑定到本地终端，例如 `exit`。您可以像 `slash_commands` 中的任何其他条目一样发送它们；该字段存在以便远程或移动客户端可以从其命令菜单中隐藏它们。该字段仅在非空时存在，需要 Agent SDK v0.3.229 或更高版本。

* `source` 在每个 `mcp_servers` 条目上：服务器定义的来源，与 [`McpServerStatus`](#mcpserverstatus) 的 `source` 值相同。需要 Agent SDK v0.3.274 或更高版本。
* `effort`：[努力级别](/docs/zh-CN/model-config#adjust-effort-level) Claude Code 在会话的下一个请求上发送，或当它不发送任何时为 `null`。Claude Code 仅在它发送到[远程控制](/docs/zh-CN/remote-control)客户端的初始化消息上设置该字段，并从您的应用程序读取的初始化消息中省略它。需要 Agent SDK v0.3.234 或更高版本。

`capabilities` 数组命名此 CLI 实现的协议行为，因此您可以进行功能检测而不是比较 `claude_code_version` 字符串。这是一个开放集：忽略您不认识的值，并检查您依赖其行为的特定功能。该字段需要 Claude Code v2.1.205 或更高版本，在早期 CLI 上不存在。

| 功能 | 含义 |
| - | - |
| `interrupt_receipt_v1` | [`interrupt()`](#query-object) 使用 [`SDKControlInterruptResponse`](#sdkcontrolinterruptresponse) 收据解析，列出中断到达时待处理的消息 |
| `interrupt_cancel_queued_v1` | `interrupt` 控制请求尊重 `cancel_queued: true`，取消收据在 `still_queued` 下列出的消息，并改为在 `cancelled` 下列出它们。请参阅 [`SDKControlInterruptResponse`](#sdkcontrolinterruptresponse)。需要 Claude Code v2.1.219 或更高版本 |

`plugin_errors` 数组列出插件加载失败。一个条目描述要么是未加载的插件且在 `plugins` 中不存在，要么是加载但没有其部分之一（例如其 hooks 文件）的插件。当没有任何东西失败时，该键被省略。`SDKSystemMessage` 在 Agent SDK v0.3.283 或更高版本中声明 `plugin_errors`。

当您的 [`plugins` 选项](#options)中的目录或存档本身无法加载时，条目的 `plugin` 字段保存位置标签（例如 `inline[0]`）而不是插件名称。例如，当路径不存在或清单无效时会发生这种情况。通过其 `path` 字段将这样的条目与您的选项匹配。

下表列出了每个 `plugin_errors` 条目的字段。

| 字段 | 类型 | 描述 |
| - | - | - |
| `plugin` | `string` | 失败插件的 ID，或位置标签（例如 `inline[0]`），当插件目录或存档本身无法加载时 |
| `type` | `string` | 来自开放集的错误类别，例如 `path-not-found` 或 `manifest-validation-error`。将您不认识的值视为通用失败 |
| `message` | `string` | 描述失败的显示文本 |
| `path` | `string` | 仅当插件目录或存档本身无法加载时存在。其绝对路径，相对路径从您的 `plugins` 选项针对 [`cwd`](#options) 选项解析 |

<h3 id="sdkpartialassistantmessage">
  `SDKPartialAssistantMessage`
</h3>

流式部分消息（仅当 `includePartialMessages` 为 true 时）。`parent_tool_use_id` 字段始终为 `null`：流事件仅为主会话发出。对于子代理归因，使用完整消息，它们携带 `parent_tool_use_id`，或启用 [`forwardSubagentText`](#options) 以接收子代理文本和思考作为完整消息。

```typescript theme={null}
type SDKPartialAssistantMessage = {
  type: "stream_event";
  event: BetaRawMessageStreamEvent; // From Anthropic SDK
  parent_tool_use_id: string | null;
  uuid: UUID;
  session_id: string;
  ttft_ms?: number; // Time to first token in ms, present only on message_start events
  user_message_uuid?: string;
  user_message_uuids?: string[];
  resume_reason?: string;
};
```

Claude Code 在轮的第一个非 ping 流事件上设置 `user_message_uuid` 和 `user_message_uuids`，并在轮回答的消息改变时再次设置，条件在 [`user_message_uuid`](#user_message_uuid) 中。当 Claude Code 重新运行被重启中断的轮时，重新运行的携带这些字段的流事件也携带 [`resume_reason`](#resume_reason)。

<h3 id="sdkcompactboundarymessage">
  `SDKCompactBoundaryMessage`
</h3>

指示对话压缩边界的消息。

```typescript theme={null}
type SDKCompactBoundaryMessage = {
  type: "system";
  subtype: "compact_boundary";
  uuid: UUID;
  session_id: string;
  compact_metadata: {
    trigger: "manual" | "auto";
    pre_tokens: number;
  };
};
```

<h3 id="sdkinformationalmessage">
  `SDKInformationalMessage`
</h3>

循环发出的通用文本横幅。携带警告、通知和其他非错误状态行 Claude Code 引发，以及钩子反馈，例如 `UserPromptSubmit` 钩子的阻止原因。

在 Claude Code v2.1.227 或更高版本上，钩子的 [`systemMessage`](/docs/zh-CN/hooks#json-output) 可以作为此消息到达，每行以钩子的名称为前缀，例如 `PostToolUse:Bash says:`。每个[事件的部分](/docs/zh-CN/hooks#hook-events)在钩子页面上说明输出如何显示。

将 `content` 呈现为给定 `level` 的纯文本。

```typescript theme={null}
type SDKInformationalMessage = {
  type: "system";
  subtype: "informational";
  content: string;
  level: "info" | "notice" | "suggestion" | "warning";
  tool_use_id?: string;
  prevent_continuation?: boolean;
  uuid: UUID;
  session_id: string;
};
```

<h3 id="sdkworkershuttingdownmessage">
  `SDKWorkerShuttingDownMessage`
</h3>

在优雅的工作进程拆卸上发出，以便远程客户端可以显示工作进程退出的原因，而不是等待心跳超时。`reason` 是由主机 CLI 设置的短 snake\_case 字符串，例如 `"host_exit"` 或 `"remote_control_disabled"`。仅在流式传输实时时对此采取行动。恢复的会话重放此消息的过去实例，因此在这种情况下忽略它们。

```typescript theme={null}
type SDKWorkerShuttingDownMessage = {
  type: "system";
  subtype: "worker_shutting_down";
  reason: string;
  uuid: UUID;
  session_id: string;
};
```

<h3 id="sdkplugininstallmessage">
  `SDKPluginInstallMessage`
</h3>

插件安装进度事件。在设置 [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/docs/zh-CN/env-vars) 时发出，以便您的 Agent SDK 应用程序可以在第一轮之前跟踪市场插件安装。`started` 和 `completed` 状态括住整体安装。`installed` 和 `failed` 状态报告单个市场并包含 `name`。

```typescript theme={null}
type SDKPluginInstallMessage = {
  type: "system";
  subtype: "plugin_install";
  status: "started" | "installed" | "failed" | "completed";
  name?: string;
  error?: string;
  uuid: UUID;
  session_id: string;
};
```

<h3 id="sdkpermissiondeniedmessage">
  `SDKPermissionDeniedMessage`
</h3>

当权限系统在没有交互式提示的情况下拒绝工具调用时发出的流事件。使用它在您的 UI 中实时呈现拒绝，而不是仅观察随后的 `is_error` 工具结果。它报告的拒绝取决于运行如何处理权限提示：

* **使用 [`canUseTool`](#canusetool) 回调**和默认 [`permissionPrompts: 'host'`](#options)：权限提示转到您的回调，此事件报告 Claude Code 自己决定的拒绝，而不调用它。
* **都没有**：裸 `-p` 运行，或 `query()` 既不设置 `canUseTool` 也不设置 `permissionPromptToolName`，拒绝任何会提示的工具调用，此事件也报告这些拒绝以及 Claude Code 自己决定的拒绝。在 v2.1.223 之前，Claude Code 在没有回调的运行中不发出此事件。
* **使用 MCP 提示工具**，使用 `permissionPromptToolName` 或 [`--permission-prompt-tool`](/docs/zh-CN/cli-reference#cli-flags) 标志设置，和默认 `permissionPrompts: 'host'`：Claude Code 根本不发出此事件，甚至不发出它自己决定的规则拒绝。
* **使用 [`permissionPrompts: 'none'`](#options)**：Claude Code 拒绝会提示的调用，即使也设置了 `canUseTool` 或 MCP 提示工具，此事件也报告这些拒绝以及 Claude Code 自己决定的拒绝。需要 Claude Code v2.1.259 或更高版本。

在每个配置中，此事件跳过在 `PreToolUse` 钩子路径上决定的任何拒绝，无论钩子本身拒绝了调用还是拒绝规则覆盖了钩子的允许或询问决定。该事件也是尽力而为的：偶尔 Claude Code 记录拒绝而不发出此事件，因此[结果消息](#sdkresultmessage)上的 `permission_denials` 是权威记录。

```typescript theme={null}
type SDKPermissionDeniedMessage = {
  type: "system";
  subtype: "permission_denied";
  tool_name: string;
  tool_use_id: string;
  agent_id?: string;
  decision_reason_type?: string;
  decision_reason?: string;
  message: string;
  uuid: UUID;
  session_id: string;
};
```

| 字段 | 类型 | 描述 |
| - | - | - |
| `tool_name` | `string` | 被拒绝的工具的名称 |
| `tool_use_id` | `string` | 此拒绝回答的 `tool_use` 块的 ID |
| `agent_id` | `string` | 当拒绝的调用源自子代理内部时的子代理 ID。镜像主机端路由的 `can_use_tool` 上的字段 |
| `decision_reason_type` | `string` | 决定组件的鉴别器，例如 `"rule"`、`"mode"`、`"classifier"` 或 `"asyncAgent"` |
| `decision_reason` | `string` | 来自决定组件的人类可读原因，当可用时 |
| `message` | `string` | 在 `tool_result` 中返回给模型的拒绝消息 |

<h3 id="sdkpermissiondenial">
  `SDKPermissionDenial`
</h3>

关于被拒绝的工具使用的信息。

```typescript theme={null}
type SDKPermissionDenial = {
  tool_name: string;
  tool_use_id: string;
  tool_input: Record<string, unknown>;
};
```

<h3 id="sdkcontextusage">
  `SDKContextUsage`
</h3>

`/context` 报告的结构化形式，作为 `context_usage` 在传递 `/context` 结果的 [`SDKAssistantMessage`](#sdkassistantmessage) 上携带。Agent SDK v0.3.232 及更高版本导出该类型。与 [`SDKControlGetContextUsageResponse`](#sdkcontrolgetcontextusageresponse) 不同，它仅携带呈现使用情况分解所需的数据，不包含 `color` 和 `gridRows` 等显示字段。

```typescript theme={null}
type SDKContextUsage = {
  model: string;
  total_tokens: number;
  raw_max_tokens: number;
  percentage: number;
  over_limit?: {
    tokens_over: number;
    kind: "hard_limit" | "compaction_window";
  };
  categories: SDKContextUsageCategory[];
  mcp_tools: {
    name: string;
    server_name: string;
    tokens: number;
  }[];
  memory_files: {
    path: string;
    type: string;
    tokens: number;
  }[];
  agents: {
    agent_type: string;
    source: string;
    tokens: number;
  }[];
  skills?: {
    name: string;
    source: string;
    plugin_name?: string;
    tokens: number;
  }[];
};
```

该表列出了 Claude Code 在每个字段中放入的内容。从 `model` 到 `over_limit` 的字段描述整个会话，集合字段将令牌归因于单个项目。

| 字段 | 类型 | 描述 |
| - | - | - |
| `model` | `string` | Claude Code 计算使用情况的主循环的模型，不是子代理的 |
| `total_tokens` | `number` | Claude Code 对使用中令牌的估计。未限制在窗口，因此当会话超过限制时可以超过 `raw_max_tokens` |
| `raw_max_tokens` | `number` | 模型的上下文窗口，或较低的[自动压缩窗口](/docs/zh-CN/model-config#context-window-and-auto-compaction)（当适用时），例如您设置的或 Claude Code 应用于某些具有 1M 令牌窗口的模型的 200K 边界。Claude Code 针对此窗口测量 `total_tokens` |
| `percentage` | `number` | `total_tokens` 作为 `raw_max_tokens` 的四舍五入百分比，因此当会话超过限制时可以超过 100 |
| `over_limit` | `object` | 仅当 `total_tokens` 超过 `raw_max_tokens` 时存在。`tokens_over` 是超过的数量，`kind` 说明 Claude Code 如何解决窗口 |
| `categories` | [`SDKContextUsageCategory`](#sdkcontextusagecategory)`[]` | 使用情况按类别分解的每一行一个条目 |
| `mcp_tools` | `object[]` | 归因于每个 MCP 工具的令牌，带有其线路名称（例如 `mcp__linear__create_issue`）和其 `server_name` |
| `memory_files` | `object[]` | 归因于每个加载的内存文件的令牌，带有其 `path` 和源标签（例如 `Project` 或 `User`）在 `type` 中 |
| `agents` | `object[]` | 归因于每个自定义子代理定义的令牌，带有源标识符，例如 `projectSettings`、`userSettings` 或 `plugin`。内置子代理未列出 |
| `skills` | `object[]` | 归因于技能列表中每个技能的令牌，带有源标识符，对于插件技能，插件的名称在 `plugin_name` 中。当没有技能贡献令牌时不存在 |

`over_limit.kind` 记录 Claude Code 如何解决窗口，而不是 API 是否接受下一个请求：

* `hard_limit`：窗口是 Claude Code 认为是模型自己的限制，超过该限制 API 拒绝请求
* `compaction_window`：窗口是压缩策略窗口，可能与模型的限制一致，也可能不一致

Claude Code 以加法方式演进该类型，添加新数据作为可选字段而不是重塑现有字段。读取您知道的字段并忽略您不认识的任何字段。

<h3 id="sdkcontextusagecategory">
  `SDKContextUsageCategory`
</h3>

`/context` 使用情况按类别分解的一行。

```typescript theme={null}
type SDKContextUsageCategory = {
  name: string;
  tokens: number;
  kind: "used" | "free" | "buffer" | "deferred";
};
```

该表列出了 Claude Code 在行的每个字段中放入的内容。

| 字段 | 类型 | 描述 |
| - | - | - |
| `name` | `string` | 行的显示名称，如 `/context` 打印的那样，例如 `Messages`。按 `kind` 分类行，而不是按名称 |
| `tokens` | `number` | 行的令牌计数。行可以携带零令牌 |
| `kind` | `string` | 行代表什么：`used`、`free`、`buffer` 或 `deferred` |

每个 `kind` 值说明行的令牌是什么：

* `used`：占据上下文窗口的内容
* `free`：剩余窗口
* `buffer`：压缩保留
* `deferred`：Claude Code 保留在窗口外的工具模式，从使用情况计算中排除，列出以供了解

<h3 id="sdkmessageorigin">
  `SDKMessageOrigin`
</h3>

用户角色消息的来源。这在 [`SDKUserMessage`](#sdkusermessage) 上显示为 `origin`，并转发到相应的 [`SDKResultMessage`](#sdkresultmessage)，以便您可以告诉什么触发了给定的轮。

```typescript theme={null}
type SDKMessageOrigin =
  | { kind: "human" }
  | { kind: "channel"; server: string }
  | {
      kind: "peer";
      from: string;
      fromMode?: "bypass" | "prompting";
      name?: string;
      fromSession?: string;
      senderTaskId?: string;
      body?: string;
      verifiedPeerPid?: number;
    }
  | {
      kind: "task-notification";
      subkind?: "scheduled-trigger" | "peer-send-message";
      fireReason?: string;
    }
  | { kind: "coordinator" }
  | { kind: "auto-continuation" }
  | { kind: "unclassified" };
```

| `kind` | 含义 |
| - | - |
| `human` | 来自最终用户的直接输入。如果您的应用程序将用户输入的内容转发为用户消息，显式将其 `origin` 设置为 `{ kind: "human" }`：Claude Code 将没有 `origin` 的用户消息视为未归因，并检查需要人类输入的提示（例如 [`ultracode` 工作流关键字](/docs/zh-CN/workflows#ask-for-a-workflow-in-your-prompt)）不接受它。在 v2.1.210 之前，Claude Code 将用户消息上缺失的 `origin` 视为人类输入。 |
| `channel` | 在[频道](/docs/zh-CN/channels)上到达的消息。`server` 是源 MCP 服务器名称。 |
| `peer` | 来自另一个代理的消息：进程内[队友](/docs/zh-CN/agent-teams)或[跨会话对等体](/docs/zh-CN/cross-session-messaging)，您的另一个 Claude Code 会话。请参阅[对等体来源字段](#peer-origin-fields)了解每个字段的语义和信任模型。 |
| `task-notification` | 为没有新鲜用户提示的传递注入的合成轮，例如完成的后台任务；请参阅 [`SDKTaskNotificationMessage`](#sdktasknotificationmessage) 了解该分支。您的应用程序[声明为计划运行](#declare-a-scheduled-run)的提示也携带此类型。可选的 `subkind` 标记引发通知的原因。请参阅[任务通知子类型](#task-notification-subkinds)。 |
| `coordinator` | 来自[代理团队](/docs/zh-CN/agent-teams)中的团队协调员的消息。 |
| `auto-continuation` | 当会话在没有新鲜用户输入的情况下继续时注入的合成轮，例如触发后续提示的命令结果。 |
| `unclassified` | 无法确定来源的注入轮。当 Claude Code 接收带有 `isSynthetic: true` 的 [`SDKUserMessage`](#sdkusermessage) 并无法将其分类为任何其他 `kind` 时，它在消息到达时设置此类型，并将轮框架化为非用户源而不是将其视为人类输入。您的应用程序不应设置此值。 |

<h3 id="task-notification-subkinds">
  任务通知子类型
</h3>

当 Claude Code 将任务通知传递到会话中时，如果 Anthropic 服务器验证了该通知的来源，它会在通知的 `origin` 上设置 `subkind`。当您的应用程序[自己声明消息为计划运行](#declare-a-scheduled-run)时，它也设置 `subkind`，这需要 TypeScript Agent SDK v0.3.280 或更高版本。`subkind` 需要 Claude Code v2.1.213 或更高版本，它采用两个值之一：

* `scheduled-trigger`：通知是[例程](/docs/zh-CN/routines)的存储提示，因为例程的触发器之一触发而传递：其计划、其 [API 触发器](/docs/zh-CN/routines#add-an-api-trigger)、其 [GitHub 触发器](/docs/zh-CN/routines#add-a-github-trigger) 或**立即运行**。您的应用程序[声明为计划运行](#declare-a-scheduled-run)的提示也携带此值。Claude Code 将这些框架化为会话的分配任务，与[其他任务通知携带的通知](#sdktasknotificationmessage)不同。
* `peer-send-message`：通知是另一个您的会话使用[云会话](/docs/zh-CN/claude-code-on-the-web)使用的服务器端 `send_message` 工具发送的消息，而不是[跨会话 `SendMessage` 工具](/docs/zh-CN/cross-session-messaging)，并且 Anthropic 服务器验证了两个会话都属于同一私有会话组。需要 Claude Code v2.1.224 或更高版本。服务器未以这种方式验证的 `send_message` 传递没有 `subkind`。

每个其他任务通知都没有 `subkind`。这包括[PR 活动](/docs/zh-CN/claude-code-on-the-web#how-claude-responds-to-pr-activity)传递到会话和后台事件，例如完成的任务。来自[跨会话 `SendMessage` 工具](/docs/zh-CN/cross-session-messaging)的消息根本不是任务通知：无论它们来自同一机器上的会话还是通过 Anthropic 服务器来自另一台机器，Claude Code 都给它们 `kind: "peer"` 和[对等体来源字段](#peer-origin-fields)。

`fireReason` 说明 `scheduled-trigger` 通知为什么触发，作为短小写令牌，例如 `scheduled`、`manual`、`retry`、`catch_up` 或 `api`。Anthropic 服务器在[例程](/docs/zh-CN/routines)的传递上设置它，您的应用程序在声明计划运行时设置它。当两者都未发送时不存在。需要 TypeScript Agent SDK v0.3.280 或更高版本。

<h4 id="declare-a-scheduled-run">
  声明计划运行
</h4>

如果您的应用程序按自己的计划运行提示，声明每个运行，以便 Claude Code 将轮框架化为计划任务而不是来自用户的实时输入。使用 [`env`](#options) 中设置为 `1` 的 `CLAUDE_CODE_HOST_SCHEDULED_RUN` 启动会话，然后发送运行的 [`SDKUserMessage`](#sdkusermessage)，其中 `origin: { kind: "task-notification", subkind: "scheduled-trigger", fireReason: "scheduled" }` 且没有 `isSynthetic`。Claude Code 忽略在没有该变量启动的进程中的声明。它也在进程的环境携带 [`CLAUDECODE`](/docs/zh-CN/env-vars) 或 `CLAUDE_CODE_CHILD_SESSION` 时忽略它。Claude Code 仅在值为 1 到 32 个小写字母或下划线时保留 `fireReason`。需要 TypeScript Agent SDK v0.3.280 或更高版本。

<h3 id="peer-origin-fields">
  对等体来源字段
</h3>

`peer` 来源标识哪个代理发送了消息：进程内[队友](/docs/zh-CN/agent-teams)使用 `SendMessage` 发送到 `main`，或[跨会话对等体](/docs/zh-CN/cross-session-messaging)，您的另一个 Claude Code 会话。跨会话对等体在 macOS 和 Linux 上需要 Claude Code v2.1.224 或更高版本；请参阅[跨会话消息传递可用性](/docs/zh-CN/cross-session-messaging#availability)了解本机 Windows 要求。跨会话对等体可以在同一机器上运行，或在[您的另一台机器](/docs/zh-CN/cross-session-messaging#message-sessions-on-other-machines)或[云中](/docs/zh-CN/claude-code-on-the-web)运行，当其消息通过远程控制到达时。两种发送者类型填充字段的方式不同：

* `from`：队友的名称，或跨会话对等体的发送者地址。对于[单向跨机器消息](/docs/zh-CN/cross-session-messaging#message-sessions-on-other-machines)，发送者没有回复地址，`from` 是 `"unknown"`。该值由发送者创作；`verifiedPeerPid` 是验证的身份。
* `fromMode`：发送会话的权限类，`bypass` 或 `prompting`，由在您的会话之间中继对等消息的主机声明，例如[桌面应用](/docs/zh-CN/desktop#work-across-sessions)。Claude Code 在接收会话中应用[入站控制](/docs/zh-CN/cross-session-messaging#control-inbound-messages)时读取它。需要 Agent SDK v0.3.234 或更高版本。
* `senderTaskId`：队友的任务 ID。对于跨会话对等体不存在。
* `name`：发送者的显示名称，由 Claude Code 规范化：它删除 Unicode 控制、格式、代理和行或段落分隔符代码点，然后修剪结果并将其限制为 64 个代码点，带有省略号。需要 Claude Code v2.1.205 或更高版本。
* `body`：解码的消息体，去除对等体信封，字节精确匹配模型看到的内容。始终存在于队友消息；对于跨会话对等体，仅当轮恰好是由 Claude Code 形成的一个对等体信封时存在。呈现 `name` 和 `body` 而不是重新解析消息文本。需要 Claude Code v2.1.205 或更高版本。
* `fromSession`：发送者的主机可打开会话 ID，由发送者的主机设置，以便您的 UI 可以链接回发送会话。像 `from` 一样，它是发送者声称的：仅将其用作导航目标，不要将其视为发送者身份的证明。需要 Claude Code v2.1.216 或更高版本。
* `verifiedPeerPid`：连接到此会话的跨会话消息传递套接字的进程的进程 ID，由内核验证并从连接本身读取，从不从有效负载读取。使用它，而不是 `from`，来标识发送者：`from` 可由任何同用户进程伪造。当 Claude Code 无法验证它时，该字段不存在，例如在 Windows 或非套接字入口上，因此缺失值意味着发送者未验证。对于中继流量，它标识中继而不是消息的作者，进程 ID 是可回收的，因此将其视为来源而不是身份验证令牌。需要 Claude Code v2.1.216 或更高版本。

<h2 id="hook-types">
  Hook 类型
</h2>

有关使用 hooks 的综合指南，包括示例和常见模式，请参阅 [Hooks 指南](/docs/zh-CN/agent-sdk/hooks)。

<h3 id="hookevent">
  `HookEvent`
</h3>

可用的 hook 事件。

```typescript theme={null}
type HookEvent =
  | "PreToolUse"
  | "PostToolUse"
  | "PostToolUseFailure"
  | "PostToolBatch"
  | "Notification"
  | "UserPromptSubmit"
  | "UserPromptExpansion"
  | "SessionStart"
  | "SessionEnd"
  | "Stop"
  | "StopFailure"
  | "SubagentStart"
  | "SubagentStop"
  | "PreCompact"
  | "PostCompact"
  | "PreModelSwitch"
  | "PostModelSwitch"
  | "PermissionRequest"
  | "PermissionDenied"
  | "Setup"
  | "TeammateIdle"
  | "TaskCreated"
  | "TaskCompleted"
  | "Elicitation"
  | "ElicitationResult"
  | "ConfigChange"
  | "DirectoryAdded"
  | "WorktreeCreate"
  | "WorktreeRemove"
  | "InstructionsLoaded"
  | "CwdChanged"
  | "FileChanged"
  | "MessageDisplay";
```

<h3 id="hookcallback">
  `HookCallback`
</h3>

Hook 回调函数类型。

```typescript theme={null}
type HookCallback = (
  input: HookInput, // 所有 hook 输入类型的联合
  toolUseID: string | undefined,
  options: { signal: AbortSignal }
) => Promise<HookJSONOutput>;
```

<h3 id="hookcallbackmatcher">
  `HookCallbackMatcher`
</h3>

带有可选匹配器的 Hook 配置。

```typescript theme={null}
interface HookCallbackMatcher {
  matcher?: string;
  hooks: HookCallback[];
  timeout?: number; // 此匹配器中所有 hooks 的超时时间（秒）
}
```

<h3 id="hookinput">
  `HookInput`
</h3>

所有 hook 输入类型的联合类型。

```typescript theme={null}
type HookInput =
  | PreToolUseHookInput
  | PostToolUseHookInput
  | PostToolUseFailureHookInput
  | PostToolBatchHookInput
  | PermissionDeniedHookInput
  | NotificationHookInput
  | UserPromptSubmitHookInput
  | UserPromptExpansionHookInput
  | SessionStartHookInput
  | SessionEndHookInput
  | StopHookInput
  | StopFailureHookInput
  | SubagentStartHookInput
  | SubagentStopHookInput
  | PreCompactHookInput
  | PostCompactHookInput
  | PreModelSwitchHookInput
  | PostModelSwitchHookInput
  | PermissionRequestHookInput
  | SetupHookInput
  | TeammateIdleHookInput
  | TaskCreatedHookInput
  | TaskCompletedHookInput
  | ElicitationHookInput
  | ElicitationResultHookInput
  | ConfigChangeHookInput
  | InstructionsLoadedHookInput
  | DirectoryAddedHookInput
  | WorktreeCreateHookInput
  | WorktreeRemoveHookInput
  | CwdChangedHookInput
  | FileChangedHookInput
  | MessageDisplayHookInput;
```

<h3 id="basehookinput">
  `BaseHookInput`
</h3>

所有 hook 输入类型扩展的基本接口。

```typescript theme={null}
type BaseHookInput = {
  session_id: string;
  transcript_path: string;
  cwd: string;
  prompt_id?: string;
  permission_mode?: string;
  effort?: { level: string };
  agent_id?: string;
  agent_type?: string;
};
```

`prompt_id` 字段是一个 UUID，用于标识当前正在处理的用户提示。它与 [OpenTelemetry 事件上的 `prompt.id` 属性](/docs/zh-CN/monitoring-usage#event-correlation-attributes)匹配，在第一个用户输入之前不存在。需要 Claude Code v2.1.196 或更高版本。

<h4 id="pretoolusehookinput">
  `PreToolUseHookInput`
</h4>

```typescript theme={null}
type PreToolUseHookInput = BaseHookInput & {
  hook_event_name: "PreToolUse";
  tool_name: string;
  tool_input: unknown;
  tool_use_id: string;
  mcp_server?: McpServerProvenance;
};
```

当工具来自 MCP 服务器时，`mcp_server` 存在；请参阅 [`McpServerProvenance`](#mcpserverprovenance)。`PostToolUse`、`PostToolUseFailure`、`PermissionRequest` 和 `PermissionDenied` 输入携带相同的字段。该字段需要 Agent SDK v0.3.274 或更高版本。

<h4 id="posttoolusehookinput">
  `PostToolUseHookInput`
</h4>

```typescript theme={null}
type PostToolUseHookInput = BaseHookInput & {
  hook_event_name: "PostToolUse";
  tool_name: string;
  tool_input: unknown;
  tool_response: unknown;
  tool_use_id: string;
  duration_ms?: number;
  mcp_server?: McpServerProvenance;
};
```

<h4 id="posttoolusefailurehookinput">
  `PostToolUseFailureHookInput`
</h4>

```typescript theme={null}
type PostToolUseFailureHookInput = BaseHookInput & {
  hook_event_name: "PostToolUseFailure";
  tool_name: string;
  tool_input: unknown;
  tool_use_id: string;
  error: string;
  is_interrupt?: boolean;
  duration_ms?: number;
  mcp_server?: McpServerProvenance;
};
```

<h4 id="posttoolbatchhookinput">
  `PostToolBatchHookInput`
</h4>

在批处理中的每个工具调用都已解决后触发一次，在下一个模型请求之前。`tool_response` 携带序列化的 `tool_result` 内容，模型会看到该内容；其形状与 `PostToolUseHookInput` 的结构化 `Output` 对象不同。

```typescript theme={null}
type PostToolBatchHookInput = BaseHookInput & {
  hook_event_name: "PostToolBatch";
  tool_calls: PostToolBatchToolCall[];
};

type PostToolBatchToolCall = {
  tool_name: string;
  tool_input: unknown;
  tool_use_id: string;
  tool_response?: unknown;
};
```

<h4 id="permissiondeniedhookinput">
  `PermissionDeniedHookInput`
</h4>

```typescript theme={null}
type PermissionDeniedHookInput = BaseHookInput & {
  hook_event_name: "PermissionDenied";
  tool_name: string;
  tool_input: unknown;
  tool_use_id: string;
  reason: string;
  mcp_server?: McpServerProvenance;
};
```

<h4 id="notificationhookinput">
  `NotificationHookInput`
</h4>

```typescript theme={null}
type NotificationHookInput = BaseHookInput & {
  hook_event_name: "Notification";
  message: string;
  title?: string;
  notification_type: string;
};
```

<h4 id="userpromptsubmithookinput">
  `UserPromptSubmitHookInput`
</h4>

```typescript theme={null}
type UserPromptSubmitHookInput = BaseHookInput & {
  hook_event_name: "UserPromptSubmit";
  prompt: string;
  session_title?: string;
};
```

<h4 id="userpromptexpansionhookinput">
  `UserPromptExpansionHookInput`
</h4>

```typescript theme={null}
type UserPromptExpansionHookInput = BaseHookInput & {
  hook_event_name: "UserPromptExpansion";
  expansion_type: "slash_command" | "mcp_prompt";
  command_name: string;
  command_args: string;
  command_source?: string;
  prompt: string;
};
```

<h4 id="sessionstarthookinput">
  `SessionStartHookInput`
</h4>

```typescript theme={null}
type SessionStartHookInput = BaseHookInput & {
  hook_event_name: "SessionStart";
  source: "startup" | "resume" | "clear" | "compact" | "fork";
  agent_type?: string;
  model?: string;
  session_title?: string;
};
```

<h4 id="sessionendhookinput">
  `SessionEndHookInput`
</h4>

```typescript theme={null}
type SessionEndHookInput = BaseHookInput & {
  hook_event_name: "SessionEnd";
  reason: ExitReason; // EXIT_REASONS 数组中的字符串
};
```

<h4 id="stophookinput">
  `StopHookInput`
</h4>

```typescript theme={null}
type StopHookInput = BaseHookInput & {
  hook_event_name: "Stop";
  stop_hook_active: boolean;
  last_assistant_message?: string;
  background_tasks?: BackgroundTaskSummary[];
  session_crons?: SessionCronSummary[];
};
```

<h4 id="stopfailurehookinput">
  `StopFailureHookInput`
</h4>

```typescript theme={null}
type StopFailureHookInput = BaseHookInput & {
  hook_event_name: "StopFailure";
  error: SDKAssistantMessageError;
  error_details?: string;
  last_assistant_message?: string;
};
```

<h4 id="subagentstarthookinput">
  `SubagentStartHookInput`
</h4>

```typescript theme={null}
type SubagentStartHookInput = BaseHookInput & {
  hook_event_name: "SubagentStart";
  agent_id: string;
  agent_type: string;
};
```

<h4 id="subagentstophookinput">
  `SubagentStopHookInput`
</h4>

```typescript theme={null}
type SubagentStopHookInput = BaseHookInput & {
  hook_event_name: "SubagentStop";
  stop_hook_active: boolean;
  agent_id: string;
  agent_transcript_path: string;
  agent_type: string;
  last_assistant_message?: string;
  background_tasks?: BackgroundTaskSummary[];
  session_crons?: SessionCronSummary[];
};

type BackgroundTaskSummary = {
  id: string;
  type: string;
  status: string;
  description: string;
  command?: string;
  agent_type?: string;
  server?: string;
  tool?: string;
  name?: string;
};

type SessionCronSummary = {
  id: string;
  schedule: string;
  recurring: boolean;
  prompt: string;
};
```

<h4 id="precompacthookinput">
  `PreCompactHookInput`
</h4>

```typescript theme={null}
type PreCompactHookInput = BaseHookInput & {
  hook_event_name: "PreCompact";
  trigger: "manual" | "auto";
  custom_instructions: string | null;
};
```

<h4 id="postcompacthookinput">
  `PostCompactHookInput`
</h4>

```typescript theme={null}
type PostCompactHookInput = BaseHookInput & {
  hook_event_name: "PostCompact";
  trigger: "manual" | "auto";
  compact_summary: string;
};
```

<h4 id="premodelswitchhookinput">
  `PreModelSwitchHookInput`
</h4>

在请求的模型切换生效之前触发。`context_tokens` 和之后的字段估计向新模型重新发送对话的成本。有关完整的字段描述和阻止语义，请参阅 [PreModelSwitch](/docs/zh-CN/hooks#premodelswitch)。

```typescript theme={null}
type PreModelSwitchHookInput = BaseHookInput & {
  hook_event_name: "PreModelSwitch";
  from_model: string;
  to_model: string;
  requested_model: string | null;
  source: "command" | "picker" | "sdk";
  context_tokens: number;
  prompt_cache_warm: boolean;
  cache_ttl: "5m" | "1h";
  estimated_cache_write_usd: number;
  pricing: "configured" | "catalog" | "default";
};
```

<h4 id="postmodelswitchhookinput">
  `PostModelSwitchHookInput`
</h4>

在会话的模型更改后触发。它携带与 `PreModelSwitchHookInput` 相同的字段，另外还有两个 `source` 值。请参阅 [PostModelSwitch](/docs/zh-CN/hooks#postmodelswitch)。

```typescript theme={null}
type PostModelSwitchHookInput = BaseHookInput & {
  hook_event_name: "PostModelSwitch";
  from_model: string;
  to_model: string;
  requested_model: string | null;
  source: "command" | "picker" | "sdk" | "auto" | "resume";
  context_tokens: number;
  prompt_cache_warm: boolean;
  cache_ttl: "5m" | "1h";
  estimated_cache_write_usd: number;
  pricing: "configured" | "catalog" | "default";
};
```

<h4 id="permissionrequesthookinput">
  `PermissionRequestHookInput`
</h4>

```typescript theme={null}
type PermissionRequestHookInput = BaseHookInput & {
  hook_event_name: "PermissionRequest";
  tool_name: string;
  tool_input: unknown;
  permission_suggestions?: PermissionUpdate[];
  mcp_server?: McpServerProvenance;
};
```

<h4 id="setuphookinput">
  `SetupHookInput`
</h4>

```typescript theme={null}
type SetupHookInput = BaseHookInput & {
  hook_event_name: "Setup";
  trigger: "init" | "maintenance";
};
```

<h4 id="teammateidlehookinput">
  `TeammateIdleHookInput`
</h4>

```typescript theme={null}
type TeammateIdleHookInput = BaseHookInput & {
  hook_event_name: "TeammateIdle";
  teammate_name: string;
  /** @deprecated 自 v2.1.178 起已弃用。携带会话派生的团队名称；将被移除。 */
  team_name: string;
};
```

<h4 id="taskcreatedhookinput">
  `TaskCreatedHookInput`
</h4>

```typescript theme={null}
type TaskCreatedHookInput = BaseHookInput & {
  hook_event_name: "TaskCreated";
  task_id: string;
  task_subject: string;
  task_description?: string;
  teammate_name?: string;
  /** @deprecated 自 v2.1.178 起已弃用。携带会话派生的团队名称；将被移除。 */
  team_name?: string;
};
```

<h4 id="taskcompletedhookinput">
  `TaskCompletedHookInput`
</h4>

```typescript theme={null}
type TaskCompletedHookInput = BaseHookInput & {
  hook_event_name: "TaskCompleted";
  task_id: string;
  task_subject: string;
  task_description?: string;
  teammate_name?: string;
  /** @deprecated 自 v2.1.178 起已弃用。携带会话派生的团队名称；将被移除。 */
  team_name?: string;
};
```

<h4 id="elicitationhookinput">
  `ElicitationHookInput`
</h4>

```typescript theme={null}
type ElicitationHookInput = BaseHookInput & {
  hook_event_name: "Elicitation";
  mcp_server_name: string;
  message: string;
  mode?: "form" | "url";
  url?: string;
  elicitation_id?: string;
  requested_schema?: Record<string, unknown>;
};
```

<h4 id="elicitationresulthookinput">
  `ElicitationResultHookInput`
</h4>

```typescript theme={null}
type ElicitationResultHookInput = BaseHookInput & {
  hook_event_name: "ElicitationResult";
  mcp_server_name: string;
  elicitation_id?: string;
  mode?: "form" | "url";
  action: "accept" | "decline" | "cancel";
  content?: Record<string, unknown>;
};
```

<h4 id="configchangehookinput">
  `ConfigChangeHookInput`
</h4>

```typescript theme={null}
type ConfigChangeHookInput = BaseHookInput & {
  hook_event_name: "ConfigChange";
  source:
    | "user_settings"
    | "project_settings"
    | "local_settings"
    | "policy_settings"
    | "skills";
  file_path?: string;
};
```

<h4 id="instructionsloadedhookinput">
  `InstructionsLoadedHookInput`
</h4>

```typescript theme={null}
type InstructionsLoadedHookInput = BaseHookInput & {
  hook_event_name: "InstructionsLoaded";
  file_path: string;
  memory_type: "User" | "Project" | "Local" | "Managed";
  load_reason:
    | "session_start"
    | "nested_traversal"
    | "path_glob_match"
    | "include"
    | "compact";
  globs?: string[];
  trigger_file_path?: string;
  parent_file_path?: string;
};
```

<h4 id="directoryaddedhookinput">
  `DirectoryAddedHookInput`
</h4>

```typescript theme={null}
type DirectoryAddedHookInput = BaseHookInput & {
  hook_event_name: "DirectoryAdded";
  directory: string;
  source: "slash_command" | "register_repo_root";
};
```

`directory` 是被添加的目录的绝对路径。当 `/add-dir` 添加它时，`source` 是 `"slash_command"`，当 SDK 控制请求添加它时，`source` 是 `"register_repo_root"`。

<h4 id="worktreecreatehookinput">
  `WorktreeCreateHookInput`
</h4>

```typescript theme={null}
type WorktreeCreateHookInput = BaseHookInput & {
  hook_event_name: "WorktreeCreate";
  name: string;
};
```

<h4 id="worktreeremovehookinput">
  `WorktreeRemoveHookInput`
</h4>

```typescript theme={null}
type WorktreeRemoveHookInput = BaseHookInput & {
  hook_event_name: "WorktreeRemove";
  worktree_path: string;
};
```

<h4 id="cwdchangedhookinput">
  `CwdChangedHookInput`
</h4>

```typescript theme={null}
type CwdChangedHookInput = BaseHookInput & {
  hook_event_name: "CwdChanged";
  old_cwd: string;
  new_cwd: string;
};
```

<h4 id="filechangedhookinput">
  `FileChangedHookInput`
</h4>

```typescript theme={null}
type FileChangedHookInput = BaseHookInput & {
  hook_event_name: "FileChanged";
  file_path: string;
  event: "change" | "add" | "unlink";
};
```

<h4 id="messagedisplayhookinput">
  `MessageDisplayHookInput`
</h4>

```typescript theme={null}
type MessageDisplayHookInput = BaseHookInput & {
  hook_event_name: "MessageDisplay";
  turn_id: string;
  message_id: string;
  index: number;
  final: boolean;
  delta: string;
};
```

<h3 id="hookjsonoutput">
  `HookJSONOutput`
</h3>

Hook 返回值。

```typescript theme={null}
type HookJSONOutput = AsyncHookJSONOutput | SyncHookJSONOutput;
```

<h4 id="asynchookjsonoutput">
  `AsyncHookJSONOutput`
</h4>

```typescript theme={null}
type AsyncHookJSONOutput = {
  async: true;
  asyncTimeout?: number;
};
```

<h4 id="synchookjsonoutput">
  `SyncHookJSONOutput`
</h4>

```typescript theme={null}
type SyncHookJSONOutput = {
  continue?: boolean;
  suppressOutput?: boolean;
  stopReason?: string;
  decision?: "approve" | "block";
  systemMessage?: string;
  /**
   * 一个终端转义序列（例如 OSC 9 / OSC 777 desktop-notification）
   * 供 Claude Code 代表您发出。仅允许通知/标题 OSCs
   * （0、1、2、9、99、777）和 BEL；包含任何其他内容的值
   * 将被整体忽略。仅交互式 CLI 会发出它；SDK 忽略该字段。
   */
  terminalSequence?: string;
  reason?: string;
  hookSpecificOutput?:
    | {
        hookEventName: "PreToolUse";
        permissionDecision?: "allow" | "deny" | "ask" | "defer";
        permissionDecisionReason?: string;
        updatedInput?: Record<string, unknown>;
        additionalContext?: string;
      }
    | {
        hookEventName: "UserPromptSubmit";
        additionalContext?: string;
        sessionTitle?: string;
        /** 当 decision 为 "block" 时，从阻止消息中省略原始提示。 */
        suppressOriginalPrompt?: boolean;
      }
    | {
        hookEventName: "UserPromptExpansion";
        additionalContext?: string;
      }
    | {
        hookEventName: "SessionStart";
        additionalContext?: string;
        initialUserMessage?: string;
        sessionTitle?: string;
        watchPaths?: string[];
        /**
         * SessionStart hooks 完成后重新扫描 skill 和命令目录，
         * 以便 hook 安装的 skills 在同一会话中可用。
         */
        reloadSkills?: boolean;
      }
    | {
        hookEventName: "Setup";
        additionalContext?: string;
      }
    | {
        hookEventName: "PreModelSwitch";
        /**
         * 与 PreToolUse 相同的约定："allow" 继续，"deny" 取消
         * 切换，"ask" 要求用户确认。仅交互式会话中的 /model
         * 显示该提示；其他所有表面，包括 set_model 请求，
         * 将 "ask" 视为拒绝。
         */
        permissionDecision?: "allow" | "deny" | "ask";
        permissionDecisionReason?: string;
      }
    | {
        hookEventName: "PostModelSwitch";
        /** 通过新模型服务的下一个请求到达模型。 */
        additionalContext?: string;
      }
    | {
        hookEventName: "SubagentStart";
        additionalContext?: string;
      }
    | {
        hookEventName: "PostToolUse";
        additionalContext?: string;
        /**
         * 关于此工具调用结果的简短说明，用于自动模式
         * 权限分类器。限制为 2000 个字符，在响应同一调用的
         * 所有 hooks 之间共享；仅在同步 hook 响应上被接受。
         * 不要将不受信任的工具输出复制到其中。
         */
        classifierContext?: string;
        updatedToolOutput?: unknown;
        /** @deprecated 使用 `updatedToolOutput`，它适用于所有工具。 */
        updatedMCPToolOutput?: unknown;
      }
    | {
        hookEventName: "PostToolUseFailure";
        additionalContext?: string;
      }
    | {
        hookEventName: "PostToolBatch";
        additionalContext?: string;
      }
    | {
        hookEventName: "Stop";
        additionalContext?: string;
      }
    | {
        hookEventName: "SubagentStop";
        additionalContext?: string;
      }
    | {
        hookEventName: "PermissionDenied";
        retry?: boolean;
      }
    | {
        hookEventName: "Notification";
        additionalContext?: string;
      }
    | {
        hookEventName: "PermissionRequest";
        decision:
          | {
              behavior: "allow";
              updatedInput?: Record<string, unknown>;
              updatedPermissions?: PermissionUpdate[];
            }
          | {
              behavior: "deny";
              message?: string;
              interrupt?: boolean;
            };
      }
    | {
        hookEventName: "Elicitation";
        action?: "accept" | "decline" | "cancel";
        content?: Record<string, unknown>;
      }
    | {
        hookEventName: "ElicitationResult";
        action?: "accept" | "decline" | "cancel";
        content?: Record<string, unknown>;
      }
    | {
        hookEventName: "CwdChanged";
        watchPaths?: string[];
      }
    | {
        hookEventName: "FileChanged";
        watchPaths?: string[];
      }
    | {
        hookEventName: "WorktreeCreate";
        worktreePath: string;
      }
    | {
        hookEventName: "MessageDisplay";
        /** 用来代替 delta 显示的文本。省略（或返回 delta 不变）以显示原始内容。 */
        displayContent?: string;
      };
};
```

<h2 id="tool-input-types">
  工具输入类型
</h2>

所有内置 Claude Code 工具的输入架构文档。这些类型从 `@anthropic-ai/claude-agent-sdk/sdk-tools` 导出，可用于类型安全的工具交互。

<h3 id="toolinputschemas">
  `ToolInputSchemas`
</h3>

从 `@anthropic-ai/claude-agent-sdk/sdk-tools` 导出的工具输入类型的联合；成员包括：

```typescript theme={null}
type ToolInputSchemas =
  | AgentInput
  | ArtifactInput
  | AskUserQuestionInput
  | BashInput
  | CronCreateInput
  | CronDeleteInput
  | CronListInput
  | EnterPlanModeInput
  | EnterWorktreeInput
  | ExitPlanModeInput
  | ExitWorktreeInput
  | FileEditInput
  | FileReadInput
  | FileWriteInput
  | GlobInput
  | GrepInput
  | ListMcpResourcesInput
  | McpInput
  | MonitorInput
  | NotebookEditInput
  | ProjectsInput
  | PushNotificationInput
  | ReadMcpResourceDirInput
  | ReadMcpResourceInput
  | RefreshMcpToolsInput
  | RemoteTriggerInput
  | ReportFindingsInput
  | ScheduleWakeupInput
  | ShowOnboardingRolePickerInput
  | TaskCreateInput
  | TaskGetInput
  | TaskListInput
  | TaskStopInput
  | TaskUpdateInput
  | TodoWriteInput
  | WebFetchInput
  | WebSearchInput
  | WorkflowInput;
```

<h3 id="agent">
  Agent
</h3>

**工具名称：** `Agent`。之前的名称 `Task` 仍然被接受作为别名，[`SDKSystemMessage`](#sdksystemmessage) 初始化消息中的 `tools` 数组目前为了向后兼容仍将此工具列为 `Task`。

<Note>
  在 Claude Code v2.1.212 或更高版本上，`mode` 字段已弃用且被忽略。子代理在父会话的权限模式或其定义的 [`permissionMode`](#agentdefinition) 中运行，[子代理继承规则](/docs/zh-CN/agent-sdk/permissions#available-modes)决定使用哪一个。
</Note>

```typescript theme={null}
type AgentInput = {
  description: string;
  prompt: string;
  subagent_type?: string;
  model?: "sonnet" | "opus" | "haiku" | "fable";
  run_in_background?: boolean;
  name?: string;
  team_name?: string; // 已弃用；被忽略
  mode?: "acceptEdits" | "auto" | "bypassPermissions" | "default" | "dontAsk" | "plan"; // 已弃用；被忽略。子代理继承规则决定子代理的权限模式
  isolation?: "worktree" | "remote";
};
```

启动新代理以自主处理复杂的多步骤任务。

<h3 id="askuserquestion">
  AskUserQuestion
</h3>

**工具名称：** `AskUserQuestion`

```typescript theme={null}
type AskUserQuestionInput = {
  questions: Array<{
    question: string;
    header: string;
    options: Array<{ label: string; description: string; preview?: string }>;
    multiSelect: boolean;
  }>;
  answers?: Record<string, string>;
  annotations?: Record<string, { preview?: string; notes?: string }>;
  metadata?: { source?: string };
};
```

在执行期间向用户提出澄清问题。请参阅[处理批准和用户输入](/docs/zh-CN/agent-sdk/user-input#handle-clarifying-questions)了解使用详情。

<h3 id="bash">
  Bash
</h3>

**工具名称：** `Bash`

```typescript theme={null}
type BashInput = {
  command: string;
  timeout?: number; // 毫秒。前台：默认上限为 600000，更高的值会被限制。使用 run_in_background（Claude Code v2.1.285 或更高版本）：后台时间限制，省略时为 1800000，上限为 7200000，除非提高
  description?: string;
  run_in_background?: boolean;
  dangerouslyDisableSandbox?: boolean;
};
```

执行 Bash 命令，支持可选超时和后台执行。工作目录在命令之间保持不变，包括多轮会话后续轮次中运行的命令；shell 状态（如导出的环境变量）不保持。有关哪些目录更改会保持的限制，请参阅[命令之间保持什么](/docs/zh-CN/tools-reference#what-persists-between-commands)。有关设置前台上限的内容，请参阅[超时和输出限制](/docs/zh-CN/tools-reference#timeout-and-output-limits)。有关后台时间限制，请参阅[后台命令的时间限制](/docs/zh-CN/tools-reference#time-limit-for-background-commands)。

<h3 id="monitor">
  Monitor
</h3>

**工具名称：** `Monitor`

```typescript theme={null}
type MonitorInput = {
  description: string;
  timeout_ms: number;
  command?: string;
  ws?: {
    url: string;
    protocols?: string[];
  };
};
```

运行后台源并将每个事件传递给 Claude，以便它可以做出反应而无需轮询：`command` 运行脚本并为每个 stdout 行发出一个事件，`ws` 打开 WebSocket 并为每个文本帧发出一个事件。恰好提供 `command` 或 `ws` 之一。`ws` 源需要 Claude Code v2.1.195 或更高版本。

`timeout_ms` 是监视的截止时间（以毫秒为单位）。它默认为 300000，接受最高 3600000 的值。有效截止时间最多为 1800000，即 30 分钟，因此更大的接受值会被缩短到该值。在截止时间，监视结束，Claude 收到一个通知，以便在仍需要时可以启动新的监视。

导出的类型将 `timeout_ms` 标记为必需，因为架构填充了默认值；省略它的调用会验证通过。

当 Monitor 运行命令时，它遵循与 Bash 相同的权限规则；WebSocket 监视会单独提示批准。请参阅 [Monitor 工具参考](/docs/zh-CN/tools-reference#monitor-tool)了解行为和提供商可用性。

<h3 id="taskoutput">
  TaskOutput
</h3>

在 Claude Code v2.1.277 中移除，连同其 `TaskOutputInput` 类型一起。之前从运行中或已完成的后台任务检索输出；Claude 改为使用 `Read` 读取后台任务的输出文件。

仍然命名 `TaskOutput` 的 `disallowedTools` 条目或拒绝规则会被忽略，不会发出警告。

<h3 id="edit">
  Edit
</h3>

**工具名称：** `Edit`

```typescript theme={null}
type FileEditInput = {
  file_path: string;
  old_string: string;
  new_string: string;
  replace_all?: boolean;
};
```

在文件中执行精确字符串替换。

<h3 id="read">
  Read
</h3>

**工具名称：** `Read`

```typescript theme={null}
type FileReadInput = {
  file_path: string;
  offset?: number;
  limit?: number;
  pages?: string;
};
```

从本地文件系统读取文件，包括文本、图像、PDF 和 Jupyter 笔记本。对 PDF 页面范围使用 `pages`（例如，`"1-5"`）。

对于 PDF，Claude 在 Read 调用的 `tool_result` 内容中接收文件的内容。返回 `pdf` [输出](#tool-output-types)的读取操作包含一个摘要 `text` 块，后跟一个 `document` 块。返回 `parts` 输出的读取操作包含摘要 `text` 块，后跟每个提取页面的一个块：一个 `image` 块，或当 Claude Code 无法将其呈现为图像时命名该页面的 `text` 块。在 Agent SDK v0.3.242 之前，Claude Code 在工具结果后作为单独的 `user` 消息传递文件的内容。

<h3 id="write">
  Write
</h3>

**工具名称：** `Write`

```typescript theme={null}
type FileWriteInput = {
  file_path: string;
  content: string;
};
```

将文件写入本地文件系统，如果存在则覆盖。

<h3 id="glob">
  Glob
</h3>

**工具名称：** `Glob`

```typescript theme={null}
type GlobInput = {
  pattern: string;
  path?: string;
};
```

快速文件模式匹配，适用于任何代码库大小。

<h3 id="grep">
  Grep
</h3>

**工具名称：** `Grep`

```typescript theme={null}
type GrepInput = {
  pattern: string;
  path?: string;
  glob?: string;
  type?: string;
  output_mode?: "content" | "files_with_matches" | "count";
  "-i"?: boolean;
  "-o"?: boolean; // 仅打印每行的匹配部分；需要 output_mode: "content"
  "-n"?: boolean;
  "-B"?: number;
  "-A"?: number;
  "-C"?: number;
  context?: number;
  head_limit?: number;
  offset?: number;
  multiline?: boolean;
};
```

基于 ripgrep 的强大搜索工具，支持正则表达式。

<h3 id="taskstop">
  TaskStop
</h3>

**工具名称：** `TaskStop`

```typescript theme={null}
type TaskStopInput = {
  task_id?: string;
  shell_id?: string; // 已弃用：使用 task_id
};
```

按 ID 停止运行的后台任务或 shell。自 v2.1.198 起，`task_id` 也接受代理团队队友或按代理 ID 或名称的命名后台代理。

<h3 id="notebookedit">
  NotebookEdit
</h3>

**工具名称：** `NotebookEdit`

```typescript theme={null}
type NotebookEditInput = {
  notebook_path: string;
  cell_id?: string;
  new_source: string;
  cell_type?: "code" | "markdown";
  edit_mode?: "replace" | "insert" | "delete";
};
```

编辑 Jupyter 笔记本文件中的单元格。

<h3 id="webfetch">
  WebFetch
</h3>

**工具名称：** `WebFetch`

```typescript theme={null}
type WebFetchInput = {
  url: string;
  prompt: string;
};
```

从 URL 获取内容并使用 AI 模型处理它。

<h3 id="websearch">
  WebSearch
</h3>

**工具名称：** `WebSearch`

```typescript theme={null}
type WebSearchInput = {
  query: string;
  allowed_domains?: string[];
  blocked_domains?: string[];
};
```

搜索网络并返回格式化的结果。

<h3 id="workflow">
  Workflow
</h3>

**工具名称：** `Workflow`

```typescript theme={null}
type WorkflowInput = {
  script?: string;
  name?: string;
  scriptPath?: string;
  args?: unknown; // 任何 JSON 值；发布的类型将其呈现为对象映射
  resumeFromRunId?: string;
  title?: string; // 被忽略；脚本的 meta 块设置标题
  description?: string; // 被忽略；脚本的 meta 块设置描述
};
```

运行[动态工作流](/docs/zh-CN/workflows)：一个脚本，在后台协调许多子代理并返回一个统一的结果。Workflow 工具在 Agent SDK v0.3.149 及更高版本中可用。至少需要 `script`、`name` 或 `scriptPath` 之一。

| 字段 | 类型 | 描述 |
| - | - | - |
| `script` | `string` | 内联工作流脚本。必须以 `export const meta = { name, description }` 作为字面量开头，后跟使用 `agent()`、`parallel()`、`pipeline()` 和 `phase()` 的脚本主体。`meta` 中的可选 `phases` 数组在进度视图中将代理分组到命名阶段下 |
| `name` | `string` | 内置工作流的名称或保存在 `.claude/workflows/` 中的工作流名称。解析为脚本 |
| `scriptPath` | `string` | 磁盘上工作流脚本文件的路径。优先于 `script` 和 `name`。Claude Code 持久化每次调用的脚本并在结果中返回路径，因此您可以编辑该文件并使用相同的 `scriptPath` 重新调用以进行迭代 |
| `args` | `unknown` | 输入值，作为全局 `args` 暴露给脚本，用于参数化的命名工作流，例如研究问题或文件路径列表。将数组和对象作为实际 JSON 值传递，而不是作为 JSON 编码的字符串 |
| `resumeFromRunId` | `string` | 要恢复的先前 `Workflow` 调用的运行 ID。具有未更改输入的已完成 `agent()` 调用通常返回缓存的结果；其余的实时运行。[暂停后恢复](/docs/zh-CN/workflows#resume-after-a-pause)涵盖哪些已完成的调用会重新运行。仅限同一会话 |
| `title` | `string` | 被忽略；脚本的 `meta` 块设置标题 |
| `description` | `string` | 被忽略；脚本的 `meta` 块设置描述 |

<h3 id="todowrite">
  TodoWrite
</h3>

**工具名称：** `TodoWrite`

```typescript theme={null}
type TodoWriteInput = {
  todos: Array<{
    content: string;
    status: "pending" | "in_progress" | "completed";
    activeForm: string;
  }>;
};
```

创建和管理结构化任务列表以跟踪进度。

<Note>
  以下工具仅在 Claude 3.x 模型、Opus 4 至 4.7、Sonnet 4 至 4.6 和 Haiku 4.5 上默认可用。在所有其他模型上，包括 Claude Code 无法识别的模型 ID，除非您选择加入，否则它们不可用：

  * `TodoWrite`
  * `TaskCreate`
  * `TaskGet`
  * `TaskUpdate`
  * `TaskList`

  无论工具在何处可用，Claude Code 都提供四个 Task 工具，或者当你设置 `CLAUDE_CODE_ENABLE_TASKS=0` 时改为提供 `TodoWrite`。

  此默认集合适用于 Claude Code v2.1.268 及更高版本，TypeScript Agent SDK 从 v0.3.268 开始捆绑此版本。

  请参阅[模型可用性](/docs/zh-CN/agent-sdk/todo-tracking#model-availability)以选择加入。
</Note>

<h3 id="taskcreate">
  TaskCreate
</h3>

**工具名称：** `TaskCreate`

```typescript theme={null}
type TaskCreateInput = {
  subject: string;
  description: string;
  activeForm?: string;
  metadata?: Record<string, unknown>;
};
```

创建单个任务并返回其分配的 ID。

<h3 id="taskupdate">
  TaskUpdate
</h3>

**工具名称：** `TaskUpdate`

```typescript theme={null}
type TaskUpdateInput = {
  taskId: string;
  status?: "pending" | "in_progress" | "completed" | "deleted";
  subject?: string;
  description?: string;
  activeForm?: string;
  addBlocks?: string[];
  addBlockedBy?: string[];
  owner?: string;
  metadata?: Record<string, unknown>;
};
```

按 ID 修补一个任务。将 `status` 设置为 `"deleted"` 以删除它。

<h3 id="taskget">
  TaskGet
</h3>

**工具名称：** `TaskGet`

```typescript theme={null}
type TaskGetInput = {
  taskId: string;
};
```

返回一个任务的完整详情，或在找不到 ID 时返回 `null`。

<h3 id="tasklist">
  TaskList
</h3>

**工具名称：** `TaskList`

```typescript theme={null}
type TaskListInput = {};
```

返回当前列表中所有任务的快照。

<h3 id="exitplanmode">
  ExitPlanMode
</h3>

**工具名称：** `ExitPlanMode`

```typescript theme={null}
type ExitPlanModeInput = {
  /** 已弃用：不再使用。 */
  allowedPrompts?: Array<{
    tool: "Bash";
    prompt: string;
  }>;
  [k: string]: unknown;
};
```

退出 Plan Mode。`allowedPrompts` 字段已弃用且被忽略；Claude Code 仍然接受它，以便现有调用者和记录验证。在 v2.1.205 之前，它请求基于提示的 Bash 权限以实现计划。

<h3 id="listmcpresources">
  ListMcpResources
</h3>

**工具名称：** `ListMcpResourcesTool`

```typescript theme={null}
type ListMcpResourcesInput = {
  server?: string;
};
```

列出来自连接服务器的可用 MCP 资源。

<h3 id="readmcpresource">
  ReadMcpResource
</h3>

**工具名称：** `ReadMcpResourceTool`

```typescript theme={null}
type ReadMcpResourceInput = {
  server: string;
  uri: string;
};
```

从服务器读取特定的 MCP 资源。

<h3 id="enterworktree">
  EnterWorktree
</h3>

**工具名称：** `EnterWorktree`

```typescript theme={null}
type EnterWorktreeInput = {
  name?: string;
  path?: string;
};
```

创建并进入临时 git worktree 以进行隔离工作。传递 `path` 以切换到现有 worktree 而不是创建新的。在首次进入时，目标必须是当前存储库的已注册 worktree，或在多存储库工作区中，必须是嵌套在其中的存储库的已注册 worktree；从 worktree 会话内进入时，必须在会话存储库的 `.claude/worktrees/` 下。`name` 和 `path` 互斥。

<h3 id="exitworktree">
  ExitWorktree
</h3>

**工具名称：** `ExitWorktree`

```typescript theme={null}
type ExitWorktreeInput = {
  action: "keep" | "remove";
  discard_changes?: boolean;
};
```

退出当前 git worktree 并返回到原始工作目录。`keep` 操作将 worktree 和分支保留在磁盘上，而 `remove` 删除两者。当删除具有未提交文件或未合并提交的 worktree 时，`discard_changes` 必须为 `true`。

<h3 id="enterplanmode">
  EnterPlanMode
</h3>

**工具名称：** `EnterPlanMode`

```typescript theme={null}
type EnterPlanModeInput = {};
```

进入 Plan Mode，Claude 在其中研究并呈现计划，然后再进行更改。

<h3 id="croncreate">
  CronCreate
</h3>

**工具名称：** `CronCreate`

```typescript theme={null}
type CronCreateInput = {
  cron: string;
  prompt: string;
  recurring?: boolean;
  durable?: boolean;
};
```

在本地时间的 5 字段 cron 计划上安排提示运行。将 `recurring` 设置为 `false` 以在下一个匹配时仅触发一次。作业默认为会话范围，恢复时使用 `--resume` 或 `--continue` 会恢复尚未过期的作业。请参阅[计划任务](/docs/zh-CN/scheduled-tasks)。

将 `durable` 设置为 `true` 请求持久化到 `.claude/scheduled_tasks.json`，以便作业在重启后继续存在。持久化调度并非在每个会话中都可用：当不可用时，Claude Code 接受 `durable: true` 但创建仅会话的作业。读取输出的 `durable` 字段以查看作业是否已持久化。

<h3 id="crondelete">
  CronDelete
</h3>

**工具名称：** `CronDelete`

```typescript theme={null}
type CronDeleteInput = {
  id: string;
};
```

按从 `CronCreate` 返回的 ID 删除计划的 cron 作业。

<h3 id="cronlist">
  CronList
</h3>

**工具名称：** `CronList`

```typescript theme={null}
type CronListInput = {};
```

列出计划的 cron 作业：来自 `.claude/scheduled_tasks.json` 的持久化作业和来自当前会话的仅会话作业。

<h3 id="schedulewakeup">
  ScheduleWakeup
</h3>

**工具名称：** `ScheduleWakeup`

```typescript theme={null}
type ScheduleWakeupInput = {
  delaySeconds?: number;
  reason?: string;
  prompt?: string;
  noop?: boolean;
  stop?: boolean;
};
```

安排一次性唤醒，在延迟后触发给定的提示。此工具支持自定步调的 `/loop` 命令。运行时将 `delaySeconds` 限制在 60 到 3600 秒之间。除非 `stop` 为 true，否则 `delaySeconds`、`reason`、`prompt` 和 `noop` 字段是必需的。`noop: true` 报告没有任何更改的唤醒。设置 `stop: true` 取消待处理的唤醒并结束自定步调的 `/loop`。`stop` 字段需要 Claude Code v2.1.202 或更高版本。请参阅[工具参考中的 ScheduleWakeup 行](/docs/zh-CN/tools-reference)。

<h3 id="remotetrigger">
  RemoteTrigger
</h3>

**工具名称：** `RemoteTrigger`

```typescript theme={null}
type RemoteTriggerInput = {
  action:
    | "list"
    | "get"
    | "create"
    | "update"
    | "run"
    | "create_webhook_trigger"
    | "list_runs"
    | "get_run_log";
  trigger_id?: string;
  session_id?: string;
  cursor?: string;
  body?: {
    [k: string]: unknown;
  };
};
```

管理[例程](/docs/zh-CN/routines)，即在云中托管的计划和触发的 Claude Code 运行。此工具支持 `/schedule` 命令。`trigger_id` 对于 `get`、`update`、`run` 和 `list_runs` 操作是必需的。`body` 对于 `create`、`update` 和 `create_webhook_trigger` 是必需的，对于 `run` 是可选的。

`create_webhook_trigger` 将事件源附加到现有例程，例如触发它的 [GitHub 事件](/docs/zh-CN/routines#add-a-github-trigger)。`body` 命名源、事件和要触发的例程。需要 Claude Code v2.1.225 或更高版本。

`list_runs` 列出例程的最近运行，`get_run_log` 读取一个运行的日志。`session_id` 从 `list_runs` 结果命名要读取的运行，`cursor` 分页浏览任一操作的结果。两个操作都需要 Claude Code v2.1.227 或更高版本。

此工具仅在会话使用启用了例程的计划的 claude.ai 账户进行身份验证时可用，当您的组织的策略禁用[网络上的 Claude Code](/docs/zh-CN/claude-code-on-the-web) 时不存在。在 Claude Code v2.1.227 或更高版本上，当所有者为组织[关闭例程](/docs/zh-CN/routines#routines-are-disabled-by-your-organizations-policy)时，该工具也不存在。在 v2.1.227 之前，仅关闭例程切换的会话仍然显示该工具，服务器拒绝其调用。

<h3 id="pushnotification">
  PushNotification
</h3>

**工具名称：** `PushNotification`

```typescript theme={null}
type PushNotificationInput = {
  message: string;
  status: "proactive";
};
```

向用户发送主动推送通知。将 `message` 保持在 200 个字符以下，因为移动操作系统会截断较长的文本。请参阅[工具参考中的 PushNotification 行](/docs/zh-CN/tools-reference)了解提供商可用性；推送传递通过 Anthropic 托管的基础设施进行，该基础设施无法从 Amazon Bedrock、AWS 上的 Claude Platform、Google Cloud 的 Agent Platform 或 Microsoft Foundry 访问。

<h3 id="repl">
  REPL
</h3>

在 v2.1.275 中移除。通过 v2.1.274，可以通过在 [`env` 选项](#options)中设置 `CLAUDE_CODE_REPL=1` 来打开实验性 `REPL` 工具。

<h3 id="reportfindings">
  ReportFindings
</h3>

**工具名称：** `ReportFindings`

```typescript theme={null}
type ReportFindingsInput = {
  level?: "low" | "medium" | "high" | "xhigh" | "max";
  findings: Array<{
    file: string;
    line?: number;
    summary: string;
    failure_scenario: string;
    short_summary?: string;
    category?: string;
    verdict?: "CONFIRMED" | "PLAUSIBLE";
    outcome?: "fixed" | "skipped" | "no_change_needed";
  }>;
};
```

将代码审查发现报告为结构化列表，以便 Claude Code 可以呈现它们而不是将其打印为文本。`level` 是审查运行的工作量级别。发现按最严重优先排序，每次调用最多 32 个，当没有发现存活时数组为空。需要 Claude Code v2.1.196 或更高版本。

每个发现包含这些字段：

* `file`：发现所在的存储库相对路径。可选的 `line` 是它锚定到的 1 索引行。
* `summary`：缺陷的单句陈述。`failure_scenario` 描述导致错误输出或崩溃的具体输入和状态。
* `short_summary`：可选的最多 60 个字符的压缩标签，用于紧凑显示。需要 Claude Code v2.1.212 或更高版本。
* `category`：可选的发现类型的短 kebab-case slug，例如 `correctness` 或 `test-coverage`。需要 Claude Code v2.1.199 或更高版本。
* `verdict`：在验证通过运行时设置；在仅内联审查中不存在。
* `outcome`：仅在应用修复后重新报告时设置。

<h3 id="artifact">
  Artifact
</h3>

**工具名称：** `Artifact`

```typescript theme={null}
type ArtifactInput = {
  action?: "publish" | "list";
  file_path?: string;
  favicon?: string;
  icon?: string;
  limit?: number;
  scope?: "mine" | "shared" | "all";
  title?: string;
  description?: string;
  label?: string;
  url?: string;
  force?: boolean;
  capabilities?: Record<string, unknown>;
  contract?: "latest" | string;
};
```

将本地 `.html` 或 `.md` 文件发布为托管的 artifact 页面，或列出用户发布的 artifacts。省略 `action` 或传递 `"publish"` 以发布 `file_path`，这对于发布操作是必需的。每个下面的字段适用于发布：

* `icon`：artifact 浏览器标签图标的一个短通用词，例如 `chart` 或 `map`。Claude 在首次发布时包含它，在更新时省略它，这会保留 artifact 的存储图标。
* `favicon`：已弃用，Claude 会省略它。
* `title`：当 HTML 文件没有 `<title>` 标签时，在浏览器标签和库中命名发布的页面。
* `url`：针对现有 artifact 以就地更新，而不是创建新的。

`force` 是最后手段的覆盖，丢弃另一个会话发布的较新版本。在冲突时，失败的发布返回较新的内容；Claude 将其更改合并到该内容上，或重新读取 artifact，然后再次发布。仅当用户明确要求丢弃该版本时才传递 `force`。

传递 `"list"` 以枚举用户发布的 artifacts；仅 `limit` 和 `scope` 可能伴随它。`scope` 默认为 `"mine"`，列出用户拥有的 artifacts；`"shared"` 列出其他人与用户共享的 artifacts，`"all"` 列出两者。

* `capabilities`：发布的页面使用的运行时功能，由功能名称键入，例如[页面可能调用的连接器](/docs/zh-CN/artifacts#pull-live-data-with-mcp-connectors)。artifact 服务验证声明并拒绝命名账户无法使用的功能或给予一个无效配置的发布。传递 `{}` 以清除存储的声明，在重新部署时省略字段以保留它。需要 Agent SDK v0.3.235 或更高版本。
* `contract`：发布的页面运行的运行时版本。省略它以保留 artifact 的当前版本，传递 `"latest"` 以升级，或传递特定版本以固定或回滚。需要 Agent SDK v0.3.235 或更高版本。

这些类型已导出，但该工具在 Agent SDK 会话中默认处于关闭状态。发布还需要 [artifacts 可用性表](/docs/zh-CN/artifacts#availability)中的每个条件，使用 API 密钥进行身份验证的会话不满足这些条件。

<h3 id="projects">
  Projects
</h3>

**工具名称：** `Projects`

```typescript theme={null}
type ProjectsInput = {
  method:
    | "project_info"
    | "project_read"
    | "project_search"
    | "project_write"
    | "project_delete";
  path?: string;
  content?: string;
  local_path?: string;
  present_to_user?: boolean;
  query?: string;
  n?: number;
};
```

读取和写入附加到会话的 claude.ai Project。在 `method` 上分派：

* `project_info`：返回项目元数据和文档列表。
* `project_read`：按 `path` 读取一个文档。
* `project_search`：使用 `query` 查询项目的知识库。`n` 限制命中数并默认为 5。
* `project_write`：从 `content`（包含内联文本）或 `local_path`（命名工作目录内的文件）中的恰好一个在 `path` 处创建或替换文档。`present_to_user: true` 将写入的文档标记为用户需要看到的可交付成果。
* `project_delete`：按 `path` 删除文档。

<h3 id="readmcpresourcedir">
  ReadMcpResourceDir
</h3>

**工具名称：** `ReadMcpResourceDirTool`

```typescript theme={null}
type ReadMcpResourceDirInput = {
  server: string;
  uri: string;
};
```

列出 MCP 服务器上目录资源的直接子项。仅可用于已声明支持目录列表的服务器；列表不是递归的。目录列表并非在每个会话中都启用：当关闭时，调用返回空的 `resources` 列表，`error` 字段报告目录列表未启用。

<h3 id="refreshmcptools">
  RefreshMcpTools
</h3>

**工具名称：** `RefreshMcpTools`

```typescript theme={null}
type RefreshMcpToolsInput = {
  server?: string; // 仅刷新此服务器；省略以刷新所有连接的服务器
};
```

重新查询连接的 MCP 服务器的工具列表并应用任何更改。这些类型已导出，但 Claude Code 仅在您在 [`env` 选项](#options)中设置 `CLAUDE_CODE_ENABLE_REFRESH_MCP_TOOLS=1` 时注册该工具，并且仅在至少有一个 MCP 服务器的会话中。需要 Claude Code v2.1.211 或更高版本。

<h3 id="showonboardingrolepicker">
  ShowOnboardingRolePicker
</h3>

**工具名称：** `ShowOnboardingRolePicker`

```typescript theme={null}
type ShowOnboardingRolePickerInput = {};
```

在 Cowork 入职期间呈现可点击的角色选择器芯片行，以便用户可以选择其角色并获得匹配的插件安装。不需要参数；角色列表由客户端定义。调用会阻塞直到用户响应。

<h3 id="mcpinput">
  McpInput
</h3>

**工具名称：** 形式为 `mcp__<server>__<tool>` 的动态 MCP 工具名称

```typescript theme={null}
type McpInput = {
  [k: string]: unknown;
};
```

MCP 工具参数是开放对象：每个服务器定义自己的参数，因此类型对字段名称或值不施加任何约束。请查阅服务器自己的工具架构以了解特定工具接受的字段。

<h2 id="tool-output-types">
  工具输出类型
</h2>

所有内置 Claude Code 工具的输出架构文档。这些类型从 `@anthropic-ai/claude-agent-sdk/sdk-tools` 导出，代表每个工具返回的实际响应数据。

<h3 id="tooloutputschemas">
  `ToolOutputSchemas`
</h3>

从 `@anthropic-ai/claude-agent-sdk/sdk-tools` 导出的工具输出类型的联合；成员包括：

```typescript theme={null}
type ToolOutputSchemas =
  | AgentOutput
  | ArtifactOutput
  | AskUserQuestionOutput
  | BashOutput
  | CronCreateOutput
  | CronDeleteOutput
  | CronListOutput
  | EnterPlanModeOutput
  | EnterWorktreeOutput
  | ExitPlanModeOutput
  | ExitWorktreeOutput
  | FileEditOutput
  | FileReadOutput
  | FileWriteOutput
  | GlobOutput
  | GrepOutput
  | ListMcpResourcesOutput
  | McpOutput
  | MonitorOutput
  | NotebookEditOutput
  | ProjectsOutput
  | PushNotificationOutput
  | ReadMcpResourceDirOutput
  | ReadMcpResourceOutput
  | RefreshMcpToolsOutput
  | RemoteTriggerOutput
  | ReportFindingsOutput
  | ScheduleWakeupOutput
  | ShowOnboardingRolePickerOutput
  | TaskCreateOutput
  | TaskGetOutput
  | TaskListOutput
  | TaskStopOutput
  | TaskUpdateOutput
  | TodoWriteOutput
  | WebFetchOutput
  | WebSearchOutput
  | WorkflowOutput;
```

<h3 id="agent-2">
  Agent
</h3>

**工具名称：** `Agent`。之前的名称 `Task` 仍然被接受作为别名，[`SDKSystemMessage`](#sdksystemmessage) 初始化消息中的 `tools` 数组目前为了向后兼容仍将此工具列为 `Task`。

```typescript theme={null}
type AgentOutput =
  | {
      status: "completed";
      agentId: string;
      agentType?: string;
      content: Array<{ type: "text"; text: string; citations?: unknown[] | null }>;
      resolvedModel?: string;
      modelsUsed?: string[];
      totalToolUseCount: number;
      totalDurationMs: number;
      totalTokens: number;
      usage: {
        input_tokens: number;
        output_tokens: number;
        cache_creation_input_tokens: number | null;
        cache_read_input_tokens: number | null;
        server_tool_use: {
          web_search_requests: number;
          web_fetch_requests: number;
        } | null;
        service_tier: string | null;
        cache_creation: {
          ephemeral_1h_input_tokens: number;
          ephemeral_5m_input_tokens: number;
        } | null;
        inference_geo?: string | null;
        speed?: string | null;
        iterations?: unknown;
        output_tokens_details?: {
          thinking_tokens?: number | null;
        } | null;
      };
      toolStats?: {
        readCount: number;
        searchCount: number;
        bashCount: number;
        editFileCount: number;
        linesAdded: number;
        linesRemoved: number;
        otherToolCount: number;
        frameCount?: number;
      };
      prompt: string;
      worktreePath?: string;
      worktreeBranch?: string;
    }
  | {
      status: "async_launched";
      isAsync?: true;
      agentId: string;
      description: string;
      resolvedModel?: string;
      modelsUsed?: string[];
      prompt: string;
      outputFile: string;
      canReadOutputFile?: boolean;
    }
  | {
      status: "remote_launched";
      taskId: string;
      sessionUrl: string;
      description: string;
      prompt: string;
      outputFile: string;
    };
```

返回来自子代理的结果。在 `status` 字段上进行区分：`"completed"` 表示已完成的任务，`"async_launched"` 表示后台任务，`"remote_launched"` 表示 Claude Code 分派到远程云会话的任务，其中 `sessionUrl` 链接到该会话，`taskId` 标识它。

在 `completed` 变体上，`resolvedModel` 命名子代理启动时所用的模型，当应用 [`availableModels`](/docs/zh-CN/model-config#restrict-model-selection) 或其他覆盖时，该模型可能与请求的 `model` 输入不同。此字段需要 Claude Code v2.1.174 或更高版本。在 `async_launched` 上，它命名任务移至后台时使用的模型。

`modelsUsed` 列出子代理使用的模型，按顺序。该字段仅在发生中途交换时出现，当运行交换回某个模型时，该模型会再次出现。在 `async_launched` 上，该列表涵盖后台处理前使用的模型。`modelsUsed` 和 `resolvedModel` 的后台处理行为都需要 Claude Code v2.1.212 或更高版本。

如果 Claude Code [保留了子代理的隔离 worktree](/docs/zh-CN/worktrees#isolate-subagents-with-worktrees)，`completed` 结果上的 `worktreePath` 是找到它的位置。`worktreeBranch` 是其分支，当 Claude Code 使用 git 创建 worktree 时出现。

Claude Code 从子代理的最终 API 请求而不是整个运行中填充 `usage` 和 `totalTokens`，因此 `usage.service_tier` 是 API 在该请求上报告的服务层字符串。当存在时，`usage.output_tokens_details.thinking_tokens` 是该请求的输出令牌中属于思考令牌的数量。`output_tokens_details` 字段需要 TypeScript SDK v0.3.228 或更高版本，该版本包含 Claude Code v2.1.228。

`usage.output_tokens_details` 在含义上与 [`Usage.output_tokens_details`](#usage) 匹配，范围限于该最终请求，但其每个级别都是可选的。保护对象和字段，例如 `usage.output_tokens_details?.thinking_tokens ?? 0`，而不是直接读取它。

在 v2.1.207 之前，发布的类型更窄。它省略了 `worktreePath`、`worktreeBranch`、`citations`、`toolStats.frameCount` 和 `inference_geo`、`speed` 和 `iterations` 使用字段，并将 `service_tier` 类型化为 `"standard" | "priority" | "batch"`。类型标记为可选的字段可能在早期版本记录的结果中不存在。

<h3 id="askuserquestion-2">
  AskUserQuestion
</h3>

**工具名称：** `AskUserQuestion`

```typescript theme={null}
type AskUserQuestionOutput = {
  questions: Array<{
    question: string;
    header: string;
    options: Array<{ label: string; description: string; preview?: string }>;
    multiSelect: boolean;
  }>;
  answers: Record<string, string>;
  response?: string;
  annotations?: Record<string, { preview?: string; notes?: string }>;
  afkTimeoutMs?: number;
};
```

返回提出的问题和用户的答案。当用户输入自由形式的回复而不是回答结构化问题时，`response` 被设置；当存在时，Claude 会收到"用户回复：…"而不是每个问题的答案列表。

<h3 id="bash-2">
  Bash
</h3>

**工具名称：** `Bash`

```typescript theme={null}
type BashOutput = {
  stdout: string;
  stderr: string;
  rawOutputPath?: string;
  interrupted: boolean;
  isImage?: boolean;
  backgroundTaskId?: string;
  backgroundedByUser?: boolean;
  timedOutAfterMs?: number;
  backgroundCwdHint?: string;
  backgroundEndsWithFinalResponse?: true;
  dangerouslyDisableSandbox?: boolean;
  returnCodeInterpretation?: string;
  noOutputExpected?: boolean;
  structuredContent?: unknown[];
  persistedOutputPath?: string;
  persistedOutputSize?: number;
  staleReadFileStateHint?: string;
  ghRateLimitHint?: string;
  gitOperation?: {
    commit?: { sha: string; kind: "committed" | "amended" | "cherry-picked"; branch?: string };
    push?: { branch: string };
    branch?: { ref: string; action: "merged" | "rebased" };
    pr?: {
      number: number;
      url?: string;
      action: "created" | "edited" | "merged" | "commented" | "closed" | "reopened" | "ready" | "draft" | "auto-merge-enabled" | "auto-merge-disabled";
    };
  };
};
```

`stdout`、`stderr` 和 `backgroundTaskId` 字段携带：

| 字段 | 它携带的内容 |
| - | - |
| `stdout` | 命令的 stdout 和 stderr，合并为一个交错流 |
| `stderr` | 工具本身添加的通知，例如 shell 工作目录重置，不是命令的 stderr |
| `backgroundTaskId` | 对于后台命令存在 |

`timedOutAfterMs` 是超时时间（以毫秒为单位），当命令达到其超时并移至后台而不是显式启动时设置。`backgroundCwdHint` 在后台命令包含目录更改内置命令（如 `cd`、`pushd`、`popd` 或 `chdir`）时设置，并注意会话工作目录未更改。两个字段都需要 Claude Code v2.1.210 或更高版本。

当在前台运行的子代理拥有后台命令时，该命令[在该子代理的运行结束时结束](/docs/zh-CN/tools-reference#when-a-background-command-stops)。Claude Code 在此类命令上将 `backgroundEndsWithFinalResponse` 设置为 `true`，并在命令存活该轮时省略该字段，如主对话或后台子代理启动的命令那样。该字段需要 Claude Code v2.1.227 或更高版本。

Claude Code 将 `gitOperation.commit.branch` 设置为 git 提交摘要行中命名的分支，对于在分离 HEAD 上进行的提交则省略它。该字段需要 Agent SDK v0.3.227 或更高版本。Claude Code 将 `gh pr reopen` 命令报告为 `reopened` PR 操作，这需要 Agent SDK v0.3.234 或更高版本。

<h3 id="monitor-2">
  Monitor
</h3>

**工具名称：** `Monitor`

```typescript theme={null}
type MonitorOutput = {
  taskId: string;
  timeoutMs: number;
  persistent?: boolean;
};
```

返回运行监视器的后台任务 ID。使用此 ID 与 `TaskStop` 一起提前取消监视。

<h3 id="edit-2">
  Edit
</h3>

**工具名称：** `Edit`

```typescript theme={null}
type FileEditOutput = {
  filePath: string;
  oldString: string;
  newString: string;
  originalFile: string | null;
  structuredPatch: Array<{
    oldStart: number;
    oldLines: number;
    newStart: number;
    newLines: number;
    lines: string[];
  }>;
  userModified: boolean;
  replaceAll: boolean;
  gitDiff?: {
    filename: string;
    status: "modified" | "added";
    additions: number;
    deletions: number;
    changes: number;
    patch: string;
    repository?: string | null;
  };
};
```

返回编辑操作的结构化差异。

<h3 id="read-2">
  Read
</h3>

**工具名称：** `Read`

```typescript theme={null}
type FileReadOutput =
  | {
      type: "text";
      file: {
        filePath: string;
        content: string;
        numLines: number;
        startLine: number;
        totalLines: number;
        /** True when a whole-file read was auto-paginated because it exceeded the token cap (the content is a partial first page). */
        truncatedByTokenCap?: boolean;
      };
    }
  | {
      type: "image";
      file: {
        base64: string;
        type: "image/jpeg" | "image/png" | "image/gif" | "image/webp";
        originalSize: number;
        dimensions?: {
          originalWidth?: number;
          originalHeight?: number;
          displayWidth?: number;
          displayHeight?: number;
        };
      };
    }
  | {
      type: "notebook";
      file: {
        filePath: string;
        cells: unknown[];
      };
    }
  | {
      type: "pdf";
      file: {
        filePath: string;
        base64: string;
        originalSize: number;
      };
    }
  | {
      type: "parts";
      file: {
        filePath: string;
        originalSize: number;
        count: number;
        outputDir: string;
      };
      /** Document page number of the first extracted page; labels the page images in the tool_result content. */
      firstPage?: number;
      /** In-process only: the page-image bytes are delivered as image blocks in the tool_result content and aren't retained on the emitted tool_use_result, so this key is absent there. */
      pages?: {
        base64: string;
        mediaType: "image/jpeg" | "image/png" | "image/gif" | "image/webp";
        error?: string;
      }[];
    }
  | {
      type: "file_unchanged";
      file: {
        filePath: string;
      };
      /** Set when the dedup matched a startup-seeded entry (CLAUDE.md / nested memory) rather than a prior Read tool_result. */
      source?: "seeded";
    };
```

返回适合文件类型的格式的文件内容。在 `type` 字段上进行区分。

<h3 id="write-2">
  Write
</h3>

**工具名称：** `Write`

```typescript theme={null}
type FileWriteOutput = {
  type: "create" | "update";
  filePath: string;
  content: string;
  structuredPatch: Array<{
    oldStart: number;
    oldLines: number;
    newStart: number;
    newLines: number;
    lines: string[];
  }>;
  originalFile: string | null;
  gitDiff?: {
    filename: string;
    status: "modified" | "added";
    additions: number;
    deletions: number;
    changes: number;
    patch: string;
    repository?: string | null;
  };
  userModified?: boolean;
};
```

返回写入结果，包含结构化差异信息。`originalFile` 和 `structuredPatch` 持有的内容取决于写入：

* 对于新创建的文件，`originalFile` 为 null，`structuredPatch` 为空
* 在覆盖时，`originalFile` 携带之前的内容，除非该内容大于约 10 MB：Claude Code 则跳过差异并返回 `originalFile` null 和 `structuredPatch` 空
* 当写入未更改任何内容或差异超时时，`structuredPatch` 也为空

<h3 id="glob-2">
  Glob
</h3>

**工具名称：** `Glob`

```typescript theme={null}
type GlobOutput = {
  durationMs: number;
  numFiles: number;
  filenames: string[];
  truncated: boolean;
  totalMatches?: number;
  countIsComplete?: boolean;
};
```

返回与 glob 模式匹配的文件路径，按修改时间排序。

`totalMatches` 和 `countIsComplete` 需要 Claude Code v2.1.191 或更高版本。`totalMatches` 报告截断前的匹配文件数。当 `countIsComplete` 为 false 时，`totalMatches` 是一个下界，因为底层搜索截断了其自己的输出。

<h3 id="grep-2">
  Grep
</h3>

**工具名称：** `Grep`

```typescript theme={null}
type GrepOutput = {
  mode?: "content" | "files_with_matches" | "count";
  numFiles: number;
  filenames: string[];
  content?: string;
  numLines?: number;
  numMatches?: number;
  totalFiles?: number;
  totalLines?: number;
  appliedLimit?: number;
  appliedOffset?: number;
};
```

返回搜索结果。形状因 `mode` 而异：文件列表、带匹配的内容或匹配计数。在 `count` 模式下，`numFiles` 和 `numMatches` 是完整结果集上的总计，不是分页切片。在 v2.1.208 之前，截断列出条目的 `head_limit` 或 `offset` 也会截断这些总计。

`totalFiles` 需要 Claude Code v2.1.208 或更高版本，并在 `files_with_matches` 模式下报告 `head_limit` 和 `offset` 分页前的总结果数。`totalLines` 需要 Claude Code v2.1.210 或更高版本，并在 `content` 模式下报告分页前的总行数。

<h3 id="taskstop-2">
  TaskStop
</h3>

**工具名称：** `TaskStop`

```typescript theme={null}
type TaskStopOutput = {
  message: string;
  task_id: string;
  task_type: string;
  command?: string;
};
```

停止后台任务后返回确认。

<h3 id="notebookedit-2">
  NotebookEdit
</h3>

**工具名称：** `NotebookEdit`

```typescript theme={null}
type NotebookEditOutput = {
  new_source: string;
  old_source?: string;
  cell_id?: string;
  cell_type: "code" | "markdown";
  language: string;
  edit_mode: string;
  error?: string;
  notebook_path: string;
  original_file: string;
  updated_file: string;
};
```

返回笔记本编辑的结果，包含原始和更新的文件内容。

<h3 id="webfetch-2">
  WebFetch
</h3>

**工具名称：** `WebFetch`

```typescript theme={null}
type WebFetchOutput = {
  bytes: number;
  code: number;
  codeText: string;
  result: string;
  durationMs: number;
  url: string;
  artifactRead?: {
    slug: string;
    ver?: string;
    seeded?: false;
  };
};
```

返回获取的内容，包含 HTTP 状态和元数据。

`artifactRead` 是 Claude Code 自己的工件读取记录，仅当 Claude 获取会话可以发布的工件时出现。Claude Code 在会话恢复时读取它回来，以便稍后的发布基于正确的版本；您的代码不需要对其采取行动。`slug` 命名工件，`ver` 是读取记录的版本，当它未记录任何内容时不存在，`seeded: false` 标记其完整源未到达 Claude 的读取。`seeded` 字段需要 Agent SDK v0.3.239 或更高版本。

<h3 id="websearch-2">
  WebSearch
</h3>

**工具名称：** `WebSearch`

```typescript theme={null}
type WebSearchOutput = {
  query: string;
  results: Array<
    | {
        tool_use_id: string;
        content: Array<{ title: string; url: string }>;
      }
    | string
  >;
  durationSeconds: number;
  searchCount?: number;
};
```

返回来自网络的搜索结果。

<h3 id="workflow-2">
  Workflow
</h3>

**工具名称：** `Workflow`

```typescript theme={null}
type WorkflowOutput = {
  status: "async_launched" | "remote_launched";
  taskId: string;
  taskType?: "local_workflow" | "remote_agent";
  workflowName?: string;
  runId?: string;
  summary?: string;
  transcriptDir?: string;
  scriptPath?: string;
  sessionUrl?: string; // set when the workflow launched as a cloud session
  warning?: string;
  error?: string;
};
```

在工具接受调用后立即返回。最终结果稍后作为任务完成到达。在将运行视为已启动之前检查 `error`：脚本如果语法检查失败，会返回 `status: "async_launched"` 并设置 `error`，且永远不会运行。

| 字段 | 类型 | 描述 |
| - | - | - |
| `status` | `"async_launched" \| "remote_launched"` | 工具接受了调用。`"async_launched"` 用于进程内运行，`"remote_launched"` 用于分派到云会话而不是在进程内运行的运行 |
| `taskId` | `string` | 运行的后台任务标识符 |
| `taskType` | `"local_workflow" \| "remote_agent"` | 已注册后台任务的任务类型，与 `status` 分支匹配 |
| `workflowName` | `string` | 工作流脚本中的 `meta.name` |
| `runId` | `string` | 工作流运行标识符，用于在后续调用中作为 `resumeFromRunId` 传递。对于 `remote_launched` 运行不存在，其中云会话 URL 是恢复句柄 |
| `summary` | `string` | 工作流功能的单行描述 |
| `transcriptDir` | `string` | 执行期间写入子代理转录的目录 |
| `scriptPath` | `string` | 此运行的持久化工作流脚本的路径。编辑它并作为 `scriptPath` 传回以重新运行而无需重新发送脚本 |
| `sessionUrl` | `string` | 云会话 URL，当 `status` 为 `"remote_launched"` 时设置 |
| `warning` | `string` | 非阻塞性提示，例如本地 git 状态与云会话将克隆的推送分支不同 |
| `error` | `string` | 当脚本语法检查失败时设置。存在时，尽管启动状态，运行未启动 |

<h3 id="todowrite-2">
  TodoWrite
</h3>

**工具名称：** `TodoWrite`

```typescript theme={null}
type TodoWriteOutput = {
  oldTodos: Array<{
    content: string;
    status: "pending" | "in_progress" | "completed";
    activeForm: string;
  }>;
  newTodos: Array<{
    content: string;
    status: "pending" | "in_progress" | "completed";
    activeForm: string;
  }>;
};
```

返回之前和更新的任务列表。

<Note>
  以下工具仅在 Claude 3.x 模型、Opus 4 至 4.7、Sonnet 4 至 4.6 和 Haiku 4.5 上默认可用。在所有其他模型上，包括 Claude Code 无法识别的模型 ID，除非您选择加入，否则它们不可用：

  * `TodoWrite`
  * `TaskCreate`
  * `TaskGet`
  * `TaskUpdate`
  * `TaskList`

  无论工具在何处可用，Claude Code 都提供四个 Task 工具，或者当你设置 `CLAUDE_CODE_ENABLE_TASKS=0` 时改为提供 `TodoWrite`。

  此默认集合适用于 Claude Code v2.1.268 及更高版本，TypeScript Agent SDK 从 v0.3.268 开始捆绑此版本。

  请参阅[模型可用性](/docs/zh-CN/agent-sdk/todo-tracking#model-availability)以选择加入。
</Note>

<h3 id="taskcreate-2">
  TaskCreate
</h3>

**工具名称：** `TaskCreate`

```typescript theme={null}
type TaskCreateOutput = {
  task: {
    id: string;
    subject: string;
  };
};
```

返回创建的任务及其分配的 ID。

<h3 id="taskupdate-2">
  TaskUpdate
</h3>

**工具名称：** `TaskUpdate`

```typescript theme={null}
type TaskUpdateOutput = {
  success: boolean;
  taskId: string;
  updatedFields: string[];
  error?: string;
  statusChange?: {
    from: string;
    to: string;
  };
};
```

返回更新结果，包括哪些字段已更改。

<h3 id="taskget-2">
  TaskGet
</h3>

**工具名称：** `TaskGet`

```typescript theme={null}
type TaskGetOutput = {
  task: {
    id: string;
    subject: string;
    description: string;
    status: "pending" | "in_progress" | "completed";
    blocks: string[];
    blockedBy: string[];
  } | null;
};
```

返回完整的任务记录，或在找不到 ID 时返回 `null`。

<h3 id="tasklist-2">
  TaskList
</h3>

**工具名称：** `TaskList`

```typescript theme={null}
type TaskListOutput = {
  tasks: Array<{
    id: string;
    subject: string;
    status: "pending" | "in_progress" | "completed";
    owner?: string;
    blockedBy: string[];
  }>;
};
```

返回当前列表中所有任务的快照。

<h3 id="exitplanmode-2">
  ExitPlanMode
</h3>

**工具名称：** `ExitPlanMode`

```typescript theme={null}
type ExitPlanModeOutput = {
  plan: string | null;
  isAgent: boolean;
  filePath?: string;
  hasTaskTool?: boolean;
  planWasEdited?: boolean;
  awaitingLeaderApproval?: boolean;
  requestId?: string;
};
```

返回退出规划模式后的计划状态。

<h3 id="listmcpresources-2">
  ListMcpResources
</h3>

**工具名称：** `ListMcpResourcesTool`

```typescript theme={null}
type ListMcpResourcesOutput = Array<{
  uri: string;
  name: string;
  mimeType?: string;
  description?: string;
  server: string;
}>;
```

返回可用 MCP 资源的数组。

<h3 id="readmcpresource-2">
  ReadMcpResource
</h3>

**工具名称：** `ReadMcpResourceTool`

```typescript theme={null}
type ReadMcpResourceOutput = {
  contents: Array<{
    uri: string;
    mimeType?: string;
    text?: string;
    blobSavedTo?: string;
  }>;
  error?: string;
};
```

返回请求的 MCP 资源的内容。

<h3 id="enterworktree-2">
  EnterWorktree
</h3>

**工具名称：** `EnterWorktree`

```typescript theme={null}
type EnterWorktreeOutput = {
  worktreePath: string;
  worktreeBranch?: string;
  message: string;
};
```

返回有关 git worktree 的信息。

<h3 id="exitworktree-2">
  ExitWorktree
</h3>

**工具名称：** `ExitWorktree`

```typescript theme={null}
type ExitWorktreeOutput = {
  action: "keep" | "remove";
  originalCwd: string;
  worktreePath: string;
  worktreeBranch?: string;
  tmuxSessionName?: string;
  discardedFiles?: number;
  discardedCommits?: number;
  message: string;
};
```

返回采取的操作和有关退出的 worktree 的详细信息。

<h3 id="enterplanmode-2">
  EnterPlanMode
</h3>

**工具名称：** `EnterPlanMode`

```typescript theme={null}
type EnterPlanModeOutput = {
  message: string;
};
```

返回进入规划模式的确认。

<h3 id="croncreate-2">
  CronCreate
</h3>

**工具名称：** `CronCreate`

```typescript theme={null}
type CronCreateOutput = {
  id: string;
  humanSchedule: string;
  recurring: boolean;
  durable?: boolean; // true when persisted to .claude/scheduled_tasks.json; false when session-only
};
```

返回作业 ID 和计划的人类可读描述。

<h3 id="crondelete-2">
  CronDelete
</h3>

**工具名称：** `CronDelete`

```typescript theme={null}
type CronDeleteOutput = {
  id: string;
};
```

返回已删除作业的 ID。

<h3 id="cronlist-2">
  CronList
</h3>

**工具名称：** `CronList`

```typescript theme={null}
type CronListOutput = {
  jobs: {
    id: string;
    cron: string;
    humanSchedule: string;
    prompt: string;
    recurring?: boolean;
    durable?: boolean;
  }[];
};
```

返回计划的 cron 作业：来自 `.claude/scheduled_tasks.json` 的持久作业和来自当前会话的仅会话作业。仅会话作业携带 `durable: false`；从磁盘读取的作业省略该字段。

<h3 id="schedulewakeup-2">
  ScheduleWakeup
</h3>

**工具名称：** `ScheduleWakeup`

```typescript theme={null}
type ScheduleWakeupOutput = {
  scheduledFor: number;
  clampedDelaySeconds: number;
  wasClamped: boolean;
  stopped?: boolean;
  cancelledWakeups?: number;
};
```

返回唤醒将触发的时间作为纪元毫秒时间戳、实际使用的延迟以及请求的延迟是否被限制。`stopped` 字段在调用以 `stop: true` 结束循环时为 `true`。它需要 Claude Code v2.1.202 或更高版本。`cancelledWakeups` 字段计算 `stop: true` 调用取消了多少待处理唤醒。值为 0 表示没有待处理，重复 `/loop` cron 不会被 `stop: true` 取消。它需要 Claude Code v2.1.206 或更高版本。

<h3 id="remotetrigger-2">
  RemoteTrigger
</h3>

**工具名称：** `RemoteTrigger`

```typescript theme={null}
type RemoteTriggerOutput = {
  status: number;
  json: string;
  summary?: string;
};
```

返回触发操作的 API 响应状态和正文。

<h3 id="pushnotification-2">
  PushNotification
</h3>

**工具名称：** `PushNotification`

```typescript theme={null}
type PushNotificationOutput = {
  message: string;
  pushSent?: boolean;
  localSent?: boolean;
  disabledReason?: "config_off" | "user_present" | "no_transport";
  sentAt?: string;
};
```

返回传递详细信息，包括是否发送了推送或本地通知以及跳过传递的原因。

<h3 id="reportfindings-2">
  ReportFindings
</h3>

**工具名称：** `ReportFindings`

```typescript theme={null}
type ReportFindingsOutput = {
  count: number;
  level?: "low" | "medium" | "high" | "xhigh" | "max";
  findings: Array<{
    file: string;
    line?: number;
    summary: string;
    failure_scenario: string;
    short_summary?: string;
    category?: string;
    verdict?: "CONFIRMED" | "PLAUSIBLE";
    outcome?: "fixed" | "skipped" | "no_change_needed";
  }>;
};
```

返回报告的发现数、审查运行的工作量级别以及为结果正文回显的发现。需要 Claude Code v2.1.196 或更高版本。回显的 `short_summary` 字段需要 Claude Code v2.1.212 或更高版本。

<h3 id="artifact-2">
  Artifact
</h3>

**工具名称：** `Artifact`

```typescript theme={null}
type ArtifactOutput =
  | {
      url: string;
      path: string;
      title?: string;
      version?: string;
      capabilities?: unknown;
      stored?: {
        contract: string;
        capabilities?: Record<string, unknown>;
      };
      warnings?: string[];
      contract?: string;
      updated?: boolean;
      liveSubscription?: string;
    }
  | {
      artifacts: Array<{
        title: string;
        url: string;
        updatedAt?: string;
        rel?: "mine" | "shared";
      }>;
      truncated?: boolean;
      scope?: "shared" | "all";
    };
```

返回已发布页面的 `url` 和为发布操作发布的本地 `path`，当发布重新部署现有工件时 `updated` 设置为 true，`warnings` 携带任何发布时建议。列表操作返回 `artifacts` 行，当存在比请求限制更多的工件时 `truncated` 设置。在范围不是 `"mine"` 的列表上，每行携带 `rel` 标记用户是否拥有工件或与他们共享，输出的 `scope` 记录哪个非默认范围产生了列表；两者在默认列表上不存在。

<h3 id="projects-2">
  Projects
</h3>

**工具名称：** `Projects`

```typescript theme={null}
type ProjectsOutput =
  | {
      method: "project_info";
      notice?: string;
      name: string;
      description: string;
      instructions: string;
      docs: Array<{ path: string; created_at: string | null }>;
      files?: Array<{
        path: string;
        file_kind: string;
        created_at: string | null;
      }>;
      sync_sources?: Array<{
        type: string | null;
        config: Record<string, unknown>;
      }>;
      knowledge: {
        knowledge_size: number;
        max_knowledge_size: number;
      };
    }
  | {
      method: "project_read";
      notice?: string;
      path: string;
      file_kind?: string;
      content?: string;
      local_file?: string;
      created_at: string | null;
    }
  | {
      method: "project_search";
      notice?: string;
      rag: boolean;
      hits?: Array<{ name?: string; doc_uuid?: string; text?: string }>;
      docs?: string[];
    }
  | {
      method: "project_write";
      notice?: string;
      path: string;
      doc_uuid: string;
      replaced: boolean;
      present_to_user?: boolean;
      local_path?: string;
    }
  | {
      method: "project_delete";
      notice?: string;
      path: string;
      deleted: boolean;
    };
```

在 `method` 字段上进行区分，镜像输入。`project_read` 在 `content` 中内联返回小文本文档，并将较大的文档写入 `local_file` 路径；`project_search` 当项目的索引可用时返回 RAG `hits` 且 `rag: true`，否则回退到 `docs` 路径列表。

<h3 id="readmcpresourcedir-2">
  ReadMcpResourceDir
</h3>

**工具名称：** `ReadMcpResourceDirTool`

```typescript theme={null}
type ReadMcpResourceDirOutput = {
  resources: Array<{
    uri: string;
    name: string;
    mimeType?: string;
  }>;
  error?: string;
};
```

返回目录资源的直接子项。子目录显示为 mimeType `"inode/directory"`；`error` 在服务器无法列出目录时携带人类可读的消息。

<h3 id="refreshmcptools-2">
  RefreshMcpTools
</h3>

**工具名称：** `RefreshMcpTools`

```typescript theme={null}
type RefreshMcpToolsOutput = Array<{
  server: string;
  status: "refreshed" | "error" | "not_connected";
  toolCount?: number; // tools now available from this server
  added?: string[]; // tool names this refresh added
  removed?: string[]; // tool names this refresh removed
  error?: string; // why the refresh failed or the server was unavailable
}>;
```

返回每个服务器一个条目：`refreshed` 表示重新查询的工具列表已应用，`error` 表示重新查询失败且保留了之前的工具集，`not_connected` 表示服务器没有实时连接来查询。

<h3 id="showonboardingrolepicker-2">
  ShowOnboardingRolePicker
</h3>

**工具名称：** `ShowOnboardingRolePicker`

```typescript theme={null}
type ShowOnboardingRolePickerOutput = {
  role?: string;
  dismissed?: boolean;
};
```

返回用户的选择：当他们选择角色芯片或输入一个时为 `role`，当他们关闭选择器时为 `dismissed: true`。空对象表示用户批准了调用而未选择角色。

<h3 id="mcpoutput">
  McpOutput
</h3>

**工具名称：** 形式为 `mcp__<server>__<tool>` 的动态 MCP 工具名称

```typescript theme={null}
type McpOutput =
  | string
  | {
      type: string;
      [k: string]: unknown;
    }[]
  | {
      [k: string]: unknown;
    };
```

MCP 工具结果作为字符串或内容块数组返回，取决于服务器。导出类型中的尾部纯对象分支是架构生成工件：SDK 不返回裸对象，因为服务器的结构化输出在返回前被序列化为 JSON 字符串。在运行时值也可能是 `undefined`，尽管导出的类型不对此建模。

<h2 id="permission-types">
  权限类型
</h2>

<h3 id="permissionupdate">
  `PermissionUpdate`
</h3>

用于更新权限的操作。

```typescript theme={null}
type PermissionUpdate =
  | {
      type: "addRules";
      rules: PermissionRuleValue[];
      behavior: PermissionBehavior;
      destination: PermissionUpdateDestination;
    }
  | {
      type: "replaceRules";
      rules: PermissionRuleValue[];
      behavior: PermissionBehavior;
      destination: PermissionUpdateDestination;
    }
  | {
      type: "removeRules";
      rules: PermissionRuleValue[];
      behavior: PermissionBehavior;
      destination: PermissionUpdateDestination;
    }
  | {
      type: "setMode";
      mode: PermissionMode;
      destination: PermissionUpdateDestination;
    }
  | {
      type: "addDirectories";
      directories: string[];
      destination: PermissionUpdateDestination;
    }
  | {
      type: "removeDirectories";
      directories: string[];
      destination: PermissionUpdateDestination;
    };
```

<h3 id="permissionbehavior">
  `PermissionBehavior`
</h3>

```typescript theme={null}
type PermissionBehavior = "allow" | "deny" | "ask";
```

<h3 id="permissionupdatedestination">
  `PermissionUpdateDestination`
</h3>

```typescript theme={null}
type PermissionUpdateDestination =
  | "userSettings" // 全局用户设置
  | "projectSettings" // 每个目录的项目设置
  | "localSettings" // 本地项目设置
  | "session" // 仅当前会话
  | "cliArg"; // CLI 参数
```

<h3 id="permissionrulevalue">
  `PermissionRuleValue`
</h3>

```typescript theme={null}
type PermissionRuleValue = {
  toolName: string;
  ruleContent?: string;
};
```

<h2 id="other-types">
  其他类型
</h2>

<h3 id="apikeysource">
  `ApiKeySource`
</h3>

会话请求的 API 密钥来源，在 [`SDKSystemMessage`](#sdksystemmessage) 初始化消息上报告为 `apiKeySource`。

```typescript theme={null}
type ApiKeySource =
  | "ANTHROPIC_API_KEY"
  | "apiKeyHelper"
  | "/login managed key"
  | "none"
  | "user"
  | "project"
  | "org"
  | "temporary"
  | "oauth";
```

Claude Code 报告以下四个值之一：

| 值 | 使用中的密钥 |
| - | - |
| `ANTHROPIC_API_KEY` | `ANTHROPIC_API_KEY` 环境变量中的密钥 |
| `apiKeyHelper` | 由您的 [`apiKeyHelper`](/docs/zh-CN/settings-reference#apikeyhelper) 命令返回的密钥 |
| `/login managed key` | Claude Code 在您使用 [Claude Console 账户](/docs/zh-CN/authentication#claude-console-authentication) 登录时存储的密钥 |
| `none` | 没有 API 密钥。会话以其他方式进行身份验证，例如 claude.ai 登录、bearer 令牌或云提供商 |

Agent SDK v0.3.234 及更高版本在类型中列出这四个值。该类型还保留 `user`、`project`、`org`、`temporary` 和 `oauth`，以便旧代码仍能编译，Claude Code 不报告它们。

<h3 id="sdkbeta">
  `SdkBeta`
</h3>

可通过 `betas` 选项启用的可用 beta 功能。有关更多信息，请参阅 [Beta headers](https://platform.claude.com/docs/en/api/beta-headers)。

```typescript theme={null}
type SdkBeta = "context-1m-2025-08-07";
```

<Warning>
  `context-1m-2025-08-07` beta 自 2026 年 4 月 30 日起已停用。使用 Claude Sonnet 4.5 或 Sonnet 4 传递此值无效，超过标准 200k 令牌上下文窗口的请求将返回错误。要使用 1M 令牌上下文窗口，请迁移到 [Claude Opus 5.5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.6、Claude Opus 4.7 或 Claude Opus 4.8](https://platform.claude.com/docs/en/about-claude/models/overview)，这些模型在标准定价下包含 1M 上下文，无需 beta 标头。
</Warning>

<h3 id="slashcommand">
  `SlashCommand`
</h3>

有关可用命令的信息。

```typescript theme={null}
type SlashCommand = {
  name: string;
  description: string;
  argumentHint: string;
  aliases?: string[];
  builtin?: boolean;
};
```

`builtin` 在命令是 Claude Code 自己的命令且输入 `/name` 运行它时为 `true`。对于由用户、项目、plugin 或 MCP 服务器定义的命令，以及由这些命令之一 [按名称替换](/docs/zh-CN/skills#resolve-skills-that-share-a-name) 的捆绑命令，它不存在。需要 Agent SDK v0.3.277 或更高版本。

<h3 id="modelinfo">
  `ModelInfo`
</h3>

有关可用模型的信息。

```typescript theme={null}
type ModelInfo = {
  value: string;
  resolvedModel?: string;
  displayName: string;
  description: string;
  supportsEffort?: boolean;
  supportedEffortLevels?: ("low" | "medium" | "high" | "xhigh" | "max")[];
  supportsAdaptiveThinking?: boolean;
  supportsFastMode?: boolean;
  supportsAutoMode?: boolean;
};
```

| 字段 | 类型 | 描述 |
| :- | :- | :- |
| `value` | `string` | 在 API 调用中传递的模型标识符 |
| `resolvedModel` | `string \| undefined` | 此条目的 `value` 解析到的规范线路模型 ID。别名条目（如 `sonnet`）解析为显式模型 ID（如 `claude-sonnet-5`），因此主机可以将存储的显式模型 ID 与覆盖它的别名条目匹配。需要 Claude Code v2.1.197 或更高版本。 |
| `displayName` | `string` | 人类可读的显示名称 |
| `description` | `string` | 模型功能的描述 |
| `supportsEffort` | `boolean \| undefined` | 此模型是否支持努力级别 |
| `supportedEffortLevels` | `("low" \| "medium" \| "high" \| "xhigh" \| "max")[] \| undefined` | 此模型接受的努力级别 |
| `supportsAdaptiveThinking` | `boolean \| undefined` | 此模型是否支持自适应思考，其中 Claude 决定何时以及思考多少 |
| `supportsFastMode` | `boolean \| undefined` | 此模型是否支持快速模式 |
| `supportsAutoMode` | `boolean \| undefined` | 此模型是否支持自动模式 |

<h3 id="agentinfo">
  `AgentInfo`
</h3>

有关可通过 Agent 工具调用的可用子代理的信息。

```typescript theme={null}
type AgentInfo = {
  name: string;
  description: string;
  model?: string;
};
```

| 字段 | 类型 | 描述 |
| :- | :- | :- |
| `name` | `string` | 代理类型标识符（例如 `"Explore"`、`"general-purpose"`） |
| `description` | `string` | 何时使用此代理的描述 |
| `model` | `string \| undefined` | 此代理使用的模型：别名或模型 ID，或 `'inherit'` 表示父级的模型。当为 `undefined` 时，Claude Code 选择 [子代理模型顺序](/docs/zh-CN/sub-agents#choose-a-model) 中的模型 |

<h3 id="mcpserverprovenance">
  `McpServerProvenance`
</h3>

提供 `mcp__*` 工具的 MCP 服务器，以及该服务器定义的来源。[`PreToolUse`](#pretoolusehookinput)、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest` 和 `PermissionDenied` 钩子输入将其作为 `mcp_server` 携带，[`CanUseTool`](#canusetool) 选项将其作为 `mcpServer` 携带。对于不来自 MCP 服务器的工具，两者都省略它。

```typescript theme={null}
type McpServerProvenance = {
  name: string;
  source: string;
};
```

| 字段 | 类型 | 描述 |
| :- | :- | :- |
| `name` | `string` | 服务器注册时使用的名称，与 [`mcpServerStatus()`](#query-object) 为其报告的值相同 |
| `source` | `string` | 服务器定义的来源：`sdk`、`plugin` 或配置范围 |

`source` 采用以下值之一。该集合是开放的，因此将您不认识的值视为配置的来源，而不是 `sdk`：

* **`sdk`**：您的应用程序注册的进程内服务器。只有 SDK 主机应用程序可以注册一个，因此配置的服务器永远不会报告 `sdk`，无论其名称如何。
* **`plugin`**：[plugin](/docs/zh-CN/agent-sdk/plugins) 提供的服务器。其 `name` 是 [plugin-provided MCP servers](/docs/zh-CN/mcp#plugin-provided-mcp-servers) 下描述的作用域 `plugin:<plugin-name>:<server-name>` 形式。
* **配置范围**：`user`、`project`、`local`、`dynamic`、`managed`、`enterprise`、`claudeai` 或 `agent`。`.mcp.json` 服务器报告 `project`，[MCP installation scopes](/docs/zh-CN/mcp#mcp-installation-scopes) 定义 `local`、`project` 和 `user`。您的应用程序在 [`mcpServers` 选项](#options) 中传递的服务器（除了进程内 SDK 服务器外）报告 `dynamic`。

基于 `source` 做出信任决策，而不是基于 `name` 或 `mcp__<server>__` 工具名称前缀。对于除 `sdk` 之外的任何来源，`name` 是不受信任的文本：在显示前对其进行转义。

`McpServerProvenance` 和携带它的字段需要 Agent SDK v0.3.274 或更高版本。

<h3 id="mcpserverstatus">
  `McpServerStatus`
</h3>

连接的 MCP 服务器的状态。

```typescript theme={null}
type McpServerStatus = {
  name: string;
  status: "connected" | "failed" | "needs-auth" | "pending" | "disabled";
  serverInfo?: {
    name: string;
    version: string;
  };
  error?: string;
  config?: McpServerStatusConfig;
  scope?: string;
  source?: string;
  tools?: {
    name: string;
    description?: string;
    annotations?: {
      readOnly?: boolean;
      destructive?: boolean;
      openWorld?: boolean;
    };
    _meta?: Record<string, unknown>;
  }[];
};
```

`source` 说明服务器定义的来源，具有与 [`McpServerProvenance`](#mcpserverprovenance) 的 `source` 相同的值和信任规则。该字段需要 Agent SDK v0.3.274 或更高版本，在早期版本中不存在。

`_meta` 在 `tools` 条目上携带该工具的 `_meta` 的 MCP Apps 成员，因此您的应用程序可以找到 `ui://` 资源以使用 [`readMcpResource()`](#query-object) 呈现。Claude Code 传递 `ui` 对象和已弃用的平面 `ui/resourceUri` 字符串，并保留所有其他密钥。在 `ui` 内，`resourceUri` 是 `ui://` 字符串，`visibility` 是当服务器设置它们时的 `"model"` 和 `"app"` 数组，任何其他成员原样传递。Claude Code 在值格式不正确时删除任一密钥，并从既不声明任何一个的工具中省略 `_meta`。该字段仅在初始化消息的 [`capabilities`](#sdksystemmessage) 包含 `mcp_tool_ui_meta_v1` 时出现，并需要 TypeScript Agent SDK v0.3.280 或更高版本。

<h3 id="mcpserverstatusconfig">
  `McpServerStatusConfig`
</h3>

MCP 服务器的配置，由 `mcpServerStatus()` 报告。这是所有 MCP 服务器传输类型的并集。

```typescript theme={null}
type McpServerStatusConfig =
  | McpStdioServerConfig
  | McpSSEServerConfig
  | McpHttpServerConfig
  | McpSdkServerConfig
  | McpClaudeAIProxyServerConfig;
```

有关每种传输类型的详细信息，请参阅 [`McpServerConfig`](#mcpserverconfig)。

<h3 id="accountinfo">
  `AccountInfo`
</h3>

经过身份验证的用户的账户信息。

```typescript theme={null}
type AccountInfo = {
  email?: string;
  organization?: string;
  subscriptionType?: string;
  tokenSource?: string;
  apiKeySource?: string;
};
```

<h3 id="modelusage">
  `ModelUsage`
</h3>

在结果消息中返回的每个模型的使用统计信息。`costUSD` 值是客户端估计。有关计费注意事项，请参阅 [Track cost and usage](/docs/zh-CN/agent-sdk/cost-tracking)。

```typescript theme={null}
type ModelUsage = {
  inputTokens: number;
  outputTokens: number;
  thinkingTokens?: number;
  cacheReadInputTokens: number;
  cacheCreationInputTokens: number;
  webSearchRequests: number;
  costUSD: number;
  contextWindow: number;
  maxOutputTokens: number;
  canonicalModel?: string;
  provider?: string;
  costBasis?: 'list' | 'managed' | 'unknown';
};
```

`thinkingTokens` 计算此模型生成的思考令牌。`outputTokens` 已包含它们，因此不要将两者相加。该字段在运行在记录它的 Claude Code 版本上的轮次之前不存在，因此在早期版本上开始的已恢复会话报告部分计数。`thinkingTokens` 需要 Agent SDK v0.3.257 或更高版本。

`canonicalModel` 和 `provider` 字段需要 Claude Code v2.1.218 或更高版本。`canonicalModel` 是定价查询使用的规范模型 ID；它可能与键入条目的原始模型字符串不同，例如当该字符串是提供商特定的 ID 或别名时。

`provider` 命名提供模型的 API 后端，例如 `firstParty`、`bedrock`、`vertex`、`foundry`、`anthropicAws`、`mantle` 或 `gateway`。

`costBasis` 命名为模型最新请求定价的价格表：`list` 表示列表价格，`managed` 表示 [`modelPricing`](/docs/zh-CN/settings-reference#modelpricing) 表，或 `unknown` 表示两者都不匹配模型 ID。该字段需要 Claude Code v2.1.246 或更高版本。

<h3 id="configscope">
  `ConfigScope`
</h3>

```typescript theme={null}
type ConfigScope = "local" | "user" | "project";
```

<h3 id="nonnullableusage">
  `NonNullableUsage`
</h3>

[`Usage`](#usage) 的一个版本，所有可空字段都变为非可空。

```typescript theme={null}
type NonNullableUsage = {
  [K in keyof Usage]: NonNullable<Usage[K]>;
};
```

<h3 id="usage">
  `Usage`
</h3>

令牌使用统计信息。这是来自 `@anthropic-ai/sdk` 的 `BetaUsage` 类型。

```typescript theme={null}
type Usage = {
  input_tokens: number;
  output_tokens: number;
  cache_creation_input_tokens: number | null;
  cache_read_input_tokens: number | null;
  cache_creation: {
    ephemeral_5m_input_tokens: number;
    ephemeral_1h_input_tokens: number;
  } | null;
  server_tool_use: BetaServerToolUsage | null;
  service_tier: "standard" | "priority" | "batch" | null;
  speed: "standard" | "fast" | null;
  inference_geo: string | null;
  iterations: BetaIterationsUsage | null;
  output_tokens_details: BetaOutputTokensDetails | null;
};
```

`BetaServerToolUsage`、`BetaIterationsUsage` 和 `BetaOutputTokensDetails` 在 `@anthropic-ai/sdk` 中定义。

`output_tokens_details` 按类别分解计费输出。它目前携带一个字段 `thinking_tokens: number`，计算模型生成的作为内部推理的输出令牌，包括思考块分隔符。`output_tokens_details` 字段需要 TypeScript SDK v0.3.228 或更高版本，它捆绑了 Claude Code v2.1.228。

* **计费**：读取分解以进行观察，而不是用于计费。`output_tokens` 保持为权威总数，`output_tokens - thinking_tokens` 近似非推理输出。
* **计数涵盖的内容**：模型生成的原始推理，可能比响应体中返回的思考文本更长。API 通过重新标记该原始文本来计算它，因此它可能与模型的精确生成计数相差几个令牌。
* **流式传输**：在流式助手消息上，此分解与 `output_tokens` 一样是 `message_start` 占位符，不携带真实计数，因此从结果消息的 `usage` 读取它，如 [Read output tokens from the result message](/docs/zh-CN/agent-sdk/cost-tracking#read-output-tokens-from-the-result-message) 所述。在结果消息上，当模型或提供商不报告分解时，`thinking_tokens` 读取 `0`。
* **`null` 情况**：`output_tokens_details` 本身在 Claude Code 合成的助手消息上为 `null`，例如 API 错误消息。

<h3 id="calltoolresult">
  `CallToolResult`
</h3>

MCP 工具结果类型（来自 `@modelcontextprotocol/sdk/types.js`）。`structuredContent` 是可与 `content` 一起返回的 JSON 对象，包括图像块。请参阅 [Return structured data](/docs/zh-CN/agent-sdk/custom-tools#return-structured-data)。

```typescript theme={null}
type CallToolResult = {
  content: Array<{
    type: "text" | "image" | "audio" | "resource" | "resource_link";
    // Additional fields vary by type
  }>;
  structuredContent?: Record<string, unknown>;
  isError?: boolean;
};
```

<h3 id="sdkmcpresourcelink">
  `SDKMcpResourceLink`
</h3>

MCP 工具通过引用返回的一个文件。Claude Code 从工具结果中的 `resource_link` 块构建每个条目，并将列表作为 `resourceLinks` 在 [`SDKUserMessage.tool_use_result`](#sdkusermessage) 上传递，或在后台完成调用时作为 `resource_links` 在 [`SDKTaskNotificationMessage`](#sdktasknotificationmessage) 上传递。需要 Agent SDK v0.3.257 或更高版本。

```typescript theme={null}
type SDKMcpResourceLink = {
  uri: string;
  name: string;
  title?: string;
  description?: string;
  mimeType?: string;
  size?: number;
  annotations?: Record<string, unknown>;
};
```

Claude Code 丢弃其 `uri` 或 `name` 不是字符串的块，并省略其值不是列出的类型的可选字段。

| 字段 | 类型 | 描述 |
| :- | :- | :- |
| `uri` | `string` | 资源的 URI，如服务器返回的那样 |
| `name` | `string` | 服务器给资源的名称 |
| `title` | `string \| undefined` | 显示标题，当服务器设置了一个时 |
| `description` | `string \| undefined` | 描述，当服务器设置了一个时 |
| `mimeType` | `string \| undefined` | MIME 类型，当服务器设置了一个时 |
| `size` | `number \| undefined` | 大小（以字节为单位），当服务器设置了一个时 |
| `annotations` | `Record<string, unknown> \| undefined` | 块的 MCP 注释对象，当服务器设置了一个时 |

<h3 id="thinkingconfig">
  `ThinkingConfig`
</h3>

控制 Claude 的思考/推理行为。优先于已弃用的 `maxThinkingTokens`。

```typescript theme={null}
type ThinkingDisplay = "summarized" | "omitted";

type ThinkingConfig =
  | { type: "adaptive"; display?: ThinkingDisplay } // The model determines when and how much to reason (Opus 4.6+)
  | { type: "enabled"; budgetTokens?: number; display?: ThinkingDisplay } // Fixed thinking token budget
  | { type: "disabled" }; // No extended thinking
```

可选的 `display` 字段控制思考文本是否返回为 `"summarized"` 或 `"omitted"`。在 Claude Opus 4.7 及更高版本上，API 默认值为 `"omitted"`，因此设置 `"summarized"` 以在 `thinking` 块中接收思考内容。Claude Code 不向 Amazon Bedrock 或 Google Cloud 的 Agent Platform 发送 `display`，因此在这些提供商上，Opus 4.7 及更高版本即使在您将 `display` 设置为 `"summarized"` 时也返回空 `thinking` 块。

<h3 id="spawnedprocess">
  `SpawnedProcess`
</h3>

自定义进程生成的接口（与 `spawnClaudeCodeProcess` 选项一起使用）。`ChildProcess` 已满足此接口。

```typescript theme={null}
interface SpawnedProcess {
  stdin: Writable;
  stdout: Readable;
  readonly killed: boolean;
  readonly exitCode: number | null;
  kill(signal: NodeJS.Signals): boolean;
  on(
    event: "exit",
    listener: (code: number | null, signal: NodeJS.Signals | null) => void
  ): void;
  on(event: "error", listener: (error: Error) => void): void;
  once(
    event: "exit",
    listener: (code: number | null, signal: NodeJS.Signals | null) => void
  ): void;
  once(event: "error", listener: (error: Error) => void): void;
  off(
    event: "exit",
    listener: (code: number | null, signal: NodeJS.Signals | null) => void
  ): void;
  off(event: "error", listener: (error: Error) => void): void;
}
```

<h3 id="spawnoptions">
  `SpawnOptions`
</h3>

传递给自定义生成函数的选项。

```typescript theme={null}
interface SpawnOptions {
  command: string;
  args: string[];
  cwd?: string;
  env: Record<string, string | undefined>;
  signal: AbortSignal;
}
```

<Note>
  `signal` 字段告诉您的生成函数何时拆除进程。将其作为 `signal` 选项传递给 Node 的 `spawn()`，或将其传递给您的 VM 或容器拆除处理程序。

  此信号不会在 [`Options.abortController`](#options) 中止时立即触发。SDK 首先关闭进程的 stdin 并等待约两秒，以便 CLI 可以干净地关闭，然后中止此信号。要在调用者中止时立即做出反应，请侦听您自己的 `Options.abortController.signal`，您的生成函数可以从其封闭范围引用。
</Note>

<h3 id="mcpsetserversresult">
  `McpSetServersResult`
</h3>

`setMcpServers()` 操作的结果。

```typescript theme={null}
type McpSetServersResult = {
  added: string[];
  removed: string[];
  errors: Record<string, string>;
};
```

当您调用 `setMcpServers()` 时，Claude Code 应用这些规则：

* **调用未命名的服务器**：Claude Code 保持 plugin 提供的服务器运行。需要 Agent SDK v0.3.210 或更高版本。
* **调用命名的服务器**：除了 CLI 在启动时启动的内置服务器外，Claude Code 仅在其配置与您传递的配置不同时才替换运行中的服务器。
* **CLI 在启动时启动的内置服务器**：如果调用命名了一个，Claude Code 会删除该条目并在 `errors` 中报告它。

承诺在新添加的 stdio、HTTP 和 SSE 服务器连接或失败后解决，因此来自已连接服务器的工具在下一轮可用。

`added` 列出 Claude Code 添加或替换的服务器，无论它们是否连接。连接失败的服务器同时出现在 `added` 和 `errors` 中，`errors` 下有失败文本，[`mcpServerStatus()`](#methods) 中有 `failed` 行。在 Claude Code v2.1.257 之前，连接尝试抛出的服务器仅在 `errors` 下报告。

<h3 id="rewindfilesresult">
  `RewindFilesResult`
</h3>

`rewindFiles()` 操作的结果。

```typescript theme={null}
type RewindFilesResult = {
  canRewind: boolean;
  error?: string;
  filesChanged?: string[];
  insertions?: number;
  deletions?: number;
  skippedLinks?: number;
};
```

`skippedLinks` 计算倒带拒绝恢复或删除以确保链接安全的跟踪路径：跟踪路径处的符号链接、硬链接或其他非常规文件，不再解析为检查点时指向的位置的父目录，或无法安全读取的备份。该字段需要 Claude Code v2.1.216 或更高版本。使用 `rewindFiles(userMessageId, { dryRun: true })` 的预览调用永远不会设置它。

<h3 id="sdkstatusmessage">
  `SDKStatusMessage`
</h3>

状态更新消息（例如压缩）。

```typescript theme={null}
type SDKStatusMessage = {
  type: "system";
  subtype: "status";
  status: "compacting" | null;
  permissionMode?: PermissionMode;
  uuid: UUID;
  session_id: string;
};
```

<h3 id="sdktasknotificationmessage">
  `SDKTaskNotificationMessage`
</h3>

后台任务完成、失败或停止时的通知。后台任务包括 `run_in_background` Bash 命令、[Monitor](#monitor) 监视和后台子代理。对于 `ambient` 字段，请参阅 [`SDKTaskStartedMessage`](#sdktaskstartedmessage)，它定义了它和它的版本要求。

```typescript theme={null}
type SDKTaskNotificationMessage = {
  type: "system";
  subtype: "task_notification";
  task_id: string;
  tool_use_id?: string;
  status: "completed" | "failed" | "stopped";
  output_file: string;
  summary: string;
  ambient?: boolean;
  usage?: {
    total_tokens: number;
    tool_uses: number;
    duration_ms: number;
  };
  resource_links?: SDKMcpResourceLink[];
  uuid: UUID;
  session_id: string;
};
```

当 Claude Code [将长 MCP 工具调用移到后台](/docs/zh-CN/mcp#automatic-backgrounding-of-long-tool-calls) 时，该调用的 `tool_result` 块仅保存占位符，调用的真实结果在此通知中到达。使用 `tool_use_id` 将通知与调用匹配。在 `completed` 通知上，`resource_links` 列出工具通过引用返回的文件，作为 [`SDKMcpResourceLink`](#sdkmcpresourcelink) 条目，具有与 [`tool_use_result.resourceLinks`](#sdkusermessage) 相同的 50 链接和 64 KiB 限制。Claude Code 在结果没有链接时省略 `resource_links`，以及在不是 MCP 工具调用的任务的通知上。`resource_links` 需要 Agent SDK v0.3.257 或更高版本。

Claude Code 在发送给模型的每个任务通知前面加上通知，除了带有 [`scheduled-trigger` subkind](#task-notification-subkinds) 戳记的通知外，它们改为携带分配任务框架。通知说明没有发生人类输入，因此模型不会将通知视为用户指令或批准。

要检测任务通知轮次，请在 [`SDKUserMessage`](#sdkusermessage) 或 [`SDKResultMessage`](#sdkresultmessage) 上检查 `origin.kind === "task-notification"`，而不是匹配通知文本。如果您需要知道是什么引发了它，请从同一字段读取 `subkind`。在 v2.1.205 之前，Claude Code 在会话空闲时到达的通知上省略了通知。

<h3 id="sdktoolusesummarymessage">
  `SDKToolUseSummaryMessage`
</h3>

对话中工具使用的摘要。

```typescript theme={null}
type SDKToolUseSummaryMessage = {
  type: "tool_use_summary";
  summary: string;
  preceding_tool_use_ids: string[];
  uuid: UUID;
  session_id: string;
};
```

<h3 id="sdkhookstartedmessage">
  `SDKHookStartedMessage`
</h3>

在钩子开始执行时发出。

Claude Code 将此消息、[`SDKHookProgressMessage`](#sdkhookprogressmessage) 和 [`SDKHookResponseMessage`](#sdkhookresponsemessage) 立即传递到消息流，包括在会话启动期间 `SessionStart` 或 `Setup` 钩子仍在运行时。Claude Code v2.1.169 至 v2.1.203 在 `SessionStart` 或 `Setup` 钩子完成后分批传递这些消息；v2.1.204 恢复了实时传递。

```typescript theme={null}
type SDKHookStartedMessage = {
  type: "system";
  subtype: "hook_started";
  hook_id: string;
  hook_name: string;
  hook_event: string;
  uuid: UUID;
  session_id: string;
};
```

<h3 id="sdkhookprogressmessage">
  `SDKHookProgressMessage`
</h3>

在钩子运行时发出，带有 stdout/stderr 输出。

```typescript theme={null}
type SDKHookProgressMessage = {
  type: "system";
  subtype: "hook_progress";
  hook_id: string;
  hook_name: string;
  hook_event: string;
  stdout: string;
  stderr: string;
  output: string;
  uuid: UUID;
  session_id: string;
};
```

<h3 id="sdkhookresponsemessage">
  `SDKHookResponseMessage`
</h3>

在钩子完成执行时发出。

```typescript theme={null}
type SDKHookResponseMessage = {
  type: "system";
  subtype: "hook_response";
  hook_id: string;
  hook_name: string;
  hook_event: string;
  output: string;
  stdout: string;
  stderr: string;
  exit_code?: number;
  outcome: "success" | "error" | "cancelled";
  uuid: UUID;
  session_id: string;
};
```

<h3 id="sdktoolprogressmessage">
  `SDKToolProgressMessage`
</h3>

在工具执行时定期发出，以指示进度。

```typescript theme={null}
type SDKToolProgressMessage = {
  type: "tool_progress";
  tool_use_id: string;
  tool_name: string;
  parent_tool_use_id: string | null;
  elapsed_time_seconds: number;
  task_id?: string;
  heartbeat?: boolean;
  subagent_type?: string;
  subagent_retry?: {
    agent_id: string;
    attempt: number;
    max_retries: number;
    retry_delay_ms: number;
    error_status: number | null;
    error_category: string;
  };
  uuid: UUID;
  session_id: string;
};
```

当工具调用在主对话中运行时，Claude Code 每 30 秒发出一条 `tool_progress` 消息，带有 `heartbeat: true`。每个心跳携带工具名称和经过的秒数，因此您可以区分长时间运行的调用和停滞的会话。Claude Code 不为子代理内的工具调用发出心跳。`heartbeat` 字段需要 Agent SDK v0.3.214 或更高版本。在 v2.1.257 之前，Claude Code 也不为前台 Agent 工具调用发出心跳。

在除心跳外的 Agent 工具的 `tool_progress` 消息上，`subagent_type` 命名运行中的子代理类型，例如 `general-purpose`。`subagent_retry` 在该子代理等待 API 错误退避（例如速率限制或过载）时出现，每次重试尝试一条消息。两个字段都需要 Agent SDK v0.3.214 或更高版本。

要从 `subagent_retry` 呈现重试指示器：

* 按 `parent_tool_use_id` 跟踪指示器，这对每个子代理是唯一的。`tool_use_id` 由来自一个助手轮次的并行子代理共享，因此按它跟踪会让一个子代理的更新清除另一个的指示器。
* 当同一 `parent_tool_use_id` 的后续 `tool_progress` 到达时清除指示器，既不带 `subagent_retry` 也不带 `heartbeat: true`，或当工具的结果消息到达时。带 `heartbeat: true` 的帧仅报告活跃性，因此在一个到达时保持指示器。`attempt` 可能在持续重试下超过 `max_retries`，因此不要从计数器派生清除。
* 将 `error_category` 视为选择您自己的消息文本的令牌，而不是显示文本。值为 `rate_limit`、`overloaded`、`authentication_failed`、`server_error`、`cloud_credential_error` 和 `unknown`。处理您不认识的值的方式与处理 `unknown` 的方式相同，因为后续版本可以添加值。

<h3 id="sdkauthstatusmessage">
  `SDKAuthStatusMessage`
</h3>

在身份验证流期间发出。

```typescript theme={null}
type SDKAuthStatusMessage = {
  type: "auth_status";
  isAuthenticating: boolean;
  output: string[];
  error?: string;
  uuid: UUID;
  session_id: string;
};
```

<h3 id="sdktaskstartedmessage">
  `SDKTaskStartedMessage`
</h3>

在任务开始时发出。`task_type` 字段对于 Bash 命令和 [Monitor](#monitor) 监视为 `"local_bash"`，对于子代理为 `"local_agent"`，或 `"remote_agent"`。

```typescript theme={null}
type SDKTaskStartedMessage = {
  type: "system";
  subtype: "task_started";
  task_id: string;
  tool_use_id?: string;
  description: string;
  task_type?: string;
  is_backgrounded?: boolean;
  spawn_depth?: number;
  ambient?: boolean;
  uuid: UUID;
  session_id: string;
};
```

`ambient` 对于不是会话工作一部分的任务为 `true`，例如 Claude Code 为其自己的操作运行的任务。实时更新监视器也是环境的，包括用户要求的监视器。从活动指示器中排除环境任务。该字段需要 Agent SDK v0.3.247 或更高版本。

`ambient` 也出现在 [`SDKTaskNotificationMessage`](#sdktasknotificationmessage) 和 [`SDKBackgroundTasksChangedMessage`](#sdkbackgroundtaskschangedmessage) 条目上。

`is_backgrounded` 和 `spawn_depth` 描述 Claude Code 如何启动任务。两个字段都需要 Agent SDK v0.3.238 或更高版本。

* `is_backgrounded`：Claude Code 在 `"local_agent"` 和 `"local_bash"` 任务上设置它。`true` 表示任务在后台运行。`false` 表示任务在前台运行，启动它的工具调用保持阻止，直到任务完成或移到后台。
* `spawn_depth`：Claude Code 仅在 `"local_agent"` 任务上设置它。主线程生成的子代理的深度为 `1`。深度 `1` 子代理生成的子代理的深度为 `2`，以此类推。

[已恢复的子代理](/docs/zh-CN/agent-sdk/subagents#resume-subagents) 始终报告 `is_backgrounded: true`，因为 Claude Code 在后台运行每个已恢复的子代理。当前台任务稍后移到后台时，Claude Code 在 [`task_updated`](#sdktaskupdatedmessage) 消息中报告新的 `is_backgrounded` 值，而不是发送第二个 `task_started`。

<h3 id="sdktaskprogressmessage">
  `SDKTaskProgressMessage`
</h3>

在子代理或后台任务运行时定期发出。对于子代理任务，`summary` 字段仅在启用 [`agentProgressSummaries`](#options) 时填充。对于 [backgrounded MCP tool call](/docs/zh-CN/mcp#automatic-backgrounding-of-long-tool-calls)，`summary` 携带 MCP 服务器的最新报告进度，不依赖于该选项。

```typescript theme={null}
type SDKTaskProgressMessage = {
  type: "system";
  subtype: "task_progress";
  task_id: string;
  tool_use_id?: string;
  description: string;
  subagent_type?: string;
  usage: {
    total_tokens: number;
    tool_uses: number;
    duration_ms: number;
  };
  last_tool_name?: string;
  summary?: string;
  uuid: UUID;
  session_id: string;
};
```

<h3 id="sdktaskupdatedmessage">
  `SDKTaskUpdatedMessage`
</h3>

在后台任务的状态更改时发出，例如当它从 `running` 转换为 `completed` 时。将 `patch` 合并到由 `task_id` 键入的本地任务映射中。`end_time` 字段是 Unix 纪元时间戳（以毫秒为单位），可与 `Date.now()` 比较。

```typescript theme={null}
type SDKTaskUpdatedMessage = {
  type: "system";
  subtype: "task_updated";
  task_id: string;
  patch: {
    status?: "pending" | "running" | "completed" | "failed" | "killed";
    description?: string;
    end_time?: number;
    total_paused_ms?: number;
    error?: string;
    is_backgrounded?: boolean;
  };
  uuid: UUID;
  session_id: string;
};
```

<h3 id="sdkbackgroundtaskschangedmessage">
  `SDKBackgroundTasksChangedMessage`
</h3>

每当实时后台任务集更改时发出：任务启动、完成、被杀死、前台代理被后台化，或任务的 `description` 或 `ambient` 字段更改。

`tasks` 数组是完整的实时集。用每个有效负载替换任何缓存的集，而不是配对 `task_started` 和 `task_notification` 事件，以便下一个成员资格更改纠正您错过的任何事件。

相对于这些每任务事件的顺序是未指定的，因此不要关联两个流。

启动时不发出任何内容。每当会话的 CLI 进程启动或重新启动时重置为空集，并让下一个成员资格更改重新填充它。

当您向运行中的会话发送重复的 `initialize` 控制请求时，例如在传输间隙后使用 [`reinitialize()`](#query-object)，Claude Code 在响应后跟随当前实时集的快照，即使它为空。因此，重新连接的主机可以了解正在运行的内容，而无需等待下一个成员资格更改。在 Agent SDK v0.3.239 之前，Claude Code 在重复的 `initialize` 后不发送快照。

需要 Claude Code v2.1.203 或更高版本。

```typescript theme={null}
type SDKBackgroundTasksChangedMessage = {
  type: "system";
  subtype: "background_tasks_changed";
  tasks: {
    task_id: string;
    task_type: string;
    description: string;
    ambient?: boolean;
  }[];
  uuid: UUID;
  session_id: string;
};
```

<h3 id="sdkthinkingtokensmessage">
  `SDKThinkingTokensMessage`
</h3>

在 Claude 生成思考块时发出，包括编辑过的块。`estimated_tokens` 是当前块中迄今为止生成的思考令牌的运行估计，`estimated_tokens_delta` 是此帧携带的增量。使用这些估计进行进度显示。

当模型或提供商报告分解时，顶级代理循环的最终计数是结果消息的 [`usage.output_tokens_details.thinking_tokens`](#usage)，它 [不包括子代理令牌](/docs/zh-CN/agent-sdk/cost-tracking#get-the-total-cost-of-a-query)。

需要 Claude Code v2.1.153 或更高版本。

```typescript theme={null}
type SDKThinkingTokensMessage = {
  type: "system";
  subtype: "thinking_tokens";
  estimated_tokens: number;
  estimated_tokens_delta: number;
  user_message_uuid?: string;
  uuid: UUID;
  session_id: string;
};
```

<h3 id="sdkfilespersistedevent">
  `SDKFilesPersistedEvent`
</h3>

在文件检查点持久化到磁盘时发出。

```typescript theme={null}
type SDKFilesPersistedEvent = {
  type: "system";
  subtype: "files_persisted";
  files: { filename: string; file_id: string }[];
  failed: { filename: string; error: string }[];
  processed_at: string;
  uuid: UUID;
  session_id: string;
};
```

<h3 id="sdkratelimitevent">
  `SDKRateLimitEvent`
</h3>

当会话遇到速率限制时发出。

```typescript theme={null}
type SDKRateLimitEvent = {
  type: "rate_limit_event";
  rate_limit_info: {
    status: "allowed" | "allowed_warning" | "rejected";
    resetsAt?: number;
    utilization?: number;
    errorCode?: "credits_required";
    canUserPurchaseCredits?: boolean;
    hasChargeableSavedPaymentMethod?: boolean;
  };
  uuid: UUID;
  session_id: string;
};
```

当 `errorCode` 为 `"credits_required"` 时，拒绝来自 claude.ai 订阅，其包含的使用已耗尽，会话在用户购买使用额度之前无法继续。`canUserPurchaseCredits` 指示经过身份验证的用户是否可以为账户购买额度，`hasChargeableSavedPaymentMethod` 指示是否有保存的付款方式在文件中。所有三个字段在不是额度必需拒绝的速率限制事件上不存在。需要 Claude Code v2.1.181 或更高版本。

<h3 id="sdklocalcommandoutputmessage">
  `SDKLocalCommandOutputMessage`
</h3>

Claude Code 不发出此消息类型。当您发送命令（如 `/context` 或 `/usage`）作为提示时，其输出作为 [`SDKAssistantMessage`](#sdkassistantmessage) 到达。

```typescript theme={null}
type SDKLocalCommandOutputMessage = {
  type: "system";
  subtype: "local_command_output";
  content: string;
  uuid: UUID;
  session_id: string;
};
```

<h3 id="sdkcommandschangedmessage">
  `SDKCommandsChangedMessage`
</h3>

当可用命令集在会话中期更改时发出，例如当 Claude Code 在代理进入子目录时发现技能时。`commands` 数组是完整的更新列表，因此用此有效负载替换任何缓存的命令列表。在此消息后调用 [`supportedCommands()`](#query-object) 返回相同的更新列表，因为该方法跟踪最新推送；这需要 Agent SDK v0.3.216 或更高版本。在早期 SDK 版本中，`supportedCommands()` 返回在初始化时捕获的快照，永远不会反映会话中期的更改。

Claude Code 也在 MCP 服务器的 [prompts](/docs/zh-CN/mcp#use-mcp-prompts-as-commands) 加入或离开列表时发出此消息，例如当服务器在会话启动后完成连接时。这需要 Claude Code v2.1.281 或更高版本。

```typescript theme={null}
type SDKCommandsChangedMessage = {
  type: "system";
  subtype: "commands_changed";
  commands: SlashCommand[];
  uuid: UUID;
  session_id: string;
};
```

<h3 id="sdkpromptsuggestionmessage">
  `SDKPromptSuggestionMessage`
</h3>

在启用 [`promptSuggestions`](#options) 且 Claude Code 为该轮生成建议时，在轮次后发出。包含预测的下一个用户提示。对于未获得任何建议的轮次，请参阅 [When Claude Code skips suggestions](/docs/zh-CN/interactive-mode#when-claude-code-skips-suggestions)。

```typescript theme={null}
type SDKPromptSuggestionMessage = {
  type: "prompt_suggestion";
  suggestion: string;
  uuid: UUID;
  session_id: string;
};
```

<h3 id="sdkconversationresetmessage">
  `SDKConversationResetMessage`
</h3>

在会话的对话被替换而不结束会话时发出。在 `query()` 调用中，只有 `/clear` 及其别名产生此消息。在 `new_conversation_id` 下挂载空成绩单并丢弃任何缓存的会话标题。

```typescript theme={null}
type SDKConversationResetMessage = {
  type: "conversation_reset";
  new_conversation_id: UUID;
  uuid: UUID;
  session_id: string;
  trigger?: "clear" | "plan_mode_exit" | "fresh_session" | "onboarding";
  user_message_uuid?: string;
  timestamp?: string;
};
```

可选字段描述重置：

* `trigger`：什么丢弃了对话。在每个 `conversation_reset` 消息上重置您的成绩单，包括此字段不存在或携带您不认识的值的消息。
* `user_message_uuid`：携带 `/clear` 的用户消息的 `uuid`。使用它将重置与该消息匹配。
* `timestamp`：重置发生的时间，作为 UTC 中的 ISO 8601 字符串。使用它进行显示，而不是用于排序消息。

`trigger`、`user_message_uuid` 和 `timestamp` 字段需要 Claude Code v2.1.281 或更高版本。

SDK 的已发布类型在 Claude Code v2.1.203 及更高版本中声明 `SDKConversationResetMessage`。在 v2.1.203 之前，`SDKMessage` 引用了该类型而不声明它，因此当 `skipLibCheck` 被禁用时，在 `type === "conversation_reset"` 上缩小范围失败类型检查。

<h3 id="aborterror">
  `AbortError`
</h3>

中止操作的自定义错误类。

```typescript theme={null}
class AbortError extends Error {}
```

`AbortError` 是 SDK 的类型化 API 中唯一的错误类。其他失败，例如 Claude Code 进程退出或启动失败，使用不携带 SDK 类以匹配的错误拒绝消息迭代。[Troubleshooting](/docs/zh-CN/agent-sdk/troubleshooting) 按消息键入这些错误，每个都有原因和修复。

<h2 id="sandbox-configuration">
  沙箱配置
</h2>

<h3 id="sandboxsettings">
  `SandboxSettings`
</h3>

沙箱行为的配置。使用此选项以编程方式启用命令沙箱和配置网络限制。

```typescript theme={null}
type SandboxSettings = {
  enabled?: boolean;
  failIfUnavailable?: boolean;
  autoAllowBashIfSandboxed?: boolean;
  excludedCommands?: string[];
  allowUnsandboxedCommands?: boolean;
  network?: SandboxNetworkConfig;
  filesystem?: SandboxFilesystemConfig;
  ignoreViolations?: Record<string, string[]>;
  enableWeakerNestedSandbox?: boolean;
  ripgrep?: { command: string; args?: string[] };
};
```

| 属性 | 类型 | 默认值 | 描述 |
| :- | :- | :- | :- |
| `enabled` | `boolean` | `false` | 为命令执行启用沙箱模式 |
| `failIfUnavailable` | `boolean` | `true` | 如果 `enabled` 为 `true` 但沙箱无法启动，则在启动时停止。设置为 `false` 以回退到沙箱外执行，并在 stderr 上显示警告 |
| `autoAllowBashIfSandboxed` | `boolean` | `true` | 启用沙箱时自动批准 Bash 命令 |
| `excludedCommands` | `string[]` | `[]` | 绕过沙箱限制的命令，例如 `['docker *']`。这些自动运行在沙箱外，无需模型参与；[`sandbox.excludedCommands`](/docs/zh-CN/settings-reference#sandbox-excludedcommands) 涵盖何时应用条目 |
| `allowUnsandboxedCommands` | `boolean` | `true` | 允许模型请求在沙箱外运行命令。当为 `true` 时，模型可以在工具输入中设置 `dangerouslyDisableSandbox`，这会回退到[权限系统](#permissions-fallback-for-unsandboxed-commands) |
| `network` | [`SandboxNetworkConfig`](#sandboxnetworkconfig) | `undefined` | 网络特定的沙箱配置 |
| `filesystem` | [`SandboxFilesystemConfig`](#sandboxfilesystemconfig) | `undefined` | 用于读/写限制的文件系统特定沙箱配置 |
| `ignoreViolations` | `Record<string, string[]>` | `undefined` | 命令子字符串或 `*` 的映射（用于每个命令）到要忽略的违规文本的子字符串，例如 `{ "*": ['/etc/hosts'] }`；请参阅 [`sandbox.ignoreViolations`](/docs/zh-CN/settings-reference#sandbox-ignoreviolations) |
| `enableWeakerNestedSandbox` | `boolean` | `false` | 为兼容性启用较弱的嵌套沙箱 |
| `ripgrep` | `{ command: string; args?: string[] }` | `undefined` | 沙箱环境中的自定义 ripgrep 二进制配置 |

<Note>
  沙箱取决于平台支持，在 Linux 上，还需要 `bubblewrap` 和 `socat` 等工具。当 `enabled` 为 `true` 且沙箱无法启动时，`query()` 报告一条 `result` 消息，其中 `subtype: "error_during_execution"`，原因在 `errors` 中。对于单个消息 `query()` 调用，SDK 在生成该错误结果后抛出异常，因此将循环包装在 try 块中以继续通过它。有关错误合约，请参阅[处理结果](/docs/zh-CN/agent-sdk/agent-loop#handle-the-result)。

  要改为运行沙箱外的命令，请设置 `failIfUnavailable: false`。
</Note>

<h4 id="example-usage">
  示例用法
</h4>

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

try {
  for await (const message of query({
    prompt: "Build and test my project",
    options: {
      sandbox: {
        enabled: true,
        autoAllowBashIfSandboxed: true,
        network: {
          allowLocalBinding: true
        }
      }
    }
  })) {
    if ("result" in message) console.log(message.result);
  }
} catch (error) {
  // 单个 query() 调用在生成错误结果后抛出异常，
  // 例如当沙箱无法启动时（failIfUnavailable 默认为 true）。
  console.log(`Session ended with an error: ${error}`);
}
```

<Warning>
  **Unix socket 安全性：** `allowUnixSockets` 选项可以授予对系统服务的访问权限，这些服务可能会到达沙箱外。例如，允许 `/var/run/docker.sock` 实际上通过 Docker API 授予对主机系统的完全访问权限，绕过沙箱隔离。仅允许严格必要的 Unix sockets 并了解每个的安全含义。
</Warning>

<h3 id="sandboxnetworkconfig">
  `SandboxNetworkConfig`
</h3>

沙箱模式的网络特定配置。这些设置适用于当父级 [`SandboxSettings`](#sandboxsettings) 中的 `enabled` 为 `true` 时的沙箱化 Bash 命令。它们不限制 WebFetch 工具，该工具改用[权限规则](/docs/zh-CN/permissions#webfetch)。

```typescript theme={null}
type SandboxNetworkConfig = {
  allowedDomains?: string[];
  deniedDomains?: string[];
  strictAllowlist?: boolean;
  allowManagedDomainsOnly?: boolean;
  allowLocalBinding?: boolean;
  allowUnixSockets?: string[];
  allowAllUnixSockets?: boolean;
  httpProxyPort?: number;
  socksProxyPort?: number;
};
```

| 属性 | 类型 | 默认值 | 描述 |
| :- | :- | :- | :- |
| `allowedDomains` | `string[]` | `[]` | 沙箱进程可以访问的域名 |
| `deniedDomains` | `string[]` | `[]` | 沙箱进程无法访问的域名。优先于 `allowedDomains` |
| `strictAllowlist` | `boolean` | `false` | 拒绝沙箱化命令访问[网络允许列表](/docs/zh-CN/sandboxing#network-isolation)之外的主机，而不是提示。仅对沙箱化命令强制执行；WebFetch 等进程内工具不受其限制。仅从用户、托管或 CLI `--settings` 设置中遵守；项目设置被忽略。需要 Claude Code v2.1.219 或更高版本 |
| `allowManagedDomainsOnly` | `boolean` | `false` | 仅限管理设置。在[管理设置](/docs/zh-CN/managed-settings)中设置时，仅遵守来自管理设置的 `allowedDomains` 条目和来自管理设置的 `WebFetch(domain:...)` 允许规则，来自用户、项目或本地设置的允许条目被忽略。从 SDK 中，通过 [`managedSettings`](#options) 选项传递它 |
| `allowLocalBinding` | `boolean` | `false` | 允许进程绑定到本地端口（例如，用于开发服务器） |
| `allowUnixSockets` | `string[]` | `[]` | 进程可以访问的 Unix socket 路径（例如，Docker socket） |
| `allowAllUnixSockets` | `boolean` | `false` | 允许访问所有 Unix sockets |
| `httpProxyPort` | `number` | `undefined` | 网络请求的 HTTP 代理端口 |
| `socksProxyPort` | `number` | `undefined` | 网络请求的 SOCKS 代理端口 |

<Note>
  内置沙箱代理基于请求的主机名强制执行 `allowedDomains`，不会终止或检查 TLS 流量，因此[域前置](https://en.wikipedia.org/wiki/Domain_fronting)等技术可能会绕过它。有关详细信息，请参阅[沙箱安全限制](/docs/zh-CN/sandboxing#security-limitations)，以及[安全部署](/docs/zh-CN/agent-sdk/secure-deployment#traffic-forwarding)以配置 TLS 终止代理。
</Note>

<h3 id="sandboxfilesystemconfig">
  `SandboxFilesystemConfig`
</h3>

沙箱模式的文件系统特定配置。

```typescript theme={null}
type SandboxFilesystemConfig = {
  allowWrite?: string[];
  denyWrite?: string[];
  denyRead?: string[];
};
```

| 属性 | 类型 | 默认值 | 描述 |
| :- | :- | :- | :- |
| `allowWrite` | `string[]` | `[]` | 允许写入访问的文件路径模式 |
| `denyWrite` | `string[]` | `[]` | 拒绝写入访问的文件路径模式 |
| `denyRead` | `string[]` | `[]` | 拒绝读取访问的文件路径模式 |

<h3 id="permissions-fallback-for-unsandboxed-commands">
  沙箱外命令的权限回退
</h3>

当 `allowUnsandboxedCommands` 启用时，模型可以通过在工具输入中设置 `dangerouslyDisableSandbox: true` 来请求在沙箱外运行命令。这些请求回退到现有权限系统，意味着您的 `canUseTool` 处理程序被调用，允许您实现自定义授权逻辑。

您的 `excludedCommands` 条目改为自动绕过沙箱，无需模型参与；[`sandbox.excludedCommands`](/docs/zh-CN/settings-reference#sandbox-excludedcommands) 涵盖何时应用条目。

在下面的示例中，`isCommandAuthorized` 代表您定义的授权检查。

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Deploy my application",
  options: {
    sandbox: {
      enabled: true,
      allowUnsandboxedCommands: true // 模型可以请求沙箱外执行
    },
    permissionMode: "default",
    canUseTool: async (tool, input) => {
      // 检查模型是否请求绕过沙箱
      if (tool === "Bash" && input.dangerouslyDisableSandbox) {
        // 模型请求在沙箱外运行此命令
        console.log(`Unsandboxed command requested: ${input.command}`);

        if (isCommandAuthorized(input.command)) {
          return { behavior: "allow" as const, updatedInput: input };
        }
        return {
          behavior: "deny" as const,
          message: "Command not authorized for unsandboxed execution"
        };
      }
      return { behavior: "allow" as const, updatedInput: input };
    }
  }
})) {
  if ("result" in message) console.log(message.result);
}
```

<Warning>
  使用 `dangerouslyDisableSandbox: true` 运行的命令具有完整的系统访问权限。确保您的 `canUseTool` 处理程序仔细验证这些请求。

  如果 `permissionMode` 设置为 `bypassPermissions` 且 `allowUnsandboxedCommands` 启用，模型可以自主执行沙箱外的命令，无需批准提示，除了[操作无模式自动批准的操作](/docs/zh-CN/permission-modes#actions-no-mode-auto-approves)。此组合实际上允许模型以静默方式逃离沙箱隔离。
</Warning>

<h2 id="see-also">
  另请参阅
</h2>

* [SDK 概述](/docs/zh-CN/agent-sdk/overview) - 常规 SDK 概念
* [Python SDK 参考](/docs/zh-CN/agent-sdk/python) - Python SDK 文档
* [CLI 参考](/docs/zh-CN/cli-reference) - 命令行界面
* [常见工作流](/docs/zh-CN/common-workflows) - 分步指南
