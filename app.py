import streamlit as st

# --- IPHONE PERFECT RESPONSIVE PAGE ENGINE ---
st.set_page_config(
    page_title="Realistic 3D Cup Shuffle",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Deep inject custom CSS style layers to format full mobile viewport matching
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="stHeader"] { display: none !important; }
        .block-container { padding: 0px !important; max-width: 100% !important; }
        iframe { width: 100% !important; height: 560px !important; border: none !important; }
    </style>
""", unsafe_allow_html=True)

# Capture internal choice payloads securely to avoid rendering errors
form_data = st.query_params
if "save_score" in form_data:
    st.session_state.score = int(form_data["save_score"])
    st.session_state.streak = int(form_data["save_streak"])
    st.query_params.clear()

# Initialize fallbacks locally so state structures survive resets
current_score = st.session_state.get("score", 0)
current_streak = st.session_state.get("streak", 0)
# --- FULL GRAPHICS CONTAINER LAYER ENGINE ---
IPHONE_GAME_HTML = f"""
<div id="canvas-container" style="width: 100%; height: 550px; background: #0b0c10; overflow: hidden; position: relative; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; -webkit-user-select: none; user-select: none; touch-action: none;">
    <canvas id="gameCanvas" style="width: 100%; height: 100%; display: block;"></canvas>
</div>

<script>
(function() {{
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const container = document.getElementById('canvas-container');

    // Telemetry storage sync blocks
    let score = {current_score};
    let streak = {current_streak};
    let lastResultMsg = "";
    let lastResultType = ""; 

    let numCups = 3;
    let baseSpeed = 180;
    let winningCup = 0;
    let chosenDifficulty = "Easy";

    let gameState = "MENU"; 
    const cups = [];
    
    let ballX = 0;
    let ballY = 320;
    let ballVisible = false;

    let stateTimer = 0;
    let shufflePhase = 0;
    let maxShuffleCycles = 6;
    let swapA = 0, swapB = 0, swapProgress = 0;
    let lastTime = performance.now();

    function resize() {{
        const dpr = window.devicePixelRatio || 1;
        canvas.width = container.clientWidth * dpr;
        canvas.height = 550 * dpr;
        ctx.scale(dpr, dpr);
    }}
    window.addEventListener('resize', resize);
    resize();

    function initGame(difficulty) {{
        chosenDifficulty = difficulty;
        if (difficulty === "Easy") {{ numCups = 3; baseSpeed = 220; maxShuffleCycles = 6; }}
        else if (difficulty === "Medium") {{ numCups = 4; baseSpeed = 340; maxShuffleCycles = 8; }}
        else if (difficulty === "Hard") {{ numCups = 5; baseSpeed = 460; maxShuffleCycles = 11; }}

        winningCup = Math.floor(Math.random() * numCups);
        const width = container.clientWidth;
        const spacing = width < 400 ? (width * 0.88) / numCups : 75;
        const startX = (width / 2) - (((numCups - 1) * spacing) / 2);

        cups.length = 0;
        for (let i = 0; i < numCups; i++) {{
            cups.push({{
                id: i,
                x: startX + (i * spacing),
                y: 320,
                targetX: startX + (i * spacing),
                liftY: 0
            }});
        }}

        ballX = cups[winningCup].x;
        ballVisible = true;
        gameState = "REVEAL";
        stateTimer = 0;
        shufflePhase = 0;
    }}

    function startNextSwap() {{
        swapA = Math.floor(Math.random() * numCups);
        do {{
            swapB = Math.floor(Math.random() * numCups);
        }} while (swapA === swapB);
        swapProgress = 0;
    }}

    function handleInput(clickX, clickY) {{
        const width = container.clientWidth;

        if (gameState === "MENU") {{
            const bx = width / 2;
            if (clickX > bx - 70 && clickX < bx + 70) {{
                if (clickY > 210 && clickY < 250) initGame("Easy");
                else if (clickY > 270 && clickY < 310) initGame("Medium");
                else if (clickY > 330 && clickY < 370) initGame("Hard");
            }}
        }} 
        else if (gameState === "PICK") {{
            cups.forEach(cup => {{
                const dx = clickX - cup.x;
                const dy = clickY - cup.y;
                if (Math.abs(dx) < 35 && dy > -65 && dy < 15) {{
                    gameState = "RESOLVE";
                    let liftProgress = 0;
                    
                    function animateLift() {{
                        liftProgress += 0.04;
                        cup.liftY = Math.sin(liftProgress * Math.PI) * 75;
                        if (cup.id !== winningCup) {{
                            cups[winningCup].liftY = Math.sin(liftProgress * Math.PI) * 75;
                        }}
                        ballVisible = true;

                        if (liftProgress >= 1) {{
                            if (cup.id === winningCup) {{
                                score++; streak++;
                                lastResultMsg = "🎉 Correct! You tracked it.";
                                lastResultType = "WIN";
                            }} else {{
                                streak = 0;
                                lastResultMsg = "❌ Wrong! Better luck next time.";
                                lastResultType = "LOSS";
                            }}
                            gameState = "RESULT";
                            window.parent.postMessage({{type: 'SCORE_UPDATE', s: score, k: streak}}, '*');
                        }} else {{
                            requestAnimationFrame(animateLift);
                        }}
                    }}
                    animateLift();
                }}
            }});
        }} 
        else if (gameState === "RESULT") {{
            const cx = width / 2;
            if (clickX > cx - 110 && clickX < cx - 10 && clickY > 440 && clickY < 485) {{
                initGame(chosenDifficulty);
            }}
            if (clickX > cx + 10 && clickX < cx + 110 && clickY > 440 && clickY < 485) {{
                gameState = "MENU";
            }}
        }}
    }}

    canvas.addEventListener('click', (e) => {{
        const r = canvas.getBoundingClientRect();
        handleInput(e.clientX - r.left, e.clientY - r.top);
    }});
    canvas.addEventListener('touchstart', (e) => {{
        if(e.touches.length > 0) {{
            const r = canvas.getBoundingClientRect();
            handleInput(e.touches[0].clientX - r.left, e.touches[0].clientY - r.top);
        }}
    }});
"""
  # Continuation layer running the canvas frame graphics matrices
    function frame(time) {{
        let dt = (time - lastTime) / 1000;
        if (dt > 0.1) dt = 0.1;
        lastTime = time;

        const w = container.clientWidth;
        ctx.clearRect(0, 0, w, 550);

        // --- DRAW HEADER DISPLAY HUD Area ---
        ctx.fillStyle = "#1f2833";
        ctx.fillRect(0, 0, w, 70);
        
        ctx.font = "bold 15px -apple-system";
        ctx.fillStyle = "#45f3ff";
        ctx.textAlign = "left";
        ctx.fillText("SCORE: " + score, 20, 42);
        
        ctx.fillStyle = "#ff4d4d";
        ctx.textAlign = "right";
        ctx.fillText("STREAK: " + streak + " 🔥", w - 20, 42);
        ctx.textAlign = "center";

        if (gameState === "MENU") {{
            ctx.font = "bold 24px -apple-system";
            ctx.fillStyle = "#fff";
            ctx.fillText("🔮 3D Cup Shuffle", w / 2, 135);
            ctx.font = "14px -apple-system";
            ctx.fillStyle = "#86c232";
            ctx.fillText("Select difficulty inside the window to play", w / 2, 165);

            const renderBtn = (y, txt, clr) => {{
                ctx.fillStyle = "#1a1a24";
                ctx.strokeStyle = clr;
                ctx.lineWidth = 2;
                ctx.beginPath(); ctx.roundRect((w/2) - 70, y, 140, 40, 10); ctx.fill(); ctx.stroke();
                ctx.font = "bold 14px -apple-system"; ctx.fillStyle = "#fff";
                ctx.fillText(txt, w/2, y + 24);
            }};
            renderBtn(210, "🟢 Easy", "#2ecc71");
            renderBtn(270, "🟡 Medium", "#f1c40f");
            renderBtn(330, "🔴 Hard", "#e74c3c");
        }} 
        else {{
            const tableGrd = ctx.createLinearGradient(0, 270, 0, 410);
            tableGrd.addColorStop(0, '#12141c'); tableGrd.addColorStop(1, '#232733');
            ctx.fillStyle = tableGrd;
            ctx.beginPath(); ctx.ellipse(w / 2, 330, w * 0.46, 50, 0, 0, 2 * Math.PI); ctx.fill();

            if (gameState === "REVEAL") {{
                ctx.font = "bold 15px -apple-system"; ctx.fillStyle = "#45f3ff";
                ctx.fillText("👀 Memorize Ball Position!", w / 2, 130);
                
                stateTimer += dt;
                ballX = cups[winningCup].x;
                cups[winningCup].liftY = Math.min(cups[winningCup].liftY + (250 * dt), 70);
                if (stateTimer > 1.6) {{ gameState = "DROP"; stateTimer = 0; }}
            }} 
            else if (gameState === "DROP") {{
                ctx.font = "bold 15px -apple-system"; ctx.fillStyle = "#45f3ff";
                ctx.fillText("Hiding Ball...", w / 2, 130);
                
                stateTimer += dt;
                cups[winningCup].liftY = Math.max(cups[winningCup].liftY - (300 * dt), 0);
                if (stateTimer > 0.5) {{
                    gameState = "SHUFFLE";
                    ballVisible = false; 
                    startNextSwap();
                }}
            }} 
            else if (gameState === "SHUFFLE") {{
                ctx.font = "bold 15px -apple-system"; ctx.fillStyle = "#ff9f43";
                ctx.fillText("⚡ Shuffling... Watch closely!", w / 2, 130);
                
                swapProgress += (baseSpeed / 100) * dt;
                const cA = cups[swapA]; const cB = cups[swapB];
                const midX = (cA.targetX + cB.targetX) / 2;
                const dist = Math.abs(cA.targetX - cB.targetX) / 2;

                cA.x = midX + dist * Math.cos(Math.PI + swapProgress * Math.PI);
                cB.x = midX + dist * Math.cos(swapProgress * Math.PI);

                if (swapProgress >= 1) {{
                    const tempX = cA.targetX;
                    cA.x = cA.targetX = cB.targetX;
                    cB.x = cB.targetX = tempX;
                    
                    shufflePhase++;
                    if (shufflePhase >= maxShuffleCycles) {{
                        gameState = "PICK";
                        ballX = cups.find(c => c.id === winningCup).x;
                    }} else {{
                        startNextSwap();
                    }}
                }}
            }} 
            else if (gameState === "PICK") {{
                ctx.font = "bold 16px -apple-system"; ctx.fillStyle = "#2ecc71";
                ctx.fillText("👉 Tap the cup hiding the ball!", w / 2, 130);
            }}
            else if (gameState === "RESULT") {{
                ctx.font = "bold 18px -apple-system";
                ctx.fillStyle = (lastResultType === "WIN") ? "#2ecc71" : "#e74c3c";
                ctx.fillText(lastResultMsg, w / 2, 125);

                const drawNavBtn = (x, txt, active) => {{
                    ctx.fillStyle = active ? "#e67e22" : "#1a1a24";
                    ctx.strokeStyle = "#fff";
                    ctx.lineWidth = 1;
                    ctx.beginPath(); ctx.roundRect(x, 440, 100, 45, 8); ctx.fill(); ctx.stroke();
                    ctx.font = "bold 13px -apple-system"; ctx.fillStyle = "#fff";
                    ctx.fillText(txt, x + 50, 467);
                }};
                drawNavBtn((w/2) - 110, "🔄 Replay", true);
                drawNavBtn((w/2) + 10, "🔙 Menu", false);
            }}

            if (ballVisible) {{
                ctx.beginPath(); ctx.arc(ballX, ballY, 13, 0, 2 * Math.PI);
                const bGrd = ctx.createRadialGradient(ballX - 4, ballY - 4, 2, ballX, ballY, 13);
                bGrd.addColorStop(0, '#ff7675'); bGrd.addColorStop(1, '#d63031');
                ctx.fillStyle = bGrd; ctx.fill(); ctx.closePath();
            }}

            cups.forEach(cup => {{
                const cx = cup.x; const cy = cup.y - cup.liftY;
                ctx.beginPath();
                ctx.moveTo(cx - 25, cy); ctx.lineTo(cx - 18, cy - 62);
                ctx.lineTo(cx + 18, cy - 62); ctx.lineTo(cx + 24, cy);
                ctx.closePath();

                const cGrd = ctx.createLinearGradient(cx - 24, 0, cx + 24, 0);
                cGrd.addColorStop(0, '#d35400'); cGrd.addColorStop(0.3, '#e67e22');
                cGrd.addColorStop(0.7, '#f39c12'); cGrd.addColorStop(1, '#ba4a00');
                ctx.fillStyle = cGrd; ctx.fill();

                ctx.beginPath(); ctx.ellipse(cx, cy, 24, 6, 0, 0, 2 * Math.PI);
                ctx.fillStyle = '#ba4a00'; ctx.fill();
            }});
        }}
        requestAnimationFrame(frame);
    }}
    requestAnimationFrame(frame);
}})();

window.addEventListener('message', function(event) {{
    if (event.data && event.data.type === 'SCORE_UPDATE') {{
        const url = new URL(window.location.href);
        url.searchParams.set('save_score', event.data.s);
        url.searchParams.set('save_streak', event.data.k);
        window.parent.location.href = url.toString();
    }}
}});
</script>
"""

st.components.v1.html(IPHONE_GAME_HTML, height=560, scrolling=False)
