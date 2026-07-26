import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="3D Ball Shuffle Protocol",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
        div[data-testid="stAppViewContainer"] {padding: 0 !important;}
        div[data-testid="stVerticalBlock"] {gap: 0 !important;}
        body {background-color: #05060a;}
    </style>
    """,
    unsafe_allow_html=True,
)

game_html = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>3D Ball Shuffle Protocol</title>
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        -webkit-tap-highlight-color: transparent;
        user-select: none;
        -webkit-user-select: none;
    }

    html, body {
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background: #05060a;
        font-family: 'Segoe UI', 'Trebuchet MS', Arial, sans-serif;
    }

    #game-root {
        position: fixed;
        inset: 0;
        width: 100vw;
        height: 100vh;
        background: #05060a;
        overflow: hidden;
    }

    #game-canvas {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: block;
        touch-action: none;
    }

    /* ---------------- INTRO OVERLAY ---------------- */
    #intro-overlay {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: radial-gradient(ellipse at center, #101423 0%, #05060a 65%, #000000 100%);
        z-index: 50;
        transition: opacity 0.6s ease, visibility 0.6s ease;
        padding: 20px;
        overflow-y: auto;
    }

    #intro-overlay.hidden {
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
    }

    .neon-title {
        font-size: clamp(22px, 5.2vw, 46px);
        font-weight: 800;
        letter-spacing: 2px;
        text-align: center;
        color: #7dffe0;
        text-shadow:
            0 0 5px #35ffce,
            0 0 15px #21e0ff,
            0 0 30px #0fa3ff,
            0 0 60px #0a6cff;
        margin-bottom: 6px;
        animation: pulseGlow 2.4s ease-in-out infinite;
    }

    .neon-sub {
        font-size: clamp(11px, 2vw, 15px);
        letter-spacing: 6px;
        color: #7799bb;
        text-transform: uppercase;
        margin-bottom: 34px;
        text-align: center;
    }

    @keyframes pulseGlow {
        0%, 100% {
            text-shadow:
                0 0 5px #35ffce,
                0 0 15px #21e0ff,
                0 0 30px #0fa3ff,
                0 0 60px #0a6cff;
        }
        50% {
            text-shadow:
                0 0 10px #35ffce,
                0 0 25px #21e0ff,
                0 0 45px #0fa3ff,
                0 0 90px #0a6cff;
        }
    }

    .section-label {
        color: #6fe3ff;
        font-size: clamp(11px, 1.8vw, 14px);
        letter-spacing: 3px;
        text-transform: uppercase;
        margin: 18px 0 12px 0;
        text-align: center;
        opacity: 0.85;
    }

    #difficulty-row {
        display: flex;
        gap: 14px;
        flex-wrap: wrap;
        justify-content: center;
        margin-bottom: 8px;
    }

    .diff-btn {
        position: relative;
        padding: 14px 30px;
        font-size: clamp(13px, 2vw, 16px);
        font-weight: 700;
        letter-spacing: 2px;
        color: #cfe8ff;
        background: linear-gradient(160deg, #131a2b 0%, #0a0e18 100%);
        border: 1.5px solid #294066;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.05), 0 4px 12px rgba(0,0,0,0.5);
    }

    .diff-btn:hover {
        border-color: #52e8ff;
        color: #ffffff;
        box-shadow: 0 0 14px rgba(82,232,255,0.45), inset 0 1px 0 rgba(255,255,255,0.08);
        transform: translateY(-2px);
    }

    .diff-btn.selected {
        border-color: #52ffb0;
        color: #eafff5;
        background: linear-gradient(160deg, #103224 0%, #081b14 100%);
        box-shadow: 0 0 20px rgba(82,255,176,0.55), inset 0 1px 0 rgba(255,255,255,0.08);
    }

    #cup-selector {
        display: flex;
        gap: 10px;
        justify-content: center;
        flex-wrap: wrap;
        margin-bottom: 10px;
    }

    .cup-slot {
        width: clamp(38px, 8vw, 54px);
        height: clamp(38px, 8vw, 54px);
        border-radius: 12px;
        border: 1.5px solid #2c3b52;
        background: linear-gradient(160deg, #101623 0%, #080b12 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: clamp(14px, 2.4vw, 18px);
        color: #8fb3d9;
        cursor: pointer;
        transition: all 0.18s ease;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
    }

    .cup-slot:hover {
        border-color: #52e8ff;
        color: #ffffff;
    }

    .cup-slot.selected {
        border-color: #17ffb4;
        background: linear-gradient(160deg, #0e3527 0%, #061c15 100%);
        color: #baffe9;
        box-shadow: 0 0 16px rgba(23,255,180,0.75), inset 0 0 10px rgba(23,255,180,0.25);
        transform: scale(1.08);
    }

    #start-descent-btn {
        margin-top: 30px;
        padding: 16px 46px;
        font-size: clamp(14px, 2.4vw, 18px);
        font-weight: 800;
        letter-spacing: 3px;
        color: #04140d;
        background: linear-gradient(160deg, #35ffce 0%, #12c98f 100%);
        border: none;
        border-radius: 40px;
        cursor: pointer;
        box-shadow: 0 0 25px rgba(53,255,206,0.55), 0 6px 18px rgba(0,0,0,0.6);
        transition: all 0.2s ease;
    }

    #start-descent-btn:disabled {
        opacity: 0.35;
        cursor: not-allowed;
        box-shadow: none;
    }

    #start-descent-btn:not(:disabled):hover {
        transform: translateY(-3px) scale(1.03);
        box-shadow: 0 0 35px rgba(53,255,206,0.8), 0 10px 22px rgba(0,0,0,0.6);
    }

    #start-descent-btn:not(:disabled):active {
        transform: translateY(0px) scale(0.98);
    }

    .hint-text {
        margin-top: 14px;
        color: #5c7590;
        font-size: clamp(10px, 1.6vw, 12px);
        letter-spacing: 1px;
        text-align: center;
    }

    /* ---------------- HUD MENU ---------------- */
    #hud-menu-btn {
        position: absolute;
        top: 16px;
        left: 16px;
        width: 42px;
        height: 42px;
        border-radius: 50%;
        background: rgba(8,12,20,0.65);
        border: 1.5px solid #2c5570;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 40;
        box-shadow: 0 0 14px rgba(33,224,255,0.35);
        transition: all 0.2s ease;
        backdrop-filter: blur(4px);
    }

    #hud-menu-btn:hover {
        border-color: #52e8ff;
        box-shadow: 0 0 20px rgba(82,232,255,0.65);
    }

    #hud-menu-btn span {
        display: block;
        width: 18px;
        height: 2px;
        background: #6fe3ff;
        margin: 2.5px 0;
        border-radius: 2px;
        box-shadow: 0 0 6px rgba(111,227,255,0.8);
    }

    .hidden-el {
        display: none !important;
    }

    #top-right-hud {
        position: absolute;
        top: 16px;
        right: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
        z-index: 40;
    }

    #mute-btn {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: rgba(8,12,20,0.65);
        border: 1.5px solid #2c5570;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 16px;
        box-shadow: 0 0 14px rgba(33,224,255,0.25);
        backdrop-filter: blur(4px);
        transition: all 0.2s ease;
        flex-shrink: 0;
    }

    #mute-btn:hover {
        border-color: #52e8ff;
        box-shadow: 0 0 20px rgba(82,232,255,0.55);
    }

    #mute-btn.muted {
        color: #ff6a6a;
        border-color: #6a2c33;
    }

    #control-pane {
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        width: min(280px, 78vw);
        background: linear-gradient(160deg, rgba(10,14,24,0.97) 0%, rgba(5,7,12,0.98) 100%);
        border-right: 1.5px solid #23384f;
        z-index: 45;
        transform: translateX(-105%);
        transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1);
        padding: 70px 22px 22px 22px;
        box-shadow: 8px 0 30px rgba(0,0,0,0.6);
    }

    #control-pane.open {
        transform: translateX(0);
    }

    .control-pane-title {
        color: #7dffe0;
        font-size: 14px;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 22px;
        text-shadow: 0 0 10px rgba(53,255,206,0.5);
    }

    .control-link {
        display: block;
        width: 100%;
        text-align: left;
        padding: 14px 16px;
        margin-bottom: 12px;
        background: rgba(255,255,255,0.03);
        border: 1px solid #23384f;
        border-radius: 8px;
        color: #cfe8ff;
        font-size: 12.5px;
        letter-spacing: 1.5px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .control-link:hover {
        border-color: #52e8ff;
        background: rgba(82,232,255,0.08);
        color: #ffffff;
    }

    .control-status {
        margin-top: 26px;
        color: #5c7590;
        font-size: 11px;
        letter-spacing: 1px;
        line-height: 1.7;
    }

    #pane-backdrop {
        position: absolute;
        inset: 0;
        background: rgba(0,0,0,0.35);
        z-index: 44;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
    }

    #pane-backdrop.open {
        opacity: 1;
        pointer-events: auto;
    }

    /* ---------------- HUD MESSAGE ---------------- */
    #hud-message {
        position: absolute;
        top: 18px;
        left: 50%;
        transform: translateX(-50%);
        color: #eafcff;
        font-size: clamp(12px, 2.4vw, 17px);
        font-weight: 700;
        letter-spacing: 2px;
        text-align: center;
        padding: 10px 22px;
        border-radius: 30px;
        background: rgba(6,10,18,0.55);
        border: 1px solid #2c5570;
        text-shadow: 0 0 10px rgba(111,227,255,0.7);
        box-shadow: 0 0 16px rgba(33,224,255,0.25);
        z-index: 30;
        opacity: 0;
        transition: opacity 0.4s ease;
        pointer-events: none;
        max-width: 90%;
        backdrop-filter: blur(3px);
    }

    #hud-message.visible {
        opacity: 1;
    }

    #score-pill {
        padding: 9px 18px;
        border-radius: 20px;
        background: rgba(8,12,20,0.65);
        border: 1.5px solid #2c5570;
        color: #9fe8ff;
        font-size: clamp(11px, 1.8vw, 13px);
        font-weight: 700;
        letter-spacing: 1.5px;
        z-index: 40;
        box-shadow: 0 0 14px rgba(33,224,255,0.25);
        backdrop-filter: blur(4px);
    }

    /* ---------------- RESULT OVERLAY ---------------- */
    #result-overlay {
        position: absolute;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        z-index: 60;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.5s ease;
        background: rgba(0,0,0,0.55);
        backdrop-filter: blur(2px);
    }

    #result-overlay.visible {
        opacity: 1;
        pointer-events: auto;
    }

    #result-title {
        font-size: clamp(28px, 7vw, 60px);
        font-weight: 900;
        letter-spacing: 3px;
        text-align: center;
        margin-bottom: 26px;
        padding: 0 16px;
    }

    #result-title.win {
        color: #ffd85c;
        text-shadow: 0 0 20px #ffb400, 0 0 50px #ff9500, 0 0 90px #ff7a00;
        animation: winPulse 1s ease-in-out infinite;
    }

    #result-title.lose {
        color: #ff5c6a;
        text-shadow: 0 0 20px #ff1e3a, 0 0 50px #d3001f, 0 0 90px #8f0015;
        animation: losePulse 1s ease-in-out infinite;
    }

    @keyframes winPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.06); }
    }

    @keyframes losePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(0.96); }
    }

    #result-again-btn {
        padding: 14px 40px;
        font-size: clamp(13px, 2.2vw, 16px);
        font-weight: 800;
        letter-spacing: 2px;
        color: #04140d;
        background: linear-gradient(160deg, #35ffce 0%, #12c98f 100%);
        border: none;
        border-radius: 40px;
        cursor: pointer;
        box-shadow: 0 0 25px rgba(53,255,206,0.55);
    }

    #result-again-btn:hover {
        transform: translateY(-2px);
    }
</style>
</head>
<body>

<div id="game-root">
    <canvas id="game-canvas"></canvas>

    <div id="hud-menu-btn" class="hidden-el">
        <span></span><span></span><span></span>
    </div>

    <div id="top-right-hud" class="hidden-el">
        <div id="mute-btn" title="Toggle Music">&#128266;</div>
        <div id="score-pill">ROUND 0 &nbsp;|&nbsp; WINS 0</div>
    </div>

    <div id="hud-message"></div>

    <div id="pane-backdrop"></div>
    <div id="control-pane">
        <div class="control-pane-title">SYSTEM CONTROL CONSOLE</div>
        <button class="control-link" id="btn-return-chassis">&#8592; RETURN TO MENU</button>
        <button class="control-link" id="btn-recalibrate">&#9881; RE-CALIBRATE SETTINGS</button>
        <div class="control-status" id="pane-status-text">DIFFICULTY: EASY<br>CUPS: 3<br>STATE: IDLE</div>
    </div>

    <div id="result-overlay">
        <div id="result-title"></div>
        <button id="result-again-btn">SHUFFLE AGAIN</button>
    </div>

    <div id="intro-overlay">
        <div class="neon-title">&#127760; 3D BALL SHUFFLE PROTOCOL</div>
        <div class="neon-sub">TRACK THE ORB &middot; TRUST NOTHING</div>

        <div class="section-label">SELECT DIFFICULTY</div>
        <div id="difficulty-row">
            <button class="diff-btn" data-diff="easy">EASY</button>
            <button class="diff-btn" data-diff="medium">MEDIUM</button>
            <button class="diff-btn" data-diff="hard">HARD</button>
        </div>

        <div class="section-label">SELECT CUP COUNT</div>
        <div id="cup-selector">
            <div class="cup-slot" data-count="0">0</div>
            <div class="cup-slot" data-count="1">1</div>
            <div class="cup-slot" data-count="2">2</div>
            <div class="cup-slot" data-count="3">3</div>
            <div class="cup-slot" data-count="4">4</div>
            <div class="cup-slot" data-count="5">5</div>
        </div>

        <button id="start-descent-btn" disabled>START DESCENT</button>
        <div class="hint-text">CHOOSE A DIFFICULTY AND A CUP COUNT TO BEGIN</div>
    </div>
</div>

<script>
(function () {
    "use strict";

    /* ======================================================
       DOM REFERENCES
       ====================================================== */
    var canvas = document.getElementById("game-canvas");
    var ctx = canvas.getContext("2d");
    var introOverlay = document.getElementById("intro-overlay");
    var difficultyRow = document.getElementById("difficulty-row");
    var cupSelector = document.getElementById("cup-selector");
    var startBtn = document.getElementById("start-descent-btn");
    var hudMenuBtn = document.getElementById("hud-menu-btn");
    var controlPane = document.getElementById("control-pane");
    var paneBackdrop = document.getElementById("pane-backdrop");
    var btnReturnChassis = document.getElementById("btn-return-chassis");
    var btnRecalibrate = document.getElementById("btn-recalibrate");
    var paneStatusText = document.getElementById("pane-status-text");
    var hudMessage = document.getElementById("hud-message");
    var topRightHud = document.getElementById("top-right-hud");
    var muteBtn = document.getElementById("mute-btn");
    var scorePill = document.getElementById("score-pill");
    var resultOverlay = document.getElementById("result-overlay");
    var resultTitle = document.getElementById("result-title");
    var resultAgainBtn = document.getElementById("result-again-btn");

    /* ======================================================
       GLOBAL GAME STATE
       ====================================================== */
    var STATE = {
        phase: "intro",          // intro | dropping | shuffling | guessing | revealing | result
        difficulty: null,        // easy | medium | hard
        cupCount: null,          // 0 - 5
        paused: false,
        round: 0,
        wins: 0,
        dpr: Math.max(1, window.devicePixelRatio || 1),
        width: 0,
        height: 0
    };

    var DIFFICULTY_PROFILES = {
        easy:   { swaps: 5,  swapDuration: 900, lift: 46, label: "EASY" },
        medium: { swaps: 9,  swapDuration: 560, lift: 60, label: "MEDIUM" },
        hard:   { swaps: 15, swapDuration: 300, lift: 78, label: "HARD" }
    };

    /* ======================================================
       CUP / BALL SCENE STATE
       ====================================================== */
    var scene = {
        slotX: [],           // canonical x-position for each slot index
        tableY: 0,
        cupBaseW: 0,
        cupBaseH: 0,
        ballRadius: 0,
        cupAtSlot: [],        // cupAtSlot[slotIndex] = cupId
        cupCurrentX: [],       // indexed by cupId -> current x
        cupLift: [],           // indexed by cupId -> current vertical lift (0 = resting)
        cupRevealLift: [],     // indexed by cupId -> vertical reveal offset (0 = down)
        ballSlot: -1,          // which slot currently holds the ball (ground truth)
        swapQueue: [],
        activeSwap: null,
        selectedGuessSlot: -1,
        revealStartTime: 0,
        revealDone: false,
        idleBobPhase: 0
    };

    var rafId = null;
    var lastFrameTime = 0;

    /* ======================================================
       CANVAS SIZING
       ====================================================== */
    function resizeCanvas() {
        STATE.dpr = Math.max(1, window.devicePixelRatio || 1);
        var w = window.innerWidth;
        var h = window.innerHeight;
        canvas.style.width = w + "px";
        canvas.style.height = h + "px";
        canvas.width = Math.floor(w * STATE.dpr);
        canvas.height = Math.floor(h * STATE.dpr);
        ctx.setTransform(STATE.dpr, 0, 0, STATE.dpr, 0, 0);
        STATE.width = w;
        STATE.height = h;
        recomputeLayout();
    }

    function recomputeLayout() {
        var w = STATE.width;
        var h = STATE.height;
        scene.tableY = h * 0.62;
        scene.cupBaseW = Math.max(46, Math.min(120, w / 8));
        scene.cupBaseH = scene.cupBaseW * 1.35;
        scene.ballRadius = scene.cupBaseW * 0.24;

        var count = STATE.cupCount === null ? 3 : STATE.cupCount;
        scene.slotX = [];
        if (count > 0) {
            var usableWidth = w * 0.82;
            var startX = (w - usableWidth) / 2;
            var spacing = count > 1 ? usableWidth / (count - 1) : 0;
            for (var i = 0; i < count; i++) {
                var x = count > 1 ? (startX + spacing * i) : (w / 2);
                scene.slotX.push(x);
            }
        }

        if (scene.cupCurrentX.length === scene.slotX.length) {
            for (var j = 0; j < scene.cupAtSlot.length; j++) {
                var cid = scene.cupAtSlot[j];
                if (cid !== undefined && scene.slotX[j] !== undefined) {
                    scene.cupCurrentX[cid] = scene.slotX[j];
                }
            }
        }
    }

    window.addEventListener("resize", resizeCanvas);
    window.addEventListener("orientationchange", function () {
        setTimeout(resizeCanvas, 200);
    });

    /* ======================================================
       DRAWING: BACKGROUND (LUXURY CASINO FELT + WOOD FRAME)
       ====================================================== */
    function drawBackground() {
        var w = STATE.width;
        var h = STATE.height;

        var woodGrad = ctx.createLinearGradient(0, 0, 0, h);
        woodGrad.addColorStop(0, "#1c1006");
        woodGrad.addColorStop(0.15, "#2b1708");
        woodGrad.addColorStop(0.5, "#170d05");
        woodGrad.addColorStop(0.85, "#2b1708");
        woodGrad.addColorStop(1, "#100904");
        ctx.fillStyle = woodGrad;
        ctx.fillRect(0, 0, w, h);

        ctx.save();
        ctx.globalAlpha = 0.08;
        ctx.strokeStyle = "#000000";
        for (var gy = -h; gy < h * 1.5; gy += 6) {
            ctx.beginPath();
            var wobble = Math.sin(gy * 0.04) * 14;
            ctx.moveTo(-20, gy + wobble);
            ctx.bezierCurveTo(w * 0.3, gy + wobble + 10, w * 0.7, gy + wobble - 10, w + 20, gy + wobble);
            ctx.stroke();
        }
        ctx.restore();

        var feltCenterX = w / 2;
        var feltCenterY = scene.tableY + scene.cupBaseH * 0.2;
        var feltRadius = Math.max(w, h) * 0.75;
        var feltGrad = ctx.createRadialGradient(
            feltCenterX, feltCenterY, feltRadius * 0.05,
            feltCenterX, feltCenterY, feltRadius
        );
        feltGrad.addColorStop(0, "#0f3d2c");
        feltGrad.addColorStop(0.45, "#0a2a1e");
        feltGrad.addColorStop(0.8, "#061a13");
        feltGrad.addColorStop(1, "#04100c");

        var matTop = h * 0.22;
        var matBottom = h;
        ctx.save();
        ctx.beginPath();
        ctx.rect(0, matTop, w, matBottom - matTop);
        ctx.clip();
        ctx.fillStyle = feltGrad;
        ctx.fillRect(0, matTop, w, matBottom - matTop);

        ctx.globalAlpha = 0.05;
        ctx.fillStyle = "#ffffff";
        for (var i = 0; i < 900; i++) {
            var rx = Math.random() * w;
            var ry = matTop + Math.random() * (matBottom - matTop);
            ctx.fillRect(rx, ry, 1, 1);
        }
        ctx.restore();

        var edgeGrad = ctx.createLinearGradient(0, matTop - 14, 0, matTop + 30);
        edgeGrad.addColorStop(0, "rgba(0,0,0,0.65)");
        edgeGrad.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = edgeGrad;
        ctx.fillRect(0, matTop - 14, w, 44);

        var vignette = ctx.createRadialGradient(
            w / 2, h / 2, Math.min(w, h) * 0.2,
            w / 2, h / 2, Math.max(w, h) * 0.8
        );
        vignette.addColorStop(0, "rgba(0,0,0,0)");
        vignette.addColorStop(1, "rgba(0,0,0,0.55)");
        ctx.fillStyle = vignette;
        ctx.fillRect(0, 0, w, h);
    }

    /* ======================================================
       DRAWING: SHADOW BENEATH OBJECTS
       ====================================================== */
    function drawShadow(x, y, radiusX, radiusY, alpha) {
        ctx.save();
        ctx.beginPath();
        ctx.ellipse(x, y, radiusX, radiusY, 0, 0, Math.PI * 2);
        var shadowGrad = ctx.createRadialGradient(x, y, 0, x, y, radiusX);
        shadowGrad.addColorStop(0, "rgba(0,0,0," + alpha + ")");
        shadowGrad.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = shadowGrad;
        ctx.fill();
        ctx.restore();
    }

    /* ======================================================
       DRAWING: 3D BALL (SPHERE WITH SPECULAR HIGHLIGHT)
       ====================================================== */
    function drawBall(x, y, radius) {
        drawShadow(x, y + radius * 0.35, radius * 1.5, radius * 0.55, 0.5);

        var sphereGrad = ctx.createRadialGradient(
            x - radius * 0.35, y - radius * 0.4, radius * 0.08,
            x, y, radius * 1.15
        );
        sphereGrad.addColorStop(0, "#fff6d8");
        sphereGrad.addColorStop(0.25, "#ffdf6b");
        sphereGrad.addColorStop(0.55, "#e8a72a");
        sphereGrad.addColorStop(0.8, "#a4650f");
        sphereGrad.addColorStop(1, "#5c3306");

        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fillStyle = sphereGrad;
        ctx.fill();

        ctx.beginPath();
        ctx.arc(x - radius * 0.38, y - radius * 0.42, radius * 0.26, 0, Math.PI * 2);
        var specGrad = ctx.createRadialGradient(
            x - radius * 0.38, y - radius * 0.42, 0,
            x - radius * 0.38, y - radius * 0.42, radius * 0.26
        );
        specGrad.addColorStop(0, "rgba(255,255,255,0.95)");
        specGrad.addColorStop(1, "rgba(255,255,255,0)");
        ctx.fillStyle = specGrad;
        ctx.fill();

        ctx.beginPath();
        ctx.arc(x + radius * 0.3, y + radius * 0.32, radius * 0.1, 0, Math.PI * 2);
        var specGrad2 = ctx.createRadialGradient(
            x + radius * 0.3, y + radius * 0.32, 0,
            x + radius * 0.3, y + radius * 0.32, radius * 0.1
        );
        specGrad2.addColorStop(0, "rgba(255,255,255,0.5)");
        specGrad2.addColorStop(1, "rgba(255,255,255,0)");
        ctx.fillStyle = specGrad2;
        ctx.fill();
    }

    /* ======================================================
       DRAWING: 3D CUP (CONE / CYLINDER WITH RIM + SHADING)
       ====================================================== */
    function drawCup(x, y, liftY, w, h, highlightSelected) {
        var topY = y - h - liftY;
        var bottomY = y - liftY;
        var topRadiusX = w * 0.5;
        var topRadiusY = w * 0.19;
        var bottomRadiusX = w * 0.66;
        var bottomRadiusY = w * 0.22;

        var shadowAlpha = Math.max(0.12, 0.5 - liftY * 0.004);
        drawShadow(x, y + bottomRadiusY * 0.4, bottomRadiusX * 1.25, bottomRadiusY * 0.9, shadowAlpha);

        ctx.save();

        ctx.beginPath();
        ctx.moveTo(x - bottomRadiusX, bottomY);
        ctx.lineTo(x - topRadiusX, topY);
        ctx.ellipse(x, topY, topRadiusX, topRadiusY, 0, Math.PI, 0, false);
        ctx.lineTo(x + bottomRadiusX, bottomY);
        ctx.ellipse(x, bottomY, bottomRadiusX, bottomRadiusY, 0, 0, Math.PI, false);
        ctx.closePath();

        var bodyGrad = ctx.createLinearGradient(x - bottomRadiusX, 0, x + bottomRadiusX, 0);
        if (highlightSelected) {
            bodyGrad.addColorStop(0, "#0a4030");
            bodyGrad.addColorStop(0.18, "#12ffb4");
            bodyGrad.addColorStop(0.42, "#0d8a63");
            bodyGrad.addColorStop(0.6, "#063d2c");
            bodyGrad.addColorStop(0.8, "#0fd695");
            bodyGrad.addColorStop(1, "#052b1f");
        } else {
            bodyGrad.addColorStop(0, "#2a0b0e");
            bodyGrad.addColorStop(0.16, "#c21f2e");
            bodyGrad.addColorStop(0.4, "#7a0f1c");
            bodyGrad.addColorStop(0.58, "#3a070d");
            bodyGrad.addColorStop(0.8, "#a81826");
            bodyGrad.addColorStop(1, "#22060a");
        }
        ctx.fillStyle = bodyGrad;
        ctx.fill();

        ctx.save();
        ctx.clip();
        var sheenGrad = ctx.createLinearGradient(x - bottomRadiusX, topY, x - bottomRadiusX * 0.2, bottomY);
        sheenGrad.addColorStop(0, "rgba(255,255,255,0.35)");
        sheenGrad.addColorStop(0.35, "rgba(255,255,255,0.05)");
        sheenGrad.addColorStop(1, "rgba(255,255,255,0)");
        ctx.fillStyle = sheenGrad;
        ctx.beginPath();
        ctx.ellipse(x - w * 0.22, (topY + bottomY) / 2, w * 0.12, h * 0.42, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        ctx.restore();

        ctx.beginPath();
        ctx.ellipse(x, topY, topRadiusX, topRadiusY, 0, 0, Math.PI * 2);
        var rimGrad = ctx.createRadialGradient(x, topY, topRadiusX * 0.2, x, topY, topRadiusX);
        if (highlightSelected) {
            rimGrad.addColorStop(0, "#e6fff6");
            rimGrad.addColorStop(0.5, "#25ffbf");
            rimGrad.addColorStop(1, "#04241a");
        } else {
            rimGrad.addColorStop(0, "#3a0d12");
            rimGrad.addColorStop(0.5, "#170608");
            rimGrad.addColorStop(1, "#000000");
        }
        ctx.fillStyle = rimGrad;
        ctx.fill();

        ctx.beginPath();
        ctx.ellipse(x, topY, topRadiusX * 0.82, topRadiusY * 0.72, 0, 0, Math.PI * 2);
        ctx.strokeStyle = highlightSelected ? "rgba(255,255,255,0.5)" : "rgba(255,255,255,0.12)";
        ctx.lineWidth = Math.max(1, w * 0.012);
        ctx.stroke();
    }

    /* ======================================================
       MAIN RENDER LOOP
       ====================================================== */
    function renderFrame(timestamp) {
        if (!lastFrameTime) lastFrameTime = timestamp;
        var dt = timestamp - lastFrameTime;
        lastFrameTime = timestamp;

        drawBackground();

        if (STATE.cupCount === null || scene.slotX.length === 0) {
            if (STATE.phase !== "intro") {
                drawBall(STATE.width / 2, scene.tableY, scene.ballRadius);
            }
            rafId = requestAnimationFrame(renderFrame);
            return;
        }

        if (!STATE.paused) {
            scene.idleBobPhase += dt * 0.002;
            stepAnimation(timestamp, dt);
        }

        var ballShown = shouldShowBallThisFrame();
        if (ballShown) {
            var bx = scene.ballSlot >= 0 && scene.slotX[scene.ballSlot] !== undefined
                ? scene.slotX[scene.ballSlot]
                : STATE.width / 2;
            drawBall(bx, scene.tableY + scene.cupBaseH * 0.14, scene.ballRadius);
        }

        var order = [];
        for (var c = 0; c < scene.cupCurrentX.length; c++) order.push(c);
        order.sort(function (a, b) {
            return scene.cupCurrentX[a] - scene.cupCurrentX[b];
        });

        for (var k = 0; k < order.length; k++) {
            var cupId = order[k];
            var cx = scene.cupCurrentX[cupId];
            if (cx === undefined) continue;
            var bob = STATE.phase === "guessing" ? Math.sin(scene.idleBobPhase + cupId) * 1.5 : 0;
            var totalLift = (scene.cupLift[cupId] || 0) + (scene.cupRevealLift[cupId] || 0) + bob;
            var isSelected = (STATE.phase === "guessing" && scene.hoverSlotForCup === cupId);
            drawCup(cx, scene.tableY, totalLift, scene.cupBaseW, scene.cupBaseH, false);
        }

        rafId = requestAnimationFrame(renderFrame);
    }

    function shouldShowBallThisFrame() {
        if (STATE.phase === "dropping") return true;
        if (STATE.phase === "revealing" || STATE.phase === "result") return true;
        return false;
    }

    /* ======================================================
       ANIMATION STEP DISPATCH
       ====================================================== */
    function stepAnimation(timestamp, dt) {
        if (STATE.phase === "dropping") {
            stepDropping(timestamp);
        } else if (STATE.phase === "shuffling") {
            stepShuffling(timestamp);
        } else if (STATE.phase === "revealing") {
            stepRevealing(timestamp);
        }
    }

    /* ---------------- DROPPING PHASE ---------------- */
    var dropStartTime = 0;
    var DROP_DURATION = 700;

    function beginDropping() {
        STATE.phase = "dropping";
        dropStartTime = 0;
        for (var i = 0; i < scene.cupLift.length; i++) {
            scene.cupLift[i] = 260;
        }
        setHudMessage("");
    }

    function stepDropping(timestamp) {
        if (!dropStartTime) dropStartTime = timestamp;
        var t = Math.min(1, (timestamp - dropStartTime) / DROP_DURATION);
        var eased = 1 - Math.pow(1 - t, 3);
        for (var i = 0; i < scene.cupLift.length; i++) {
            scene.cupLift[i] = 260 * (1 - eased);
        }
        if (t >= 1) {
            for (var j = 0; j < scene.cupLift.length; j++) scene.cupLift[j] = 0;
            beginShuffling();
        }
    }

    /* ---------------- SHUFFLING PHASE ---------------- */
    function beginShuffling() {
        STATE.phase = "shuffling";
        var profile = DIFFICULTY_PROFILES[STATE.difficulty];
        scene.swapQueue = [];
        var count = STATE.cupCount;
        if (count >= 2) {
            for (var s = 0; s < profile.swaps; s++) {
                var a = Math.floor(Math.random() * count);
                var b = Math.floor(Math.random() * count);
                while (b === a) b = Math.floor(Math.random() * count);
                scene.swapQueue.push([a, b]);
            }
        }
        scene.activeSwap = null;
        setHudMessage("TRACK THE ORB");
        if (count < 2) {
            finishShuffling();
        }
    }

    function stepShuffling(timestamp) {
        var profile = DIFFICULTY_PROFILES[STATE.difficulty];

        if (!scene.activeSwap) {
            if (scene.swapQueue.length === 0) {
                finishShuffling();
                return;
            }
            var pair = scene.swapQueue.shift();
            var slotA = pair[0];
            var slotB = pair[1];
            var cupA = scene.cupAtSlot[slotA];
            var cupB = scene.cupAtSlot[slotB];
            scene.activeSwap = {
                slotA: slotA,
                slotB: slotB,
                cupA: cupA,
                cupB: cupB,
                startXA: scene.slotX[slotA],
                startXB: scene.slotX[slotB],
                startTime: timestamp,
                duration: profile.swapDuration,
                lift: profile.lift
            };
        }

        var sw = scene.activeSwap;
        var t = Math.min(1, (timestamp - sw.startTime) / sw.duration);
        var easedT = t < 0.5
            ? 2 * t * t
            : 1 - Math.pow(-2 * t + 2, 2) / 2;

        var newXA = sw.startXA + (sw.startXB - sw.startXA) * easedT;
        var newXB = sw.startXB + (sw.startXA - sw.startXB) * easedT;
        scene.cupCurrentX[sw.cupA] = newXA;
        scene.cupCurrentX[sw.cupB] = newXB;

        var arcLift = Math.sin(Math.PI * t) * sw.lift;
        scene.cupLift[sw.cupA] = arcLift;
        scene.cupLift[sw.cupB] = arcLift;

        if (t >= 1) {
            scene.cupAtSlot[sw.slotA] = sw.cupB;
            scene.cupAtSlot[sw.slotB] = sw.cupA;
            scene.cupCurrentX[sw.cupA] = scene.slotX[sw.slotB];
            scene.cupCurrentX[sw.cupB] = scene.slotX[sw.slotA];
            scene.cupLift[sw.cupA] = 0;
            scene.cupLift[sw.cupB] = 0;

            if (scene.ballSlot === sw.slotA) {
                scene.ballSlot = sw.slotB;
            } else if (scene.ballSlot === sw.slotB) {
                scene.ballSlot = sw.slotA;
            }

            scene.activeSwap = null;
        }
    }

    function finishShuffling() {
        STATE.phase = "guessing";
        setHudMessage("SELECT THE TARGET NODE");
    }

    /* ---------------- REVEALING PHASE ---------------- */
    var REVEAL_LIFT_HEIGHT = 210;
    var REVEAL_DURATION = 650;

    function beginRevealing(guessedSlot) {
        STATE.phase = "revealing";
        scene.revealStartTime = 0;
        scene.revealDone = false;
        scene.selectedGuessSlot = guessedSlot;
        var win = (guessedSlot === scene.ballSlot);

        STATE.round += 1;
        if (win) STATE.wins += 1;
        updateScorePill();

        scene.pendingWin = win;

        for (var i = 0; i < scene.cupRevealLift.length; i++) {
            scene.cupRevealLift[i] = 0;
        }

        if (win) {
            var cupId = scene.cupAtSlot[guessedSlot];
            scene.revealTargets = [cupId];
        } else {
            var targets = [];
            for (var s = 0; s < scene.cupAtSlot.length; s++) {
                targets.push(scene.cupAtSlot[s]);
            }
            scene.revealTargets = targets;
        }
        setHudMessage("");
    }

    function stepRevealing(timestamp) {
        if (!scene.revealStartTime) scene.revealStartTime = timestamp;
        var t = Math.min(1, (timestamp - scene.revealStartTime) / REVEAL_DURATION);
        var eased = 1 - Math.pow(1 - t, 3);

        for (var i = 0; i < scene.revealTargets.length; i++) {
            var cid = scene.revealTargets[i];
            scene.cupRevealLift[cid] = REVEAL_LIFT_HEIGHT * eased;
        }

        if (t >= 1 && !scene.revealDone) {
            scene.revealDone = true;
            setTimeout(function () {
                showResultOverlay(scene.pendingWin);
            }, 260);
        }
    }

    /* ======================================================
       SCENE INITIALIZATION FOR A NEW ROUND
       ====================================================== */
    function initSceneForRound() {
        recomputeLayout();
        var count = STATE.cupCount;
        scene.cupAtSlot = [];
        scene.cupCurrentX = [];
        scene.cupLift = [];
        scene.cupRevealLift = [];

        for (var i = 0; i < count; i++) {
            scene.cupAtSlot.push(i);
            scene.cupCurrentX.push(scene.slotX[i]);
            scene.cupLift.push(0);
            scene.cupRevealLift.push(0);
        }

        scene.ballSlot = count > 0 ? Math.floor(Math.random() * count) : -1;
        scene.swapQueue = [];
        scene.activeSwap = null;
        scene.selectedGuessSlot = -1;
        scene.revealTargets = [];
    }

    /* ======================================================
       HUD MESSAGE HELPER
       ====================================================== */
    function setHudMessage(text) {
        if (!text) {
            hudMessage.classList.remove("visible");
            hudMessage.textContent = "";
            return;
        }
        hudMessage.textContent = text;
        hudMessage.classList.add("visible");
    }

    function updateScorePill() {
        scorePill.textContent = "ROUND " + STATE.round + "  |  WINS " + STATE.wins;
    }

    function updatePaneStatus() {
        var diffLabel = STATE.difficulty ? DIFFICULTY_PROFILES[STATE.difficulty].label : "-";
        paneStatusText.innerHTML =
            "DIFFICULTY: " + diffLabel + "<br>" +
            "CUPS: " + (STATE.cupCount === null ? "-" : STATE.cupCount) + "<br>" +
            "STATE: " + STATE.phase.toUpperCase();
    }

    /* ======================================================
       RESULT OVERLAY
       ====================================================== */
    function showResultOverlay(win) {
        STATE.phase = "result";
        resultTitle.textContent = win ? "NICE WORK" : "OOPSY DOOPSY";
        resultTitle.className = win ? "win" : "lose";
        resultOverlay.classList.add("visible");
    }

    function hideResultOverlay() {
        resultOverlay.classList.remove("visible");
    }

    resultAgainBtn.addEventListener("click", function () {
        hideResultOverlay();
        initSceneForRound();
        beginDropping();
    });

    /* ======================================================
       INPUT HANDLING: DIFFICULTY + CUP SELECTOR
       ====================================================== */
    var diffButtons = difficultyRow.querySelectorAll(".diff-btn");
    diffButtons.forEach(function (btn) {
        btn.addEventListener("click", function () {
            diffButtons.forEach(function (b) { b.classList.remove("selected"); });
            btn.classList.add("selected");
            STATE.difficulty = btn.getAttribute("data-diff");
            updateStartButtonState();
        });
    });

    var cupSlots = cupSelector.querySelectorAll(".cup-slot");
    cupSlots.forEach(function (slot) {
        slot.addEventListener("click", function () {
            cupSlots.forEach(function (s) { s.classList.remove("selected"); });
            slot.classList.add("selected");
            STATE.cupCount = parseInt(slot.getAttribute("data-count"), 10);
            updateStartButtonState();
        });
    });

    function updateStartButtonState() {
        var ready = (STATE.difficulty !== null) && (STATE.cupCount !== null);
        startBtn.disabled = !ready;
    }

    startBtn.addEventListener("click", function () {
        if (startBtn.disabled) return;
        introOverlay.classList.add("hidden");
        hudMenuBtn.classList.remove("hidden-el");
        scorePill.classList.remove("hidden-el");
        updatePaneStatus();
        initSceneForRound();
        beginDropping();
    });

    /* ======================================================
       INPUT HANDLING: CANVAS CLICK / TOUCH FOR GUESSING
       ====================================================== */
    function getPointerPos(evt) {
        var rect = canvas.getBoundingClientRect();
        var clientX, clientY;
        if (evt.touches && evt.touches.length > 0) {
            clientX = evt.touches[0].clientX;
            clientY = evt.touches[0].clientY;
        } else if (evt.changedTouches && evt.changedTouches.length > 0) {
            clientX = evt.changedTouches[0].clientX;
            clientY = evt.changedTouches[0].clientY;
        } else {
            clientX = evt.clientX;
            clientY = evt.clientY;
        }
        return {
            x: clientX - rect.left,
            y: clientY - rect.top
        };
    }

    function handlePointerDown(evt) {
        var pos = getPointerPos(evt);

        if (hudMenuBtn.getBoundingClientRect().width > 0 && !hudMenuBtn.classList.contains("hidden-el")) {
            var menuRect = hudMenuBtn.getBoundingClientRect();
            var canvasRect = canvas.getBoundingClientRect();
            if (evt.target === hudMenuBtn || hudMenuBtn.contains(evt.target)) {
                return;
            }
        }

        if (STATE.paused) return;
        if (STATE.phase !== "guessing") return;

        var count = STATE.cupCount;
        if (count < 1) return;

        var closestSlot = -1;
        var closestDist = Infinity;
        for (var i = 0; i < scene.slotX.length; i++) {
            var sx = scene.slotX[i];
            var dist = Math.abs(pos.x - sx);
            var withinY = Math.abs(pos.y - scene.tableY) < scene.cupBaseH * 1.1;
            if (dist < scene.cupBaseW * 0.9 && withinY && dist < closestDist) {
                closestDist = dist;
                closestSlot = i;
            }
        }

        if (closestSlot >= 0) {
            evt.preventDefault();
            beginRevealing(closestSlot);
        }
    }

    canvas.addEventListener("mousedown", handlePointerDown, { passive: false });
    canvas.addEventListener("touchstart", handlePointerDown, { passive: false });

    /* ======================================================
       HUD MENU / CONTROL PANE LOGIC
       ====================================================== */
    var wasPausedBeforeMenu = false;

    function openControlPane() {
        wasPausedBeforeMenu = STATE.paused;
        STATE.paused = true;
        updatePaneStatus();
        controlPane.classList.add("open");
        paneBackdrop.classList.add("open");
    }

    function closeControlPane() {
        controlPane.classList.remove("open");
        paneBackdrop.classList.remove("open");
        STATE.paused = wasPausedBeforeMenu;
    }

    hudMenuBtn.addEventListener("click", function () {
        if (controlPane.classList.contains("open")) {
            closeControlPane();
        } else {
            openControlPane();
        }
    });

    paneBackdrop.addEventListener("click", function () {
        closeControlPane();
    });

    btnReturnChassis.addEventListener("click", function () {
        closeControlPane();
        resetToChassisCore();
    });

    btnRecalibrate.addEventListener("click", function () {
        closeControlPane();
        recalibrateSettings();
    });

    function resetToChassisCore() {
        STATE.phase = "intro";
        STATE.paused = false;
        STATE.difficulty = null;
        STATE.cupCount = null;
        STATE.round = 0;
        STATE.wins = 0;
        updateScorePill();
        hideResultOverlay();
        setHudMessage("");
        hudMenuBtn.classList.add("hidden-el");
        scorePill.classList.add("hidden-el");

        diffButtons.forEach(function (b) { b.classList.remove("selected"); });
        cupSlots.forEach(function (s) { s.classList.remove("selected"); });
        startBtn.disabled = true;

        scene.cupAtSlot = [];
        scene.cupCurrentX = [];
        scene.cupLift = [];
        scene.cupRevealLift = [];
        scene.ballSlot = -1;
        scene.swapQueue = [];
        scene.activeSwap = null;

        introOverlay.classList.remove("hidden");
    }

    function recalibrateSettings() {
        STATE.phase = "intro";
        STATE.paused = false;
        hideResultOverlay();
        setHudMessage("");
        hudMenuBtn.classList.add("hidden-el");
        scorePill.classList.add("hidden-el");

        scene.cupAtSlot = [];
        scene.cupCurrentX = [];
        scene.cupLift = [];
        scene.cupRevealLift = [];
        scene.ballSlot = -1;
        scene.swapQueue = [];
        scene.activeSwap = null;

        introOverlay.classList.remove("hidden");
    }

    /* ======================================================
       BOOTSTRAP
       ====================================================== */
    resizeCanvas();
    updateScorePill();
    rafId = requestAnimationFrame(renderFrame);

})();
</script>
</body>
</html>
"""

components.html(game_html, height=700, scrolling=False)
