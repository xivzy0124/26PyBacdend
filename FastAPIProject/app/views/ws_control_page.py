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
            max-width: 1100px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1.1fr 0.9fr;
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
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
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
            font-size: 22px;
        }

        .section-desc {
            margin: 8px 0 0;
            color: var(--muted);
            font-size: 14px;
            line-height: 1.8;
        }

        .status-box,
        .mode-box,
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
            cursor: wait;
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

        @media (max-width: 920px) {
            body {
                padding: 18px;
            }

            .shell {
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
            这个页面负责两件事：一是检查鸿蒙应用 websocket 是否在线，二是切换 AI 卡片当前运行模式。
            切换成功后，鸿蒙 AI 页面右上角会实时更新为模式1、模式2或模式3，点击“开启分析”会按当前模式播放本地文案。
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

    <aside class="card panel">
        <div>
            <h2 class="section-title">控制操作</h2>
            <p class="section-desc">先看设备是否在线，再切 AI 模式，最后可以点按钮让鸿蒙应用弹出 websocket 连接成功气泡。</p>
        </div>

        <section class="status-box">
            <div class="row">
                <div class="status-pill offline" id="device-status-pill">暂无设备在线</div>
                <div class="muted">WebSocket 路径：<span id="socket-path">/ws/harmony-app</span></div>
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

        <section class="action-box">
            <div class="row">
                <button type="button" class="primary" id="test-btn">发送"连接成功"气泡</button>
                <button type="button" id="refresh-btn">刷新状态</button>
            </div>
        </section>

        <section class="log-box">
            <pre class="log-body" id="log-body">系统已就绪，等待操作...</pre>
        </section>
    </aside>
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

    function writeLog(message) {
        const now = SHANGHAI_TIME_FORMATTER.format(new Date());
        logBodyEl.textContent = `[${now}] ${message}\\n` + logBodyEl.textContent;
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

    refreshBtn.addEventListener('click', async () => {
        await refreshDeviceStatus(false);
        await refreshAiMode(false);
    });
    testBtn.addEventListener('click', testConnection);
    modeButtons.mode1.addEventListener('click', () => switchAiMode('mode1'));
    modeButtons.mode2.addEventListener('click', () => switchAiMode('mode2'));
    modeButtons.mode3.addEventListener('click', () => switchAiMode('mode3'));

    refreshDeviceStatus(false);
    refreshAiMode(false);
    window.setInterval(() => {
        refreshDeviceStatus(true);
        refreshAiMode(true);
    }, 5000);
</script>
</body>
</html>
"""
