> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 设置文件和优先级

> 更改 Claude Code 设置，选择键所属的作用域，验证更改，并了解当键在多个位置设置时 Claude Code 使用哪个值。

export const SettingsPrecedence = () => {
  const LEVELS = [{
    n: 1,
    name: 'Managed settings',
    file: 'managed-settings.json, MDM, or the claude.ai console',
    who: 'Your organization',
    w: 390
  }, {
    n: 2,
    name: 'Command line',
    file: 'claude --settings',
    who: 'You, this session',
    w: 420
  }, {
    n: 3,
    name: 'Project local',
    file: '.claude/settings.local.json',
    who: 'You, this project',
    w: 480
  }, {
    n: 4,
    name: 'Shared project',
    file: '.claude/settings.json',
    who: 'Everyone in the project',
    w: 540
  }, {
    n: 5,
    name: 'User',
    file: '~/.claude/settings.json',
    who: 'You, every project',
    w: 600
  }];
  const W = 760;
  const ROW = 58;
  const GAP = 8;
  const TOP = 34;
  const H = TOP + LEVELS.length * (ROW + GAP) + 30;
  const cx = W / 2;
  const mono = 'var(--font-mono, ui-monospace, SFMono-Regular, Menlo, monospace)';
  const sans = 'var(--font-sans, system-ui, -apple-system, sans-serif)';
  return <div className="sp-root not-prose" role="img" aria-label="Settings precedence, highest first: managed settings, command line, project local, shared project, user. A key set at a higher level overrides the same key set lower down.">
      <style>{`
        .sp-root { --sp-text: #1A1918; --sp-sub: #5E5D59; --sp-faint: #8A8880; --sp-fill: #F5F4EF; --sp-stroke: rgba(0,0,0,0.12); --sp-top: #D97757; --sp-top-fill: rgba(217,119,87,0.14); --sp-arrow: #8A8880; margin: 1.25rem 0; }
        .dark .sp-root { --sp-text: #F1EFE9; --sp-sub: #B8B5AD; --sp-faint: #8A8880; --sp-fill: #24231F; --sp-stroke: rgba(255,255,255,0.12); --sp-top-fill: rgba(217,119,87,0.22); --sp-arrow: #8A8880; }
        .sp-root svg { width: 100%; height: auto; display: block; max-width: ${W}px; margin: 0 auto; }
      `}</style>
      <svg viewBox={`0 0 ${W} ${H}`} xmlns="http://www.w3.org/2000/svg">
        <text x={cx} y={18} textAnchor="middle" fontFamily={sans} fontSize="12.5" fontWeight="600" fill="var(--sp-sub)">Highest precedence</text>
        {LEVELS.map((l, i) => {
    const y = TOP + i * (ROW + GAP);
    const x = cx - l.w / 2;
    const top = i === 0;
    return <g key={l.n}>
              <rect x={x} y={y} width={l.w} height={ROW} rx={10} fill={top ? 'var(--sp-top-fill)' : 'var(--sp-fill)'} stroke={top ? 'var(--sp-top)' : 'var(--sp-stroke)'} strokeWidth={top ? 1.5 : 1} />
              <text x={x + 14} y={y + 24} fontFamily={sans} fontSize="14" fontWeight="600" fill="var(--sp-text)">{l.n}. {l.name}</text>
              <text x={x + 14} y={y + 43} fontFamily={mono} fontSize="11.5" fill="var(--sp-sub)">{l.file}</text>
              <text x={x + l.w - 14} y={y + 24} textAnchor="end" fontFamily={sans} fontSize="12" fill="var(--sp-faint)">{l.who}</text>
            </g>;
  })}
        <text x={cx} y={H - 10} textAnchor="middle" fontFamily={sans} fontSize="12.5" fontWeight="600" fill="var(--sp-sub)">Lowest precedence</text>
        <g stroke="var(--sp-arrow)" strokeWidth="1.5" fill="none">
          <line x1={W - 40} y1={TOP + 10} x2={W - 40} y2={H - 38} />
          <path d={`M ${W - 46} ${TOP + 18} L ${W - 40} ${TOP + 10} L ${W - 34} ${TOP + 18}`} />
        </g>
        <text x={W - 40} y={H - 22} textAnchor="middle" fontFamily={sans} fontSize="10.5" fill="var(--sp-faint)">overrides</text>
      </svg>
    </div>;
};

export const SettingsScope = ({defaultSelected = 'project'}) => {
  const FILES = [{
    id: 'user',
    path: '~/.claude/settings.json'
  }, {
    id: 'project',
    path: 'acme-app/.claude/settings.json'
  }, {
    id: 'local',
    path: 'acme-app/.claude/settings.local.json'
  }, {
    id: 'managed',
    path: 'Managed settings',
    ring: 'managed-settings.json, MDM, or the claude.ai console'
  }];
  const SHORT = {
    user: '~/.claude/settings.json',
    project: 'acme-app/.claude/settings.json',
    local: 'acme-app/.claude/settings.local.json',
    managed: 'managed-settings.json, MDM, or the claude.ai console'
  };
  const TILE_MARK = {
    project: 'settings.json',
    local: 'settings.local.json'
  };
  const initial = FILES.some(f => f.id === defaultSelected) ? defaultSelected : 'project';
  const [sel, setSel] = useState(initial);
  const [scale, setScale] = useState(1);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const rootRef = useRef(null);
  const frameRef = useRef(null);
  const CANVAS_W = 862;
  const CANVAS_H = 240;
  useEffect(() => {
    const el = frameRef.current;
    if (!el) return;
    const measure = () => setScale(Math.min(1, el.clientWidth / CANVAS_W));
    measure();
    if (typeof ResizeObserver === 'undefined') {
      window.addEventListener('resize', measure);
      return () => window.removeEventListener('resize', measure);
    }
    const ro = new ResizeObserver(measure);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  useEffect(() => {
    const onFsChange = () => setIsFullscreen(!!document.fullscreenElement);
    document.addEventListener('fullscreenchange', onFsChange);
    return () => document.removeEventListener('fullscreenchange', onFsChange);
  }, []);
  const toggleFullscreen = () => {
    if (!rootRef.current) return;
    if (document.fullscreenElement) document.exitFullscreen(); else rootRef.current.requestFullscreen().catch(() => {});
  };
  const COVERAGE = {
    user: ['website', 'api', 'yacme'],
    project: ['yacme', 'tacme', 'cacme'],
    local: ['yacme'],
    managed: ['website', 'api', 'yacme', 'tacme', 'cacme']
  };
  const RINGS = {
    local: {
      l: 282,
      t: 50,
      w: 142,
      h: 124
    },
    project: {
      l: 282,
      t: 50,
      w: 560,
      h: 124
    },
    user: {
      l: 2,
      t: 34,
      w: 446,
      h: 198
    },
    managed: {
      l: 0,
      t: 32,
      w: 862,
      h: 204
    }
  };
  const TILES = [{
    id: 'website',
    name: 'website/',
    left: 30,
    caption: ''
  }, {
    id: 'api',
    name: 'api/',
    left: 160,
    caption: ''
  }, {
    id: 'yacme',
    name: 'acme-app/',
    left: 290,
    caption: ''
  }, {
    id: 'tacme',
    name: 'acme-app/',
    left: 497,
    caption: sel === 'project' ? 'their clone, once you commit the file' : 'their clone'
  }, {
    id: 'cacme',
    name: 'acme-app/',
    left: 704,
    caption: sel === 'project' ? 'fresh clone, once you commit the file' : sel === 'managed' ? 'server-managed only' : 'fresh clone'
  }];
  const FILE_AT = {
    user: {
      machine: 'you',
      tiles: []
    },
    project: {
      machine: null,
      tiles: ['yacme', 'tacme', 'cacme']
    },
    local: {
      machine: null,
      tiles: ['yacme']
    },
    managed: {
      machine: null,
      tiles: []
    }
  };
  const fileAt = FILE_AT[sel];
  const coverage = COVERAGE[sel];
  const ring = RINGS[sel];
  const selFile = FILES.find(f => f.id === sel);
  const FolderIcon = ({open}) => <svg width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinejoin="round" aria-hidden="true">
      <path d="M1.5 4.5a1 1 0 0 1 1-1h3.2l1.3 1.5h6a1 1 0 0 1 1 1V12a1 1 0 0 1-1 1h-10.5a1 1 0 0 1-1-1z" />
      {open && <path d="M1.5 7.5h13" />}
    </svg>;
  const FileIcon = () => <svg width="10" height="10" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinejoin="round" aria-hidden="true">
      <path d="M4 1.5h5.5L13 5v9.5H4z" />
      <path d="M9.5 1.5V5H13" />
    </svg>;
  const CloudIcon = () => <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinejoin="round" aria-hidden="true">
      <path d="M4.5 12.5h7a2.5 2.5 0 0 0 .4-4.97A3.5 3.5 0 0 0 5.2 6.6 3 3 0 0 0 4.5 12.5z" />
    </svg>;
  const LaptopIcon = () => <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinejoin="round" aria-hidden="true">
      <rect x="2.5" y="3" width="11" height="7.5" rx="1" />
      <path d="M1 12.5h14" />
    </svg>;
  return <div ref={rootRef} className={'ssc-root not-prose' + (isFullscreen ? ' ssc-fs' : '')}>
      <style>{`
        .ssc-root {
          --ssc-bg: #FFFFFF;
          --ssc-text: #1A1918;
          --ssc-sub: #5E5D59;
          --ssc-faint: #8A8880;
          --ssc-border: rgba(0,0,0,0.12);
          --ssc-panel: #F5F4EF;
          --ssc-tile: #FAFAF8;
          --ssc-clay: #D97757;
          --ssc-clay-bg: rgba(217,119,87,0.14);
          --ssc-label: #B0562F;
          --ssc-hover: rgba(115,114,108,0.10);
          font-family: var(--font-sans, system-ui, -apple-system, sans-serif);
          background: var(--ssc-bg);
          color: var(--ssc-text);
          border: 1px solid var(--ssc-border);
          border-radius: 16px;
          padding: 20px 24px 24px;
          margin: 1.5rem 0;
          box-sizing: border-box;
        }
        .dark .ssc-root {
          --ssc-bg: #1B1A18;
          --ssc-text: #F1EFE9;
          --ssc-sub: #B8B5AD;
          --ssc-faint: #8A8880;
          --ssc-border: rgba(255,255,255,0.12);
          --ssc-panel: #24231F;
          --ssc-tile: #2A2925;
          --ssc-clay-bg: rgba(217,119,87,0.20);
          --ssc-label: #EBC9B7;
        }
        .ssc-fs { display: flex; flex-direction: column; justify-content: center; align-items: center; margin: 0; border-radius: 0; height: 100vh; }
        .ssc-fs .ssc-head { width: 100%; max-width: ${CANVAS_W}px; }
        .ssc-fs .ssc-frame { width: 100%; }
        .ssc-mono { font-family: var(--font-mono, ui-monospace, SFMono-Regular, Menlo, monospace); }
        .ssc-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; margin-bottom: 20px; }
        .ssc-files { display: flex; gap: 8px; flex-wrap: wrap; }
        .ssc-file {
          font-size: 12.5px; font-weight: 430; padding: 8px 13px; border-radius: 10px; cursor: pointer;
          border: 0.5px solid var(--ssc-border); background: var(--ssc-tile); color: var(--ssc-text);
          white-space: nowrap; transition: background 0.2s, border-color 0.2s;
        }
        .ssc-file:hover { filter: brightness(0.97); }
        .ssc-file[aria-pressed="true"] { font-weight: 600; border: 1.5px solid var(--ssc-clay); background: var(--ssc-clay-bg); }
        .ssc-fsbtn {
          display: flex; align-items: center; justify-content: center; width: 28px; height: 28px; flex-shrink: 0;
          border: none; background: none; border-radius: 6px; cursor: pointer; color: var(--ssc-faint); font-size: 15px;
        }
        .ssc-fsbtn:hover { background: var(--ssc-hover); }
        .ssc-frame { width: 100%; max-width: ${CANVAS_W}px; margin: 0 auto; }
        .ssc-canvas { position: relative; width: ${CANVAS_W}px; height: ${CANVAS_H}px; transform-origin: top left; }
        .ssc-machine { position: absolute; top: 42px; height: 182px; background: var(--ssc-panel); border-radius: 16px; }
        .ssc-machine-label { position: absolute; top: 192px; display: flex; align-items: center; gap: 8px; font-size: 13.5px; font-weight: 600; }
        .ssc-tile {
          position: absolute; top: 58px; width: 126px; height: 108px; border-radius: 12px; padding: 11px 12px; box-sizing: border-box;
          background: var(--ssc-tile); border: 0.5px solid var(--ssc-border); opacity: 0.6;
          transition: background 0.25s, border-color 0.25s, opacity 0.25s;
        }
        .ssc-tile.ssc-on { background: var(--ssc-clay-bg); border: 1px solid var(--ssc-clay); opacity: 1; }
        .ssc-tile-name { display: flex; align-items: center; gap: 6px; color: var(--ssc-faint); }
        .ssc-tile.ssc-on .ssc-tile-name { color: var(--ssc-clay); }
        .ssc-tile-name span { font-size: 12px; font-weight: 430; white-space: nowrap; color: var(--ssc-text); }
        .ssc-tile.ssc-on .ssc-tile-name span { font-weight: 600; }
        .ssc-tile-caption { font-size: 10.5px; color: var(--ssc-sub); margin-top: 5px; line-height: 1.35; }
        .ssc-filemark {
          position: absolute; left: 5px; right: 5px; bottom: 8px; display: inline-flex; align-items: center; justify-content: center; gap: 2px;
          font-size: 8.5px; color: var(--ssc-label); background: var(--ssc-bg); border: 1px solid var(--ssc-clay);
          border-radius: 6px; padding: 2px 3px; white-space: nowrap; overflow: hidden;
        }
        .ssc-filemark svg { flex-shrink: 0; }
        .ssc-machine-filemark { display: inline-flex; align-items: center; gap: 4px; margin-left: 10px; font-size: 10.5px; font-weight: 500; color: var(--ssc-label); }
        .ssc-ring {
          position: absolute; border: 2px solid var(--ssc-clay); border-radius: 18px; pointer-events: none;
          transition: left 0.35s ease, top 0.35s ease, width 0.35s ease, height 0.35s ease;
        }
        .ssc-ring-label {
          position: absolute; font-size: 12px; font-weight: 600; color: var(--ssc-label); white-space: nowrap; pointer-events: none;
          transition: left 0.35s ease, top 0.35s ease;
        }
      `}</style>

      <div className="ssc-head">
        <div className="ssc-files" role="group" aria-label="Settings file">
          {FILES.map(f => <button key={f.id} type="button" className="ssc-file ssc-mono" aria-pressed={f.id === sel} onClick={() => setSel(f.id)}>{f.path}</button>)}
        </div>
        <button type="button" className="ssc-fsbtn" onClick={toggleFullscreen} aria-label={isFullscreen ? 'Exit fullscreen' : 'Enter fullscreen'} title={isFullscreen ? 'Exit fullscreen' : 'Fullscreen'}>{isFullscreen ? '⤡' : '⛶'}</button>
      </div>

      <div ref={frameRef} className="ssc-frame" style={{
    height: CANVAS_H * scale + 'px'
  }}>
        <div className="ssc-canvas" style={{
    transform: 'scale(' + scale + ')'
  }}>
          <div className="ssc-machine" style={{
    left: '10px',
    width: '430px'
  }} />
          <span className="ssc-machine-label" style={{
    left: '30px'
  }}><LaptopIcon />Your machine{fileAt.machine === 'you' && <span className="ssc-machine-filemark ssc-mono"><FileIcon />{selFile.path}</span>}</span>
          <div className="ssc-machine" style={{
    left: '460px',
    width: '200px'
  }} />
          <span className="ssc-machine-label" style={{
    left: '470px'
  }}><LaptopIcon />A teammate’s machine</span>
          <div className="ssc-machine" style={{
    left: '682px',
    width: '170px'
  }} />
          <span className="ssc-machine-label" style={{
    left: '692px'
  }}><CloudIcon />A cloud session</span>

          {TILES.map(t => {
    const on = coverage.includes(t.id);
    return <div key={t.id} className={'ssc-tile' + (on ? ' ssc-on' : '')} style={{
      left: t.left + 'px'
    }}>
                <div className="ssc-tile-name"><FolderIcon open={on} /><span className="ssc-mono">{t.name}</span></div>
                {t.caption && <div className="ssc-tile-caption">{t.caption}</div>}
                {fileAt.tiles.includes(t.id) && <span className="ssc-filemark ssc-mono" title={SHORT[sel]}><FileIcon />{TILE_MARK[sel]}</span>}
              </div>;
  })}

          <div className="ssc-ring" style={{
    left: ring.l + 'px',
    top: ring.t + 'px',
    width: ring.w + 'px',
    height: ring.h + 'px'
  }} />
          <span className="ssc-ring-label ssc-mono" style={{
    left: ring.l + 14 + 'px',
    top: ring.t - 26 + 'px'
  }}>{selFile.ring || selFile.path}</span>
        </div>
      </div>
    </div>;
};

设置是改变 Claude Code 行为方式的 JSON 键：它启动时使用的模型、它可以在不询问的情况下运行的内容、它无法读取的文件、它在终端中的外观，以及您的组织强制执行的内容。

<Tip>
  要查找特定键，请转到[所有设置](/docs/zh-CN/settings-reference)，其中列出了每个键、设置它的文件、其默认值和示例。
</Tip>

Claude Code 从 JSON 设置文件（如 `~/.claude/settings.json`）读取设置。它在几个位置查找它们，[它读取设置的文件决定了设置适用于谁](#settings-files-and-who-they-affect)。本页涵盖这些文件：将设置放在哪个文件中、如何更改设置并确认它已应用，以及当同一键在多个文件中设置时 Claude Code 使用哪个值。[配置权限](/docs/zh-CN/permissions)涵盖 Claude Code 可以在不询问的情况下运行的内容以及如何编写 `allow`、`ask` 和 `deny` 规则。

<Note>
  本页涵盖在您的机器上运行的 Claude Code：终端、[VS Code](/docs/zh-CN/vs-code) 和 [JetBrains](/docs/zh-CN/jetbrains) 扩展，以及[桌面应用](/docs/zh-CN/desktop)，它们都读取相同的设置文件。[Claude Code on the web](/docs/zh-CN/claude-code-on-the-web) 上的云会话在不同的机器上运行并仅读取其中一些；请参阅[云会话中的设置](#settings-in-cloud-sessions)。
</Note>

<span id="settings-files" />

<span id="configuration-scopes" />

<span id="available-scopes" />

<span id="when-to-use-each-scope" />

<span id="what-uses-scopes" />

<span id="subagent-configuration" />

<span id="where-settings-live" />

<h2 id="settings-files-and-who-they-affect">
  设置文件及其影响范围
</h2>

Claude Code 从四个文件读取设置，组织也可以从 claude.ai 控制台提供托管设置。每个来源都有一个作用域：设置应用的人员和项目范围，可能是仅限于你、项目中的所有人，或组织中的所有人。

| 作用域 | 文件 | 影响范围 | 用途 |
| :- | :- | :- | :- |
| 用户 | `~/.claude/settings.json` | 你在这台机器上的每个项目中 | 个人偏好：主题、编辑器模式、默认模型、你自己的权限规则 |
| 共享项目 | `.claude/settings.json` | 包含该文件的文件夹中的所有人。在 git 仓库中，提交它以便队友获得 | 团队权限、hooks、plugins 和项目需要的环境变量 |
| 项目本地 | `.claude/settings.local.json` | 仅在这个项目中的你。Claude Code 在创建文件时将其排除在 git 之外；如果你手动创建，请自己添加到 `.gitignore` | 单个项目的个人覆盖，以及在共享前的测试 |
| 托管 | `managed-settings.json` 和其他[托管来源](/docs/zh-CN/managed-settings#delivery-mechanisms) | 你的组织部署到的所有人；你设置的任何内容都不会覆盖它，除了少数[安全敏感的例外](#exceptions-to-managed-settings-precedence) | 安全策略和合规要求 |

在"文件"列中，`~/.claude` 是你主目录中的 `.claude` 文件夹，而单独的 `.claude` 是项目内的 `.claude` 文件夹。

<span id="where-each-file-applies" />

<span id="compare-what-each-file-reaches" />

<h3 id="compare-the-scope-of-each-settings-file">
  比较每个设置文件的作用域
</h3>

假设你在机器上有三个项目：`website/`、`api/` 和 `acme-app/`，一个队友有他们自己的 `acme-app/` 克隆，你在 `acme-app/` 上启动了一个[云会话](#settings-in-cloud-sessions)。

下面的图表显示当你从这些文件夹启动 Claude Code 时，设置应用在哪些文件夹中。点击一个设置文件查看它到达的文件夹。

<SettingsScope />

* **`~/.claude/settings.json`**：你机器上的每个项目，以及队友机器上或云会话中都没有
* **`acme-app/.claude/settings.json`**：你的 `acme-app/`。只有当你将文件提交到版本控制时，它才会到达你队友的克隆和云会话；在此之前，它就像任何其他磁盘上的文件一样，其他人没有它
* **`acme-app/.claude/settings.local.json`**：仅你的 `acme-app/`。Claude Code 第一次写入文件时将其添加到你的全局 git 排除项中，因此它不会进入你的提交；如果你手动创建文件，[自己添加到 `.gitignore`](#keep-personal-settings-out-of-a-repository)
* **托管设置**，无论是 `managed-settings.json` 文件、MDM 策略，还是来自 claude.ai 控制台的[服务器托管设置](/docs/zh-CN/server-managed-settings)：你的组织部署到的每台机器上的每个项目，或你使用组织账户登录的地方。只有服务器托管设置到达云会话

<span id="which-files-you-have" />

<h3 id="find-or-create-your-settings-files">
  查找或创建你的设置文件
</h3>

安装 Claude Code 不会创建任何设置文件。如果你的机器或项目已经有一个，它来自以下来源之一：

* **托管**：你的组织部署它。你不创建或编辑它。
* **共享项目**：已经使用 Claude Code 的项目可能已提交一个。如果没有，在项目文件夹中的 `.claude/settings.json` 创建一个。
* **用户**和**项目本地**：自己创建它们，或让 Claude Code 创建它们。当你在 `/config` 菜单中更改存储在用户设置中的选项（如主题）时，它会写入 `~/.claude/settings.json`，当你在权限提示上给予常设批准（如对 Bash 命令的"是的，不要再问"）时，它会写入 `.claude/settings.local.json`。一些 `/config` 选项，包括**显示提示**，保存到 `.claude/settings.local.json` 而不是用户文件。

<Info>
  在 Windows 上，`~/.claude` 表示 `%USERPROFILE%\.claude`。要将主目录文件保存在其他地方，设置 [`CLAUDE_CONFIG_DIR`](/docs/zh-CN/env-vars)；Claude Code 然后将你的设置、会话历史和 plugins 存储在那里。
</Info>

Claude Code 还保留第五个文件 [`~/.claude.json`](/docs/zh-CN/claude-directory#ce-claude-json)，它为自己写入；你不需要编辑它。它保存你的登录会话、[MCP server](/docs/zh-CN/mcp) 配置、每个项目的状态（如信任决定），以及 `/config` 为你写入的[全局配置键](/docs/zh-CN/settings-reference#global-config-settings)。

<h3 id="share-settings-with-your-team">
  与你的团队共享设置
</h3>

提交 `.claude/settings.json` 以便克隆仓库的每个人都获得相同的权限、hooks 和 plugins。每个队友仍然可以在他们自己的 `.claude/settings.local.json` 中为自己覆盖它，因此个人例外不需要提交。有关完整的团队文件，请参阅[团队的共享设置](/docs/zh-CN/settings-example#a-teams-shared-settings)。

你提交的一些内容等待每个队友[信任文件夹](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)，少数键永远不会从仓库文件生效；[排查不适用的设置](#common-cases)涵盖两者。

<span id="local-settings-file" />

<span id="where-claude-code-saves-the-project-local-file" />

<span id="the-project-local-file" />

<span id="keep-personal-settings-out-of-the-repository" />

<h3 id="keep-personal-settings-out-of-a-repository">
  将个人设置保留在仓库之外
</h3>

要在一个项目中为自己更改设置而不为队友更改，请在项目内的 `.claude/settings.local.json` 中保存它。Claude Code 在提交的 `.claude/settings.json` 上应用该文件，因此如果你的团队文件设置 `"model": "claude-sonnet-5"` 而你想要 Opus，在你的本地文件中放入 `"model": "claude-opus-5-5"`，只有你的会话会改变。

Claude Code 也会写入此文件，将其保留在你的提交之外，并应用其允许规则而无需信任步骤：

* **Claude Code 也会写入它。** 当 Claude 要求运行 Bash 命令的权限，你选择"是的，不要再问"时，Claude Code 将该[权限批准](/docs/zh-CN/permissions#permission-system)保存为此处的 `allow` 规则。
* **除非你手动创建，否则你不需要 gitignore 它。** Claude Code 第一次在不已忽略它的 git 仓库中写入文件时，它会将 `**/.claude/settings.local.json` 添加到你的全局 git 排除文件中，因此该文件在每个仓库中都不会进入你的提交。该文件是 `core.excludesFile`（当你的全局 git 配置将其设置为绝对路径或 `~` 前缀路径时）；否则是 `$XDG_CONFIG_HOME/git/ignore`，或当 `XDG_CONFIG_HOME` 未设置时是 `~/.config/git/ignore`。如果你手动创建了文件，Claude Code 还没有写入它，请自己添加到 `.gitignore`。
* **当文件保持未跟踪时，其允许规则不等待信任。** 因为文件是你的而不是仓库的，Claude Code 应用其 `allow` 规则而无需它对提交文件要求的[工作区信任](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)步骤。如果文件被 git 跟踪，信任步骤也适用于它；请参阅[当你的本地设置文件需要信任](/docs/zh-CN/permissions#when-your-local-settings-file-needs-trust)。

<span id="where-claude-code-looks-for-each-file" />

<span id="how-claude-code-keeps-the-local-file-out-of-git" />

<span id="local-allow-rules-dont-wait-for-workspace-trust" />

<h4 id="where-claude-code-keeps-the-local-file-in-a-git-repository">
  Claude Code 在 git 仓库中保留本地文件的位置
</h4>

当 Claude 要求运行 Bash 命令的权限，你选择"是的，不要再问"时，Claude Code 将该批准保存为 `.claude/settings.local.json` 中的 `allow` 规则。如果你在 git 仓库的子目录中启动 Claude Code，它会在仓库根目录读取和写入该文件，并在整个仓库中应用批准。在[worktree](/docs/zh-CN/worktrees) 中，它使用主检出根目录处的文件。

两条规则限定根位置：

* **当文件与 `.claude/settings.json` 保持在一起时**：在 git 仓库之外，当仓库根是你的主目录时，在 Windows 上，或当仓库根或其 `.git` 或 `.claude` 条目不由你的用户拥有时。
* **文件中的路径不在仓库根处锚定**：以 `/` 开头的权限规则或相对沙箱路径[在会话的主工作目录处锚定](/docs/zh-CN/permissions#read-and-edit)。

在 v2.1.211 之前，Claude Code 将文件保留在启动目录中。它仍然读取早期版本在根文件旁边留下的文件；当两者设置相同的键时，根的值适用，两个文件的权限规则都适用。Agent SDK 的 [`resolveSettings()`](/docs/zh-CN/agent-sdk/typescript#resolvesettings) 助手始终从启动目录读取文件。

Claude Code 从会话的[主工作目录](/docs/zh-CN/permissions#working-directories)读取共享的 `.claude/settings.json`，因此要使用在仓库根处提交的文件，请从那里启动 Claude Code。在你[使用 `/cd` 移动会话](/docs/zh-CN/permissions#move-the-session-to-another-directory)后，Claude Code 改为从新目录读取两个项目文件，按相同规则放置本地文件。从你移动到的目录读取它们需要 Claude Code v2.1.246 或更高版本。

<span id="managed-settings-delivery" />

<span id="precedence-within-the-managed-tier" />

<span id="parent-settings-from-embedding-hosts" />

<span id="enforce-settings-for-an-organization" />

<span id="settings-your-organization-manages" />

<h3 id="check-what-your-organization-enforces">
  检查你的组织强制执行的内容
</h3>

如果你的组织管理 Claude Code，某些设置是为你决定的，你在自己的文件中放入的任何内容都不会改变它们。要查看哪些，运行 `/status`：`Setting sources` 行命名适用于你的托管来源。托管设置在这台机器上 Claude Code 运行的任何地方都适用；[开发人员可以更改的内容](/docs/zh-CN/managed-settings#what-a-developer-can-change)涵盖本地管理员权限和 Claude Code 以外的工具。

托管设置通过托管设置页面上的[交付机制](/docs/zh-CN/managed-settings#delivery-mechanisms)到达你，最常见的是：

* [服务器托管设置](/docs/zh-CN/server-managed-settings)，Claude Code 从 claude.ai 管理控制台或自托管的 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 获取
* MDM 或操作系统级别的策略，以及系统目录中的 `managed-settings.json` 文件
* 嵌入主机（如 Claude Desktop），通过 SDK `managedSettings` 选项；请参阅[从嵌入主机控制策略](/docs/zh-CN/managed-settings#parent-settings-from-embedding-hosts)

在在 Claude Desktop 应用中在你的机器上运行的 [Cowork](https://claude.com/docs/cowork/overview) 会话中，Claude Code 不会从 claude.ai 管理控制台获取服务器托管设置，它读取部署到你的设备的策略，除非你的组织的 Claude Desktop 配置设置 `requireCoworkFullVmSandbox`。[策略应用的位置和时间](/docs/zh-CN/managed-settings#where-and-when-a-policy-applies)涵盖 Cowork 和云会话。

如果你是管理员，[为你的组织设置 Claude Code](/docs/zh-CN/admin-setup) 介绍了选择要强制执行的内容，[部署托管设置](/docs/zh-CN/managed-settings)涵盖交付以及如何确认策略生效。

<h2 id="change-a-setting">
  更改设置
</h2>

您可以从 `/config` 菜单、通过编辑设置文件或对一个会话从命令行更改设置。

<span id="system-prompt" />

Claude Code 的系统提示未发布。要给 Claude 常设指令，使用 [`CLAUDE.md` 文件](/docs/zh-CN/memory)或 `--append-system-prompt` 标志。

<h3 id="use-the-/config-menu">
  使用 /config 菜单
</h3>

在 Claude Code 内运行 `/config` 并打开**配置**选项卡。它列出了一小组个人选项，如主题、编辑器模式和详细输出，而不是每个设置键。选择一个选项来更改它；Claude Code 为您保存它：

* **大多数选项**：`~/.claude/settings.json`
* **一些选项，如显示提示**：`.claude/settings.local.json`
* **[全局配置选项](/docs/zh-CN/settings-reference#global-config-settings)**：`~/.claude.json`

要设置一个选项而不使用菜单，传递 `key=value`，例如 `/config verbose=true`。

<Note>
  `/config` 是终端界面的一部分。[VS Code](/docs/zh-CN/vs-code) 聊天面板和[桌面应用](/docs/zh-CN/desktop)不打开它；通过编辑设置文件或通过这些应用自己的设置在那里更改设置。
</Note>

<h3 id="edit-a-settings-file">
  编辑设置文件
</h3>

在您的编辑器中打开您想要的作用域的设置文件并添加或更改键。设置文件是严格的 JSON：`//` 注释或尾部逗号是语法错误，Claude Code 在下次启动时将文件报告为[设置错误](#fix-a-broken-settings-file)。例如，要让 Claude Code 在不询问的情况下运行您的 lint 和测试命令并阻止它读取 `.env` 文件，将此添加到 `~/.claude/settings.json`：

```json ~/.claude/settings.json theme={null}
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)"
    ]
  }
}
```

`permissions` 下的每个条目是一个命名工具及其可能做什么的规则；[配置权限](/docs/zh-CN/permissions)解释语法。`$schema` 行指向 Claude Code 设置的[已发布 JSON 架构](https://json.schemastore.org/claude-code-settings.json)，它在 VS Code、Cursor 和任何其他支持 JSON 架构的编辑器中为您提供自动完成和内联验证。架构可能滞后于最新的 CLI 版本，因此最近记录的键上的验证警告并不意味着您的配置无效。

保存后，在 Claude Code 内运行 `/status` 以确认文件已加载；[确认已加载的内容](#check-what-loaded)说明 `Setting sources` 行显示什么以及如何报告损坏的文件。

有关完整的个人文件、团队文件和组织文件，每个都带有每个键的注释，请参阅[示例设置文件](/docs/zh-CN/settings-example)。

<span id="pass-settings-for-one-session" />

<h3 id="change-a-setting-for-one-session">
  为一个会话更改设置
</h3>

要尝试一个值而不保存它，在启动 Claude Code 时设置它。该值适用于该会话，您的设置文件保持原样。您有三种方式做到：

* **`--settings`**：将键作为 JSON 传递，内联或作为文件路径。Claude Code 在您的用户、项目和本地文件上方以及托管设置下方应用它。它可以设置您的用户设置文件可以设置的任何键；它不能设置 `Managed` 或 `Global config` 键。
* **该键的标志**：某些键有自己的标志，如 `--model` 用于 `model` 和 `--effort` 用于 `effortLevel` 和 `modelSettings`。
* **环境变量**：在运行 `claude` 之前导出键的配对变量，如 `ANTHROPIC_MODEL` 用于 `model`。

每个键在[设置参考](/docs/zh-CN/settings-reference)上的条目列出其每个会话覆盖以及哪个优先，因此检查您想更改的键的条目。

您在会话内运行的命令大多保存您的选择：当您在 `/config` 中更改设置时，Claude Code 将其写入您的设置文件，`/model` 将值保存为您新会话的默认值。

如果您在 `/model` 选择器中按 `s`，Claude Code 切换模型而不将其保存为您的用户默认值。[调整努力级别](/docs/zh-CN/model-config#adjust-effort-level)说明哪些 `/effort` 选择 Claude Code 保存为您使用的模型的默认值，哪些仅适用于当前会话。

例如，要在 Opus 上启动一个会话而不更改您的默认值：

```bash theme={null}
claude --settings '{"model": "claude-opus-5-5"}'
```

<h3 id="when-edits-take-effect">
  编辑何时生效
</h3>

Claude Code 监视您的设置文件并在它们更改时重新加载它们，因此它在运行的会话中应用大多数编辑而不需要重启，包括对 `permissions`、`hooks` 和凭证助手（如 `apiKeyHelper`）的编辑。Claude Code 也在会话中期加载您创建的设置文件，如果其文件夹在会话启动时存在。对于项目的 `.claude/` 文件夹，即使您在同一会话中创建文件夹，它也加载文件。

重新加载涵盖用户、项目、本地和托管设置，Claude Code 为每个它检测到的设置文件更改运行 [`ConfigChange` hook](/docs/zh-CN/hooks#configchange)，而不是来自 MDM 或 claude.ai 控制台的托管设置。来自 MDM 或 claude.ai 控制台的托管设置按计划而不是保存时到达运行的会话；[传递表](/docs/zh-CN/managed-settings#choose-a-delivery-mechanism)给出每个来源的。

Claude Code 仅在会话启动时读取某些键一次，因此对其中一个的编辑不会到达运行的会话。也等待重启的管理员端键，如 `requiredMinimumVersion`，在[策略适用的位置和时间](/docs/zh-CN/managed-settings#where-and-when-a-policy-applies)下列出。您最可能在会话中期编辑的：

* [`model`](/docs/zh-CN/settings-reference#model)：使用 [`/model`](/docs/zh-CN/model-config#setting-your-model) 在会话中期切换。每个模型有自己的提示缓存，因此切换后的第一个请求重新读取整个对话未缓存；请参阅[切换模型](/docs/zh-CN/prompt-caching#switching-models)
* [`effortLevel`](/docs/zh-CN/settings-reference#effortlevel) 和 [`modelSettings`](/docs/zh-CN/settings-reference#modelsettings)：使用 [`/effort`](/docs/zh-CN/model-config#adjust-effort-level) 在会话中期更改努力

<span id="verify-active-settings" />

<span id="check-what-loaded" />

<h3 id="confirm-what-loaded">
  确认已加载的内容
</h3>

在 Claude Code 内运行 `/status` 以查看哪些设置来源处于活跃状态。**状态**选项卡包含一个 `Setting sources` 行，列出 Claude Code 为当前会话加载的每个设置文件，如 `User settings` 或 `Project local settings`。当[托管设置](/docs/zh-CN/admin-setup#decide-how-settings-reach-devices)生效时，托管设置条目在括号中显示它们如何到达您的机器。

该行确认 Claude Code 读取了哪些文件；它不显示哪个文件提供了每个键。要列出 Claude Code 拒绝的条目，运行 [`claude doctor`](/docs/zh-CN/debug-your-config)；对于项目或托管设置设置的模型，启动标头命名设置它的文件。`/status` 和 `/config` 在不同选项卡上打开相同的对话框，**配置**选项卡不是您的 `settings.json` 内容的视图。

<h3 id="fix-a-broken-settings-file">
  修复损坏的设置文件
</h3>

如果您拼错 JSON 或将键设置为 Claude Code 不接受的值，Claude Code 在交互式会话启动时告诉您。它显示的内容取决于文件受影响的程度：

* **设置错误**：用户、项目或本地文件有无效的 JSON 或架构拒绝的值。在交互式会话启动时，Claude Code 显示一个对话框，让您在 Claude 的帮助下修复文件、退出，或在不加载这些损坏设置的情况下继续。
* **设置警告**：仅单个条目失败，如格式错误的权限规则或未知的 hook 事件名称。Claude Code 跳过这些值并保持文件的其余部分生效。
* **托管设置**：Claude Code 继续强制执行文件的其余部分。[托管设置中的无效条目](/docs/zh-CN/managed-settings#invalid-entries-in-managed-settings)说明它删除什么以及哪些键回退到更严格的值，直到您修复它们。对于不是有效 JSON 的托管设置文档，请参阅[托管设置文档无法解析](/docs/zh-CN/errors#managed-settings-document-could-not-be-parsed)。
* **配置错误**：`~/.claude.json` 无法解析。Claude Code 将损坏的文件复制到 `~/.claude/backups/.claude.json.corrupted.<timestamp>` 并询问是否退出并手动修复它或重置为默认配置；`-p` 运行打印错误并退出。要恢复您之前的状态，复制回 `~/.claude/backups/` 中最近五个 `.claude.json.backup.<timestamp>` 文件之一，Claude Code 在写入文件前保存。

在您继续后，运行 `/status` 以查看受影响的文件，`claude doctor` 以查看每个错误的详情。

`-p` 运行显示无对话框。除非[托管设置文档无法解析](/docs/zh-CN/errors#managed-settings-document-could-not-be-parsed)，Claude Code 跳过损坏的文件或值并继续其余的，因此在忽略设置的 `-p` 运行后，运行 `claude doctor` 以查看它删除了什么。

<span id="how-scopes-interact" />

<span id="key-points-about-the-configuration-system" />

<span id="which-value-claude-code-uses" />

<span id="which-value-wins" />

<h2 id="settings-precedence">
  设置优先级
</h2>

当同一键出现在多个位置时，Claude Code 使用设置它的最高级别的值。下面的堆栈显示级别，最高在顶部；更高级别的键覆盖它在下面任何地方的相同键。

<SettingsPrecedence />

按顺序，最高优先级优先：

1. **托管设置**：您的组织部署的设置，通过 `managed-settings.json` 文件、MDM 策略或来自 claude.ai 控制台的[服务器管理设置](/docs/zh-CN/server-managed-settings)。您设置的任何内容都不会覆盖它们：您使用 `--settings` 传递的键不会覆盖相同的托管键，`--model` 等标志仅从您的组织允许的模型中选择。托管 `model` 设置每个会话启动的模型，您仍然可以使用 `/model` 切换；锁定是 [`availableModels`](/docs/zh-CN/settings-reference#availablemodels)，它限制 `/model`、`--model` 和您自己文件中的 `model` 键。当您的组织传递多个托管来源时，[托管层内的优先级](/docs/zh-CN/managed-settings#precedence-within-the-managed-tier)的规则说 Claude Code 从每个读取什么。
2. **命令行参数**：您在从终端启动 `claude` 时传递的标志，用于一个会话；请参阅[为一个会话更改设置](#change-a-setting-for-one-session)。Claude Code 使用与其他级别相同的规则将您使用 `--settings <file-or-json>` 传递的 JSON 与您的设置文件合并：它在此处设置的键优先于本地、项目或用户设置中的相同键，省略的键保持较低级别的值。
3. **项目本地设置** (`.claude/settings.local.json`)：您对此项目的个人设置。
4. **共享项目设置** (`.claude/settings.json`)：您的团队检入源代码管理的设置。
5. **用户设置** (`~/.claude/settings.json`)：您对每个项目的个人设置。

环境变量不是此堆栈中的级别。当行为同时有 shell 变量和设置键时，哪个适用是按对决定的，而不是按级别：在您的 shell 中导出的 `ANTHROPIC_MODEL` 适用于任何文件中的 `model` 键，而 `ANTHROPIC_DEFAULT_MODEL` 仅当没有文件设置 `model` 时适用。[环境变量参考](/docs/zh-CN/env-vars#precedence)说哪些键有对以及 Claude Code 首先读取哪个。设置文件内的 `env` 块是普通键并遵循上面的级别。

对于少数安全敏感的键，Claude Code 尊重来自较低级别的更严格值而不是托管值；[托管设置优先级的例外](#exceptions-to-managed-settings-precedence)列出它们。

<h3 id="lists-merge-instead-of-overriding">
  列表合并而不是覆盖
</h3>

当您在多个文件中设置相同的列表键（如 `permissions.allow`）时，Claude Code 组合列表而不是选择一个，因此每个文件可以添加条目而不删除另一个文件的。四个保存模型列表或每个模型条目的键遵循自己的规则：

* [`fallbackModel`](/docs/zh-CN/settings-reference#fallbackmodel) 是一个有序链，其中位置具有意义，因此 Claude Code 从定义它的最高优先级文件获取整个值。
* [`modelPicker`](/docs/zh-CN/settings-reference#modelpicker) 保存一个有序的行列表加上替换标志，因此 Claude Code 永远不会合并来自两个来源的行。它从托管设置、`--settings` 和用户设置中定义它的最高获取整个值，并忽略项目和本地设置中的键。需要 Claude Code v2.1.242 或更高版本。
* [`availableModels`](/docs/zh-CN/settings-reference#availablemodels)：当 Claude Code 应用的托管设置定义它时，Claude Code 按原样应用该列表并忽略您在用户、项目或本地设置中添加的条目，除非嵌入 Claude Code 的应用提供自己的模型列表；请参阅[托管设置优先级的例外](#exceptions-to-managed-settings-precedence)。跨托管来源列表也永远不会合并；[Claude Code 如何组合托管来源](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)说哪个来源的列表适用。跨非托管作用域 Claude Code 照常合并数组。
* [`modelSettings`](/docs/zh-CN/settings-reference#modelsettings)：Claude Code 一次解决它一个模型，与 [`effortLevel`](/docs/zh-CN/settings-reference#effortlevel) 一起。`modelSettings` 条目说明哪个文件的值适用于模型。

<span id="examples" />

<h3 id="precedence-examples">
  优先级示例
</h3>

当 Claude 工作时，Claude Code 在微调器下显示一行提示，如"使用 /config 更改您的默认权限模式（包括 Plan Mode）"。假设您想关闭这些提示，因此您在 `~/.claude/settings.json` 中将 [`spinnerTipsEnabled`](/docs/zh-CN/settings-reference#spinnertipsenabled) 设置为 `false`。下面的每个场景是可以打开它们的东西，以及您可以做什么。

<h4 id="team-settings-override-personal-settings">
  团队设置覆盖个人设置
</h4>

您的团队的 `.claude/settings.json` 将其设置为 `true`。Claude Code 使用项目值，因为共享项目位于用户上方，因此您在该项目中看到提示，其他地方都没有。

您可以恢复您的值：在该项目中的 `.claude/settings.local.json` 中添加 `"spinnerTipsEnabled": false`。项目本地位于共享项目上方，因此您的会话停止显示提示，您队友的会话不改变。

<h4 id="organization-settings-override-everything">
  组织设置覆盖一切
</h4>

您的组织的托管设置将其设置为 `true`。您在用户、项目或本地设置中放入的任何内容都不会关闭提示，`--settings` 也不会。托管是最高级别。

您无法恢复您的值。运行 `/status` 以查看哪个托管来源适用，并询问您的管理员策略是否应改变。

<h4 id="the-command-line-overrides-your-files-for-one-session">
  命令行为一个会话覆盖您的文件
</h4>

您使用 `claude --settings '{"spinnerTipsEnabled": true}'` 启动了会话。命令行位于除托管外的每个文件上方，因此该会话显示提示，即使您的文件说 `false`。

您在下一个会话上恢复您的值；`--settings` 持续一个会话并不写入任何文件。

<h4 id="a-flag-or-environment-variable-sets-the-same-thing">
  标志或环境变量设置相同的东西
</h4>

某些键有命令行标志或环境变量，无论哪个文件设置它都覆盖设置值：`ANTHROPIC_MODEL` 覆盖 [`model`](/docs/zh-CN/settings-reference#model) 设置，`--model` 为一个会话覆盖两者。

您是否可以恢复您的值取决于键：取消设置变量或删除标志，并检查[设置参考](/docs/zh-CN/settings-reference)上的键条目和[环境变量参考](/docs/zh-CN/env-vars)上的变量行，了解 Claude Code 使用哪个。

<span id="keys-ignored-in-a-repository-file" />

<span id="keys-only-you-or-your-organization-can-set" />

<span id="common-cases" />

<span id="which-value-applies-in-common-situations" />

<h3 id="troubleshoot-a-setting-that-doesn’t-apply">
  排除不适用的设置
</h3>

当您设置键而 Claude Code 不表现得好像您有时，从 `/status` 开始以查看它加载了哪些文件，然后在下面找到您的症状。[调试您的配置](/docs/zh-CN/debug-your-config)涵盖更广泛的检查，包括干净配置测试。

<h4 id="a-value-you-set-is-ignored">
  您设置的值被忽略
</h4>

其他东西设置相同的键，文件无法设置该值，或文件没有加载：

* **更高级别设置它。** 另一个设置文件、`--settings` 标志或托管来源在您的上方设置键；[堆栈](#settings-precedence)说哪个。标志或环境变量也可以自己覆盖键，按键决定；[设置参考](/docs/zh-CN/settings-reference)上的键条目说 Claude Code 使用哪个，[`env` 条目](/docs/zh-CN/settings-reference#env)涵盖托管 `env` 值与 shell 导出。
* **安全键保持其严格值。** 对于少数几个键 Claude Code 尊重任何文件的限制值，因此项目 `true` 用于 [`disableClaudeAiConnectors`](/docs/zh-CN/settings-reference#disableclaudeaiconnectors) 保持开启；请参阅[托管设置优先级的例外](#exceptions-to-managed-settings-precedence)。
* **文件无法设置该值。** [`permissions.defaultMode`](/docs/zh-CN/settings-reference#permissions-defaultmode) 值 `auto` 和 `bypassPermissions` 不从项目或本地设置生效；改为在用户或托管设置中设置它们，或为一个会话传递 `--permission-mode`。在 v2.1.257 之前，`bypassPermissions` 从任何文件生效。

  [`env`](/docs/zh-CN/settings-reference#env) 块中的遥测导出变量也不从项目或本地设置生效，除了少数关闭值。[Claude Code 在 `env` 中忽略的变量](/docs/zh-CN/settings-reference#variables-claude-code-ignores-in-env)列出变量和这些值。
* **文件损坏。** 无效的 JSON 或拒绝的值使 Claude Code 跳过文件或条目；请参阅[修复损坏的设置文件](#fix-a-broken-settings-file)。

<h4 id="a-change-you-made-in-claude-code-is-lost-in-new-sessions">
  您在 Claude Code 中所做的更改在新会话中丢失
</h4>

当您从 Claude Code 内保存新会话的选择时，如使用 `/model` 的默认模型，Claude Code 将其写入您的用户设置文件 `~/.claude/settings.json`。如果您无法写入该文件，例如因为另一个工具生成它或将其链接到只读副本，更改适用于当前会话并在下一个会话中消失。在生成文件的工具中设置键，或用您可以写入的文件替换文件。

如果您可以写入文件而更改仍然不持续，检查更改是否[仅用于一个会话](#change-a-setting-for-one-session)或[更高级别设置相同的键](#a-value-you-set-is-ignored)。对于 `model` 键，[新会话在与您选择的不同的模型上启动](/docs/zh-CN/model-config#a-new-session-starts-on-a-different-model-than-you-picked)列出更多原因。

<h4 id="a-managed-change-hasn’t-reached-you">
  托管更改还没有到达您
</h4>

托管来源按[传递表](/docs/zh-CN/managed-settings#choose-a-delivery-mechanism)中的计划到达运行的会话，因此首先重启会话。如果 `/status` 然后命名与您的管理员更改的不同的来源，更高优先级的来源适用；[Claude Code 如何组合托管来源](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)给出顺序。

<h4 id="a-committed-key-doesn’t-reach-teammates">
  提交的键不到达队友
</h4>

两件事阻止 `.claude/settings.json` 中的键为克隆它的每个人应用：

* **Claude Code 忽略存储库文件中的键。** 在[设置索引](/docs/zh-CN/settings-reference#settings-index)的作用域列中查找 `User, local, or managed`、`User or managed`、`Managed` 或 `Global config`。这些键永远不会从共享文件应用，除了少数几个存储库文件仍然可以关闭的。每个这些条目在其作用域行上说明。`Global config` 键仅从 `~/.claude.json` 应用。

  在 `env` 键内，遥测导出变量也永远不会从共享文件应用，除了少数关闭值；请参阅[Claude Code 在 `env` 中忽略的变量](/docs/zh-CN/settings-reference#variables-claude-code-ignores-in-env)。
* **键等待信任。** `permissions.allow` 规则、`permissions.additionalDirectories`、`extraKnownMarketplaces` 和大多数 [`env`](/docs/zh-CN/settings-reference#env) 值仅在每个队友[信任文件夹](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)后应用。在那之前他们仍然看到提示并不从文件声明的市场获得插件。`deny` 和 `ask` 规则立即应用。

<h4 id="permission-rules-combine-differently-than-you-expected">
  权限规则组合方式与您预期不同
</h4>

* **您在权限提示上选择了"是的，不要再问"但仍然为相同的工具获得提示。** 该选择将 `allow` 规则保存到您的本地文件，本地的 `allow` 规则不优先于项目或托管文件中的 `ask` 规则；[权限规则如何组合](/docs/zh-CN/permissions#settings-precedence)解释顺序。在 VS Code 扩展中，批准卡让您选择目标文件，包括项目的共享文件，这改变了每个人的规则；在 CLI 中，Claude Code 仅写入您的本地文件。
* **您的组织的允许规则仍然与您的一起应用。** 这是预期的：Claude Code 跨作用域合并 [`permissions.allow`](/docs/zh-CN/settings-reference#permissions-allow)，除非您的组织设置 [`allowManagedPermissionRulesOnly`](/docs/zh-CN/settings-reference#allowmanagedpermissionrulesonly)。

<span id="security-keys-where-the-stricter-value-applies" />

<h3 id="exceptions-to-managed-settings-precedence">
  托管设置优先级的例外
</h3>

对于少数几个值限制会话的键，Claude Code 尊重来自否则无法覆盖托管设置的作用域的限制值。在此表中找到键以查看它尊重哪个值以及从哪里。

| 键 | Claude Code 尊重的值 | 注释 |
| :- | :- | :- |
| [`disableClaudeAiConnectors`](/docs/zh-CN/settings-reference#disableclaudeaiconnectors) | 来自任何作用域的 `true` | 即使托管来源设置 `false` 也被尊重 |
| [`enableArtifact`](/docs/zh-CN/settings-reference#enableartifact) | 来自任何作用域的 `false`，以及来自任何作用域的 `disableArtifact: true` | 即使托管来源设置 `true` 也被尊重；没有什么打开[Artifact 工具](/docs/zh-CN/artifacts#disable-artifacts)。需要 Claude Code v2.1.242 或更高版本 |
| [`isolatePeerMachines`](/docs/zh-CN/settings-reference#isolatepeermachines) | 来自任何作用域的 `true` | 即使托管来源设置 `false` 也被尊重 |
| [`remoteControlAtStartup`](/docs/zh-CN/settings-reference#remotecontrolatstartup) | 来自 `.claude/settings.json` 或 `.claude/settings.local.json` 的 `false` | 即使托管来源设置 `true` 也被尊重；项目或本地 `true` 被忽略 |
| [`crossSessionInbound`](/docs/zh-CN/settings-reference#crosssessioninbound) | 来自 `.claude/settings.json` 或 `.claude/settings.local.json` 的更严格值，在 `accept` \< `hold` \< `refuse` 梯形上 | 在托管、`--settings` 和用户值上被尊重；不是更严格的项目或本地值被忽略 |
| [`useAutoModeDuringPlan`](/docs/zh-CN/settings-reference#useautomodeduringplan) | 来自任何托管来源、`--settings`、`~/.claude/settings.json` 或 `.claude/settings.local.json` 的 `false` | 即使获胜的托管来源设置 `true` 也被尊重；`.claude/settings.json` 中的 `false` 被忽略 |
| [`syncClaudeAiSkills`](/docs/zh-CN/settings-reference#syncclaudeaiskills) | 来自任何托管来源、`--settings`、`~/.claude/settings.json` 或 `.claude/settings.local.json` 的 `false` | 即使获胜的托管来源设置 `true` 也被尊重；`.claude/settings.json` 中的 `false` 被忽略 |
| [`syncClaudeAiPlugins`](/docs/zh-CN/settings-reference#syncclaudeaiplugins) | 来自任何托管来源、`--settings`、`~/.claude/settings.json` 或 `.claude/settings.local.json` 的 `false` | 即使获胜的托管来源设置 `true` 也被尊重；`.claude/settings.json` 中的 `false` 被忽略 |
| [`maxEffortLevel`](/docs/zh-CN/settings-reference#maxeffortlevel) | 来自任何作用域（包括 `--settings`）的较低上限 | 即使 Claude Code 应用的托管设置设置更高的上限也被尊重；最低的上限适用。需要 Claude Code v2.1.267 或更高版本 |

运行 Claude Code 的应用并设置 [`CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST`](/docs/zh-CN/env-vars) 也是例外。Claude Code 从该应用的模型配置优先于来自每个托管来源的 `model`、`fallbackModel`、`modelPicker` 和 `modelOverrides` 键，以及托管 `env` 块中的模型选择变量，如 `ANTHROPIC_MODEL` 和 `ANTHROPIC_DEFAULT_*_MODEL` 系列。Claude Code 保持托管 [`availableModels`](/docs/zh-CN/settings-reference#availablemodels) 允许列表生效，除非应用提供自己的。

<h2 id="settings-in-cloud-sessions">
  云会话中的设置
</h2>

[云会话](/docs/zh-CN/claude-code-on-the-web)在[云环境](/docs/zh-CN/cloud-environments)中运行在您的存储库的新克隆上，而不是在您的机器上。这改变了哪些设置到达它：

* **共享项目设置** (`.claude/settings.json`)：在一个存储库的会话中读取，因为该文件是克隆的一部分，会话在其中启动。在那里提交设置以在这些会话中应用它。具有多个存储库的会话在克隆上方启动，因此从每个存储库的 `.claude/settings.json` 仅读取 `enabledPlugins` 和 `extraKnownMarketplaces` 键，而不是权限规则、hooks、`env` 或其他键。这些两个键声明的市场和插件仍然[不在云会话中加载](/docs/zh-CN/cloud-environments#what-carries-over-from-your-setup)。
* **用户和项目本地设置** (`~/.claude/settings.json` 和 `.claude/settings.local.json`)：不读取。两者都保持在您的机器上，本地文件不在克隆中。
* **托管设置**：您设备上的 `managed-settings.json` 文件或 MDM 配置文件不会到达云会话。您组织的[服务器管理设置](/docs/zh-CN/server-managed-settings)会；[表面覆盖](/docs/zh-CN/model-config#surface-coverage)列出哪些云会话接收它们。[自托管环境](/docs/zh-CN/self-hosted-environments)也读取其运行器镜像中的托管设置文件。[Claude Code 如何组合托管来源](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)说该文件何时适用。
* **`/config`**：在您的浏览器中的 claude.ai/code，打开您的 claude.ai 设置的 Claude Code 部分而不是更改值。要为云会话更改设置，在环境上设置[环境变量](/docs/zh-CN/cloud-environments#set-environment-variables)，或在具有一个存储库的会话中，将键提交到该存储库的 `.claude/settings.json`。

[从您的设置中携带什么](/docs/zh-CN/cloud-environments#what-carries-over-from-your-setup)列出其余的：`CLAUDE.md`、skills、MCP 服务器、plugins 和凭证。

<h2 id="what’s-next">
  接下来是什么
</h2>

* [所有设置](/docs/zh-CN/settings-reference)：每个键，以及您在哪里设置它和示例
* [示例设置文件](/docs/zh-CN/settings-example)：个人文件、团队文件和组织的托管文件
* [配置权限](/docs/zh-CN/permissions)：允许、询问和拒绝规则，以及 Claude Code 在不询问的情况下运行什么
* [环境变量](/docs/zh-CN/env-vars)：Claude Code 读取的变量和 `env` 块
* [调试您的配置](/docs/zh-CN/debug-your-config)：当设置不适用时
* [Claude 目录参考](/docs/zh-CN/claude-directory)：Claude Code 读取的每个文件，包括 subagents、MCP 服务器、插件和 `CLAUDE.md`
