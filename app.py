from flask import Flask, request, jsonify
from composer import compose

app = Flask(__name__)


@app.route('/v1/healthz', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


@app.route('/v1/metadata', methods=['GET'])
def metadata():
    return jsonify({
        "name": "Vera Bot",
        "version": "1.0"
    })


@app.route('/v1/context', methods=['POST'])
def context():
    return jsonify({"status": "ok"})


@app.route('/v1/tick', methods=['POST'])
def tick():
    data = request.json

    result = compose(
        data.get("category"),
        data.get("merchant"),
        data.get("trigger"),
        data.get("customer")
    )

    return jsonify(result)


# -----------------------------
# REPLY (CRITICAL FIX)
# -----------------------------
@app.route('/v1/reply', methods=['POST'])
def reply():
    data = request.json
    msg = data.get("message", "").lower()

    # STOP handling
    if "stop" in msg:
        return jsonify({"action": "end"})

    # positive intent
    if "yes" in msg or "book" in msg:
        return jsonify({
            "action": "reply",
            "text": "Great! Your booking is confirmed."
        })

    # negative intent
    if "no" in msg:
        return jsonify({"action": "end"})

    # fallback
    return jsonify({
        "action": "reply",
        "text": "Could you please confirm your preference?"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)