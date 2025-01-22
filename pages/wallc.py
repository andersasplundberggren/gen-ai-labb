import streamlit as st

# HTML och JavaScript för spelet
game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        canvas {
            background: #87CEEB;
            display: block;
            margin: 0 auto;
            border: 2px solid #000;
        }
        body {
            font-family: Arial, sans-serif;
        }
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="800" height="400"></canvas>
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        // Spelvariabler
        let mario = { x: 50, y: 300, width: 30, height: 30, color: 'red', dy: 0, onGround: true };
        const gravity = 0.5;
        const jumpPower = -10;
        const groundHeight = 50;
        const groundY = canvas.height - groundHeight;

        // Kontrollvariabler
        let keys = {};

        // Lyssna efter tangenttryck
        document.addEventListener('keydown', (e) => { keys[e.key] = true; });
        document.addEventListener('keyup', (e) => { keys[e.key] = false; });

        function gameLoop() {
            // Rensa canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Rita mark
            ctx.fillStyle = 'green';
            ctx.fillRect(0, groundY, canvas.width, groundHeight);

            // Hoppa
            if (keys[' '] && mario.onGround) {
                mario.dy = jumpPower;
                mario.onGround = false;
            }

            // Rörelse åt höger/vänster
            if (keys['ArrowRight']) mario.x += 5;
            if (keys['ArrowLeft']) mario.x -= 5;

            // Gravitation
            mario.dy += gravity;
            mario.y += mario.dy;

            // Kollisionsdetektion med marken
            if (mario.y + mario.height > groundY) {
                mario.y = groundY - mario.height;
                mario.dy = 0;
                mario.onGround = true;
            }

            // Begränsa Mario till canvasens gränser
            mario.x = Math.max(0, Math.min(canvas.width - mario.width, mario.x));

            // Rita Mario
            ctx.fillStyle = mario.color;
            ctx.fillRect(mario.x, mario.y, mario.width, mario.height);

            // Loopa spelet
            requestAnimationFrame(gameLoop);
        }

        // Starta spelet
        gameLoop();
    </script>
</body>
</html>
"""

# Streamlit-konfiguration
st.set_page_config(page_title="Förenklad Mario-upplevelse", layout="centered")

st.title("Förenklad Mario-upplevelse")
st.write("Använd piltangenterna för att röra dig och mellanslag för att hoppa!")

# Visa spelet med hjälp av Streamlit Components
st.components.v1.html(game_code, height=500)
