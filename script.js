const WS_URL =
  "wss://s15592.fra1.piesocket.com/v3/1" +
  "?api_key=CHAKAsMULcSYP514xXMuX50m1ZF8MgjSpMpIvTfo" +
  "&notify_self=1";

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let ws;
let myId = Math.random().toString(36).slice(2);
let nick = "";
let players = {};
let lastTime = performance.now();
let fps = 0;

function joinGame() {
  nick = document.getElementById("nick").value;
  const room = document.getElementById("room").value;

  if (!nick || !room) {
    alert("Nick ve oda şifresi gir!");
    return;
  }

  ws = new WebSocket(WS_URL + "&room=" + encodeURIComponent(room));

  ws.onopen = () => {
    ws.send(JSON.stringify({
      type: "join",
      id: myId,
      nick: nick
    }));

    document.getElementById("login").style.display = "none";
    canvas.style.display = "block";
    document.getElementById("chat").style.display = "flex";

    players[myId] = {
      x: Math.random() * 700 + 50,
      y: Math.random() * 300 + 50,
      nick: nick
    };

    requestAnimationFrame(loop);
  };

  ws.onmessage = (e) => {
    const data = JSON.parse(e.data);

    if (data.type === "join") {
      players[data.id] = {
        x: 100,
        y: 100,
        nick: data.nick
      };
      addMsg(`🟢 ${data.nick} odaya katıldı`);
    }

    if (data.type === "leave") {
      if (players[data.id]) {
        addMsg(`🔴 ${players[data.id].nick} çıktı`);
        delete players[data.id];
      }
    }

    if (data.type === "move") {
      if (players[data.id]) {
        players[data.id].x = data.x;
        players[data.id].y = data.y;
      }
    }

    if (data.type === "chat") {
      addMsg(`${data.nick}: ${data.msg}`);
    }
  };

  window.addEventListener("beforeunload", () => {
    ws.send(JSON.stringify({ type: "leave", id: myId }));
  });
}

// CHAT
function sendChat(e) {
  if (e.key === "Enter") {
    const input = e.target;
    ws.send(JSON.stringify({
      type: "chat",
      nick: nick,
      msg: input.value
    }));
    input.value = "";
  }
}

function addMsg(msg) {
  const div = document.createElement("div");
  div.textContent = msg;
  document.getElementById("messages").appendChild(div);
}

// HAREKET
window.addEventListener("keydown", (e) => {
  const p = players[myId];
  if (!p) return;

  const speed = 5;
  if (e.key === "w") p.y -= speed;
  if (e.key === "s") p.y += speed;
  if (e.key === "a") p.x -= speed;
  if (e.key === "d") p.x += speed;

  ws.send(JSON.stringify({
    type: "move",
    id: myId,
    x: p.x,
    y: p.y
  }));
});

// OYUN DÖNGÜSÜ
function loop(time) {
  fps = Math.round(1000 / (time - lastTime));
  lastTime = time;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (const id in players) {
    const p = players[id];

    ctx.fillStyle = id === myId ? "#ff4444" : "#4444ff";
    ctx.fillRect(p.x, p.y, 40, 20);

    ctx.fillStyle = "#000";
    ctx.fillText(p.nick, p.x, p.y - 5);
  }

  ctx.fillStyle = "#000";
  ctx.fillText("FPS: " + fps, 10, 20);

  requestAnimationFrame(loop);
}
