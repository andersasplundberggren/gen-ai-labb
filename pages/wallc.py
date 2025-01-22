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
        const levelWidth = 3000; // Total bredd på banan
        let mario = { x: 50, y: 300, width: 30, height: 30, color: 'red', dy: 0, onGround: true };
        const gravity = 0.5;
        const jumpPower = -10;
        const groundHeight = 50;
        const groundY = canvas.height - groundHeight;
        const camera = { x: 0 }; // Kamerans position

        // Kontrollvariabler
        let keys = {};

        // Lyssna efter tangenttryck
        document.addEventListener('keydown', (e) => { keys[e.key] = true; });
        document.addEventListener('keyup', (e) => { keys[e.key] = false; });

        function gameLoop() {
            // Rensa canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Rita mark (scrollande)
            ctx.fillStyle = 'green';
            ctx.fillRect(-camera.x, groundY, levelWidth, groundHeight);

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

            // Begränsa Mario till banans gränser
            mario.x = Math.max(0, Math.min(levelWidth - mario.width, mario.x));

            // Uppdatera kamerans position så att den följer Mario
            camera.x = Math.max(0, Math.min(mario.x - canvas.width / 2, levelWidth - canvas.width));

            // Rita Mario i relation till kameran
            ctx.fillStyle = mario.color;
            ctx.fillRect(mario.x - camera.x, mario.y, mario.width, mario.height);

            // Rita mållinjen
            ctx.fillStyle = 'blue';
            ctx.fillRect(levelWidth - 50 - camera.x, groundY - 50, 50, 50);

            // Kontrollera om Mario når mållinjen
            if (mario.x + mario.width >= levelWidth - 50) {
                alert('Grattis! Du klarade banan!');
                mario.x = 50; // Starta om
                mario.y = 300;
                camera.x = 0;
            }

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
st.set_page_config(page_title="Mario med start och slut", layout="centered")

st.title("Mario med start och slut")
st.write("Använd piltangenterna för att röra dig och mellanslag för att hoppa! Målet är att nå den blå rutan.")

# Visa spelet med hjälp av Streamlit Components
st.components.v1.html(game_code, height=500)
