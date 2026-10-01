> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 概述

> Claude Code 是一个代理编码工具，可以读取你的代码库、编辑文件、运行命令，并与你的开发工具集成。可在终端、IDE、桌面应用和浏览器中使用。

Claude Code 是一个由 AI 驱动的编码助手，可帮助你构建功能、修复错误和自动化开发任务。它理解你的整个代码库，可以跨多个文件和工具工作以完成任务。

<Note>
  默认配置下，Claude Code 需要能够访问 claude.ai 和 Anthropic API 等端点才能完成安装、登录和正常使用。在中国大陆的网络环境中，这些端点可能无法直接访问。开始前，请先确认所在网络能够连通这些服务。企业代理配置以及 Amazon Bedrock 等第三方提供商的网络要求，请参阅[网络配置](/docs/zh-CN/network-config#network-access-requirements)。
</Note>

<h2 id="get-started">
  开始使用
</h2>

Claude Code 在多个平台上运行：终端、IDE 扩展、桌面应用和网络。从下面的标签页中选择一个来开始使用。大多数平台需要 [Claude 订阅](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=overview_pricing) 或 [Anthropic 控制台](https://platform.claude.com/) 账户。终端 CLI、VS Code 和 JetBrains 也支持[第三方提供商](/docs/zh-CN/third-party-integrations)。

<Tabs>
  <Tab title="Terminal">
    功能完整的 CLI，用于直接在终端中使用 Claude Code。编辑文件、运行命令，并从命令行管理整个项目。

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

    然后在任何项目中启动 Claude Code。将 `your-project` 替换为你机器上项目目录的路径：

    ```bash theme={null}
    cd your-project
    claude
    ```

    首次使用时，系统会提示你登录。如果你已设置 `ANTHROPIC_API_KEY` 环境变量，Claude Code 会跳过登录提示，改为要求你批准该密钥。就这样！[继续快速入门 →](/docs/zh-CN/quickstart)

    <Tip>
      查看[高级设置](/docs/zh-CN/setup)了解安装选项、手动更新或卸载说明。如果遇到问题，请访问[安装故障排除](/docs/zh-CN/troubleshoot-install)。
    </Tip>
  </Tab>

  <Tab title="VS Code">
    VS Code 扩展在编辑器中直接提供内联差异、@-提及、计划审查和对话历史。

    * [为 VS Code 安装](vscode:extension/anthropic.claude-code)
    * [为 Cursor 安装](cursor:extension/anthropic.claude-code)

    或在扩展视图中搜索"Claude Code"（Mac 上为 `Cmd+Shift+X`，Windows/Linux 上为 `Ctrl+Shift+X`）。安装后，打开命令面板（`Cmd+Shift+P` / `Ctrl+Shift+P`），输入"Claude Code"，然后选择**在新标签页中打开**。

    [开始使用 VS Code →](/docs/zh-CN/vs-code#get-started)
  </Tab>

  <Tab title="Desktop app">
    一个独立应用，用于在 IDE 或终端之外运行 Claude Code。直观地查看差异、并行运行多个会话、安排定期任务，并启动云会话。

    下载并安装：

    * [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs)（Intel 和 Apple Silicon）
    * [Windows](https://claude.ai/api/desktop/win32/x64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs)（x64）
    * [Windows ARM64](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs)
    * 在 Ubuntu 或 Debian 上，该应用处于测试阶段，可通过 apt 安装，请按照 [Linux 安装说明](/docs/zh-CN/desktop-linux) 进行操作

    安装后，启动 Claude，登录，然后点击**代码**标签开始编码。该应用包含 Claude Code，因此你无需单独安装 CLI。需要[付费订阅](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=overview_desktop_pricing)。

    [了解更多关于桌面应用的信息 →](/docs/zh-CN/desktop-quickstart)
  </Tab>

  <Tab title="Web">
    在浏览器中运行 Claude Code，无需本地设置。启动长时间运行的任务，完成后再检查，处理你本地没有的仓库，或并行运行多个任务。对于较长的工作，创建一个[项目](/docs/zh-CN/claude-projects)，让 Claude 为你协调并行会话。可在桌面浏览器和 [Claude iOS 和 Android 应用](/docs/zh-CN/mobile)中使用。

    在 [claude.ai/code](https://claude.ai/code) 开始编码。

    [开始在网络上使用 →](/docs/zh-CN/web-quickstart)
  </Tab>

  <Tab title="JetBrains">
    一个用于 IntelliJ IDEA、PyCharm、WebStorm 和其他 JetBrains IDE 的插件，具有交互式差异查看和选择上下文共享。

    从 JetBrains Marketplace 安装 [Claude Code 插件](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-)，然后重启你的 IDE。该插件需要单独安装 Claude Code CLI；请参阅 [JetBrains 设置步骤](/docs/zh-CN/jetbrains#installation)。

    [开始使用 JetBrains →](/docs/zh-CN/jetbrains)
  </Tab>
</Tabs>

<h2 id="what-you-can-do">
  你可以做什么
</h2>

以下是你可以使用 Claude Code 的一些方式：

<AccordionGroup>
  <Accordion title="自动化你一直在推迟的工作" icon="wand-magic-sparkles">
    Claude Code 处理那些占用你一整天的繁琐任务：为未测试的代码编写测试、修复项目中的 lint 错误、解决合并冲突、更新依赖项和编写发布说明。

    ```bash theme={null}
    claude "write tests for the auth module, run them, and fix any failures"
    ```
  </Accordion>

  <Accordion title="构建功能和修复错误" icon="hammer">
    用简单的语言描述你想要的内容。Claude Code 规划方法、跨多个文件编写代码，并验证其工作。

    对于错误，粘贴错误消息或描述症状。Claude Code 通过你的代码库追踪问题、识别根本原因并实施修复。查看[常见工作流](/docs/zh-CN/common-workflows)了解更多示例。
  </Accordion>

  <Accordion title="创建提交和拉取请求" icon="code-branch">
    Claude Code 直接与 git 配合工作。它暂存更改、编写提交消息、创建分支并打开拉取请求。

    ```bash theme={null}
    claude "commit my changes with a descriptive message"
    ```

    在 CI 中，你可以使用 [GitHub Actions](/docs/zh-CN/github-actions) 或 [GitLab CI/CD](/docs/zh-CN/gitlab-ci-cd) 自动化代码审查和问题分类。
  </Accordion>

  <Accordion title="使用 MCP 连接你的工具" icon="plug">
    [Model Context Protocol (MCP)](/docs/zh-CN/mcp) 是一个开放标准，用于将 AI 工具连接到外部数据源。使用 MCP，Claude Code 可以读取 Google Drive 中的设计文档、更新 Jira 中的工单、从 Slack 拉取数据，或使用你自己的自定义工具。[MCP 快速入门](/docs/zh-CN/mcp-quickstart)端到端连接你的第一个服务器。
  </Accordion>

  <Accordion title="使用说明、skills 和 hooks 进行自定义" icon="sliders">
    [`CLAUDE.md`](/docs/zh-CN/memory) 是一个 markdown 文件，你可以将其添加到项目根目录，Claude Code 会在每个会话开始时读取它。使用它来设置编码标准、架构决策、首选库和审查清单。如果你的存储库已经有一个用于其他编码代理的 `AGENTS.md`，Claude Code [可以自己读取它](/docs/zh-CN/memory#agents-md)或与 `CLAUDE.md` 一起读取。Claude 还会在工作时构建[自动内存](/docs/zh-CN/memory#auto-memory)，保存学习内容，跨会话使用，无需你编写任何内容。

    创建 [skills](/docs/zh-CN/skills) 来打包你的团队可以共享的可重复工作流，如 `/review-pr` 或 `/deploy-staging`。

    [Hooks](/docs/zh-CN/hooks) 让你在 Claude Code 操作之前或之后运行 shell 命令，如在每次文件编辑后自动格式化或在提交前运行 lint。
  </Accordion>

  <Accordion title="运行代理团队并构建自定义代理" icon="users">
    生成[多个 Claude Code 代理](/docs/zh-CN/sub-agents)，同时处理任务的不同部分。主导代理协调工作、分配子任务并合并结果。

    要在并行中运行多个完整会话并从一个屏幕观看它们，请使用[后台代理](/docs/zh-CN/agent-view)。对于完全自定义的工作流，[Agent SDK](/docs/zh-CN/agent-sdk/overview) 让你构建由 Claude Code 的工具和功能驱动的自己的代理，完全控制编排、工具访问和权限。
  </Accordion>

  <Accordion title="使用 CLI 进行管道、脚本和自动化" icon="terminal">
    Claude Code 是可组合的，遵循 Unix 哲学。将日志管道传入其中、在 CI 中运行它，或将其与其他工具链接：

    ```bash theme={null}
    # 分析最近的日志输出
    tail -200 app.log | claude -p "Slack me if you see any anomalies"

    # 在 CI 中自动化翻译
    claude -p "translate new strings into French and raise a PR for review"

    # 跨文件的批量操作
    git diff main --name-only | claude -p "review these changed files for security issues"
    ```

    查看 [CLI 参考](/docs/zh-CN/cli-reference)了解完整的命令和标志集。
  </Accordion>

  <Accordion title="安排定期任务" icon="clock">
    按计划运行 Claude 以自动化重复的工作：早晨 PR 审查、夜间 CI 失败分析、每周依赖项审计或在 PR 合并后同步文档。

    * [Routines](/docs/zh-CN/routines) 在云中运行，因此即使你的计算机关闭，它们也会继续运行。它们也可以在 API 调用或 GitHub 事件上触发。从网络、桌面应用或通过在 CLI 中运行 `/schedule` 来创建它们。
    * [桌面计划任务](/docs/zh-CN/desktop-scheduled-tasks)在你的机器上运行，可直接访问你的本地文件和工具
    * [`/loop`](/docs/zh-CN/scheduled-tasks) 在 CLI 会话中重复提示以进行快速轮询
  </Accordion>

  <Accordion title="从任何地方工作" icon="globe">
    会话不受限于单一界面。当你的上下文改变时，在环境之间移动工作：

    * 离开你的办公桌，使用[远程控制](/docs/zh-CN/remote-control)从你的手机或任何浏览器继续工作
    * 向 [Dispatch](/docs/zh-CN/desktop#sessions-from-dispatch) 发送来自你手机的任务，并打开它创建的桌面会话
    * 在[网络](/docs/zh-CN/claude-code-on-the-web)或 [Claude 移动应用](/docs/zh-CN/mobile)上启动长时间运行的任务，然后使用 `claude --teleport` 将其拉入你的终端。Teleport 需要 claude.ai 订阅。
    * 运行 `/desktop` 将你当前的终端会话交给[桌面应用](/docs/zh-CN/desktop)进行视觉差异审查。`/desktop` 交接需要 claude.ai 订阅。可在 macOS 和 x64 Windows 上使用。
    * 从团队聊天路由任务：在 [Slack](/docs/zh-CN/slack) 中提及 `@Claude` 并附上错误报告，获得拉取请求
  </Accordion>
</AccordionGroup>

<h2 id="use-claude-code-everywhere">
  在任何地方使用 Claude Code
</h2>

每个[界面](/docs/zh-CN/glossary#surface)都连接到相同的底层 Claude Code 引擎，因此你的 CLAUDE.md 文件、设置和 MCP 服务器可在所有界面中工作。

除了上面的[终端](/docs/zh-CN/quickstart)、[VS Code](/docs/zh-CN/vs-code)、[JetBrains](/docs/zh-CN/jetbrains)、[桌面](/docs/zh-CN/desktop)和[网络](/docs/zh-CN/claude-code-on-the-web)界面外，Claude Code 还与 CI/CD、聊天和浏览器工作流集成：

| 我想要... | 最佳选项 |
| - | - |
| 从我的手机或另一台设备继续本地会话 | [远程控制](/docs/zh-CN/remote-control) |
| 从 Telegram、Discord、iMessage 或我自己的 webhook 推送事件到会话中 | [Channels](/docs/zh-CN/channels) |
| 在本地启动任务，在移动设备上继续 | [`claude --cloud`](/docs/zh-CN/claude-code-on-the-web#from-terminal-to-cloud)，然后使用 [Claude 移动应用](/docs/zh-CN/mobile) |
| 按定期计划运行 Claude | [Routines](/docs/zh-CN/routines) 或[桌面计划任务](/docs/zh-CN/desktop-scheduled-tasks) |
| 自动化 PR 审查和问题分类 | [GitHub Actions](/docs/zh-CN/github-actions) 或 [GitLab CI/CD](/docs/zh-CN/gitlab-ci-cd) |
| 在每个 PR 上获得自动代码审查 | [GitHub Code Review](/docs/zh-CN/code-review) |
| 将 Slack 中的错误报告路由到拉取请求 | [Slack](/docs/zh-CN/slack) |
| 调试实时网络应用 | [Chrome](/docs/zh-CN/chrome) |
| 为你自己的工作流构建自定义代理 | [Agent SDK](/docs/zh-CN/agent-sdk/overview) |

<h2 id="next-steps">
  后续步骤
</h2>

安装 Claude Code 后，这些指南可帮助你深入了解。

* [快速入门](/docs/zh-CN/quickstart)：通过你的第一个真实任务，从探索代码库到提交修复
* [存储说明和内存](/docs/zh-CN/memory)：使用 CLAUDE.md 文件和自动内存为 Claude 提供持久说明
* [常见工作流](/docs/zh-CN/common-workflows)和[最佳实践](/docs/zh-CN/best-practices)：充分利用 Claude Code 的模式
* [Claude Academy](https://academy.claude.com/)：免费自主学习课程，包括 [Claude Code 101](https://academy.claude.com/courses/claude-code-101) 和 [Claude Code in Action](https://academy.claude.com/courses/claude-code-in-action)
* [每项任务的框架](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)：Claude Code 团队如何使用[动态工作流](/docs/zh-CN/workflows)大规模编排子代理
* [设置](/docs/zh-CN/settings)：为你的工作流自定义 Claude Code
* [故障排除](/docs/zh-CN/troubleshooting)：常见问题的解决方案
* [code.claude.com](https://code.claude.com/)：演示、定价和产品详情
