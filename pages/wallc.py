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

        // Lista över hinder
        const obstacles = [
            { x: 400, y: groundY - 20, width: 20, height: 20 },
            { x: 800, y: groundY - 40, width: 40, height: 40 },
            { x: 1200, y: groundY - 30, width: 30, height: 30 },
            { x: 1800, y: groundY - 50, width: 50, height: 50 }
        ];

        // Lista över mynt
        const coins = [
            { x: 300, y: groundY - 60, width: 15, height: 15 },
            { x: 700, y: groundY - 90, width: 15, height: 15 },
            { x: 1100, y: groundY - 70, width: 15, height: 15 },
            { x: 1500, y: groundY - 100, width: 15, height: 15 }
        ];

        // Poäng och timer
        let score = 0;
        let startTime = Date.now();

        // Kontrollvariabler
        let keys = {};

        // Lyssna efter tangenttryck
        document.addEventListener('keydown', (e) => { keys[e.key] = true; });
        document.addEventListener('keyup', (e) => { keys[e.key] = false; });

        function gameLoop() {
            // Rensa canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Rita bakgrund (varierande färg baserat på kamerans position)
            const section = Math.floor(camera.x / 800) % 2;
            ctx.fillStyle = section === 0 ? '#87CEEB' : '#ADD8E6';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Rita mark
            ctx.fillStyle = 'green';
            ctx.fillRect(-camera.x, groundY, levelWidth, groundHeight);

            // Rita hinder
            ctx.fillStyle = 'brown';
            for (const obstacle of obstacles) {
                ctx.fillRect(obstacle.x - camera.x, obstacle.y, obstacle.width, obstacle.height);
            }

            // Rita mynt
            ctx.fillStyle = 'gold';
            for (const coin of coins) {
                ctx.fillRect(coin.x - camera.x, coin.y, coin.width, coin.height);
            }

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

            // Kontrollera kollisioner med hinder
            for (const obstacle of obstacles) {
                if (
                    mario.x < obstacle.x + obstacle.width &&
                    mario.x + mario.width > obstacle.x &&
                    mario.y < obstacle.y + obstacle.height &&
                    mario.y + mario.height > obstacle.y
                ) {
                    alert('Oh no! Du träffade ett hinder. Försök igen!');
                    mario.x = 50; // Starta om
                    mario.y = 300;
                    camera.x = 0;
                    score = 0; // Återställ poäng
                    return;
                }
            }

            // Samla mynt
            for (let i = coins.length - 1; i >= 0; i--) {
                const coin = coins[i];
                if (
                    mario.x < coin.x + coin.width &&
                    mario.x + mario.width > coin.x &&
                    mario.y < coin.y + coin.height &&
                    mario.y + mario.height > coin.y
                ) {
                    coins.splice(i, 1); // Ta bort myntet från listan
                    score += 10; // Öka poäng
                }
            }

            // Uppdatera kamerans position så att den följer Mario
            camera.x = Math.max(0, Math.min(mario.x - canvas.width / 2, levelWidth - canvas.width));

            // Rita Mario i relation till kameran
            ctx.fillStyle = mario.color;
            ctx.fillRect(mario.x - camera.x, mario.y, mario.width, mario.height);

            // Rita mållinjen
            ctx.fillStyle = 'blue';
            ctx.fillRect(levelWidth - 50 - camera.x, groundY - 50, 50, 50);

            // Uppdatera poäng baserat på tid
            const timeElapsed = Math.floor((Date.now() - startTime) / 1000);
            const timeScore = timeElapsed * 5; // Poäng baserat på tid
            const totalScore = score + timeScore;

            // Rita poäng
            ctx.fillStyle = 'black';
            ctx.font = '20px Arial';
            ctx.fillText(`Poäng: ${totalScore}`, 10, 30);

            // Kontrollera om Mario når mållinjen
            if (mario.x + mario.width >= levelWidth - 50) {
                alert(`Grattis! Du klarade banan med ${totalScore} poäng!`);
                mario.x = 50; // Starta om
                mario.y = 300;
                camera.x = 0;
                score = 0; // Återställ poäng
                startTime = Date.now();
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
st.set_page_config(page_title="Mario med poängsystem", layout="centered")

st.title("Mario med poängsystem")
st.write("Använd piltangenterna för att röra dig och mellanslag för att hoppa! Samla mynt och undvik hinder för att få högsta poäng!")

# Visa spelet med hjälp av Streamlit Components
st.components.v1.html(game_code, height=500)
