
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Coconut Shuffle",
    page_icon="🥥",
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
        body {background-color: #0f1d3a;}
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
<title>Coconut Shuffle</title>
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
        background: #0f1d3a;
        font-family: 'Georgia', 'Trebuchet MS', serif;
    }

    #game-root {
        position: fixed;
        inset: 0;
        width: 100vw;
        height: 100vh;
        background: #0f1d3a;
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

    /* ================= LOADING SCREEN ================= */
    #loading-screen {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: linear-gradient(180deg, #0f1d3a 0%, #16294f 45%, #1c355e 100%);
        z-index: 80;
        overflow: hidden;
        transition: opacity 0.6s ease, visibility 0.6s ease;
    }

    #loading-screen.hidden {
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
    }

    .foam-particle {
        position: absolute;
        bottom: -20px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255,255,255,0.85) 0%, rgba(255,255,255,0) 70%);
        filter: blur(0.5px);
        animation-name: floatFoam;
        animation-timing-function: ease-in;
        animation-iteration-count: infinite;
    }

    @keyframes floatFoam {
        0% { transform: translateY(0) translateX(0); opacity: 0; }
        10% { opacity: 0.9; }
        90% { opacity: 0.5; }
        100% { transform: translateY(-115vh) translateX(var(--drift, 20px)); opacity: 0; }
    }

    .palm-silhouette {
        position: absolute;
        bottom: 0;
        width: 140px;
        height: 260px;
        opacity: 0.55;
    }

    #loading-hud {
        position: relative;
        z-index: 5;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 0 20px;
    }

    .wood-title {
        font-size: clamp(24px, 5.4vw, 48px);
        font-weight: 900;
        letter-spacing: 2px;
        text-align: center;
        color: #d9b578;
        background: linear-gradient(180deg, #e8c98d 0%, #b98a4c 55%, #7a4f2a 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 0 rgba(0,0,0,0.55), 0 4px 8px rgba(0,0,0,0.5);
        margin-bottom: 8px;
        filter: drop-shadow(0 1px 0 rgba(255,235,200,0.25));
    }

    .wood-subtitle {
        font-size: clamp(11px, 2vw, 14px);
        letter-spacing: 5px;
        color: #9fb3d0;
        text-transform: uppercase;
        margin-bottom: 42px;
        text-align: center;
    }

    #bamboo-track {
        position: relative;
        width: clamp(220px, 50vw, 380px);
        height: 26px;
        border-radius: 14px;
        background: repeating-linear-gradient(
            90deg,
            #cbb37c 0px, #cbb37c 34px,
            #b89c60 34px, #b89c60 38px
        );
        border: 3px solid #6b5330;
        box-shadow: inset 0 3px 6px rgba(0,0,0,0.35), 0 6px 14px rgba(0,0,0,0.4);
        overflow: hidden;
    }

    #bamboo-fill {
        height: 100%;
        width: 0%;
        border-radius: 10px;
        background: linear-gradient(180deg, #5a3820 0%, #3d2314 55%, #22120a 100%);
        box-shadow: inset 0 2px 4px rgba(255,220,170,0.15), inset 0 -3px 6px rgba(0,0,0,0.4);
        transition: width 0.12s linear;
    }

    #loading-pct {
        margin-top: 14px;
        color: #b9c9e6;
        font-size: 13px;
        letter-spacing: 3px;
    }

    #enter-resort-btn {
        display: none;
        margin-top: 6px;
        padding: 18px 50px;
        font-size: clamp(15px, 2.4vw, 19px);
        font-weight: 800;
        letter-spacing: 3px;
        color: #f3e4c4;
        background: linear-gradient(180deg, #8a5a30 0%, #5c3a21 55%, #3d2314 100%);
        border: 3px solid #22120a;
        border-radius: 10px;
        cursor: pointer;
        box-shadow: 0 6px 0 #1a0d06, 0 10px 18px rgba(0,0,0,0.55);
        transition: transform 0.12s ease, box-shadow 0.12s ease;
    }

    #enter-resort-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 0 #1a0d06, 0 14px 22px rgba(0,0,0,0.6);
    }

    #enter-resort-btn:active {
        transform: translateY(3px);
        box-shadow: 0 3px 0 #1a0d06, 0 6px 10px rgba(0,0,0,0.5);
    }

    /* ================= WOODEN CONFIG WINDOW ================= */
    #intro-overlay {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: linear-gradient(180deg, #22150c 0%, #150d07 100%);
        z-index: 50;
        transition: opacity 0.5s ease, visibility 0.5s ease;
        padding: 20px;
        overflow-y: auto;
    }

    #intro-overlay.hidden {
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
    }

    .plank-title {
        font-size: clamp(20px, 4.4vw, 34px);
        font-weight: 900;
        letter-spacing: 2px;
        text-align: center;
        color: #e8c98d;
        text-shadow: 0 2px 0 rgba(0,0,0,0.6);
        margin-bottom: 30px;
    }

    .section-label {
        color: #c9a869;
        font-size: clamp(11px, 1.8vw, 14px);
        letter-spacing: 3px;
        text-transform: uppercase;
        margin: 18px 0 14px 0;
        text-align: center;
        opacity: 0.9;
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
        padding: 15px 30px;
        font-size: clamp(13px, 2vw, 16px);
        font-weight: 700;
        letter-spacing: 2px;
        color: #e9d4ac;
        background: linear-gradient(180deg, #7a4f30 0%, #5c3a21 100%);
        border: 2px solid #3d2314;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.15s ease;
        box-shadow: 0 4px 0 #22120a, inset 0 1px 0 rgba(255,255,255,0.08);
    }

    .diff-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 0 #22120a, inset 0 1px 0 rgba(255,255,255,0.1);
    }

    .diff-btn.selected {
        background: linear-gradient(180deg, #caa250 0%, #d4af37 55%, #8a6a1e 100%);
        color: #2a1a06;
        border-color: #6b5119;
        box-shadow: 0 4px 0 #4a3813, inset 0 1px 0 rgba(255,255,255,0.35);
    }

    #cup-selector {
        display: flex;
        gap: 10px;
        justify-content: center;
        flex-wrap: wrap;
        margin-bottom: 10px;
    }

    .cup-slot {
        width: clamp(42px, 8vw, 58px);
        height: clamp(42px, 8vw, 58px);
        border-radius: 8px;
        border: 2px solid #3d2314;
        background: linear-gradient(180deg, #6b4527 0%, #4a2e16 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: clamp(15px, 2.4vw, 19px);
        color: #d9c3a0;
        cursor: pointer;
        transition: all 0.15s ease;
        box-shadow: 0 3px 0 #22120a, inset 0 1px 0 rgba(255,255,255,0.06);
    }

    .cup-slot:hover {
        transform: translateY(-2px);
    }

    .cup-slot.selected {
        background: linear-gradient(180deg, #eccb70 0%, #d4af37 55%, #93711f 100%);
        border-color: #3d2314;
        color: #2a1a06;
        box-shadow: 0 3px 0 #4a3813, inset 0 1px 0 rgba(255,255,255,0.4);
        transform: scale(1.06);
    }

    #start-descent-btn {
        margin-top: 30px;
        padding: 17px 48px;
        font-size: clamp(14px, 2.4vw, 18px);
        font-weight: 800;
        letter-spacing: 3px;
        color: #f3e4c4;
        background: linear-gradient(180deg, #8a5a30 0%, #5c3a21 55%, #3d2314 100%);
        border: 3px solid #22120a;
        border-radius: 10px;
        cursor: pointer;
        box-shadow: 0 6px 0 #1a0d06, 0 10px 18px rgba(0,0,0,0.5);
        transition: all 0.15s ease;
    }

    #start-descent-btn:disabled {
        opacity: 0.35;
        cursor: not-allowed;
        box-shadow: 0 6px 0 #1a0d06;
    }

    #start-descent-btn:not(:disabled):hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 0 #1a0d06, 0 12px 20px rgba(0,0,0,0.55);
    }

    #start-descent-btn:not(:disabled):active {
        transform: translateY(3px);
        box-shadow: 0 3px 0 #1a0d06;
    }

    .hint-text {
        margin-top: 14px;
        color: #8a7455;
        font-size: clamp(10px, 1.6vw, 12px);
        letter-spacing: 1px;
        text-align: center;
    }

    /* ================= HUD (WOOD, NO GLOW) ================= */
    #hud-menu-btn {
        position: absolute;
        top: 16px;
        left: 16px;
        width: 44px;
        height: 44px;
        border-radius: 6px;
        background: linear-gradient(180deg, #6b4527 0%, #4a2e16 100%);
        border: 2px solid #22120a;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 40;
        box-shadow: 0 4px 0 #17100a, 0 6px 10px rgba(0,0,0,0.4);
        transition: transform 0.15s ease;
    }

    #hud-menu-btn:hover {
        transform: translateY(-1px);
    }

    #hud-menu-btn span {
        display: block;
        width: 20px;
        height: 3px;
        background: #d9c3a0;
        margin: 2.5px 0;
        border-radius: 2px;
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
        width: 40px;
        height: 40px;
        border-radius: 6px;
        background: linear-gradient(180deg, #6b4527 0%, #4a2e16 100%);
        border: 2px solid #22120a;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 16px;
        box-shadow: 0 4px 0 #17100a, 0 6px 10px rgba(0,0,0,0.4);
        transition: transform 0.15s ease;
        flex-shrink: 0;
    }

    #mute-btn:hover {
        transform: translateY(-1px);
    }

    #mute-btn.muted {
        filter: grayscale(0.4);
    }

    #control-pane {
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        width: min(280px, 78vw);
        background:
            repeating-linear-gradient(115deg, rgba(0,0,0,0.08) 0px, rgba(0,0,0,0.08) 3px, transparent 3px, transparent 9px),
            linear-gradient(160deg, #3d2b18 0%, #22150c 100%);
        border-right: 3px solid #1a0d06;
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
        color: #e8c98d;
        font-size: 14px;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 22px;
    }

    .control-link {
        display: block;
        width: 100%;
        text-align: left;
        padding: 14px 16px;
        margin-bottom: 12px;
        background: linear-gradient(180deg, #6b4527 0%, #4a2e16 100%);
        border: 2px solid #22120a;
        border-radius: 8px;
        color: #e9d4ac;
        font-size: 12.5px;
        letter-spacing: 1.5px;
        font-weight: 700;
        cursor: pointer;
        box-shadow: 0 3px 0 #17100a;
        transition: all 0.15s ease;
    }

    .control-link:hover {
        transform: translateY(-1px);
    }

    .control-status {
        margin-top: 26px;
        color: #9c8362;
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
        color: #3d2314;
        font-size: clamp(12px, 2.4vw, 17px);
        font-weight: 800;
        letter-spacing: 2px;
        text-align: center;
        padding: 10px 22px;
        border-radius: 8px;
        background: linear-gradient(180deg, #e8c98d 0%, #cbaa66 100%);
        border: 2px solid #6b5330;
        z-index: 30;
        opacity: 0;
        transition: opacity 0.4s ease;
        pointer-events: none;
        max-width: 90%;
        box-shadow: 0 4px 10px rgba(0,0,0,0.35);
    }

    #hud-message.visible {
        opacity: 1;
    }

    #score-pill {
        padding: 9px 18px;
        border-radius: 8px;
        background: linear-gradient(180deg, #6b4527 0%, #4a2e16 100%);
        border: 2px solid #22120a;
        color: #e9d4ac;
        font-size: clamp(11px, 1.8vw, 13px);
        font-weight: 700;
        letter-spacing: 1.5px;
        z-index: 40;
        box-shadow: 0 4px 0 #17100a, 0 6px 10px rgba(0,0,0,0.4);
    }

    #audio-unlock-hint {
        position: absolute;
        bottom: 22px;
        left: 50%;
        transform: translateX(-50%);
        padding: 11px 22px;
        border-radius: 8px;
        background: linear-gradient(180deg, #6b4527 0%, #4a2e16 100%);
        border: 2px solid #d4af37;
        color: #f0e0bb;
        font-size: clamp(11px, 2vw, 13px);
        font-weight: 700;
        letter-spacing: 1.5px;
        z-index: 65;
        cursor: pointer;
        box-shadow: 0 4px 0 #17100a, 0 6px 14px rgba(0,0,0,0.45);
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
        animation: hintBob 1.6s ease-in-out infinite;
    }

    #audio-unlock-hint.visible {
        opacity: 1;
        pointer-events: auto;
    }

    @keyframes hintBob {
        0%, 100% { transform: translateX(-50%) translateY(0); }
        50% { transform: translateX(-50%) translateY(-4px); }
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
        background: rgba(10,6,3,0.6);
    }

    #result-overlay.visible {
        opacity: 1;
        pointer-events: auto;
    }

    #result-title {
        font-size: clamp(28px, 7vw, 58px);
        font-weight: 900;
        letter-spacing: 3px;
        text-align: center;
        margin-bottom: 26px;
        padding: 0 16px;
        text-shadow: 0 3px 0 rgba(0,0,0,0.6);
    }

    #result-title.win {
        color: #f3d98a;
        animation: winPulse 1s ease-in-out infinite;
    }

    #result-title.lose {
        color: #d98a7a;
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
        padding: 15px 42px;
        font-size: clamp(13px, 2.2vw, 16px);
        font-weight: 800;
        letter-spacing: 2px;
        color: #f3e4c4;
        background: linear-gradient(180deg, #8a5a30 0%, #5c3a21 55%, #3d2314 100%);
        border: 3px solid #22120a;
        border-radius: 10px;
        cursor: pointer;
        box-shadow: 0 6px 0 #1a0d06;
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

    <div id="audio-unlock-hint">&#128266; TAP HERE TO ENABLE SOUND</div>

    <div id="pane-backdrop"></div>
    <div id="control-pane">
        <div class="control-pane-title">RESORT CONTROL DESK</div>
        <button class="control-link" id="btn-return-chassis">&#8592; RETURN TO MAIN GATE</button>
        <button class="control-link" id="btn-recalibrate">&#9881; ADJUST SHUFFLE SETTINGS</button>
        <div class="control-status" id="pane-status-text">DIFFICULTY: EASY<br>CUPS: 3<br>STATE: IDLE</div>
    </div>

    <div id="result-overlay">
        <div id="result-title"></div>
        <button id="result-again-btn">SHUFFLE AGAIN</button>
    </div>

    <div id="intro-overlay" class="hidden">
        <div class="plank-title">&#129381; COCONUT SHUFFLE</div>

        <div class="section-label">SELECT DIFFICULTY</div>
        <div id="difficulty-row">
            <button class="diff-btn" data-diff="easy">EASY</button>
            <button class="diff-btn" data-diff="medium">MEDIUM</button>
            <button class="diff-btn" data-diff="hard">HARD</button>
        </div>

        <div class="section-label">SELECT CUP COUNT</div>
        <div id="cup-selector">
            <div class="cup-slot" data-count="1">1</div>
            <div class="cup-slot" data-count="2">2</div>
            <div class="cup-slot selected" data-count="3">3</div>
            <div class="cup-slot" data-count="4">4</div>
            <div class="cup-slot" data-count="5">5</div>
        </div>

        <button id="start-descent-btn" disabled>BEGIN SHUFFLE &#127754;</button>
        <div class="hint-text">CHOOSE A DIFFICULTY TO BEGIN</div>
    </div>

    <div id="loading-screen">
        <div id="foam-container"></div>
        <div id="loading-hud">
            <div class="wood-title">&#129381; COCONUT SHUFFLE</div>
            <div class="wood-subtitle">A RUSTIC RESORT GUESSING GAME</div>
            <div id="bamboo-track"><div id="bamboo-fill"></div></div>
            <div id="loading-pct">LOADING RESORT... 0%</div>
            <button id="enter-resort-btn">ENTER RESORT &#127796;</button>
        </div>
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
    var loadingScreen = document.getElementById("loading-screen");
    var bambooFill = document.getElementById("bamboo-fill");
    var loadingPct = document.getElementById("loading-pct");
    var enterResortBtn = document.getElementById("enter-resort-btn");
    var foamContainer = document.getElementById("foam-container");
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
    var audioUnlockHint = document.getElementById("audio-unlock-hint");
    var scorePill = document.getElementById("score-pill");
    var resultOverlay = document.getElementById("result-overlay");
    var resultTitle = document.getElementById("result-title");
    var resultAgainBtn = document.getElementById("result-again-btn");

    /* ======================================================
       GLOBAL GAME STATE
       ====================================================== */
    var STATE = {
        phase: "loading",        // loading | intro | dropping | shuffling | guessing | revealing | result
        difficulty: null,        // easy | medium | hard
        cupCount: 3,              // 1 - 5 (no zero-cup option)
        paused: false,
        round: 0,
        wins: 0,
        dpr: Math.max(1, window.devicePixelRatio || 1),
        width: 0,
        height: 0
    };

    var DIFFICULTY_PROFILES = {
        easy:   { swaps: 5,  swapDuration: 950, lift: 40, label: "EASY",   waveSpeed: 0.7,  orbitAmp: 16, fig8Amp: 10 },
        medium: { swaps: 9,  swapDuration: 600, lift: 54, label: "MEDIUM", waveSpeed: 1.3,  orbitAmp: 30, fig8Amp: 22 },
        hard:   { swaps: 15, swapDuration: 320, lift: 70, label: "HARD",   waveSpeed: 2.2,  orbitAmp: 48, fig8Amp: 38 }
    };

    /* ======================================================
       LOADING SCREEN: FOAM PARTICLES + PROGRESS BAR
       ====================================================== */
    function spawnFoamParticles() {
        var count = 26;
        for (var i = 0; i < count; i++) {
            var p = document.createElement("div");
            p.className = "foam-particle";
            var size = 4 + Math.random() * 10;
            p.style.width = size + "px";
            p.style.height = size + "px";
            p.style.left = (Math.random() * 100) + "vw";
            var duration = 6 + Math.random() * 7;
            p.style.animationDuration = duration + "s";
            p.style.animationDelay = (-Math.random() * duration) + "s";
            p.style.setProperty("--drift", (Math.random() * 80 - 40) + "px");
            foamContainer.appendChild(p);
        }
    }

    function drawPalmSVG(flip) {
        var ns = "http://www.w3.org/2000/svg";
        var svg = document.createElementNS(ns, "svg");
        svg.setAttribute("viewBox", "0 0 140 260");
        svg.setAttribute("class", "palm-silhouette");
        svg.style.left = flip ? "auto" : "-6px";
        svg.style.right = flip ? "-6px" : "auto";
        if (flip) svg.style.transform = "scaleX(-1)";
        var g = document.createElementNS(ns, "path");
        g.setAttribute("d",
            "M70 260 Q60 170 66 110 Q40 90 20 60 Q46 70 68 92 Q58 50 40 10 Q62 40 70 90 " +
            "Q78 40 100 10 Q82 50 72 92 Q94 70 120 60 Q100 90 74 110 Q80 170 70 260 Z");
        g.setAttribute("fill", "#0a1526");
        svg.appendChild(g);
        return svg;
    }

    function initLoadingVisuals() {
        spawnFoamParticles();
        foamContainer.appendChild(drawPalmSVG(false));
        foamContainer.appendChild(drawPalmSVG(true));
    }

    var loadingProgress = 0;
    var loadingIntervalId = null;

    function runLoadingBar() {
        loadingIntervalId = setInterval(function () {
            var step = loadingProgress < 60 ? (0.8 + Math.random() * 1.6) : (0.4 + Math.random() * 1.0);
            loadingProgress = Math.min(99, loadingProgress + step);
            bambooFill.style.width = loadingProgress + "%";
            loadingPct.textContent = "LOADING RESORT... " + Math.floor(loadingProgress) + "%";
            if (loadingProgress >= 99) {
                clearInterval(loadingIntervalId);
                loadingIntervalId = null;
                bambooFill.parentElement.style.display = "none";
                loadingPct.style.display = "none";
                enterResortBtn.style.display = "inline-block";
            }
        }, 90);
    }

    enterResortBtn.addEventListener("click", function () {
        loadingScreen.classList.add("hidden");
        introOverlay.classList.remove("hidden");
        STATE.phase = "intro";
    });

    /* ======================================================
       AUDIO ENGINE
       Fully synthesized in-browser via the Web Audio API.
       No external audio files are loaded. Background music is
       a syncopated steel-drum / marimba style tropical vacation
       loop, and every sound effect (coconut taps, whooshes,
       thuds, stingers) is built from oscillators and filtered
       noise buffers.
       ====================================================== */
    var AudioEngine = {
        ctx: null,
        master: null,
        musicBus: null,
        sfxBus: null,
        delayNode: null,
        delayFeedback: null,
        muted: false,
        musicPlaying: false,
        schedulerId: null,
        nextStepTime: 0,
        stepIndex: 0,
        tempo: 112,
        stepsPerBeat: 2,
        /* Calypso-ish major/pentatonic progression, tuned for steel drum + marimba plinks */
        chords: [
            { notes: [220.00, 277.18, 329.63, 440.00], bass: 110.00 },
            { notes: [246.94, 293.66, 369.99, 493.88], bass: 123.47 },
            { notes: [196.00, 246.94, 293.66, 392.00], bass: 98.00 },
            { notes: [220.00, 277.18, 329.63, 415.30], bass: 110.00 }
        ],
        /* syncopated hit pattern across 8 steps per bar: 1 = accent plink */
        rhythmPattern: [1, 0, 1, 1, 0, 1, 0, 1],

        init: function () {
            if (this.ctx) return;
            var AC = window.AudioContext || window.webkitAudioContext;
            if (!AC) return;
            this.ctx = new AC();

            this.master = this.ctx.createGain();
            this.master.gain.value = this.muted ? 0 : 1.0;

            this.compressor = this.ctx.createDynamicsCompressor();
            this.compressor.threshold.value = -18;
            this.compressor.knee.value = 24;
            this.compressor.ratio.value = 4;
            this.compressor.attack.value = 0.003;
            this.compressor.release.value = 0.25;

            this.master.connect(this.compressor);
            this.compressor.connect(this.ctx.destination);

            this.musicBus = this.ctx.createGain();
            this.musicBus.gain.value = 0.5;
            this.musicBus.connect(this.master);

            this.sfxBus = this.ctx.createGain();
            this.sfxBus.gain.value = 1.0;
            this.sfxBus.connect(this.master);

            this.delayNode = this.ctx.createDelay();
            this.delayNode.delayTime.value = 0.19;
            this.delayFeedback = this.ctx.createGain();
            this.delayFeedback.gain.value = 0.16;
            var delayFilter = this.ctx.createBiquadFilter();
            delayFilter.type = "lowpass";
            delayFilter.frequency.value = 3200;
            this.delayNode.connect(delayFilter);
            delayFilter.connect(this.delayFeedback);
            this.delayFeedback.connect(this.delayNode);
            this.delayNode.connect(this.musicBus);
        },

        resume: function () {
            if (this.ctx && this.ctx.state !== "running") {
                return this.ctx.resume();
            }
            return Promise.resolve();
        },

        toggleMute: function () {
            this.muted = !this.muted;
            if (this.master && this.ctx) {
                this.master.gain.setTargetAtTime(this.muted ? 0 : 1.0, this.ctx.currentTime, 0.05);
            }
            return this.muted;
        },

        /* ---------------- BACKGROUND MUSIC ---------------- */
        startMusic: function () {
            this.init();
            this.resume();
            if (this.musicPlaying || !this.ctx) return;
            this.musicPlaying = true;
            this.stepIndex = 0;
            this.nextStepTime = this.ctx.currentTime + 0.05;
            var self = this;
            this.schedulerId = setInterval(function () { self.scheduler(); }, 25);
        },

        stopMusic: function () {
            this.musicPlaying = false;
            if (this.schedulerId) {
                clearInterval(this.schedulerId);
                this.schedulerId = null;
            }
        },

        scheduler: function () {
            if (!this.ctx) return;
            if (this.nextStepTime < this.ctx.currentTime) {
                this.nextStepTime = this.ctx.currentTime + 0.02;
            }
            var secondsPerStep = (60.0 / this.tempo) / this.stepsPerBeat;
            while (this.nextStepTime < this.ctx.currentTime + 0.12) {
                try {
                    this.scheduleStep(this.stepIndex, this.nextStepTime);
                } catch (schedErr) {
                    /* never let one bad note stop the whole loop */
                }
                this.nextStepTime += secondsPerStep;
                this.stepIndex = (this.stepIndex + 1) % 32;
            }
        },

        scheduleStep: function (step, time) {
            var barIndex = Math.floor(step / 8) % this.chords.length;
            var chord = this.chords[barIndex];
            var stepInBar = step % 8;

            if (stepInBar === 0) {
                this.playMarimbaPad(chord.notes, time);
            }
            if (stepInBar === 0 || stepInBar === 4) {
                this.playSteelBass(chord.bass, time);
            }
            if (this.rhythmPattern[stepInBar] === 1) {
                var note = chord.notes[(step + barIndex) % chord.notes.length];
                this.playSteelDrum(note * 2, time, stepInBar % 4 === 0 ? 0.55 : 0.34);
            }
            if (stepInBar % 2 === 1) {
                this.playShaker(time, stepInBar === 7 ? 0.22 : 0.12);
            }
        },

        /* soft marimba pad -- rounded triangle tone, quick soft attack */
        playMarimbaPad: function (freqs, time) {
            if (!this.musicPlaying) return;
            var self = this;
            var duration = (60.0 / this.tempo) * 4;
            freqs.forEach(function (f, idx) {
                var t = time + idx * 0.015;
                var osc = self.ctx.createOscillator();
                osc.type = "triangle";
                osc.frequency.value = f / 2;
                var filter = self.ctx.createBiquadFilter();
                filter.type = "lowpass";
                filter.frequency.value = 1400;
                var g = self.ctx.createGain();
                g.gain.setValueAtTime(0.0001, t);
                g.gain.exponentialRampToValueAtTime(0.11, t + 0.03);
                g.gain.exponentialRampToValueAtTime(0.0001, t + duration * 0.8);
                osc.connect(filter);
                filter.connect(g);
                g.connect(self.musicBus);
                osc.start(t);
                osc.stop(t + duration);
            });
        },

        /* warm rounded steel-drum bass thump */
        playSteelBass: function (freq, time) {
            if (!this.musicPlaying) return;
            var osc = this.ctx.createOscillator();
            osc.type = "sine";
            osc.frequency.value = freq;
            var g = this.ctx.createGain();
            g.gain.setValueAtTime(0.0001, time);
            g.gain.exponentialRampToValueAtTime(0.38, time + 0.015);
            g.gain.exponentialRampToValueAtTime(0.0001, time + 0.5);
            osc.connect(g);
            g.connect(this.musicBus);
            osc.start(time);
            osc.stop(time + 0.52);
        },

        /* bright bell-like steel drum plink -- fundamental + detuned overtone through a resonant bandpass */
        playSteelDrum: function (freq, time, velocity) {
            if (!this.musicPlaying) return;
            var self = this;
            var g = this.ctx.createGain();
            g.gain.setValueAtTime(0.0001, time);
            g.gain.exponentialRampToValueAtTime(velocity * 0.3, time + 0.008);
            g.gain.exponentialRampToValueAtTime(0.0001, time + 0.42);

            var bandpass = this.ctx.createBiquadFilter();
            bandpass.type = "bandpass";
            bandpass.frequency.value = freq * 1.5;
            bandpass.Q.value = 3.5;

            g.connect(bandpass);
            bandpass.connect(this.musicBus);
            if (this.delayNode) bandpass.connect(this.delayNode);

            [1.0, 2.005, 3.01].forEach(function (mult, idx) {
                var osc = self.ctx.createOscillator();
                osc.type = "sine";
                osc.frequency.value = freq * mult;
                var og = self.ctx.createGain();
                og.gain.value = idx === 0 ? 1.0 : (idx === 1 ? 0.35 : 0.15);
                osc.connect(og);
                og.connect(g);
                osc.start(time);
                osc.stop(time + 0.45);
            });
        },

        /* soft shaker/maraca-style noise tick for the tropical groove */
        playShaker: function (time, velocity) {
            if (!this.musicPlaying) return;
            var bufferSize = Math.floor(this.ctx.sampleRate * 0.06);
            var buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
            var data = buffer.getChannelData(0);
            for (var i = 0; i < bufferSize; i++) {
                data[i] = (Math.random() * 2 - 1) * (1 - i / bufferSize);
            }
            var noise = this.ctx.createBufferSource();
            noise.buffer = buffer;
            var filter = this.ctx.createBiquadFilter();
            filter.type = "bandpass";
            filter.frequency.value = 5200;
            filter.Q.value = 0.9;
            var g = this.ctx.createGain();
            g.gain.setValueAtTime(velocity * 0.35, time);
            g.gain.exponentialRampToValueAtTime(0.0001, time + 0.07);
            noise.connect(filter);
            filter.connect(g);
            g.connect(this.musicBus);
            noise.start(time);
            noise.stop(time + 0.08);
        },

        /* ---------------- SOUND EFFECTS ---------------- */
        makeNoiseBuffer: function (duration) {
            var bufferSize = Math.max(1, Math.floor(this.ctx.sampleRate * duration));
            var buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
            var data = buffer.getChannelData(0);
            for (var i = 0; i < bufferSize; i++) {
                data[i] = Math.random() * 2 - 1;
            }
            return buffer;
        },

        /* woody "tock" when a coconut cup is tapped -- softer & lower than a metallic clack */
        playCupClack: function () {
            this.init();
            this.resume();
            if (!this.ctx) return;
            var now = this.ctx.currentTime;

            var noise = this.ctx.createBufferSource();
            noise.buffer = this.makeNoiseBuffer(0.06);
            var bandpass = this.ctx.createBiquadFilter();
            bandpass.type = "bandpass";
            bandpass.frequency.value = 750 + Math.random() * 220;
            bandpass.Q.value = 1.2;
            var noiseGain = this.ctx.createGain();
            noiseGain.gain.setValueAtTime(0.28, now);
            noiseGain.gain.exponentialRampToValueAtTime(0.0001, now + 0.07);
            noise.connect(bandpass);
            bandpass.connect(noiseGain);
            noiseGain.connect(this.sfxBus);
            noise.start(now);
            noise.stop(now + 0.08);

            var tock = this.ctx.createOscillator();
            tock.type = "sine";
            tock.frequency.setValueAtTime(140 + Math.random() * 30, now);
            tock.frequency.exponentialRampToValueAtTime(70, now + 0.1);
            var tockGain = this.ctx.createGain();
            tockGain.gain.setValueAtTime(0.6, now);
            tockGain.gain.exponentialRampToValueAtTime(0.0001, now + 0.14);
            tock.connect(tockGain);
            tockGain.connect(this.sfxBus);
            tock.start(now);
            tock.stop(now + 0.16);
        },

        playSwapWhoosh: function () {
            this.init();
            this.resume();
            if (!this.ctx) return;
            var now = this.ctx.currentTime;
            var noise = this.ctx.createBufferSource();
            noise.buffer = this.makeNoiseBuffer(0.16);
            var filter = this.ctx.createBiquadFilter();
            filter.type = "bandpass";
            filter.Q.value = 0.8;
            filter.frequency.setValueAtTime(350, now);
            filter.frequency.exponentialRampToValueAtTime(1600, now + 0.14);
            var g = this.ctx.createGain();
            g.gain.setValueAtTime(0.0001, now);
            g.gain.exponentialRampToValueAtTime(0.18, now + 0.03);
            g.gain.exponentialRampToValueAtTime(0.0001, now + 0.16);
            noise.connect(filter);
            filter.connect(g);
            g.connect(this.sfxBus);
            noise.start(now);
            noise.stop(now + 0.17);
        },

        playThud: function () {
            this.init();
            this.resume();
            if (!this.ctx) return;
            var now = this.ctx.currentTime;
            var osc = this.ctx.createOscillator();
            osc.type = "sine";
            osc.frequency.setValueAtTime(110, now);
            osc.frequency.exponentialRampToValueAtTime(50, now + 0.18);
            var g = this.ctx.createGain();
            g.gain.setValueAtTime(0.5, now);
            g.gain.exponentialRampToValueAtTime(0.0001, now + 0.22);
            osc.connect(g);
            g.connect(this.sfxBus);
            osc.start(now);
            osc.stop(now + 0.25);

            var noise = this.ctx.createBufferSource();
            noise.buffer = this.makeNoiseBuffer(0.05);
            var filter = this.ctx.createBiquadFilter();
            filter.type = "lowpass";
            filter.frequency.value = 450;
            var ng = this.ctx.createGain();
            ng.gain.setValueAtTime(0.3, now);
            ng.gain.exponentialRampToValueAtTime(0.0001, now + 0.05);
            noise.connect(filter);
            filter.connect(ng);
            ng.connect(this.sfxBus);
            noise.start(now);
            noise.stop(now + 0.06);
        },

        playRevealWhoosh: function () {
            this.init();
            this.resume();
            if (!this.ctx) return;
            var now = this.ctx.currentTime;
            var noise = this.ctx.createBufferSource();
            noise.buffer = this.makeNoiseBuffer(0.5);
            var filter = this.ctx.createBiquadFilter();
            filter.type = "bandpass";
            filter.Q.value = 0.7;
            filter.frequency.setValueAtTime(220, now);
            filter.frequency.exponentialRampToValueAtTime(1500, now + 0.45);
            var g = this.ctx.createGain();
            g.gain.setValueAtTime(0.0001, now);
            g.gain.exponentialRampToValueAtTime(0.22, now + 0.08);
            g.gain.exponentialRampToValueAtTime(0.0001, now + 0.5);
            noise.connect(filter);
            filter.connect(g);
            g.connect(this.sfxBus);
            noise.start(now);
            noise.stop(now + 0.52);
        },

        playWinStinger: function () {
            this.init();
            this.resume();
            if (!this.ctx) return;
            var self = this;
            var now = this.ctx.currentTime;
            var notes = [392.00, 493.88, 587.33, 783.99];
            notes.forEach(function (freq, idx) {
                var t = now + idx * 0.1;
                self.playSteelDrum(freq, t, 0.9);
            });
        },

        playLoseStinger: function () {
            this.init();
            this.resume();
            if (!this.ctx) return;
            var self = this;
            var now = this.ctx.currentTime;
            var notes = [196.00, 174.61, 155.56];
            notes.forEach(function (freq, idx) {
                var t = now + idx * 0.15;
                var osc = self.ctx.createOscillator();
                osc.type = "sine";
                osc.frequency.value = freq;
                var filter = self.ctx.createBiquadFilter();
                filter.type = "lowpass";
                filter.frequency.value = 700;
                var g = self.ctx.createGain();
                g.gain.setValueAtTime(0.0001, t);
                g.gain.exponentialRampToValueAtTime(0.26, t + 0.02);
                g.gain.exponentialRampToValueAtTime(0.0001, t + 0.4);
                osc.connect(filter);
                filter.connect(g);
                g.connect(self.sfxBus);
                osc.start(t);
                osc.stop(t + 0.42);
            });
        }
    };

    /* ======================================================
       CUP / BALL SCENE STATE
       ====================================================== */
    var scene = {
        slotX: [],
        tableY: 0,
        cupBaseW: 0,
        cupBaseH: 0,
        ballRadius: 0,
        cupAtSlot: [],
        cupCurrentX: [],
        cupLift: [],
        cupRevealLift: [],
        ballSlot: -1,
        swapQueue: [],
        activeSwap: null,
        selectedGuessSlot: -1,
        revealStartTime: 0,
        revealDone: false,
        idleBobPhase: 0,
        splashParticles: [],
        bgCache: null,
        bgCacheW: 0,
        bgCacheH: 0
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
        scene.cupBaseH = scene.cupBaseW * 1.3;
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
       DRAWING: BACKGROUND (SUNNY RESORT BEACH SCENE)
       ====================================================== */
    function buildBackgroundCache() {
        var w = STATE.width;
        var h = STATE.height;
        if (w <= 0 || h <= 0) return;

        var cache = document.createElement("canvas");
        cache.width = Math.floor(w * STATE.dpr);
        cache.height = Math.floor(h * STATE.dpr);
        var bctx = cache.getContext("2d");
        bctx.setTransform(STATE.dpr, 0, 0, STATE.dpr, 0, 0);

        var horizonY = h * 0.34;

        var skyGrad = bctx.createLinearGradient(0, 0, 0, horizonY);
        skyGrad.addColorStop(0, "#3fa9f5");
        skyGrad.addColorStop(0.45, "#7ecbfa");
        skyGrad.addColorStop(0.8, "#bfe8fb");
        skyGrad.addColorStop(1, "#fdf3d0");
        bctx.fillStyle = skyGrad;
        bctx.fillRect(0, 0, w, horizonY);

        var sunX = w * 0.78;
        var sunY = h * 0.14;
        var sunGlow = bctx.createRadialGradient(sunX, sunY, 0, sunX, sunY, w * 0.28);
        sunGlow.addColorStop(0, "rgba(255,250,210,0.95)");
        sunGlow.addColorStop(0.25, "rgba(255,235,150,0.55)");
        sunGlow.addColorStop(1, "rgba(255,235,150,0)");
        bctx.fillStyle = sunGlow;
        bctx.fillRect(0, 0, w, horizonY);

        bctx.beginPath();
        bctx.arc(sunX, sunY, Math.max(20, w * 0.035), 0, Math.PI * 2);
        bctx.fillStyle = "#fffbe8";
        bctx.fill();

        function drawCloud(cx, cy, scale) {
            bctx.save();
            bctx.globalAlpha = 0.85;
            bctx.fillStyle = "#ffffff";
            var puffs = [
                [0, 0, 1.0], [0.55, 0.08, 0.75], [-0.5, 0.1, 0.7],
                [0.2, -0.18, 0.6], [-0.2, -0.14, 0.55]
            ];
            for (var pI = 0; pI < puffs.length; pI++) {
                var p = puffs[pI];
                bctx.beginPath();
                bctx.ellipse(
                    cx + p[0] * 70 * scale, cy + p[1] * 70 * scale,
                    46 * scale * p[2], 30 * scale * p[2], 0, 0, Math.PI * 2
                );
                bctx.fill();
            }
            bctx.restore();
        }
        drawCloud(w * 0.18, h * 0.1, 1.1);
        drawCloud(w * 0.42, h * 0.06, 0.75);
        drawCloud(w * 0.62, h * 0.17, 0.6);

        var oceanGrad = bctx.createLinearGradient(0, horizonY, 0, horizonY + h * 0.16);
        oceanGrad.addColorStop(0, "#1a95c9");
        oceanGrad.addColorStop(0.5, "#1476a8");
        oceanGrad.addColorStop(1, "#0d5a86");
        bctx.fillStyle = oceanGrad;
        bctx.fillRect(0, horizonY, w, h * 0.16);

        bctx.save();
        bctx.globalAlpha = 0.18;
        bctx.strokeStyle = "#ffffff";
        bctx.lineWidth = 1.5;
        for (var wv = 0; wv < 10; wv++) {
            var wy = horizonY + 8 + wv * (h * 0.16) / 10;
            bctx.beginPath();
            for (var wx = 0; wx <= w; wx += 26) {
                var wOff = Math.sin(wx * 0.05 + wv) * 3;
                if (wx === 0) bctx.moveTo(wx, wy + wOff);
                else bctx.lineTo(wx, wy + wOff);
            }
            bctx.stroke();
        }
        bctx.restore();

        var sandTop = horizonY + h * 0.16;
        var sandGrad = bctx.createLinearGradient(0, sandTop, 0, h);
        sandGrad.addColorStop(0, "#f3d9a0");
        sandGrad.addColorStop(0.3, "#e4bd77");
        sandGrad.addColorStop(0.7, "#caa05c");
        sandGrad.addColorStop(1, "#a97d42");
        bctx.fillStyle = sandGrad;
        bctx.fillRect(0, sandTop, w, h - sandTop);

        bctx.save();
        bctx.globalAlpha = 0.06;
        bctx.fillStyle = "#5c3d16";
        for (var sp = 0; sp < 260; sp++) {
            var spx = Math.random() * w;
            var spy = sandTop + Math.random() * (h - sandTop);
            bctx.beginPath();
            bctx.arc(spx, spy, 1 + Math.random() * 1.4, 0, Math.PI * 2);
            bctx.fill();
        }
        bctx.restore();

        function drawPalmSilhouette(px, py, scaleX, scaleY) {
            bctx.save();
            bctx.translate(px, py);
            bctx.scale(scaleX, scaleY);
            bctx.fillStyle = "rgba(20,40,20,0.55)";
            bctx.beginPath();
            bctx.moveTo(-6, 0);
            bctx.quadraticCurveTo(-22, -70, -8, -150);
            bctx.quadraticCurveTo(0, -160, 8, -150);
            bctx.quadraticCurveTo(22, -70, 6, 0);
            bctx.closePath();
            bctx.fill();
            var fronds = [
                [-1.0, -1.5, 0.9], [-0.6, -1.9, 1.05], [0, -2.0, 1.15],
                [0.6, -1.9, 1.05], [1.0, -1.5, 0.9], [-1.3, -1.0, 0.7], [1.3, -1.0, 0.7]
            ];
            for (var f = 0; f < fronds.length; f++) {
                var fr = fronds[f];
                bctx.save();
                bctx.translate(0, -150);
                bctx.rotate(fr[0] * 0.55);
                bctx.beginPath();
                bctx.moveTo(0, 0);
                bctx.quadraticCurveTo(fr[0] * 40, -50 * fr[2], fr[1] * 70, -95 * fr[2]);
                bctx.quadraticCurveTo(fr[0] * 30, -40 * fr[2], 0, -6);
                bctx.closePath();
                bctx.fill();
                bctx.restore();
            }
            bctx.restore();
        }
        drawPalmSilhouette(w * 0.06, horizonY + h * 0.05, 0.9, 0.85);
        drawPalmSilhouette(w * 0.97, horizonY + h * 0.02, -0.65, 0.65);

        var vignette = bctx.createRadialGradient(
            w / 2, h / 2, Math.min(w, h) * 0.25,
            w / 2, h / 2, Math.max(w, h) * 0.85
        );
        vignette.addColorStop(0, "rgba(0,0,0,0)");
        vignette.addColorStop(1, "rgba(20,20,10,0.22)");
        bctx.fillStyle = vignette;
        bctx.fillRect(0, 0, w, h);

        scene.bgCache = cache;
        scene.bgCacheW = w;
        scene.bgCacheH = h;
        scene.horizonY = horizonY;
        scene.sandTop = sandTop;
    }

    function drawBackground() {
        var w = STATE.width;
        var h = STATE.height;

        if (scene.bgCache && scene.bgCacheW === w && scene.bgCacheH === h) {
            ctx.drawImage(scene.bgCache, 0, 0, w, h);
        } else {
            buildBackgroundCache();
            if (scene.bgCache) {
                ctx.drawImage(scene.bgCache, 0, 0, w, h);
            }
        }

        var matTop = scene.tableY - scene.cupBaseH * 1.4;
        if (matTop < (scene.sandTop || h * 0.5)) matTop = scene.sandTop || h * 0.5;
        var matGrad = ctx.createLinearGradient(0, matTop, 0, h);
        matGrad.addColorStop(0, "rgba(207,163,90,0.0)");
        matGrad.addColorStop(0.12, "rgba(178,132,70,0.55)");
        matGrad.addColorStop(1, "rgba(120,84,42,0.7)");
        ctx.fillStyle = matGrad;
        ctx.fillRect(0, matTop, w, h - matTop);

        ctx.save();
        ctx.globalAlpha = 0.14;
        ctx.strokeStyle = "#5a3c1c";
        ctx.lineWidth = 1;
        for (var my = matTop; my < h; my += 9) {
            ctx.beginPath();
            ctx.moveTo(0, my);
            ctx.lineTo(w, my);
            ctx.stroke();
        }
        ctx.restore();
    }

    /* ======================================================
       DRAWING: SPLASH PARTICLES (COCONUT WATER SPLASH)
       ====================================================== */
    function spawnSplash(x, y) {
        var count = 10 + Math.floor(Math.random() * 6);
        for (var i = 0; i < count; i++) {
            var angle = Math.PI + Math.random() * Math.PI;
            var speed = 60 + Math.random() * 130;
            scene.splashParticles.push({
                x: x,
                y: y,
                vx: Math.cos(angle) * speed * 0.6,
                vy: Math.sin(angle) * speed - 40,
                life: 0,
                maxLife: 380 + Math.random() * 260,
                r: 1.5 + Math.random() * 2.5
            });
        }
    }

    function updateSplashParticles(dt) {
        if (scene.splashParticles.length === 0) return;
        var gravity = 0.0016;
        for (var i = scene.splashParticles.length - 1; i >= 0; i--) {
            var p = scene.splashParticles[i];
            p.life += dt;
            if (p.life >= p.maxLife) {
                scene.splashParticles.splice(i, 1);
                continue;
            }
            p.vy += gravity * dt;
            p.x += p.vx * (dt / 1000);
            p.y += p.vy * (dt / 1000);
        }
    }

    function drawSplashParticles() {
        for (var i = 0; i < scene.splashParticles.length; i++) {
            var p = scene.splashParticles[i];
            var t = p.life / p.maxLife;
            var alpha = Math.max(0, 1 - t);
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r * (1 - t * 0.4), 0, Math.PI * 2);
            ctx.fillStyle = "rgba(255,255,255," + (alpha * 0.85) + ")";
            ctx.fill();
        }
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
       DRAWING: 3D POLISHED WOODEN BALL (MARBLE)
       ====================================================== */
    function drawBall(x, y, radius) {
        drawShadow(x, y + radius * 0.35, radius * 1.5, radius * 0.55, 0.5);

        var sphereGrad = ctx.createRadialGradient(
            x - radius * 0.35, y - radius * 0.4, radius * 0.08,
            x, y, radius * 1.15
        );
        sphereGrad.addColorStop(0, "#f3e2c2");
        sphereGrad.addColorStop(0.22, "#c99b5c");
        sphereGrad.addColorStop(0.5, "#8b5a2b");
        sphereGrad.addColorStop(0.78, "#5c3a1a");
        sphereGrad.addColorStop(1, "#2c1a0c");

        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fillStyle = sphereGrad;
        ctx.fill();

        /* subtle grain rings for a hand-carved feel */
        ctx.save();
        ctx.clip();
        ctx.globalAlpha = 0.12;
        ctx.strokeStyle = "#3a2410";
        ctx.lineWidth = Math.max(1, radius * 0.05);
        for (var g = 1; g <= 3; g++) {
            ctx.beginPath();
            ctx.ellipse(x, y, radius * (0.3 * g), radius * (0.14 * g), 0.6, 0, Math.PI * 2);
            ctx.stroke();
        }
        ctx.restore();

        /* warm cream highlight, matte -- softer & smaller than a glossy sheen */
        ctx.beginPath();
        ctx.arc(x - radius * 0.34, y - radius * 0.4, radius * 0.2, 0, Math.PI * 2);
        var specGrad = ctx.createRadialGradient(
            x - radius * 0.34, y - radius * 0.4, 0,
            x - radius * 0.34, y - radius * 0.4, radius * 0.2
        );
        specGrad.addColorStop(0, "rgba(255,244,220,0.55)");
        specGrad.addColorStop(1, "rgba(255,244,220,0)");
        ctx.fillStyle = specGrad;
        ctx.fill();
    }

    /* ======================================================
       DRAWING: HYPER-REALISTIC 3D COCONUT CUP
       ====================================================== */
    function drawCup(x, y, liftY, w, h, highlightSelected) {
        var topY = y - h - liftY;
        var bottomY = y - liftY;
        var topRadiusX = w * 0.5;
        var topRadiusY = w * 0.2;
        var bottomRadiusX = w * 0.6;
        var bottomRadiusY = w * 0.24;

        var shadowAlpha = Math.max(0.12, 0.5 - liftY * 0.004);
        drawShadow(x, y + bottomRadiusY * 0.4, bottomRadiusX * 1.25, bottomRadiusY * 0.9, shadowAlpha);

        ctx.save();

        /* organic semi-spherical husk shell body */
        ctx.beginPath();
        ctx.moveTo(x - bottomRadiusX, bottomY);
        ctx.quadraticCurveTo(x - topRadiusX * 1.08, (topY + bottomY) / 2, x - topRadiusX, topY);
        ctx.ellipse(x, topY, topRadiusX, topRadiusY, 0, Math.PI, 0, false);
        ctx.quadraticCurveTo(x + topRadiusX * 1.08, (topY + bottomY) / 2, x + bottomRadiusX, bottomY);
        ctx.ellipse(x, bottomY, bottomRadiusX, bottomRadiusY, 0, 0, Math.PI, false);
        ctx.closePath();

        var bodyGrad = ctx.createLinearGradient(x - bottomRadiusX, 0, x + bottomRadiusX, 0);
        if (highlightSelected) {
            bodyGrad.addColorStop(0, "#2a1a0c");
            bodyGrad.addColorStop(0.18, "#9c7a3a");
            bodyGrad.addColorStop(0.42, "#6b4e22");
            bodyGrad.addColorStop(0.6, "#3d2c14");
            bodyGrad.addColorStop(0.8, "#8a6a30");
            bodyGrad.addColorStop(1, "#221708");
        } else {
            bodyGrad.addColorStop(0, "#22120a");
            bodyGrad.addColorStop(0.16, "#5c3a20");
            bodyGrad.addColorStop(0.4, "#3d2314");
            bodyGrad.addColorStop(0.58, "#25150c");
            bodyGrad.addColorStop(0.8, "#4a2e18");
            bodyGrad.addColorStop(1, "#160c06");
        }
        ctx.fillStyle = bodyGrad;
        ctx.fill();

        /* fibrous husk shadow bands */
        ctx.save();
        ctx.clip();
        for (var band = 0; band < 5; band++) {
            ctx.globalAlpha = 0.09;
            ctx.strokeStyle = "#0e0803";
            ctx.lineWidth = Math.max(1, w * 0.025);
            var bandX = x - bottomRadiusX * 0.75 + band * (bottomRadiusX * 1.5 / 4);
            ctx.beginPath();
            ctx.moveTo(bandX, topY + topRadiusY);
            ctx.quadraticCurveTo(bandX + (band % 2 === 0 ? -6 : 6), (topY + bottomY) / 2, bandX, bottomY - bottomRadiusY * 0.2);
            ctx.stroke();
        }

        var sheenGrad = ctx.createLinearGradient(x - bottomRadiusX, topY, x - bottomRadiusX * 0.2, bottomY);
        sheenGrad.addColorStop(0, "rgba(255,235,200,0.16)");
        sheenGrad.addColorStop(0.35, "rgba(255,235,200,0.03)");
        sheenGrad.addColorStop(1, "rgba(255,235,200,0)");
        ctx.fillStyle = sheenGrad;
        ctx.beginPath();
        ctx.ellipse(x - w * 0.2, (topY + bottomY) / 2, w * 0.12, h * 0.4, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        ctx.restore();

        /* rim: outer husk ring */
        ctx.beginPath();
        ctx.ellipse(x, topY, topRadiusX, topRadiusY, 0, 0, Math.PI * 2);
        var rimGrad = ctx.createRadialGradient(x, topY, topRadiusX * 0.2, x, topY, topRadiusX);
        if (highlightSelected) {
            rimGrad.addColorStop(0, "#eadfc0");
            rimGrad.addColorStop(0.45, "#c9a24a");
            rimGrad.addColorStop(1, "#2a1a06");
        } else {
            rimGrad.addColorStop(0, "#4a2e18");
            rimGrad.addColorStop(0.45, "#2a1810");
            rimGrad.addColorStop(1, "#0c0602");
        }
        ctx.fillStyle = rimGrad;
        ctx.fill();

        /* crisp milky-white inner meat rim -- freshly sliced coconut edge */
        ctx.beginPath();
        ctx.ellipse(x, topY, topRadiusX * 0.8, topRadiusY * 0.7, 0, 0, Math.PI * 2);
        ctx.strokeStyle = highlightSelected ? "rgba(248,250,252,0.95)" : "rgba(248,250,252,0.88)";
        ctx.lineWidth = Math.max(2, w * 0.045);
        ctx.stroke();

        ctx.beginPath();
        ctx.ellipse(x, topY, topRadiusX * 0.66, topRadiusY * 0.56, 0, 0, Math.PI * 2);
        ctx.strokeStyle = "rgba(210,190,150,0.5)";
        ctx.lineWidth = Math.max(1, w * 0.014);
        ctx.stroke();
    }

    /* ======================================================
       MAIN RENDER LOOP
       ====================================================== */
    function renderFrame(timestamp) {
        if (!lastFrameTime) lastFrameTime = timestamp;
        var dt = timestamp - lastFrameTime;
        lastFrameTime = timestamp;

        if (STATE.phase === "loading") {
            rafId = requestAnimationFrame(renderFrame);
            return;
        }

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
            updateSplashParticles(dt);
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
            drawCup(cx, scene.tableY, totalLift, scene.cupBaseW, scene.cupBaseH, false);
        }

        drawSplashParticles();

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
            AudioEngine.playThud();
            spawnSplash(STATE.width / 2, scene.tableY);
            beginShuffling();
        }
    }

    /* ---------------- SHUFFLING PHASE ----------------
       Triple-axis wave shuffle: every swap combines
         1) horizontal sinusoidal cross-over (base position swap)
         2) vertical orbital sway (sin loop, simulating a 3D orbit)
         3) figure-eight intercept curve (Lissajous 2:1 wobble)
       Speed + amplitude scale with the chosen difficulty.
       ==================================================== */
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
        setHudMessage("TRACK THE COCONUT");
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
                lift: profile.lift,
                waveSpeed: profile.waveSpeed,
                orbitAmp: profile.orbitAmp,
                fig8Amp: profile.fig8Amp,
                orbitCycles: 1 + Math.round(profile.waveSpeed),
                fig8Seed: Math.random() * Math.PI * 2,
                fig8Dir: Math.random() > 0.5 ? 1 : -1
            };
            AudioEngine.playSwapWhoosh();
        }

        var sw = scene.activeSwap;
        var t = Math.min(1, (timestamp - sw.startTime) / sw.duration);
        var easedT = t < 0.5
            ? 2 * t * t
            : 1 - Math.pow(-2 * t + 2, 2) / 2;

        /* (1) horizontal cross-over: base swap position */
        var baseXA = sw.startXA + (sw.startXB - sw.startXA) * easedT;
        var baseXB = sw.startXB + (sw.startXA - sw.startXB) * easedT;

        /* (3) figure-eight intercept curve -- Lissajous 2:1 (x: 2*theta, y: theta) */
        var theta = t * Math.PI * sw.fig8Dir;
        var fig8X = Math.sin(theta * 2 + sw.fig8Seed) * sw.fig8Amp * Math.sin(Math.PI * t);
        var fig8Y = Math.cos(theta + sw.fig8Seed) * sw.fig8Amp * 0.6 * Math.sin(Math.PI * t);

        scene.cupCurrentX[sw.cupA] = baseXA + fig8X;
        scene.cupCurrentX[sw.cupB] = baseXB - fig8X;

        /* (2) vertical orbital sway -- loops up/down like a circular 3D orbit, on top of the swap arc */
        var arcLift = Math.sin(Math.PI * t) * sw.lift;
        var orbitalSway = Math.sin(t * Math.PI * 2 * sw.orbitCycles) * sw.orbitAmp * Math.sin(Math.PI * t);
        scene.cupLift[sw.cupA] = arcLift + orbitalSway + fig8Y;
        scene.cupLift[sw.cupB] = arcLift - orbitalSway - fig8Y;

        if (t >= 1) {
            scene.cupAtSlot[sw.slotA] = sw.cupB;
            scene.cupAtSlot[sw.slotB] = sw.cupA;
            scene.cupCurrentX[sw.cupA] = scene.slotX[sw.slotB];
            scene.cupCurrentX[sw.cupB] = scene.slotX[sw.slotA];
            scene.cupLift[sw.cupA] = 0;
            scene.cupLift[sw.cupB] = 0;
            AudioEngine.playCupClack();

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
        setHudMessage("SELECT THE TARGET SHELL");
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
        AudioEngine.playRevealWhoosh();
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
        scene.splashParticles = [];
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
        if (win) {
            AudioEngine.playWinStinger();
        } else {
            AudioEngine.playLoseStinger();
        }
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
            AudioEngine.init();
            AudioEngine.resume();
            diffButtons.forEach(function (b) { b.classList.remove("selected"); });
            btn.classList.add("selected");
            STATE.difficulty = btn.getAttribute("data-diff");
            updateStartButtonState();
        });
    });

    var cupSlots = cupSelector.querySelectorAll(".cup-slot");
    cupSlots.forEach(function (slot) {
        slot.addEventListener("click", function () {
            AudioEngine.init();
            AudioEngine.resume();
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
        AudioEngine.init();
        var resumePromise = AudioEngine.resume();
        AudioEngine.startMusic();
        if (resumePromise && typeof resumePromise.then === "function") {
            resumePromise.then(checkAudioUnlockState).catch(checkAudioUnlockState);
        }
        setTimeout(checkAudioUnlockState, 350);
        introOverlay.classList.add("hidden");
        hudMenuBtn.classList.remove("hidden-el");
        topRightHud.classList.remove("hidden-el");
        updatePaneStatus();
        initSceneForRound();
        beginDropping();
    });

    function checkAudioUnlockState() {
        if (AudioEngine.ctx && AudioEngine.ctx.state !== "running") {
            audioUnlockHint.classList.add("visible");
        } else {
            audioUnlockHint.classList.remove("visible");
        }
    }

    audioUnlockHint.addEventListener("click", function () {
        AudioEngine.init();
        var p = AudioEngine.resume();
        if (!AudioEngine.musicPlaying) {
            AudioEngine.startMusic();
        }
        if (p && typeof p.then === "function") {
            p.then(checkAudioUnlockState).catch(checkAudioUnlockState);
        } else {
            checkAudioUnlockState();
        }
    });

    /* Any tap anywhere in the game can also nudge a suspended
       AudioContext back to life -- some browsers only fully
       unlock audio after a couple of direct interactions. */
    document.addEventListener("pointerdown", function () {
        if (AudioEngine.ctx && AudioEngine.ctx.state !== "running") {
            AudioEngine.resume().then(checkAudioUnlockState).catch(function () {});
        }
    });

    muteBtn.addEventListener("click", function () {
        var nowMuted = AudioEngine.toggleMute();
        muteBtn.innerHTML = nowMuted ? "&#128263;" : "&#128266;";
        muteBtn.classList.toggle("muted", nowMuted);
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
        resetToMainGate();
    });

    btnRecalibrate.addEventListener("click", function () {
        closeControlPane();
        adjustShuffleSettings();
    });

    function resetToMainGate() {
        STATE.phase = "intro";
        STATE.paused = false;
        STATE.difficulty = null;
        STATE.cupCount = 3;
        STATE.round = 0;
        STATE.wins = 0;
        updateScorePill();
        hideResultOverlay();
        setHudMessage("");
        AudioEngine.stopMusic();
        audioUnlockHint.classList.remove("visible");
        hudMenuBtn.classList.add("hidden-el");
        topRightHud.classList.add("hidden-el");

        diffButtons.forEach(function (b) { b.classList.remove("selected"); });
        cupSlots.forEach(function (s) { s.classList.remove("selected"); });
        var defaultSlot = cupSelector.querySelector('[data-count="3"]');
        if (defaultSlot) defaultSlot.classList.add("selected");
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

    function adjustShuffleSettings() {
        STATE.phase = "intro";
        STATE.paused = false;
        hideResultOverlay();
        setHudMessage("");
        AudioEngine.stopMusic();
        audioUnlockHint.classList.remove("visible");
        hudMenuBtn.classList.add("hidden-el");
        topRightHud.classList.add("hidden-el");

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
    initLoadingVisuals();
    runLoadingBar();
    rafId = requestAnimationFrame(renderFrame);

})();
</script>
</body>
</html>
"""

components.html(game_html, height=700, scrolling=False)
