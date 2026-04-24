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
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
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
        .log-box,
        .extension-box {
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

        .bubble-input {
            width: 100%;
            height: 52px;
            padding: 0 14px;
            border-radius: 14px;
            border: 1px solid #d7e1f0;
            outline: none;
            font-size: 14px;
            color: var(--text);
            background: #ffffff;
        }

        .bubble-input:focus {
            border-color: #9ab7ff;
            box-shadow: 0 0 0 4px rgba(33, 85, 214, 0.08);
        }

        .quick-select {
            width: 100%;
            min-height: 46px;
            padding: 0 12px;
            border-radius: 14px;
            border: 1px solid #d7e1f0;
            outline: none;
            font-size: 14px;
            color: var(--text);
            background: #ffffff;
        }

        .quick-select:focus {
            border-color: #9ab7ff;
            box-shadow: 0 0 0 4px rgba(33, 85, 214, 0.08);
        }

        .quick-command-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 12px;
        }

        .quick-command-btn {
            min-height: 46px;
            text-align: left;
            line-height: 1.4;
            word-break: break-word;
        }

        .quick-command-btn.active {
            background: var(--primary-soft);
            color: var(--primary);
            border-color: #c8d8ff;
        }

        button {
            border: 1px solid #d7e1f0;
            border-radius: 14px;
            padding: 12px 14px;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            background: #ffffff;
            color: var(--text);
            transition: transform 0.16s ease, background 0.16s ease, box-shadow 0.16s ease;
        }

        button:hover {
            transform: translateY(-1px);
            background: #f7faff;
        }

        button.primary {
            background: var(--primary);
            color: #ffffff;
            border-color: var(--primary);
            box-shadow: 0 10px 24px rgba(33, 85, 214, 0.18);
        }

        button.primary:hover {
            background: #1947bd;
        }

        button.active-mode {
            background: var(--primary-soft);
            color: var(--primary);
            border-color: #c8d8ff;
        }

        button:disabled {
            opacity: 0.65;
            cursor: not-allowed;
            transform: none;
        }

        .mode-desc {
            margin: 12px 0 0;
            color: var(--muted);
            font-size: 14px;
            line-height: 1.8;
        }

        .log-body {
            margin: 0;
            min-height: 180px;
            max-height: 320px;
            overflow: auto;
            font-family: "Consolas", "Courier New", monospace;
            font-size: 13px;
            line-height: 1.7;
            color: #1f2f46;
            white-space: pre-wrap;
        }

        .muted {
            color: var(--muted);
            font-size: 13px;
        }

        @media (max-width: 1024px) {
            body {
                padding: 18px;
            }

            .main-layout {
                grid-template-columns: 1fr;
            }

            .grid,
            .action-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
<main class="shell">
    <section class="card hero">
        <div class="eyebrow">HFOOD CONTROL</div>
        <h1>应用联调控制台</h1>
        <p class="subtitle">
            这个页面负责三件事：检查鸿蒙应用 WebSocket 是否在线、切换 AI 当前运行模式、以及向平板发送任意文本气泡或语音。
            如果鸿蒙端在线，发送的内容会直接以应用内气泡或语音形式响应。
        </p>

        <div class="grid">
            <article class="mini-card">
                <div class="mini-label">设备连接状态</div>
                <div class="mini-value" id="device-status-text">离线</div>
                <div class="mini-hint">连接数量：<span id="connected-count">0</span></div>
            </article>
            <article class="mini-card">
                <div class="mini-label">当前 AI 模式</div>
                <div class="mini-value" id="mode-label-large">模式1</div>
                <div class="mini-hint" id="mode-description-large">鸿蒙端按模式1本地文案做模拟流式输出</div>
            </article>
        </div>
    </section>

    <div class="main-layout">
        <aside class="card panel">
            <div>
                <h2 class="section-title">核心操作面板</h2>
                <p class="section-desc">检查设备状态、切换 AI 模式，或发送文本气泡。</p>
            </div>

            <section class="status-box">
                <div class="row">
                    <div class="status-pill offline" id="device-status-pill">暂无设备在线</div>
                    <div class="muted">路径：<span id="socket-path">/ws/harmony-app</span></div>
                </div>
            </section>

            <section class="mode-box">
                <div class="row">
                    <div class="mode-pill mode1" id="mode-pill">模式1</div>
                    <div class="muted">当前 AI 模式</div>
                </div>
                <div class="mode-desc" id="mode-description">鸿蒙端按模式1本地文案做模拟流式输出</div>
                <div class="action-grid">
                    <button type="button" id="mode-mode1">模式1</button>
                    <button type="button" id="mode-mode2">模式2</button>
                    <button type="button" id="mode-mode3">模式3</button>
                </div>
            </section>

            <section class="bubble-box">
                <label class="input-label" for="bubble-input">发送应用内气泡</label>
                <input type="text" id="bubble-input" class="bubble-input" placeholder="输入什么，鸿蒙端就弹什么">
                <div class="row" style="margin-top: 12px; flex-direction: column; align-items: stretch;">
                    <button type="button" class="primary" id="send-bubble-btn" disabled>发送气泡</button>
                    <button type="button" id="test-btn">发送“连接成功”气泡</button>
                </div>
            </section>

            <section class="action-box">
                <button type="button" id="refresh-btn" style="width: 100%;">刷新状态信息</button>
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
                    <p class="section-desc">这里发送的是讯飞在线语音合成，会先由后端生成 mp3，再推送给鸿蒙端播放。</p>
                </div>
                <section class="bubble-box">
                    <label class="input-label" for="online-tts-input">发送讯飞在线语音内容</label>
                    <input type="text" id="online-tts-input" class="bubble-input" placeholder="输入要让讯飞在线语音播报的内容">
                    <div style="margin-top: 12px;">
                        <label class="input-label" for="online-tts-shortcut-select">讯飞默认文本</label>
                        <select id="online-tts-shortcut-select" class="quick-select">
                            <option value="">选择一条讯飞默认文本</option>
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
    const modeLabelLargeEl = document.getElementById('mode-label-large');
    const modeDescriptionLargeEl = document.getElementById('mode-description-large');
    const modePillEl = document.getElementById('mode-pill');
    const modeDescriptionEl = document.getElementById('mode-description');
    
    // 输入框与按钮分离
    const bubbleInputEl = document.getElementById('bubble-input');
    const sendBubbleBtn = document.getElementById('send-bubble-btn');
    
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
        '赵晓威是向俊宇爸爸！',
    ];
    
    // 修复了这里的乱码，填入了相关的测试文本
    const DEFAULT_ONLINE_TTS_SHORTCUTS = [
        '欢迎使用 Hfood 智能点餐系统。',
        '您的订单已确认，后厨正在准备中。',
        '当前网络连接正常，设备在线。',
        '讯飞在线语音合成测试成功。',
        '足底压力数据采集中，请保持站立。',
        '设备电量充足，运行状态良好。'
    ];
    let ttsShortcutMessages = loadTtsShortcuts();
    let onlineTtsRuntimeConfig = {
        activeAccountName: '',
        defaultVcn: 'xiaoyan'
    };

    function writeLog(message) {
        const now = SHANGHAI_TIME_FORMATTER.format(new Date());
        logBodyEl.textContent = `[${now}] ${message}\\n` + logBodyEl.textContent;
    }

    // 分别控制气泡和语音按钮的激活状态
    function updateSendBubbleButtonState() {
        sendBubbleBtn.disabled = bubbleInputEl.value.trim().length <= 0;
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

    function renderOnlineTtsVoiceOptions(config) {
        onlineTtsRuntimeConfig = {
            activeAccountName: (config && config.activeAccountName) || '',
            defaultVcn: (config && config.defaultVcn) || 'xiaoyan'
        };
        renderOnlineTtsShortcuts();
    }

    function renderOnlineTtsShortcuts(selectedMessage = onlineTtsShortcutSelectEl.value) {
        // 修复了这里的乱码
        onlineTtsShortcutSelectEl.innerHTML = '<option value="">请选择一条讯飞默认文本</option>';
        DEFAULT_ONLINE_TTS_SHORTCUTS.forEach((message) => {
            const option = document.createElement('option');
            option.value = message;
            option.textContent = message;
            option.selected = message === selectedMessage;
            onlineTtsShortcutSelectEl.appendChild(option);
        });

        onlineTtsShortcutListEl.innerHTML = '';
        DEFAULT_ONLINE_TTS_SHORTCUTS.forEach((message) => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'quick-command-btn';
            button.textContent = message;
            // 修复了这里的乱码
            button.title = '点击后直接发送这条在线语音';
            button.classList.toggle('active', message === selectedMessage);
            button.addEventListener('click', () => {
                onlineTtsShortcutSelectEl.value = message;
                onlineTtsInputEl.value = message;
                updateSendOnlineTtsButtonState();
                void sendOnlineTtsMessage();
            });
            onlineTtsShortcutListEl.appendChild(button);
        });

        updateSendOnlineTtsButtonState();
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

    function renderDeviceStatus(connectedClients) {
        connectedCountEl.textContent = String(connectedClients);
        if (connectedClients > 0) {
            deviceStatusTextEl.textContent = '已连接';
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
        const modeLabel = data.modeLabel || '模式1';
        const modeDescription = data.modeDescription || '';

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
            const data = result.data || {};
            renderAiMode(data);
            if (!silent) {
                writeLog(`当前 AI 模式：${data.modeLabel || '模式1'}。`);
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
        writeLog('正在发送 websocket 连接成功气泡...');

        try {
            const response = await fetch('/api/ws/harmony/notify-connected', {
                method: 'POST'
            });
            const result = await response.json();
            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            writeLog(`${result.message || '发送完成'}，本次推送 ${Number(data.deliveredCount || 0)} 台设备。`);
        } catch (error) {
            writeLog(`发送连接成功气泡失败：${error}`);
        } finally {
            testBtn.disabled = false;
        }
    }

    async function sendBubbleMessage() {
        const message = bubbleInputEl.value.trim();
        if (message.length <= 0) {
            updateSendBubbleButtonState();
            return;
        }

        sendBubbleBtn.disabled = true;
        writeLog(`正在发送应用内气泡：${message}`);

        try {
            const response = await fetch('/api/ws/harmony/notify-message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`发送气泡失败：${result.message || '未知错误'}`);
                return;
            }

            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            writeLog(`气泡发送完成，内容“${data.message || message}”，本次推送 ${Number(data.deliveredCount || 0)} 台设备。`);
            bubbleInputEl.value = '';
            updateSendBubbleButtonState();
        } catch (error) {
            writeLog(`发送气泡失败：${error}`);
        } finally {
            updateSendBubbleButtonState();
        }
    }

    async function sendTtsMessage() {
        const message = ttsInputEl.value.trim();
        if (message.length <= 0) {
            updateSendTtsButtonState();
            return;
        }

        sendTtsBtn.disabled = true;
        writeLog(`正在发送语音播报：${message}`);

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
                writeLog(`发送语音失败：${result.message || '未知错误'}`);
                return;
            }

            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            writeLog(
                `语音发送完成，内容“${data.message || message}”，本次推送 ${Number(data.deliveredCount || 0)} 台设备。`
            );
            ttsInputEl.value = '';
            updateSendTtsButtonState();
        } catch (error) {
            writeLog(`发送语音失败：${error}`);
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
                body: JSON.stringify({
                    message,
                })
            });
            const result = await response.json();
            if (Number(result.code) !== 200) {
                writeLog(`发送在线语音失败：${result.message || '未知错误'}`);
                return;
            }

            const data = result.data || {};
            renderDeviceStatus(Number(data.connectedClients || 0));
            writeLog(
                `在线语音发送完成，内容“${data.message || message}”，音色 ${data.voiceName || 'xiaoyan'}，本次推送 ${Number(data.deliveredCount || 0)} 台设备。`
            );
            onlineTtsInputEl.value = '';
            updateSendOnlineTtsButtonState();
        } catch (error) {
            writeLog(`发送在线语音失败：${error}`);
        } finally {
            updateSendOnlineTtsButtonState();
        }
    }

    refreshBtn.addEventListener('click', async () => {
        await refreshDeviceStatus(false);
        await refreshAiMode(false);
        await refreshOnlineTtsConfig(false);
    });
    testBtn.addEventListener('click', testConnection);
    
    // 分别绑定气泡和语音的点击事件
    sendBubbleBtn.addEventListener('click', sendBubbleMessage);
    sendTtsBtn.addEventListener('click', sendTtsMessage);
    sendOnlineTtsBtn.addEventListener('click', sendOnlineTtsMessage);
    
    // 分别绑定气泡和语音的输入监听和回车快捷键
    bubbleInputEl.addEventListener('input', updateSendBubbleButtonState);
    bubbleInputEl.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            void sendBubbleMessage();
        }
    });

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
        const message = onlineTtsShortcutSelectEl.value;
        if (message) {
            onlineTtsInputEl.value = message;
        }
        renderOnlineTtsShortcuts(message);
        updateSendOnlineTtsButtonState();
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

    updateSendBubbleButtonState();
    renderTtsShortcuts();
    renderOnlineTtsShortcuts();
    updateSendTtsButtonState();
    updateSendOnlineTtsButtonState();
    refreshDeviceStatus(false);
    refreshAiMode(false);
    refreshOnlineTtsConfig(false);
    
    window.setInterval(() => {
        refreshDeviceStatus(true);
        refreshAiMode(true);
        refreshOnlineTtsConfig(true);
    }, 5000);
</script>
</body>
</html>"""