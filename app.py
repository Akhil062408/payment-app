import os
from flask import Flask, jsonify

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "dev")
GIT_COMMIT = os.getenv("GIT_COMMIT", "unknown")
BUILD_NUMBER = os.getenv("BUILD_NUMBER", "unknown")
BRANCH_NAME = os.getenv("BRANCH_NAME", "unknown")
DOCKER_IMAGE = os.getenv("DOCKER_IMAGE", "unknown")


@app.route("/")
def home():
    return jsonify({
        "application": "payment",
        "version": VERSION,
        "git_commit": GIT_COMMIT,
        "build_number": BUILD_NUMBER,
        "branch": BRANCH_NAME,
        "docker_image": DOCKER_IMAGE
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
