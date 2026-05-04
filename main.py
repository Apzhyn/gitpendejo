from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)
path = "repo"

def run(cmd):
    return subprocess.check_output(cmd, cwd=path).decode()

if not os.path.exists(path):
    os.makedirs(path)
    subprocess.run(["git", "init"], cwd=path)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    user = data["user"]
    text = data["text"]

    f = os.path.join(path, "chat.txt")
    with open(f, "a") as x:
        x.write(f"{user}: {text}\n")

    subprocess.run(["git", "add", "."], cwd=path)
    subprocess.run(["git", "commit", "-m", f"{user}:{text}"], cwd=path)

    return jsonify(ok=True)

@app.route("/msgs")
def msgs():
    log = run(["git", "log", "--pretty=format:%s"])
    out = []
    for i in log.split("\n"):
        if ":" in i:
            u, t = i.split(":", 1)
            out.append({"user": u, "text": t})
    return jsonify(out[::-1])

if __name__ == "__main__":
    app.run(debug=True)
