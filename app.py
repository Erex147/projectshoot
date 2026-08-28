import math
import random
import threading

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

players = {}
bullets = []
lock = threading.Lock()
world_width = 8000
world_height = 5000


def random_spawn():
    x = random.randint(40, world_width - 40)
    y = random.randint(40, world_height - 40)
    return x, y


def game_loop():
    while True:
        with lock:
            for bullet in bullets[:]:
                bullet["x"] += bullet["vx"]
                bullet["y"] += bullet["vy"]

                if bullet["x"] < 0 or bullet["x"] > world_width or bullet["y"] < 0 or bullet["y"] > world_height:
                    bullets.remove(bullet)
                    continue

                for player_id, player in players.items():
                    if player_id != bullet["owner"] and math.hypot(
                        player["x"] - bullet["x"], player["y"] - bullet["y"]
                    ) < 20:
                        player["health"] = player["health"] - 20
                        bullets.remove(bullet)
                        if player["health"] <= 0:
                            new_x, new_y = random_spawn()
                            player["health"] = 100
                            player["x"] = new_x
                            player["y"] = new_y
                        break

            state = {"players": players, "bullets": bullets}

        socketio.emit("state", state)
        socketio.sleep(0.05)


@app.get("/")
def home():
    return render_template("index.html")


@socketio.on("join")
def join(username):
    name = str(username)[:16]
    if name == "":
        name = "Player"

    with lock:
        new_x, new_y = random_spawn()
        players[request.sid] = {
            "name": name,
            "x": new_x,
            "y": new_y,
            "health": 100,
        }
    emit("joined", {"id": request.sid})


@socketio.on("move")
def move(data):
    with lock:
        player = players.get(request.sid)
        if player:
            new_x = float(data.get("x", player["x"]))
            new_y = float(data.get("y", player["y"]))
            player["x"] = max(20, min(world_width - 20, new_x))
            player["y"] = max(20, min(world_height - 20, new_y))


@socketio.on("shoot")
def shoot(target):
    with lock:
        player = players.get(request.sid)
        if not player:
            return
        dx = float(target["x"]) - player["x"]
        dy = float(target["y"]) - player["y"]
        distance = math.hypot(dx, dy) or 1
        bullets.append({
            "owner": request.sid,
            "x": player["x"],
            "y": player["y"],
            "vx": dx / distance * 9,
            "vy": dy / distance * 9,
        })


@socketio.on("disconnect")
def disconnect():
    with lock:
        players.pop(request.sid, None)


if __name__ == "__main__":
    socketio.start_background_task(game_loop)
    socketio.run(app, host="0.0.0.0", port=8000, debug=True, use_reloader=False)