from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import random

app = Flask(__name__)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    max_http_buffer_size=10_000_000
)

statuses = []
chats = {}

colors = [
    "#e542a3",
    "#00a8ff",
    "#9b59b6",
    "#2ecc71",
    "#f39c12",
    "#e74c3c",
    "#1abc9c",
    "#3498db"
]


def left(ts):
    diff = 24 * 3600 - (time.time() - ts)

    if diff <= 0:
        return None

    h = int(diff // 3600)
    m = int((diff % 3600) // 60)

    return f"{h}h {m}m" if h > 0 else f"{m}m"


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("load_chat")
def load_chat(data):
    chat = data["chat"]
    emit("chat_history", chats.get(chat, []))


@socketio.on("get_status")
def get_status():
    global statuses

    statuses = [
        s for s in statuses
        if left(s["time"]) is not None
    ]

    emit(
        "all_status",
        [
            {
                "user": s["user"],
                "img": s["img"],
                "left": left(s["time"]),
                "color": s["color"]
            }
            for s in statuses
        ]
    )


@socketio.on("add_status")
def add_status(data):
    global statuses

    # Remove previous status from the same user
    statuses = [
        s for s in statuses
        if s["user"] != data["user"]
    ]

    statuses.append({
        "user": data["user"],
        "img": data["img"],
        "time": time.time(),
        "color": random.choice(colors)
    })

    # Remove expired statuses
    statuses = [
        s for s in statuses
        if left(s["time"]) is not None
    ]

    emit(
        "new_status",
        [
            {
                "user": s["user"],
                "img": s["img"],
                "left": left(s["time"]),
                "color": s["color"]
            }
            for s in statuses
        ],
        broadcast=True
    )


@socketio.on("message")
def message(data):
    chat = data["chat"]

    chats.setdefault(chat, []).append(data)

    # Keep only the last 100 messages
    chats[chat] = chats[chat][-100:]

    emit("message", data, broadcast=True)


@socketio.on("offer")
def offer(data):
    emit(
        "offer",
        data,
        broadcast=True,
        include_self=False
    )


@socketio.on("answer")
def answer(data):
    emit(
        "answer",
        data,
        broadcast=True,
        include_self=False
    )


@socketio.on("ice")
def ice(data):
    emit(
        "ice",
        data,
        broadcast=True,
        include_self=False
    )


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
