import os
code='''from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time, random, os
app=Flask(__name__)
socketio=SocketIO(app,cors_allowed_origins="*",max_http_buffer_size=10_000_000)
statuses=[];chats={};colors=["#e542a3","#00a884","#1f7aec","#ffbc38","#a884ff"]
def left(ts):
 diff=24*3600-(time.time()-ts)
 if diff<=0:return None
 h=int(diff//3600);m=int((diff%3600)//60)
 return f"{h}h {m}m" if h>0 else f"{m}m"
@app.route("/")
def i():return render_template("index.html")
@socketio.on("load_chat")
def lc(d):emit("chat_history",chats.get(d["chat"],[]))
@socketio.on("get_status")
def gs():
 global statuses;statuses=[s for s in statuses if left(s['time'])];emit("all_status",[{"user":s["user"],"img":s["img"],"left":left(s["time"]),"color":s["color"]} for s in statuses])
@socketio.on("add_status")
def ad(d):
 global statuses;statuses=[s for s in statuses if s["user"]!=d["user"]];statuses.append({"user":d["user"],"img":d["img"],"time":time.time(),"color":random.choice(colors)});statuses=[s for s in statuses if left(s['time'])];emit("new_status",[{"user":s["user"],"img":s["img"],"left":left(s["time"]),"color":s["color"]} for s in statuses],broadcast=True)
@socketio.on("message")
def m(d):
 c=d["chat"];chats.setdefault(c,[]).append(d);chats[c]=chats[c][-100:];emit("message",d,broadcast=True)
@socketio.on("offer")
def o(o):emit("offer",o,broadcast=True,include_self=False)
@socketio.on("answer")
def a(a):emit("answer",a,broadcast=True,include_self=False)
@socketio.on("ice")
def ic(c):emit("ice",c,broadcast=True,include_self=False)
if __name__=="__main__":port=int(os.environ.get("PORT",5000));socketio.run(app,host="0.0.0.0",port=port)
'''
open("app.py","w").write(code)
# delete extra files
for f in ["requirement.txt","main.py","whatsapp v12.py"]:
  if os.path.exists(f): os.remove(f)
print("✅ FIXED! Now app.py should be ~1.5KB and only 2 files left")
