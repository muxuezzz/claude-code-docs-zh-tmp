> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 快速开始

> 欢迎使用 Claude Code！

本快速开始指南将在几分钟内让您使用 AI 驱动的编码辅助。完成本指南后，您将了解如何使用 Claude Code 完成常见的开发任务。

<Note>
  默认配置下，Claude Code 需要能够访问 claude.ai 和 Anthropic API 等端点才能完成安装、登录和正常使用。在中国大陆的网络环境中，这些端点可能无法直接访问。开始前，请先确认所在网络能够连通这些服务。企业代理配置以及 Amazon Bedrock 等第三方提供商的网络要求，请参阅[网络配置](/docs/zh-CN/network-config#network-access-requirements)。
</Note>

<h2 id="before-you-begin">
  开始前
</h2>

确保您拥有：

* 打开的终端或命令提示符
  * 如果您之前从未使用过终端，请查看[终端指南](/docs/zh-CN/terminal-guide)
* 一个可以使用的代码项目
* 一个 [Claude 订阅](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=quickstart_prereq)（Pro、Max、Team 或 Enterprise）、[Claude Console](https://platform.claude.com/) 账户，或通过[支持的云提供商](/docs/zh-CN/third-party-integrations)的访问权限

<Note>
  本指南涵盖终端 CLI。Claude Code 也可在[网页](https://claude.ai/code)、[桌面应用](/docs/zh-CN/desktop)、[VS Code](/docs/zh-CN/vs-code) 和 [JetBrains IDE](/docs/zh-CN/jetbrains)、[Slack](/docs/zh-CN/slack) 中使用，以及通过 [GitHub Actions](/docs/zh-CN/github-actions) 和 [GitLab](/docs/zh-CN/gitlab-ci-cd) 进行 CI/CD。查看[所有界面](/docs/zh-CN/overview#use-claude-code-everywhere)。
</Note>

<h2 id="step-1-install-claude-code">
  步骤 1：安装 Claude Code
</h2>

要安装 Claude Code，请打开终端并运行适用于您的系统的命令。如果您之前没有使用过终端，[终端指南](/docs/zh-CN/terminal-guide)会展示如何打开终端并粘贴命令。

<Tabs>
  <Tab title="原生安装（推荐）">
    **macOS、Linux、WSL：**

    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell：**

    ```powershell theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD：**

    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    安装程序完成后，打开一个新的终端窗口并运行 `claude --version`。正常的安装会打印一个版本号。如果您的 shell 显示找不到 `claude` 或无法识别，说明安装目录还不在您的 PATH 中：请参阅[修复您的 PATH](/docs/zh-CN/troubleshoot-install#command-not-found-claude-after-installation)。

    如果您看到 `The token '&&' is not a valid statement separator`，说明您在 PowerShell 中，而不是 CMD。如果您看到 `'irm' is not recognized as an internal or external command`，说明您在 CMD 中，而不是 PowerShell。当您在 PowerShell 中时，您的提示符显示 `PS C:\`，当您在 CMD 中时显示 `C:\`（没有 `PS`）。

    如果安装命令失败并显示 `syntax error near unexpected token '<'`、`403` 或其他 curl 错误，请参阅 [Troubleshoot installation](/docs/zh-CN/troubleshoot-install#find-your-error) 以匹配错误并获得修复方案和替代安装方法。

    建议在原生 Windows 上安装 [Git for Windows](https://git-scm.com/downloads/win)，以便 Claude Code 可以使用 Bash 工具。如果未安装 Git for Windows，Claude Code 将使用 PowerShell 作为 shell 工具。WSL 设置不需要 Git for Windows。

    <Info>
      原生安装会在后台自动更新，以保持您使用最新版本。
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash theme={null}
    brew install --cask claude-code
    ```

    Homebrew 提供两个 casks。`claude-code` 跟踪稳定发布渠道，通常比最新版本晚约一周，并跳过有重大回归的版本。`claude-code@latest` 跟踪最新渠道，在新版本发布时立即接收。

    <Info>
      Homebrew 安装不会自动更新。运行 `brew upgrade claude-code` 或 `brew upgrade claude-code@latest`（取决于您安装的 cask）以获取最新功能和安全修复。
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet 安装不会自动更新。定期运行 `winget upgrade Anthropic.ClaudeCode` 以获取最新功能和安全修复。
    </Info>
  </Tab>
</Tabs>

您也可以在 Debian、Fedora、RHEL 和 Alpine 上使用 [apt、dnf 或 apk](/docs/zh-CN/setup#install-with-linux-package-managers) 进行安装。

要确认安装成功，请运行：

```bash theme={null}
claude --version
```

该命令会打印一个版本号，后面跟着 `(Claude Code)`。

<h2 id="step-2-log-in-to-your-account">
  步骤 2：登录您的账户
</h2>

Claude Code 需要账户才能使用。使用 `claude` 命令启动交互式会话，首次使用时系统会提示您登录：

```bash theme={null}
claude
```

对于 Claude 订阅或 Console 账户，请按照提示在浏览器中完成身份验证。如果您已设置 `ANTHROPIC_API_KEY` 环境变量，Claude Code 会跳过登录提示，改为要求您批准该密钥。要稍后切换账户或重新身份验证，请在运行的会话中输入 `/login`：

```text wrap theme={null}
/login
```

您可以使用以下任何账户类型登录：

* [Claude Pro、Max、Team 或 Enterprise](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=quickstart_login)（推荐）
* [Claude Console](https://platform.claude.com/)（具有预付费额度的 API 访问）。首次登录时，Console 中会自动为集中成本跟踪创建一个"Claude Code"工作区。
* [Amazon Bedrock、Google Cloud 的 Agent Platform 或 Microsoft Foundry](/docs/zh-CN/third-party-integrations)（企业云提供商）
* 自托管的 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway)（如果您的组织运行一个）：您的管理员会预先配置网关 URL，`/login` 会直接在 **Cloud gateway** 屏幕上打开，供您使用企业 SSO 登录

登录后，您的凭证将被存储，您无需再次登录。详细了解 [凭证管理](/docs/zh-CN/authentication#credential-management)。

<h2 id="step-3-start-your-first-session">
  步骤 3：启动您的第一个会话
</h2>

在任何项目目录中打开您的终端并启动 Claude Code：

```bash theme={null}
cd /path/to/your/project
claude
```

将 `/path/to/your/project` 替换为您要处理的项目的路径。

您将看到 Claude Code 提示符，其中显示版本、当前模型和上方显示的工作目录。输入 `/help` 查看可用命令，或输入 `/resume` 继续之前的对话。

<h2 id="step-4-ask-your-first-question">
  步骤 4：提出您的第一个问题
</h2>

让我们从理解您的代码库开始。尝试以下命令之一：

```text wrap theme={null}
what does this project do?
```

Claude 将分析您的文件并提供摘要。您也可以提出更具体的问题：

```text wrap theme={null}
what technologies does this project use?
```

```text wrap theme={null}
where is the main entry point?
```

```text wrap theme={null}
explain the folder structure
```

您也可以询问 Claude 关于其自身功能的问题：

```text wrap theme={null}
what can Claude Code do?
```

```text wrap theme={null}
how do I create custom skills in Claude Code?
```

```text wrap theme={null}
can Claude Code work with Docker?
```

<Note>
  Claude Code 根据需要读取您的项目文件。您不必手动添加上下文。
</Note>

<h2 id="step-5-make-your-first-code-change">
  步骤 5：进行您的第一次代码更改
</h2>

现在让我们让 Claude Code 进行一些实际的编码。尝试一个简单的任务：

```text wrap theme={null}
在主文件中添加一个 hello world 函数
```

Claude Code 找到适当的文件并向您显示更改。如果它在进行更改前询问，请选择**是**以批准。

使用 Claude Code v2.1.283 或更高版本，auto 模式是交互式终端会话的[内置起始权限模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)：分类器审查操作而不是您，Claude 在不询问的情况下编辑大多数文件并运行大多数命令。在早期版本上，auto 模式仅在 Pro、Max 和 Team 计划上是内置起始权限模式。对于安装后立即启动的会话，请参阅[安装或升级后的首个会话](/docs/zh-CN/env-vars#first-session-after-an-install-or-upgrade)。

<Note>
  您的设置或您的组织可以设置不同的起始权限模式。[会话启动时的权限模式](/docs/zh-CN/permission-modes#which-mode-a-session-starts-in)列出了相关内容。随时按 `Shift+Tab` 切换您所在会话的权限模式。
</Note>

<h2 id="step-6-use-git-with-claude-code">
  步骤 6：在 Claude Code 中使用 Git
</h2>

Claude Code 使 Git 操作变得对话式：

```text wrap theme={null}
我更改了哪些文件？
```

```text wrap theme={null}
用描述性消息提交我的更改
```

您也可以提示更复杂的 Git 操作：

```text wrap theme={null}
创建一个名为 feature/quickstart 的新分支
```

```text wrap theme={null}
显示我最后的 5 次提交
```

```text wrap theme={null}
帮我解决合并冲突
```

<h2 id="step-7-fix-a-bug-or-add-a-feature">
  步骤 7：修复错误或添加功能
</h2>

Claude 擅长调试和功能实现。

用自然语言描述您想要的内容：

```text wrap theme={null}
向用户注册表单添加输入验证
```

或修复现有问题：

```text wrap theme={null}
有一个错误，用户可以提交空表单 - 修复它
```

Claude Code 将：

* 定位相关代码
* 理解上下文
* 实现解决方案
* 如果可用，运行测试

<h2 id="step-8-test-out-other-common-workflows">
  步骤 8：尝试其他常见工作流
</h2>

有多种方式可以与 Claude 一起工作：

**重构代码**

```text wrap theme={null}
refactor the authentication module to use async/await instead of callbacks
```

**编写测试**

```text wrap theme={null}
write unit tests for the calculator functions
```

**更新文档**

```text wrap theme={null}
update the README with installation instructions
```

**代码审查**

```text wrap theme={null}
review my changes and suggest improvements
```

<Tip>
  像与有帮助的同事交谈一样与 Claude 交谈。描述您想要实现的目标，它将帮助您实现。
</Tip>

<h2 id="essential-commands">
  基本命令
</h2>

以下是日常使用中最重要的命令。Shell 命令从您的终端运行以启动或恢复 Claude Code。会话命令在 Claude Code 启动后在其内部运行。

**Shell 命令**

| 命令 | 功能 | 示例 |
| - | - | - |
| `claude` | 启动交互模式 | `claude` |
| `claude "task"` | 使用初始提示启动交互模式 | `claude "fix the build error"` |
| `claude -p "query"` | 运行一次性查询，然后退出 | `claude -p "explain this function"` |
| `claude -c` | 在当前目录中继续最近的对话 | `claude -c` |
| `claude -r` | 恢复之前的对话 | `claude -r` |

**会话命令**

| 命令 | 功能 | 示例 |
| - | - | - |
| `/clear` | 清除对话历史 | `/clear` |
| `/help` | 显示可用命令 | `/help` |
| `/exit` 或 Ctrl+D 两次 | 退出 Claude Code | `/exit` |

有关完整的 shell 命令列表，请参阅 [CLI 参考](/docs/zh-CN/cli-reference)，有关完整的会话命令列表，请参阅 [命令参考](/docs/zh-CN/commands)。

<h2 id="pro-tips-for-beginners">
  初学者专业提示
</h2>

有关更多信息，请参阅[最佳实践](/docs/zh-CN/best-practices)和[常见工作流](/docs/zh-CN/common-workflows)。

<AccordionGroup>
  <Accordion title="对您的请求要具体">
    不要说："修复错误"

    尝试："修复登录错误，用户输入错误凭证后看到空白屏幕"
  </Accordion>

  <Accordion title="使用分步说明">
    将复杂任务分解为步骤：

    ```text wrap theme={null}
    1. 为用户配置文件创建新的数据库表
    2. 创建 API 端点以获取和更新用户配置文件
    3. 构建允许用户查看和编辑其信息的网页
    ```
  </Accordion>

  <Accordion title="让 Claude 先探索">
    在进行更改之前，让 Claude 理解您的代码：

    ```text wrap theme={null}
    分析数据库架构
    ```

    ```text wrap theme={null}
    构建一个仪表板，显示英国客户最常退货的产品
    ```
  </Accordion>

  <Accordion title="使用快捷方式节省时间">
    * 输入 `/` 查看所有命令和 skills
    * 使用 Tab 进行命令补全
    * 按 ↑ 查看命令历史
    * 按 `Shift+Tab` 循环切换权限模式
  </Accordion>
</AccordionGroup>

<h2 id="what’s-next">
  接下来呢？
</h2>

现在您已经学习了基础知识，探索更多高级功能：

<CardGroup cols={2}>
  <Card title="Claude Code 如何工作" icon="microchip" href="/docs/zh-CN/how-claude-code-works">
    了解代理循环、内置工具以及 Claude Code 如何与您的项目交互
  </Card>

  <Card title="最佳实践" icon="star" href="/docs/zh-CN/best-practices">
    通过有效的提示和项目设置获得更好的结果
  </Card>

  <Card title="常见工作流" icon="graduation-cap" href="/docs/zh-CN/common-workflows">
    常见任务的分步指南
  </Card>

  <Card title="扩展 Claude Code" icon="puzzle-piece" href="/docs/zh-CN/features-overview">
    使用 CLAUDE.md、skills、hooks、MCP 等进行自定义
  </Card>
</CardGroup>

<h2 id="getting-help">
  获取帮助
</h2>

* **在 Claude Code 中**：输入 `/help` 或询问"我如何..."
* **文档**：您在这里！浏览其他指南
* **课程**：参加 [Claude Code 101](https://academy.claude.com/courses/claude-code-101) 和 [Claude Academy](https://academy.claude.com/) 上的其他免费自学课程
* **社区**：加入我们的 [Discord](https://www.anthropic.com/discord) 获取提示和支持
