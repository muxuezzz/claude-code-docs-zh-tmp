> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 向插件添加组件

> 向 Claude Code 插件添加 skills、hooks、MCP 服务器和其他所有组件类型，并提供针对每种类型的验证示例。

export const Piece = ({id, children}) => <div className="pe-piece" data-piece={id}>{children}</div>;

export const PluginExplorer = ({children}) => {
  const PIECES = [{
    id: 'manifest',
    name: 'Manifest',
    path: '.claude-plugin/plugin.json',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: '.claude-plugin/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'plugin.json'
    }],
    href: '/en/plugins/manifest-reference#manifest-file',
    linkText: 'Go to the manifest reference'
  }, {
    id: 'skills',
    name: 'Skills',
    path: 'skills/review/SKILL.md',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'skills/'
    }, {
      depth: 1,
      kind: 'folder',
      text: 'review/'
    }, {
      depth: 2,
      kind: 'file',
      text: 'SKILL.md'
    }],
    href: '/en/plugins/components#skills',
    linkText: 'Go to the Skills section'
  }, {
    id: 'commands',
    name: 'Commands',
    path: 'commands/about.md',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'commands/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'about.md'
    }],
    href: '/en/plugins/components#commands',
    linkText: 'Go to the Commands section'
  }, {
    id: 'agents',
    name: 'Agents',
    path: 'agents/security-reviewer.md',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'agents/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'security-reviewer.md'
    }],
    href: '/en/plugins/components#agents',
    linkText: 'Go to the Agents section'
  }, {
    id: 'hooks',
    name: 'Hooks',
    path: 'hooks/hooks.json',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'hooks/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'hooks.json'
    }],
    href: '/en/plugins/components#hooks',
    linkText: 'Go to the Hooks section'
  }, {
    id: 'monitors',
    name: 'Monitors',
    path: 'monitors/monitors.json',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'monitors/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'monitors.json'
    }],
    href: '/en/plugins/components#monitors',
    linkText: 'Go to the Monitors section'
  }, {
    id: 'output-styles',
    name: 'Output styles',
    path: 'output-styles/terse.md',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'output-styles/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'terse.md'
    }],
    href: '/en/plugins/components#themes-and-output-styles',
    linkText: 'Go to the Themes and output styles section'
  }, {
    id: 'themes',
    name: 'Themes',
    path: 'themes/dracula.json',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'themes/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'dracula.json'
    }],
    href: '/en/plugins/components#themes-and-output-styles',
    linkText: 'Go to the Themes and output styles section'
  }, {
    id: 'workflows',
    name: 'Workflows',
    path: 'workflows/audit-routes.js',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'workflows/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'audit-routes.js'
    }],
    href: '/en/workflows#distribute-a-workflow-in-a-plugin',
    linkText: 'Go to Distribute a workflow in a plugin'
  }, {
    id: 'bin',
    name: 'Executables',
    path: 'bin/hello-plugin',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'bin/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'hello-plugin'
    }],
    href: '/en/plugins/components#executables',
    linkText: 'Go to the Executables section'
  }, {
    id: 'scripts',
    name: 'Scripts',
    path: 'scripts/format.sh',
    lines: [{
      depth: 0,
      kind: 'folder',
      text: 'scripts/'
    }, {
      depth: 1,
      kind: 'file',
      text: 'format.sh'
    }],
    href: '/en/plugins/components#hooks',
    linkText: 'Go to the Hooks section'
  }, {
    id: 'settings',
    name: 'Default settings',
    path: 'settings.json',
    lines: [{
      depth: 0,
      kind: 'file',
      text: 'settings.json'
    }],
    href: '/en/plugins/components#default-settings',
    linkText: 'Go to the Default settings section'
  }, {
    id: 'mcp',
    name: 'MCP servers',
    path: '.mcp.json',
    lines: [{
      depth: 0,
      kind: 'file',
      text: '.mcp.json'
    }],
    href: '/en/plugins/components#mcp-servers',
    linkText: 'Go to the MCP servers section'
  }, {
    id: 'lsp',
    name: 'LSP servers',
    path: '.lsp.json',
    lines: [{
      depth: 0,
      kind: 'file',
      text: '.lsp.json'
    }],
    href: '/en/plugins/components#lsp-servers',
    linkText: 'Go to the LSP servers section'
  }];
  const [selectedId, setSelectedId] = useState('manifest');
  const [isFullscreen, setIsFullscreen] = useState(false);
  const rootRef = useRef(null);
  useEffect(() => {
    const onFsChange = () => setIsFullscreen(!!document.fullscreenElement);
    document.addEventListener('fullscreenchange', onFsChange);
    return () => document.removeEventListener('fullscreenchange', onFsChange);
  }, []);
  const toggleFullscreen = () => {
    if (!rootRef.current) return;
    if (document.fullscreenElement) document.exitFullscreen(); else rootRef.current.requestFullscreen().catch(() => {});
  };
  const selected = PIECES.find(p => p.id === selectedId) || PIECES[0];
  const onTreeKeyDown = e => {
    const keys = ['ArrowDown', 'ArrowUp', 'Home', 'End'];
    if (keys.indexOf(e.key) === -1) return;
    const i = PIECES.findIndex(p => p.id === selectedId);
    let next = i;
    if (e.key === 'ArrowDown') next = Math.min(PIECES.length - 1, i + 1);
    if (e.key === 'ArrowUp') next = Math.max(0, i - 1);
    if (e.key === 'Home') next = 0;
    if (e.key === 'End') next = PIECES.length - 1;
    e.preventDefault();
    if (next === i) return;
    const id = PIECES[next].id;
    setSelectedId(id);
    const el = document.getElementById('pe-node-' + id);
    if (el) el.focus();
  };
  const FolderIcon = () => <svg className="pe-icon" width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinejoin="round" aria-hidden="true">
      <path d="M1.5 4.5a1 1 0 0 1 1-1h3.2l1.3 1.5h6a1 1 0 0 1 1 1V12a1 1 0 0 1-1 1h-10.5a1 1 0 0 1-1-1z" />
    </svg>;
  const FileIcon = () => <svg className="pe-icon" width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinejoin="round" aria-hidden="true">
      <path d="M4 1.5h5.5L13 5v9.5H4z" />
      <path d="M9.5 1.5V5H13" />
    </svg>;
  return <div ref={rootRef} className={isFullscreen ? 'pe-root pe-fullscreen not-prose' : 'pe-root not-prose'} data-selected={selected.id}>
      <style>{`
        .pe-root {
          --pe-mono: var(--font-mono, ui-monospace, SFMono-Regular, Menlo, monospace);
          --pe-accent: #D97757;
          --pe-accent-text: #A8502F;
          --pe-accent-bg: rgba(217,119,87,0.10);
          --pe-bg: #FFFFFF;
          --pe-surface: #FAFAF7;
          --pe-hover: #F0EEE6;
          --pe-border: #E8E6DC;
          --pe-text: #141413;
          --pe-text-2: #3D3D3A;
          --pe-text-3: #5E5D59;
          font-family: inherit;
          background: var(--pe-bg);
          color: var(--pe-text);
          border: 1px solid var(--pe-border);
          border-radius: 12px;
          margin: 1.5rem 0;
          overflow: hidden;
          box-sizing: border-box;
        }
        .dark .pe-root {
          --pe-accent-text: #EBA98F;
          --pe-accent-bg: rgba(217,119,87,0.18);
          --pe-bg: #1A1918;
          --pe-surface: #232221;
          --pe-hover: #2E2D2B;
          --pe-border: #3A3936;
          --pe-text: #F1EFE9;
          --pe-text-2: #D6D4CA;
          --pe-text-3: #B8B5AD;
        }
        .pe-root *, .pe-root *::before, .pe-root *::after { box-sizing: border-box; }
        .pe-head { display: flex; align-items: flex-start; gap: 12px; padding: 18px 24px 16px; border-bottom: 1px solid var(--pe-border); }
        .pe-head-text { flex: 1; min-width: 0; }
        .pe-fs-btn { flex-shrink: 0; width: 32px; height: 32px; display: inline-flex; align-items: center; justify-content: center; border: 1px solid var(--pe-border); border-radius: 6px; background: var(--pe-surface); color: var(--pe-text-2); font-size: 15px; line-height: 1; cursor: pointer; }
        .pe-fs-btn:hover { background: var(--pe-hover); }
        .pe-fs-btn:focus-visible { outline: 2px solid var(--pe-accent); outline-offset: 2px; }
        .pe-fullscreen { border-radius: 0; height: 100vh; display: flex; flex-direction: column; overflow: auto; }
        .pe-fullscreen .pe-body { flex: 1; }
        .pe-title { font-size: 19px; font-weight: 600; line-height: 1.3; color: var(--pe-text); margin: 0; }
        .pe-sub { font-size: 15px; line-height: 1.5; color: var(--pe-text-3); margin: 4px 0 0; }
        .pe-sub code { font-family: var(--pe-mono); font-size: 0.88em; padding: 1px 5px; border-radius: 4px; background: var(--pe-surface); border: 1px solid var(--pe-border); }
        .pe-body { display: flex; align-items: stretch; }
        .pe-tree-pane { width: 270px; flex-shrink: 0; background: var(--pe-surface); border-right: 1px solid var(--pe-border); padding: 16px 0 12px; }
        .pe-panel { flex: 1; min-width: 0; padding: 16px 24px 24px; }
        .pe-caption { font-size: 13px; font-weight: 600; color: var(--pe-text-3); margin: 0 0 10px; }
        .pe-tree-pane .pe-caption { padding: 0 16px; }
        .pe-rootline { display: flex; align-items: center; gap: 7px; padding: 3px 16px; font-family: var(--pe-mono); font-size: 13.5px; color: var(--pe-text-3); }
        .pe-node {
          display: block; width: 100%; margin: 0; padding: 3px 16px 3px 30px; text-align: left; cursor: pointer;
          background: transparent; color: var(--pe-text-2);
          border: none; border-left: 3px solid transparent;
          font-family: var(--pe-mono); font-size: 13.5px; line-height: 1.4;
        }
        .pe-node:hover { background: var(--pe-hover); }
        .pe-node:focus-visible { outline: 2px solid var(--pe-accent); outline-offset: -2px; }
        .pe-node[aria-pressed="true"] { background: var(--pe-accent-bg); border-left-color: var(--pe-accent); color: var(--pe-accent-text); font-weight: 600; }
        .pe-line { display: flex; align-items: center; gap: 7px; padding: 2px 0; }
        .pe-line-tree { flex-wrap: wrap; }
        .pe-line-tree .pe-req { flex-basis: 100%; margin: 2px 0 0 22px; white-space: normal; width: fit-content; max-width: calc(100% - 22px); }
        .pe-line span { overflow-wrap: anywhere; }
        .pe-piece { display: none; font-size: 16px; line-height: 1.6; color: var(--pe-text-2); }
        .pe-root[data-selected="manifest"] .pe-piece[data-piece="manifest"],
        .pe-root[data-selected="skills"] .pe-piece[data-piece="skills"],
        .pe-root[data-selected="commands"] .pe-piece[data-piece="commands"],
        .pe-root[data-selected="agents"] .pe-piece[data-piece="agents"],
        .pe-root[data-selected="hooks"] .pe-piece[data-piece="hooks"],
        .pe-root[data-selected="monitors"] .pe-piece[data-piece="monitors"],
        .pe-root[data-selected="output-styles"] .pe-piece[data-piece="output-styles"],
        .pe-root[data-selected="themes"] .pe-piece[data-piece="themes"],
        .pe-root[data-selected="workflows"] .pe-piece[data-piece="workflows"],
        .pe-root[data-selected="bin"] .pe-piece[data-piece="bin"],
        .pe-root[data-selected="scripts"] .pe-piece[data-piece="scripts"],
        .pe-root[data-selected="settings"] .pe-piece[data-piece="settings"],
        .pe-root[data-selected="mcp"] .pe-piece[data-piece="mcp"],
        .pe-root[data-selected="lsp"] .pe-piece[data-piece="lsp"] { display: block; }
        .pe-piece p { margin: 0 0 10px; }
        .pe-piece p:last-child { margin-bottom: 0; }
        .pe-piece code { font-family: var(--pe-mono); font-size: 0.88em; padding: 1px 5px; border-radius: 4px; background: var(--pe-surface); border: 1px solid var(--pe-border); }
        .pe-piece .code-block { margin: 12px 0 0; }
        .pe-piece pre code { padding: 0; border: none; background: none; }
        .pe-piece a { color: var(--pe-accent-text); }
        .pe-line-compact { display: none; }
        .pe-icon { flex-shrink: 0; }
        .pe-req { margin-left: 8px; padding: 0 6px; border-radius: 999px; font-size: 11px; line-height: 18px; letter-spacing: .02em; color: var(--pe-accent-text); border: 1px solid var(--pe-border); background: var(--pe-surface); white-space: nowrap; font-weight: 500; vertical-align: middle; }
        .pe-name { font-size: 22px; font-weight: 600; line-height: 1.25; letter-spacing: -0.2px; color: var(--pe-text); margin: 0; }
        .pe-path { font-family: var(--pe-mono); font-size: 13.5px; color: var(--pe-accent-text); margin: 4px 0 0; overflow-wrap: anywhere; }
        .pe-block { margin: 20px 0 0; }
        .pe-link {
          display: inline-block; margin: 24px 0 0; padding: 8px 14px; border-radius: 8px;
          font-size: 14.5px; font-weight: 600; text-decoration: none;
          color: var(--pe-accent-text); background: var(--pe-accent-bg); border: 1px solid var(--pe-accent);
        }
        .pe-link:hover { filter: brightness(0.97); }
        .pe-link:focus-visible { outline: 2px solid var(--pe-accent); outline-offset: 2px; }
        @media (max-width: 700px) {
          .pe-head { padding: 16px 16px 14px; }
          .pe-body { flex-direction: column; }
          .pe-tree-pane { width: 100%; border-right: none; border-bottom: 1px solid var(--pe-border); }
          .pe-line-tree { display: none; }
          .pe-line-compact { display: flex; }
          .pe-panel { padding: 16px 16px 20px; }
        }
      `}</style>

      <div className="pe-head">
        <div className="pe-head-text">
          <div className="pe-title">What goes in a plugin</div>
          <div className="pe-sub">This example plugin, <code>my-plugin</code>, has one of every kind of component, each in its default location. Select a file or folder to read what it’s for and see what goes in it.</div>
        </div>
        <button type="button" className="pe-fs-btn" onClick={toggleFullscreen} aria-label={isFullscreen ? 'Exit fullscreen' : 'Fullscreen'} title={isFullscreen ? 'Exit fullscreen' : 'Fullscreen'}>
          {isFullscreen ? '⤡' : '⛶'}
        </button>
      </div>

      <div className="pe-body">
        <div className="pe-tree-pane">
          <div className="pe-caption" id="pe-tree-caption">Plugin directory</div>
          <div role="group" aria-labelledby="pe-tree-caption" onKeyDown={onTreeKeyDown}>
            <div className="pe-rootline"><FolderIcon /><span>my-plugin/</span></div>
            {PIECES.map(p => <button key={p.id} id={'pe-node-' + p.id} type="button" className="pe-node" aria-pressed={p.id === selected.id} aria-label={p.name + ', ' + p.path} onClick={() => setSelectedId(p.id)}>
                {p.lines.map((line, i) => <span key={i} className="pe-line pe-line-tree" style={{
    paddingLeft: line.depth * 18 + 'px'
  }}>
                    {line.kind === 'folder' ? <FolderIcon /> : <FileIcon />}
                    <span>{line.text}</span>
                    {p.required && i === p.lines.length - 1 ? <span className="pe-req">{p.required}</span> : null}
                  </span>)}
                <span className="pe-line pe-line-compact">
                  <FileIcon />
                  <span>{p.path}</span>
                  {p.required ? <span className="pe-req">{p.required}</span> : null}
                </span>
              </button>)}
          </div>
        </div>

        <div className="pe-panel" role="region" aria-labelledby="pe-panel-caption" aria-live="polite" aria-atomic="true">
          <div className="pe-caption" id="pe-panel-caption">Selected piece</div>
          <div className="pe-name">{selected.name}{selected.required ? <span className="pe-req">{selected.required}</span> : null}</div>
          <div className="pe-path">{selected.path}</div>

          <div className="pe-block">{children}</div>

          <a className="pe-link" href={selected.href}>{selected.linkText}</a>
        </div>
      </div>
    </div>;
};

Claude Code 插件由多个组件构建而成，例如 skills、agents、hooks 和 MCP 服务器。每个组件在插件中都有一个默认文件夹，在 `.claude-plugin/plugin.json` 中有一个可选的清单键来替换或添加到该文件夹，以及用户看到的名称。有关每个键的完整字段表，请参阅[清单参考](/docs/zh-CN/plugins/manifest-reference#fields)。

使用此页面向已加载的插件添加组件。

添加组件后，在运行中的会话中运行 `/reload-plugins` 或启动新会话，以便 Claude Code 加载它。要在加载前检查组件的文件，请从插件目录在 shell 中运行 [`claude plugin validate .`](/docs/zh-CN/plugins/cli-reference#plugin-validate)。

<Note>
  这些情况在其他页面上有介绍：

  * **构建您的第一个插件**：从[创建插件](/docs/zh-CN/plugins/create)开始
  * **安装他人的插件**：请参阅[安装插件](/docs/zh-CN/plugins/install)
  * **您的插件用户在 claude.ai 或 Cowork 中**：那里加载的是不同的组件集。请参阅[插件结构和测试](https://claude.com/docs/plugins/build)和[组件支持表](https://claude.com/docs/plugins/platform-support#compare-component-support-by-app)
</Note>

<h2 id="explore-the-plugin-directory">
  浏览插件目录
</h2>

浏览器显示了一个示例插件 `my-plugin`，它在其默认位置拥有每种组件的一个副本：

* 一个审查 skill 和一个 `about` 命令
* 一个 security-review 子代理
* 一个在 Claude 编辑文件后格式化文件的 hook，以及它调用的 `scripts/` 文件夹
* 一个日志监视器
* 一个输出样式和一个颜色主题
* 一个 route-audit 工作流
* 一个 `hello-plugin` 可执行文件
* 默认设置
* 一个本地 MCP 服务器和一个 Go 语言服务器

每个文件都是其格式的最小有效示例，用于展示形状而不是实用性：真实的 skill 或 agent 包含完整的说明，通常还有支持文件，真实的 hook 或监视器执行真实的工作。浏览器后的部分使用与浏览器相同的文件作为示例，并链接到更完整的文件。选择一个文件或文件夹来阅读其用途、查看其内容，并找到涵盖它的部分。

<PluginExplorer>
  <Piece id="manifest">
    [清单](/docs/zh-CN/plugins/manifest-reference)是插件 `.claude-plugin/` 目录中的 `plugin.json` 文件。它包含插件的元数据和 Claude Code 提示用户的 `userConfig` 值。Claude Code 可以在没有清单的情况下加载插件。在文件中，只有 `name` 是必需的。在这个文件中，`description` 是用户在 `/plugin` 中看到的插件文本，`version` 使用户保持在该版本，直到您更改它：

    ```json theme={null}
    {
      "name": "my-plugin",
      "version": "1.0.0",
      "description": "Review, formatting, and database tools for this team"
    }
    ```
  </Piece>

  <Piece id="skills">
    一个 [skill](/docs/zh-CN/skills) 是一个 `SKILL.md` 文件。将每个 skill 保存在 `skills/` 下的自己的目录中。Claude 读取每个 skill 的 `description`，当用户要求的内容与其匹配时，例如在这里要求 Claude 审查拉取请求，Claude 加载 skill 的说明并遵循它们。用户也可以直接将其作为 `/my-plugin:review` 运行：

    ```markdown theme={null}
    ---
    description: Reviews a pull request for style and test coverage. Use when asked to review code.
    ---

    Review the changed files. Report style problems first, then missing tests.
    ```
  </Piece>

  <Piece id="commands">
    命令是用户按名称运行的单个 Markdown 文件。命令是较旧的格式：skill 以相同的方式按名称运行，也可以在其自己的目录中携带支持文件，因此将新的写成 skills，并为您已有的文件保留 `commands/`。此文件变成 `/my-plugin:about` 并采用与 skill 相同的 frontmatter：

    ```markdown theme={null}
    ---
    description: Summarize the repository
    ---

    Summarize what this repository does in three sentences.
    ```
  </Piece>

  <Piece id="agents">
    一个[子代理](/docs/zh-CN/sub-agents)是一个单独的助手，拥有自己的说明和自己的上下文窗口，Claude 可以将任务委托给它并获得结果。`agents/` 下的每个 Markdown 文件定义一个：frontmatter 命名它并说明何时使用它，正文是其系统提示。这个被命名为 `my-plugin:security-reviewer`，用户可以使用 `@agent-my-plugin:security-reviewer` 调用它：

    ```markdown theme={null}
    ---
    name: security-reviewer
    description: Reviews code changes for security issues. Use after edits to authentication or input handling.
    model: sonnet
    ---

    You are a security reviewer. Read the changed files and report injection, authentication, and secrets-handling risks.
    ```
  </Piece>

  <Piece id="hooks">
    一个 [hook](/docs/zh-CN/hooks-guide) 在 Claude Code 生命周期中的某个点自动运行某些内容，例如在每次文件编辑后：shell 命令、HTTP 请求、MCP 工具调用、对模型的提示或子代理。将插件的 hooks 保存在插件根目录的 `hooks/hooks.json` 中。这个在 Claude 写入或编辑文件后运行插件的 `scripts/format.sh`：

    ```json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "\"${CLAUDE_PLUGIN_ROOT}/scripts/format.sh\""
              }
            ]
          }
        ]
      }
    }
    ```
  </Piece>

  <Piece id="monitors">
    监视器是一个 shell 命令，Claude Code 在会话启动时在后台启动它，并保持运行直到会话结束。它打印的内容作为通知到达 Claude。`when` 字段可以改为在命名 skill 首次运行时启动它。这个跟踪错误日志：

    ```json theme={null}
    [
      {
        "name": "error-log",
        "command": "tail -F ./logs/error.log",
        "description": "Application error log"
      }
    ]
    ```
  </Piece>

  <Piece id="output-styles">
    插件可以包含[输出样式](/docs/zh-CN/output-styles)，这改变了 Claude 如何格式化和表述其回复。将每个输出样式保存为 `output-styles/<name>.md`。这个在 `/output-style` 中显示为 `my-plugin:terse`：

    ```markdown theme={null}
    ---
    name: terse
    description: Answer in as few words as possible
    keep-coding-instructions: true
    ---

    Keep every reply short. Skip preambles and summaries.
    ```
  </Piece>

  <Piece id="themes">
    插件可以包含 [Claude Code 界面的颜色主题](/docs/zh-CN/terminal-config#create-a-custom-theme)。将每个主题保存为 `themes/<slug>.json`。这个在 `/theme` 中显示为 `Dracula`，标记为来自 `my-plugin`：

    ```json theme={null}
    {
      "name": "Dracula",
      "base": "dark",
      "overrides": {
        "claude": "#bd93f9",
        "error": "#ff5555"
      }
    }
    ```
  </Piece>

  <Piece id="workflows">
    `workflows/` 文件夹包含 [workflow](/docs/zh-CN/workflows) `.js` 文件：一个 `meta` 块，然后是协调多个子代理的脚本正文。这个作为 `/my-plugin:audit-routes` 运行：

    ```javascript theme={null}
    export const meta = {
      name: 'audit-routes',
      description: 'Audit every route handler for missing auth checks',
    }

    const found = await agent('List every .ts file under src/routes/.', {
      schema: { type: 'object', required: ['files'], properties: { files: { type: 'array', items: { type: 'string' } } } },
    })

    const audits = await pipeline(found.files, file =>
      agent(`Audit ${file} for missing authentication checks.`, { label: file }),
    )

    return audits.filter(Boolean)
    ```
  </Piece>

  <Piece id="bin">
    `bin/` 是插件如何提供命令行工具的方式。启用插件时，Claude Code 将此文件夹放在它运行命令的 shell 的 `PATH` 上，因此 Claude 或 skill 的说明可以按名称运行该工具，而无需用户安装任何东西。有了这个[可执行文件](#executables)，`hello-plugin` 是 Claude 可以运行的命令：

    ```bash theme={null}
    #!/bin/bash
    echo "hello from my-plugin"
    ```
  </Piece>

  <Piece id="scripts">
    `hooks/hooks.json` 中的 hook 运行一个脚本，这个文件夹是示例保留它的地方。名称 `scripts/` 是一个约定，不是 Claude Code 查找的东西：hook 通过其路径指向文件，`${CLAUDE_PLUGIN_ROOT}/scripts/format.sh`。格式化脚本可能看起来像这样：

    ```bash theme={null}
    #!/bin/bash
    npx prettier --write .
    ```
  </Piece>

  <Piece id="settings">
    插件根目录中的 `settings.json` 包含在启用插件时应用的[设置](/docs/zh-CN/settings-reference)，因此插件可以改变会话的行为方式，而不仅仅是添加组件。只有两个键从插件生效，[`agent`](/docs/zh-CN/settings-reference#agent) 和 [`subagentStatusLine`](/docs/zh-CN/settings-reference#subagentstatusline)；所有其他键都被丢弃。请参阅[默认设置](#default-settings)。

    这个设置 `agent`，它将会话的主线程作为插件自己的 `security-reviewer` agent 运行，因此该 agent 的系统提示、工具限制和模型应用于整个会话：

    ```json theme={null}
    {
      "agent": "security-reviewer"
    }
    ```
  </Piece>

  <Piece id="mcp">
    一个 [MCP 服务器](/docs/zh-CN/mcp)从外部系统为 Claude 提供工具。在插件根目录的 `.mcp.json` 中声明它。这个从插件内的脚本启动本地服务器，并在 `/mcp` 中显示为 `plugin:my-plugin:db`：

    ```json theme={null}
    {
      "mcpServers": {
        "db": {
          "command": "node",
          "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"]
        }
      }
    }
    ```
  </Piece>

  <Piece id="lsp">
    LSP 服务器为 Claude 提供[诊断和代码导航](/docs/zh-CN/plugins/code-intelligence)。在插件根目录的 `.lsp.json` 中声明服务器。这个为 `.go` 文件连接 Go 语言服务器：

    ```json theme={null}
    {
      "gopls": {
        "command": "gopls",
        "args": ["serve"],
        "extensionToLanguage": {
          ".go": "go"
        }
      }
    }
    ```
  </Piece>
</PluginExplorer>

<h2 id="add-each-kind-of-component">
  添加每种组件
</h2>

下面的每个部分涵盖一种组件：其文件在插件中的位置、一个验证示例、插件加载后用户看到的内容，以及更改默认位置的清单键。添加你的插件需要的组件；没有任何组件是必需的。

<h3 id="skills">
  Skills
</h3>

一个 [skill](/docs/zh-CN/skills) 是一个 `SKILL.md` 文件，当其描述与任务匹配时，Claude 可以加载它。用户也可以将其作为命令运行。将每个 skill 保存在 `skills/` 下的自己的目录中：

```text theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── review/
        └── SKILL.md
```

给 `SKILL.md` 一个 `description`，以便 Claude 知道何时使用它：

```markdown skills/review/SKILL.md theme={null}
---
description: Reviews a pull request for style and test coverage. Use when asked to review code.
---

Review the changed files. Report style problems first, then missing tests.
```

加载插件后，`/my-plugin:review` 运行该 skill。命令名称和谁可以调用它遵循以下规则：

* **命令名称**：`/<plugin>:<directory>`，所以 `my-plugin` 中的 `skills/review/SKILL.md` 是 `/my-plugin:review`。如果你在 frontmatter 中设置 `name`，它会替换最后一段，插件前缀保持不变。参见 [skill 如何获得其命令名称](/docs/zh-CN/skills#how-a-skill-gets-its-command-name)
* **谁调用它**：Claude、用户或两者，由 frontmatter 控制。参见 [控制谁调用 skill](/docs/zh-CN/skills#control-who-invokes-a-skill)

你也可以将 skills 放在默认 `skills/` 目录之外：

* **其他目录**：在 `skills` 清单键中列出它们。它们添加到默认 `skills/` 扫描中，而不是替换它，不同于 `commands` 和 `agents`
* **插件根目录中的单个 skill**：没有 `skills/` 目录且没有 `skills` 清单键的情况下，插件根目录中的 `SKILL.md` 作为一个 skill 加载。在其 frontmatter 中设置 `name`，因为否则 marketplace 安装会根据其 [缓存目录](/docs/zh-CN/plugins/loading#find-plugins-on-disk) 而不是你的插件来命名该 skill

要在插件中包含说明，将其写成 skill。Claude Code 不会在插件根目录加载 `CLAUDE.md`，`claude plugin validate` 会警告 `CLAUDE.md at the plugin root is not loaded as project context`。

如果规则必须每次都成立，例如 [阻止编辑受保护的文件](/docs/zh-CN/hooks-guide#block-edits-to-protected-files)，将其添加到插件作为 [hook](#hooks) 而不是 skill。要在两者之间选择，参见 [比较相似功能](/docs/zh-CN/features-overview#compare-similar-features) 下的 Hook vs Skill 标签页。

对于 frontmatter 字段和支持文件，参见 [Skills](/docs/zh-CN/skills)。

<h3 id="commands">
  Commands
</h3>

命令是用户按名称运行的单个 Markdown 文件，例如 `/my-plugin:about`。

<Note>
  Commands 是较旧的格式，[skills](#skills) 对新工作已经取代了它们。skill 以相同的方式按名称运行，它也可以在其目录中携带支持文件。对于你从 `.claude/commands/` 迁移过来的文件，保留 `commands/`。
</Note>

在 `commands/<file>.md` 保存命令，它变成 `/<plugin>:<file>`。子目录添加一个段，所以 `commands/db/migrate.md` 是 `/my-plugin:db:migrate`。

命令文件采用与 skills 相同的 frontmatter。

<h4 id="define-commands-in-the-manifest">
  在清单中定义命令
</h4>

只有当你想将命令文件保存在 `commands/` 之外的地方，或在 `plugin.json` 中定义一个短命令而不需要单独的 Markdown 文件时，你才需要这样做。设置 `commands` 清单键，Claude Code 会读取它而不是扫描 `commands/`。该键接受一个路径、路径数组或一个对象，该对象将每个命令名称映射到 `source` 文件或内联 `content`。

此清单内联定义 `/my-plugin:about`，没有 Markdown 文件：

```json .claude-plugin/plugin.json theme={null}
{
  "name": "my-plugin",
  "commands": {
    "about": {
      "content": "Summarize what this repository does in three sentences.",
      "description": "Summarize the repository"
    }
  }
}
```

加载插件并在会话中运行 `/my-plugin:about` 以确认它已加载。

对于完整的键语法，参见 [`commands`](/docs/zh-CN/plugins/manifest-reference#commands)。

<h3 id="agents">
  Agents
</h3>

一个 [subagent](/docs/zh-CN/sub-agents) 是一个单独的助手，有自己的说明和上下文窗口，Claude 可以将任务委托给它。`agents/` 下的每个 Markdown 文件定义一个：

```markdown agents/security-reviewer.md theme={null}
---
name: security-reviewer
description: Reviews code changes for security issues. Use after edits to authentication or input handling.
model: sonnet
---

You are a security reviewer. Read the changed files and report injection, authentication, and secrets-handling risks.
```

此 Agent 名为 `my-plugin:security-reviewer`，用户可以使用 `@agent-my-plugin:security-reviewer` [显式调用它](/docs/zh-CN/sub-agents#invoke-subagents-explicitly)。名称形式是 `<plugin>:<name>`，其中 `<name>` 来自 frontmatter 的 `name` 字段，或在该字段缺失时来自文件名。

`agents` 清单键替换 `agents/` 扫描。

<h4 id="organize-agents-in-subfolders">
  在子文件夹中组织代理
</h4>

你可以将插件代理文件放在 `agents/` 的子文件夹中。Claude Code [递归加载它们](/docs/zh-CN/sub-agents#choose-the-subagent-scope)，并用冒号连接插件名称、每个子文件夹名称和文件名，以形成代理的作用域名称。例如，`my-plugin` 插件中的 `agents/review/security.md` 加载为 `my-plugin:review:security`。两个设置改变该名称：

* Frontmatter `name`：它仅替换文件名，所以 `agents/review/security.md` 中的 `name: audit` 加载为 `my-plugin:review:audit`
* 清单 [`agents`](/docs/zh-CN/plugins/manifest-reference#fields) 字段：你在那里列出的文件加载时不带子文件夹名称，所以 `"agents": "./custom/review/security.md"` 加载为 `my-plugin:security`

<h4 id="frontmatter-fields-in-plugin-agents">
  插件代理中的 Frontmatter 字段
</h4>

插件代理的 frontmatter 遵循以下规则：

* **支持的字段**：`name`、`description`、`model`、`effort`、`maxTurns`、`tools`、`disallowedTools`、`skills`、`memory`、`background`、`omitClaudeMd`、`isolation`、`color` 和 `experimental` 的 `cacheTtl` 键。唯一有效的 `isolation` 值是 `"worktree"`。参见 [支持的 frontmatter 字段](/docs/zh-CN/sub-agents#supported-frontmatter-fields) 了解每个字段的作用
* **忽略的字段**：`permissionMode`、`hooks`、`mcpServers` 和 `initialPrompt`。代理文件不能自己添加 hooks 或 MCP 服务器，所以改为添加为插件 [hooks](#hooks) 和 [MCP 服务器](#mcp-servers)
* **不解析的 Frontmatter**：代理仍然加载，每个字段都被忽略。它以文件名命名，其描述读作 `Agent from my-plugin plugin`。在你的 shell 中运行 [`claude plugin validate`](/docs/zh-CN/plugins/cli-reference#plugin-validate) 来找到这些文件

对于每个字段的作用和优先级规则，参见 [Subagents](/docs/zh-CN/sub-agents#supported-frontmatter-fields)。

<h3 id="hooks">
  Hooks
</h3>

一个 [hook](/docs/zh-CN/hooks-guide) 在 Claude Code 生命周期中的某个点自动运行某些东西，例如在每次文件编辑后：shell 命令、HTTP 请求、MCP 工具调用、对模型的提示或 subagent。在插件根目录的 `hooks/hooks.json` 中保存插件的 hooks，在顶级 `"hooks"` 键下，形状与 `settings.json` 中的 `hooks` 对象相同。这让你可以复制现有的设置 hook 而不做任何改变。

此 hook 在每次 `Write` 或 `Edit` 后运行一个捆绑脚本：

```json hooks/hooks.json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/scripts/format.sh\""
          }
        ]
      }
    ]
  }
}
```

在 `scripts/format.sh` 保存脚本并使其可执行。

加载插件并要求 Claude 编辑文件。退出 0 的 `PostToolUse` hook 在记录中不显示任何内容，所以用 [调试日志](/docs/zh-CN/hooks#debug-hooks) 或脚本本身所做的更改来确认它运行了。

`hooks/hooks.json` 和 `hooks` 清单键中的 hooks 都会加载。对于每个事件及其有效负载，参见 [Hook 事件](/docs/zh-CN/hooks#hook-events)。

要将 hooks 写成在 Claude Code 内运行并可以在其界面中绘制的 JavaScript 函数，在同一 `hooks/hooks.json` 中的 `modules` 键下列出一个模块文件。具有一个的插件是 mod。参见 [创建 mod](/docs/zh-CN/plugins/mods/create)。

<h4 id="when-plugin-hooks-fire">
  插件 hooks 何时触发
</h4>

插件的 hooks 不会等待使用插件的某个 skill 或命令。Claude Code 在会话加载插件时注册它们，从那时起它们在其事件上触发。要限制 hook 何时运行，缩小其 `matcher`。

如果 hook 从不触发，参见 [不触发的 hooks](/docs/zh-CN/plugins/troubleshooting#failed-to-load-hooks-from-and-hooks-that-dont-fire)。

<h4 id="environment-quoting-and-matching-mcp-tools">
  环境、引用和匹配 MCP 工具
</h4>

hook 的环境、`${CLAUDE_PLUGIN_ROOT}` 的引用和插件自己的 MCP 工具的匹配器工作如下：

* **环境**：每个 hook 进程在其环境中接收 `CLAUDE_PLUGIN_ROOT` 和 `CLAUDE_PLUGIN_DATA`，加上每个 [用户配置](#user-configuration) 值的 `CLAUDE_PLUGIN_OPTION_<KEY>`，所以你的脚本可以从那里读取它们
* **引用**：当 `command` 没有 `args` 时，它通过 shell 运行，所以用双引号包装 `${CLAUDE_PLUGIN_ROOT}` 路径，如 [Hooks](#hooks) 下的 `hooks/hooks.json` 示例所做的那样，以保持展开的路径为一个 shell 单词。当你改为传递 `args` 时，每个元素作为一个参数传递，没有 shell，不需要引用。参见 [exec 形式和 shell 形式](/docs/zh-CN/hooks#exec-form-and-shell-form)
* **匹配插件自己的 MCP 工具**：来自此插件声明的 [MCP 服务器](#mcp-servers) 的工具名为 `mcp__plugin_<plugin>_<server>__<tool>`，所以在匹配器中写入该完整名称。仅在服务器名称上的匹配器从不触发。参见 [匹配 MCP 工具](/docs/zh-CN/hooks#match-mcp-tools)

<h3 id="mcp-servers">
  MCP servers
</h3>

MCP 服务器从外部系统为 Claude 提供工具。在插件根目录的 `.mcp.json` 中声明它，形状与 [项目 `.mcp.json`](/docs/zh-CN/mcp#project-scope) 相同。此 `.mcp.json` 声明一个名为 `db` 的服务器：

```json .mcp.json theme={null}
{
  "mcpServers": {
    "db": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"]
    }
  }
}
```

你也可以省略 `mcpServers` 包装器，将 `db` 放在文件的顶级。

加载插件并运行 `/mcp` 以确认服务器显示为 `plugin:my-plugin:db`。

`claude plugin validate` 检查 `.mcp.json` 并报告 Claude Code 在加载时会丢弃的服务器条目为错误。需要 Claude Code v2.1.281 或更高版本。

对于坏条目在加载时显示的位置，参见 [不启动的 MCP 服务器](/docs/zh-CN/plugins/troubleshooting#invalid-mcp-server-config-for-and-mcp-servers-that-dont-start)。

`mcpServers` 清单键接受内联服务器映射、JSON 文件的路径或这些的数组。当清单服务器与 `.mcp.json` 中的服务器同名时，清单服务器替换它。

<h4 id="reach-users-on-claude-ai-and-cowork">
  到达 claude.ai 和 Cowork 上的用户
</h4>

本地 stdio 服务器，例如 [MCP 服务器](#mcp-servers) 下的 `db` 服务器，在 Claude Code 和在 Claude Desktop 应用中在你的机器上运行的 Cowork 会话中运行，但不在 claude.ai 上。要到达那里的用户，通过其 `https://` URL 引用远程服务器，claude.ai 和 Cowork 将其作为连接器提供给用户，如 [将 MCP 连接器与其 skill 捆绑](https://claude.com/docs/plugins/build#bundle-an-mcp-connector-with-its-skill) 所示。

<h4 id="server-names-tool-names-and-reloads">
  服务器名称、工具名称和重新加载
</h4>

服务器的名称、变量替换和重新加载行为遵循以下规则：

* **服务器名称**：`plugin:<plugin>:<server>`，所以 `my-plugin` 中的 `db` 服务器在 `/mcp` 中是 `plugin:my-plugin:db`。使用相同的形式在 [`mcp_tool` hook](/docs/zh-CN/hooks#mcp-tool-hook-fields) 中命名服务器
* **工具名称**：`mcp__plugin_<plugin>_<server>__<tool>`，所以该 `db` 服务器上的 `query` 工具是 `mcp__plugin_my-plugin_db__query`。这是在 [权限规则](/docs/zh-CN/permissions) 和 [hook 匹配器](#hooks) 中使用的名称
* **替换**：`${CLAUDE_PLUGIN_ROOT}` 和其他 [路径变量](#path-variables-and-persistent-data) 在 `command`、`args` 和 `env` 中被替换。`args` 中不需要引用，因为每个元素作为一个参数传递
* **重新加载**：当用户运行 `/reload-plugins` 且 [重新加载适用](/docs/zh-CN/plugins/cli-reference#reloads-that-change-mcp-tools) 时，配置未更改的服务器保持其连接。配置已更改的服务器重新连接，你删除的服务器断开连接

<h4 id="include-a-packaged-mcpb-server">
  包含打包的 MCPB 服务器
</h4>

`mcpServers` 键也接受打包的服务器作为 [MCPB 文件](https://github.com/modelcontextprotocol/mcpb)，其扩展名为 `.mcpb` 或较旧的 `.dxt`。将键指向文件，作为插件内的路径或 `https://` URL：

```json .claude-plugin/plugin.json theme={null}
{
  "name": "my-plugin",
  "mcpServers": "./servers/db.mcpb"
}
```

服务器从捆绑清单中的 `name` 获取其名称。

捆绑的自己的清单可以在 `user_config` 块中声明服务器需要的用户设置。具有必需设置但没有保存值的捆绑服务器不启动。`/plugin` **Errors** 标签显示 `Bundled MCP server "<name>" was not started: it needs configuration`。

用户可以通过以下两种方式之一提供值：

* **在 `/plugin` 中**：在 **Installed** 标签上选择插件并选择 **Configure**
* **在安装时，从 shell**：将 [`--config <server>.<key>=<value>`](/docs/zh-CN/plugins/cli-reference#plugin-install) 传递给 `claude plugin install`。需要 Claude Code v2.1.285 或更高版本，仅适用于打包在插件内的捆绑。

对于传输和身份验证，参见 [MCP](/docs/zh-CN/mcp#plugin-provided-mcp-servers)。

<h3 id="lsp-servers">
  LSP servers
</h3>

LSP 服务器为 Claude 提供诊断和代码导航。如果 [官方代码智能插件](/docs/zh-CN/plugins/code-intelligence) 已经涵盖你的语言，安装那个而不是写一个。否则在插件根目录的 `.lsp.json` 中声明服务器：

```json .lsp.json theme={null}
{
  "gopls": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

文件直接将每个服务器名称映射到其配置，映射周围没有包装对象。`command` 是二进制文件的名称，其参数在 `args` 中。`extensionToLanguage` 需要至少一个扩展名，每个都以 `.` 开头。

`claude plugin validate` 不读取此文件。当任何条目无效时，整个文件在加载时被跳过，`Invalid LSP server config for ".lsp.json"` 出现在 `/plugin` **Errors** 标签中。

你的插件配置连接但不安装服务器二进制文件，每个文件扩展名获得一个服务器：

* **缺少二进制文件**：Claude Code 从用户的 `PATH` 按名称启动 `command`。当二进制文件不存在时，服务器启动失败，`claude --debug` 记录 `LSP server <name> failed to start`
* **扩展名冲突**：当两个启用的服务器声称相同的扩展名时，首先注册的处理这些文件，另一个不用于它们，无论服务器来自一个插件还是两个。`/plugin` **Errors** 标签显示警告 `LSP server "<name>" is not used for <ext> files`

`lspServers` 清单键接受相同的映射内联、JSON 文件的路径或这些的数组，其服务器添加到 `.lsp.json` 中的服务器。当清单服务器与 `.lsp.json` 中的服务器同名时，清单服务器替换它。

对于 `transport`、超时、重启和其他字段，参见 [`lspServers`](/docs/zh-CN/plugins/manifest-reference#lspservers)。

将日志输出发送到 stderr，而不是 stdout。Claude Code 仅将服务器的 stdout 读取为协议消息，并接受最多 64 KiB 的消息头和最多 32 MiB 的消息体。

Claude Code 断开超过任一限制或向 stdout 写入非协议输出的服务器，并将断开连接计为 `restartOnCrash` 和 `maxRestarts` 的崩溃。当你使用 `--debug` 运行时，Claude Code 将命名原因的错误写入调试日志。

<h3 id="executables">
  Executables
</h3>

插件根目录中 `bin/` 中的文件在启用插件时位于 Bash 工具的 shell 的 `PATH` 上，所以 Claude 可以将它们作为裸命令运行。添加一个可执行脚本：

```bash bin/hello-plugin theme={null}
#!/bin/bash
echo "hello from my-plugin"
```

用 `chmod +x bin/hello-plugin` 使其可执行并加载插件。当你要求 Claude 运行 `hello-plugin` 时，Bash 工具结果显示脚本的输出。

插件 `bin/` 目录位于用户自己的 `PATH` 条目之后，所以插件不能遮蔽 `git`、`ls` 或另一个系统命令。

claude.ai 和 Cowork 不安装具有顶级 `bin/` 目录的插件，包括你 [通过 claude.ai 组织设置分发的](https://claude.com/docs/plugins/org-sync#keep-executables-out-of-the-top-level-bin-directory) 插件。

<h3 id="default-settings">
  Default settings
</h3>

要设置在启用插件时应用的默认值，在插件根目录添加 `settings.json`，或将相同的对象内联放在 `settings` 清单键中。两个键生效，`agent` 和 `subagentStatusLine`，每个其他键都被丢弃。

设置 `agent` 以将插件自己的一个代理作为主线程运行：

```json settings.json theme={null}
{
  "agent": "security-reviewer"
}
```

加载插件并启动会话。Claude 然后在主对话中用 `security-reviewer` 代理的系统提示和模型回答。

对于该键控制的所有内容，参见 [`agent` 设置](/docs/zh-CN/settings-reference#agent)。

当相同的键在多个地方设置时，这些规则决定哪个值适用：

* **文件优于清单**：当两者都存在且 `settings.json` 设置至少一个支持的键时，`settings.json` 适用，清单的 `settings` 被忽略
* **用户设置优于插件默认值**：跨设置源，插件默认值是最低层，所以用户自己在 `~/.claude/settings.json` 中的 `agent` 覆盖你的
* **两个插件设置相同的键**：来自最后加载的插件的值适用，`claude --debug` 记录 `overrides setting`

对于 `subagentStatusLine` 形状，参见 [subagent 状态行](/docs/zh-CN/statusline#subagent-status-lines)。

<h3 id="themes-and-output-styles">
  Themes and output styles
</h3>

插件可以包含颜色主题和输出样式。两者都出现在与用户自己相同的选择器中。对于任一个，设置清单键替换文件夹扫描。

| 组件 | 保存为 | 格式 | 出现在 | 清单键 |
| :- | :- | :- | :- | :- |
| 主题 | `themes/<slug>.json` | 用户在 `~/.claude/themes/` 中写入的 [自定义主题文件](/docs/zh-CN/terminal-config#create-a-custom-theme) 格式 | `/theme`，在文件的 `name` 下 | `experimental.themes` |
| 输出样式 | `output-styles/<name>.md` | [自定义输出样式](/docs/zh-CN/output-styles#create-a-custom-output-style) 格式，带有 `name` 和 `description` frontmatter | `/output-style`，作为 `<plugin>:<name>` | `outputStyles` |

插件主题是只读的，所以当用户在 `/theme` 中编辑一个时，编辑被保存为其自己的主题目录中的副本。

此主题在深色预设上重新着色提示符强调和错误文本：

```json themes/dracula.json theme={null}
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555"
  }
}
```

<h3 id="channels">
  Channels
</h3>

一个 [channel](/docs/zh-CN/channels) 让外部系统（如聊天应用）将消息发送到会话中。在插件中，channel 是 MCP 服务器之一加上一个 `channels` 条目，该条目绑定到它并可以提示其自己的配置。此清单将 channel 绑定到 `telegram` 服务器并要求机器人令牌：

```json .claude-plugin/plugin.json theme={null}
{
  "name": "my-plugin",
  "mcpServers": {
    "telegram": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": { "BOT_TOKEN": "${user_config.bot_token}" }
    }
  },
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": {
          "type": "string",
          "title": "Bot token",
          "description": "Telegram bot token",
          "sensitive": true
        }
      }
    }
  ]
}
```

`server` 必须匹配 `mcpServers` 中的键。每个 channel 的 `userConfig` 采用与 [顶级 `userConfig` 键](#user-configuration) 相同的形状。

对于服务器必须实现的内容以及用户如何启用 channel 插件，参见 channels 参考中的 [打包为插件](/docs/zh-CN/channels-reference#package-as-a-plugin)。对于字段表，参见 [`channels`](/docs/zh-CN/plugins/manifest-reference#channels)。

<h3 id="monitors">
  Monitors
</h3>

monitor 是在整个会话中在后台运行的 shell 命令。它打印的内容作为通知到达 Claude，所以 Claude 可以对日志或状态更改做出反应，而无需被要求观看它。在 `monitors/monitors.json` 中保存条目：

```json monitors/monitors.json theme={null}
[
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log"
  }
]
```

命令在 shell 中运行，位于会话的当前工作目录中。它以您的完整用户权限运行，并且在 [沙箱](/docs/zh-CN/sandboxing) 之外运行。

monitor 的命令在其启动位置和可以引用的内容方面受到限制：

* **仅限交互式会话**：插件 monitor 在交互式会话中启动，从不在使用 `-p` 标志的非交互模式中启动。在 API 提供商或遥测设置导致 [Monitor 工具](/docs/zh-CN/tools-reference#monitor-tool) 不可用的会话中，它们也不会启动
* **无用户配置**：`command` 从环境中获取 [路径变量](#path-variables-and-persistent-data) 和 `${ENV_VAR}`，但从不获取 `${user_config.*}`。引用一个的 monitor 不启动，monitor 进程也不接收 `CLAUDE_PLUGIN_OPTION_<KEY>`
* **会话中期禁用**：如果你在会话中期禁用插件，Claude Code 不会停止已经运行的 monitors。它们在会话结束时停止

`experimental.monitors` 清单键接受相同的数组内联或 JSON 文件的路径，并被读取而不是 `monitors/monitors.json`。

对于 `when` 触发器和其他字段，参见 [`monitors`](/docs/zh-CN/plugins/manifest-reference#monitors)。

<h2 id="user-configuration">
  要求用户提供配置值
</h2>

在 `userConfig` 清单键中声明您的插件需要的值，以便用户不自己编辑 `settings.json`。每个选项显示在一个对话框中，其 `title` 作为标签，其 `description` 在下方。

为令牌或密码设置 `"sensitive": true`。对话框然后掩盖输入，值存储在安全存储中而不是 `settings.json`。

此清单要求端点和令牌：

```json .claude-plugin/plugin.json theme={null}
{
  "name": "my-plugin",
  "userConfig": {
    "api_url": {
      "type": "string",
      "title": "API URL",
      "description": "Base URL of your team's API"
    },
    "api_token": {
      "type": "string",
      "title": "API token",
      "description": "Token for your team's API",
      "sensitive": true
    }
  }
}
```

<h3 id="when-the-configuration-dialog-appears">
  配置对话框何时出现
</h3>

对话框是交互式 `/plugin` 界面的一部分。当用户执行以下任何操作时，它为任何尚未设置的选项打开：

* 在 `/plugin` 中安装插件
* 在会话内运行 `/plugin install <plugin>@<marketplace>`
* 从 `/plugin` 中的 **Installed** 标签启用插件

要在任何时间打开相同的对话框，用户运行 `/plugin configure <plugin>@<marketplace>`。

VS Code 扩展的[管理插件对话框](/docs/zh-CN/vs-code#install-plugins)在安装后作为表单请求未设置的选项，插件行上的齿轮图标再次打开包含每个选项的表单。

`claude plugin install` shell 命令从不提示 `userConfig` 值。要从 shell 设置值，在安装时将每个值作为 `--config KEY=VALUE` 传递，或之后将 JSON 对象管道传输到 [`claude plugin configure --values-stdin`](/docs/zh-CN/plugins/cli-reference#plugin-configure)。

当选项保持未设置时，`claude plugin install` 打印一个 `userConfig options not yet set` 行。有关该行的确切文本，请参阅[`userConfig` 对话框从不出现](/docs/zh-CN/plugins/troubleshooting#the-userconfig-dialog-never-appears)。

对于选项字段、每个值存储的位置、组件如何引用保存的值以及哪些字段拒绝 `${user_config.*}`，请参阅[用户配置](/docs/zh-CN/plugins/manifest-reference#user-configuration)。

<h2 id="path-variables-and-persistent-data">
  引用插件路径和存储数据
</h2>

您不知道您的插件将被安装在哪里，所以通过这些变量而不是固定路径引用其文件和数据。它们在 skill、命令和 agent 内容、hook 和监视器命令以及 MCP 和 LSP 服务器配置中被替换。它们也被导出到 hook、MCP 和 LSP 进程：

* **`${CLAUDE_PLUGIN_ROOT}`**：插件的安装目录。每个版本都有自己的[缓存目录](/docs/zh-CN/plugins/loading#find-plugins-on-disk)，所以当插件更新时路径改变。不要在那里写状态
* **`${CLAUDE_PLUGIN_DATA}`**：一个在更新中存活的目录，用于 `node_modules`、虚拟环境和缓存。它解析为 `~/.claude/plugins/data/<id>/` 并在首次引用时创建
* **`${CLAUDE_PROJECT_DIR}`**：项目根目录，hooks 接收的相同值

在数据目录路径中，`<id>` 是插件标识符，每个字符除了字母、数字、`_` 和 `-` 被替换为 `-`，所以 `my-plugin@my-marketplace` 变成 `my-plugin-my-marketplace`。

在 Windows 上，替换的路径使用正斜杠，所以 shell 不将反斜杠读取为转义。

<h3 id="install-dependencies-into-the-data-directory">
  将依赖项安装到数据目录
</h3>

对于市场安装的插件，Claude Code 在缓存插件时自动安装符合条件的 [Node.js 包依赖项](/docs/zh-CN/plugins/loading#node-js-package-dependencies)，所以您可能不需要自己安装它们。当您这样做时，此 `SessionStart` hook 在首次运行时将 `node_modules` 安装到 `${CLAUDE_PLUGIN_DATA}` 中，并在更新改变 `package.json` 后再次安装：

```json hooks/hooks.json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}
```

在第一个会话后，`~/.claude/plugins/data/<id>/node_modules` 存在。MCP 服务器然后可以在其 `env` 中设置 `NODE_PATH` 为 `${CLAUDE_PLUGIN_DATA}/node_modules`。对于哪些字段替换哪个变量，请参阅[环境变量](/docs/zh-CN/plugins/manifest-reference#environment-variables)。

<h2 id="next-steps">
  后续步骤
</h2>

* [插件清单参考](/docs/zh-CN/plugins/manifest-reference)：`plugin.json` 字段、路径规则和标准布局
* [使用 evals 测试插件](/docs/zh-CN/plugin-evals)：检查您添加的组件以您打算的方式改变 Claude 的行为
* [发布和分发插件](/docs/zh-CN/plugins/publish)：版本化插件并将其放在市场中
* [排查插件问题](/docs/zh-CN/plugins/troubleshooting)：当组件不加载或 hook 不触发时该怎么办
