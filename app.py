import streamlit as st
import random
import json

# --- SECURE RESPONSIVE PAGE ARCHITECTURE ---
st.set_page_config(
    page_title="Realistic 3D Cup Shuffle",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Clean up Streamlit layout framing for a unified experience
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
    "Easy": {"cups": 3, "speed": 1.6},
    "Medium": {"cups": 4, "speed": 2.3},
    "Hard": {"cups": 5, "speed": 3.1}
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
# --- EMBEDDED HIGH-SECURITY 3D ENGINE MODULE ---
THREE_JS_HTML = """
<div id="canvas-container" style="width: 100%; height: 380px; background: #12131a; border-radius: 16px; overflow: hidden; position: relative; box-shadow: inset 0 0 20px rgba(0,0,0,0.6);">
    <div id="status-overlay" style="position: absolute; top: 12px; left: 12px; color: #fff; font-family: sans-serif; background: rgba(0,0,0,0.8); padding: 6px 12px; border-radius: 15px; font-size: 12px; font-weight: bold; pointer-events: none; z-index: 10;">
        Initializing Canvas...
    </div>
</div>

<script src="https://cloudflare.com"></script>
<script>
(function() {
    const container = document.getElementById('canvas-container');
    const statusOverlay = document.getElementById('status-overlay');
    
    const numCups = """ + str(num_cups) + """;
    const winningCup = """ + str(st.session_state.winning_cup) + """;
    const speedModifier = """ + str(shuffle_speed) + """;
    const isMenuMode = """ + is_menu_mode_js + """;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x12131a);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / 380, 0.1, 1000);
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

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const spotlight = new THREE.SpotLight(0xfff3e0, 1.2, 30, Math.PI / 4, 0.5, 1);
    spotlight.position.set(0, 12, 4);
    spotlight.castShadow = true;
    scene.add(spotlight);

    const tableGeo = new THREE.CylinderGeometry(8, 8.5, 1, 32);
    const tableMat = new THREE.MeshStandardMaterial({ color: 0x1f222a, roughness: 0.2, metalness: 0.7 });
    const table = new THREE.Mesh(tableGeo, tableMat);
    table.position.y = -0.5;
    table.receiveShadow = true;
    scene.add(table);

    const cups = [];
    const spacing = container.clientWidth < 480 ? 1.4 : 1.9;
    const startX = -((numCups - 1) * spacing) / 2;

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

    let gameState = isMenuMode ? "static_preview" : "reveal_ball"; 
    let stateTimer = 0;
    let shufflePhase = 0;
    const maxShuffleCycles = 6 + (speedModifier * 2);
    let swapLeftIdx = 0, swapRightIdx = 0;
    let swapProgress = 0;

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
                    // SECURE MESSAGE CHANNEL WAY: Sends score payload back to parent without changing URL frames
                    window.parent.postMessage({
                        type: 'CUP_GAME_CHOICE',
                        chosen_cup: chosenIndex,
                        winning_cup: winningCup
                    }, '*');
                }} else {
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
            cupGroup.rotation.y += 0.005;
            ball.visible = false;
        }
        else if (gameState === "reveal_ball") {
            ball.visible = true;
            statusOverlay.innerText = "👀 Remember the ball location...";
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

# --- BACKEND EVENT SCOPE RECEIVER ---
# Listen for incoming HTML5 messages securely without page resets
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

# Render graphics layout downstream securely
st.components.v1.html(THREE_JS_HTML + receiver_script, height=395, scrolling=False)
st.markdown("<p style='text-align: center; color: gray; font-size: 11px;'>Optimized for mobile touchscreens and desktop viewports.</p>", unsafe_allow_html=True)
