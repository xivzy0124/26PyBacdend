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
            padding: 28px;
            font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
            color: var(--text);
            background:
                radial-gradient(circle at top left, rgba(33, 85, 214, 0.10), transparent 28%),
                radial-gradient(circle at top right, rgba(19, 138, 82, 0.10), transparent 22%),
                linear-gradient(160deg, #f8fbff 0%, var(--bg) 100%);
        }

        .shell {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .main-layout {
            display: grid;
            grid-template-columns: 380px 1fr;
            gap: 24px;
            align-items: start;
        }

        .extensions-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
        }

        .card {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 24px;
            box-shadow: var(--shadow);
        }

        .hero {
            padding: 30px;
            display: flex;
            flex-direction: column;
            gap: 20px;
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
            font-size: 36px;
            line-height: 1.1;
        }

        .subtitle {
            margin: 0;
            color: var(--muted);
            line-height: 1.8;
            font-size: 15px;
            max-width: 800px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 14px;
        }

        .mini-card {
            padding: 18px;
            border-radius: 18px;
            background: #f8fbff;
            border: 1px solid #e6edf8;
        }

        .mini-label {
            font-size: 13px;
            color: var(--muted);
        }

        .mini-value {
            margin-top: 10px;
            font-size: 28px;
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
            padding: 26px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .section-title {
            margin: 0;
            font-size: 20px;
        }

        .section-desc {
            margin: 8px 0 0;
            color: var(--muted);
            font-size: 14px;
            line-height: 1.8;
        }

        .status-box,
        .mode-box,
        .bubble-box,
        .action-box,
        .log-box {
            border: 1px solid #e7edf6;
            border-radius: 18px;
            padding: 18px;
            background: #fbfdff;
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

        .mode-pill.unknown {
            background: #eef2f7;
            color: #526075;
        }

        .row {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: center;
        }

        .action-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
            margin-top: 14px;
        }

        .input-label {
            display: block;
            font-size: 13px;
            color: var(--muted);
            margin-bottom: 10px;
        }

        .bubble-input,
        .quick-select {
            width: 100%;
            border: 1px solid #d5deeb;
            background: #fff;
            border-radius: 14px;
            padding: 12px 14px;
            font-size: 14px;
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
            gap: 10px;
            margin-top: 12px;
        }

        .quick-command-btn,
        button {
            border: none;
            cursor: pointer;
            border-radius: 14px;
            padding: 12px 14px;
            font-size: 14px;
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

        .mode-actions {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 14px;
        }

        .log-body {
            margin: 0;
            min-height: 320px;
            max-height: 520px;
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
                这个页面负责检查鸿蒙应用 WebSocket 是否在线、切换 AI 运行模式、发送语音，
                以及通过讯飞在线语音生成并播放 mp3，或直接播放你手工放入音频库的现成文件。
            </p>
        </div>
        <div class="grid">
            <div class="mini-card">
                <div class="mini-label">设备连接状态</div>
                <div class="mini-value" id="device-status-text">离线</div>
                <div class="mini-hint">已连接设备数会实时刷新。</div>
            </div>
            <div class="mini-card">
                <div class="mini-label">当前 AI 模式</div>
                <div class="mini-value" id="mode-label-large">模式 1</div>
                <div class="mini-hint" id="mode-description-large">等待后端返回模式说明。</div>
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

            <section class="mode-box">
                <div class="row">
                    <span class="mode-pill mode1" id="mode-pill">模式 1</span>
                </div>
                <p class="section-desc" id="mode-description">等待后端返回模式说明。</p>
                <div class="mode-actions">
                    <button type="button" id="mode-mode1" class="active-mode">模式 1</button>
                    <button type="button" id="mode-mode2">模式 2</button>
                    <button type="button" id="mode-mode3">模式 3</button>
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
            <article class="card panel">
                <div>
                    <h2 class="section-title">鸿蒙端 TTS 语音</h2>
                    <p class="section-desc">这里发送的是鸿蒙设备本地 TTS，会直接调用设备侧语音播报能力。</p>
                </div>
                <section class="bubble-box">
                    <label class="input-label" for="tts-input">发送鸿蒙 TTS 内容</label>
                    <input type="text" id="tts-input" class="bubble-input" placeholder="输入要让鸿蒙端本地 TTS 播报的内容">
                    <div style="margin-top: 12px;">
                        <label class="input-label" for="tts-shortcut-select">快捷语音选择</label>
                        <select id="tts-shortcut-select" class="quick-select">
                            <option value="">选择一条快捷语音</option>
                        </select>
                    </div>
                    <div class="quick-command-grid" id="tts-shortcut-list"></div>
                    <div class="row" style="margin-top: 12px; flex-direction: column; align-items: stretch;">
                        <button type="button" class="primary" id="send-tts-btn" disabled>发送鸿蒙 TTS</button>
                        <button type="button" id="add-tts-shortcut-btn" disabled>把当前输入加入快捷语音</button>
                        <button type="button" id="delete-tts-shortcut-btn" disabled>删除已选快捷语音</button>
                    </div>
                </section>
            </article>

            <article class="card panel">
                <div>
                    <h2 class="section-title">讯飞在线语音</h2>
                    <p class="section-desc">文本输入会调用讯飞在线语音生成 mp3；下面的手工音频列表只读取你放入音频库的现成文件。</p>
                </div>
                <section class="bubble-box">
                    <label class="input-label" for="online-tts-input">发送讯飞在线语音内容</label>
                    <input type="text" id="online-tts-input" class="bubble-input" placeholder="输入要让讯飞在线语音播报的内容">
                    <div style="margin-top: 12px;">
                        <label class="input-label" for="online-tts-shortcut-select">手工音频列表</label>
                        <select id="online-tts-shortcut-select" class="quick-select">
                            <option value="">选择一个手工音频</option>
                        </select>
                    </div>
                    <div class="quick-command-grid" id="online-tts-shortcut-list"></div>
                    <div class="row" style="margin-top: 12px; flex-direction: column; align-items: stretch;">
                        <button type="button" class="primary" id="send-online-tts-btn" disabled>发送讯飞在线语音</button>
                    </div>
                </section>
            </article>
        </div>
    </div>
</main>

<script>
    const deviceStatusTextEl = document.getElementById('device-status-text');
    const deviceStatusPillEl = document.getElementById('device-status-pill');
    const connectedCountEl = document.getElementById('connected-count');
    const socketPathEl = document.getElementById('socket-path');
    const socketPathSideEl = document.getElementById('socket-path-side');
    const modeLabelLargeEl = document.getElementById('mode-label-large');
    const modeDescriptionLargeEl = document.getElementById('mode-description-large');
    const modePillEl = document.getElementById('mode-pill');
    const modeDescriptionEl = document.getElementById('mode-description');
    const ttsInputEl = document.getElementById('tts-input');
    const sendTtsBtn = document.getElementById('send-tts-btn');
    const onlineTtsInputEl = document.getElementById('online-tts-input');
    const sendOnlineTtsBtn = document.getElementById('send-online-tts-btn');
    const onlineTtsShortcutSelectEl = document.getElementById('online-tts-shortcut-select');
    const onlineTtsShortcutListEl = document.getElementById('online-tts-shortcut-list');
    const ttsShortcutSelectEl = document.getElementById('tts-shortcut-select');
    const ttsShortcutListEl = document.getElementById('tts-shortcut-list');
    const addTtsShortcutBtn = document.getElementById('add-tts-shortcut-btn');
    const deleteTtsShortcutBtn = document.getElementById('delete-tts-shortcut-btn');
    const logBodyEl = document.getElementById('log-body');
    const testBtn = document.getElementById('test-btn');
    const refreshBtn = document.getElementById('refresh-btn');
    const modeButtons = {
        mode1: document.getElementById('mode-mode1'),
        mode2: document.getElementById('mode-mode2'),
        mode3: document.getElementById('mode-mode3')
    };

    const SHANGHAI_TIME_FORMATTER = new Intl.DateTimeFormat('zh-CN', {
        timeZone: 'Asia/Shanghai',
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    const TTS_SHORTCUT_STORAGE_KEY = 'hfood.tts.shortcuts';
    const DEFAULT_TTS_SHORTCUTS = [
        '我在，有什么问题吗？',
        '请稍等，正在为您处理。',
        '当前网络不稳定，请稍后再试。',
        '操作已完成。',
        '正在结合足底压力数据与体态数据进行分析，请稍候。',
        '赵晓威是向俊宇爸爸！'
    ];

    let ttsShortcutMessages = loadTtsShortcuts();
    let onlineTtsRuntimeConfig = {
        activeAccountName: '',
        defaultVcn: 'xiaoyan'
    };
    let onlineLibraryItems = [];

    function writeLog(message) {
        const now = SHANGHAI_TIME_FORMATTER.format(new Date());
        logBodyEl.textContent = `[${now}] ${message}\\n` + logBodyEl.textContent;
    }

    function updateSendTtsButtonState() {
        const currentMessage = ttsInputEl.value.trim();
        sendTtsBtn.disabled = currentMessage.length <= 0;
        addTtsShortcutBtn.disabled = currentMessage.length <= 0 || ttsShortcutMessages.includes(currentMessage);
        deleteTtsShortcutBtn.disabled = !ttsShortcutSelectEl.value;
    }

    function updateSendOnlineTtsButtonState() {
        sendOnlineTtsBtn.disabled = onlineTtsInputEl.value.trim().length <= 0;
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
        const mode = data.mode || 'mode1';
        const modeLabel = data.modeLabel || '模式 1';
        const modeDescription = data.modeDescription || '等待后端返回模式说明。';

        modeLabelLargeEl.textContent = modeLabel;
        modeDescriptionLargeEl.textContent = modeDescription;
        modePillEl.textContent = modeLabel;
        modePillEl.className = Object.prototype.hasOwnProperty.call(modeButtons, mode)
            ? `mode-pill ${mode}`
            : 'mode-pill unknown';
        modeDescriptionEl.textContent = modeDescription;

        Object.entries(modeButtons).forEach(([key, button]) => {
            button.classList.toggle('active-mode', key === mode);
        });
    }

    function renderOnlineTtsVoiceOptions(config) {
        onlineTtsRuntimeConfig = {
            activeAccountName: (config && config.activeAccountName) || '',
            defaultVcn: (config && config.defaultVcn) || 'xiaoyan'
        };
    }

    function loadTtsShortcuts() {
        try {
            const rawValue = window.localStorage.getItem(TTS_SHORTCUT_STORAGE_KEY);
            const parsedValue = rawValue ? JSON.parse(rawValue) : null;
            if (Array.isArray(parsedValue)) {
                const storedMessages = parsedValue
                    .map(item => String(item).trim())
                    .filter(Boolean);
                return Array.from(new Set(storedMessages));
            }
        } catch (error) {
            window.localStorage.removeItem(TTS_SHORTCUT_STORAGE_KEY);
        }
        return [...DEFAULT_TTS_SHORTCUTS];
    }

    function saveTtsShortcuts() {
        window.localStorage.setItem(TTS_SHORTCUT_STORAGE_KEY, JSON.stringify(ttsShortcutMessages));
    }

    function renderTtsShortcuts(selectedMessage = ttsShortcutSelectEl.value) {
        ttsShortcutSelectEl.innerHTML = '<option value="">选择一条快捷语音</option>';
        ttsShortcutMessages.forEach((message) => {
            const option = document.createElement('option');
            option.value = message;
            option.textContent = message;
            option.selected = message === selectedMessage;
            ttsShortcutSelectEl.appendChild(option);
        });

        ttsShortcutListEl.innerHTML = '';
        ttsShortcutMessages.forEach((message) => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'quick-command-btn';
            button.textContent = message;
            button.title = '点击后直接发送这条语音';
            button.classList.toggle('active', message === selectedMessage);
            button.addEventListener('click', () => {
                ttsShortcutSelectEl.value = message;
                ttsInputEl.value = message;
                updateSendTtsButtonState();
                void sendTtsMessage();
            });
            ttsShortcutListEl.appendChild(button);
        });

        updateSendTtsButtonState();
    }

    function renderOnlineAudioLibrary(selectedFilename = onlineTtsShortcutSelectEl.value) {
        onlineTtsShortcutSelectEl.innerHTML = '<option value="">选择一个手工音频</option>';
        onlineLibraryItems.forEach((item) => {
            const option = document.createElement('option');
            option.value = item.filename;
            option.textContent = item.displayName;
            option.selected = item.filename === selectedFilename;
            onlineTtsShortcutSelectEl.appendChild(option);
        });

        onlineTtsShortcutListEl.innerHTML = '';
        onlineLibraryItems.forEach((item) => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'quick-command-btn';
            button.textContent = item.displayName;
            button.title = '点击后直接播放这条手工音频';
            button.classList.toggle('active', item.filename === selectedFilename);
            button.addEventListener('click', () => {
                onlineTtsShortcutSelectEl.value = item.filename;
                renderOnlineAudioLibrary(item.filename);
                void playLibraryAudio(item.filename);
            });
            onlineTtsShortcutListEl.appendChild(button);
        });

        updateSendOnlineTtsButtonState();
    }

    function addCurrentTtsShortcut() {
        const message = ttsInputEl.value.trim();
        if (message.length <= 0 || ttsShortcutMessages.includes(message)) {
            updateSendTtsButtonState();
            return;
        }

        ttsShortcutMessages = [...ttsShortcutMessages, message];
        saveTtsShortcuts();
        ttsShortcutSelectEl.value = message;
        renderTtsShortcuts(message);
        writeLog(`已加入快捷语音：${message}`);
    }

    function deleteSelectedTtsShortcut() {
        const message = ttsShortcutSelectEl.value;
        if (!message) {
            updateSendTtsButtonState();
            return;
        }

        ttsShortcutMessages = ttsShortcutMessages.filter(item => item !== message);
        saveTtsShortcuts();
        ttsShortcutSelectEl.value = '';
        renderTtsShortcuts('');
        writeLog(`已删除快捷语音：${message}`);
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

    async function refreshOnlineTtsConfig(silent = true) {
        try {
            const response = await fetch('/api/tts/online/config', {
                method: 'GET',
                cache: 'no-store'
            });
            const result = await response.json();
            const data = result.data || {};
            renderOnlineTtsVoiceOptions(data);
            if (!silent && data.activeAccountName) {
                writeLog(`在线语音配置已刷新，当前账号：${data.activeAccountName}，默认音色：${data.defaultVcn || 'xiaoyan'}。`);
            }
        } catch (error) {
            writeLog(`在线语音配置刷新失败：${error}`);
        }
    }

    async function refreshOnlineAudioLibrary(silent = true) {
        try {
            const response = await fetch('/api/tts/online/library', {
                method: 'GET',
                cache: 'no-store'
            });
            const result = await response.json();
            const data = Array.isArray(result.data) ? result.data : [];
            onlineLibraryItems = data
                .map((item) => ({
                    filename: String(item.filename || '').trim(),
                    displayName: String(item.displayName || item.filename || '').trim(),
                    audioUrl: String(item.audioUrl || '').trim()
                }))
                .filter((item) => item.filename.length > 0 && item.displayName.length > 0);
            renderOnlineAudioLibrary();
            if (!silent) {
                writeLog(`手工音频列表已刷新，当前共 ${onlineLibraryItems.length} 条。`);
            }
        } catch (error) {
            writeLog(`手工音频列表刷新失败：${error}`);
        }
    }

    async function switchAiMode(mode) {
        const buttons = Object.values(modeButtons);
        buttons.forEach(button => button.disabled = true);
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

    async function sendTtsMessage() {
        const message = ttsInputEl.value.trim();
        if (message.length <= 0) {
            updateSendTtsButtonState();
            return;
        }

        sendTtsBtn.disabled = true;
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
            ttsInputEl.value = '';
            updateSendTtsButtonState();
        } catch (error) {
            writeLog(`发送鸿蒙端 TTS 失败：${error}`);
        } finally {
            updateSendTtsButtonState();
        }
    }

    async function sendOnlineTtsMessage() {
        const message = onlineTtsInputEl.value.trim();
        if (message.length <= 0) {
            updateSendOnlineTtsButtonState();
            return;
        }

        sendOnlineTtsBtn.disabled = true;
        writeLog(`正在发送在线语音播报：${message}`);

        try {
            const response = await fetch('/api/ws/harmony/notify-online-tts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`发送在线语音失败：${result.message || '未知错误'}`);
                return;
            }

            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            writeLog(`在线语音发送完成，内容“${data.message || message}”，文件 ${data.filename || '未返回'}，音色 ${data.voiceName || 'xiaoyan'}，本次推送 ${Number(data.deliveredCount || 0)} 台设备。`);
            onlineTtsInputEl.value = '';
            updateSendOnlineTtsButtonState();
            void refreshOnlineAudioLibrary(true);
        } catch (error) {
            writeLog(`发送在线语音失败：${error}`);
        } finally {
            updateSendOnlineTtsButtonState();
        }
    }

    async function playLibraryAudio(filename) {
        const normalizedFilename = String(filename || '').trim();
        if (normalizedFilename.length <= 0) {
            return;
        }

        writeLog(`正在播放手工音频：${normalizedFilename}`);
        try {
            const response = await fetch('/api/ws/harmony/play-library-audio', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ filename: normalizedFilename })
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`播放手工音频失败：${result.message || '未知错误'}`);
                return;
            }

            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            writeLog(`手工音频播放完成，文件“${data.filename || normalizedFilename}”，本次推送 ${Number(data.deliveredCount || 0)} 台设备。`);
        } catch (error) {
            writeLog(`播放手工音频失败：${error}`);
        }
    }

    refreshBtn.addEventListener('click', async () => {
        await refreshDeviceStatus(false);
        await refreshAiMode(false);
        await refreshOnlineTtsConfig(false);
        await refreshOnlineAudioLibrary(false);
    });

    testBtn.addEventListener('click', testConnection);
    sendTtsBtn.addEventListener('click', sendTtsMessage);
    sendOnlineTtsBtn.addEventListener('click', sendOnlineTtsMessage);

    ttsInputEl.addEventListener('input', updateSendTtsButtonState);
    ttsInputEl.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            void sendTtsMessage();
        }
    });

    onlineTtsInputEl.addEventListener('input', updateSendOnlineTtsButtonState);
    onlineTtsInputEl.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            void sendOnlineTtsMessage();
        }
    });

    onlineTtsShortcutSelectEl.addEventListener('change', () => {
        const filename = onlineTtsShortcutSelectEl.value;
        renderOnlineAudioLibrary(filename);
        if (filename) {
            void playLibraryAudio(filename);
        }
    });

    ttsShortcutSelectEl.addEventListener('change', () => {
        const message = ttsShortcutSelectEl.value;
        if (message) {
            ttsInputEl.value = message;
        }
        renderTtsShortcuts(message);
        updateSendTtsButtonState();
    });

    addTtsShortcutBtn.addEventListener('click', addCurrentTtsShortcut);
    deleteTtsShortcutBtn.addEventListener('click', deleteSelectedTtsShortcut);

    modeButtons.mode1.addEventListener('click', () => switchAiMode('mode1'));
    modeButtons.mode2.addEventListener('click', () => switchAiMode('mode2'));
    modeButtons.mode3.addEventListener('click', () => switchAiMode('mode3'));

    renderTtsShortcuts();
    renderOnlineAudioLibrary();
    updateSendTtsButtonState();
    updateSendOnlineTtsButtonState();
    refreshDeviceStatus(false);
    refreshAiMode(false);
    refreshOnlineTtsConfig(false);
    refreshOnlineAudioLibrary(false);

    window.setInterval(() => {
        refreshDeviceStatus(true);
        refreshAiMode(true);
        refreshOnlineTtsConfig(true);
        refreshOnlineAudioLibrary(true);
    }, 5000);
</script>
</body>
</html>"""
