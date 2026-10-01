> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 配置沙箱化 Bash 工具

> 了解 Claude Code 的沙箱化 Bash 工具如何提供文件系统和网络隔离，以实现更安全、更自主的代理执行。

Bash 沙箱让 Claude 可以运行大多数 shell 命令，而无需停下来请求权限。与其批准每个命令不同，你定义命令可以接触哪些文件和网络域，操作系统为每个 Bash、PowerShell 或 Monitor 命令及其子进程强制执行该边界。

<Note>
  要比较其他隔离方法，如开发容器、自定义容器和虚拟机，请参阅 [Sandbox environments](/docs/zh-CN/sandbox-environments)。要减少 Bash 以外工具的权限提示，请参阅 [permission modes](/docs/zh-CN/permission-modes)。
</Note>

<h2 id="get-started">
  入门
</h2>

沙箱内置于 Claude Code 中，在 macOS、Linux 和 WSL2 上运行。不支持原生 Windows。在 Windows 上，在 WSL2 发行版内运行 Claude Code。

在 macOS 上，无需安装任何内容：沙箱使用内置的 Seatbelt 框架。在 Linux 和 WSL2 上，沙箱依赖两个包，详见 [设置 Linux 和 WSL2](#set-up-linux-and-wsl2)。即使你还没有安装它们，你也可以从 `/sandbox` 开始，因为它的面板显示是否缺少任何内容。

<Steps>
  <Step title="运行 /sandbox">
    启动 Claude Code 会话并运行 `/sandbox` 命令：

    ```text theme={null}
    /sandbox
    ```

    这会打开沙箱面板，有三个选项卡，在 Linux 上缺少可选的 seccomp 过滤器时还有一个 Dependencies 选项卡：

    * **Mode**：选择沙箱化命令的批准方式，在下一步中介绍
    * **Overrides**：选择在沙箱下失败的命令是否可以回退到运行非沙箱化。这是 [`allowUnsandboxedCommands`](/docs/zh-CN/settings-reference#sandbox-allowunsandboxedcommands) 设置
    * **Config**：查看已解析的沙箱设置

    如果面板仅显示 Dependencies 选项卡，则缺少必需的包。按照 [设置 Linux 和 WSL2](#set-up-linux-and-wsl2) 中的说明安装它，重启 Claude Code，然后再次运行 `/sandbox`。
  </Step>

  <Step title="选择一个模式">
    在 Mode 选项卡上，选择自动允许或常规权限。自动允许在不提示的情况下运行沙箱化命令，常规权限即使在命令沙箱化时也保持常规权限提示。有关在自动允许模式下仍会提示哪些命令，请参阅 [沙箱模式](#sandbox-modes)。
  </Step>

  <Step title="运行 Bash 命令">
    要求 Claude 运行一个命令，例如构建或测试套件。默认情况下，沙箱内的命令可以写入工作目录、[每用户临时目录](/docs/zh-CN/env-vars) 以及任何你用 `--add-dir`、`/add-dir` 或 `permissions.additionalDirectories` [添加的目录](/docs/zh-CN/permissions#additional-directories-grant-file-access-not-configuration)。

    命令第一次需要新的网络域时，Claude Code 会提示批准；在 [自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode) 中，Claude 改为在 [命令本身上命名](#per-command-allowed-domains-in-auto-mode) 命令需要的主机供分类器与其一起审查。

    无法沙箱化运行的命令会回退到常规权限流程。Claude Code 将其权限提示标题为"Bash 命令（非沙箱化）"而不是"Bash 命令"，这样你可以看出哪些命令在沙箱外运行。要扩大或缩小沙箱允许的范围，请参阅 [配置沙箱](#configure-sandboxing)。

    如果沙箱化命令在容器内因 `Operation not permitted` 失败，请参阅 [故障排除](#troubleshooting) 下的 Bubblewrap 条目。
  </Step>
</Steps>

在面板中选择一个模式时，Claude Code 会将其保存到你的项目的本地设置 `.claude/settings.local.json`，这些设置适用于当前项目。Claude Code 在那里保存设置时会将该文件添加到你的全局 gitignore。要在所有项目中启用沙箱，请在 `~/.claude/settings.json` 的用户设置中将 [`sandbox.enabled`](/docs/zh-CN/settings-reference#sandbox-enabled) 设置为 `true`。要为组织中的每个开发者强制执行沙箱，请使用 [托管设置](#enforce-sandboxing-with-managed-settings)。

要在一个会话中更改沙箱而不写入设置文件，请使用 [`--settings`](/docs/zh-CN/settings#change-a-setting-for-one-session) 启动 Claude Code。例如，此命令启动一个沙箱化会话，其中 Claude 无法在沙箱外重试被阻止的命令：

```bash theme={null}
claude --settings '{"sandbox": {"enabled": true, "allowUnsandboxedCommands": false}}'
```

<Warning>
  默认情况下，如果沙箱因缺少依赖项或不支持的平台而无法启动，Claude Code 会显示警告并在没有沙箱的情况下运行命令。要使其成为硬失败，请将 [`sandbox.failIfUnavailable`](/docs/zh-CN/settings-reference#sandbox-failifunavailable) 设置为 `true`。这适用于需要沙箱作为安全门的托管部署。
</Warning>

<h3 id="set-up-linux-and-wsl2">
  设置 Linux 和 WSL2
</h3>

在 Linux 和 WSL2 上，沙箱依赖两个包：

* [`bubblewrap`](https://github.com/containers/bubblewrap)：无特权沙箱工具，强制执行文件系统隔离
* [`socat`](http://www.dest-unreach.org/socat/)：用于通过沙箱代理路由网络流量的中继

使用你的发行版的包管理器安装它们：

<Tabs>
  <Tab title="Ubuntu/Debian">
    ```bash theme={null}
    sudo apt-get install bubblewrap socat
    ```
  </Tab>

  <Tab title="Fedora">
    ```bash theme={null}
    sudo dnf install bubblewrap socat
    ```
  </Tab>
</Tabs>

当缺少依赖项时，`/sandbox` 中的 Dependencies 选项卡列出你的平台缺少 `ripgrep`、`bubblewrap`、`socat` 和 seccomp 过滤器中的哪些。如果在安装并重启 Claude Code 后没有看到该选项卡，则所有依赖项都已存在。

Ripgrep 与原生 Claude Code 二进制文件捆绑在一起。seccomp 过滤器是可选的，添加 Unix 域套接字阻止。如果缺少，请使用 `npm install -g @anthropic-ai/sandbox-runtime` 安装它。

当缺少必需的依赖项时，Dependencies 选项卡是唯一显示的选项卡，直到你安装它。当仅缺少可选的 seccomp 过滤器时，Dependencies 选项卡与其他选项卡一起出现。依赖项检查在启动时运行，因此在安装包后重启 Claude Code，以便 `/sandbox` 检测到它们。

<AccordionGroup>
  <Accordion title="Ubuntu 24.04 及更高版本：允许 bubblewrap 创建用户命名空间">
    在 Ubuntu 24.04 及更高版本上，默认 AppArmor 策略阻止 bubblewrap 创建隔离所需的用户命名空间。

    要检查你的环境（包括 WSL2 内）是否强制执行此限制，请运行 `sysctl kernel.apparmor_restrict_unprivileged_userns`。如果命令返回 `0`，请跳过此步骤。如果打印 `No such file or directory` 错误，该密钥不存在，你可以跳过此步骤。如果返回 `1`，请添加一个 AppArmor 配置文件，授予 `bwrap` 此功能：

    ```bash theme={null}
    sudo tee /etc/apparmor.d/bwrap > /dev/null <<'EOF'
    abi <abi/4.0>,
    include <tunables/global>

    profile bwrap /usr/bin/bwrap flags=(unconfined) {
      userns,
      include if exists <local/bwrap>
    }
    EOF
    ```

    该配置文件仅适用于 `bwrap` 本身，不适用于在沙箱内运行的命令。重新加载 AppArmor 以应用它：

    ```bash theme={null}
    sudo systemctl reload apparmor
    ```
  </Accordion>

  <Accordion title="WSL2 注意事项">
    使用 PowerShell 中的 `wsl -l -v` 检查你的 WSL 版本。如果你看到 `Sandboxing requires WSL2`，你的发行版运行的是 WSL1。将其升级到 WSL2 或在没有沙箱的情况下运行 Claude Code。

    在 WSL2 上，WSL 通过 Unix 套接字将 Windows 二进制文件（如 `cmd.exe`、`powershell.exe` 或 `/mnt/c/` 下的任何内容）的启动交给 Windows 主机，因此沙箱化命令是否可以启动一个取决于沙箱的 [Unix 套接字设置](/docs/zh-CN/settings-reference#sandbox-network-allowunixsockets)：必须安装可选的 seccomp 过滤器才能首先阻止套接字。要允许这些启动，请设置 `allowAllUnixSockets`；要将它们完全排除在沙箱外，请将命令添加到 [`excludedCommands`](/docs/zh-CN/settings-reference#sandbox-excludedcommands)。
  </Accordion>
</AccordionGroup>

<h3 id="sandbox-modes">
  沙箱模式
</h3>

Claude Code 提供两种沙箱模式。在两种模式中，沙箱都强制执行相同的文件系统和网络限制；区别仅在于沙箱化命令是自动批准还是需要明确权限。

<h4 id="auto-allow-mode">
  自动允许模式
</h4>

当命令可以沙箱化时，Claude Code 在沙箱内运行它并自动批准，无需询问你的权限。无法沙箱化的命令（例如需要访问非允许主机的网络访问的命令）会回退到常规权限流程，其中 Claude Code 检查你的 [权限规则](/docs/zh-CN/permissions) 并为这些规则不允许的任何命令提示，在 Manual 模式下提示。

即使在自动允许模式下，以下仍然适用：

* 显式 [拒绝规则](/docs/zh-CN/permissions) 始终被尊重
* 针对 [关键路径](/docs/zh-CN/permission-modes#critical-paths) 的 `rm` 或 `rmdir` 命令仍会通过常规权限流程
* 内容范围的 [询问规则](/docs/zh-CN/permissions)（如 `Bash(git push *)`）仍会强制提示，即使对于沙箱化命令
* 裸 `Bash` 询问规则，或等效的 `Bash(*)` 形式，对于运行沙箱化的命令会被跳过；它仍然适用于回退到常规权限流程的命令。在 [Plan Mode](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode) 中，该规则不会被跳过：它也会对沙箱化命令提示，包括只读命令。在 v2.1.212 之前，跳过也适用于 Plan Mode

<Info>
  自动允许模式独立于你的权限模式设置工作，除了在 [Plan Mode](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode) 中，以及在自动模式中，对于携带 [per-command allowed domains](#per-command-allowed-domains-in-auto-mode) 的命令，以及 [服务器端分类器审查](/docs/zh-CN/permission-modes#how-the-classifier-evaluates-actions) 自动模式中的沙箱化命令。即使你不在"接受编辑"模式中，启用自动允许时沙箱化的 Bash 命令也会自动运行。这意味着在沙箱边界内修改文件的 Bash 命令将执行而不提示，即使在 Manual 模式下，文件编辑工具会提示。

  在 Plan Mode 中，自动允许不会扩大批准；请参阅 [Plan Mode](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode) 了解 Claude Code 如何在你计划时限制命令。在 v2.1.212 之前，自动允许在 Plan Mode 中也无需提示地运行沙箱化命令。
</Info>

<h4 id="regular-permissions-mode">
  常规权限模式
</h4>

所有 Bash 命令都通过常规权限流程，即使沙箱化也是如此。这提供了更多控制，但需要更多批准。

<h4 id="the-unsandboxed-retry-escape-hatch">
  非沙箱化重试逃生舱
</h4>

某些命令根本无法在沙箱内运行，例如与其不兼容的工具或需要你未允许的主机的工具。Claude Code 在被阻止命令的结果中报告沙箱违规，命名沙箱拒绝的路径或主机，因此 Claude 看到沙箱阻止了什么。与其让任务失败或要求你关闭沙箱，Claude Code 包括一个逃生舱：Claude 分析违规并可能使用 `dangerouslyDisableSandbox` 参数重试命令。

重试的命令在沙箱外运行，因此通过常规权限流程进行。在 Manual 模式下你会获得确认提示。在 [自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode) 中，分类器评估基础命令。当 [`permissions.blockReadsOutsideWorkingDirectories`](/docs/zh-CN/settings-reference#permissions-blockreadsoutsideworkingdirectories) 打开时，需要批准才能在沙箱外运行的重试会提示你。要在自动模式下的每次非沙箱化重试时都被提示，请为 `Bash(dangerouslyDisableSandbox:true)` 添加一个 [询问规则](/docs/zh-CN/permissions#match-by-input-parameter)。

你可以通过在 [沙箱设置](/docs/zh-CN/settings-reference#sandbox-settings) 中设置 `"allowUnsandboxedCommands": false` 来禁用此逃生舱。禁用逃生舱后，Claude Code 忽略 `dangerouslyDisableSandbox` 参数，Claude 运行的每个命令都必须沙箱化运行，除非你已在 `excludedCommands` 中列出它。`/sandbox` **Overrides** 选项卡将此设置显示为 **Strict sandbox mode**。

严格沙箱模式适用于 Claude 运行的命令。你在 [`!` shell-mode 提示符](/docs/zh-CN/interactive-mode#shell-mode-with-prefix) 处自己输入的命令在沙箱外运行，除非会话是以下之一：

* **一个 [后台会话](/docs/zh-CN/agent-view)**：严格沙箱模式也覆盖 shell-mode 命令
* **一个设置了 [`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`](/docs/zh-CN/env-vars#variables) 的 Linux 会话**：每个命令都沙箱化运行，包括 shell-mode 命令

在 v2.1.260 之前，严格沙箱模式在每个会话中沙箱化 shell-mode 命令。

<h4 id="temporary-directories">
  临时目录
</h4>

会话临时目录在沙箱内默认可写，与工作目录一起。除非你 [禁用文件系统隔离](#disable-filesystem-isolation)，Claude Code 为沙箱化命令设置 `$TMPDIR` 为此目录，因此写入临时文件的工具无需额外配置即可工作。非沙箱化命令继承你的 shell 的 `$TMPDIR` 不变，因此当文件系统隔离打开时，沙箱化和非沙箱化命令将 `$TMPDIR` 解析为不同的目录。如果你的 shell 将 `$TMPDIR` 留空或未设置，引用 `$TMPDIR` 的非沙箱化命令会接收你的 [`CLAUDE_CODE_TMPDIR`](/docs/zh-CN/env-vars) 覆盖，或当你未设置覆盖或覆盖是长路径时接收操作系统的临时目录，因此变量不会展开为空字符串。要在两者之间传递临时文件，请改为在工作目录下写入它们。

<h2 id="configure-sandboxing">
  配置沙箱
</h2>

通过 `settings.json` 文件自定义沙箱行为。有关完整的配置参考，请参阅 [Settings](/docs/zh-CN/settings-reference#sandbox-settings)。

默认情况下，沙箱化命令可以写入当前工作目录、会话临时目录以及任何[你已添加](/docs/zh-CN/permissions#additional-directories-grant-file-access-not-configuration)的目录（使用 `--add-dir`、`/add-dir` 或 `permissions.additionalDirectories`）。如果子进程命令（如 `kubectl`、`terraform` 或 `npm`）需要在这些目录外写入，请使用 `sandbox.filesystem.allowWrite` 向特定路径授予访问权限：

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "allowWrite": ["~/.kube", "/tmp/build"]
    }
  }
}
```

这些路径在操作系统级别强制执行，因此在沙箱内运行的所有命令（包括其子进程）都尊重它们。这是推荐的方法，当工具需要对特定位置的写入访问时，而不是使用 `excludedCommands` 将工具从沙箱中完全排除。

当在多个 [settings scopes](/docs/zh-CN/settings#settings-precedence) 中定义相同的文件系统数组时，Claude Code 会合并它们，组合来自每个范围的路径，而不是用另一个范围的数组替换一个范围的数组。

如果你在 CLI 上使用 [`--setting-sources`](/docs/zh-CN/cli-reference) 或在 Agent SDK 中使用 [`settingSources`](/docs/zh-CN/agent-sdk/claude-code-features#control-filesystem-settings-with-settingsources) 排除一个源，Claude Code 会在构建沙箱配置时忽略其 `sandbox.filesystem` 条目、其 `Edit` 权限规则以及其 `Read` 拒绝规则。需要 Claude Code v2.1.246 或更高版本。

当你在会话期间编辑这些文件系统列表时，Claude Code [将更改应用于运行中的会话](/docs/zh-CN/settings#when-edits-take-effect)，因此下一个沙箱化命令在新路径下运行。

路径前缀控制路径的解析方式：

| 前缀 | 含义 | 示例 |
| :- | :- | :- |
| `/` | 从文件系统根目录的绝对路径 | `/tmp/build` 保持 `/tmp/build` |
| `~/` | 相对于主目录 | `~/.kube` 变为 `$HOME/.kube` |
| `./` 或无前缀 | 对于项目设置相对于项目根目录，或对于用户设置相对于 `~/.claude` | `.claude/settings.json` 中的 `./output` 解析为 `<project-root>/output` |

此语法与 [Read and Edit permission rules](/docs/zh-CN/permissions#read-and-edit) 不同，后者使用 `//path` 表示绝对路径，`/path` 表示项目相对路径。沙箱文件系统路径使用标准约定：`/tmp/build` 是绝对路径。有关 Claude Code 如何处理这些路径中的尾部斜杠或通配符，请参阅 [Sandbox path prefixes](/docs/zh-CN/settings-reference#sandbox-path-prefixes)。

你也可以使用 `sandbox.filesystem.denyWrite` 和 `sandbox.filesystem.denyRead` 拒绝写入或读取访问，以及使用 `sandbox.filesystem.allowRead` 重新允许被拒绝区域内的特定路径。当读取规则重叠时，更具体的路径获胜：

| 示例规则 | 结果 |
| :- | :- |
| `"denyRead": ["~/"]` 与 `"allowRead": ["~/projects"]` | `~/projects` 可读，主目录的其余部分保持被阻止。更窄的允许重新打开被拒绝区域的该部分 |
| `"allowRead": ["~/"]` 与 `"denyRead": ["~/.env"]` | `~/.env` 保持被阻止，主目录的其余部分可读。精确的拒绝在更广泛的允许内部保持有效，因此广泛的允许无法悄悄地重新暴露秘密 |
| `"allowRead": ["~/"]` 与 `"denyRead": ["~/**/.env"]` | 主目录下的每个 `.env` 保持被阻止，其余部分可读。[通配符拒绝](/docs/zh-CN/settings-reference#sandbox-path-prefixes)在更广泛的允许内部保持有效，就像精确路径一样 |

下面的示例阻止从整个主目录读取，同时仍允许从当前项目读取。将其放在你的项目的 `.claude/settings.json` 中，因为相对路径 `.` 仅在配置位于项目设置中时才解析为项目根目录：

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": ["."]
    }
  }
}
```

如果你将相同的配置放在 `~/.claude/settings.json` 中，`.` 将解析为 `~/.claude`，项目文件将保持被 `denyRead` 规则阻止。

要拒绝沙箱化命令对主目录和挂载卷的读取访问，同时保持工作目录可读，请改为设置 [`permissions.blockReadsOutsideWorkingDirectories`](/docs/zh-CN/settings-reference#permissions-blockreadsoutsideworkingdirectories)，而不是编写路径规则。

<h3 id="disable-filesystem-isolation">
  禁用文件系统隔离
</h3>

设置 `sandbox.filesystem.disabled` 为 `true` 以跳过文件系统隔离，同时保持网络隔离。下面的示例关闭文件系统隔离，同时保持网络域的允许列表：

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "disabled": true
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"]
    }
  }
}
```

沙箱有两个独立的层：[文件系统隔离](#filesystem-isolation)控制沙箱化命令可以读写哪些路径，[网络隔离](#network-isolation)控制它们可以到达哪些域。关闭文件系统层后，沙箱化命令获得对主机文件系统的无限制读写访问权限，同时其网络出站流量仍然限制在你允许的域内。当你沙箱化以控制命令连接的位置而不是它们写入的内容时，请关闭该层。

该设置默认关闭，适用于沙箱运行的平台：macOS、Linux 和 WSL2。需要 Claude Code v2.1.216 或更高版本。

<Warning>
  关闭文件系统隔离且命令自动允许时，沙箱化命令可以写入文件，这些文件稍后可能被其他命令运行或读取，例如 shell 启动文件、`$PATH` 上的可执行文件或 `~/.claude/settings.json`，并使用它们在下一次运行时扩大自己的访问权限。仅当你信任工作负载不会升级自己的访问权限时，才将 `filesystem.disabled` 设置为 `true`。使用 [`allowManagedDomainsOnly`](#keep-developers-from-widening-the-policy) 锁定网络域会缩小风险，但不会消除它，因为该锁定仅适用于在沙箱内运行的命令。
</Warning>

<h4 id="which-settings-can-disable-it">
  哪些设置可以禁用它
</h4>

由于关闭文件系统隔离会扩大沙箱化命令可以做的事情，Claude Code 仅从这些设置源中遵守 `filesystem.disabled`：

* 用户设置、托管设置和 `--settings` CLI 标志可以设置它。`.claude/settings.json` 和 `.claude/settings.local.json` 中的项目设置不能，因此已检出的项目无法关闭文件系统隔离。
* 当托管设置配置 `sandbox.filesystem` 时，或列出任何 `sandbox.credentials.files` 条目且 `"mode": "deny"` 时，仅托管设置可以设置该键。这保持管理员部署的文件系统限制有效；要放松此类部署，请在托管设置中设置 `"disabled": true`。
* 当设置 [`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`](/docs/zh-CN/env-vars) 时，Claude Code 会忽略来自每个源（包括托管设置）的 `filesystem.disabled`，并保持文件系统隔离开启。

托管 `credentials.files` 条目是否固定 `filesystem.disabled`（将键锁定到托管设置，以便开发人员无法关闭文件系统隔离）取决于条目的 `mode` 以及沙箱启动时条目发生的情况：

| 托管条目 | 固定 `filesystem.disabled` | 隔离关闭时保护文件的内容 |
| - | - | - |
| `"mode": "deny"` | 是 | 无：读取块是文件系统层的一部分 |
| `"mode": "mask"`，应用为掩盖 | 否 | 掩盖本身：Linux 和 WSL2 上的[哨兵副本和代理](#mask-credential-files)，macOS 上沙箱自己的读取规则 |
| `"mode": "mask"`，[在设置时回退到 `deny`](#mask-credential-files) | 否 | 无，与 `deny` 相同。将无法掩盖的路径（如目录）列为显式 `deny` 条目，这会固定该键 |
| `"mode": "mask"`，[由验证降级为 `deny`](/docs/zh-CN/managed-settings#invalid-entries-in-managed-settings) | 是，如显式 `deny` | 无，与 `deny` 相同 |

回退发生在沙箱启动时，在 Claude Code 已读取设置后，固定检查运行，因此回退条目永远不会固定。验证在设置加载时将无效条目重写为 `deny`，因此降级条目的固定方式与你写为 `deny` 的条目相同。

<h4 id="what-changes-when-filesystem-isolation-is-off">
  文件系统隔离关闭时的变化
</h4>

设置 `filesystem.disabled` 会解除文件系统层本身强制执行的保护。其他层强制执行的保护继续适用：

| 保护 | 文件系统隔离关闭时 |
| - | - |
| `filesystem.denyRead` 和 [`credentials.files`](#protect-credentials) `deny` 读取块 | 未强制执行。文件系统层应用两者 |
| `credentials.envVars` `deny` 和 `mask` 条目 | 强制执行。环境变量清理独立于文件系统层 |
| [`credentials.files` `mask` 条目](#mask-credential-files)应用为掩盖 | 强制执行：掩盖独立于文件系统层。[回退到 `deny`](#mask-credential-files) 的条目未被强制执行，如任何 `deny` 条目 |

另外两件事会改变：

* 沙箱化命令继承你的 shell 的 `$TMPDIR`，而不是会话临时目录，因为每个临时目录都是可写的，Claude Code 不再将命令重定向到会话临时目录。

  在 Linux 上，该变量通常在父 shell 中未设置。Bash 工具指导告诉 Claude 使用 `mktemp -d` 创建临时目录，而不是依赖 `$TMPDIR`。
* [`autoAllowBashIfSandboxed`](/docs/zh-CN/settings-reference#sandbox-autoallowbashifsandboxed) 仍默认为 `true`，因此沙箱化命令继续运行而无需提示。设置为 `false` 以提示沙箱化命令。

<h3 id="protect-credentials">
  保护凭证
</h3>

`sandbox.credentials` 设置声明凭证文件和环境变量，以保护其免受沙箱化命令的访问。每个条目命名一个文件路径或环境变量以及一个 `mode`。专用的 `credentials` 块将凭证规则分组在一起，并与常规文件系统规则分开。

对于 `"mode": "deny"` 的条目，文件路径在沙箱内被拒绝读取，与 `filesystem.denyRead` 应用的限制相同，环境变量在每个沙箱化命令运行前被取消设置。文件保护是文件系统层的一部分，因此如果你[禁用文件系统隔离](#disable-filesystem-isolation)，它不适用；环境变量保护仍然适用。

下面的示例阻止读取 AWS 凭证文件和 SSH 目录，并从沙箱化命令的环境中删除 `GITHUB_TOKEN` 和 `NPM_TOKEN`：

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "credentials": {
      "files": [
        { "path": "~/.aws/credentials", "mode": "deny" },
        { "path": "~/.ssh", "mode": "deny" }
      ],
      "envVars": [
        { "name": "GITHUB_TOKEN", "mode": "deny" },
        { "name": "NPM_TOKEN", "mode": "deny" }
      ]
    }
  }
}
```

环境变量条目和文件条目也接受 `"mode": "mask"`，如下所述 [Mask credentials](#mask-credentials)。

文件路径遵循与 `sandbox.filesystem.*` 设置相同的[前缀规则](/docs/zh-CN/settings-reference#sandbox-path-prefixes)。

Claude Code 合并来自会话加载的每个 [settings scope](/docs/zh-CN/settings#settings-precedence) 的 `deny` 条目。`deny` 条目只会缩小访问权限，因此任何范围都可以添加一个，但没有任何范围可以删除另一个范围添加的条目。

当你[排除一个设置源](#configure-sandboxing)时：

* **项目或本地设置**：Claude Code 不应用它们的任何 `credentials` 条目。需要 Claude Code v2.1.246 或更高版本。
* **用户设置**：Claude Code 仍然应用 `~/.claude/settings.json` 中的 `deny` 条目，并将其[文件 `mask` 条目](#mask-credential-files)保持为限制，但删除其[环境变量 `mask` 条目](#mask-environment-variables)。

没有内置的凭证拒绝列表，因此只有你列出的文件和变量被限制。

`sandbox.credentials` 仅影响沙箱化的 Bash 命令。要从所有子进程中删除凭证，无论是否进行沙箱处理，请设置 [`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`](/docs/zh-CN/env-vars)。

<h3 id="mask-credentials">
  掩盖凭证
</h3>

掩盖比 [Protect credentials](#protect-credentials) 下的 `deny` 条目更进一步。Claude Code 不是阻止凭证，而是向沙箱化命令显示占位符（哨兵），[沙箱代理](#network-isolation)在出站请求到你允许的主机时交换真实值。对于文件，替换是 Linux 和 WSL2 行为；[macOS 改为阻止文件](#mask-credential-files)。

<h4 id="mask-environment-variables">
  掩盖环境变量
</h4>

`"mode": "mask"` 保护凭证，同时保持使用它进行身份验证的工具正常工作。`deny` 完全删除变量，这也会破坏需要它的工具，例如 `gh` 或 `npm`。需要 Claude Code v2.1.199 或更高版本。

使用 `mask`，沙箱化命令看到的是每个会话的哨兵值，而不是真实值。每个 `mask` 条目可以列出 `injectHosts`，真实值被允许到达的主机。当请求离开沙箱前往其中一个主机时，[沙箱代理](#network-isolation)将哨兵值替换为真实值。命令及其记录的任何内容都不会持有真实凭证，但其请求仍然进行身份验证。

代理在请求内容中替换凭证，因此它必须看到它们。设置 [`network.tlsTerminate`](/docs/zh-CN/settings-reference#sandbox-network-tlsterminate) 以便代理自己终止 TLS。

没有它，掩盖会失败关闭：命令仍然只看到哨兵值，但哨兵值不变地到达服务器，身份验证失败。Claude Code 在启动时报告此配置错误。

替换涵盖标头和请求体。使用从凭证派生的签名进行身份验证的请求，而不是凭证本身，需要在代理处重新签名；[Re-sign AWS requests](#re-sign-aws-requests) 涵盖这对 AWS 的工作原理。

代理仅在[域允许列表](#network-isolation)允许的连接上注入，因此每个 `injectHosts` 目标也必须通过 `network.allowedDomains` 可达。

下面的示例掩盖两个令牌。`GH_TOKEN` 仅在对 `api.github.com` 的请求上被替换，而 `NPM_TOKEN` 没有 `injectHosts`，在对 `network.allowedDomains` 中每个主机的请求上被替换。

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "network": {
      "tlsTerminate": {},
      "allowedDomains": ["*.github.com", "registry.npmjs.org"]
    },
    "credentials": {
      "envVars": [
        { "name": "GH_TOKEN", "mode": "mask", "injectHosts": ["api.github.com"] },
        { "name": "NPM_TOKEN", "mode": "mask" }
      ]
    }
  }
}
```

<span id="ipv6-destinations-in-injecthosts" />在两个列表中以不同方式拼写 IPv6 目标，因为每个列表都有自己的匹配器：

* **`network.allowedDomains`**：[括号形式域列表使用](#ipv6-addresses-in-domain-lists)，例如 `"[::1]"`。代理检查此列表以允许连接。
* **`injectHosts`**：其规范压缩形式中的裸地址，例如 `"::1"` 或 `"2001:db8::1"`。代理将每个条目与连接的裸目标地址匹配，忽略端口，因此括号、区域 ID 或不同压缩的拼写永远不会匹配，代理永远不会在那里注入凭证。

`claude doctor` 标记 `injectHosts` 条目，这些条目永远无法与警告 `Sandbox credential injectHosts entries can never match their destination` 匹配。此检查需要 Claude Code v2.1.229 或更高版本。

与 `deny` 不同，掩盖授权代理将你的真实凭证发送到列出的主机，因此 Claude Code 仅从你或你的管理员控制的设置中遵守它：用户设置、托管设置和 `--settings` CLI 标志。Claude Code 忽略存储库的 `.claude/settings.json` 或 `.claude/settings.local.json` 中的 `mask` 条目。在这些文件中，它也忽略 `network.tlsTerminate` 和 [`credentials.allowPlaintextInject`](/docs/zh-CN/settings-reference#sandbox-credentials-allowplaintextinject)，允许代理将凭证注入未加密请求的设置。如果你[排除用户设置](#configure-sandboxing)，Claude Code 也会删除 `~/.claude/settings.json` 中的环境变量 `mask` 条目。

当你的管理员通过服务器托管设置交付 `mask` 条目、`network.tlsTerminate` 或 `credentials.allowPlaintextInject` 时，它们计为[需要批准的设置](/docs/zh-CN/server-managed-settings#security-approval-dialogs)。

当相同的变量在任何范围中以 `deny` 列出时，`deny` 优先。

掩盖默认替换变量的整个值，这适合裸令牌。可选条目字段（需要 Claude Code v2.1.224 或更高版本）处理具有结构的值：

* `extract`：Claude Code 在整个值上应用的正则表达式，仅替换每个匹配的第 1 组捕获的文本，因此解析值的工具（如 `DATABASE_URL` 连接字符串）仍在沙箱内工作。模式必须包含至少一个捕获组。
* `onExtractNoMatch` 控制模式匹配不到任何内容时发生的情况：
  * `warn`，默认值，警告并不掩盖地传递变量
  * `deny` 在沙箱内取消设置变量
  * `error` 停止沙箱设置，直到你修复配置
* `decode: "jwt"`：对于持有 JSON Web Token (JWT) 的变量。Claude Code 验证值是 JWT 并将其替换为结构上有效的假令牌，因此沙箱内解码令牌的代码继续工作。添加 `maskClaims` 以列出要单独掩盖的顶级有效负载声明，而不是替换整个令牌；其他声明保持可读。当值未验证为 JWT 或没有列出的声明匹配时，Claude Code 会以警告不掩盖地传递变量。`decode` 不能与 `extract` 组合。

有关完整字段列表，请参阅[设置参考中的 `credentials.envVars[]` 行](/docs/zh-CN/settings-reference#sandbox-settings)。

<h4 id="re-sign-aws-requests">
  重新签名 AWS 请求
</h4>

AWS 请求在请求内容上携带 SigV4 签名，因此一起掩盖 `AWS_ACCESS_KEY_ID` 和 `AWS_SECRET_ACCESS_KEY`。代理通过访问密钥的哨兵检测 SigV4 请求，并在替换真实值后重新签名。仅掩盖秘密会使请求使用占位符签名，代理无法检测，因此它们在 AWS 处失败；Claude Code 在启动时警告此情况，但仅掩盖访问密钥 ID 时不警告。代理无法重新签名的检测到的请求（如缺少其 `x-amz-date` 标头的请求）会因代理错误而失败，而不是到达服务器并带有损坏的签名。

当你掩盖它们的整个值时，Claude Code 会自动将常规 `AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY` 和 `AWS_SESSION_TOKEN` 变量链接到一个凭证中。如果你的 AWS 凭证位于其他名称的变量中，请使用 [`credentials.awsPairs`](/docs/zh-CN/settings-reference#sandbox-credentials-awspairs) 自己分组，这需要 Claude Code v2.1.224 或更高版本。此示例将配对添加到已掩盖 `MY_KEY_ID`、`MY_SECRET_KEY` 和 `MY_SESSION_TOKEN` 整个值的配置中，如上面的[掩盖配置](#mask-environment-variables)所示：

```json theme={null}
{
  "sandbox": {
    "credentials": {
      "awsPairs": [
        {
          "accessKeyIdVar": "MY_KEY_ID",
          "secretAccessKeyVar": "MY_SECRET_KEY",
          "sessionTokenVar": "MY_SESSION_TOKEN"
        }
      ]
    }
  }
}
```

每个条目遵循这些规则：

* `accessKeyIdVar` 和 `secretAccessKeyVar` 命名持有访问密钥 ID 和秘密密钥的掩盖 `envVars` 条目。可选的 `sessionTokenVar` 命名持有临时凭证会话令牌的条目；设置时，代理在重新签名的请求上将真实令牌作为 `x-amz-security-token` 发送。
* 每个命名的变量必须是掩盖其整个值的 `mask` 条目，不带 `extract` 或 `decode`。
* 代理在访问密钥 ID 条目的 `injectHosts` 中列出的主机上重新签名请求。
* 在对中命名任何常规变量会替换自动配对。

与 `mask` 条目一样，`awsPairs` 仅从用户设置、托管设置和 `--settings` CLI 标志中遵守。

三种 AWS 请求形式携带代理无法重新计算的签名。当此类请求使用掩盖对的占位符签名时，代理会失败它而不是转发损坏的签名；使用未掩盖凭证签名的请求永远不会受到影响。[`credentials.sigv4`](/docs/zh-CN/settings-reference#sandbox-credentials-sigv4) 设置（需要 Claude Code v2.1.224 或更高版本）放松每种形式：将形式的键设置为 `passthrough` 会转发带有其占位符派生签名的请求，因此调用工具接收 AWS 自己的拒绝响应而不是代理错误。与 `awsPairs` 一样，`sigv4` 仅从用户设置、托管设置和 `--settings` CLI 标志中遵守。

| 请求形式 | `sigv4` 键 | 代理无法重新签名的原因 |
| :- | :- | :- |
| aws-chunked 流式上传 | `streaming` | 每个块签名链接到种子签名，因此重新签名需要重写正文 |
| 预签名 URL | `presigned` | 签名位于 URL 本身，没有 `Authorization` 标头 |
| SigV4A 非对称签名 | `sigv4a` | 没有共享密钥 HMAC 可重新计算 |

<h4 id="mask-credential-files">
  掩盖凭证文件
</h4>

文件条目也接受 `"mode": "mask"`，这需要 Claude Code v2.1.221 或更高版本。沙箱化命令看到的内容取决于平台：

* **Linux 和 WSL2**：沙箱化命令读取文件的哨兵副本，一个替代品，其秘密被替换为占位符值，[沙箱代理](#network-isolation)在出站时替换真实值。
* **macOS**：沙箱化命令根本无法读取列出的文件。Claude Code 不构建哨兵副本，也不在出站时替换任何内容，因此使用文件进行身份验证的工具在沙箱内不工作，与 `deny` 的效果相同。与 `deny` 条目不同，即使你[禁用文件系统隔离](#disable-filesystem-isolation)，读取块也保持有效。

在每个平台上，Claude Code 应用 [`network.tlsTerminate`](/docs/zh-CN/settings-reference#sandbox-network-tlsterminate) 要求和 `injectHosts` 的方式与[掩盖环境变量](#mask-environment-variables)相同，并以相同方式忽略存储库设置。如果你[排除用户设置](#configure-sandboxing)，Claude Code 将 `~/.claude/settings.json` 中的文件 `mask` 条目保持为限制，但条目不再授权代理替换真实值。

下面的示例掩盖存储在 `~/.config/gh/hosts.yml` 中的 GitHub 令牌；`extract` 模式（如下所述）告诉 Claude Code 文件的哪一部分是秘密。在 Linux 和 WSL2 上，读取文件的沙箱化命令获得令牌位置的哨兵，代理在对 `api.github.com` 的请求上替换真实令牌：

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "network": {
      "tlsTerminate": {},
      "allowedDomains": ["*.github.com"]
    },
    "credentials": {
      "files": [
        {
          "path": "~/.config/gh/hosts.yml",
          "mode": "mask",
          "extract": "oauth_token:\\s*(\\S+)",
          "injectHosts": ["api.github.com"]
        }
      ]
    }
  }
}
```

要确认掩盖处于活动状态，请要求 Claude 在沙箱化命令中运行 `cat ~/.config/gh/hosts.yml`：在 Linux 和 WSL2 上，输出显示令牌位置的哨兵值，在 macOS 上，读取失败。

在 Linux 和 WSL2 上，`extract` 模式是保持 `hosts.yml` 其余部分可读的原因。Claude Code 在整个文件上应用正则表达式，仅替换每个匹配的第 1 组捕获的文本，因此 `gh` 仍然解析其配置，仅令牌是占位符。对任何工具解析的结构化文件使用 `extract`，例如 `.netrc`、JSON 或 YAML；模式必须包含至少一个捕获组。没有 `extract`，Claude Code 将整个文件内容替换为一个哨兵值，这适合持有单个裸秘密且没有其他内容的文件。

对于持有 JSON Web Token (JWT) 的文件，设置 `decode: "jwt"` 而不是或与 `extract` 一起。`decode` 需要 Claude Code v2.1.224 或更高版本。Claude Code 使用内置模式或你的 `extract` 模式（设置时）查找 JWT 候选项，验证每个候选项是 JWT，并将其替换为结构上有效的假令牌，因此在沙箱内解码令牌的代码继续工作。添加 `maskClaims` 以仅掩盖每个验证令牌内的命名顶级有效负载声明，并保持其他声明可读。当没有候选项验证或没有命名声明匹配时，下面的 `onExtractNoMatch` 字段控制结果，就像模式匹配不到任何内容一样。

两个可选字段细化匹配行为。两者仅在 `mode` 为 `mask` 且 `extract` 或 `decode` 设置时适用。在 macOS 上，当文件系统隔离开启时，Claude Code 在模式运行前将 `mask` 条目应用为 `deny`，因此这些字段和下面的不匹配结果仅在[文件系统隔离关闭](#disable-filesystem-isolation)时在那里生效：

* `onExtractNoMatch` 控制匹配在文件中找不到任何内容要掩盖时发生的情况：

  * `warn`，默认值，警告并跳过条目，因此沙箱化命令可以不掩盖地读取真实文件。默认值适合凭证可能合法不存在的情况；如果秘密可能存在但模式可能错过它，使用 `deny`
  * `deny` 使文件改为不可读
  * `error` 停止沙箱设置，直到你修复配置

  当读取块不会被强制执行时，Claude Code 将 `deny` 视为 `error`：当你[禁用文件系统隔离](#disable-filesystem-isolation)时，以及当任何设置源中的 `filesystem.allowRead` 条目重新打开文件的路径时。
* `maskDuplicates` 也替换每个掩盖凭证值的逐字副本，一个 `extract` 捕获或 `decode` 验证的令牌，在匹配跨度外找到，对于在匹配无法到达的地方重复的秘密。它匹配原始子字符串，因此短或常见的值会被替换到处出现；为长、高熵秘密保留它。默认值：false。

`mask` 适用于单个文件，因此单独列出每个凭证文件。Claude Code 回退到 `deny` 对于它无法安全掩盖的 `mask` 条目：目录路径、glob 模式、大于 8 MiB 的文件或非 UTF-8 文本文件。改为将目录写为显式 `deny` 条目；[Which settings can disable it](#which-settings-can-disable-it) 下的表格涵盖每种形式是否固定 `filesystem.disabled` 以及它在文件系统隔离关闭时的行为。

<h2 id="how-sandboxing-works">
  沙箱如何工作
</h2>

<h3 id="filesystem-isolation">
  文件系统隔离
</h3>

沙箱化 Bash 工具将文件系统访问限制在特定目录：

* **默认写入行为**：对当前工作目录及其子目录的读写访问，加上使用 `--add-dir`、`/add-dir` 或 [`permissions.additionalDirectories`](/docs/zh-CN/settings-reference#permissions-additionaldirectories) 添加的任何目录，以及 `$TMPDIR` 指向的会话临时目录
* **默认读取行为**：对整个计算机的读取访问，除了某些被拒绝的目录。注意此默认仍允许读取凭证文件，例如 `~/.aws/credentials` 和 `~/.ssh/`。使用 [`sandbox.credentials`](#protect-credentials) 阻止读取这些文件并取消设置密钥环境变量，或将路径添加到 `denyRead`。
* **读取阻止**：启用 [`permissions.blockReadsOutsideWorkingDirectories`](/docs/zh-CN/settings-reference#permissions-blockreadsoutsideworkingdirectories) 时，沙箱化命令也会失去对你的主目录和其他保存用户文件的目录的读取访问权限，除了 [Sandboxed commands under the block](/docs/zh-CN/settings-reference#sandboxed-commands-under-the-block) 列出的路径。该部分也说明了此阻止部分何时不适用。
* **被阻止的访问**：无法在没有明确权限的情况下修改工作目录、添加的目录和会话临时目录外的文件，包括 shell 配置文件（例如 `~/.bashrc`）和 `/bin/` 中的系统二进制文件
* **Git worktrees**：当工作目录是[链接的 git worktree](/docs/zh-CN/worktrees)时，沙箱还允许写入主存储库的共享 `.git` 目录，以便 `git commit` 等命令可以更新引用和索引。对该目录内的 `hooks/` 和 `config` 的写入仍然被拒绝。
* **可配置**：通过设置定义自定义允许和拒绝的路径

要完全跳过文件系统隔离同时保持网络隔离，请设置 [`sandbox.filesystem.disabled`](#disable-filesystem-isolation)。

<h3 id="protected-paths">
  受保护的路径
</h3>

在沙箱化命令可以写入的目录内，沙箱仍然拒绝对 Claude Code 从中加载配置和代码的文件进行写入。可以编辑这些文件的命令可能会授予自己权限，或添加 Claude Code 在沙箱外运行的 hook 或 MCP 服务器。权限系统有自己的[受保护路径](/docs/zh-CN/permission-modes#protected-paths)，它控制 Claude Code 在工具运行前批准的内容；沙箱的列表适用于已经运行的命令。它涵盖四组路径：

* **在你的工作目录及其上方的目录中**：`.claude` 设置文件、`.claude/skills`、`.claude/agents`、`.claude/commands` 和 `.claude/hooks` 目录、`.mcp.json`，以及 Claude Code 自己运行的文件，例如 `.claude/workflows` 和 `.claude/scheduled_tasks.json`
* **仅在你的工作目录中**：shell 启动文件，例如 `.bashrc` 和 `.zshrc`、`.gitconfig`、`.vscode` 和 `.idea` 目录，以及 `.git` 内的 `hooks` 和 `config`
* **会将你的工作目录变成裸 git 存储库的文件**：顶级的 `HEAD`、`objects` 和 `refs`，加上 `config` 和 `hooks`（当它们已经存在时）。即使 `config` 文件没有 `HEAD` 也会被拒绝。在 Linux 和 WSL2 上，沙箱删除在沙箱化命令运行时出现的顶级 `HEAD` 文件或 `objects` 或 `refs` 目录
* **在 `~/.claude` 中，或 `CLAUDE_CONFIG_DIR` 指向的目录中**：其大部分内容，加上 `~/.claude.json` 和 `.credentials.json` 凭证存储

如果在会话期间受保护设置文件的路径处出现符号链接，沙箱也会拒绝对其指向的文件进行写入，从下一个命令开始。

无法豁免这些路径之一：覆盖该路径的 `allowWrite` 条目或 `Edit` 允许规则不会解除保护。关闭保护的唯一方法是 [`filesystem.disabled`](#disable-filesystem-isolation)，它为每个路径关闭文件系统隔离。要查看为你的机器解析的大多数这些路径，请运行 `/sandbox` 并打开 **Config** 选项卡，它在 **Denied within allowed** 下列出它们，混合在你自己的 `denyWrite` 条目中。

如果 `git merge` 或 `git checkout` 在这些路径之一上失败并显示 `unable to unlink old`，请参阅[故障排除](#troubleshooting)。

<h3 id="network-isolation">
  网络隔离
</h3>

网络访问通过在沙箱外运行的代理服务器进行控制：

* **域名限制**：Claude Code 默认不预先允许任何域名。命令第一次需要新的域名时，Claude Code 会提示批准；在[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)中，Claude 会根据[按命令允许的域名](#per-command-allowed-domains-in-auto-mode)在命令本身上命名命令需要的主机。
* **批准选择**：如果在提示时选择"是"，Claude Code 会在当前会话的其余时间内允许该主机，之后连接到同一主机时不会再次提示。如果选择"是，以后不再询问"，Claude Code 会将 `WebFetch(domain:...)` 允许规则保存到你的[本地设置](/docs/zh-CN/permissions#permission-system)，因此该主机在未来会话中保持允许。
* **预先允许的域名**：使用 [`allowedDomains`](/docs/zh-CN/settings-reference#sandbox-network-alloweddomains) 预先允许域名以完全避免提示。Claude Code 也预先允许来自 `WebFetch(domain:...)` 允许规则的域名，如[权限规则](#permission-rules)中所述。
* **严格允许列表**：如果在用户、托管或 CLI `--settings` 设置中将 [`strictAllowlist`](/docs/zh-CN/settings-reference#sandbox-network-strictallowlist) 设置为 `true`，Claude Code 会拒绝沙箱化命令访问允许列表外的任何主机，而不是提示。允许列表与沙箱否则会提示的相同：`allowedDomains` 加上来自 `WebFetch(domain:...)` 允许规则的域名，或当设置了 `allowManagedDomainsOnly` 时仅限托管设置条目。Claude Code 仅对沙箱化命令强制执行此；进程内工具（例如 `WebFetch`）仍然遵循其[权限规则](#permission-rules)。在存储库的 `.claude/settings.json` 或 `.claude/settings.local.json` 中设置它没有效果。需要 Claude Code v2.1.219 或更高版本。
* **托管锁定**：如果在托管设置中设置了 [`allowManagedDomainsOnly`](/docs/zh-CN/settings-reference#sandbox-network-allowmanageddomainsonly)，非允许的域名会自动被阻止而不是提示，只有来自托管设置的 `allowedDomains` 和 `WebFetch(domain:...)` 允许规则被尊重。
* **企业代理**：当你的网络要求出站流量通过企业代理时，按照[代理配置](/docs/zh-CN/network-config#proxy-configuration)的描述在你的设置的 `env` 块中设置 `HTTPS_PROXY`、`HTTP_PROXY` 和 `NO_PROXY`，以便[后台代理](/docs/zh-CN/network-config#set-network-variables-in-settings-not-the-shell)也能获得它们，或在你启动 Claude Code 的环境中设置。Claude Code 强制执行域名允许列表，然后通过该上游代理隧道允许的连接。
* **自定义代理支持**：高级用户可以在出站流量上实现自定义规则
* **全面覆盖**：限制适用于所有脚本、程序和由命令生成的子进程

在 `WebFetch(domain:...)` 规则中，沙箱尊重两种通配符形式：前导 `*.`，例如 `*.example.com`，和裸 `*`。裸 `*` 形式需要 Claude Code v2.1.186 或更高版本。任何其他位置的通配符，例如 `WebFetch(domain:example.*)`，仍然匹配获取但对沙箱化命令没有影响。

<Note>
  内置代理基于请求的主机名强制执行允许列表，默认情况下不会终止或检查 TLS 流量。实验性的 [`network.tlsTerminate`](/docs/zh-CN/settings-reference#sandbox-network-tlsterminate) 设置在 Claude Code v2.1.199 及更高版本中可用，使内置代理自行终止 TLS，这是 [`mask` 凭证条目](#mask-credentials)所需的。有关默认设置的含义，请参阅[安全限制](#security-limitations)，如果你的威胁模型需要 TLS 检查，请参阅[自定义代理配置](#custom-proxy-configuration)。
</Note>

<h4 id="per-command-allowed-domains-in-auto-mode">
  自动模式中按命令允许的域名
</h4>

在启用沙箱的[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)中，Claude 会在命令本身上命名命令需要的主机，而不是为每个连接触发网络批准。在沙箱中运行的每个 Bash、PowerShell 或[监视器](/docs/zh-CN/tools-reference#monitor-tool)命令都可以携带超出沙箱允许列表的主机列表：一个域名，例如 `registry.npmjs.org`，一个通配符，例如 `*.pythonhosted.org`，或一个 IP 地址，每个都带有可选的 `:port`。分类器将主机与命令一起审查。需要 Claude Code v2.1.271 或更高版本。

批准的列表仅为该一个命令打开这些主机，只要它运行。没有任何内容被添加到你的会话允许的主机或你的设置；下一个命令命名它自己的主机。

携带主机的命令会进入分类器，而不是由权限规则或沙箱的[自动允许模式](#sandbox-modes)批准。如果[询问规则](/docs/zh-CN/permissions#manage-permissions)强制对命令进行提示，你的终端中的权限对话框会在其旁边列出主机，在那里批准会同时覆盖两者。

按命令列表仅扩大沙箱默认拒绝的内容。[`deniedDomains`](/docs/zh-CN/settings-reference#sandbox-network-denieddomains) 条目仍然会阻止。当 [`strictAllowlist`](/docs/zh-CN/settings-reference#sandbox-network-strictallowlist) 或 [`allowManagedDomainsOnly`](/docs/zh-CN/settings-reference#sandbox-network-allowmanageddomainsonly) 锁定允许列表时，Claude Code 拒绝按命令列表。

当按命令列表适用时，Claude Code 拒绝连接到没有批准命令列出的主机，没有提示或分类器检查。拒绝在命令的结果中命名主机，Claude 会重新运行添加了主机的命令。

<h4 id="ipv6-addresses-in-domain-lists">
  域名列表中的 IPv6 地址
</h4>

沙箱的域名列表是 `allowedDomains`、`deniedDomains` 和为其提供数据的 `WebFetch(domain:...)` 规则。要在其中任何一个中匹配 IPv6 地址，请在括号中写入文字：`"[::1]"` 在每个端口上匹配该地址，`"[::1]:443"` 仅在端口 443 上匹配它。将端口写为 1 到 65535 之间的数字，不带前导零。括号形式需要 Claude Code v2.1.229 或更高版本。在 v2.1.229 之前，当未括号条目的最后一个冒号后的文本是端口号时，Claude Code 将其读为一个，所以 `::1:443` 命名地址 `::1` 在端口 443 上。

当你在 IPv6 地址的网络批准提示处选择"是，以后不再询问"时，Claude Code 会使用括号地址保存 `WebFetch(domain:...)` 规则，因此该规则在未来会话中继续匹配该地址。

未括号的条目有两个或更多冒号是模糊的：`::1:443` 既是完整的 IPv6 地址，也是后跟端口的地址。Claude Code 保守地强制执行模糊的拼写，而不是猜测你的意思是哪种读法：

* **拒绝列表**：Claude Code 拒绝条目解析为的每种读法，因此无论你的意思是哪种读法都被阻止。对于没有可解析读法的条目，Claude Code 不阻止任何内容。
* **允许列表**：Claude Code 永远不允许超过你写的内容。当主机和端口读法干净地解析时，它会将模糊条目重写为其主机和端口读法，并可能完全删除条目，而不是扩大允许列表。

在你的终端中运行 `claude doctor` 以找到受影响的条目：`Sandbox network domain entries have unreliable spellings` 警告命名最多三个条目并计算其余的。将每个条目重写为括号形式以清除警告。警告也命名拼写不可靠的条目，原因包括 `@`、路径或查询字符，或括号内的通配符。

<h3 id="os-level-enforcement">
  操作系统级强制执行
</h3>

沙箱化 Bash 工具使用操作系统安全原语：

* **macOS**：使用 Seatbelt 进行沙箱强制执行
* **Linux**：使用 [bubblewrap](https://github.com/containers/bubblewrap) 进行隔离
* **WSL2**：使用 bubblewrap，与 Linux 相同

不支持 WSL1，因为 bubblewrap 需要仅在 WSL2 中可用的内核功能。

这些相同的原语作为独立的 [`@anthropic-ai/sandbox-runtime`](https://github.com/anthropic-experimental/sandbox-runtime) 包提供，[Sandbox environments](/docs/zh-CN/sandbox-environments#sandbox-runtime) 页面将其作为包装整个 Claude Code 进程的单独方法进行介绍。

<h2 id="how-sandboxing-relates-to-permissions-and-permission-modes">
  沙箱隔离与权限和权限模式的关系
</h2>

沙箱隔离、[权限规则](/docs/zh-CN/permissions)和[权限模式](/docs/zh-CN/permission-modes)是互补的层级。下面的部分涵盖了沙箱隔离如何与每一个交互。

<h3 id="permission-rules">
  权限规则
</h3>

权限规则和沙箱隔离控制不同的事项：

* **权限规则**控制 Claude Code 可以使用哪些工具，并在任何工具运行之前进行评估。它们适用于每个工具：Bash、Read、Edit、WebFetch、MCP 和其他工具，除了拒绝或询问规则无法阻止 [`EndConversation`](/docs/zh-CN/tools-reference#endconversation-tool-behavior)，而任何其他工具仍然存在。
* **沙箱隔离**提供操作系统级别的强制执行，限制 shell 命令在文件系统和网络级别可以访问的内容。它仅适用于 Bash、PowerShell 和 [Monitor](/docs/zh-CN/tools-reference#monitor-tool) 命令及其子进程。

这两个层级在强制执行方式上也有所不同。Claude Code 在命令运行之前根据命令字符串和在自动模式下单独分类器对命令是否安全的判断来评估权限决策。操作系统在运行的进程上强制执行沙箱边界，因此无论模型选择运行什么，即使允许的命令执行的操作超出其名称所示，它也会保持有效。

文件系统和网络限制通过沙箱设置和权限规则进行配置：

| 设置或规则 | 作用 |
| :- | :- |
| `sandbox.filesystem.allowWrite` | 授予子进程对工作目录外路径的写入访问权限 |
| `sandbox.filesystem.denyWrite` 和 `sandbox.filesystem.denyRead` | 阻止子进程访问特定路径 |
| `sandbox.filesystem.allowRead` | 重新允许读取 `denyRead` 区域内的特定路径 |
| [`sandbox.filesystem.disabled`](#disable-filesystem-isolation) | 完全关闭文件系统层，同时保持网络隔离 |
| `Edit` 允许规则 | 授予对特定路径的写入访问权限，与 `sandbox.filesystem.allowWrite` 的方式相同 |
| `Read` 和 `Edit` 拒绝规则 | 阻止访问特定文件或目录 |
| `WebFetch(domain:...)` 允许和拒绝规则 | 控制域访问 |
| 沙箱 `allowedDomains` | 控制 Bash 命令可以访问哪些域 |
| 沙箱 `deniedDomains` | 阻止特定域，即使更广泛的 `allowedDomains` 通配符本来会允许它们 |

来自沙箱设置和权限规则的路径和域被合并到最终的沙箱配置中。

[claude-code 存储库的示例目录](https://github.com/anthropics/claude-code/tree/main/examples/settings)包含常见部署场景的启动设置配置，包括沙箱特定的示例。使用这些作为起点，并根据您的需求进行调整。

<h3 id="permission-modes">
  权限模式
</h3>

`/sandbox` 不是[权限模式](/docs/zh-CN/permission-modes)。权限模式决定工具调用是否运行以及是否首先提示您，而沙箱限制 Bash 命令运行后可以访问的内容。它们在控制的内容和替代每个操作提示的内容上有所不同：

| | 控制的内容 | 替代提示的内容 |
| :- | :- | :- |
| `/sandbox` | Bash 命令运行后可以访问的内容 | 沙箱边界本身，在[自动允许模式](#sandbox-modes)中 |
| [自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode) | 每个工具调用是否运行 | 审查操作的分类器 |
| `--dangerously-skip-permissions` | 每个工具调用是否运行 | 无。[受保护路径](/docs/zh-CN/permission-modes#protected-paths)检查也被跳过；[模式自动批准的操作](/docs/zh-CN/permission-modes#actions-no-mode-auto-approves)仍然适用 |

沙箱的[自动允许模式](#sandbox-modes)与[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)分开：自动允许批准 Bash 命令是因为沙箱边界包含它们，而自动模式使用分类器来审查操作。这两者独立工作，可以组合，但[沙箱模式](#sandbox-modes)下列出的例外除外。要为无人值守运行选择隔离边界，请参阅[沙箱环境](/docs/zh-CN/sandbox-environments#how-isolation-relates-to-permission-modes)。有关常见权限模式和沙箱配对及启动每个配对的标志的表格，请参阅[常见设置](/docs/zh-CN/permission-modes#common-setups)。

<h2 id="configure-the-sandbox-for-your-organization">
  为你的组织配置沙箱
</h2>

管理员可以为每个用户要求沙箱，防止开发者扩大策略，并通过公司代理路由沙箱流量。

<h3 id="enforce-sandboxing-with-managed-settings">
  使用托管设置强制执行沙箱
</h3>

要为每个开发者要求沙箱，通过 [managed settings](/docs/zh-CN/managed-settings#delivery-mechanisms) 提供 `sandbox` 密钥，可以是由你的 MDM 管理的文件，也可以是通过 claude.ai 上的 [server-managed settings](/docs/zh-CN/server-managed-settings)。

以下托管设置配置启用沙箱，如果沙箱无法初始化则拒绝启动 Claude Code，并防止模型在沙箱外重试命令：

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false
  }
}
```

超过 `enabled` 的两个密钥控制沙箱无法运行命令时会发生什么：

* **`failIfUnavailable`**：缺少的依赖项（例如 Linux 上的 bubblewrap）会阻止 Claude Code 启动，而不是显示警告并回退到非沙箱化执行
* **`allowUnsandboxedCommands: false`**：Claude Code 忽略 `dangerouslyDisableSandbox` 逃生舱，因此在沙箱下失败的命令无法在其外重试

值得考虑与它们一起添加两个补充。为任何必须在没有隔离的情况下运行的组织批准的工具添加 `excludedCommands`。为凭证目录（例如 `~/.aws` 和 `~/.ssh`）和秘密环境变量添加 [`sandbox.credentials`](#protect-credentials) 条目，因为默认读取策略仍允许这些。

此配置对 Claude 运行的命令进行沙箱化。开发者仍然可以在 [`!` shell 模式提示符](/docs/zh-CN/interactive-mode#shell-mode-with-prefix) 处键入命令，并在沙箱外运行它，具有与他们在 Claude Code 外任何终端中已有的相同访问权限。有关键入命令运行沙箱化的会话，请参阅 [The unsandboxed retry escape hatch](#the-unsandboxed-retry-escape-hatch)。

沙箱不在原生 Windows 上运行，因此如果你的队伍包括 Windows 主机，请将此配置的范围限制在 macOS 和 Linux，或让这些用户在 WSL2 或容器内运行 Claude Code。

<h3 id="keep-developers-from-widening-the-policy">
  防止开发者扩大策略
</h3>

对于布尔密钥（例如 `enabled` 和 `failIfUnavailable`），Claude Code 使用托管值并忽略开发者在本地设置的任何内容。对于数组密钥（例如 `excludedCommands` 和 `allowRead`），Claude Code 合并来自会话加载的每个范围的条目，因此开发者可以追加扩大策略的条目。

在托管设置中将 `allowManagedReadPathsOnly` 设置为 `true`，以便仅尊重来自托管设置的 `allowRead` 条目。这防止开发者扩大读取访问权限超过组织批准的路径。要以相同的方式将网络域锁定到托管值，请设置 [`allowManagedDomainsOnly`](/docs/zh-CN/settings-reference#sandbox-network-allowmanageddomainsonly)。

当托管设置配置 `sandbox.filesystem` 或列出任何带有 `"mode": "deny"` 的 `sandbox.credentials.files` 条目时，仅托管设置可以设置 [`filesystem.disabled`](#disable-filesystem-isolation)，因此开发者无法关闭管理员部署的文件系统限制。`mask` 条目是否固定密钥取决于它如何解析；[Which settings can disable it](#which-settings-can-disable-it) 下的表格涵盖了四种情况。

`excludedCommands` 没有等效的仅托管锁定，因此开发者总是可以追加在沙箱外运行其他命令的条目。保持托管列表狭窄。

<h3 id="custom-proxy-configuration">
  自定义代理配置
</h3>

对于需要高级网络安全的组织，你可以实现自定义代理以：

* 解密和检查 HTTPS 流量
* 应用自定义过滤规则
* 记录所有网络请求
* 与现有安全基础设施集成

要将 Claude Code 指向你的代理，请在 [sandbox settings](/docs/zh-CN/settings-reference#sandbox-settings) 中设置代理端口：

```json theme={null}
{
  "sandbox": {
    "network": {
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    }
  }
}
```

<h2 id="troubleshooting">
  故障排除
</h2>

某些命令在沙箱内失败，即使它们在沙箱外工作。下面的修复涵盖最常见的情况。

* **命令因主机不允许错误而失败**：许多 CLI 工具需要到达特定的主机。在提示时授予权限会将主机添加到你的允许列表，以便该工具在将来在沙箱内运行。
* **`jest` 挂起或失败**：`watchman` 与沙箱不兼容。改为运行 `jest --no-watchman`。
* **Go 基础 CLI 在 macOS 上 TLS 验证失败**：`gh`、`gcloud` 和 `terraform` 等工具在 Seatbelt 下可能无法进行 TLS 验证。在 [`excludedCommands`](/docs/zh-CN/settings-reference#sandbox-excludedcommands) 中列出这些工具。如果你使用 `httpProxyPort` 与 MITM 代理和自定义 CA，请改为将 [`enableWeakerNetworkIsolation`](/docs/zh-CN/settings-reference#sandbox-enableweakernetworkisolation) 设置为 `true`。
* **`open`、`osascript` 或基于浏览器的身份验证流在 macOS 上因错误 `-600` 失败**：沙箱默认阻止 Apple Events。在你的用户、托管或 CLI 设置中将 [`allowAppleEvents`](/docs/zh-CN/settings-reference#sandbox-allowappleevents) 设置为 `true` 以允许它们。项目设置对此密钥被忽略。启用它会移除代码执行隔离，因为沙箱化命令随后可以在没有用户提示的情况下启动其他未沙箱化的应用程序，并向运行的应用程序发送 AppleScript 命令，受 macOS 自动化同意提示 (TCC) 的约束。或者，将命令添加到 [`excludedCommands`](/docs/zh-CN/settings-reference#sandbox-excludedcommands)。
* **`docker` 命令失败**：`docker` 与沙箱不兼容。将 `docker *` 添加到 [`excludedCommands`](/docs/zh-CN/settings-reference#sandbox-excludedcommands)。
* **`pbcopy`、`xclip` 或 `wl-copy` 不更新剪贴板**：这些剪贴板实用程序可能无法从沙箱内到达系统剪贴板，在这种情况下，管道传输到它们的文本不会到达。

  要将 Claude 的输出放在你的剪贴板上，请要求 Claude 在其响应中打印它，然后运行 [`/copy`](/docs/zh-CN/commands)。`/copy` 从 Claude Code 进程而不是从沙箱化命令写入剪贴板。

  当 Claude 将文本管道传输到这些工具之一时，将该工具添加到 [`excludedCommands`](/docs/zh-CN/settings-reference#sandbox-excludedcommands) 本身不会将该调用从沙箱中取出。
* **git 命令因 `unable to unlink old` 失败**：`git merge`、`git checkout` 和类似命令在需要替换沙箱拒绝写入的文件时以这种方式失败，无论该文件是在 [protected path](#protected-paths) 下（如 `.claude/skills`），在你的 `denyWrite` 条目之一下，还是在沙箱允许命令写入的目录之外。在 Linux 和 WSL2 上，错误以 `Read-only file system` 结尾。

  失败后，Claude 可能会 [提供在沙箱外重新运行命令](#the-unsandboxed-retry-escape-hatch)；批准该重试，或在另一个终端中自己运行 git 命令。如果你已将 `allowUnsandboxedCommands` 设置为 `false`，Claude 无法提供重试，所以自己运行该命令。如果相同的 git 命令经常失败，将其添加到 [`excludedCommands`](/docs/zh-CN/settings-reference#sandbox-excludedcommands)。
* **Bubblewrap 在容器内启动失败**：在无特权容器中，bubblewrap 无法挂载新的 `/proc` 文件系统，所以沙箱化命令因 `bwrap` 错误（如 `Can't mount proc on /newroot/proc: Operation not permitted`）失败。将 [`enableWeakerNestedSandbox`](/docs/zh-CN/settings-reference#sandbox-enableweakernestedsandbox) 设置为 `true`，以便内部沙箱绑定挂载容器的现有 `/proc`。仅在外部容器已提供你需要的隔离边界时使用此设置，因为它向沙箱化命令公开进程信息，而新的 `/proc` 挂载会隐藏这些信息。
* **0 字节只读文件出现在 `.claude` 设置路径，"是的，不要再问"不保存**：在 Linux 和 WSL2 上，沙箱通过在沙箱化命令运行时在那里创建 0 字节只读占位符来对不存在的文件持有写入拒绝。沙箱在之后移除占位符。如果会话在该清理运行之前被杀死，例如通过 SIGKILL，占位符会留下。后续会话在每次启动时再次将它们绑定为只读，所以设置写入（如保存权限选择）在其中一个坐着的地方失败。

  运行 `claude doctor` 以列出剩余的占位符文件。[`Stale sandbox mask files left by a killed session`](/docs/zh-CN/errors#stale-sandbox-mask-files-left-by-a-killed-session) 警告命名最多三个，并计算其余的。在该项目中没有其他 Claude Code 会话运行时，使用 `rm` 删除每个文件。在 v2.1.257 之前，Claude Code 留下相同的占位符而不标记它们。
* **`--dangerously-skip-permissions` 以 root 身份失败**：当在 Linux 和 macOS 上以 root 身份或通过 sudo 运行时，此标志被阻止，因为 root 访问加上没有权限提示可以修改系统上的任何文件或服务。检查在识别的沙箱内自动跳过。要在容器中自主运行，请使用 [dev container](/docs/zh-CN/devcontainer) 配置，它以非 root 用户身份运行 Claude Code。

<h2 id="limitations">
  限制
</h2>

沙箱降低风险，但不是完整的隔离边界。在依赖它作为硬安全控制之前，请查看下面的限制。

<h3 id="security-limitations">
  安全限制
</h3>

* **网络过滤**：沙箱限制进程可以连接的域。默认情况下，内置代理不会终止或检查出站流量上的 TLS，因此不会检查加密连接的内容。实验性的 [`network.tlsTerminate`](/docs/zh-CN/settings-reference#sandbox-network-tlsterminate) 设置在代理处终止 TLS 以进行 [`mask` 凭证替换](#mask-credentials)，但不添加内容过滤。你负责确保只有受信任的域在你的策略中被允许。

<Warning>
  允许广泛的域名（例如 `github.com`）可能会为数据泄露创建路径。因为代理从客户端提供的主机名做出允许决定而不检查 TLS，在沙箱内运行的代码可能会使用 [domain fronting](https://en.wikipedia.org/wiki/Domain_fronting) 或类似技术来到达允许列表外的主机。如果你的威胁模型需要更强的保证，请配置一个 [custom proxy](#custom-proxy-configuration)，它终止 TLS 并检查流量，并在沙箱内安装其 CA 证书。更强的 TLS 感知网络隔离是一个活跃的开发领域。
</Warning>

* **通过 Unix 套接字的权限提升**：`allowUnixSockets` 配置可能会无意中授予对可能导致沙箱绕过的系统服务的访问权限。例如，允许访问 `/var/run/docker.sock` 有效地通过 Docker 套接字授予对主机系统的访问权限。仔细考虑你通过沙箱允许的任何 Unix 套接字。
* **文件系统权限提升**：过于宽泛的文件系统写入权限可能导致权限提升攻击。允许写入包含 `$PATH` 中的可执行文件、系统配置目录或用户 shell 配置文件（例如 `.bashrc` 或 `.zshrc`）的目录可能导致当其他用户或系统进程访问这些文件时在不同的安全上下文中执行代码。
* **Linux 沙箱强度**：Linux 实现提供强大的文件系统和网络隔离，但包括一个 `enableWeakerNestedSandbox` 模式，使其能够在 Docker 环境中工作而无需特权命名空间，或在禁用无特权用户命名空间的 Linux 主机上。此选项大大削弱了安全性，应仅在其他隔离被强制执行时使用。
* **macOS 上的 Apple Events**：macOS 沙箱默认阻止 Apple Events。`allowAppleEvents` 设置解除此限制，以便 `open` 和 `osascript` 等工具可以工作，但它移除了代码执行隔离：沙箱化命令可以在没有用户提示的情况下启动其他未沙箱化的应用程序，并可以向运行的应用程序发送 AppleScript 命令，受限于每个应用程序的 macOS 自动化同意提示 (TCC)。它仅从用户、托管或 CLI 设置中被遵守。项目设置无法启用它。

<h3 id="platform-and-tool-compatibility">
  平台和工具兼容性
</h3>

* **平台支持**：支持 macOS、Linux 和 WSL2。不支持 WSL1 和原生 Windows。
* **性能开销**：最小，但某些文件系统操作可能稍慢。
* **工具兼容性**：某些需要特定系统访问模式的工具可能需要配置调整，或可能需要在沙箱外运行。

<h3 id="scope">
  范围
</h3>

沙箱隔离 Bash 子进程。其他工具在不同的边界下运行：

* **内置文件工具**：Read、Edit 和 Write 直接使用权限系统，而不是通过沙箱运行。请参阅 [permissions](/docs/zh-CN/permissions)。
* **计算机使用**：当 Claude 打开应用程序并控制你的屏幕时，它在你的实际桌面上运行，而不是在隔离的环境中。每个应用程序的权限提示控制每个应用程序。请参阅 [CLI 中的计算机使用](/docs/zh-CN/computer-use) 或 [Desktop 中的计算机使用](/docs/zh-CN/desktop#let-claude-use-your-computer)。
* **环境变量**：沙箱化 Bash 命令默认继承父进程环境，包括在那里设置的任何凭证。使用 [`sandbox.credentials`](#protect-credentials) 为沙箱化命令取消设置或掩盖特定变量，或设置 [`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`](/docs/zh-CN/env-vars) 以从所有子进程中删除凭证。
* **子代理**：[subagents](/docs/zh-CN/sub-agents) 在与父会话相同的进程中运行，并使用相同的沙箱配置。当在父会话中启用沙箱时，子代理内的 Bash 命令被沙箱化。

<Warning>
  有效的沙箱需要同时进行文件系统和网络隔离。没有网络隔离，被破坏的代理可能会泄露敏感文件，如 SSH 密钥。没有文件系统隔离，无论是来自宽泛的策略还是来自 [disabling the filesystem layer](#disable-filesystem-isolation)，被破坏的代理可能会后门系统资源以获得网络访问权限。当你扩大默认值时，检查 `allowWrite` 路径、广泛的 `allowedDomains` 条目或 `excludedCommands` 异常是否不会撤销另一侧的限制。
</Warning>

<h2 id="see-also">
  另请参阅
</h2>

* [Sandbox environments](/docs/zh-CN/sandbox-environments)：比较内置沙箱与开发容器、容器和虚拟机
* [Security](/docs/zh-CN/security)：全面的安全功能和最佳实践
* [Permissions](/docs/zh-CN/permissions)：权限配置和访问控制
* [All settings](/docs/zh-CN/settings-reference)：每个设置键
* [CLI reference](/docs/zh-CN/cli-reference)：命令行选项
