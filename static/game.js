const canvas = document.querySelector("#game");
const ctx = canvas.getContext("2d");
const form = document.querySelector("#username-form");
const socket = io();

let myId = null;
let state = { players: {}, bullets: [] };
const keys = {};
const worldWidth = 8000;
const worldHeight = 5000;

form.addEventListener("submit", event => {
    event.preventDefault();
    socket.emit("join", document.querySelector("#username").value.trim());
    form.style.display = "none";
    canvas.style.display = "block";
});

socket.on("joined", data => { myId = data.id; });
socket.on("state", newState => { state = newState; });

addEventListener("keydown", event => {
    keys[event.key] = true;
    if (["w", "a", "s", "d"].includes(event.key.toLowerCase())) event.preventDefault();
});

addEventListener("keyup", event => {
    keys[event.key] = false;
});

canvas.addEventListener("click", event => {
    const rectangle = canvas.getBoundingClientRect();
    const camera = getCamera();
    socket.emit("shoot", {
        x: (event.clientX - rectangle.left) * canvas.width / rectangle.width + camera.x,
        y: (event.clientY - rectangle.top) * canvas.height / rectangle.height + camera.y
    });
});

function getCamera() {
    const player = state.players[myId];
    if (!player) return { x: 0, y: 0 };

    let x = player.x - canvas.width / 2;
    let y = player.y - canvas.height / 2;
    x = Math.max(0, Math.min(worldWidth - canvas.width, x));
    y = Math.max(0, Math.min(worldHeight - canvas.height, y));
    return { x: x, y: y };
}

function update() {
    const player = state.players[myId];
    if (!player) return;

    const speed = 5;
    let moveX = 0;
    let moveY = 0;
    if (keys["w"] || keys["W"]) moveY -= 1;
    if (keys["a"] || keys["A"]) moveX -= 1;
    if (keys["s"] || keys["S"]) moveY += 1;
    if (keys["d"] || keys["D"]) moveX += 1;

    const moveLength = Math.hypot(moveX, moveY);
    if (moveLength > 0) {
        player.x += moveX / moveLength * speed;
        player.y += moveY / moveLength * speed;
    }
    socket.emit("move", { x: player.x, y: player.y });
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const camera = getCamera();
    ctx.save();
    ctx.translate(-camera.x, -camera.y);

    ctx.fillStyle = "#182235";
    ctx.fillRect(0, 0, worldWidth, worldHeight);

    ctx.strokeStyle = "#263653";
    ctx.lineWidth = 1;
    for (let x = 0; x <= worldWidth; x += 100) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, worldHeight);
        ctx.stroke();
    }
    for (let y = 0; y <= worldHeight; y += 100) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(worldWidth, y);
        ctx.stroke();
    }

    Object.entries(state.players).forEach(([id, player]) => {
        ctx.fillStyle = id === myId ? "#42d392" : "#f59e0b";
        ctx.beginPath();
        ctx.arc(player.x, player.y, 18, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = "white";
        ctx.textAlign = "center";
        ctx.fillText(`${player.name} (${player.health})`, player.x, player.y - 26);
    });

    ctx.fillStyle = "#f87171";
    state.bullets.forEach(bullet => ctx.fillRect(bullet.x - 3, bullet.y - 3, 6, 6));

    ctx.restore();
}

function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

requestAnimationFrame(loop);