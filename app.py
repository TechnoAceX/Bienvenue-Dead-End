from flask import Flask, redirect, render_template, request, session
from ai_res import generate_complete_story, generate_image
import os

app = Flask(__name__)

# Secret Key Handling
try:
    from keys import secret_key
    app.config['SECRET_KEY'] = secret_key
except ImportError:
    app.config['SECRET_KEY'] = os.environ.get("secret_key", "fallback_secret")


@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        # Clear any previous session data related to story
        session.clear()

        # Save new form inputs
        session["name"] = request.form.get("name", "").strip()
        session["blueprint"] = request.form.get("blueprint", "").strip()
        session["duration"] = request.form.get("duration", "2")  # default medium duration
        session["protocol"] = request.form.get("protocol", "poem")  # default protocol

        # Validation
        if not session["name"] or not session["blueprint"]:
            return render_template("form.html", error="Please fill all required fields.")

        return redirect("/response")

    return render_template("form.html")


@app.route("/response", methods=["GET"])
def response():
    # Check required session keys
    if not session.get("name") or not session.get("blueprint"):
        return redirect("/")

    # Generate story and image using ai_res functions
    story_text = generate_complete_story(
        name=session["name"],
        blueprint=session["blueprint"],
        duration=session.get("duration"),
        protocol=session.get("protocol")
    )
    image_url = generate_image(session["blueprint"])

    # Save generated results in session
    session["story_text"] = story_text
    session["image_url"] = image_url

    # Render response page with story and image
    return render_template("index.html", story=story_text, image_url=image_url)


if __name__ == "__main__":
    app.run(debug=True)
