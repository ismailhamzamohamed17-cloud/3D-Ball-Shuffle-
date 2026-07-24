import streamlit as st
import random

# --- MULTI-PLATFORM RESPONSIVE PAGE ARCHITECTURE ---
st.set_page_config(
    page_title="Realistic 3D Cup Shuffle",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit structural clutter to maximize mobile device focus
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
    st.session_state.stage = "MENU"  # Lifecycle Stages: MENU, GAME
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Easy"
if "game_id" not in st.session_state:
    st.session_state.game_id = 0
if "winning_cup" not in st.session_state:
    st.session_state.winning_cup = 0

# DIFFICULTY BALANCING PARAMETERS
DIFFICULTY_METRICS = {
    "Easy": {"cups": 3, "speed": 1.6},
    "Medium": {"cups": 4, "speed": 2.3},
    "Hard": {"cups": 5, "speed": 3.1}
}

# --- PROCESS INCOMING USER TAP ACTIONS ---
query_params = st.query_params
if "chosen_cup" in query_params:
    chosen = int(query_params["chosen_cup"])
    winning = int(query_params.get("winning_cup", 0))
    st.query_params.clear()
    
    if chosen == winning:
        st.session_state.score += 1
        st.session_state.streak += 1
        st.session_state.last_result = f"🎉 Correct! The ball was under Cup {chosen + 1}."
    else:
        st.session_state.streak = 0
        st.session_state.last_result = f"❌ Wrong! The ball was under Cup {winning + 1}."
    st.session_state.stage = "MENU"

# --- RENDER MAIN INTERACTIVE GAME WINDOW ---
st.markdown("<h2 style='text-align: center; margin-bottom: 0px;'>🔮 3D Real Shuffle</h2>", unsafe_allow_html=True)

# Multi-Column Scoreboard
col_sc1, col_sc2 = st.columns(2)
with col_sc1:
    st.metric("Total Score", st.session_state.score)
with col_sc2:
    st.metric("Streak 🔥", st.session_state.streak)

if st.session_state.last_result:
    st.info(st.session_state.last_result)

# Fetch configuration stats
metrics = DIFFICULTY_METRICS[st.session_state.difficulty]
num_cups = metrics["cups"]
shuffle_speed = metrics["speed"]

# --- HANDLE GRAPHICS LIFECYCLE ROUTING ---
if st.session_state.stage == "MENU":
    st.markdown("<p style='text-align: center;'>Choose difficulty below to start playing!</p>", unsafe_allow_html=True)
    
    # Inline Difficulty Grid Layout
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        if st.button("🟢 Easy", use_container_width=True):
            st.session_state.difficulty = "Easy"
            st.session_state.winning_cup = random.randint(0, DIFFICULTY_METRICS["Easy"]["cups"] - 1)
            st.session_state.game_id += 1
            st.session_state.last_result = None
            st.session_state.stage = "GAME"
            st.rerun()
    with btn_col2:
        if st.button("🟡 Medium", use_container_width=True):
            st.session_state.difficulty = "Medium"
            st.session_state.winning_cup = random.randint(0, DIFFICULTY_METRICS["Medium"]["cups"] - 1)
            st.session_state.game_id += 1
            st.session_state.last_result = None
            st.session_state.stage = "GAME"
            st.rerun()
    with btn_col3:
        if st.button("🔴 Hard", use_container_width=True):
            st.session_state.difficulty = "Hard"
            st.session_state.winning_cup = random.randint(0, DIFFICULTY_METRICS["Hard"]["cups"] - 1)
            st.session_state.game_id += 1
            st.session_state.last_result = None
            st.session_state.stage = "GAME"
            st.rerun()
            
    # Display Frozen Preview Table state while waiting
    num_cups = 3
    shuffle_speed = 0.0
    # --- FULLY RESIZEABLE THREE.JS WEBGL CONTAINER ---
THREE_JS_HTML = """
<div id="canvas-container" style="width: 100%; height: 380px; background: #12131a; border-radius: 16px; overflow: hidden; position: relative; box-shadow: inset 0 0 20px rgba(0,0,0,0.6);">
    <div id="status-overlay" style="position: absolute; top: 12px; left: 12px; color: #fff; font-family: sans-serif; background: rgba(0,0,0,0.8); padding: 6px 12px; border-radius: 15px; font-size: 12px; font-weight: bold; pointer-events: none; z-index: 10;">
        Ready...
    </div>
</div>

<script src="https://cloudflare.com"></script>
<script>
(function() {
    const container = document.getElementById('canvas-container');
    const statusOverlay = document.getElementById('status-overlay');
    
    const config = window.STREAMLIT_GAME_CONFIG || { numCups: 3, winningCup: 0, shuffleSpeed: 0.0, stage: "MENU" };
    const numCups = config.numCups;
    const winningCup = config.winningCup;
    const speedModifier = config.shuffleSpeed;
    const isMenuMode = (config.stage === "MENU");

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x12131a);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / 380, 0.1, 1000);
    // Dynamically adjust camera zoom depending on mobile vs desktop widths
    if(container.clientWidth < 480) {
        camera.position.set(0, 8.5, 11);
    } else {
        camera.position.set(0, 7.5, 9);
    }
    camera.lookAt(0, 1.2, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, 380);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    // Realistic Shader Illumination Setup
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const spotlight = new THREE.SpotLight(0xfff3e0, 1.2, 30, Math.PI / 4, 0.5, 1);
    spotlight.position.set(0, 12, 4);
    spotlight.castShadow = true;
    scene.add(spotlight);

    // Polished Obsidian Tabletop Surface Mesh
    const tableGeo = new THREE.CylinderGeometry(8, 8.5, 1, 32);
    const tableMat = new THREE.MeshStandardMaterial({ color: 0x1f222a, roughness: 0.2, metalness: 0.7 });
    const table = new THREE.Mesh(tableGeo, tableMat);
    table.position.y = -0.5;
    table.receiveShadow = true;
    scene.add(table);

    const cups = [];
    // Auto-scale layout item gaps on narrow smartphone displays
    const spacing = container.clientWidth < 480 ? 1.4 : 1.9;
    const startX = -((numCups - 1) * spacing) / 2;

    // Shiny Ceramic Red Ball Object
    const ballGeo = new THREE.SphereGeometry(0.25, 32, 32);
    const ballMat = new THREE.MeshStandardMaterial({ color: 0xff4757, roughness: 0.1, metalness: 0.3 });
    const ball = new THREE.Mesh(ballGeo, ballMat);
    ball.castShadow = true;
    ball.position.set(startX + (winningCup * spacing), 0.25, 0);
    scene.add(ball);

    const cupGroup = new THREE.Group();
    for (let i = 0; i < numCups; i++) {
        const cupContainer = new THREE.Group();
        cupContainer.position.set(startX + (i * spacing), 0, 0);

        // Smooth Procedural Mahogany Wood/Copper Material Texture
        const bodyGeo = new THREE.CylinderGeometry(0.5, 0.65, 1.5, 32);
        const bodyMat = new THREE.MeshStandardMaterial({ color: 0xffa726, roughness: 0.3, metalness: 0.4 });
        const body = new THREE.Mesh(bodyGeo, bodyMat);
        body.position.y = 0.75;
        body.castShadow = true;
        cupContainer.add(body);

        cupContainer.userData = { index: i, targetX: cupContainer.position.x };
        cups.push(cupContainer);
        cupGroup.add(cupContainer);
    }
    scene.add(cupGroup);

    // Dynamic State Routing Lifecycle Loops
    let gameState = isMenuMode ? "static_preview" : "reveal_ball"; 
    let stateTimer = 0;
    let shufflePhase = 0;
    const maxShuffleCycles = 6 + (speedModifier * 2);
    let swapLeftIdx = 0, swapRightIdx = 0;
    let swapProgress = 0;

    // Mobile-Friendly Touch Pointer Raycasting
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    function handleSelection(clientX, clientY) {
        if (gameState !== "pick") return;

        const rect = renderer.domElement.getBoundingClientRect();
        mouse.x = ((clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((clientY - rect.top) / rect.height) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(cupGroup.children, true);

        if (intersects.length > 0) {
            let hitCup = intersects.object;
            while (hitCup.parent && hitCup.parent !== cupGroup) {
                hitCup = hitCup.parent;
            }
            
            gameState = "resolve_choice";
            const chosenIndex = hitCup.userData.index;
            
            let liftTime = 0;
            function liftAnim() {
                liftTime += 0.05;
                hitCup.position.y = Math.sin(liftTime * Math.PI) * 1.5;
                if (chosenIndex !== winningCup) {
                    cups.forEach(c => {
                        if(c.userData.index === winningCup) c.position.y = Math.sin(liftTime * Math.PI) * 1.5;
                    });
                }
                
                if (liftTime >= 1) {
                    window.parent.location.search = "?chosen_cup=" + chosenIndex + "&winning_cup=" + winningCup;
                } else {
                    requestAnimationFrame(liftAnim);
                }
            }
            liftAnim();
        }
    }

    container.addEventListener('click', (e) => handleSelection(e.clientX, e.clientY));
    container.addEventListener('touchstart', (e) => {
        if(e.touches.length > 0) handleSelection(e.touches[0].clientX, e.touches[0].clientY);
    });

    function setupNextSwap() {
        swapLeftIdx = Math.floor(Math.random() * numCups);
        do {
            swapRightIdx = Math.floor(Math.random() * numCups);
        } while (swapLeftIdx === swapRightIdx);
        swapProgress = 0;
    }

    function animate() {
        requestAnimationFrame(animate);
        stateTimer += 0.01;

        if (gameState === "static_preview") {
            statusOverlay.innerText = "Select Difficulty Above To Play!";
        }
        else if (gameState === "reveal_ball") {
            statusOverlay.innerText = "👀 Watch carefully! Memorize the ball...";
            cups.forEach(c => {
                if (c.userData.index === winningCup) {
                    c.position.y = THREE.MathUtils.lerp(c.position.y, 1.6, 0.12);
                }
            });
            if (stateTimer > 1.5) {
                gameState = "drop_cups";
                stateTimer = 0;
            }
        } 
        else if (gameState === "drop_cups") {
            statusOverlay.innerText = "Hiding ball...";
            cups.forEach(c => {
                c.position.y = THREE.MathUtils.lerp(c.position.y, 0, 0.18);
            });
            if (stateTimer > 0.6) {
                gameState = "shuffle";
                setupNextSwap();
            }
        } 
        else if (gameState === "shuffle") {
            statusOverlay.innerText = "⚡ Shuffling cups... Keep tracking!";
            swapProgress += 0.045 * speedModifier;

            const cupA = cups[swapLeftIdx];
            const cupB = cups[swapRightIdx];

            const xA = cupA.userData.targetX;
            const xB = cupB.userData.targetX;

            const midX = (xA + xB) / 2;
            const radius = Math.abs(xA - xB) / 2;

            cupA.position.x = midX + radius * Math.cos(Math.PI + swapProgress * Math.PI);
            cupA.position.z = radius * Math.sin(swapProgress * Math.PI);

            cupB.position.x = midX + radius * Math.cos(swapProgress * Math.PI);
            cupB.position.z = -radius * Math.sin(swapProgress * Math.PI);

            if (swapProgress >= 1) {
                cupA.position.x = xB; cupA.position.z = 0;
                cupB.position.x = xA; cupB.position.z = 0;
                cupA.userData.targetX = xB;
                cupB.userData.targetX = xA;

                shufflePhase++;
                if (shufflePhase >= maxShuffleCycles) {
                    gameState = "pick";
                    cups.forEach(c => {
                        if (c.userData.index === winningCup) ball.position.x = c.position.x;
                    });
                } else {
                    setupNextSwap();
                }
            }
        } 
        else if (gameState === "pick") {
            statusOverlay.innerText = "👉 Tap on the cup hiding the ball!";
        }

        renderer.render(scene, camera);
    }

    animate();
})();
</script>
"""

# --- ATTACH PIPELINE LAYER FOR LIVE PROCESSING ---
config_injection = f"""
<script>
    window.STREAMLIT_GAME_CONFIG = {{
        numCups: {num_cups},
        winningCup: {st.session_state.winning_cup},
        shuffleSpeed: {shuffle_speed},
        stage: "{st.session_state.stage}"
    }};
</script>
"""

st.components.v1.html(config_injection + THREE_JS_HTML, height=395, scrolling=False)
st.markdown("<p style='text-align: center; color: gray; font-size: 11px;'>Optimized for mobile touchscreens and desktop viewports.</p>", unsafe_allow_html=True)
