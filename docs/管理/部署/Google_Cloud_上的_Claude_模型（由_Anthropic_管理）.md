> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 在 Claude Code 中使用 Google Cloud 上的 Claude 模型（由 Anthropic 管理）

> 配置 Claude Code，使其通过您的 Google Cloud 项目使用由 Anthropic 运行的 Claude API，并使用 Google Cloud 凭据、IAM 和 Marketplace 计费。

Google Cloud 上的 Claude 模型（由 Anthropic 管理）是由 Anthropic 运行、通过您的 Google Cloud 项目访问的 Claude API。要在 Claude Code 中使用它，请登录 Google Cloud 并设置三个环境变量。

> [!NOTE]
>
> Google Cloud 还通过 Google Cloud 的 Agent Platform（前身为 Vertex AI）提供 Claude，该平台由 Google 管理。如果您使用的是 Agent Platform，请改为参阅 [Google Cloud Agent Platform 上的 Claude Code](https://code.claude.com/docs/zh-CN/google-vertex-ai.md)。要确定您使用的是哪一种，请参阅 [Which offering are you using?](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/overview#which-offering-are-you-using)

开始之前，请[安装 Claude Code](https://code.claude.com/docs/zh-CN/setup.md#install-claude-code) v2.1.307 或更高版本。要检查版本，请在 shell 中运行 `claude --version`。要更新，请运行 `claude update`。

## 前提条件

* 一个已完成[账户设置](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#set-up-your-account)的 Google Cloud 项目
* 运行 Claude Code 的每个 Google 账号或服务账号在该项目上都具有 `roles/claude.user` [IAM 角色](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#iam-roles)
* 您的项目 ID 和[工作区 ID](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#find-your-workspace-id)（以 `wrkspc_` 开头）
* 如果您使用 Google 账号而非服务账号密钥文件登录，则需要 [gcloud CLI](https://cloud.google.com/sdk/docs/install)

## 设置 Claude Code

**1. 创建应用默认凭据**

> [tab] Google 账号
>
> 在 shell 中运行以下命令，并使用具有 `roles/claude.user` 角色的 Google 账号登录：
>
> ```bash theme={null}
> gcloud auth application-default login
> ```
>
> 即使您已经运行过 `gcloud auth login`，也请运行此命令。
>
> 如果设置了 `GOOGLE_APPLICATION_CREDENTIALS`，请取消设置。只要设置了该变量，Claude Code 就会使用它指定的文件，并忽略该命令保存的凭据。

> [tab] 服务账号密钥文件
>
> 在运行 Claude Code 的 shell 或 CI 作业中，将 `GOOGLE_APPLICATION_CREDENTIALS` 设置为[服务账号密钥文件](https://docs.cloud.google.com/iam/docs/keys-create-delete)的路径。有关其他凭据来源，请参阅[如何进行身份验证](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#authentication)。

**2. 将变量添加到设置中**

将三个变量添加到[用户设置文件](https://code.claude.com/docs/zh-CN/settings.md) `~/.claude/settings.json` 的 `env` 块中。如果该文件不存在，请使用以下内容创建它：

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_USE_ANTHROPIC_GOOGLE_CLOUD": "1",
    "ANTHROPIC_GOOGLE_CLOUD_PROJECT": "my-project-id",
    "ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID": "wrkspc_01ABCDEFGHIJKLMN"
  }
}
```

请使用您自己的项目 ID 和[工作区 ID](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#find-your-workspace-id) 替换 `my-project-id` 和 `wrkspc_` 值。如果要改为仅配置单个 shell 或 CI 作业，请在该环境中设置相同的三个变量。

您无需登录 Anthropic 账户，也无需注销 Anthropic 账户。

**3. 启动 Claude Code 并检查提供商**

在 shell 中运行 `claude`，然后在 Claude Code 提示符处运行 `/status`。`API provider` 行包含 `on Google Cloud`，其后的各行显示您的 `Workspace ID`、`GCP project` 和 `GCP location`。要从 shell 或 CI 作业中输出相同的内容，请运行 [`claude auth status --text`](https://code.claude.com/docs/zh-CN/cli-reference)。

如果您看到 `on Google Cloud`，请发送一条提示词，或在 CI 作业中运行 `claude -p "hello"`。收到回复即表示您的凭据和 IAM 角色正常工作。如果您没有看到它，或者 Claude Code 显示错误，请[排查提供商设置问题](#troubleshooting)。

### 为团队设置 Claude Code

将[设置 Claude Code](#set-up-claude-code) 第 2 步中的 `env` 块放入每位开发者计算机上的[托管设置](https://code.claude.com/docs/zh-CN/managed-settings.md)文件中。为每位开发者授予该项目上的 `roles/claude.user` 角色，并让每位开发者在自己的计算机上运行 `gcloud auth application-default login`。

## 固定模型版本

如果您面向团队进行部署，请[固定模型 ID](https://code.claude.com/docs/zh-CN/model-config.md#pin-models-for-third-party-deployments)，以免 Claude Code 更新时所有人同时切换到更新的模型。将以下变量添加到包含[设置 Claude Code](#set-up-claude-code) 中三个变量的 `env` 块中：

```json theme={null}
{
  "env": {
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-5-5",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-5-5",
    "ANTHROPIC_DEFAULT_FABLE_MODEL": "claude-fable-5-1",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-haiku-4-5-20251001"
  }
}
```

请使用您从[模型概览](https://platform.claude.com/docs/en/about-claude/models/overview)中选择的 Claude API 模型 ID 替换示例值。

## 环境变量

| 变量 | 是否必需 | 说明 |
| - | - | - |
| `CLAUDE_CODE_USE_ANTHROPIC_GOOGLE_CLOUD` | 是 | 设置为 `1` 可将模型请求发送到 Google Cloud 上的 Claude 模型（由 Anthropic 管理） |
| `ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID` | 是，除非您设置了 `ANTHROPIC_GOOGLE_CLOUD_BASE_URL` | 您的工作区 ID |
| `ANTHROPIC_GOOGLE_CLOUD_PROJECT` | 推荐 | 您的 Google Cloud 项目 ID。如果未设置，Claude Code 将使用 `GOOGLE_CLOUD_PROJECT` |
| `ANTHROPIC_GOOGLE_CLOUD_LOCATION` | 否 | 请求 URL 中的[位置](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#project-location-and-workspace-resolution)。默认为 `global` |
| `ANTHROPIC_GOOGLE_CLOUD_BASE_URL` | 否 | 替换 Claude Code 根据项目、位置和工作区 ID 构建的基础 URL，例如替换为 [LLM 网关](https://code.claude.com/docs/zh-CN/llm-gateway)的地址。Claude Code 会追加 API 路径，例如 `/v1/messages` |
| `CLAUDE_CODE_SKIP_ANTHROPIC_GOOGLE_CLOUD_AUTH` | 否 | 当网关自行附加 Google 凭据时设置为 `1`，这样 Claude Code 就不会发送 Google 访问令牌 |

## 不可用的 Claude Code 功能

在 Claude Models on Google Cloud（Anthropic managed）中，您无法使用的功能包括：

* [快速模式](https://code.claude.com/docs/zh-CN/fast-mode.md)：您无法通过 `/fast` 或 `fastMode` 设置启用它
* [Remote Control](https://code.claude.com/docs/zh-CN/remote-control.md) 和[云端会话](https://code.claude.com/docs/zh-CN/claude-code-on-the-web.md)
* [来自 claude.ai 的 MCP 连接器](https://code.claude.com/docs/zh-CN/mcp.md#use-mcp-servers-from-claude-ai)
* [频道](https://code.claude.com/docs/zh-CN/channels.md)
* [`/design-sync` 和 `/import` 命令](https://code.claude.com/docs/zh-CN/commands#all-commands)
* [服务器托管设置](https://code.claude.com/docs/zh-CN/server-managed-settings.md)。要为团队强制执行设置，请改为在每台计算机上使用[托管设置](https://code.claude.com/docs/zh-CN/managed-settings.md)

要查看其他不可用或仅部分支持的功能，请在[功能可用性摘要](https://code.claude.com/docs/zh-CN/feature-availability.md#summary-by-provider)中选择 **Google Cloud (Anthropic managed)** 选项卡。

## 故障排除

如果 Claude Code 要求您登录，或者 `/status` 中的 `API provider` 行不包含 `on Google Cloud`：

* 确保 `CLAUDE_CODE_USE_ANTHROPIC_GOOGLE_CLOUD` 为 `1`
* 确保 `claude --version` 输出 2.1.307 或更高版本
* 从您的 shell 和[设置文件](https://code.claude.com/docs/zh-CN/settings.md#find-or-create-your-settings-files)中移除 `CLAUDE_CODE_USE_BEDROCK`、`CLAUDE_CODE_USE_FOUNDRY` 和 `CLAUDE_CODE_USE_ANTHROPIC_AWS`

`CLAUDE_CODE_USE_VERTEX` 可以保持设置。更改变量后，请重启 Claude Code。如果 `/status` 未显示更改，请参阅[您设置的值被忽略](https://code.claude.com/docs/zh-CN/settings.md#a-value-you-set-is-ignored)。

### `No workspace ID found`

将 `ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID` 设置为您的[工作区 ID](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#find-your-workspace-id)，然后重启 Claude Code。请忽略消息中提到的 `workspaceId` 构造函数选项：它适用于在自己的代码中调用 Anthropic SDK 的用户。

### `No project was given`

将 `ANTHROPIC_GOOGLE_CLOUD_PROJECT` 设置为您的 Google Cloud 项目 ID，然后重启 Claude Code。

### `Could not load Google Cloud credentials`

重复[设置 Claude Code](#set-up-claude-code) 的第 1 步；如果您使用服务账号密钥文件，请使用新密钥。

### `Google Cloud credentials expired or invalid`

如果消息提示您刷新 Google Cloud 凭据，请重复[设置 Claude Code](#set-up-claude-code) 的第 1 步。如果使用服务账号密钥文件，请使用新密钥。

### `Google Cloud authentication failed`

按照 [`Google Cloud credentials expired or invalid`](#google-cloud-credentials-expired-or-invalid) 中的步骤操作。如果这样仍无法消除错误：

* **项目**：在 `/status` 中，确保 `GCP project` 行显示的是您的项目。如果显示的是其他项目，或者没有该行，请按照 [`No project was given`](#no-project-was-given) 操作
* **工作区**：在 `/status` 中，确保 `Workspace ID` 行显示的是您的工作区 ID。如果显示的是其他 ID，请按照 [`No workspace ID found`](#no-workspace-id-found) 操作
* **IAM 角色**：确保运行 Claude Code 的 Google 账号或服务账号在 `GCP project` 行所示的项目上具有 `roles/claude.user` 或 `roles/claude.admin`。要授予该角色，请使用[该服务的授权命令](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#before-making-api-calls)，或请项目管理员授予
* **服务**：确保 `GCP project` 行所示的项目上已启用 `claude.googleapis.com` 服务。要启用它，请按照[该服务的账户设置步骤](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#set-up-your-account)操作，或请项目管理员启用

## 相关资源

* [Google Cloud 上的 Claude 模型（由 Anthropic 管理）](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed)：账户设置、IAM 角色、计费、数据保留和功能支持
* [企业部署概览](https://code.claude.com/docs/zh-CN/third-party-integrations.md)：部署 Claude Code 的其他方式，以及代理和网关设置
* [模型配置](https://code.claude.com/docs/zh-CN/model-config.md)：模型别名、固定模型版本以及限制用户可选择的模型
