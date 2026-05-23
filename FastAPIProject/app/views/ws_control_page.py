from __future__ import annotations


def render_ws_control_page() -> str:
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hfood 控制台</title>
    <style>
        :root {
            --bg: #f4f7fb;
            --card: #ffffff;
            --line: #d8e1ee;
            --text: #18263b;
            --muted: #64748b;
            --primary: #2155d6;
            --primary-soft: #eef3ff;
            --success: #138a52;
            --success-soft: #e9f8f0;
            --warn: #b56a11;
            --warn-soft: #fff3e4;
            --danger: #d92d20;
            --danger-soft: #fff0ee;
            --shadow: 0 16px 40px rgba(24, 38, 59, 0.08);
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            padding: 16px;
            font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
            color: var(--text);
            background:
                radial-gradient(circle at top left, rgba(33, 85, 214, 0.10), transparent 28%),
                radial-gradient(circle at top right, rgba(19, 138, 82, 0.10), transparent 22%),
                linear-gradient(160deg, #f8fbff 0%, var(--bg) 100%);
        }

        .shell {
            max-width: 1380px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .main-layout {
            display: grid;
            grid-template-columns: 320px 1fr;
            gap: 16px;
            align-items: start;
        }

        .extensions-grid {
            display: flex;
            flex-direction: column;
            gap: 14px;
        }

        .domain-block {
            display: flex;
            flex-direction: column;
            gap: 14px;
        }

        .domain-header {
            padding: 14px 18px;
            border-radius: 18px;
            background: linear-gradient(135deg, #ffffff 0%, #f7fbff 100%);
            border: 1px solid #dce7f4;
            box-shadow: var(--shadow);
        }

        .domain-kicker {
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.08em;
            color: var(--primary);
        }

        .domain-title {
            margin: 6px 0 0;
            font-size: 21px;
            line-height: 1.2;
        }

        .domain-desc {
            margin: 6px 0 0;
            color: var(--muted);
            font-size: 13px;
            line-height: 1.7;
        }

        .domain-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 12px;
        }

        .card {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 18px;
            box-shadow: var(--shadow);
        }

        .hero {
            padding: 18px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            width: fit-content;
            padding: 8px 12px;
            border-radius: 999px;
            background: var(--primary-soft);
            color: var(--primary);
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.08em;
        }

        .eyebrow::before {
            content: "";
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--primary);
        }

        h1 {
            margin: 0;
            font-size: 30px;
            line-height: 1.1;
        }

        .subtitle {
            margin: 0;
            color: var(--muted);
            line-height: 1.7;
            font-size: 14px;
            max-width: 780px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 10px;
        }

        .mini-card {
            padding: 14px;
            border-radius: 14px;
            background: #f8fbff;
            border: 1px solid #e6edf8;
        }

        .mini-label {
            font-size: 13px;
            color: var(--muted);
        }

        .mini-value {
            margin-top: 8px;
            font-size: 24px;
            font-weight: 800;
            line-height: 1.1;
        }

        .mini-hint {
            margin-top: 10px;
            font-size: 12px;
            color: var(--muted);
            line-height: 1.6;
        }

        .panel {
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .compact-panel {
            padding: 14px;
            gap: 8px;
        }

        .section-title {
            margin: 0;
            font-size: 17px;
        }

        .section-desc {
            margin: 6px 0 0;
            color: var(--muted);
            font-size: 13px;
            line-height: 1.7;
        }

        .status-box,
        .mode-box,
        .bubble-box,
        .action-box,
        .log-box {
            border: 1px solid #e7edf6;
            border-radius: 14px;
            padding: 12px;
            background: #fbfdff;
        }

        .compact-box {
            padding: 8px;
            border-radius: 10px;
        }

        .status-pill,
        .mode-pill {
            display: inline-flex;
            align-items: center;
            padding: 8px 12px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
        }

        .status-pill.online {
            background: var(--success-soft);
            color: var(--success);
        }

        .status-pill.offline {
            background: var(--danger-soft);
            color: var(--danger);
        }

        .mode-pill.mode1 {
            background: var(--primary-soft);
            color: var(--primary);
        }

        .mode-pill.mode2 {
            background: var(--warn-soft);
            color: var(--warn);
        }

        .mode-pill.mode3 {
            background: var(--success-soft);
            color: var(--success);
        }

        .mode-pill.empty {
            background: var(--danger-soft);
            color: var(--danger);
        }

        .mode-pill.direct {
            background: var(--primary-soft);
            color: var(--primary);
        }

        .mode-pill.repair {
            background: var(--success-soft);
            color: var(--success);
        }

        .mode-pill.normal {
            background: var(--primary-soft);
            color: var(--primary);
        }

        .mode-pill.jitter {
            background: var(--warn-soft);
            color: var(--warn);
        }

        .mode-pill.unknown {
            background: #eef2f7;
            color: #526075;
        }

        .row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
        }

        .action-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 8px;
            margin-top: 8px;
        }

        .input-label {
            display: block;
            font-size: 13px;
            color: var(--muted);
            margin-bottom: 8px;
        }

        .bubble-input,
        .quick-select {
            width: 100%;
            border: 1px solid #d5deeb;
            background: #fff;
            border-radius: 12px;
            padding: 10px 12px;
            font-size: 13px;
            color: var(--text);
            outline: none;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        .bubble-input:focus,
        .quick-select:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(33, 85, 214, 0.12);
        }

        .quick-command-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 8px;
        }

        .quick-command-btn,
        button {
            border: none;
            cursor: pointer;
            border-radius: 12px;
            padding: 10px 12px;
            font-size: 13px;
            transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
        }

        button {
            background: #eef3fa;
            color: var(--text);
            font-weight: 600;
        }

        button.primary {
            background: var(--primary);
            color: #fff;
        }

        button:hover:not(:disabled),
        .quick-command-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 20px rgba(24, 38, 59, 0.10);
        }

        button:disabled {
            opacity: 0.55;
            cursor: not-allowed;
            box-shadow: none;
            transform: none;
        }

        .quick-command-btn {
            background: #f4f7fb;
            color: var(--text);
        }

        .quick-command-btn.active,
        .active-mode {
            background: var(--primary-soft);
            color: var(--primary);
        }

        .stage-btn-active {
            background: var(--primary) !important;
            color: #fff !important;
            box-shadow: 0 10px 24px rgba(33, 85, 214, 0.20);
        }

        .mode-actions {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 8px;
        }

        .log-body {
            margin: 0;
            min-height: 220px;
            max-height: 360px;
            overflow: auto;
            white-space: pre-wrap;
            word-break: break-word;
            font-family: "Consolas", "JetBrains Mono", monospace;
            font-size: 13px;
            line-height: 1.7;
            color: #12304f;
        }

        .status-meta {
            margin-top: 12px;
            display: grid;
            gap: 10px;
            font-size: 14px;
            color: var(--muted);
        }

        .status-meta strong {
            color: var(--text);
        }

        @media (max-width: 1080px) {
            body {
                padding: 18px;
            }

            .main-layout {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
<main class="shell">
    <section class="card hero">
        <span class="eyebrow">HFOOD CONTROL</span>
        <div>
            <h1>Harmony 控制面板</h1>
            <p class="subtitle">
                这个页面负责检查鸿蒙应用 WebSocket 是否在线、切换运行模式、发送语音，
                并把控制项按嵌入式软件、计算机视觉、AI 智能体三大区域进行集中展示。
            </p>
        </div>
        <div class="grid">
            <div class="mini-card">
                <div class="mini-label">设备连接状态</div>
                <div class="mini-value" id="device-status-text">离线</div>
                <div class="mini-hint">已连接设备数会实时刷新。</div>
            </div>
            <div class="mini-card">
                <div class="mini-label">当前足压模式</div>
                <div class="mini-value" id="pressure-mode-label-large">模式 2</div>
                <div class="mini-hint" id="pressure-mode-description-large">等待后端返回足压模式说明。</div>
            </div>
            <div class="mini-card">
                <div class="mini-label">WebSocket 路径</div>
                <div class="mini-value" id="socket-path">/ws/harmony-app</div>
                <div class="mini-hint">鸿蒙端应用通过该路径接收控制消息。</div>
            </div>
        </div>
    </section>

    <div class="main-layout">
        <aside class="card panel">
            <section class="status-box">
                <div class="row">
                    <span class="status-pill offline" id="device-status-pill">暂无设备在线</span>
                </div>
                <div class="status-meta">
                    <div><strong>已连接设备数：</strong><span id="connected-count">0</span></div>
                    <div><strong>WebSocket 路径：</strong><span id="socket-path-side">/ws/harmony-app</span></div>
                </div>
            </section>
            <section class="action-box">
                <div class="action-grid">
                    <button type="button" id="test-btn">连接测试</button>
                    <button type="button" id="refresh-btn">刷新状态</button>
                    <button type="button" id="noop-btn" disabled>预留</button>
                </div>
            </section>

            <section class="log-box">
                <pre class="log-body" id="log-body">系统已就绪，等待操作...</pre>
            </section>
        </aside>

        <div class="extensions-grid">
            <section class="domain-block">
                <div class="domain-header">
                <div class="domain-kicker">DOMAIN 01</div>
                    <h2 class="domain-title">嵌入式软件</h2>
                    <p class="domain-desc">聚焦蓝牙双脚连接、真实落点直出、足压模式与重心轨迹合成显示。</p>
                </div>
                <div class="domain-grid">
                    <article class="card panel">
                        <div>
                            <h2 class="section-title">足压模式</h2>
                            <p class="section-desc">模式 2 为真实落点直出；蓝牙双脚连接后按当前实时效果直接点亮。</p>
                        </div>
                        <section class="mode-box">
                            <div class="row">
                                <span class="mode-pill direct" id="pressure-mode-pill">模式 2 直出</span>
                            </div>
                            <p class="section-desc" id="pressure-mode-description">蓝牙双脚连接后按真实落点直接点亮，对应当前实时直出效果。</p>
                            <div class="mode-actions">
                                <button type="button" id="pressure-mode-empty">模式 1 空白</button>
                                <button type="button" id="pressure-mode-direct" class="active-mode">模式 2 直出</button>
                                <button type="button" id="pressure-mode-repair">模式 3 修复</button>
                            </div>
                        </section>
                    </article>

                    <article class="card panel">
                        <div>
                            <h2 class="section-title">重心轨迹</h2>
                            <p class="section-desc">轨迹正常时按左右脚最新实时数据正常合成显示，不影响其他足压卡片。</p>
                        </div>
                        <section class="mode-box">
                            <div class="row">
                                <span class="mode-pill normal" id="trace-mode-pill">轨迹正常</span>
                            </div>
                            <p class="section-desc" id="trace-mode-description">重心轨迹按左右脚最新实时数据正常合成显示，不影响其他足压卡片。</p>
                            <div class="mode-actions">
                                <button type="button" id="trace-mode-normal" class="active-mode">轨迹正常</button>
                                <button type="button" id="trace-mode-jitter">轨迹波动</button>
                            </div>
                        </section>
                    </article>

                    <article class="card panel">
                        <div>
                            <h2 class="section-title">鸿蒙端 TTS</h2>
                            <p class="section-desc">本地 TTS 独立板块，直接调用设备侧播报能力。</p>
                        </div>
                        <section class="bubble-box">
                            <label class="input-label" for="local-tts-input">发送鸿蒙端 TTS 内容</label>
                            <input type="text" id="local-tts-input" class="bubble-input" placeholder="输入要让鸿蒙设备本地 TTS 播报的内容">
                            <div class="row" style="margin-top: 12px; flex-direction: column; align-items: stretch;">
                                <button type="button" class="primary" id="send-local-tts-btn" disabled>发送鸿蒙端 TTS</button>
                            </div>
                        </section>
                    </article>

                    <article class="card panel">
                        <div>
                            <h2 class="section-title">蓝牙在线语音</h2>
                            <p class="section-desc">蓝牙板块使用独立的在线语音接口与独立音频库目录，只保留蓝牙相关播报。</p>
                        </div>
                        <section class="bubble-box">
                            <label class="input-label" for="embedded-tts-input">发送蓝牙语音内容</label>
                            <input type="text" id="embedded-tts-input" class="bubble-input" placeholder="输入要让设备播报的蓝牙语音">
                            <div style="margin-top: 12px;">
                                <label class="input-label" for="embedded-library-select">蓝牙音频库</label>
                                <select id="embedded-library-select" class="quick-select">
                                    <option value="">选择一个蓝牙音频</option>
                                </select>
                            </div>
                            <div class="quick-command-grid" id="embedded-library-list"></div>
                            <div class="row" style="margin-top: 12px; flex-direction: column; align-items: stretch;">
                                <button type="button" class="primary" id="send-embedded-tts-btn" disabled>发送蓝牙在线语音</button>
                                <button type="button" id="add-embedded-library-btn" disabled>加入蓝牙语音库</button>
                            </div>
                            <div class="section-desc" id="embedded-cache-hint">发送后会先进入 cache，再可加入蓝牙语音库。</div>
                        </section>
                    </article>
                </div>
            </section>

            <section class="domain-block">
                <div class="domain-header">
                    <div class="domain-kicker">DOMAIN 02</div>
                    <h2 class="domain-title">计算机视觉</h2>
                    <p class="domain-desc">聚焦单目体态链路、模型驱动阶段切换、渲染状态播报与采集引导。</p>
                </div>
                <div class="domain-grid">
                    <article class="card panel compact-panel">
                        <div>
                            <h2 class="section-title">体态演示卡片</h2>
                            <p class="section-desc">体态实时演示控制。</p>
                        </div>
                        <section class="bubble-box compact-box">
                            <div class="quick-command-grid">
                                <button type="button" id="posture-ready-btn">默认</button>
                                <button type="button" id="posture-render-btn">渲染</button>
                                <button type="button" id="posture-step2-btn">阶段2</button>
                                <button type="button" id="posture-step3-btn">阶段3</button>
                                <button type="button" id="posture-step4-btn">阶段4</button>
                                <button type="button" id="posture-reload-btn">重载</button>
                            </div>
                        </section>
                    </article>

                    <article class="card panel">
                        <div>
                            <h2 class="section-title">计算机视觉在线语音</h2>
                            <p class="section-desc">只保留体态、采集、分析与渲染相关语音，不混入蓝牙播报。</p>
                        </div>
                        <section class="bubble-box">
                            <label class="input-label" for="cv-tts-input">发送计算机视觉语音内容</label>
                            <input type="text" id="cv-tts-input" class="bubble-input" placeholder="输入要让设备播报的计算机视觉语音">
                            <div style="margin-top: 12px;">
                                <label class="input-label" for="cv-library-select">计算机视觉音频库</label>
                                <select id="cv-library-select" class="quick-select">
                                    <option value="">选择一个计算机视觉音频</option>
                                </select>
                            </div>
                            <div class="quick-command-grid" id="cv-library-list"></div>
                            <div class="row" style="margin-top: 12px; flex-direction: column; align-items: stretch;">
                                <button type="button" class="primary" id="send-cv-tts-btn" disabled>发送计算机视觉在线语音</button>
                                <button type="button" id="add-cv-library-btn" disabled>加入计算机视觉语音库</button>
                            </div>
                            <div class="section-desc" id="cv-cache-hint">发送后会先进入 cache，再可加入计算机视觉语音库。</div>
                        </section>
                    </article>
                </div>
            </section>

            <section class="domain-block">
                <div class="domain-header">
                    <div class="domain-kicker">DOMAIN 03</div>
                    <h2 class="domain-title">AI 智能体</h2>
                    <p class="domain-desc">保留 AI 智能体独立在线语音链路，使用 ai_cache 与 ai_library。</p>
                </div>
                <div class="domain-grid">
                    <article class="card panel">
                        <div>
                            <h2 class="section-title">AI 分析样本</h2>
                            <p class="section-desc">默认是非正常样本；可切到正常样本查看标准流式分析过程。</p>
                        </div>
                        <section class="mode-box">
                            <div class="row">
                                <span class="mode-pill unknown" id="ai-mode-pill">非正常</span>
                            </div>
                            <p class="section-desc" id="ai-mode-description">当前默认展示的是非正常样本分析流式输出。</p>
                            <div class="mode-actions">
                                <button type="button" id="ai-mode-normal">正常</button>
                                <button type="button" id="ai-mode-abnormal" class="active-mode">非正常</button>
                            </div>
                        </section>
                    </article>
                    <article class="card panel">
                        <div>
                            <h2 class="section-title">AI 智能体在线语音</h2>
                            <p class="section-desc">AI 智能体板块使用独立在线语音接口与独立音频库目录。</p>
                        </div>
                        <section class="bubble-box">
                            <label class="input-label" for="ai-tts-input">发送 AI 智能体语音内容</label>
                            <input type="text" id="ai-tts-input" class="bubble-input" placeholder="输入要让设备播报的 AI 智能体语音">
                            <div style="margin-top: 12px;">
                                <label class="input-label" for="ai-library-select">AI 智能体音频库</label>
                                <select id="ai-library-select" class="quick-select">
                                    <option value="">选择一个 AI 智能体音频</option>
                                </select>
                            </div>
                            <div class="quick-command-grid" id="ai-library-list"></div>
                            <div class="row" style="margin-top: 12px; flex-direction: column; align-items: stretch;">
                                <button type="button" class="primary" id="send-ai-tts-btn" disabled>发送 AI 智能体在线语音</button>
                                <button type="button" id="add-ai-library-btn" disabled>加入 AI 智能体语音库</button>
                            </div>
                            <div class="section-desc" id="ai-cache-hint">发送后会先进入 cache，再可加入 AI 智能体语音库。</div>
                        </section>
                    </article>
                    <article class="card panel">
                        <div>
                            <h2 class="section-title">AI 陪练动作</h2>
                            <p class="section-desc">点击后会同步切换前端 AI 陪练右侧视频，并播放对应语音。</p>
                        </div>
                        <section class="action-box">
                            <div class="action-grid" style="grid-template-columns: repeat(2, minmax(0, 1fr));">
                                <button type="button" id="ai-coach-speech1-btn">讲话1</button>
                                <button type="button" id="ai-coach-speech2-btn">讲话2</button>
                                <button type="button" id="ai-coach-speech3-btn">讲话3</button>
                                <button type="button" class="primary" id="ai-coach-encourage-btn">鼓励</button>
                            </div>
                            <div class="section-desc" style="margin-top: 10px;">
                                讲话按钮会切到桌面 `讲话.mp4` 并播放对应 `mp3`，鼓励会切到 `鼓励.mp4` 播放一次后自动回到 `常态待机.mp4`。
                            </div>
                        </section>
                    </article>
                </div>
            </section>
        </div>
    </div>
</main>

<script>
    const deviceStatusTextEl = document.getElementById('device-status-text');
    const deviceStatusPillEl = document.getElementById('device-status-pill');
    const connectedCountEl = document.getElementById('connected-count');
    const socketPathEl = document.getElementById('socket-path');
    const socketPathSideEl = document.getElementById('socket-path-side');
    const pressureModeLabelLargeEl = document.getElementById('pressure-mode-label-large');
    const pressureModeDescriptionLargeEl = document.getElementById('pressure-mode-description-large');
    const pressureModePillEl = document.getElementById('pressure-mode-pill');
    const pressureModeDescriptionEl = document.getElementById('pressure-mode-description');
    const traceModePillEl = document.getElementById('trace-mode-pill');
    const traceModeDescriptionEl = document.getElementById('trace-mode-description');
    const localTtsInputEl = document.getElementById('local-tts-input');
    const sendLocalTtsBtn = document.getElementById('send-local-tts-btn');
    const embeddedTtsInputEl = document.getElementById('embedded-tts-input');
    const sendEmbeddedTtsBtn = document.getElementById('send-embedded-tts-btn');
    const addEmbeddedLibraryBtn = document.getElementById('add-embedded-library-btn');
    const embeddedCacheHintEl = document.getElementById('embedded-cache-hint');
    const embeddedLibrarySelectEl = document.getElementById('embedded-library-select');
    const embeddedLibraryListEl = document.getElementById('embedded-library-list');
    const cvTtsInputEl = document.getElementById('cv-tts-input');
    const sendCvTtsBtn = document.getElementById('send-cv-tts-btn');
    const addCvLibraryBtn = document.getElementById('add-cv-library-btn');
    const cvCacheHintEl = document.getElementById('cv-cache-hint');
    const cvLibrarySelectEl = document.getElementById('cv-library-select');
    const cvLibraryListEl = document.getElementById('cv-library-list');
    const aiTtsInputEl = document.getElementById('ai-tts-input');
    const sendAiTtsBtn = document.getElementById('send-ai-tts-btn');
    const addAiLibraryBtn = document.getElementById('add-ai-library-btn');
    const aiCacheHintEl = document.getElementById('ai-cache-hint');
    const aiLibrarySelectEl = document.getElementById('ai-library-select');
    const aiLibraryListEl = document.getElementById('ai-library-list');
    const aiModePillEl = document.getElementById('ai-mode-pill');
    const aiModeDescriptionEl = document.getElementById('ai-mode-description');
    const aiModeNormalBtn = document.getElementById('ai-mode-normal');
    const aiModeAbnormalBtn = document.getElementById('ai-mode-abnormal');
    const aiCoachSpeech1Btn = document.getElementById('ai-coach-speech1-btn');
    const aiCoachSpeech2Btn = document.getElementById('ai-coach-speech2-btn');
    const aiCoachSpeech3Btn = document.getElementById('ai-coach-speech3-btn');
    const aiCoachEncourageBtn = document.getElementById('ai-coach-encourage-btn');
    const logBodyEl = document.getElementById('log-body');
    const testBtn = document.getElementById('test-btn');
    const refreshBtn = document.getElementById('refresh-btn');
    const postureReadyBtn = document.getElementById('posture-ready-btn');
    const postureRenderBtn = document.getElementById('posture-render-btn');
    const postureStep2Btn = document.getElementById('posture-step2-btn');
    const postureStep3Btn = document.getElementById('posture-step3-btn');
    const postureStep4Btn = document.getElementById('posture-step4-btn');
    const postureReloadBtn = document.getElementById('posture-reload-btn');
    const pressureModeButtons = {
        empty: document.getElementById('pressure-mode-empty'),
        direct: document.getElementById('pressure-mode-direct'),
        repair: document.getElementById('pressure-mode-repair')
    };
    const traceModeButtons = {
        normal: document.getElementById('trace-mode-normal'),
        jitter: document.getElementById('trace-mode-jitter')
    };

    const SHANGHAI_TIME_FORMATTER = new Intl.DateTimeFormat('zh-CN', {
        timeZone: 'Asia/Shanghai',
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    let embeddedOnlineTtsRuntimeConfig = {
        activeAccountName: '',
        defaultVcn: 'xiaoyan'
    };
    let cvOnlineTtsRuntimeConfig = {
        activeAccountName: '',
        defaultVcn: 'xiaoyan'
    };
    let aiOnlineTtsRuntimeConfig = {
        activeAccountName: '',
        defaultVcn: 'xiaoyan'
    };
    let embeddedLibraryItems = [];
    let cvLibraryItems = [];
    let aiLibraryItems = [];
    let lastEmbeddedCacheFilename = '';
    let lastCvCacheFilename = '';
    let lastAiCacheFilename = '';

    function writeLog(message) {
        const now = SHANGHAI_TIME_FORMATTER.format(new Date());
        logBodyEl.textContent = `[${now}] ${message}\\n` + logBodyEl.textContent;
    }

    function updateSendEmbeddedTtsButtonState() {
        const currentMessage = embeddedTtsInputEl.value.trim();
        sendEmbeddedTtsBtn.disabled = currentMessage.length <= 0;
        addEmbeddedLibraryBtn.disabled = lastEmbeddedCacheFilename.length <= 0;
    }

    function updateSendCvTtsButtonState() {
        const currentMessage = cvTtsInputEl.value.trim();
        sendCvTtsBtn.disabled = currentMessage.length <= 0;
        addCvLibraryBtn.disabled = lastCvCacheFilename.length <= 0;
    }

    function updateSendAiTtsButtonState() {
        const currentMessage = aiTtsInputEl.value.trim();
        sendAiTtsBtn.disabled = currentMessage.length <= 0;
        addAiLibraryBtn.disabled = lastAiCacheFilename.length <= 0;
    }

    function updateSendLocalTtsButtonState() {
        const currentMessage = localTtsInputEl.value.trim();
        sendLocalTtsBtn.disabled = currentMessage.length <= 0;
    }

    function renderDeviceStatus(connectedClients) {
        connectedCountEl.textContent = String(connectedClients);
        if (connectedClients > 0) {
            deviceStatusTextEl.textContent = '在线';
            deviceStatusPillEl.textContent = `已有 ${connectedClients} 台设备在线`;
            deviceStatusPillEl.className = 'status-pill online';
        } else {
            deviceStatusTextEl.textContent = '离线';
            deviceStatusPillEl.textContent = '暂无设备在线';
            deviceStatusPillEl.className = 'status-pill offline';
        }
    }

    function renderAiMode(data) {
        const mode = data.mode || 'mode2';
        const modeLabel = data.modeLabel || (mode === 'mode1' ? '正常' : '非正常');
        const modeDescription = data.modeDescription || '等待后端返回 AI 模式说明。';
        aiModePillEl.textContent = modeLabel;
        aiModePillEl.className = `mode-pill ${mode === 'mode1' ? 'normal' : (mode === 'mode2' ? 'jitter' : 'mode3')}`;
        aiModeDescriptionEl.textContent = modeDescription;
        aiModeNormalBtn.classList.toggle('active-mode', mode === 'mode1');
        aiModeAbnormalBtn.classList.toggle('active-mode', mode !== 'mode1');
    }

    function renderPressureDemoMode(data) {
        const mode = data.mode || 'direct';
        const modeLabel = data.modeLabel || '模式 2';
        const modeDescription = data.modeDescription || '等待后端返回足压模式说明。';

        pressureModeLabelLargeEl.textContent = modeLabel;
        pressureModeDescriptionLargeEl.textContent = modeDescription;
        pressureModePillEl.textContent = modeLabel;
        pressureModePillEl.className = Object.prototype.hasOwnProperty.call(pressureModeButtons, mode)
            ? `mode-pill ${mode}`
            : 'mode-pill unknown';
        pressureModeDescriptionEl.textContent = modeDescription;

        Object.entries(pressureModeButtons).forEach(([key, button]) => {
            button.classList.toggle('active-mode', key === mode);
        });
    }

    function renderPressureTraceDemoMode(data) {
        const mode = data.mode || 'normal';
        const modeLabel = data.modeLabel || '轨迹正常';
        const modeDescription = data.modeDescription || '等待后端返回轨迹演示说明。';

        traceModePillEl.textContent = modeLabel;
        traceModePillEl.className = Object.prototype.hasOwnProperty.call(traceModeButtons, mode)
            ? `mode-pill ${mode}`
            : 'mode-pill unknown';
        traceModeDescriptionEl.textContent = modeDescription;

        Object.entries(traceModeButtons).forEach(([key, button]) => {
            button.classList.toggle('active-mode', key === mode);
        });
    }

    function renderEmbeddedOnlineTtsVoiceOptions(config) {
        embeddedOnlineTtsRuntimeConfig = {
            activeAccountName: (config && config.activeAccountName) || '',
            defaultVcn: (config && config.defaultVcn) || 'xiaoyan'
        };
    }

    function renderCvOnlineTtsVoiceOptions(config) {
        cvOnlineTtsRuntimeConfig = {
            activeAccountName: (config && config.activeAccountName) || '',
            defaultVcn: (config && config.defaultVcn) || 'xiaoyan'
        };
    }

    function renderAiOnlineTtsVoiceOptions(config) {
        aiOnlineTtsRuntimeConfig = {
            activeAccountName: (config && config.activeAccountName) || '',
            defaultVcn: (config && config.defaultVcn) || 'xiaoyan'
        };
    }

    function renderEmbeddedAudioLibrary(selectedFilename = embeddedLibrarySelectEl.value) {
        embeddedLibrarySelectEl.innerHTML = '<option value="">选择一个嵌入式音频</option>';
        embeddedLibraryItems.forEach((item) => {
            const option = document.createElement('option');
            option.value = item.filename;
            option.textContent = item.displayName;
            option.selected = item.filename === selectedFilename;
            embeddedLibrarySelectEl.appendChild(option);
        });

        embeddedLibraryListEl.innerHTML = '';
        embeddedLibraryItems.forEach((item) => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'quick-command-btn';
            button.textContent = item.displayName;
            button.title = '点击后直接播放这条嵌入式音频';
            button.classList.toggle('active', item.filename === selectedFilename);
            button.addEventListener('click', () => {
                embeddedLibrarySelectEl.value = item.filename;
                renderEmbeddedAudioLibrary(item.filename);
                void playEmbeddedLibraryAudio(item.filename);
            });
            embeddedLibraryListEl.appendChild(button);
        });
    }

    function renderCvAudioLibrary(selectedFilename = cvLibrarySelectEl.value) {
        cvLibrarySelectEl.innerHTML = '<option value="">选择一个计算机视觉音频</option>';
        cvLibraryItems.forEach((item) => {
            const option = document.createElement('option');
            option.value = item.filename;
            option.textContent = item.displayName;
            option.selected = item.filename === selectedFilename;
            cvLibrarySelectEl.appendChild(option);
        });

        cvLibraryListEl.innerHTML = '';
        cvLibraryItems.forEach((item) => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'quick-command-btn';
            button.textContent = item.displayName;
            button.title = '点击后直接播放这条计算机视觉音频';
            button.classList.toggle('active', item.filename === selectedFilename);
            button.addEventListener('click', () => {
                cvLibrarySelectEl.value = item.filename;
                renderCvAudioLibrary(item.filename);
                void playCvLibraryAudio(item.filename);
            });
            cvLibraryListEl.appendChild(button);
        });
    }

    function renderAiAudioLibrary(selectedFilename = aiLibrarySelectEl.value) {
        aiLibrarySelectEl.innerHTML = '<option value="">选择一个 AI 智能体音频</option>';
        aiLibraryItems.forEach((item) => {
            const option = document.createElement('option');
            option.value = item.filename;
            option.textContent = item.displayName;
            option.selected = item.filename === selectedFilename;
            aiLibrarySelectEl.appendChild(option);
        });

        aiLibraryListEl.innerHTML = '';
        aiLibraryItems.forEach((item) => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'quick-command-btn';
            button.textContent = item.displayName;
            button.title = '点击后直接播放这条 AI 智能体音频';
            button.classList.toggle('active', item.filename === selectedFilename);
            button.addEventListener('click', () => {
                aiLibrarySelectEl.value = item.filename;
                renderAiAudioLibrary(item.filename);
                void playAiLibraryAudio(item.filename);
            });
            aiLibraryListEl.appendChild(button);
        });
    }

    async function refreshDeviceStatus(silent = true) {
        try {
            const response = await fetch('/api/ws/harmony/status', {
                method: 'GET',
                cache: 'no-store'
            });
            const result = await response.json();
            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            socketPathEl.textContent = data.webSocketPath || '/ws/harmony-app';
            socketPathSideEl.textContent = data.webSocketPath || '/ws/harmony-app';
            if (!silent) {
                writeLog(`设备状态已刷新，当前连接 ${Number(data.connectedClients || 0)} 台。`);
            }
        } catch (error) {
            writeLog(`设备状态刷新失败：${error}`);
        }
    }

    async function refreshAiMode(silent = true) {
        try {
            const response = await fetch('/api/ai/mode', {
                method: 'GET',
                cache: 'no-store'
            });
            const result = await response.json();
            renderAiMode(result.data || {});
            if (!silent) {
                const data = result.data || {};
                writeLog(`AI 模式已刷新，当前为 ${(data.modeLabel || data.mode || '模式 1')}。`);
            }
        } catch (error) {
            writeLog(`AI 模式刷新失败：${error}`);
        }
    }

    async function refreshPressureDemoMode(silent = true) {
        try {
            const response = await fetch('/api/pressure/demo-mode', {
                method: 'GET',
                cache: 'no-store'
            });
            const result = await response.json();
            renderPressureDemoMode(result.data || {});
            if (!silent) {
                const data = result.data || {};
                writeLog(`足压模式已刷新，当前为 ${(data.modeLabel || data.mode || '模式 2')}。`);
            }
        } catch (error) {
            writeLog(`足压模式刷新失败：${error}`);
        }
    }

    async function refreshPressureTraceDemoMode(silent = true) {
        try {
            const response = await fetch('/api/pressure/trace-mode', {
                method: 'GET',
                cache: 'no-store'
            });
            const result = await response.json();
            renderPressureTraceDemoMode(result.data || {});
            if (!silent) {
                const data = result.data || {};
                writeLog(`轨迹模式已刷新，当前为 ${(data.modeLabel || data.mode || '轨迹正常')}。`);
            }
        } catch (error) {
            writeLog(`轨迹模式刷新失败：${error}`);
        }
    }

    async function refreshEmbeddedOnlineTtsConfig(silent = true) {
        try {
            const response = await fetch('/api/tts/bt/config', {
                method: 'GET',
                cache: 'no-store'
            });
            const result = await response.json();
            const data = result.data || {};
            renderEmbeddedOnlineTtsVoiceOptions(data);
            if (!silent && data.activeAccountName) {
                writeLog(`蓝牙在线语音配置已刷新，当前账号：${data.activeAccountName}，默认音色：${data.defaultVcn || 'xiaoyan'}。`);
            }
        } catch (error) {
            writeLog(`蓝牙在线语音配置刷新失败：${error}`);
        }
    }

    async function refreshEmbeddedAudioLibrary(silent = true) {
        try {
            const response = await fetch('/api/tts/bt/library', {
                method: 'GET',
                cache: 'no-store'
            });
            const result = await response.json();
            const data = Array.isArray(result.data) ? result.data : [];
            embeddedLibraryItems = data
                .map((item) => ({
                    filename: String(item.filename || '').trim(),
                    displayName: String(item.displayName || item.filename || '').trim(),
                    audioUrl: String(item.audioUrl || '').trim()
                }))
                .filter((item) => item.filename.length > 0 && item.displayName.length > 0);
            renderEmbeddedAudioLibrary();
            if (!silent) {
                writeLog(`蓝牙音频库已刷新，当前共 ${embeddedLibraryItems.length} 条。`);
            }
        } catch (error) {
            writeLog(`蓝牙音频库刷新失败：${error}`);
        }
    }

    async function refreshCvOnlineTtsConfig(silent = true) {
        try {
            const response = await fetch('/api/tts/cp/config', {
                method: 'GET',
                cache: 'no-store'
            });
            const result = await response.json();
            const data = result.data || {};
            renderCvOnlineTtsVoiceOptions(data);
            if (!silent && data.activeAccountName) {
                writeLog(`计算机视觉在线语音配置已刷新，当前账号：${data.activeAccountName}，默认音色：${data.defaultVcn || 'xiaoyan'}。`);
            }
        } catch (error) {
            writeLog(`计算机视觉在线语音配置刷新失败：${error}`);
        }
    }

    async function refreshCvAudioLibrary(silent = true) {
        try {
            const response = await fetch('/api/tts/cp/library', {
                method: 'GET',
                cache: 'no-store'
            });
            const result = await response.json();
            const data = Array.isArray(result.data) ? result.data : [];
            cvLibraryItems = data
                .map((item) => ({
                    filename: String(item.filename || '').trim(),
                    displayName: String(item.displayName || item.filename || '').trim(),
                    audioUrl: String(item.audioUrl || '').trim()
                }))
                .filter((item) => item.filename.length > 0 && item.displayName.length > 0);
            renderCvAudioLibrary();
            if (!silent) {
                writeLog(`计算机视觉音频库已刷新，当前共 ${cvLibraryItems.length} 条。`);
            }
        } catch (error) {
            writeLog(`计算机视觉音频库刷新失败：${error}`);
        }
    }

    async function refreshAiOnlineTtsConfig(silent = true) {
        try {
            const response = await fetch('/api/tts/ai/config', {
                method: 'GET',
                cache: 'no-store'
            });
            const result = await response.json();
            const data = result.data || {};
            renderAiOnlineTtsVoiceOptions(data);
            if (!silent && data.activeAccountName) {
                writeLog(`AI 智能体在线语音配置已刷新，当前账号：${data.activeAccountName}，默认音色：${data.defaultVcn || 'xiaoyan'}。`);
            }
        } catch (error) {
            writeLog(`AI 智能体在线语音配置刷新失败：${error}`);
        }
    }

    async function refreshAiAudioLibrary(silent = true) {
        try {
            const response = await fetch('/api/tts/ai/library', {
                method: 'GET',
                cache: 'no-store'
            });
            const result = await response.json();
            const data = Array.isArray(result.data) ? result.data : [];
            aiLibraryItems = data
                .map((item) => ({
                    filename: String(item.filename || '').trim(),
                    displayName: String(item.displayName || item.filename || '').trim(),
                    audioUrl: String(item.audioUrl || '').trim()
                }))
                .filter((item) => item.filename.length > 0 && item.displayName.length > 0);
            renderAiAudioLibrary();
            if (!silent) {
                writeLog(`AI 智能体音频库已刷新，当前共 ${aiLibraryItems.length} 条。`);
            }
        } catch (error) {
            writeLog(`AI 智能体音频库刷新失败：${error}`);
        }
    }

    async function switchAiMode(mode) {
        writeLog(`正在切换 AI 模式到 ${mode}...`);

        try {
            const response = await fetch(`/api/ai/mode?mode=${encodeURIComponent(mode)}`, {
                method: 'POST'
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`切换失败：${result.message || '未知错误'}`);
                return;
            }

            renderAiMode(result.data || {});
            writeLog(`切换成功：${(result.data && result.data.modeLabel) || mode}`);
        } catch (error) {
            writeLog(`切换 AI 模式失败：${error}`);
        }
    }

    async function switchPressureDemoMode(mode) {
        const buttons = Object.values(pressureModeButtons);
        buttons.forEach(button => button.disabled = true);
        writeLog(`正在切换足压模式到 ${mode}...`);

        try {
            const response = await fetch(`/api/pressure/demo-mode?mode=${encodeURIComponent(mode)}`, {
                method: 'POST'
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`足压模式切换失败：${result.message || '未知错误'}`);
                return;
            }

            renderPressureDemoMode(result.data || {});
            writeLog(`足压模式切换成功：${(result.data && result.data.modeLabel) || mode}`);
        } catch (error) {
            writeLog(`足压模式切换失败：${error}`);
        } finally {
            buttons.forEach(button => button.disabled = false);
        }
    }

    async function switchPressureTraceDemoMode(mode) {
        const buttons = Object.values(traceModeButtons);
        buttons.forEach(button => button.disabled = true);
        writeLog(`正在切换轨迹模式到 ${mode}...`);

        try {
            const response = await fetch(`/api/pressure/trace-mode?mode=${encodeURIComponent(mode)}`, {
                method: 'POST'
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`轨迹模式切换失败：${result.message || '未知错误'}`);
                return;
            }

            renderPressureTraceDemoMode(result.data || {});
            writeLog(`轨迹模式切换成功：${(result.data && result.data.modeLabel) || mode}`);
        } catch (error) {
            writeLog(`轨迹模式切换失败：${error}`);
        } finally {
            buttons.forEach(button => button.disabled = false);
        }
    }

    async function testConnection() {
        testBtn.disabled = true;
        writeLog('正在发送 websocket 连接成功通知...');

        try {
            const response = await fetch('/api/ws/harmony/notify-connected', {
                method: 'POST'
            });
            const result = await response.json();
            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            writeLog(`${result.message || '发送完成'}，本次推送 ${Number(data.deliveredCount || 0)} 台设备。`);
        } catch (error) {
            writeLog(`发送连接成功通知失败：${error}`);
        } finally {
            testBtn.disabled = false;
        }
    }

    async function sendLocalTtsMessage() {
        const message = localTtsInputEl.value.trim();
        if (message.length <= 0) {
            updateSendLocalTtsButtonState();
            return;
        }

        sendLocalTtsBtn.disabled = true;
        writeLog(`正在发送鸿蒙端 TTS：${message}`);

        try {
            const response = await fetch('/api/ws/harmony/notify-tts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`发送鸿蒙端 TTS 失败：${result.message || '未知错误'}`);
                return;
            }

            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            writeLog(`鸿蒙端 TTS 发送完成，内容“${data.message || message}”，本次推送 ${Number(data.deliveredCount || 0)} 台设备。`);
            localTtsInputEl.value = '';
            updateSendLocalTtsButtonState();
        } catch (error) {
            writeLog(`发送鸿蒙端 TTS 失败：${error}`);
        } finally {
            updateSendLocalTtsButtonState();
        }
    }

    async function sendEmbeddedOnlineTtsMessage() {
        const message = embeddedTtsInputEl.value.trim();
        if (message.length <= 0) {
            updateSendEmbeddedTtsButtonState();
            return;
        }

        sendEmbeddedTtsBtn.disabled = true;
        writeLog(`正在发送蓝牙在线语音：${message}`);

        try {
            const response = await fetch('/api/ws/harmony/notify-bt-online-tts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`发送蓝牙在线语音失败：${result.message || '未知错误'}`);
                return;
            }

            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            lastEmbeddedCacheFilename = String(data.filename || '').trim();
            embeddedCacheHintEl.textContent = lastEmbeddedCacheFilename
                ? `最近生成的蓝牙缓存文件：${lastEmbeddedCacheFilename}`
                : '发送后会先进入 cache，再可加入蓝牙语音库。';
            writeLog(`蓝牙在线语音发送完成，内容“${data.message || message}”，文件 ${data.filename || '未返回'}，音色 ${data.voiceName || embeddedOnlineTtsRuntimeConfig.defaultVcn || 'xiaoyan'}，本次推送 ${Number(data.deliveredCount || 0)} 台设备。`);
            embeddedTtsInputEl.value = '';
            updateSendEmbeddedTtsButtonState();
            void refreshEmbeddedAudioLibrary(true);
        } catch (error) {
            writeLog(`发送蓝牙在线语音失败：${error}`);
        } finally {
            updateSendEmbeddedTtsButtonState();
        }
    }

    async function sendCvOnlineTtsMessage() {
        const message = cvTtsInputEl.value.trim();
        if (message.length <= 0) {
            updateSendCvTtsButtonState();
            return;
        }

        sendCvTtsBtn.disabled = true;
        writeLog(`正在发送计算机视觉在线语音：${message}`);

        try {
            const response = await fetch('/api/ws/harmony/notify-cp-online-tts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`发送计算机视觉在线语音失败：${result.message || '未知错误'}`);
                return;
            }

            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            lastCvCacheFilename = String(data.filename || '').trim();
            cvCacheHintEl.textContent = lastCvCacheFilename
                ? `最近生成的计算机视觉缓存文件：${lastCvCacheFilename}`
                : '发送后会先进入 cache，再可加入计算机视觉语音库。';
            writeLog(`计算机视觉在线语音发送完成，内容“${data.message || message}”，文件 ${data.filename || '未返回'}，音色 ${data.voiceName || cvOnlineTtsRuntimeConfig.defaultVcn || 'xiaoyan'}，本次推送 ${Number(data.deliveredCount || 0)} 台设备。`);
            cvTtsInputEl.value = '';
            updateSendCvTtsButtonState();
            void refreshCvAudioLibrary(true);
        } catch (error) {
            writeLog(`发送计算机视觉在线语音失败：${error}`);
        } finally {
            updateSendCvTtsButtonState();
        }
    }

    async function sendAiOnlineTtsMessage() {
        const message = aiTtsInputEl.value.trim();
        if (message.length <= 0) {
            updateSendAiTtsButtonState();
            return;
        }

        sendAiTtsBtn.disabled = true;
        writeLog(`正在发送 AI 智能体在线语音：${message}`);

        try {
            const response = await fetch('/api/ws/harmony/notify-ai-online-tts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`发送 AI 智能体在线语音失败：${result.message || '未知错误'}`);
                return;
            }

            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            lastAiCacheFilename = String(data.filename || '').trim();
            aiCacheHintEl.textContent = lastAiCacheFilename
                ? `最近生成的 AI 智能体缓存文件：${lastAiCacheFilename}`
                : '发送后会先进入 cache，再可加入 AI 智能体语音库。';
            writeLog(`AI 智能体在线语音发送完成，内容“${data.message || message}”，文件 ${data.filename || '未返回'}，音色 ${data.voiceName || aiOnlineTtsRuntimeConfig.defaultVcn || 'xiaoyan'}，本次推送 ${Number(data.deliveredCount || 0)} 台设备。`);
            aiTtsInputEl.value = '';
            updateSendAiTtsButtonState();
            void refreshAiAudioLibrary(true);
        } catch (error) {
            writeLog(`发送 AI 智能体在线语音失败：${error}`);
        } finally {
            updateSendAiTtsButtonState();
        }
    }

    async function addEmbeddedCacheToLibrary() {
        if (!lastEmbeddedCacheFilename) {
            return;
        }
        addEmbeddedLibraryBtn.disabled = true;
        writeLog(`正在将蓝牙缓存音频加入语音库：${lastEmbeddedCacheFilename}`);
        try {
            const response = await fetch('/api/tts/bt/promote-cache', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ filename: lastEmbeddedCacheFilename })
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`加入蓝牙语音库失败：${result.message || '未知错误'}`);
                return;
            }
            embeddedCacheHintEl.textContent = `已加入蓝牙语音库：${lastEmbeddedCacheFilename}`;
            writeLog(`蓝牙缓存音频已加入语音库：${lastEmbeddedCacheFilename}`);
            void refreshEmbeddedAudioLibrary(true);
        } catch (error) {
            writeLog(`加入蓝牙语音库失败：${error}`);
        } finally {
            updateSendEmbeddedTtsButtonState();
        }
    }

    async function addCvCacheToLibrary() {
        if (!lastCvCacheFilename) {
            return;
        }
        addCvLibraryBtn.disabled = true;
        writeLog(`正在将计算机视觉缓存音频加入语音库：${lastCvCacheFilename}`);
        try {
            const response = await fetch('/api/tts/cp/promote-cache', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ filename: lastCvCacheFilename })
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`加入计算机视觉语音库失败：${result.message || '未知错误'}`);
                return;
            }
            cvCacheHintEl.textContent = `已加入计算机视觉语音库：${lastCvCacheFilename}`;
            writeLog(`计算机视觉缓存音频已加入语音库：${lastCvCacheFilename}`);
            void refreshCvAudioLibrary(true);
        } catch (error) {
            writeLog(`加入计算机视觉语音库失败：${error}`);
        } finally {
            updateSendCvTtsButtonState();
        }
    }

    async function addAiCacheToLibrary() {
        if (!lastAiCacheFilename) {
            return;
        }
        addAiLibraryBtn.disabled = true;
        writeLog(`正在将 AI 智能体缓存音频加入语音库：${lastAiCacheFilename}`);
        try {
            const response = await fetch('/api/tts/ai/promote-cache', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ filename: lastAiCacheFilename })
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`加入 AI 智能体语音库失败：${result.message || '未知错误'}`);
                return;
            }
            aiCacheHintEl.textContent = `已加入 AI 智能体语音库：${lastAiCacheFilename}`;
            writeLog(`AI 智能体缓存音频已加入语音库：${lastAiCacheFilename}`);
            void refreshAiAudioLibrary(true);
        } catch (error) {
            writeLog(`加入 AI 智能体语音库失败：${error}`);
        } finally {
            updateSendAiTtsButtonState();
        }
    }

    async function sendPostureDemoCommand(action, label) {
        const normalizedAction = String(action || '').trim();
        if (normalizedAction.length <= 0) {
            return;
        }

        writeLog(`正在发送体态演示指令：${label}`);
        try {
            const response = await fetch('/api/ws/harmony/posture-demo', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ action: normalizedAction })
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`体态演示指令失败：${result.message || '未知错误'}`);
                return;
            }

            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            if (Number(data.deliveredCount || 0) <= 0) {
                writeLog(`体态演示未投递到设备：${data.title || label}，当前无在线设备连接。`);
                return;
            }
            writeLog(`体态动作已发送：${data.action || action} -> ${data.title || label}，${data.message || ''}`);
        } catch (error) {
            writeLog(`体态演示指令失败：${error}`);
        }
    }

    async function sendPostureDemoReload() {
        writeLog('正在发送体态工作台重载指令');
        try {
            const response = await fetch('/api/ws/harmony/posture-demo-reload', {
                method: 'POST'
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`体态工作台重载失败：${result.message || '未知错误'}`);
                return;
            }

            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            writeLog(`体态工作台重载已发送，本次推送 ${Number(data.deliveredCount || 0)} 台设备。`);
        } catch (error) {
            writeLog(`体态工作台重载失败：${error}`);
        }
    }

    function setActiveStageButton(activeButton) {
        [
            postureReadyBtn,
            postureRenderBtn,
            postureStep2Btn,
            postureStep3Btn,
            postureStep4Btn
        ].forEach((button) => {
            button.classList.toggle('stage-btn-active', button === activeButton);
        });
    }

    async function playEmbeddedLibraryAudio(filename) {
        const normalizedFilename = String(filename || '').trim();
        if (normalizedFilename.length <= 0) {
            return;
        }

        writeLog(`正在播放蓝牙音频：${normalizedFilename}`);
        try {
            const response = await fetch('/api/ws/harmony/play-bt-library-audio', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ filename: normalizedFilename })
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`播放蓝牙音频失败：${result.message || '未知错误'}`);
                return;
            }

            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            writeLog(`蓝牙音频播放完成，文件“${data.filename || normalizedFilename}”，本次推送 ${Number(data.deliveredCount || 0)} 台设备。`);
        } catch (error) {
            writeLog(`播放蓝牙音频失败：${error}`);
        }
    }

    async function playCvLibraryAudio(filename) {
        const normalizedFilename = String(filename || '').trim();
        if (normalizedFilename.length <= 0) {
            return;
        }

        writeLog(`正在播放计算机视觉音频：${normalizedFilename}`);
        try {
            const response = await fetch('/api/ws/harmony/play-cp-library-audio', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ filename: normalizedFilename })
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`播放计算机视觉音频失败：${result.message || '未知错误'}`);
                return;
            }

            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            writeLog(`计算机视觉音频播放完成，文件“${data.filename || normalizedFilename}”，本次推送 ${Number(data.deliveredCount || 0)} 台设备。`);
        } catch (error) {
            writeLog(`播放计算机视觉音频失败：${error}`);
        }
    }

    async function playAiLibraryAudio(filename) {
        const normalizedFilename = String(filename || '').trim();
        if (normalizedFilename.length <= 0) {
            return;
        }

        writeLog(`正在播放 AI 智能体音频：${normalizedFilename}`);
        try {
            const response = await fetch('/api/ws/harmony/play-ai-library-audio', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ filename: normalizedFilename })
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`播放 AI 智能体音频失败：${result.message || '未知错误'}`);
                return;
            }

            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            writeLog(`AI 智能体音频播放完成，文件“${data.filename || normalizedFilename}”，本次推送 ${Number(data.deliveredCount || 0)} 台设备。`);
        } catch (error) {
            writeLog(`播放 AI 智能体音频失败：${error}`);
        }
    }

    async function sendAiCoachAction(action, label) {
        const normalizedAction = String(action || '').trim();
        if (normalizedAction.length <= 0) {
            return;
        }

        const actionButtons = [
            aiCoachSpeech1Btn,
            aiCoachSpeech2Btn,
            aiCoachSpeech3Btn,
            aiCoachEncourageBtn
        ];
        actionButtons.forEach((button) => {
            button.disabled = true;
        });

        writeLog(`正在发送 AI 陪练动作：${label}`);
        try {
            const response = await fetch('/api/ws/harmony/ai-coach-action', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ action: normalizedAction })
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`AI 陪练动作发送失败：${result.message || '未知错误'}`);
                return;
            }

            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            writeLog(`AI 陪练动作已发送：${data.title || label}，视频 ${data.videoUrl || '未返回'}，音频 ${data.audioFilename || '未返回'}，本次推送 ${Number(data.deliveredCount || 0)} 台设备。`);
        } catch (error) {
            writeLog(`AI 陪练动作发送失败：${error}`);
        } finally {
            actionButtons.forEach((button) => {
                button.disabled = false;
            });
        }
    }

    refreshBtn.addEventListener('click', async () => {
        await refreshDeviceStatus(false);
        await refreshAiMode(false);
        await refreshPressureDemoMode(false);
        await refreshPressureTraceDemoMode(false);
        await refreshEmbeddedOnlineTtsConfig(false);
        await refreshEmbeddedAudioLibrary(false);
        await refreshCvOnlineTtsConfig(false);
        await refreshCvAudioLibrary(false);
        await refreshAiOnlineTtsConfig(false);
        await refreshAiAudioLibrary(false);
    });

    testBtn.addEventListener('click', testConnection);
    sendLocalTtsBtn.addEventListener('click', sendLocalTtsMessage);
    sendEmbeddedTtsBtn.addEventListener('click', sendEmbeddedOnlineTtsMessage);
    sendCvTtsBtn.addEventListener('click', sendCvOnlineTtsMessage);
    sendAiTtsBtn.addEventListener('click', sendAiOnlineTtsMessage);

    localTtsInputEl.addEventListener('input', updateSendLocalTtsButtonState);
    localTtsInputEl.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            void sendLocalTtsMessage();
        }
    });
    embeddedTtsInputEl.addEventListener('input', updateSendEmbeddedTtsButtonState);
    embeddedTtsInputEl.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            void sendEmbeddedOnlineTtsMessage();
        }
    });
    embeddedLibrarySelectEl.addEventListener('change', () => {
        const filename = embeddedLibrarySelectEl.value;
        renderEmbeddedAudioLibrary(filename);
        if (filename) {
            void playEmbeddedLibraryAudio(filename);
        }
    });
    addEmbeddedLibraryBtn.addEventListener('click', addEmbeddedCacheToLibrary);

    cvTtsInputEl.addEventListener('input', () => {
        updateSendCvTtsButtonState();
    });
    cvTtsInputEl.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            void sendCvOnlineTtsMessage();
        }
    });
    cvLibrarySelectEl.addEventListener('change', () => {
        const filename = cvLibrarySelectEl.value;
        renderCvAudioLibrary(filename);
        if (filename) {
            void playCvLibraryAudio(filename);
        }
    });
    addCvLibraryBtn.addEventListener('click', addCvCacheToLibrary);

    aiTtsInputEl.addEventListener('input', updateSendAiTtsButtonState);
    aiTtsInputEl.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            void sendAiOnlineTtsMessage();
        }
    });
    aiLibrarySelectEl.addEventListener('change', () => {
        const filename = aiLibrarySelectEl.value;
        renderAiAudioLibrary(filename);
        if (filename) {
            void playAiLibraryAudio(filename);
        }
    });
    addAiLibraryBtn.addEventListener('click', addAiCacheToLibrary);
    aiCoachSpeech1Btn.addEventListener('click', () => {
        void sendAiCoachAction('speech1', '讲话1');
    });
    aiCoachSpeech2Btn.addEventListener('click', () => {
        void sendAiCoachAction('speech2', '讲话2');
    });
    aiCoachSpeech3Btn.addEventListener('click', () => {
        void sendAiCoachAction('speech3', '讲话3');
    });
    aiCoachEncourageBtn.addEventListener('click', () => {
        void sendAiCoachAction('encourage', '鼓励');
    });
    aiModeNormalBtn.addEventListener('click', () => {
        void switchAiMode('mode1');
    });
    aiModeAbnormalBtn.addEventListener('click', () => {
        void switchAiMode('mode2');
    });
    postureReadyBtn.textContent = '默认';
    postureRenderBtn.textContent = '渲染';
    postureStep2Btn.textContent = '阶段2';
    postureStep3Btn.textContent = '阶段3';
    postureStep4Btn.textContent = '阶段4';
    postureReloadBtn.textContent = '重载';
    postureReadyBtn.addEventListener('click', () => {
        setActiveStageButton(postureReadyBtn);
        void sendPostureDemoCommand('normal', '默认');
    });
    postureRenderBtn.addEventListener('click', () => {
        setActiveStageButton(postureRenderBtn);
        void sendPostureDemoCommand('render', '渲染');
    });
    postureStep2Btn.addEventListener('click', () => {
        setActiveStageButton(postureStep2Btn);
        void sendPostureDemoCommand('stage2', '阶段2');
    });
    postureStep3Btn.addEventListener('click', () => {
        setActiveStageButton(postureStep3Btn);
        void sendPostureDemoCommand('stage3', '阶段3');
    });
    postureStep4Btn.addEventListener('click', () => {
        setActiveStageButton(postureStep4Btn);
        void sendPostureDemoCommand('stage4', '阶段4');
    });
    postureReloadBtn.addEventListener('click', () => void sendPostureDemoReload());
    setActiveStageButton(postureReadyBtn);

    pressureModeButtons.empty.addEventListener('click', () => switchPressureDemoMode('empty'));
    pressureModeButtons.direct.addEventListener('click', () => switchPressureDemoMode('direct'));
    pressureModeButtons.repair.addEventListener('click', () => switchPressureDemoMode('repair'));
    traceModeButtons.normal.addEventListener('click', () => switchPressureTraceDemoMode('normal'));
    traceModeButtons.jitter.addEventListener('click', () => switchPressureTraceDemoMode('jitter'));

    renderEmbeddedAudioLibrary();
    renderCvAudioLibrary();
    renderAiAudioLibrary();
    updateSendLocalTtsButtonState();
    updateSendEmbeddedTtsButtonState();
    updateSendCvTtsButtonState();
    updateSendAiTtsButtonState();
    refreshDeviceStatus(false);
    refreshAiMode(false);
    refreshPressureDemoMode(false);
    refreshPressureTraceDemoMode(false);
    refreshEmbeddedOnlineTtsConfig(false);
    refreshEmbeddedAudioLibrary(false);
    refreshCvOnlineTtsConfig(false);
    refreshCvAudioLibrary(false);
    refreshAiOnlineTtsConfig(false);
    refreshAiAudioLibrary(false);

    window.setInterval(() => {
        refreshDeviceStatus(true);
        refreshAiMode(true);
        refreshPressureDemoMode(true);
        refreshPressureTraceDemoMode(true);
        updateSendLocalTtsButtonState();
        refreshEmbeddedOnlineTtsConfig(true);
        refreshEmbeddedAudioLibrary(true);
        refreshCvOnlineTtsConfig(true);
        refreshCvAudioLibrary(true);
        refreshAiOnlineTtsConfig(true);
        refreshAiAudioLibrary(true);
    }, 5000);
</script>
</body>
</html>"""

