import streamlit as st
import random

# --- SECURE RESPONSIVE PAGE ARCHITECTURE ---
st.set_page_config(
    page_title="Realistic 3D Cup Shuffle",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Remove layout padding gaps to center the mobile view surface nicely
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="stHeader"] { display: none !important; }
        .block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- TRACK SESSION STATES ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "stage" not in st.session_state:
    st.session_state.stage = "MENU"
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Easy"
if "winning_cup" not in st.session_state:
    st.session_state.winning_cup = 0

# CONFIGURATION BALANCING METRICS
DIFFICULTY_METRICS = {
    "Easy": {"cups": 3, "speed": 1.4},
    "Medium": {"cups": 4, "speed": 2.2},
    "Hard": {"cups": 5, "speed": 3.2}
}

# --- HEADER INTERACTIVE PANEL ---
st.markdown("<h2 style='text-align: center; margin-bottom: 0px;'>🔮 3D Real Shuffle</h2>", unsafe_allow_html=True)

col_sc1, col_sc2 = st.columns(2)
with col_sc1:
    st.metric("Total Score", st.session_state.score)
with col_sc2:
    st.metric("Streak 🔥", st.session_state.streak)

if st.session_state.last_result:
    st.info(st.session_state.last_result)

# --- ENGINE STATE CONTROLLER ---
if st.session_state.stage == "MENU":
    st.markdown("<p style='text-align: center;'>Choose difficulty below to start playing!</p>", unsafe_allow_html=True)
    
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        if st.button("🟢 Easy", use_container_width=True):
            st.session_state.difficulty = "Easy"
            st.session_state.winning_cup = random.randint(0, DIFFICULTY_METRICS["Easy"]["cups"] - 1)
            st.session_state.last_result = None
            st.session_state.stage = "GAME"
            st.rerun()
    with btn_col2:
        if st.button("🟡 Medium", use_container_width=True):
            st.session_state.difficulty = "Medium"
            st.session_state.winning_cup = random.randint(0, DIFFICULTY_METRICS["Medium"]["cups"] - 1)
            st.session_state.last_result = None
            st.session_state.stage = "GAME"
            st.rerun()
    with btn_col3:
        if st.button("🔴 Hard", use_container_width=True):
            st.session_state.difficulty = "Hard"
            st.session_state.winning_cup = random.randint(0, DIFFICULTY_METRICS["Hard"]["cups"] - 1)
            st.session_state.last_result = None
            st.session_state.stage = "GAME"
            st.rerun()

# Fetch parameters based on active choice state
metrics = DIFFICULTY_METRICS[st.session_state.difficulty]
num_cups = metrics["cups"]
shuffle_speed = metrics["speed"]
is_menu_mode_js = "true" if st.session_state.stage == "MENU" else "false"
# --- NATIVE SELF-CONTAINED HIGH-PERFORMANCE 3D ENGINE MODULE ---
CANVAS_GAME_HTML = """
<div id="canvas-container" style="width: 100%; height: 380px; background: #12131a; border-radius: 16px; overflow: hidden; position: relative; box-shadow: inset 0 0 20px rgba(0,0,0,0.6);">
    <canvas id="gameCanvas" style="width: 100%; height: 100%; display: block;"></canvas>
    <div id="status-overlay" style="position: absolute; top: 12px; left: 12px; color: #fff; font-family: sans-serif; background: rgba(0,0,0,0.8); padding: 6px 12px; border-radius: 15px; font-size: 12px; font-weight: bold; pointer-events: none; z-index: 10;">
        Ready...
    </div>
</div>

<script>
(function() {
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const container = document.getElementById('canvas-container');
    const statusOverlay = document.getElementById('status-overlay');
    
    // Injected properties from Python State Management layer
    const numCups = """ + str(num_cups) + """;
    const winningCup = """ + str(st.session_state.winning_cup) + """;
    const speedModifier = """ + str(shuffle_speed) + """;
    const isMenuMode = """ + is_menu_mode_js + """;

    // Layout resizing metrics
    function resize() {
        canvas.width = container.clientWidth * window.devicePixelRatio;
        canvas.height = 380 * window.devicePixelRatio;
        ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    }
    window.addEventListener('resize', resize);
    resize();

    // Constructing game objects
    const cups = [];
    const width = container.clientWidth;
    const spacing = width < 480 ? (width * 0.8) / numCups : 80;
    const startX = (width / 2) - (((numCups - 1) * spacing) / 2);

    for (let i = 0; i < numCups; i++) {
        cups.push({
            id: i,
            x: startX + (i * spacing),
            y: 220,
            targetX: startX + (i * spacing),
            liftY: 0
        });
    }

    let ballX = cups[winningCup].x;
    let ballVisible = !isMenuMode;
    let gameState = isMenuMode ? "static_preview" : "reveal_ball";

    let stateTimer = 0;
    let shufflePhase = 0;
    const maxShuffleCycles = 8 + (speedModifier * 2);
    let swapA = 0, swapB = 0, swapProgress = 0;

    function startNextSwap() {
        swapA = Math.floor(Math.random() * numCups);
        do {
            swapB = Math.floor(Math.random() * numCups);
        } while (swapA === swapB);
        swapProgress = 0;
    }

    // Touch and mouse intercept listener actions
    function processTouch(clientX, clientY) {
        if (gameState !== "pick") return;
        const rect = canvas.getBoundingClientRect();
        const clickX = clientX - rect.left;
        const clickY = clientY - rect.top;

        cups.forEach(cup => {
            // Distance checking logic
            const dx = clickX - cup.x;
            const dy = clickY - cup.y;
            if (Math.abs(dx) < 35 && dy > -60 && dy < 10) {
                gameState = "resolve_choice";
                let liftProgress = 0;
                
                function liftTransition() {
                    liftProgress += 0.05;
                    cup.liftY = Math.sin(liftProgress * Math.PI) * 70;
                    if (cup.id !== winningCup) {
                        cups[winningCup].liftY = Math.sin(liftProgress * Math.PI) * 70;
                    }
                    ballVisible = true;

                    if (liftProgress >= 1) {
                        window.parent.postMessage({
                            type: 'CUP_GAME_CHOICE',
                            chosen_cup: cup.id,
                            winning_cup: winningCup
                        }, '*');
                    } else {
                        requestAnimationFrame(liftTransition);
                    }
                }
                liftTransition();
            }
        });
    }

    canvas.addEventListener('click', (e) => processTouch(e.clientX, e.clientY));
    canvas.addEventListener('touchstart', (e) => {
        if(e.touches.length > 0) processTouch(e.touches[0].clientX, e.touches[0].clientY);
    });

    if (!isMenuMode) startNextSwap();

    // Graphic render animation engine loop pipeline
    function gameLoop() {
        stateTimer += 0.016;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Realistic tabletop background styling 
        const grd = ctx.createLinearGradient(0, 180, 0, 300);
        grd.addColorStop(0, '#1a1d24');
        grd.addColorStop(1, '#2c313d');
        ctx.fillStyle = grd;
        ctx.beginPath();
        ctx.ellipse(container.clientWidth / 2, 230, container.clientWidth * 0.45, 60, 0, 0, 2 * Math.PI);
        ctx.fill();

        // Game engine lifecycle loop routing
        if (gameState === "static_preview") {
            statusOverlay.innerText = "Select Difficulty Above To Play!";
            ballVisible = false;
        } 
        else if (gameState === "reveal_ball") {
            statusOverlay.innerText = "👀 Watch carefully! Memorize the ball...";
            cups[winningCup].liftY = Math.min(cups[winningCup].liftY + 4, 65);
            if (stateTimer > 1.8) {
                gameState = "drop_cups";
                stateTimer = 0;
            }
        } 
        else if (gameState === "drop_cups") {
            statusOverlay.innerText = "Hiding ball...";
            cups[winningCup].liftY = Math.max(cups[winningCup].liftY - 5, 0);
            if (stateTimer > 0.6) {
                gameState = "shuffle";
                ballVisible = false;
                startNextSwap();
            }
        } 
        else if (gameState === "shuffle") {
            statusOverlay.innerText = "⚡ Shuffling cups... Keep tracking!";
            swapProgress += 0.04 * speedModifier;

            const cA = cups[swapA];
            const cB = cups[swapB];

            const midX = (cA.targetX + cB.targetX) / 2;
            const dist = Math.abs(cA.targetX - cB.targetX) / 2;

            // Perfect dynamic arc paths using trigonometric formatting
            cA.x = midX + dist * Math.cos(Math.PI + swapProgress * Math.PI);
            cB.x = midX + dist * Math.cos(swapProgress * Math.PI);

            if (swapProgress >= 1) {
                cA.x = cA.targetX = cB.targetX;
                cB.x = cB.targetX = midX + dist;
                
                shufflePhase++;
                if (shufflePhase >= maxShuffleCycles) {
                    gameState = "pick";
                    ballX = cups.find(c => c.id === winningCup).x;
                } else {
                    startNextSwap();
                }
            }
        } 
        else if (gameState === "pick") {
            statusOverlay.innerText = "👉 Tap on the cup hiding the ball!";
        }

        // Draw Ball Object
        if (ballVisible) {
            ctx.beginPath();
            ctx.arc(ballX, 225, 12, 0, 2 * Math.PI);
            const ballGrd = ctx.createRadialGradient(ballX - 4, 221, 2, ballX, 225, 12);
            ballGrd.addColorStop(0, '#ff7675');
            ballGrd.addColorStop(1, '#d63031');
            ctx.fillStyle = ballGrd;
            ctx.fill();
            ctx.closePath();
        }

        # Draw Cups Objects
        cups.forEach(cup => {
            const cx = cup.x;
            const cy = cup.y - cup.liftY;

            ctx.beginPath();
            ctx.moveTo(cx - 24, cy);
            ctx.lineTo(cx - 18, cy - 55);
            ctx.lineTo(cx + 18, cy - 55);
            ctx.lineTo(cx + 24, cy);
            ctx.closePath();

            // High performance depth gradient shading
            const cupGrd = ctx.createLinearGradient(cx - 24, 0, cx + 24, 0);
            cupGrd.addColorStop(0, '#e67e22');
            cupGrd.addColorStop(0.3, '#f39c12');
            cupGrd.addColorStop(0.7, '#f1c40f');
            cupGrd.addColorStop(1, '#d35400');
            ctx.fillStyle = cupGrd;
            ctx.fill();

            // Draw cup rim outline
            ctx.beginPath();
            ctx.ellipse(cx, cy, 24, 6, 0, 0, 2 * Math.PI);
            ctx.fillStyle = '#d35400';
            ctx.fill();
        });

        requestAnimationFrame(gameLoop);
    }
    gameLoop();
})();
</script>
"""

# --- BACKEND LINK RECEIVER ---
receiver_script = """
<script>
window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'CUP_GAME_CHOICE') {
        const url = new URL(window.location.href);
        url.searchParams.set('chosen_cup', event.data.chosen_cup);
        url.searchParams.set('winning_cup', event.data.winning_cup);
        window.location.href = url.toString();
    }
});
</script>
"""

st.components.v1.html(CANVAS_GAME_HTML + receiver_script, height=395, scrolling=False)
st.markdown("<p style='text-align: center; color: gray; font-size: 11px;'>Optimized for mobile touchscreens and desktop viewports.</p>", unsafe_allow_html=True)
