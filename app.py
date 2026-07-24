import streamlit as st
import random

# --- SECURE MOBILE INTERACTIVE PAGE ARTIFACT ---
st.set_page_config(
    page_title="Realistic 3D Cup Shuffle",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Clean up layout view frame sizes to optimize screen space
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="stHeader"] { display: none !important; }
        .block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- TRACK LIFECYCLE SESSION STATES ---
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

# GAMEPLAY DIFFICULTY METRICS
DIFFICULTY_METRICS = {
    "Easy": {"cups": 3, "speed": 180},
    "Medium": {"cups": 4, "speed": 280},
    "Hard": {"cups": 5, "speed": 400}
}

# --- HEADER INTERACTIVE PANEL ---
st.markdown("<h2 style='text-align: center; margin-bottom: 0px;'>🔮 3D Real Shuffle</h2>", unsafe_allow_html=True)

col_sc1, col_sc2 = st.columns(2)
with col_sc1:
    st.metric("Total Score", st.session_state.score)
with col_sc2:
    st.metric("Streak 🔥", st.session_state.streak)

# --- CAPTURE CHOICE PAYLOAD ---
form_data = st.query_params

if "chosen_cup" in form_data:
    chosen = int(form_data["chosen_cup"])
    winning = int(form_data.get("winning_cup", 0))
    st.query_params.clear()
    
    if chosen == winning:
        st.session_state.score += 1
        st.session_state.streak += 1
        st.session_state.last_result = f"🎉 Correct! The ball was under Cup {chosen + 1}."
    else:
        st.session_state.streak = 0
        st.session_state.last_result = f"❌ Wrong! The ball was under Cup {winning + 1}."
    st.session_state.stage = "RESULT"
    st.rerun()

if st.session_state.last_result:
    st.info(st.session_state.last_result)

# --- MENU & NAVIGATION ROUTING LAYER ---
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

elif st.session_state.stage == "RESULT":
    # Show navigation options directly below the game box after a round completes
    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        if st.button("🔄 Play Again", type="primary", use_container_width=True):
            # Instant replay with current difficulty level selection
            st.session_state.winning_cup = random.randint(0, DIFFICULTY_METRICS[st.session_state.difficulty]["cups"] - 1)
            st.session_state.last_result = None
            st.session_state.stage = "GAME"
            st.rerun()
    with nav_col2:
        if st.button("🔙 Main Menu", use_container_width=True):
            # Back out completely to change modes
            st.session_state.last_result = None
            st.session_state.stage = "MENU"
            st.rerun()

# Map properties into temporary rendering hooks
metrics = DIFFICULTY_METRICS[st.session_state.difficulty]
num_cups = metrics["cups"]
shuffle_speed = metrics["speed"]
is_menu_or_result_mode = "true" if st.session_state.stage in ["MENU", "RESULT"] else "false"
# --- HIGH-COMPATIBILITY NATIVE CANVAS GAME ENGINE ---
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
    
    const numCups = """ + str(num_cups) + """;
    const winningCup = """ + str(st.session_state.winning_cup) + """;
    const baseSpeed = """ + str(shuffle_speed) + """;
    const isStaticMode = """ + is_menu_or_result_mode + """;

    function resize() {
        canvas.width = container.clientWidth * window.devicePixelRatio;
        canvas.height = 380 * window.devicePixelRatio;
        ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    }
    window.addEventListener('resize', resize);
    resize();

    const cups = [];
    const width = container.clientWidth;
    const spacing = width < 480 ? (width * 0.9) / numCups : 85;
    const startX = (width / 2) - (((numCups - 1) * spacing) / 2);

    for (let i = 0; i < numCups; i++) {
        cups.push({
            id: i,
            x: startX + (i * spacing),
            y: 230,
            targetX: startX + (i * spacing),
            liftY: isStaticMode ? 70 : 0
        });
    }

    let ballX = cups[winningCup].x;
    let ballVisible = isStaticMode;
    let gameState = isStaticMode ? "static_preview" : "reveal_ball";

    let stateTimer = 0;
    let shufflePhase = 0;
    const maxShuffleCycles = 6 + Math.floor(baseSpeed / 100);
    let swapA = 0, swapB = 0, swapProgress = 0;

    let lastTime = performance.now();

    function startNextSwap() {
        swapA = Math.floor(Math.random() * numCups);
        do {
            swapB = Math.floor(Math.random() * numCups);
        } while (swapA === swapB);
        swapProgress = 0;
    }

    function processTouch(clientX, clientY) {
        if (gameState !== "pick") return;
        const rect = canvas.getBoundingClientRect();
        const clickX = clientX - rect.left;
        const clickY = clientY - rect.top;

        cups.forEach(cup => {
            const dx = clickX - cup.x;
            const dy = clickY - cup.y;
            if (Math.abs(dx) < 38 && dy > -65 && dy < 15) {
                gameState = "resolve_choice";
                let liftProgress = 0;
                
                function liftTransition() {
                    liftProgress += 0.05;
                    cup.liftY = Math.sin(liftProgress * Math.PI) * 75;
                    if (cup.id !== winningCup) {
                        cups[winningCup].liftY = Math.sin(liftProgress * Math.PI) * 75;
                    }
                    ballVisible = true;

                    if (liftProgress >= 1) {
                        const targetUrl = window.parent.location.href.split('?') + 
                                          '?chosen_cup=' + cup.id + 
                                          '&winning_cup=' + winningCup;
                        window.parent.location.href = targetUrl;
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
        if(e.touches.length > 0) processTouch(e.touches.clientX, e.touches.clientY);
    });

    if (!isStaticMode) startNextSwap();

    function gameLoop(currentTime) {
        // DELTA TIME FRAME RECONCILIATION LAYER: Guarantees uniform rendering speed cross-platform
        let dt = (currentTime - lastTime) / 1000;
        if (dt > 0.1) dt = 0.1; // Cap jumps during tab switches
        lastTime = currentTime;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Render circular platform silhouette
        const grd = ctx.createLinearGradient(0, 190, 0, 310);
        grd.addColorStop(0, '#161920');
        grd.addColorStop(1, '#252a36');
        ctx.fillStyle = grd;
        ctx.beginPath();
        ctx.ellipse(container.clientWidth / 2, 240, container.clientWidth * 0.46, 55, 0, 0, 2 * Math.PI);
        ctx.fill();

        if (gameState === "static_preview") {
            statusOverlay.innerText = "Game Over or Menu Active!";
            ballVisible = true;
            ballX = cups.find(c => c.id === winningCup).x;
        } 
        else if (gameState === "reveal_ball") {
            statusOverlay.innerText = "👀 Remember the ball location...";
            stateTimer += dt;
            cups[winningCup].liftY = Math.min(cups[winningCup].liftY + (250 * dt), 70);
            if (stateTimer > 1.5) {
                gameState = "drop_cups";
                stateTimer = 0;
            }
        } 
        else if (gameState === "drop_cups") {
            statusOverlay.innerText = "Hiding ball...";
            stateTimer += dt;
            cups[winningCup].liftY = Math.max(cups[winningCup].liftY - (300 * dt), 0);
            if (stateTimer > 0.5) {
                gameState = "shuffle";
                ballVisible = false;
                startNextSwap();
            }
        } 
        else if (gameState === "shuffle") {
            statusOverlay.innerText = "⚡ Shuffling cups... Watch closely!";
            // Use real time duration multipliers instead of rigid frame indexes
            swapProgress += (baseSpeed / 100) * dt;

            const cA = cups[swapA];
            const cB = cups[swapB];

            const midX = (cA.targetX + cB.targetX) / 2;
            const dist = Math.abs(cA.targetX - cB.targetX) / 2;

            cA.x = midX + dist * Math.cos(Math.PI + swapProgress * Math.PI);
            cB.x = midX + dist * Math.cos(swapProgress * Math.PI);

            if (swapProgress >= 1) {
                const tempX = cA.targetX;
                cA.x = cA.targetX = cB.targetX;
                cB.x = cB.targetX = tempX;
                
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

        // Render Ball Object
        if (ballVisible) {
            ctx.beginPath();
            ctx.arc(ballX, 235, 12, 0, 2 * Math.PI);
            const ballGrd = ctx.createRadialGradient(ballX - 4, 231, 2, ballX, 235, 12);
            ballGrd.addColorStop(0, '#ff7675');
            ballGrd.addColorStop(1, '#d63031');
            ctx.fillStyle = ballGrd;
            ctx.fill();
            ctx.closePath();
        }

        // Render Cup Objects
        cups.forEach(cup => {
            const cx = cup.x;
            const cy = cup.y - cup.liftY;

            ctx.beginPath();
            ctx.moveTo(cx - 24, cy);
            ctx.lineTo(cx - 18, cy - 60);
            ctx.lineTo(cx + 18, cy - 60);
            ctx.lineTo(cx + 24, cy);
            ctx.closePath();

            const cupGrd = ctx.createLinearGradient(cx - 24, 0, cx + 24, 0);
            cupGrd.addColorStop(0, '#d35400');
            cupGrd.addColorStop(0.3, '#e67e22');
            cupGrd.addColorStop(0.7, '#f39c12');
            cupGrd.addColorStop(1, '#ba4a00');
            ctx.fillStyle = cupGrd;
            ctx.fill();

            ctx.beginPath();
            ctx.ellipse(cx, cy, 24, 6, 0, 0, 2 * Math.PI);
            ctx.fillStyle = '#ba4a00';
            ctx.fill();
        });

        requestAnimationFrame(gameLoop);
    }
    requestAnimationFrame(gameLoop);
})();
</script>
"""

# Push clean container out downstream 
st.components.v1.html(CANVAS_GAME_HTML, height=395, scrolling=False)
st.markdown("<p style='text-align: center; color: gray; font-size: 11px;'>Optimized for mobile touchscreens and desktop viewports.</p>", unsafe_allow_html=True)
