import streamlit as st
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="3D Realistic Cup Shuffle",
    page_icon="🔮",
    layout="centered"
)

# --- DIFFICULTY CONFIGURATION ---
DIFFICULTY_CONFIG = {
    "Easy": {"cups": 3, "speed": 1.5},
    "Medium": {"cups": 4, "speed": 2.2},
    "Hard": {"cups": 5, "speed": 3.2}
}

st.title("🔮 3D Realistic Cup Shuffle")
st.write("Track the ball in a real-time WebGL 3D environment. Higher difficulties increase cup counts.")

# --- SIDEBAR SETTINGS ---
st.sidebar.header("🎮 Game Settings")
difficulty = st.sidebar.selectbox(
    "Select Difficulty Level:",
    options=["Easy", "Medium", "Hard"]
)

config = DIFFICULTY_CONFIG[difficulty]
num_cups = config["cups"]
shuffle_speed = config["speed"]

# --- INITIALIZE SESSION STATE & FORCE AUTO-START ---
if "game_id" not in st.session_state:
    st.session_state.game_id = 1
    st.session_state.winning_cup = random.randint(0, num_cups - 1)
if "score" not in st.session_state:
    st.session_state.score = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# Manual Reset button
if st.button("🔀 Start New 3D Shuffle", type="primary", use_container_width=True):
    st.session_state.game_id += 1
    st.session_state.winning_cup = random.randint(0, num_cups - 1)
    st.session_state.last_result = None

# --- PROCESS JAVASCRIPT RESPONSES ---
query_params = st.query_params
if "chosen_cup" in query_params:
    chosen = int(query_params["chosen_cup"])
    winning = int(query_params.get("winning_cup", 0))
    st.query_params.clear()
    
    if chosen == winning:
        st.session_state.score += 1
        st.session_state.streak += 1
        st.session_state.last_result = f"🎉 Correct! You found it under Cup {chosen + 1}."
    else:
        st.session_state.streak = 0
        st.session_state.last_result = f"❌ Wrong! The ball was hiding under Cup {winning + 1}."

# --- SCOREBOARD DISPLAY ---
col_score1, col_score2 = st.columns(2)
with col_score1:
    st.metric("Total Score", st.session_state.score)
with col_score2:
    st.metric("Current Streak 🔥", st.session_state.streak)

if st.session_state.last_result:
    st.info(st.session_state.last_result)

if "winning_cup" not in st.session_state:
    st.session_state.winning_cup = random.randint(0, num_cups - 1)
    # --- EMBEDDED THREE.JS WEBGL RENDER ENGINE ---
THREE_JS_HTML = """
<div id="canvas-container" style="width: 100%; height: 450px; background: #1a1a24; border-radius: 12px; overflow: hidden; position: relative;">
    <div id="status-overlay" style="position: absolute; top: 15px; left: 15px; color: #fff; font-family: sans-serif; background: rgba(0,0,0,0.75); padding: 8px 15px; border-radius: 20px; font-size: 14px; pointer-events: none; z-index: 10;">
        Initializing Canvas...
    </div>
</div>

<script src="https://cloudflare.com"></script>
<script>
(function() {
    const container = document.getElementById('canvas-container');
    const statusOverlay = document.getElementById('status-overlay');
    
    const config = window.STREAMLIT_GAME_CONFIG || { numCups: 3, winningCup: 0, shuffleSpeed: 1.5, gameId: 1 };
    const numCups = config.numCups;
    const winningCup = config.winningCup;
    const speedModifier = config.shuffleSpeed;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a24);
    scene.fog = new THREE.FogExp2(0x1a1a24, 0.05);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / 450, 0.1, 1000);
    camera.position.set(0, 8, 12);
    camera.lookAt(0, 1.5, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, 450);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffeebb, 0.8);
    dirLight.position.set(5, 15, 5);
    dirLight.castShadow = true;
    scene.add(dirLight);

    const floorGeo = new THREE.PlaneGeometry(50, 50);
    const floorMat = new THREE.MeshStandardMaterial({ color: 0x22252c, roughness: 0.2, metalness: 0.8 });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    floor.receiveShadow = true;
    scene.add(floor);

    const cups = [];
    const spacing = 2.2;
    const startX = -((numCups - 1) * spacing) / 2;

    const ballGeo = new THREE.SphereGeometry(0.3, 32, 32);
    const ballMat = new THREE.MeshStandardMaterial({ color: 0xe63946, roughness: 0.1, metalness: 0.1 });
    const ball = new THREE.Mesh(ballGeo, ballMat);
    ball.castShadow = true;
    ball.position.set(startX + (winningCup * spacing), 0.3, 0);
    scene.add(ball);

    const cupGroup = new THREE.Group();
    for (let i = 0; i < numCups; i++) {
        const cupContainer = new THREE.Group();
        cupContainer.position.set(startX + (i * spacing), 0, 0);

        const bodyGeo = new THREE.CylinderGeometry(0.6, 0.8, 1.8, 32);
        const bodyMat = new THREE.MeshStandardMaterial({ color: 0xd4a373, roughness: 0.4, metalness: 0.3 });
        const body = new THREE.Mesh(bodyGeo, bodyMat);
        body.position.y = 0.9;
        body.castShadow = true;
        cupContainer.add(body);

        cupContainer.userData = { index: i, targetX: cupContainer.position.x };
        cups.push(cupContainer);
        cupGroup.add(cupContainer);
    }
    scene.add(cupGroup);

    let gameState = "reveal_ball"; 
    let stateTimer = 0;
    let shufflePhase = 0;
    const maxShuffleCycles = 8 + (speedModifier * 2);
    let swapLeftIdx = 0, swapRightIdx = 0;
    let swapProgress = 0;

    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    container.addEventListener('click', function(event) {
        if (gameState !== "pick") return;

        const rect = renderer.domElement.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

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

        if (gameState === "reveal_ball") {
            statusOverlay.innerText = "Remember the ball location...";
            cups.forEach(c => {
                if (c.userData.index === winningCup) {
                    c.position.y = THREE.MathUtils.lerp(c.position.y, 1.8, 0.1);
                }
            });
            if (stateTimer > 1.8) {
                gameState = "drop_cups";
                stateTimer = 0;
            }
        } 
        else if (gameState === "drop_cups") {
            statusOverlay.innerText = "Hiding ball...";
            cups.forEach(c => {
                c.position.y = THREE.MathUtils.lerp(c.position.y, 0, 0.15);
            });
            if (stateTimer > 0.8) {
                gameState = "shuffle";
                setupNextSwap();
            }
        } 
        else if (gameState === "shuffle") {
            statusOverlay.innerText = "Shuffling dynamically... Watch closely!";
            swapProgress += 0.04 * speedModifier;

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
                cupA.position.x = xB;
                cupA.position.z = 0;
                cupB.position.x = xA;
                cupB.position.z = 0;

                cupA.userData.targetX = xB;
                cupB.userData.targetX = xA;

                shufflePhase++;
                if (shufflePhase >= maxShuffleCycles) {
                    gameState = "pick";
                    cups.forEach(c => {
                        if (c.userData.index === winningCup) {
                            ball.position.x = c.position.x;
                        }
                    });
                } else {
                    setupNextSwap();
                }
            }
        } 
        else if (gameState === "pick") {
            statusOverlay.innerText = "Click on the 3D Cup you think holds the ball!";
        }

        renderer.render(scene, camera);
    }

    animate();

})();
</script>
"""

# --- INJECT CONFIG AND RENDER ENGINE ---
config_injection = f"""
<script>
    window.STREAMLIT_GAME_CONFIG = {{
        numCups: {num_cups},
        winningCup: {st.session_state.winning_cup},
        shuffleSpeed: {shuffle_speed},
        gameId: {st.session_state.game_id}
    }};
</script>
"""

st.components.v1.html(config_injection + THREE_JS_HTML, height=470, scrolling=False)
st.markdown("---")
st.caption("Powered by Streamlit engine and Three.js real-time WebGL rendering wrappers.")
