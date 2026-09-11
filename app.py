from openai import OpenAI
import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static"


@app.route("/", methods=["GET", "POST"])
def main():

    if request.method == "POST":

        language = request.form.get("language")
        file = request.files.get("file")

        if not file or file.filename == "":
            return jsonify({
                "error": "No audio file uploaded"
            }), 400

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)

        # Audio → English
        with open(filepath, "rb") as audio_file:

            transcript = client.audio.translations.create(
                model="whisper-1",
                file=audio_file
            )

        english_text = transcript.text

        # English → Selected language
        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions=f"""
Translate the following English text into {language}.

Return only the translated text.
Do not provide explanations.
""",
            input=english_text
        )

        translated_text = response.output_text

        return jsonify({
            "original_text": english_text,
            "translated_text": translated_text,
            "language": language
        })

    return render_template("index.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
        port=8080
    )
