> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 通过 MCP 将 Claude Code 连接到工具

> 了解如何使用 Model Context Protocol 将 Claude Code 连接到您的工具。

Claude Code 可以通过 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction)（一个用于 AI 工具集成的开源标准）连接到数百个外部工具和数据源。MCP 服务器为 Claude Code 提供对您的工具、数据库和 API 的访问权限。

当您发现自己从另一个工具（如问题跟踪器或监控仪表板）复制数据到聊天中时，请连接一个服务器。连接后，Claude 可以直接读取和操作该系统，而不是从您粘贴的内容中工作。

如果您是第一次连接服务器，请从 [MCP 快速入门](/docs/zh-CN/mcp-quickstart) 开始，获取分步演练。本页面是完整参考。

<h2 id="what-you-can-do-with-mcp">
  使用 MCP 可以做什么
</h2>

连接 MCP 服务器后，您可以要求 Claude Code：

* **从问题跟踪器实现功能**："添加 JIRA 问题 ENG-4521 中描述的功能，并在 GitHub 上创建 PR。"
* **分析监控数据**："检查 Sentry 和 Statsig 以检查 ENG-4521 中描述的功能的使用情况。"
* **查询数据库**："根据我们的 PostgreSQL 数据库，查找使用功能 ENG-4521 的 10 个随机用户的电子邮件。"
* **集成设计**："根据在 Slack 中发布的新 Figma 设计更新我们的标准电子邮件模板"
* **自动化工作流**："创建 Gmail 草稿，邀请这 10 个用户参加关于新功能的反馈会议。"
* **对外部事件做出反应**：MCP 服务器也可以充当[频道](/docs/zh-CN/channels)，将消息推送到您的会话中，因此当您不在时，Claude 可以对 Telegram 消息、Discord 聊天或 webhook 事件做出反应。

<h2 id="find-and-build-mcp-servers">
  查找和构建 MCP 服务器
</h2>

在 [Anthropic Directory](https://claude.ai/directory) 中浏览已审核的连接器。Directory 连接器使用与 Claude Code 相同的 MCP 基础设施，因此您可以使用 `claude mcp add` 添加列出的任何远程服务器。

<Warning>
  在连接每个服务器之前，请验证您信任该服务器。获取外部内容的服务器可能会使您面临 [提示注入风险](/docs/zh-CN/security#protect-against-prompt-injection)。
</Warning>

要构建您自己的服务器，请参阅 [MCP 服务器指南](https://modelcontextprotocol.io/docs/develop/build-server) 了解协议基础知识，以及 [Claude 连接器构建文档](https://claude.com/docs/connectors/building) 了解身份验证、测试和 Directory 提交。

您也可以使用官方的 [`mcp-server-dev` plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/mcp-server-dev) 让 Claude 为您搭建服务器。

<Steps>
  <Step title="安装插件">
    在 VS Code 扩展或桌面应用中，请按照 [安装插件](/docs/zh-CN/plugins/install#install-a-plugin) 操作，而不是执行此步骤。在终端中，运行 `claude` 启动 Claude Code，然后在其提示符处输入以下内容：

    ```
    /plugin install mcp-server-dev@claude-plugins-official
    ```

    如果安装失败，请匹配 Claude Code 报告的消息：

    * `Marketplace "claude-plugins-official" not found`：使用 `/plugin marketplace add anthropics/claude-plugins-official` 添加 marketplace，然后重试安装。
    * plugin [在 marketplace 中找不到](/docs/zh-CN/plugins/install#install-a-plugin)：检查 plugin 名称。

    如果安装摘要报告 `Run /reload-plugins to apply.`，Claude Code 会为您运行该重新加载。如果重新加载警告您的下一条消息会重新读取对话，请运行 `/reload-plugins --force`。
  </Step>

  <Step title="运行构建 skill">
    ```
    /mcp-server-dev:build-mcp-server
    ```

    Claude 会询问您的用例，并搭建一个远程 HTTP 或本地 stdio 服务器。
  </Step>
</Steps>

<h2 id="installing-mcp-servers">
  安装 MCP 服务器
</h2>

MCP 服务器可以根据您的需求以多种方式进行配置：

<h3 id="option-1-add-a-remote-http-server">
  选项 1：添加远程 HTTP 服务器
</h3>

HTTP 服务器是连接到远程 MCP 服务器的推荐选项。这是云服务最广泛支持的传输方式。

```bash theme={null}
# 基本语法
claude mcp add --transport http <name> <url>

# 真实示例：连接到 Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# 带有 Bearer 令牌的示例
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

通过 `.mcp.json`、`~/.claude.json` 或 `claude mcp add-json` 中的 JSON 配置 MCP 服务器时，`type` 字段接受 `streamable-http` 作为 `http` 的别名。MCP 规范对此传输使用名称 `streamable-http`，因此从服务器文档复制的配置无需修改即可工作。

具有 `url` 但没有 `type` 的 JSON 条目是配置错误，因为 Claude Code 将没有 `type` 的条目读取为 stdio 服务器。Claude Code 跳过该服务器并报告 `MCP server "<name>" has a "url" but no "type"; add "type": "http" (or "sse" / "ws") to this entry`。在 v2.1.202 之前，Claude Code 将此配置错误报告为 `command: expected string, received undefined`。

只有 SDK 主机应用程序（例如 [Agent SDK](/docs/zh-CN/agent-sdk/mcp) 应用程序或 [桌面应用](/docs/zh-CN/desktop)）可以注册进程内 `"type": "sdk"` 服务器。Claude Code 跳过 `.mcp.json`、`~/.claude.json` 或设置中的 `"type": "sdk"` 条目，并报告 `Skipped — MCP server "<name>" declares type "sdk", which only an SDK host application can register`。

在 `--output-format stream-json` 运行中，Claude Code 还在 `system/init` 事件的 [`mcp_server_errors` 字段](/docs/zh-CN/headless#stream-responses) 中报告跳过的 `--mcp-config` 条目，以便脚本可以检测到服务器从未加载。这需要 Claude Code v2.1.219 或更高版本。

<h3 id="option-2-add-a-remote-sse-server">
  选项 2：添加远程 SSE 服务器
</h3>

<Warning>
  SSE（Server-Sent Events）传输已弃用。请在可用的地方使用 HTTP 服务器。
</Warning>

某些服务仍然仅公开 SSE 端点。使用与 [HTTP 服务器](#option-1-add-a-remote-http-server) 相同的 `claude mcp add --transport http <name> <url>` 命令添加这些。Claude Code 首先尝试 HTTP 传输，当服务器不接受时切换到 SSE。自动切换需要 Claude Code v2.1.265 或更高版本。

在较早的版本上，或直接通过 SSE 连接，请改为传递 `--transport sse`：

```bash theme={null}
# 基本语法
claude mcp add --transport sse <name> <url>

# 真实示例：连接到 Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse

# 带有身份验证标头的示例
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"
```

<h3 id="option-3-add-a-local-stdio-server">
  选项 3：添加本地 stdio 服务器
</h3>

Stdio 服务器作为本地进程在您的机器上运行。它们非常适合需要直接系统访问或自定义脚本的工具。

Claude Code 在生成的服务器的环境中设置 `CLAUDE_PROJECT_DIR` 为项目根目录，以便您的服务器可以解析项目相对路径，而不依赖于工作目录。这与 hook 在其 `CLAUDE_PROJECT_DIR` 变量中接收的目录相同。从服务器进程内读取它，例如 Node 中的 `process.env.CLAUDE_PROJECT_DIR` 或 Python 中的 `os.environ["CLAUDE_PROJECT_DIR"]`。

`CLAUDE_PROJECT_DIR` 是稳定的项目根目录，在会话中添加或删除工作目录时不会更改。限制自己的文件系统访问到一组允许目录的服务器应该改为实现 MCP `roots/list` 请求。Claude Code 使用会话的启动目录加上您通过 `--add-dir`、`/add-dir` 或 `additionalDirectories` 设置授予的每个 [额外工作目录](/docs/zh-CN/permissions#working-directories) 来回答 `roots/list`。当该集合更改时，Claude Code 发送 `notifications/roots/list_changed`。在 v2.1.203 之前，`roots/list` 仅返回启动目录，Claude Code 不发送 `notifications/roots/list_changed`。

此变量在服务器的环境中设置，而不是在 Claude Code 自己的环境中，因此通过项目作用域的 `.mcp.json` 条目或 `~/.claude.json` 中的本地或用户作用域服务器条目中的 `command` 或 `args` 中的 `${VAR}` 扩展来引用它需要默认值，例如 `${CLAUDE_PROJECT_DIR:-.}`。插件提供的 MCP 配置直接替换 `${CLAUDE_PROJECT_DIR}` 并且不需要默认值。

```bash theme={null}
# 基本语法
claude mcp add [options] <name> -- <command> [args...]

# 真实示例：添加 Airtable 服务器
claude mcp add --env AIRTABLE_API_KEY=YOUR_KEY --transport stdio airtable \
  -- npx -y airtable-mcp-server
```

<Note>
  对于 stdio 服务器，`--`（双破折号）将 Claude 自己的选项（例如 `--transport`、`--env` 和 `--scope`）与运行服务器的命令和参数分开。`--` 之后的所有内容都原封不动地传递给服务器。

  例如：

  * `claude mcp add --transport stdio myserver -- npx server` → 运行 `npx server`
  * `claude mcp add --env KEY=value --transport stdio myserver -- python server.py --port 8080` → 使用环境中的 `KEY=value` 运行 `python server.py --port 8080`

  没有 `--`，Claude Code 会尝试将服务器的标志（如上面的 `--port`）解析为自己的选项。

  `--env` 接受多个 `KEY=value` 对。如果服务器名称直接跟在 `--env` 之后，CLI 会将该名称读取为另一对并拒绝它，因此在 `--env` 和服务器名称之间至少放置一个其他选项，例如 `--transport stdio`。
</Note>

<h3 id="option-4-add-a-remote-websocket-server">
  选项 4：添加远程 WebSocket 服务器
</h3>

WebSocket 服务器保持持久的双向连接，适合主动向 Claude 推送事件的远程 MCP 服务器。当您的服务器仅响应请求时，请改用 HTTP，因为 HTTP 支持 OAuth 和 `claude mcp add --transport` 标志，而 WebSocket 都不支持。

在 `.mcp.json` 中或使用 `claude mcp add-json` 配置 WebSocket 服务器：

```bash theme={null}
claude mcp add-json events-server \
  '{"type":"ws","url":"wss://mcp.example.com/socket","headers":{"Authorization":"Bearer YOUR_TOKEN"}}'
```

`type: "ws"` 条目接受与 `http` 相同的 `url`、`headers`、`headersHelper`、`timeout` 和 `alwaysLoad` 字段。身份验证仅限标头，因此在 `headers` 中传递静态令牌或在连接时使用 [`headersHelper`](#use-dynamic-headers-for-custom-authentication) 生成一个。`claude mcp add --transport` 标志不接受 `ws`。

<h3 id="add-a-server-from-setup-instructions-written-for-another-client">
  从为另一个客户端编写的设置说明添加服务器
</h3>

MCP 服务器不特定于 Claude Code，因此服务器的设置说明可能是为 Claude Desktop、Cursor 或另一个 MCP 客户端编写的，并且不提供 `claude mcp add` 命令。要添加服务器，请在这些说明中查找 URL、启动命令或 JSON 块：

* **URL**，例如 `https://mcp.example.com/mcp`：服务器是远程的。
* **启动命令**，例如 `npx -y @example/mcp-server`：服务器在您的机器上运行。
* **`mcpServers` JSON 块**：为另一个客户端的设置文件编写的配置。

每一个都是 [安装 MCP 服务器](#installing-mcp-servers) 中四个选项之一接受的输入。找到您下面拥有的形状，将其转换为 Claude Code 接受的命令。除非您添加 `--scope project` 或 `--scope user`，否则每个命令都写入 [本地作用域](#local-scope)。

<h4 id="from-a-url">
  从 URL
</h4>

URL 表示服务器是远程的。对于 `https://` 端点，使用 `--transport http` 添加它，或在说明说端点使用 SSE 时遵循 [选项 2](#option-2-add-a-remote-sse-server)。对于 `wss://` 端点，改为使用 [选项 4](#option-4-add-a-remote-websocket-server)，因为 `--transport` 不接受 `ws`：

```bash theme={null}
claude mcp add --transport http example https://mcp.example.com/mcp
```

如果说明还提供 API 密钥或令牌标头，请使用 `--header` 传递它，如 [选项 1](#option-1-add-a-remote-http-server) 所示。

<h4 id="from-an-npx-uvx-or-binary-command">
  从 `npx`、`uvx` 或二进制命令
</h4>

启动命令表示服务器作为本地 stdio 进程运行。将整个命令放在 `--` 之后，以便 Claude Code 将标志（如 `-y`）传递给启动服务器的命令，而不是将它们读取为自己的选项。使用 `--env` 传递说明要求的任何环境变量，在服务器名称之后和 `--` 之前：

```bash theme={null}
claude mcp add example --env API_KEY=your-key -- npx -y @example/mcp-server
```

[选项 3](#option-3-add-a-local-stdio-server) 完整涵盖 `--` 分隔符。

<h4 id="from-an-mcpservers-json-block">
  从 `mcpServers` JSON 块
</h4>

为另一个 MCP 客户端（例如 Claude Desktop）编写的 `mcpServers` 块使用 Claude Code 读取的包装器键和条目形状。将 `mcpServers` 内的对象（而不是包装器）传递给 `claude mcp add-json`。两种条目需要先修复：

* **`url` 没有 `type`**：添加 `"type": "http"`、`"type": "sse"` 或 `"type": "ws"` 以匹配端点。Claude Code 将没有 `type` 的条目读取为 stdio 服务器，因此没有 `type` 的 `url` 条目会失败。
* **键包含除字母、数字、连字符和下划线以外的字符**：选择仅使用这些字符的服务器名称。否则键就是服务器名称。

例如，此块：

```json theme={null}
{
  "mcpServers": {
    "example": {
      "command": "npx",
      "args": ["-y", "@example/mcp-server"]
    }
  }
}
```

变成此命令：

```bash theme={null}
claude mcp add-json example '{"command":"npx","args":["-y","@example/mcp-server"]}'
```

[从 JSON 配置添加 MCP 服务器](#add-mcp-servers-from-json-configuration) 涵盖 `add-json` 的 shell 转义和 `--scope` 标志。要与您的团队共享服务器，请改为添加 `--scope project`，或在项目根目录的 `.mcp.json` 中的 `mcpServers` 下添加条目并提交它。[项目作用域](#project-scope) 涵盖 Claude Code 如何加载和批准该文件。

每个 `claude mcp add` 和 `claude mcp add-json` 命令在成功时打印 `Added ...` 行。要检查 Claude Code 是否已连接，请运行 `claude mcp get <name>`；[服务器状态](#server-status) 涵盖它显示的状态和 `.mcp.json` 服务器的批准步骤。

<h3 id="managing-your-servers">
  管理您的服务器
</h3>

配置后，您可以使用这些命令管理您的 MCP 服务器：

```bash theme={null}
# 列出所有配置的服务器
claude mcp list

# 获取特定服务器的详细信息
claude mcp get notion

# 删除服务器
claude mcp remove notion

# （在 Claude Code 中）检查服务器状态
/mcp
```

删除远程服务器时，Claude Code 也会删除为该服务器存储的 OAuth 令牌和客户端注册。

<h4 id="server-status">
  服务器状态
</h4>

`claude mcp add` 通过打印 `Added ...` 行确认成功添加，这意味着配置已写入。如果命令改为打印 `was not saved` 消息，请参阅 [MCP 服务器未保存或删除](/docs/zh-CN/errors#mcp-server-was-not-saved-or-removed)；对于 `may not have been saved` 消息，请参阅 [MCP 服务器可能未保存或删除](/docs/zh-CN/errors#mcp-server-may-not-have-been-saved-or-removed)。

`claude mcp list` 在它列出的每个服务器旁边显示健康状态，例如 `✔ Connected`、`! Needs authentication` 或 `✘ Failed to connect`。失败状态意味着 Claude Code 无法连接到该服务器，而不是列表命令失败。

此列表中的状态报告配置决策而不是连接尝试，因此 Claude Code 在不连接到服务器的情况下打印它们：

* ``⏸ Pending approval (run `claude` to approve)``：来自 `.mcp.json` 的项目作用域服务器，您尚未批准。Claude Code 在 `claude mcp list` 和 `claude mcp get <name>` 中都显示它。运行 `claude` 交互式地审查和批准它。
* `✘ Rejected (see disabledMcpjsonServers in settings)`：由 [`disabledMcpjsonServers`](/docs/zh-CN/settings-reference#disabledmcpjsonservers) 条目拒绝的 `.mcp.json` 服务器。Claude Code 仅在 `claude mcp get <name>` 中显示它。
* `⊘ Disabled for this project (re-enable via /mcp)`：项目的 [`disabledMcpServers`](#disable-a-server-without-removing-it) 列表命名的服务器。Claude Code 在 `claude mcp list` 和 `claude mcp get <name>` 中都显示它。从 `/mcp` 面板重新打开服务器。

<h4 id="project-server-approvals-and-workspace-trust">
  项目服务器批准和工作区信任
</h4>

从 v2.1.196 开始，`claude mcp list` 和 `claude mcp get` 仅从未签入仓库的设置文件中读取 `.mcp.json` 批准，直到您通过在其中运行 `claude` 并接受工作区信任对话框来信任工作区。克隆的仓库无法批准自己的服务器：提交到项目的 `.claude/settings.json` 的 [`enableAllProjectMcpServers`](/docs/zh-CN/settings-reference#enableallprojectmcpservers) 或 [`enabledMcpjsonServers`](/docs/zh-CN/settings-reference#enabledmcpjsonservers) 在不受信任的文件夹中被忽略，服务器保持在 `⏸ Pending approval` 而不是被连接和健康检查。

这些来源的批准仍然适用于不受信任的文件夹：

* 您的用户 `~/.claude/settings.json`
* 托管设置
* 使用 `--settings` 传递的设置

Claude Code 也应用来自未跟踪的 `.claude/settings.local.json` 的批准，但它运行 git 来检查文件是否被跟踪，并且仅在 [受信任的文件夹](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust) 中运行该检查。在您从未信任的文件夹中，Claude Code 等待信任对话框后才应用文件的批准，除非该文件夹是您自己的配置主目录：您的主目录，或其 `.claude` 您已设置为 [`CLAUDE_CONFIG_DIR`](/docs/zh-CN/env-vars) 的目录。在 v2.1.207 之前，Claude Code 即使在您从未信任的文件夹中也应用来自未跟踪的 `.claude/settings.local.json` 的批准。

任何设置文件中的 `disabledMcpjsonServers` 条目仍然拒绝服务器。

<h4 id="server-status-detail">
  服务器状态详情
</h4>

在 `/mcp` 中（包括服务器的菜单）和 [`/plugin`](/docs/zh-CN/plugins/install) 管理器中，您之前使用过的远程 HTTP 或 SSE 服务器可以显示 `cached` 状态，例如 `cached 2h ago · connects on first use · 5 tools`。Claude Code 从发现缓存加载了服务器的工具列表，该缓存保存在上一个会话中，而不是在启动时连接，Claude Code 在 Claude 首次调用服务器的工具之一时连接服务器。工具从您的第一条消息开始可用，因此您无需执行任何操作。发现缓存及其 `cached` 状态需要 Claude Code v2.1.221 或更高版本。

发现缓存默认关闭，除非逐步推出已为您的帐户启用它。设置 [`MCP_DISCOVERY_CACHE=1`](/docs/zh-CN/env-vars) 打开它，或设置为 `0` 即使推出已启用它也保持关闭。在 v2.1.238 之前，缓存默认打开。

当您从 `/mcp` 中的服务器菜单选择 **Disable** 或 **Clear authentication** 时，Claude Code 也会丢弃该服务器的缓存条目。**Reconnect** 在已连接或失败的服务器上也会丢弃它；在 `cached` 服务器上，**Reconnect** 会立即连接服务器并保留条目。丢弃条目后，Claude Code 下次连接到服务器时，会从服务器而不是从缓存获取工具列表。

当服务器的状态为 `✘ Failed to connect` 时，`claude mcp list` 将失败详情附加到该状态行，`claude mcp get <name>` 在 `Issue:` 行上显示它：HTTP 状态或错误代码，加上服务器返回的任何错误文本。`/mcp` 中的服务器详情视图在其 `Issue:` 行中包含相同的服务器报告文本。Claude Code 从此详情中编辑掉类似凭据的文本，并且永远不包括展开后的服务器 URL，它可能携带机密。Claude Code 不向 `✘ Connection error` 状态附加详情，因为它会打印的异常文本可能嵌入该 URL。在 v2.1.219 之前，两个命令仅显示裸失败状态，没有状态代码或服务器的错误文本。

当您从 `/mcp` 完成身份验证且连接仍然因 HTTP 状态或传输错误代码失败时，Claude Code 在尝试后打印的消息中添加该代码和服务器 URL 的来源。来源是方案和主机，加上 URL 命名的端口（如果有），例如 `https://mcp.example.com`。

* 路径和查询永远不会出现在该消息中。
* 对于本地、项目或用户 [作用域](#mcp-installation-scopes) 中的服务器或托管 MCP 配置中的服务器，来源显示该配置中写入的主机，因此主机中的 `${VAR}` 引用在消息中不会展开。
* 对于没有状态或错误代码的失败，Claude Code 显示错误文本而不显示来源。

配置为空 `url` 的远程服务器在 `/mcp`、`claude mcp list` 和 [`/plugin`](/docs/zh-CN/plugins/install) 管理器中显示为 `not configured`，Claude Code 不尝试连接到它。插件可以包含这样的占位符条目，用于您稍后配置的连接器，因此 Claude Code 不将其报告为错误或设置问题。`/mcp` 中的服务器详情视图显示 `No URL configured for this server`；设置条目的 `url` 以连接它。在 v2.1.208 之前，Claude Code 将空 `url` 报告为配置问题，并提示重新连接。

<h4 id="configuration-warnings">
  配置警告
</h4>

Claude Code 警告以下配置问题。每个条目说明 Claude Code 检查什么以及如何清除警告：

* **隐藏的空格**：当 MCP 配置值携带隐藏的前导或尾随空格时，Claude Code 发出警告，这通常来自粘贴带有尾随换行符的令牌。Claude Code 检查 `command`、`url`、每个 `args` 条目以及 `env` 和 `headers` 下的值和键名称。Claude Code 在 `claude mcp list` 输出和 `/mcp` 中显示警告，命名受影响的字段而不回显其值，例如 `Leading or trailing whitespace in: headers.Authorization`。Claude Code 不修剪空格并完全按照写入的方式使用值，因此请编辑配置以删除它。
* **在多个作用域中使用相同名称**：如果您在多个 [作用域](#mcp-installation-scopes) 中定义相同的服务器名称，具有不同的端点，Claude Code 在 `claude mcp list` 输出和 `/mcp` 中警告冲突。Claude Code 按端点存储 OAuth 登录，因此当您在一个项目中对加载的定义进行身份验证时，您仍然需要在加载不同定义的项目中单独登录。保留您想要的端点并使用 `claude mcp remove <name> --scope <scope>` 删除其他端点。在警告中，Claude Code 按您的配置中所写的形式引用每个作用域的端点，[`${VAR}` 引用](#environment-variable-expansion-in-mcp-json) 保持未展开，因此它永远不显示已解析的值，例如 API 密钥。
* **保留名称**：Claude Code 保留其内置服务器的名称，包括 `workspace`、`claude-in-chrome`、`computer-use`、`Claude Preview` 和 `Claude Browser`。如果您的配置定义具有保留名称的服务器，Claude Code 在加载时跳过它并显示警告，要求您重命名它。`claude mcp add` 拒绝保留名称并出现错误。`Claude Preview` 和 `Claude Browser` 都命名 [Claude Code 桌面应用的预览窗格](/docs/zh-CN/desktop#preview-your-app) 使用的内置服务器。
* **缺少环境变量**：如果服务器配置中的 [`${VAR}` 引用](#environment-variable-expansion-in-mcp-json) 命名未设置且没有 `:-default` 的变量，Claude Code 在 `claude mcp list` 输出和 `/mcp` 中警告，命名变量，并仍然使用 `${VAR}` 文本未展开加载服务器。设置变量或添加 `${VAR:-default}` 备用值。在远程服务器的 `url` 和 `headers` 中，某些凭据变量 [读取为空](#credential-variables-that-read-as-empty) 而不显示警告。

<h4 id="tool-availability">
  工具可用性
</h4>

`/mcp` 面板在每个连接的服务器旁边显示工具计数，并标记声称工具能力但不公开工具的服务器。

如果您的请求需要来自仍在后台连接的服务器的工具，Claude 会在继续之前等待该服务器。等待的方式取决于您的配置：

* **使用 [工具搜索](#scale-with-mcp-tool-search)（默认）**：等待发生在 `ToolSearch` 调用内。
* **不使用工具搜索**：Claude 改为使用 `WaitForMcpServers` 工具。不使用工具搜索的配置包括自定义 `ANTHROPIC_BASE_URL`、`ENABLE_TOOL_SEARCH=false` 和 Google Cloud 的 Agent Platform 上早于 Claude 4.5 代的模型。
* **在 Microsoft Foundry [部署托管在 Azure 上](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry#hosting-options)**：Claude 在工具搜索路径上启动而不是使用 `WaitForMcpServers`，因为 Claude Code 仅从 API 发现部署的服务器端拒绝。Claude Code 将该部署切换到 [前期加载](#scale-with-mcp-tool-search) 后，来自完成连接的服务器的工具在 Claude 的下一个请求中变为可用。

启用工具搜索后，当服务器在 Claude 工作时完成连接时，Claude Code 在同一轮次的下一个请求中将服务器的工具名称列出给 Claude。Claude 然后可以搜索和调用这些工具，而无需等待您的下一条消息。

恢复会话后，Claude 可以在工具的 MCP 服务器仍在连接时调用已保存对话中的工具。当服务器处于首次连接尝试时，Claude Code 会将该调用保留最多 10 秒，并在工具可用后运行它。如果服务器未能及时连接，或者已在 [失败尝试后重试](#automatic-reconnection)，调用会失败并返回 `No such tool available` [工具错误](/docs/zh-CN/errors#no-such-tool-available)。

<h3 id="disable-a-server-without-removing-it">
  禁用服务器而不删除它
</h3>

在 `/mcp` 面板中切换服务器关闭，以停止 Claude Code 连接到它，而不丢失其配置。Claude Code 仍然在 `/mcp` 中列出服务器，标记为禁用。

当您切换服务器时，Claude Code 在 `~/.claude.json` 中按项目记录您的选择，在两个涵盖不相交服务器集的列表之一中：

* `disabledMcpServers`：用户配置的服务器、插件服务器、您的组织 [通过托管设置提供](/docs/zh-CN/managed-mcp#provide-servers-through-managed-settings) 的服务器、Claude Code [自己获取](#how-connectors-reach-claude-code) 的 claude.ai 连接器以及默认打开的内置服务器的选择退出列表。Claude Code 不连接您在此处列出的服务器。当您使用 [禁用 claude.ai 连接器](#disable-claude-ai-connectors) 中描述的按项目 `/mcp` 切换禁用 claude.ai 连接器时，Claude Code 在此列表下使用其显示名称（例如 `claude.ai Slack`）写入它。
* `enabledMcpServers`：默认关闭的内置服务器（例如 `computer-use`）的选择加入列表。Claude Code 仅当您在此处列出它时才连接默认关闭的服务器。

Claude Code 为每个服务器查询恰好两个列表之一，因此两个列表都不会覆盖另一个。如果您将常规服务器添加到 `enabledMcpServers`，或将默认关闭的内置服务器添加到 `disabledMcpServers`，Claude Code 会忽略该条目。

`disabledMcpServers` 和 `enabledMcpServers` 与 [`enabledMcpjsonServers`](/docs/zh-CN/settings-reference#enabledmcpjsonservers) 和 [`disabledMcpjsonServers`](/docs/zh-CN/settings-reference#disabledmcpjsonservers) 无关，后者控制项目的 `.mcp.json` 文件中定义的服务器的批准。

<h3 id="mcp-client-runtimes">
  MCP 客户端运行时
</h3>

Claude Code 通过两个客户端运行时之一连接到 MCP 服务器。v1 运行时基于 MCP TypeScript SDK 1.x。v2 运行时是 [MCP TypeScript SDK 2.0](https://ts.sdk.modelcontextprotocol.io/v2/) 上的相同代码，它添加了 MCP 协议修订版 2026-07-28。本页的其余部分适用于两个运行时，除非某个部分指明 v2 运行时。

Claude Code 在每次启动时选择一个运行时，并在您退出前保持它。在 [获取功能标志](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching) 的会话中，它在 Claude Code v2.1.232 或更高版本上使用 v2 运行时。

在不获取功能标志的会话中，Claude Code 在 Claude Code v2.1.274 或更高版本上默认使用 v2 运行时：

* Amazon Bedrock、Claude Platform on AWS、Google Cloud 的 Agent Platform 或 Microsoft Foundry 上的会话，除非嵌入 Claude Code 的主机平台设置 [`CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST`](/docs/zh-CN/env-vars)
* 通过 [Claude 应用网关](/docs/zh-CN/claude-apps-gateway) 登录的会话
* 您关闭遥测或功能标志获取的会话，例如使用 `DISABLE_TELEMETRY`

在 v2 上，Claude Code 还会：

* 询问 HTTP 和 stdio 服务器是否支持较新的修订版，并与支持的服务器一起使用它。在获取功能标志的会话中，它还会询问 claude.ai 连接器服务器。它与 v1 一样连接到其他所有服务器。
* 通过 [它保持打开的流](#notification-streams-on-the-v2-runtime) 从使用较新修订版的服务器接收 `list_changed` 通知。
* 不注册在较新修订版上连接的 [频道](#push-messages-with-channels) 服务器，因为该修订版无法携带频道消息。
* 当授权响应指明意外的发行者时，使 [MCP OAuth 登录](#authenticate-with-remote-mcp-servers) 失败。
* 仅将 [MCP OAuth](#authenticate-with-remote-mcp-servers) 凭据发送到通过 HTTPS 或在 `localhost`、`127.0.0.1` 或 `::1` 上提供的令牌端点。对于令牌端点在其他任何地方为纯 `http://` 的服务器（例如本地网络上的设备），登录失败。请参阅 [拒绝向非 https 令牌端点发送凭据](/docs/zh-CN/errors#refusing-to-send-credentials-to-non-https-token-endpoint)。

Anthropic 可以通过 Claude Code 获取的功能标志，将特定服务器保持在较早的协议上，或不使用该流。

要自己选择运行时，请设置 [`MCP_SDK_GENERATION`](/docs/zh-CN/env-vars) 为 `v1` 或 `v2`。要决定 Claude Code 是否询问，请设置 [`MCP_PROTOCOL_NEGOTIATION`](/docs/zh-CN/env-vars) 为 `auto` 或 `legacy`。

<h3 id="dynamic-tool-updates">
  动态工具更新
</h3>

MCP 服务器可以在连接期间更改其提供的工具、提示词或资源，并发送 `list_changed` 通知。收到通知时：

* **在交互式终端会话中**，Claude Code 从该服务器获取更新后的列表，因此您无需重新连接它。
* **在使用 `-p` 标志的 [非交互模式](/docs/zh-CN/headless) 和 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 中**，Claude Code 在收到这些通知时仅刷新工具列表。

如果刷新请求失败，Claude Code 保留服务器之前发现的工具、提示词和资源，直到稍后的刷新成功。在 v2.1.214 之前，刷新期间的瞬时错误将服务器的工具、提示词和资源替换为空列表。

<h4 id="notification-streams-on-the-v2-runtime">
  v2 运行时上的通知流
</h4>

在 [v2 运行时](#mcp-client-runtimes) 上，Claude Code 通过它保持打开的流从使用较新协议修订版的服务器接收 `list_changed` 通知。当流关闭时，Claude Code 重新打开它，有两个限制：

* **流在 10 秒内再次关闭**：Claude Code 最多重新打开三次，然后停止该连接。
* **流保持打开超过 10 秒，然后关闭**，连接到无服务器主机的流通常如此：在一小时内五次重新打开后，Claude Code 在下一次之前等待约六小时。

在流重新打开之前，您保留服务器最后获取的工具、提示词和资源。要更快地获取其更改，请从 `/mcp` 重新连接服务器。

<h3 id="automatic-reconnection">
  自动重新连接
</h3>

Claude Code 重新连接在会话中途断开的远程服务器，并在瞬时错误后重试 HTTP 或 SSE 服务器的首次连接。Stdio 服务器是本地进程，Claude Code 不会自动重新连接它们。

<h4 id="mid-session-drops-of-a-remote-server">
  远程服务器的会话中途断开
</h4>

Claude Code 使用指数退避重新连接断开的远程服务器：最多五次尝试，从一秒延迟开始，每次加倍。您看到的内容取决于您如何运行 Claude Code：

* **在交互式会话中**：`/mcp` 在 Claude Code 重新连接时显示服务器为待处理。在五次失败尝试后，Claude Code 将服务器标记为失败，或在服务器需要再次授权时标记为需要身份验证。当它将服务器标记为失败时，您会看到 `MCP server "<name>" disconnected · open /mcp to reconnect` 通知。您可以从 `/mcp` 手动重试。
* **在 [`claude -p`](/docs/zh-CN/headless) 运行和 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 会话中**：Claude Code 按相同的计划重新连接，没有 `/mcp` 面板显示尝试。

<h4 id="failed-first-connections">
  失败的首次连接
</h4>

当 HTTP 或 SSE 服务器的首次连接因瞬时错误（例如 5xx 响应、连接被拒绝或超时）失败时，Claude Code 最多重试三次。如果连接仍然失败，Claude Code 将服务器标记为失败。

Claude Code 在这些情况下不重试：

* WebSocket 服务器的首次连接
* 身份验证或未找到错误，因为它需要配置更改来解决。当 [`headersHelper`](#use-dynamic-headers-for-custom-authentication) 是服务器唯一的 `Authorization` 标头来源时，Claude Code 仍然重试身份验证错误，因为它在每次尝试时重新运行助手并可以获取新凭据

<h4 id="failed-discovery-requests">
  失败的发现请求
</h4>

服务器连接后，Claude Code 向其发送能力发现请求，例如 `tools/list`、`prompts/list` 和 `resources/list`。Claude Code 在瞬时网络或服务器错误后最多重试这些请求三次，短退避。它不重试身份验证错误、4xx 响应或请求超时。

<h4 id="retry-failed-servers-yourself">
  自行重试失败的服务器
</h4>

要重试所有失败或需要身份验证的服务器，请运行 `/mcp reconnect all`。在交互式终端中，这需要 Claude Code v2.1.284 或更高版本，较早的版本会在此处打印 `MCP server "all" not found`。

<h4 id="how-claude-learns-that-a-server-failed">
  Claude 如何了解服务器失败
</h4>

Claude Code 是否告诉 Claude 配置的服务器未能连接取决于 [工具搜索](#scale-with-mcp-tool-search)，默认打开：

* 使用工具搜索，Claude Code 告诉 Claude 哪个服务器失败及其连接错误，因此 Claude 在其回复中报告连接失败。Claude Code 在找不到匹配工具的 `ToolSearch` 结果中包含相同的信息。
* 在任何 [不使用工具搜索的配置](#configure-tool-search) 中，Claude Code 不向 Claude 报告失败的服务器连接。

<h3 id="push-messages-with-channels">
  使用频道推送消息
</h3>

MCP 服务器也可以直接将消息推送到您的会话中，以便 Claude 可以对外部事件（如 CI 结果、监控警报或聊天消息）做出反应。要启用此功能，您的服务器声明 `claude/channel` 能力，您在启动时使用 `--channels` 标志选择加入。请参阅 [频道](/docs/zh-CN/channels) 以使用官方支持的频道，或 [频道参考](/docs/zh-CN/channels-reference) 以构建您自己的。

在 [v2 运行时](#mcp-client-runtimes) 上，协商 MCP 协议修订版 2026-07-28 的频道服务器无法传递频道消息，因此 Claude Code 不将其注册为频道。不支持该修订版的频道服务器会在较早的握手上连接，并像以前一样注册。

Claude Code 默认会向 stdio 服务器询问该修订版。要将 stdio 频道服务器保持在较早的握手上，请将 [`MCP_PROTOCOL_NEGOTIATION`](/docs/zh-CN/env-vars) 设置为 `legacy`，这会将所有服务器都保持在较早的握手上。

<Tip>
  提示：

  * 使用 `-s` 或 `--scope` 标志指定配置的存储位置：
    * `local`（默认）：仅在当前项目中对您可用
    * `project`：通过 `.mcp.json` 文件与项目中的每个人共享
    * `user`：在所有项目中对您可用
  * 使用 `-e` 或 `--env` 标志设置环境变量（例如 `-e KEY=value`）
  * `--transport` 和 `--header` 标志也接受 `-t` 和 `-H` 短形式
  * 使用 `MCP_TIMEOUT` 环境变量配置 MCP 服务器启动超时（例如 `MCP_TIMEOUT=10000 claude` 设置 10 秒超时）
  * 通过在该服务器的 `.mcp.json` 条目中添加 `timeout` 字段（以毫秒为单位）来设置按服务器工具执行超时，例如 `"timeout": 600000` 表示十分钟。这仅对该服务器覆盖 `MCP_TOOL_TIMEOUT` 环境变量
  * 当 MCP 工具输出超过 10,000 个 token 时，Claude Code 显示警告，默认限制输出为 25,000 个 token。要更改 token 限制，请设置 `MAX_MCP_OUTPUT_TOKENS` 环境变量，例如 `MAX_MCP_OUTPUT_TOKENS=50000`。警告阈值是固定的。除非服务器提高了某个工具自身的限制，否则超过 50,000 个字符的成功文本结果会被保存到文件中，不受此变量影响。请参阅 [MCP 输出限制和警告](#mcp-output-limits-and-warnings)
  * 使用 `/mcp` 与需要 OAuth 2.0 身份验证的远程服务器进行身份验证
</Tip>

按服务器的 `timeout` 是每个工具调用的硬性墙钟时间限制，来自服务器的进度通知不会延长它。低于 1000 的值被忽略并回退到 `MCP_TOOL_TIMEOUT`，或在该变量未设置时回退到其约 28 小时的默认值。对于 HTTP、SSE 或 [claude.ai 连接器](/docs/zh-CN/mcp#use-mcp-servers-from-claude-ai) 服务器，还有第二个按请求计时器，覆盖每个请求直到服务器的第一个响应字节。Claude Code 将该计时器设置为三个值中最大的：60 秒、适用于服务器的工具超时和 `MCP_TIMEOUT`。未设置的 `MCP_TOOL_TIMEOUT` 的 28 小时默认值不参与该比较，低于 60 秒的值不会缩短计时器。Stdio 和 WebSocket 服务器没有按请求计时器。

至少 1000 的按服务器 `timeout` 也充当下面描述的空闲超时的下限：Claude Code 永远不会早于按服务器 `timeout` 因空闲而中止该服务器的工具调用。需要 Claude Code v2.1.203 或更高版本。

对 MCP 服务器的工具调用，如果在空闲窗口内既没有响应也没有进度通知，会以错误中止，而不是等待墙钟时间限制。空闲超时适用于除 IDE 服务器和 SDK 进程内服务器外的每种服务器类型。空闲窗口对 HTTP、SSE、WebSocket 和 [claude.ai 连接器](#use-mcp-servers-from-claude-ai) 服务器默认为五分钟，对 stdio 服务器默认为 30 分钟。在 v2.1.203 之前，stdio 服务器免除空闲超时。

设置 [`CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`](/docs/zh-CN/env-vars) 环境变量（以毫秒为单位）来更改空闲窗口，或将其设置为 `0` 以禁用检查。

这些超时限制调用可以运行多长时间，但不一定是它阻塞会话多长时间：运行超过两分钟的主对话调用会先移到后台任务。请参阅 [长工具调用的自动后台处理](#automatic-backgrounding-of-long-tool-calls)。

<h3 id="automatic-backgrounding-of-long-tool-calls">
  长工具调用的自动后台处理
</h3>

主对话中的 MCP 工具调用在两分钟后仍在运行时会移到后台任务，而不是阻塞会话。Claude 立即收到任务 ID 并继续工作，结果在调用完成时作为任务通知到达。自动后台处理需要 Claude Code v2.1.212 或更高版本。

任务出现在 [`/tasks`](/docs/zh-CN/commands#all-commands) 中，您也可以在其中停止它，退出会话后它不会保留。任务的条目显示服务器报告的最新进度。

调用在后台运行时，每次调用的限制仍然适用：由按服务器 `timeout` 或 [`MCP_TOOL_TIMEOUT`](/docs/zh-CN/env-vars) 设置的墙钟时间限制，以及由 [`CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`](/docs/zh-CN/env-vars) 设置的空闲超时。

设置 [`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`](/docs/zh-CN/env-vars) 环境变量（以毫秒为单位）来更改阈值，或将其设置为 `0` 以关闭自动后台处理。将 `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` 设置为 `1` 也会关闭它，以及所有其他后台任务功能。

某些调用永远不会移到后台：

* 来自 [子代理](/docs/zh-CN/sub-agents) 的调用；Claude Code 仅后台处理主对话调用
* 对 IDE 服务器的调用
* [非交互模式](/docs/zh-CN/headless) 中的调用，除非 `CLAUDE_AUTO_BACKGROUND_TASKS` 设置为 `1`，因为一次性运行可能在结果到达前结束

等待已打开的 [引出对话框](#respond-to-mcp-elicitation-requests) 的调用在对话框打开期间不会后台处理；服务器是在等待您的输入，而不是运行缓慢，因此 Claude Code 将移动推迟到对话框关闭。

<h3 id="plugin-provided-mcp-servers">
  插件提供的 MCP 服务器
</h3>

[插件](/docs/zh-CN/plugins/overview) 可以捆绑 MCP 服务器，在您启用插件时提供工具和集成。

**插件 MCP 服务器如何工作**：

* 插件在插件根目录的 `.mcp.json` 中或内联在 `plugin.json` 中定义 MCP 服务器
* 当您启用插件时，Claude Code 自动启动其 MCP 服务器
* Claude Code 将插件 MCP 工具与手动配置的 MCP 工具一起提供
* 您通过安装或卸载插件来添加和删除插件服务器，而不是使用 `/mcp` 命令。您仍然可以在 `/mcp` 中 [切换已安装的插件服务器关闭](#disable-a-server-without-removing-it)，这会停止 Claude Code 连接到它而不删除插件

**示例插件 MCP 配置**：

在插件根目录的 `.mcp.json` 中：

```json theme={null}
{
  "mcpServers": {
    "database-tools": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_URL": "${DB_URL}"
      }
    }
  }
}
```

或内联在 `plugin.json` 中：

```json theme={null}
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

**插件 MCP 功能**：

* **自动生命周期**：服务器在这些时间点连接和断开：
  * 在会话启动时，Claude Code 自动连接已启用插件的服务器。在 `/mcp` 中，您之前使用过的远程（HTTP 或 SSE）插件服务器可能改为显示 [`cached` 状态](#server-status-detail)；Claude Code 在 Claude 首次调用其工具之一时连接它
  * 如果您在会话期间启用或禁用插件，Claude Code 在更改生效时连接或断开其 MCP 服务器。[在不重新启动的情况下应用插件更改](/docs/zh-CN/plugins/cli-reference#reload-plugins) 说明了生效时间。在没有交互式终端的会话中，`/reload-plugins` 不连接或断开插件 MCP 服务器；这些更改在您的下一个会话中生效
  * 当您重新加载时，Claude Code 保留配置未更改的插件服务器的实时连接，当您从 Agent SDK [替换会话的 MCP 服务器列表](/docs/zh-CN/agent-sdk/typescript#mcpsetserversresult) 而未列出它们时也是如此
  * 当您在 v2.1.246 或更高版本上 [使用 `/cd` 移动会话](/docs/zh-CN/permissions#move-the-session-to-another-directory) 时，Claude Code 连接新目录的设置所启用插件的服务器，并断开不再启用的插件的服务器，因此您无需在移动后运行 `/reload-plugins`
  * 在 [云端会话](/docs/zh-CN/claude-code-on-the-web) 中，对尚未连接的插件服务器的 MCP 调用（例如空闲会话唤醒后）会按需启动服务器并等待它连接
* **路径占位符**：`${CLAUDE_PLUGIN_ROOT}` 解析为插件的安装目录，`${CLAUDE_PLUGIN_DATA}` 解析为其 [持久状态](/docs/zh-CN/plugins/components#path-variables-and-persistent-data) 目录，`${CLAUDE_PROJECT_DIR}` 解析为稳定的项目根目录。替换适用于：
  * `stdio` 服务器：`command`、`args`、`env`
  * `http`、`sse` 和 `ws` 服务器：`url`、`headers` 和 `headersHelper`
* **用户环境访问**：访问与手动配置的服务器相同的环境变量
* **多种传输类型**：支持 stdio、SSE、HTTP 和 WebSocket 传输，尽管传输支持可能因服务器而异

插件服务器在 `/mcp` 中出现，并带有表明它们来自插件的指示器。

对于插件的 stdio 服务器，`claude mcp get` 打印 `Command: stdio`、空的 `Args:` 行，并将每个环境变量显示为 `NAME=[REDACTED]`。值被隐藏，因为它们可能携带凭据。

**插件 MCP 工具名称**：

来自插件捆绑的 MCP 服务器的工具在其可调用名称中包含插件名称和服务器键。完整形式是 `mcp__plugin_<plugin-name>_<server-name>__<tool-name>`，其中 `A-Z`、`a-z`、`0-9`、`_` 和 `-` 之外的任何字符都被替换为 `_`。对于名为 `my-plugin` 的插件中捆绑的 `database-tools` 服务器，`query` 工具的可调用名称为：

```
mcp__plugin_my-plugin_database-tools__query
```

在 [权限规则](/docs/zh-CN/permissions)、skill 的 `allowed-tools` 列表、[子代理的 `tools` 字段](/docs/zh-CN/sub-agents#available-tools) 或 [hook 匹配器](/docs/zh-CN/hooks#match-mcp-tools) 中引用工具时使用此完整名称。针对裸服务器键编写的 hook 匹配器（例如 `mcp__database-tools__.*`）永远不会为插件捆绑的服务器触发。

服务器本身以限定名称 `plugin:<plugin-name>:<server-name>` 注册，例如 `plugin:my-plugin:database-tools`。在需要配置的服务器名称的地方使用该名称，例如 [`mcp_tool` hook 的 `server` 字段](/docs/zh-CN/hooks#mcp-tool-hook-fields)。

有关使用插件捆绑 MCP 服务器的详细信息，请参阅 [插件组件参考](/docs/zh-CN/plugins/components#mcp-servers)。

<h2 id="mcp-installation-scopes">
  MCP 安装范围
</h2>

MCP 服务器可以在三个不同的范围级别进行配置。您选择的范围控制服务器在哪些项目中加载以及配置是否与您的团队共享。管理员还可以通过[托管配置](#managed-mcp-configuration)为每个用户部署或提供服务器。

| 范围 | 加载位置 | 与团队共享 | 存储位置 |
| - | - | - | - |
| [本地](#local-scope) | 仅当前项目 | 否 | `~/.claude.json` |
| [项目](#project-scope) | 仅当前项目 | 是，通过版本控制 | 项目根目录中的 `.mcp.json` |
| [用户](#user-scope) | 您的所有项目 | 否 | `~/.claude.json` |

<h3 id="local-scope">
  本地范围
</h3>

本地范围是默认范围。本地范围的服务器仅在您添加它的项目中加载，并对您保持私密。Claude Code 将其存储在 `~/.claude.json` 中该项目的路径下，因此相同的服务器不会出现在您的其他项目中。对个人开发服务器、实验配置或包含您不想在版本控制中的凭据的服务器使用本地范围。

<Note>
  MCP 服务器的"本地范围"术语与一般本地设置不同。MCP 本地范围的服务器存储在 `~/.claude.json`（您的主目录）中，而一般本地设置使用 `.claude/settings.local.json`（在项目目录中）。有关设置文件位置的详细信息，请参阅[设置](/docs/zh-CN/settings#where-settings-live)。
</Note>

```bash theme={null}
# 添加本地范围的服务器（默认）
claude mcp add --transport http stripe https://mcp.stripe.com

# 显式指定本地范围
claude mcp add --transport http stripe --scope local https://mcp.stripe.com
```

该命令将服务器写入 `~/.claude.json` 中您当前项目的条目。下面的示例显示从 `/path/to/your/project` 运行时的结果：

```json theme={null}
{
  "projects": {
    "/path/to/your/project": {
      "mcpServers": {
        "stripe": {
          "type": "http",
          "url": "https://mcp.stripe.com"
        }
      }
    }
  }
}
```

<h3 id="project-scope">
  项目范围
</h3>

项目范围的服务器通过在项目根目录中存储配置在 `.mcp.json` 文件中来启用团队协作。当您添加项目范围的服务器时，Claude Code 会自动创建或更新此文件，使用适当的配置结构。将 `.mcp.json` 检入版本控制，以便您团队中的每个人都能获得相同的 MCP 工具和服务。

```bash theme={null}
# 添加项目范围的服务器
claude mcp add --transport http shared-server --scope project https://example.com/mcp
```

生成的 `.mcp.json` 文件遵循标准化格式：

```json theme={null}
{
  "mcpServers": {
    "shared-server": {
      "type": "http",
      "url": "https://example.com/mcp"
    }
  }
}
```

出于安全原因，Claude Code 在交互式会话中使用来自 `.mcp.json` 文件的项目范围的服务器之前会提示批准。要重置这些批准选择，请运行 `claude mcp reset-project-choices`。

在 `claude -p` 运行、[Agent SDK](/docs/zh-CN/headless) 会话和[云会话](/docs/zh-CN/claude-code-on-the-web)中，Claude Code 无法显示该提示：它加载项目范围的服务器而不询问。Claude Code 还会在您以 `bypassPermissions` 模式启动的会话中跳过提示，其中用户设置或托管设置中设置了 [`skipDangerousModePermissionPrompt`](/docs/zh-CN/settings-reference#skipdangerousmodepermissionprompt)。要无论如何保持服务器不加载：

* 将其添加到 [`disabledMcpjsonServers`](/docs/zh-CN/settings-reference#disabledmcpjsonservers)，这会在每个权限模式中阻止它。
* 使用 [`--setting-sources`](/docs/zh-CN/cli-reference#cli-flags) 或 SDK 的 `settingSources` 选项完全排除项目设置。
* 使用 [`--strict-mcp-config`](/docs/zh-CN/cli-reference#cli-flags) 启动会话。Claude Code 随后仅使用您通过 `--mcp-config` 传递的 MCP 服务器。跳过 Claude Code 未加载的项目范围服务器的批准提示需要 Claude Code v2.1.246 或更高版本；在 v2.1.246 之前，严格会话仍然会等待它们的批准，这会导致后台会话在启动时等待。有关该标志在托管 MCP 文件下的作用，请参阅[使用 managed-mcp.json 进行独占控制](/docs/zh-CN/managed-mcp#exclusive-control-with-managed-mcp-json)。

[项目服务器批准和工作区信任](#project-server-approvals-and-workspace-trust)涵盖了提交到存储库的批准如何与工作区信任交互。

<h3 id="user-scope">
  用户范围
</h3>

用户范围的服务器存储在 `~/.claude.json` 中，并提供跨项目可访问性，使其在您机器上的所有项目中可用，同时对您的用户帐户保持私密。此范围适用于个人实用程序服务器、开发工具或您在不同项目中经常使用的服务。

```bash theme={null}
# 添加用户服务器
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

<h3 id="scope-hierarchy-and-precedence">
  范围层次结构和优先级
</h3>

当具有相同名称的服务器在多个位置定义时，Claude Code 连接到它一次，使用来自最高优先级源的定义。整个服务器条目来自该源；字段不会跨范围合并。

1. 本地范围
2. 项目范围
3. 用户范围
4. [插件提供的服务器](/docs/zh-CN/plugins/components#mcp-servers)
5. [claude.ai 连接器](#use-mcp-servers-from-claude-ai)

Claude Code 按名称匹配三个范围中的重复项。插件和连接器按端点匹配，因此指向与上述服务器相同的 URL 或命令的连接器被视为重复项。

当两个 URL 拼写仅在方案或主机的字母大小写、方案的默认端口（例如 `https` 上的 `:443`）或尾部斜杠方面不同时，它们被视为相同的端点。不同的路径、查询字符串、用户信息或非默认端口会使两个服务器不同。

您的组织通过 [`managedMcpServers`](/docs/zh-CN/managed-mcp#provide-servers-through-managed-settings) 托管设置提供的服务器排名高于所有这些，因此当其中一个重复它时，Claude Code 连接组织的定义。需要 Claude Code v2.1.259 或更高版本。

如果您在[桌面应用的代码选项卡](/docs/zh-CN/desktop#mcp-servers-from-the-claude-desktop-chat-app)中打开本地会话，其中 `~/.claude.json`（用户范围）的顶级和 `.mcp.json` 中具有相同的 stdio 服务器名称，代码选项卡使用 `~/.claude.json` 定义。

<h3 id="environment-variable-expansion-in-mcp-json">
  `.mcp.json` 中的环境变量扩展
</h3>

Claude Code 支持 `.mcp.json` 文件中的环境变量扩展，允许团队共享配置，同时为特定于机器的路径和 API 密钥等敏感值保持灵活性。

<h4 id="supported-syntax">
  支持的语法
</h4>

* `${VAR}`：扩展为环境变量 `VAR` 的值
* `${VAR:-default}`：如果设置了 `VAR`，则扩展为 `VAR`，否则使用 `default`

<h4 id="expansion-locations">
  扩展位置
</h4>

环境变量可以在以下位置扩展：

* `command`：服务器可执行文件路径
* `args`：命令行参数
* `env`：传递给服务器的环境变量
* `url`：对于 HTTP 服务器类型
* `headers`：对于 HTTP 服务器身份验证

<h4 id="example-with-variable-expansion">
  带有变量扩展的示例
</h4>

```json theme={null}
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

<h4 id="unset-variables-without-a-default">
  未设置且无默认值的变量
</h4>

如果未设置所需的环境变量且没有默认值，配置仍然会加载：Claude Code 在 `claude mcp list` 输出中为该服务器报告缺失变量警告，并按原样使用未扩展的 `${VAR}` 文本。设置变量或添加 `:-default` 回退，以便服务器使用您想要的值启动。在远程服务器的 `url` 和 `headers` 中，某些凭据变量[读取为空](#credential-variables-that-read-as-empty)，没有警告。

<h4 id="credential-variables-that-read-as-empty">
  读取为空的凭据变量
</h4>

在远程服务器的 `url` 和 `headers` 中，Claude Code 从您的环境中读取凭据变量为空，而不是扩展它们。这可以防止项目的 `.mcp.json` 或插件将您的 Claude Code 或云提供商凭据发送到它命名的服务器。如果您写入 `Bearer ${ANTHROPIC_AUTH_TOKEN}`，服务器会收到 `Bearer ` 而没有凭据，并拒绝请求，通常返回 `401`。Claude Code 将其报告为连接失败。

涵盖的名称包括：

* Claude Code 自己的凭据，例如 `ANTHROPIC_API_KEY` 和 `ANTHROPIC_AUTH_TOKEN`
* 您的云提供商的凭据，例如 `AWS_BEARER_TOKEN_BEDROCK`
* 您的环境携带的其他凭据，例如 `HTTPS_PROXY` 和 `NPM_TOKEN`

涵盖的名称读取为空，无论您是否设置了变量，其上的 `:-default` 回退被忽略。提供商基础 URL（例如 `ANTHROPIC_BASE_URL`）仍然会扩展，因此 `"url": "${ANTHROPIC_BASE_URL}/mcp"` 有效，除非 URL 的值本身嵌入凭据（例如用户名和密码）。

此集合之外的名称（例如 `API_KEY`）按原样扩展。要向服务器提供涵盖的凭据之一，请将其复制到具有您自己的名称的变量中，并改为引用该名称。

当远程服务器的 `url` 或 `headers` 引用您已设置的涵盖变量时，Claude Code 在调试日志行中命名它。要读取该行，请运行 `claude --debug-file /tmp/claude-debug.log` 并在该文件中搜索 `never expanded toward a remote server`。

<h4 id="how-references-appear-in-/mcp-and-cli-output">
  引用在 `/mcp` 和 CLI 输出中的显示方式
</h4>

对于本地、项目或用户[范围](#mcp-installation-scopes)中的服务器，以下界面按名称而不是按其解析值显示 `${VAR}` 引用：

* 服务器的 `/mcp` 详细视图中的 URL 或命令行
* `claude mcp list` 和 `claude mcp get` 输出

`/mcp` 详细视图在 Claude Code v2.1.268 或更高版本中以这种方式显示引用。

对于您的组织通过 `managedMcpServers` 设置提供的服务器，这些界面仅显示[URL 的主机](/docs/zh-CN/managed-mcp#what-users-can-see-and-change)。

要检查当连接失败时 `claude mcp list`、`claude mcp get` 和 `/mcp` 显示的内容，请参阅[服务器状态详情](#server-status-detail)。

<h2 id="practical-examples">
  实际示例
</h2>

<h3 id="example-connect-to-github-for-code-reviews">
  示例：连接到 GitHub 进行代码审查
</h3>

GitHub 的远程 MCP 服务器使用作为标头传递的 GitHub 个人访问令牌进行身份验证。要获取一个，请打开您的 [GitHub 令牌设置](https://github.com/settings/personal-access-tokens)，生成一个新的细粒度令牌，具有对您希望 Claude 使用的存储库的访问权限，然后添加服务器：

```bash theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer YOUR_GITHUB_PAT"
```

将 `YOUR_GITHUB_PAT` 替换为您的个人访问令牌。`claude mcp add` 命令保存配置而不验证凭据，因此此处接受占位符值，但服务器稍后无法连接。要验证连接，请运行 `/mcp` 并检查服务器是否显示 `connected`。具有错误凭据的服务器显示 `failed`，失败详情包括服务器返回的 HTTP 状态，例如 401。

然后使用 GitHub：

```text wrap theme={null}
审查 PR #456 并建议改进
```

```text wrap theme={null}
为我们刚发现的错误创建新问题
```

```text wrap theme={null}
显示分配给我的所有开放 PR
```

<h3 id="example-query-your-postgresql-database">
  示例：查询您的 PostgreSQL 数据库
</h3>

[DBHub](https://github.com/bytebase/dbhub)，`@bytebase/dbhub` 包，是一个 MCP 服务器，通过您在 `--dsn` 中传递的连接字符串将 Claude 连接到关系数据库。在连接字符串中使用只读数据库用户，以便 Claude 运行的查询无法修改数据：

```bash theme={null}
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"
```

要确认服务器启动，请运行 `/mcp` 并检查 `db` 是否显示 `connected`。

然后自然地查询您的数据库：

```text wrap theme={null}
本月我们的总收入是多少？
```

```text wrap theme={null}
显示订单表的架构
```

```text wrap theme={null}
查找 90 天内未进行购买的客户
```

<h2 id="authenticate-with-remote-mcp-servers">
  使用远程 MCP 服务器进行身份验证
</h2>

许多基于云的 MCP 服务器需要身份验证。Claude Code 支持 OAuth 2.0 以实现安全连接。

当服务器响应 `401 Unauthorized` 或 `403 Forbidden` 时，Claude Code 会将远程服务器标记为需要身份验证。Claude Code 显示的内容取决于服务器：

* 对于您尚未登录的服务器，任一状态代码都会在 `/mcp` 中标记它，以便您可以完成 OAuth 流程。
* 对于 [claude.ai 连接器](#use-mcp-servers-from-claude-ai)，由 claude.ai 拒绝您的会话令牌导致的 `401` 不会标记连接器，因为重新授权连接器无法修复您的登录。Claude Code 改为显示 [会话令牌被拒绝状态](/docs/zh-CN/errors#claude-ai-rejected-the-session-token)。
* 对于您在 `headers` 中配置了 `Authorization` 标头的服务器，或通过 [`headersHelper`](#use-dynamic-headers-for-custom-authentication) 配置的服务器，连接时的 `401` 或 `403` 不会标记服务器，因为要修复的凭证是您配置的凭证。Claude Code 改为报告连接失败。如果您从 `${VAR}` 引用设置该标头，请检查该变量是否是 Claude Code [读取为空](#credential-variables-that-read-as-empty) 的变量之一。
* 对于 [传递到云会话的连接器](#how-connectors-reach-claude-code)，Claude Code 不运行登录流程，因为会话的代理使用您在 claude.ai 中授予的授权向连接器进行身份验证。当那里的连接器需要再次授权时，请在 [claude.ai/customize/connectors](https://claude.ai/customize/connectors) 重新连接它，而不是从会话中连接。

当对您已登录的 OAuth 服务器的请求返回 `401 Unauthorized` 时，Claude Code 会刷新存储的令牌、重新连接并重试请求一次。只有在该重试也失败时，它才会在 `/mcp` 中标记服务器。在 v2.1.206 之前，由于网络错误等暂时原因导致的令牌刷新失败会将 OAuth 服务器标记为在会话的其余时间内需要身份验证，即使其刷新令牌仍然有效。

当服务器拒绝存储的刷新令牌时，Claude Code 会立即显示一条指向 `/mcp` 的通知。打开 `/mcp` 并在服务器上选择 **Re-authenticate** 以在下一个工具调用失败之前再次登录。

返回指向其授权服务器的 `WWW-Authenticate` 标头的自定义服务器会获得与任何其他远程服务器相同的自动发现。

当一个或多个配置的服务器需要身份验证时，Claude Code 也会显示启动通知，因此您不必打开 `/mcp` 来发现哪些服务器需要登录。该通知仅计算您可以从 Claude Code 登录的服务器。在 v2.1.218 之前，它还计算了在 claude.ai 中未连接的 [claude.ai 连接器](#use-mcp-servers-from-claude-ai)，您只能从 claude.ai 设置中连接这些连接器。

该通知每次宣布每个服务器一次，并在后续启动时将其排除在计数之外，直到该服务器已连接并再次需要登录。`/mcp` 仍然列出每个需要登录的服务器。

在非交互模式下，没有 `/mcp` 面板，因此 Claude Code 无法为您运行 OAuth 流程。从 v2.1.196 开始，当配置的服务器在启用了 [工具搜索](#scale-with-mcp-tool-search)（这是默认设置）的 `claude -p` 或 Agent SDK 运行期间需要身份验证时，Claude Code 会告诉 Claude 该服务器的工具不可用，直到您授权它。Claude 然后可以命名需要登录的服务器，而不是响应就像服务器未配置一样。从使用 `/mcp` 或 `claude mcp login <name>` 的交互式会话完成登录。

如果您为服务器配置了 `headers.Authorization`，而服务器拒绝了该标头，Claude Code 会报告连接失败，而不是回退到 OAuth。检查令牌对 MCP 端点是否有效，或删除标头以使用 OAuth 流程。

<Steps>
  <Step title="添加需要身份验证的服务器">
    如果您已在 [MCP 快速入门](/docs/zh-CN/mcp-quickstart#connect-a-server-that-requires-sign-in) 中添加了 `sentry` 服务器，请跳过此步骤：使用相同的服务器名称在相同的范围内再次运行 `claude mcp add` 会失败，并显示 `MCP server sentry already exists in local config`。否则，运行：

    ```bash theme={null}
    claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
    ```
  </Step>

  <Step title="在 Claude Code 中使用 /mcp 命令">
    在 Claude Code 中，使用命令：

    ```text wrap theme={null}
    /mcp
    ```

    然后按照浏览器中的步骤登录。
  </Step>
</Steps>

<Tip>
  提示：

  * 身份验证令牌存储安全且自动刷新
  * 使用 `/mcp` 菜单中的"Clear authentication"撤销访问权限
  * 如果浏览器未自动打开，请复制提供的 URL 并手动打开
  * 如果浏览器重定向在身份验证后失败并出现连接错误，请将浏览器地址栏中的完整回调 URL 粘贴到 Claude Code 中出现的 URL 提示中
  * OAuth 身份验证适用于 HTTP 服务器
</Tip>

<h3 id="authenticate-from-the-command-line">
  从命令行进行身份验证
</h3>

`claude mcp login <name>` 命令直接从您的 shell 运行配置的服务器的 OAuth 流程，因此您不需要在会话内打开 `/mcp` 面板。

```bash theme={null}
claude mcp login sentry
```

要稍后清除存储的凭证，请运行 `claude mcp logout <name>`。

`claude mcp login` 检测何时没有本地浏览器可用，例如在 SSH 会话期间或在没有显示服务器的 Linux 上，并打印授权 URL 而不是尝试打开浏览器。在您的本地计算机上打开 URL，然后将浏览器地址栏中的完整重定向 URL 粘贴回提示符。该命令需要交互式终端来执行粘贴步骤，因此请使用 `ssh -t` 连接。传递 `--no-browser` 以强制 URL 提示，即使检测到本地浏览器。

```bash theme={null}
claude mcp login sentry --no-browser
```

<h3 id="use-a-fixed-oauth-callback-port">
  使用固定的 OAuth 回调端口
</h3>

某些 MCP 服务器需要预先注册的特定重定向 URI。默认情况下，Claude Code 为 OAuth 回调选择随机可用端口。使用 `--callback-port` 固定端口，使其与 `http://localhost:PORT/callback` 形式的预注册重定向 URI 匹配。如果在 Claude Code v2.1.229 上登录失败并出现重定向 URI 不匹配，请参阅 [使用预配置的 OAuth 凭证](#use-pre-configured-oauth-credentials) 下的版本说明。

您可以单独使用 `--callback-port`（使用动态客户端注册）或与 `--client-id` 一起使用（使用预配置的凭证）。

```bash theme={null}
# 使用动态客户端注册的固定回调端口
claude mcp add --transport http \
  --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

<h3 id="use-pre-configured-oauth-credentials">
  使用预配置的 OAuth 凭证
</h3>

某些 MCP 服务器不支持通过动态客户端注册进行自动 OAuth 设置。如果您看到类似"Incompatible auth server: does not support dynamic client registration"的错误，服务器需要预配置的凭证。Claude Code 也支持使用客户端 ID 元数据文档 (CIMD) 而不是动态客户端注册的服务器，并自动发现这些服务器。如果自动发现失败，请先通过服务器的开发者门户注册 OAuth 应用，然后在添加服务器时提供凭证。

<Steps>
  <Step title="向服务器注册 OAuth 应用">
    通过服务器的开发者门户创建应用并记下您的客户端 ID 和客户端密钥。

    如果注册表单要求重定向 URI，请选择任何可用端口并输入 `http://localhost:PORT/callback`，其中包含该端口。您将在下一步中使用相同的端口。

    在 v2.1.229 中，Claude Code 改为发送 `http://127.0.0.1:PORT/callback`，而精确匹配注册重定向 URI 的服务器会以重定向 URI 不匹配拒绝登录。Claude Code v2.1.231 恢复了 `localhost` 形式。要在 v2.1.229 上恢复，请升级 Claude Code，或临时将 `http://127.0.0.1:PORT/callback` 形式添加到服务器的注册重定向 URI。
  </Step>

  <Step title="使用您的凭证添加服务器">
    这些选项卡涵盖两个命令：`claude mcp add` 将您的客户端 ID 和回调端口作为标志，`claude mcp add-json` 在 `oauth` 对象中获取它们。如果您注册了重定向 URI，请将回调端口设置为该 URI 中的端口。

    <Tabs>
      <Tab title="claude mcp add">
        使用 `--client-id` 传递您的应用的客户端 ID。`--client-secret` 标志使用掩码输入提示输入密钥：

        ```bash theme={null}
        claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>

      <Tab title="claude mcp add-json">
        在 JSON 配置中包含 `oauth` 对象，并将 `--client-secret` 作为单独的标志传递：

        ```bash theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' \
          --client-secret
        ```
      </Tab>

      <Tab title="claude mcp add-json (仅回调端口)">
        要仅固定回调端口并让 Claude Code 自动注册客户端，请单独设置 `callbackPort`：

        ```bash theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"callbackPort":8080}}'
        ```
      </Tab>

      <Tab title="CI / 环境变量">
        通过环境变量设置密钥以跳过交互式提示：

        ```bash theme={null}
        MCP_CLIENT_SECRET=your-secret claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="在 Claude Code 中进行身份验证">
    在 Claude Code 中运行 `/mcp` 并按照浏览器登录流程。
  </Step>
</Steps>

<Tip>
  提示：

  * 客户端密钥安全地存储在您的系统钥匙链 (macOS) 或凭证文件中，而不是在您的配置中
  * 您只能在添加服务器时设置客户端密钥。当您使用 `claude mcp login` 或从 `/mcp` 进行身份验证时，Claude Code 使用存储的密钥，不会提示输入密钥或读取 `MCP_CLIENT_SECRET`
  * 要稍后添加或更改密钥，请使用 `claude mcp remove <name>` 删除服务器，然后使用 `--client-secret` 和相同的 `--scope` 再次添加它
  * 如果服务器使用没有密钥的公共 OAuth 客户端，请仅使用 `--client-id` 而不使用 `--client-secret`
  * 这些标志仅适用于 HTTP 和 SSE 传输。它们对 stdio 服务器没有影响
  * 使用 `claude mcp get <name>` 验证为服务器配置了 OAuth 凭证
</Tip>

<h3 id="override-oauth-metadata-discovery">
  覆盖 OAuth 元数据发现
</h3>

指向 Claude Code 特定的 OAuth 授权服务器元数据 URL 以绕过默认发现链。当 MCP 服务器的标准端点出错时，或当您想通过内部代理路由发现时，设置 `authServerMetadataUrl`。默认情况下，Claude Code 首先检查 `/.well-known/oauth-protected-resource` 处的 RFC 9728 受保护资源元数据，然后回退到 `/.well-known/oauth-authorization-server` 处的 RFC 8414 授权服务器元数据。

在 `.mcp.json` 中您的服务器配置的 `oauth` 对象中设置 `authServerMetadataUrl`：

```json theme={null}
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}
```

URL 必须使用 `https://`。元数据 URL 的 `scopes_supported` 覆盖上游服务器宣传的范围。

<h3 id="restrict-oauth-scopes">
  限制 OAuth 范围
</h3>

设置 `oauth.scopes` 以固定 Claude Code 在授权流程期间请求的范围。这是当上游授权服务器宣传的范围超过您想要授予的范围时，将 MCP 服务器限制为安全团队批准的子集的受支持方式。该值是单个空格分隔的字符串，与 RFC 6749 §3.3 中的 `scope` 参数格式匹配。

```json theme={null}
{
  "mcpServers": {
    "slack": {
      "type": "http",
      "url": "https://mcp.slack.com/mcp",
      "oauth": {
        "scopes": "channels:read chat:write search:read"
      }
    }
  }
}
```

`oauth.scopes` 优先于 `authServerMetadataUrl` 和服务器在 `/.well-known` 处发现的范围。将其保留为未设置以让 MCP 服务器确定请求的范围集。

从 v2.1.196 开始，当未设置 `oauth.scopes` 时，Claude Code 请求服务器的 `WWW-Authenticate` 标头或其受保护资源元数据提供的范围，当两者都不提供时不发送 `scope` 参数。它不再从自动发现的授权服务器元数据请求完整的 `scopes_supported` 目录。请求该目录导致宣传仅限管理员或模板范围的身份提供者以 `invalid_scope` 错误拒绝授权请求。从配置的 `authServerMetadataUrl` 获取的元数据仍然将其 `scopes_supported` 作为请求的范围提供。

如果授权服务器在 `scopes_supported` 中宣传 `offline_access`，Claude Code 会将其附加到固定范围，以便可以在没有新浏览器登录的情况下刷新访问令牌。

如果服务器稍后为工具调用返回 403 `insufficient_scope`，调用会失败并显示 [`needs additional permissions`](/docs/zh-CN/errors#mcp-server-needs-you-to-sign-in-again) 消息，该消息命名服务器要求的范围。该服务器在 `/mcp` 中显示为需要身份验证。

如果该范围不在您的固定 `oauth.scopes` 中，请添加它，然后运行 `/mcp` 并再次对服务器进行身份验证。Claude Code 请求固定范围而不是服务器命名的范围，因此如果您在不添加它的情况下再次进行身份验证，您获得的令牌仍然缺少它。

<h3 id="use-dynamic-headers-for-custom-authentication">
  使用动态标头进行自定义身份验证
</h3>

如果您的 MCP 服务器使用 OAuth 以外的身份验证方案，例如 Kerberos、短期令牌或内部 SSO，请使用 `headersHelper` 在连接时生成请求标头。Claude Code 运行命令并将其输出合并到连接标头中。

```json theme={null}
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "/opt/bin/get-mcp-auth-headers.sh"
    }
  }
}
```

该命令也可以是内联的：

```json theme={null}
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "echo '{\"Authorization\": \"Bearer '\"$(get-token)\"'\"}'"
    }
  }
}
```

**要求：**

* 该命令必须将字符串键值对的 JSON 对象写入 stdout
* Claude Code 在 shell 中运行该命令，并在 10 秒后放弃
* Claude Code 通过 [您配置服务器的位置](#where-the-helper-runs) 选择命令的工作目录，因此将脚本作为绝对路径给出或将其放在 `PATH` 上
* 动态标头覆盖任何具有相同名称的静态 `headers`

Claude Code 在每次连接时运行助手，在会话启动和重新连接时，一旦 [项目和本地范围服务器的信任规则](#trust-a-folder-before-its-headershelper-runs) 允许它运行。它不缓存结果，因此您的脚本负责任何令牌重用。

如果工具调用返回 `401 Unauthorized` 或 `403 Forbidden`，Claude Code 会自动在相同规则下重新运行助手，使用新标头重新连接，并重试调用一次。Claude Code 仅在该重试也失败时才在 `/mcp` 中将服务器标记为需要身份验证。

当助手的输出包含 `Authorization` 标头时，Claude Code 使用该凭证作为服务器的身份验证，不会回退到服务器的 OAuth。

如果服务器在连接时拒绝助手的凭证，Claude Code 会报告连接失败，而不是将服务器标记为需要身份验证。修复您的助手返回的凭证，然后从 `/mcp` 重新连接以重新运行助手。

Claude Code 在执行助手时设置这些环境变量：

| 变量 | 值 |
| :- | :- |
| `CLAUDE_CODE_MCP_SERVER_NAME` | MCP 服务器的名称 |
| `CLAUDE_CODE_MCP_SERVER_URL` | MCP 服务器的 URL |
| `CLAUDE_PLUGIN_ROOT` | 插件的根目录。仅当 [插件](/docs/zh-CN/plugins/components#mcp-servers) 提供服务器时设置 |

使用这些来编写为多个 MCP 服务器服务的单个助手脚本。

插件提供的 `headersHelper` 无法引用插件的 [`${user_config.*}`](/docs/zh-CN/plugins/manifest-reference#user-configuration) 值，因为该命令通过 shell 运行。Claude Code 报告服务器配置错误并显示 [错误](/docs/zh-CN/errors#plugin-command-references-user-config)，不替换该值。将 `${user_config.KEY}` 放在服务器的 `headers` 字段中，该字段不是 shell 解析的，或让助手脚本从配置文件读取该值。在 v2.1.207 之前，`headersHelper` 替换了 `${user_config.*}` 值。

<h4 id="where-the-helper-runs">
  助手运行的位置
</h4>

Claude Code 从声明服务器的配置中选择 `headersHelper` 命令的工作目录。Claude 在 Bash 中运行的 `cd` 不会移动它，[`/cd`](/docs/zh-CN/permissions#move-the-session-to-another-directory) 仅对从会话主工作目录运行的服务器移动它。下面的每一行给出您的 `headersHelper` 命令中相对路径解析的目录。

| 您配置服务器的位置 | 工作目录 |
| :- | :- |
| [插件](/docs/zh-CN/plugins/components#mcp-servers) | 插件的根目录 |
| 项目 `.mcp.json` 或 [本地范围](#local-scope) 服务器 | 声明服务器的项目目录 |
| 您项目中的代理文件、来自 SDK 的 `mcpServers` 选项或 `setMcpServers()` 方法的服务器，或 [`--mcp-config`](/docs/zh-CN/cli-reference) | 会话的 [主工作目录](/docs/zh-CN/permissions#working-directories) |
| [用户范围](#user-scope)、[托管 MCP](/docs/zh-CN/managed-mcp)、[claude.ai 连接器](#use-mcp-servers-from-claude-ai)，或来自您项目外的代理文件，包括来自 `--add-dir` 目录的代理文件 | 您的配置目录，`~/.claude` 除非您设置 [`CLAUDE_CONFIG_DIR`](/docs/zh-CN/env-vars) |

在 v2.1.238 之前，Claude Code 也从您启动它的目录运行用户范围、托管和 claude.ai 连接器服务器的助手，以及来自您项目外的代理文件。

<h4 id="which-variables-a-helper-can-read">
  助手可以读取哪些变量
</h4>

存储库或插件提供的 `headersHelper` 是您没有编写的命令，因此 Claude Code 运行它时不使用来自您环境的凭证变量，例如 `ANTHROPIC_API_KEY`。您配置服务器的位置决定这是否适用：

* **已删除**：项目 `.mcp.json` 中的服务器或在插件中，以及来自您项目或 `--add-dir` 目录的代理文件中的内联服务器
* **未删除**：[用户](#user-scope) 或 [本地范围](#local-scope) 的服务器、[托管 MCP](/docs/zh-CN/managed-mcp) 中的服务器、来自 [claude.ai 连接器](#use-mcp-servers-from-claude-ai) 的服务器、由 SDK 或 [`--mcp-config`](/docs/zh-CN/cli-reference) 提供的服务器，以及来自 `~/.claude/agents/` 的代理文件中的内联服务器、来自托管设置的服务器或使用 `--agents` 传递的服务器

除了 Git 的 `GIT_CONFIG_KEY_<n>` 变量外，Claude Code 会从您的环境中删除每个名称看起来像凭证的变量，例如名称中包含 `TOKEN`、`SECRET`、`PASSWORD`、`KEY` 或 `AUTH` 的名称（无论大小写），因此 `ANTHROPIC_API_KEY` 和 `MY_REGISTRY_TOKEN` 都被删除。Claude Code 也删除了一个固定的凭证变量列表，其名称不遵循该模式，例如 `ANTHROPIC_CUSTOM_HEADERS`。

当这适用于您的助手时，让脚本从文件或凭证存储读取其凭证。如果服务器的 `url` [携带这些变量之一的实时值](#environment-variable-expansion-in-mcp-json)，例如 `MY_REGISTRY_TOKEN`，助手接收的 `CLAUDE_CODE_MCP_SERVER_URL` 值也将该部分替换为 `REDACTED`。

<h4 id="trust-a-folder-before-its-headershelper-runs">
  在其 headersHelper 运行之前信任文件夹
</h4>

Claude Code 将 `headersHelper` 作为任意 shell 命令执行。对于项目 `.mcp.json` 中的服务器或 [本地范围](#local-scope) 的服务器，它仅在您接受声明服务器的项目目录的 [信任对话](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust) 后运行助手。在 v2.1.238 之前，`claude -p` 或 SDK 会话运行这些助手而不检查信任，交互式会话在您信任父文件夹后运行它们。

* **不计算的信任**：父文件夹的信任，以及 `claude -p` 或 SDK 会话为 [设置文件中的钩子](/docs/zh-CN/permissions#what-runs-before-you-trust-a-folder) 获得的自动信任
* **直到您信任文件夹**：Claude Code 仅使用其静态 `headers` 连接服务器。在 `claude -p` 或 SDK 会话中，它也会向 stderr 打印每个服务器一行 [`headersHelper not run`](/docs/zh-CN/errors#headershelper-not-run)，告诉您如何授予信任。
* **无对话的信任**：在 `~/.claude.json` 中设置 `projects["<path>"].hasTrustDialogAccepted` 为 `true`。`<path>` 是文件夹 [项目允许规则和工作区信任](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust) 说 Claude Code 将信任键入的文件夹。

Claude Code 对声明为内联的服务器应用相同的规则，在 [代理文件](/docs/zh-CN/sub-agents#scope-mcp-servers-to-a-subagent) 中，检查该代理文件来自何处：您的项目，对于其 `.claude/agents/` 目录中的文件，或 `--add-dir` 目录。直到您 [信任该项目或目录本身](/docs/zh-CN/permissions#what-runs-before-you-trust-a-folder)，Claude Code 不加载服务器，因此其助手也永远不会运行。

<h2 id="add-mcp-servers-from-json-configuration">
  从 JSON 配置添加 MCP 服务器
</h2>

如果您有 MCP 服务器的 JSON 配置，您可以直接添加它：

<Steps>
  <Step title="从 JSON 添加 MCP 服务器">
    ```bash theme={null}
    # 基本语法
    claude mcp add-json <name> '<json>'

    # 示例：添加带有 JSON 配置的 HTTP 服务器
    claude mcp add-json weather-api '{"type":"http","url":"https://api.weather.com/mcp","headers":{"Authorization":"Bearer token"}}'

    # 示例：添加带有 JSON 配置的 stdio 服务器
    claude mcp add-json local-weather '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'

    # 示例：添加带有预配置 OAuth 凭据的 HTTP 服务器
    claude mcp add-json my-server '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' --client-secret
    ```
  </Step>

  <Step title="验证服务器已添加">
    ```bash theme={null}
    claude mcp get weather-api
    ```
  </Step>
</Steps>

<Tip>
  提示：

  * 确保 JSON 在您的 shell 中正确转义
  * JSON 必须符合 MCP 服务器配置架构
  * 您可以使用 `--scope user` 将服务器添加到您的用户配置而不是项目特定的配置
</Tip>

<h2 id="import-mcp-servers-from-claude-desktop">
  从 Claude Desktop 导入 MCP 服务器
</h2>

如果您已在 Claude Desktop 中配置了 MCP 服务器，您可以导入它们：

<Steps>
  <Step title="从 Claude Desktop 导入服务器">
    ```bash theme={null}
    # 基本语法 
    claude mcp add-from-claude-desktop 
    ```
  </Step>

  <Step title="选择要导入的服务器">
    运行命令后，您将看到一个交互式对话框，允许您选择要导入的服务器。
  </Step>

  <Step title="验证服务器已导入">
    ```bash theme={null}
    claude mcp list 
    ```
  </Step>
</Steps>

通过 `claude mcp` 命令添加的服务器名称只能包含字母、数字、连字符和下划线。Claude Desktop 不应用该限制，因此名称中包含任何其他字符（如空格）的 Claude Desktop 服务器无法导入。导入会报告它拒绝的每个名称，并仍然导入您选择的其他服务器。在 v2.1.205 之前，第一个无效名称会停止导入，所选的服务器都不会被添加。

<Tip>
  提示：

  * 此功能仅在 macOS 和 Windows Subsystem for Linux (WSL) 上有效
  * 它从这些平台上的标准位置读取 Claude Desktop 配置文件
  * 使用 `--scope user` 标志将服务器添加到您的用户配置
  * 导入的服务器将保持与 Claude Desktop 中相同的名称，当名称仅包含字母、数字、连字符和下划线时。Claude Code 会报告名称中包含任何其他字符的服务器并跳过它
  * 如果具有相同名称的服务器已存在，它们将获得数字后缀（例如，`server_1`）
</Tip>

<h2 id="use-mcp-servers-from-claude-ai">
  使用来自 claude.ai 的 MCP 服务器
</h2>

如果您已使用 [claude.ai](https://claude.ai) 账户登录 Claude Code，您在 claude.ai 中添加的 MCP 服务器（称为 [connectors](https://claude.com/docs/connectors)）会自动在 Claude Code 中可用：

<Steps>
  <Step title="在 claude.ai 中配置 MCP 服务器">
    在 [claude.ai/customize/connectors](https://claude.ai/customize/connectors) 添加服务器。在 Team 和 Enterprise 计划中，只有管理员可以添加服务器。
  </Step>

  <Step title="对 MCP 服务器进行身份验证">
    在 claude.ai 中完成任何必需的身份验证步骤。
  </Step>

  <Step title="在 Claude Code 中查看和管理服务器">
    在 Claude Code 中，使用命令：

    ```text wrap theme={null}
    /mcp
    ```

    来自 claude.ai 的服务器会出现在列表中，并带有指示符显示它们来自 claude.ai。
  </Step>
</Steps>

Anthropic 本身也提供一些 connectors，无需您或管理员添加。在 [Claude Docs](/docs/zh-CN/artifacts#write-a-document-with-claude-docs) 可用的账户上，`/mcp` 列出 `claude.ai Claude Docs`，无需设置，当您要求创建供他人使用的文档时，Claude 会使用它。要关闭它，请将 `"claude.ai Claude Docs"` 的 `serverName` 条目添加到 `deniedMcpServers`，或使用 `/mcp` 切换，两者都在 [禁用 claude.ai connectors](#disable-claude-ai-connectors) 中描述。

当您的组织在 claude.ai 中管理其身份验证时，Claude Code 在 `/mcp` 和 [`/plugin`](/docs/zh-CN/plugins/install) 管理器中将 connector 标记为 `managed`。Managed 状态不会改变 Claude Code 连接到 connector 的方式或应用您组织的 [工具控制](#organization-controls-on-connector-tools)。

您从未登录过的 Connectors 会折叠在 claude.ai 部分末尾的 `Show unused connectors` 行后面，因此组织预配的列表不会填满面板。选择该行以展开它们。您之前登录过的 connector 即使当前需要重新身份验证，也会保持可见。

Connectors 来自 claude.ai 仅在您的活跃 [身份验证方法](/docs/zh-CN/authentication#authentication-precedence) 是 claude.ai 订阅登录时才会获取。即使您之前运行过 `/login`，在以下情况下也不会加载：

* `ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN` 或 `apiKeyHelper` 处于活跃状态
* 第三方提供商（如 Amazon Bedrock 或 Google Cloud 的 Agent Platform）处于活跃状态
* `ANTHROPIC_PROFILE`、联合变量或活跃的 [Anthropic 配置文件](/docs/zh-CN/authentication#anthropic-profiles-and-federation-credentials) 提供凭据
* `CLAUDE_CODE_OAUTH_TOKEN` 持有来自 [`claude setup-token`](/docs/zh-CN/authentication#generate-a-long-lived-token) 的令牌，该令牌只能进行模型请求

如果 `/mcp` 没有列出您添加的 connector，请运行 `/status` 以确认哪个身份验证方法处于活跃状态。取消设置该环境变量，删除 `apiKeyHelper` 设置，或 [关闭配置文件](/docs/zh-CN/authentication#anthropic-profiles-and-federation-credentials)，然后运行 `/login` 以选择您的 claude.ai 账户。

如果临时网络问题导致您的会话启动时 connector 列表无法加载，Claude Code 会在后台重试最多三次，一旦重试成功，connectors 就会出现。如果它们仍未出现，请重启 Claude Code 以再次获取列表。

如果 `/mcp` 显示 connector 为 `session token rejected`，或其详细视图显示 [`claude.ai rejected the session token`](/docs/zh-CN/errors#claude-ai-rejected-the-session-token)，则 claude.ai 拒绝了您的 Claude Code 登录中的令牌。再次授权 connector 不会清除此状态，因为被拒绝的不是 connector 在 claude.ai 中的自身授权。要清除它：

1. 运行 `/login` 以重新登录。
2. 从 `/mcp` 重新连接 connector。

在 v2.1.222 之前，Claude Code 将 connectors 标记为需要身份验证，授权它们无法解决此问题。

您在 Claude Code 中添加的服务器[优先于](#scope-hierarchy-and-precedence)指向相同 URL 的 claude.ai connector。发生这种情况时，`/mcp` 将 connector 列为隐藏，并显示如何删除重复项（如果您更希望使用 connector）。

某些 Anthropic 托管的 connectors（如 Microsoft 365、Gmail 和 Google Calendar）不支持来自 Claude Code 的本地 OAuth，因为上游身份提供商仅接受 claude.ai 注册的重定向 URL。当您使用 `claude mcp add` 或在 `.mcp.json` 中添加的服务器指向这些主机之一，并且您从 `/mcp` 或使用 `claude mcp login` 登录时，Claude Code 会显示 [`is Anthropic-hosted and doesn't support local OAuth`](/docs/zh-CN/errors#anthropic-hosted-and-doesnt-support-local-oauth)，指导您改为在 [claude.ai/customize/connectors](https://claude.ai/customize/connectors) 连接该服务。

在您使用 `claude mcp remove <name>` 删除您的条目并在 claude.ai 上连接该服务后，connector 会自动出现在 Claude Code 中。

<h3 id="how-connectors-reach-claude-code">
  Connectors 如何到达 Claude Code
</h3>

哪些设置管理 claude.ai connector 取决于您的会话在哪里运行，因为只有某些会话从 claude.ai 本身获取 connectors。下表中的每一行命名 connectors 在一种会话中的到达方式以及在那里控制它们的内容。桌面应用的 [WSL 会话](/docs/zh-CN/desktop-wsl#what-works-in-a-wsl-session) 没有行，因为 connectors 在其中尚不可用。

| 会话运行的位置 | Connectors 如何到达 | 什么管理它们 |
| :- | :- | :- |
| 终端、[VS Code](/docs/zh-CN/vs-code)、[JetBrains](/docs/zh-CN/jetbrains) 和 [Agent SDK](/docs/zh-CN/agent-sdk/claude-code-features) 会话 | Claude Code 从 claude.ai 获取它们 | 本部分中的设置和 [managed MCP 配置](/docs/zh-CN/managed-mcp) |
| [云端会话](/docs/zh-CN/claude-code-on-the-web) | 云主机传入它们 | 您的 claude.ai 组织设置，加上到达会话的 [允许列表和拒绝列表](/docs/zh-CN/managed-mcp#policy-based-control-with-allowlists-and-denylists) 设置以及运行它的主机上的任何 `managed-mcp.json` |
| [桌面应用](/docs/zh-CN/desktop) 的本地和 SSH 会话 | 桌面应用在进程中传入它们 | 您组织的 [connector 工具控制](#organization-controls-on-connector-tools) 中的 `blocked` 条目 |

[`disableClaudeAiConnectors`](#disable-claude-ai-connectors)、`ENABLE_CLAUDEAI_MCP_SERVERS` 和 [`allowAllClaudeAiMcps`](/docs/zh-CN/settings-reference#allowallclaudeaimcps) 仅作用于第一行，即 Claude Code 自身获取的 connectors。其他两行在这些方面与它不同：

* **云端会话**：到达会话的 `allowedMcpServers` 和 `deniedMcpServers` 条目（例如通过 [server-managed 设置](/docs/zh-CN/server-managed-settings)）也会过滤传入的 connectors。会话的代理重写每个 connector 的 URL，因此为 connector 自身 URL 编写的 `serverUrl` 模式不会匹配它。要在自托管环境中的 URL 允许列表旁边允许传入的 connectors，请添加 [Connector 流量离开您的网络](/docs/zh-CN/self-hosted-environments-deploy#connector-traffic-leaves-your-network) 下列出的 `serverUrl` 条目。当运行会话的主机上存在 `managed-mcp.json` 时（例如 [self-hosted runner 主机](/docs/zh-CN/self-hosted-environments-configuration#mcp-servers)），Claude Code 会删除传入的 connectors，无论您是否设置 `allowAllClaudeAiMcps`。
* **桌面应用本地和 SSH 会话**：桌面应用将 connectors 注册为进程内 `type: "sdk"` 服务器，没有 MCP 设置或 `managed-mcp.json` 到达它们。用户通过在 [claude.ai/customize/connectors](https://claude.ai/customize/connectors) 断开连接来将 connector 排除在自己的会话之外。组织阻止 connector 的 [工具](#organization-controls-on-connector-tools) 或完全关闭 [桌面应用中的 Claude Code](/docs/zh-CN/desktop#admin-console-controls)。

<h3 id="organization-controls-on-connector-tools">
  组织对 connector 工具的控制
</h3>

您的组织可以在 [claude.ai connectors](https://claude.com/docs/connectors) 上设置每个工具的控制。Claude Code 在启动时读取这些设置并在本地强制执行它们，除了桌面应用的 [本地和 SSH 会话](#how-connectors-reach-claude-code)。在那里，桌面应用在传入 connector 之前扣留 `blocked` 工具，`ask` 设置不会到达 Claude Code，因此它将会话的普通 [权限规则](/docs/zh-CN/permissions) 应用于这些工具，而不是在每次调用时提示。在 Claude Code 自身获取 connectors 的会话中，运行 `/mcp` 以查看哪个设置适用于 connector 上的每个工具。

* **工具设置为 `ask`**：Claude Code 在每次调用时提示，原因是 `Your organization requires approval for this tool`。即使在 `acceptEdits`、`auto` 和 `bypassPermissions` [权限模式](/docs/zh-CN/permissions#permission-modes) 中，提示也会出现，并且从不提供记住您选择的选项。匹配该工具的 [Allow 规则](/docs/zh-CN/permissions) 也不会跳过提示。在 `dontAsk` 模式中（从不提示），Claude Code 会改为拒绝调用。
* **工具设置为 `blocked`**：Claude Code 在 Claude 看到它之前过滤掉该工具，因此它从不出现在 Claude 的工具列表中。在 Claude Code 自身获取 connectors 的会话中，`/mcp` 工具列表仍然显示该工具，标记为 `disabled by your organization`。

桌面应用和 claude.ai 聊天应用相同的 `blocked` 设置，因此 Claude 也无法在那里使用被阻止的工具，您无法从桌面应用的会话中扣留工具，同时在聊天中保持其可用。桌面应用跳过其所有工具都被阻止的 connector。

<h3 id="disable-claude-ai-connectors">
  禁用 claude.ai connectors
</h3>

Claude Code 仅将 [`disableClaudeAiConnectors`](/docs/zh-CN/settings-reference#disableclaudeaiconnectors) 应用于它 [自身获取](#how-connectors-reach-claude-code) 的 connectors，而不是云主机或桌面应用传入的 connectors。要关闭它获取的 connectors，请在任何设置作用域中将该设置项设置为 `true`：

```json theme={null}
{
  "disableClaudeAiConnectors": true
}
```

此设置使用任何源为真的语义：任何设置源中的 `true` 优先。已检入的项目 `.claude/settings.json` 可以选择退出 Claude Code 自身获取的 connectors，但项目级别的 `false` 无法重新启用用户或策略级别的 `true` 已禁用的 connectors。通过 `--mcp-config` 显式传递的服务器不受影响。

您也可以将 `ENABLE_CLAUDEAI_MCP_SERVERS` 环境变量设置为 `false`，这对当前 shell 会话具有相同的效果：

```bash theme={null}
ENABLE_CLAUDEAI_MCP_SERVERS=false claude
```

要阻止单个 claude.ai connectors 而不是全部，请按名称或 URL 模式将它们添加到 [`deniedMcpServers`](/docs/zh-CN/managed-mcp) 中。例如，`"claude.ai Slack"` 的 `serverName` 条目会阻止 Slack connector。您也可以运行 `/mcp` 以仅为当前项目切换 Claude Code 获取的任何 connector。

<h2 id="use-claude-code-as-an-mcp-server">
  将 Claude Code 用作 MCP 服务器
</h2>

您可以将 Claude Code 本身用作 MCP 服务器，其他应用程序可以连接到它：

```bash theme={null}
# 启动 Claude 作为 stdio MCP 服务器
claude mcp serve
```

该命令启动时不会打印任何内容。stdio MCP 服务器通过 stdin 和 stdout 进行通信，因此沉默的、被阻止的终端意味着服务器正在运行并等待客户端连接。

您可以通过将此配置添加到 claude\_desktop\_config.json 在 Claude Desktop 中使用它：

```json theme={null}
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

<Warning>
  **配置可执行文件路径**：`command` 字段必须引用 Claude Code 可执行文件。如果 `claude` 命令不在您系统的 PATH 中，您需要指定可执行文件的完整路径。

  要查找完整路径：

  ```bash theme={null}
  which claude
  ```

  然后在您的配置中使用完整路径：

  ```json theme={null}
  {
    "mcpServers": {
      "claude-code": {
        "type": "stdio",
        "command": "/full/path/to/claude",
        "args": ["mcp", "serve"],
        "env": {}
      }
    }
  }
  ```

  如果没有正确的可执行文件路径，您会遇到类似 `spawn claude ENOENT` 的错误。
</Warning>

<Tip>
  提示：

  * 在 Claude Desktop 中，尝试要求 Claude 读取目录中的文件、进行编辑等操作。
  * 此 MCP 服务器仅向您的 MCP 客户端公开 Claude Code 的工具，因此您自己的客户端负责为各个工具调用实现用户确认。
</Tip>

<h2 id="mcp-output-limits-and-warnings">
  MCP 输出限制和警告
</h2>

当 MCP 工具产生大量输出时，Claude Code 会帮助管理 token 使用情况，以防止压倒您的对话上下文：

* **输出警告阈值**：当任何 MCP 工具输出超过 10,000 个 token 时，Claude Code 会显示警告
* **可配置限制**：您可以使用 `MAX_MCP_OUTPUT_TOKENS` 环境变量调整允许的最大 MCP 输出 token 数
* **默认限制**：默认最大值为 25,000 个 token
* **范围**：环境变量适用于未声明自己限制的工具。设置了 [`anthropic/maxResultSizeChars`](#raise-the-limit-for-a-specific-tool) 的工具会对文本内容使用该值，而不管 `MAX_MCP_OUTPUT_TOKENS` 设置为什么。返回图像数据的工具仍然受 `MAX_MCP_OUTPUT_TOKENS` 限制
* **超过限制**：当没有图像内容的成功结果超过 token 限制时，Claude Code 会将其保存到文件中，并在对话中用一条消息替换它，该消息指定文件路径，以便 Claude 在需要内容时读取该文件。该文件位于会话的 `tool-results` 目录中，在 [`~/.claude/projects/`](/docs/zh-CN/claude-directory#cleaned-up-automatically) 下。
* **来自 HTTP 和 SSE 服务器的响应大小**：一旦某个 JSON 响应体或事件流中的某个事件在解压后超过 16 MB，Claude Code 就会停止读取来自 [HTTP](#option-1-add-a-remote-http-server) 或 [SSE](#option-2-add-a-remote-sse-server) 服务器的响应。该响应所对应的请求会失败。如果您负责维护该服务器，请减少每个响应返回的数据量以保持在限制之内，例如对结果进行分页

已被 Claude Code [移至后台任务](#automatic-backgrounding-of-long-tool-calls)的调用会通过任务通知报告其结果。对于在前台完成的调用，还有另外两项限制：

* **文本结果的字符限制**：对于未声明 [`anthropic/maxResultSizeChars`](#raise-the-limit-for-a-specific-tool) 的工具，当没有图像内容的成功结果长度超过 50,000 个字符时，无论其 token 数是多少，Claude Code 都会将其保存到文件中。设置 `MAX_MCP_OUTPUT_TOKENS` 不会改变此阈值
* **错误结果**：当工具返回标记为 `isError: true` 的结果时，Claude 会将该结果的文本作为工具的错误消息接收。超过约 11,000 个字符的错误文本只会保留其前 5,000 个和后 5,000 个字符，中间带有一个标记，说明删除了多少个字符

要更改 token 限制，请在启动 Claude Code 之前在您的 shell 中设置 `MAX_MCP_OUTPUT_TOKENS`：

```bash theme={null}
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

<h3 id="raise-the-limit-for-a-specific-tool">
  为特定工具提高限制
</h3>

如果您正在构建 MCP 服务器，可以通过在工具的 `tools/list` 响应条目中设置 `_meta["anthropic/maxResultSizeChars"]` 来允许单个工具返回超过默认持久化到磁盘阈值（50,000 个字符）的结果。Claude Code 会将该工具的阈值提高到注释值，最高可达 500,000 个字符的硬上限。

这对于返回本质上很大但必要的输出的工具很有用，例如数据库 schema 或完整文件树。如果没有注释，超过默认阈值的成功结果会被持久化到磁盘，并在对话中被替换为文件引用。

```json theme={null}
{
  "name": "get_schema",
  "description": "Returns the full database schema",
  "_meta": {
    "anthropic/maxResultSizeChars": 200000
  }
}
```

该注释对文本内容独立于 `MAX_MCP_OUTPUT_TOKENS` 应用，因此用户不需要为声明它的工具提高环境变量。返回图像数据的工具仍然受 token 限制。

<h3 id="images-in-tool-results">
  工具结果中的图像
</h3>

当 MCP 工具返回 PNG、JPEG、GIF 或 WebP 图像时，Claude 会在对话中内联看到该图像。内联副本可能会缩小或压缩以适应模型的图像大小限制。Claude Code 还会将原始字节保存到会话的 `tool-results` 目录中的文件中，该目录位于 [`~/.claude/projects/`](/docs/zh-CN/claude-directory#cleaned-up-automatically) 下，并向 Claude 提供路径。Claude 随后可以使用 Bash 等工具裁剪、转换或重新使用完整分辨率的文件。

如果您使用 [`--no-session-persistence`](/docs/zh-CN/cli-reference#cli-flags) 或 [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](/docs/zh-CN/env-vars) 禁用会话持久化，Claude Code 将不会写入图像文件，Claude 仅接收内联副本。

将 MCP 图像结果保存到文件需要 Claude Code v2.1.283 或更高版本。

<h2 id="tool-input-schemas-with-a-root-level-combinator">
  具有根级组合器的工具输入模式
</h2>

某些 MCP 服务器将工具的输入模式声明为 JSON Schema 联合，在模式的顶级使用 `anyOf`、`oneOf` 或 `allOf`。Claude API 不接受这些关键字在模式根部。它接受嵌套在 `properties` 内的组合器，Claude Code 会原样发送这些组合器。

具有根级组合器的工具保持可用。在将工具发送到 API 之前，Claude Code 将模式展平为单个对象，并在工具描述前面添加一句话，告诉 Claude 哪些参数组属于一起：

* `allOf`：来自每个分支的属性被合并，每个分支的 `required` 列表仍然适用
* `anyOf` 和 `oneOf`：来自每个分支的属性被合并，每个分支的 `required` 列表在工具描述中描述，而不是由模式强制执行

您的服务器接收 Claude 选择的任何参数，因此请继续在服务器端验证组合。

当 Claude Code 无法生成 API 接受的模式，或在未收到启用重写的远程配置的部署上时，它会跳过该工具，在服务器日志中记录原因，并保持服务器的其他工具可用。

<h2 id="tools-with-invalid-input-schemas">
  具有无效输入架构的工具
</h2>

Claude API 检查请求中每个工具的输入架构，当任何一个架构失败时会拒绝整个请求，因此单个 MCP 工具的格式错误的架构会导致包含它的每个请求都以 400 错误失败。Claude Code 在加载服务器的工具时自己运行 API 的两个检查，并排除每个会失败的工具，这样服务器的其他工具可以继续工作：

* 顶级属性名称必须为 1 到 64 个字符长，并且只能使用 ASCII 字母和数字、`_`、`.` 和 `-`
* 架构必须对 JSON Schema draft 2020-12 元架构有效。Claude Code 对未声明 `$schema` 的架构和声明 draft 2020-12 的架构应用此检查。声明任何其他方言的架构会跳过此检查，尽管上面的属性名称检查仍然适用

当 Claude Code 排除一个工具时，它会在服务器的日志中记录原因，并告诉 Claude 它排除了哪些工具以及原因，这样你可以询问 Claude 为什么工具缺失。如果你修复了服务器上的架构，下次 Claude Code 加载服务器的工具时该工具就会回来。

Claude Code 通过从 Anthropic 获取的功能标志打开排除。在 [禁用标志获取的部署](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching) 上，或在标志从未到达的机器上（例如隔离的机器），Claude Code 仍然运行检查并在服务器的日志中记录哪个工具会被拒绝，但仍然将工具的架构发送到 API。API 拒绝包含该架构的请求，并 [以 400 错误按其位置命名工具](/docs/zh-CN/errors#tool-input-schema-is-invalid)。在 v2.1.216 之前，没有部署运行这些检查。

[根级组合器处理](#tool-input-schemas-with-a-root-level-combinator) 是独立的，当标志获取关闭或标志从未到达时保持其自己的行为。

<h2 id="require-approval-for-a-specific-tool">
  要求对特定工具进行批准
</h2>

如果您正在构建 MCP 服务器，可以通过在工具的 `tools/list` 响应条目中将 `_meta["anthropic/requiresUserInteraction"]` 设置为 `true` 来标记工具需要在每次调用时获得明确批准。该值必须是 JSON 布尔值 `true`；任何其他值都会被忽略。

Claude Code 会在每次调用时显示该工具的权限提示，即使在 `acceptEdits`、`auto` 和 `bypassPermissions` [权限模式](/docs/zh-CN/permissions#permission-modes)中也是如此，并且不会为其提供"不再询问"选项。与该工具匹配的 [允许规则](/docs/zh-CN/permissions#permission-rule-syntax)也不会跳过提示。在 `dontAsk` 模式中（从不提示），Claude Code 会拒绝该调用。

提示必须到达一个人。在非交互模式下使用 [`--permission-prompt-tool`](/docs/zh-CN/cli-reference#cli-flags)，来自提示工具的标记工具的 `allow` 结果会被转换为拒绝，消息为 `MCP tool requires user interaction; not supported via --permission-prompt-tool`。Agent SDK 的 [`canUseTool` 回调](/docs/zh-CN/agent-sdk/permissions)确实会接收这些调用并可以批准它们，因为您的 SDK 应用程序应该将它们显示给用户。

将此用于权限提示本身就是目的的工具，例如同意或访问授予步骤，其中自动批准意味着没有人类曾经同意。来自同一服务器的其他工具保持其正常的权限行为。

以下 `tools/list` 条目将一个工具标记为始终需要批准。

```json theme={null}
{
  "name": "grant_access",
  "description": "Requests access to a protected resource",
  "_meta": {
    "anthropic/requiresUserInteraction": true
  }
}
```

某些使用入口，例如 [Remote Control](/docs/zh-CN/remote-control) 和基于 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 构建的应用程序，通常允许您通过一次点击来批准工具调用。对于使用此注解标记的工具，Claude Code 会禁用一次点击操作并显示工具的完整权限提示，因此批准仍然来自回答提示的人，而不是点击。

Claude Code 对任何只有终端对话框才能完整呈现的权限请求（例如带有安全警告或远程使用入口无法显示的始终允许选项的请求）也会以相同方式禁用一次点击批准。您需要在终端对话框中回答该请求，而不是从 Remote Control 中回答。需要 Claude Code v2.1.214 或更高版本。

<h2 id="respond-to-mcp-elicitation-requests">
  响应 MCP 引出请求
</h2>

MCP 服务器可以在任务进行中使用引出功能向你请求结构化输入。当服务器需要无法自行获取的信息时，Claude Code 会显示一个交互式对话框，并将你的响应传回服务器。你无需进行任何配置：当服务器请求引出对话框时，它们会自动出现。

服务器可以通过两种方式请求输入：

* **表单模式**：Claude Code 显示一个对话框，其中包含由服务器定义的表单字段（例如，用户名和密码提示）。填写字段并提交。
* **URL 模式**：Claude Code 询问是否在浏览器中打开链接。服务器使用此模式处理在终端外完成的流程，例如登录。

在 URL 模式中，Claude Code 将 URL 作为命令行参数传递给系统的 URL 处理程序，并限制该参数的长度。当 URL 在为命令行转义后超过该限制时，你只能拒绝该请求。每个需要转义的字符，例如 `%` 或 `&`，都会计为上限的四倍：其自身字符加上三个转义字符。没有这些字符的 URL 在大约 8,000 个字符处达到上限。主要由百分比转义组成的 URL，其中每三个字符中有一个是 `%`，在大约 4,000 处达到上限。

要在不显示对话框的情况下自动响应引出请求，请使用 [`Elicitation` hook](/docs/zh-CN/hooks#elicitation)。

如果你正在构建使用引出功能的 MCP 服务器，请参阅 [MCP 引出规范](https://modelcontextprotocol.io/docs/learn/client-concepts#elicitation) 了解协议详情和架构示例。

在使用 [protocol revision 2026-07-28](#mcp-client-runtimes) 的连接上，Claude Code 在其客户端功能中声明 `elicitation: {form: {}, url: {}}`，因此该处的服务器可以通过协议的标准引出请求来请求任一模式。

<h2 id="use-mcp-resources">
  使用 MCP 资源
</h2>

MCP 服务器可以公开资源，您可以使用 @ 提及来引用这些资源，类似于引用文件的方式。

<h3 id="reference-mcp-resources">
  引用 MCP 资源
</h3>

<Steps>
  <Step title="列出可用资源">
    在您的提示中键入 `@` 以查看来自所有连接的 MCP 服务器的可用资源。资源与文件一起出现在自动完成菜单中。
  </Step>

  <Step title="引用特定资源">
    使用格式 `@server:protocol://resource/path` 来引用资源：

    ```text wrap theme={null}
    Can you analyze @github:issue://123 and suggest a fix?
    ```

    ```text wrap theme={null}
    Please review the API documentation at @docs:file://api/authentication
    ```
  </Step>

  <Step title="多个资源引用">
    您可以在单个提示中引用多个资源：

    ```text wrap theme={null}
    Compare @postgres:schema://users with @docs:file://database/user-model
    ```
  </Step>
</Steps>

<Tip>
  提示：

  * 引用资源时，资源会自动获取并作为附件包含
  * 资源路径在 @ 提及自动完成中可进行模糊搜索
  * Claude Code 在服务器支持时自动提供列出和读取 MCP 资源的工具
  * 资源可以包含 MCP 服务器提供的任何类型的内容（文本、JSON、结构化数据等）
</Tip>

MCP Apps UI 资源是具有 `ui://` URI 或 `text/html;profile=mcp-app` 媒体类型的条目：这些是供主机应用程序呈现的页面，而不是供 Claude 读取的内容。它们不会出现在 `@` 建议中或资源列表工具的结果中，仅提供 UI 资源的服务器会显示空资源列表。通过其 URI 读取 UI 资源仍然有效。

<h2 id="scale-with-mcp-tool-search">
  使用 MCP 工具搜索进行扩展
</h2>

工具搜索通过延迟加载工具定义直到 Claude 需要时，来保持 MCP 上下文使用量较低。只有工具名称和服务器说明在会话开始时加载，因此添加更多 MCP 服务器对您的上下文窗口的影响最小。Claude Code 不会对每个服务器施加固定的工具上限；实际限制是您的上下文窗口预算。

<Note>
  工具搜索在 Microsoft Foundry [部署在 Azure 上的部署](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry#hosting-options)上不受支持，这些部署在服务器端拒绝它：Claude Code 检测到拒绝并为该部署改为预先加载 MCP 工具。[`ENABLE_TOOL_SEARCH`](#configure-tool-search) 无法覆盖此设置，因为拒绝来自部署本身。
</Note>

<h3 id="for-mcp-server-authors">
  对于 MCP 服务器作者
</h3>

如果您正在构建 MCP 服务器，启用工具搜索后，服务器说明字段会变得更加有用。服务器说明帮助 Claude 理解何时搜索您的工具，类似于 [skills](/docs/zh-CN/skills) 的工作方式。

添加清晰、描述性的服务器说明，说明：

* 您的工具处理的任务类别
* Claude 应该何时搜索您的工具
* 您的服务器提供的关键功能

Claude Code 将每个工具描述和每个服务器的说明截断为默认 2,048 个字符。保持它们简洁，并将关键细节放在开头。

要更改会话中每个 MCP 服务器的限制，请将 [`CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH`](/docs/zh-CN/env-vars#variables) 设置为字符数。此变量需要 Claude Code v2.1.280 或更高版本。

<h4 id="per-tool-alwaysload">
  将工具标记为预先加载或保持延迟
</h4>

要控制服务器中某个工具的加载方式，请在该工具的 `_meta` 对象中设置 `"anthropic/alwaysLoad"`。将您的服务器添加到 Claude Code 的人也可以在其配置中为整个服务器设置 [`alwaysLoad`](#exempt-a-server-from-deferral)，并且其设置可以覆盖您的设置：

| 您的工具的值 | 结果 |
| :- | :- |
| `true` | 该工具预先加载。启动不会因为此值而等待您的服务器。配置您的服务器的人仍然可以[延迟其所有工具](#defer-a-servers-tools) |
| `false` | 当其配置设置了 `"alwaysLoad": true` 时，该工具保持延迟。这适用于通过 [`--mcp-config`](/docs/zh-CN/cli-reference#cli-flags) 传入、由 [Agent SDK 应用程序](/docs/zh-CN/agent-sdk/mcp#in-code)提供或由[插件](#plugin-provided-mcp-servers)提供的服务器。在其他服务器上，该工具预先加载。需要 Claude Code v2.1.285 或更高版本 |

以下 `tools/list` 条目请求预先加载一个工具：

```json theme={null}
{
  "name": "search_tickets",
  "description": "Searches the ticket tracker by keyword",
  "_meta": {
    "anthropic/alwaysLoad": true
  }
}
```

<h3 id="configure-tool-search">
  配置工具搜索
</h3>

工具搜索默认启用：MCP 工具被延迟并按需发现。当 `ANTHROPIC_BASE_URL` 指向非第一方主机时，Claude Code 会禁用它，因为大多数代理不转发 `tool_reference` 块。设置 `ENABLE_TOOL_SEARCH` 显式覆盖该回退。

设置 [`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`](/docs/zh-CN/env-vars) 保持工具搜索关闭。您无法通过自己设置 `ENABLE_TOOL_SEARCH` 来覆盖它。您的组织可以通过 [managed settings](/docs/zh-CN/managed-settings) 在 Claude Code v2.1.227 或更高版本上保持工具搜索开启。[禁用预发布功能](/docs/zh-CN/llm-gateway-protocol#disable-pre-release-capabilities) 涵盖了覆盖应用的位置以及变量剥离的内容。

工具搜索需要支持 `tool_reference` 块的模型：Claude Sonnet 4.5、Claude Haiku 4.5、Claude Opus 4.5 及更高版本的模型。有关当前列表，请参阅 [API 文档中的模型兼容性](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool#model-compatibility)。

在 Google Cloud 的 Agent Platform 上，Claude Code 按模型代数决定：

* **Claude Opus 4.5、Sonnet 4.5、Haiku 4.5 及更高版本**：工具搜索默认开启，与 Anthropic API 上相同。
* **早期 Agent Platform 模型**：Claude Code 预先加载所有 MCP 工具，因为它们的服务堆栈拒绝所需的 beta 标头。`ENABLE_TOOL_SEARCH=true` 不会覆盖此设置。

在 v2.1.221 之前，Claude Code 在 Google Cloud 的 Agent Platform 上为所有模型禁用工具搜索，除非您设置 `ENABLE_TOOL_SEARCH=true`。

使用 `ENABLE_TOOL_SEARCH` 环境变量控制工具搜索行为：

| 值 | 行为 |
| :- | :- |
| (未设置) | 所有 MCP 工具延迟并按需加载。在 Google Cloud 的 Agent Platform 早于 Claude 4.5 代的模型上、当 `ANTHROPIC_BASE_URL` 是非第一方主机时、或在 Microsoft Foundry 部署在 Azure 上时回退到预先加载 |
| `true` | 所有 MCP 工具延迟，除了在 Microsoft Foundry 部署在 Azure 上，其中服务器端拒绝仍然强制预先加载，以及在 Google Cloud 的 Agent Platform 早于 Claude 4.5 代的模型上，Claude Code 保持预先加载工具。Claude Code 通过代理发送 beta 标头，在不支持 `tool_reference` 块的代理上请求失败 |
| `auto` | 阈值模式：Claude Code 预先加载它本来会延迟的工具，同时它们的定义总计少于上下文窗口的 10%，一旦定义达到 10% 就延迟所有工具 |
| `auto:N` | 具有自定义百分比的阈值模式，其中 `N` 是 0-100。例如，`auto:5` 表示 5% |
| `false` | 所有 MCP 工具预先加载，无延迟 |

```bash theme={null}
# 使用自定义 5% 阈值
ENABLE_TOOL_SEARCH=auto:5 claude

# 完全禁用工具搜索
ENABLE_TOOL_SEARCH=false claude
```

或在您的 [settings.json `env` 字段](/docs/zh-CN/settings-reference#env) 中设置该值。

您也可以特别禁用 `ToolSearch` 工具：

```json theme={null}
{
  "permissions": {
    "deny": ["ToolSearch"]
  }
}
```

<h3 id="exempt-a-server-from-deferral">
  豁免服务器不延迟
</h3>

如果服务器的工具应该始终对 Claude 可见而无需搜索步骤，请在该服务器的配置中将 `alwaysLoad` 设置为 `true`。之后，该服务器的工具会加载到上下文中，无论 `ENABLE_TOOL_SEARCH` 设置如何。对于 Claude 在每一轮都需要的少量工具使用此选项，因为每个预先加载的工具会消耗本来可用于您的对话的上下文。

以下 `.mcp.json` 条目豁免一个 HTTP 服务器，同时保持其他服务器延迟：

```json theme={null}
{
  "mcpServers": {
    "core-tools": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "alwaysLoad": true
    }
  }
}
```

`alwaysLoad` 字段在所有服务器类型上都可用。

设置 `alwaysLoad: true` 也会使启动等待服务器的工具，上限为标准 5 秒连接超时，因为它们必须在构建第一个提示时存在。具有有效 [`cached` 条目](#server-status-detail) 的远程服务器从缓存提供其工具而无需连接，因此它不会延迟启动。其他服务器默认在后台连接；设置 [`MCP_CONNECTION_NONBLOCKING=0`](/docs/zh-CN/env-vars) 也使启动等待它们。

<h3 id="defer-a-servers-tools">
  延迟服务器的工具
</h3>

要让服务器的所有工具都保持在工具搜索之后，请在 MCP 配置中该服务器的条目里设置 `"alwaysLoad": false`。这包括服务器作者已[标记为预先加载](#per-tool-alwaysload)的工具。如果您省略 `alwaysLoad`，这些已标记的工具会预先加载。需要 Claude Code v2.1.287 或更高版本。

<h2 id="use-mcp-prompts-as-commands">
  将 MCP 提示用作命令
</h2>

MCP 服务器可以公开提示，这些提示在 Claude Code 中作为命令可用。

来自名为 `anthropic-skills` 的服务器的提示不会出现，因为 Claude Code [保留该名称](/docs/zh-CN/skills#names-reserved-for-synced-skills)用于从 claude.ai 同步的 skills。该服务器的工具仍然有效。在您的 MCP 配置中重命名服务器以列出其提示。

<h3 id="execute-mcp-prompts">
  执行 MCP 提示
</h3>

<Steps>
  <Step title="发现可用的提示">
    输入 `/` 以查看可用的命令，包括来自 MCP 服务器的命令。Claude Code 将每个 MCP 提示列为 `/servername:promptname (MCP)`。输入 `/mcp__servername__promptname` 也可以运行它。
  </Step>

  <Step title="执行没有参数的提示">
    ```text wrap theme={null}
    /mcp__github__list_prs
    ```
  </Step>

  <Step title="执行带有参数的提示">
    许多提示接受参数。在命令后面用空格分隔传递它们。Claude Code 在空格处分割参数，因此每个参数是单个令牌：

    ```text wrap theme={null}
    /mcp__github__pr_review 456
    ```

    ```text wrap theme={null}
    /mcp__jira__create_issue login-bug high
    ```
  </Step>
</Steps>

<Tip>
  提示：

  * MCP 提示从连接的服务器动态发现
  * 参数根据提示的定义参数进行解析
  * 提示结果直接注入到对话中
  * 在 `/mcp__servername__promptname` 形式中，Claude Code 将服务器名称中 `A-Z`、`a-z`、`0-9`、`_` 和 `-` 之外的任何字符替换为 `_`，并使用服务器声明的提示名称
</Tip>

<h2 id="managed-mcp-configuration">
  托管 MCP 配置
</h2>

对于需要集中控制用户可以连接到哪些 MCP 服务器的组织，请参阅[托管 MCP 配置](/docs/zh-CN/managed-mcp)。它涵盖使用 `managed-mcp.json` 部署固定服务器集、使用 `managedMcpServers` 为每个用户提供服务器、使用 `allowedMcpServers` 和 `deniedMcpServers` 限制服务器，以及当服务器被阻止时用户看到的内容。
