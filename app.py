from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from io import BytesIO
import os
import openai
import random
from quiz_people_server_algo import *

openai.api_key = "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"


app = Flask(__name__)
CORS(app) 


conn = sqlite3.connect("bd_ia_generated_images.db")
cursor = conn.cursor()
generate_bd(cursor)
conn.commit()
conn.close()


@app.route("/api", methods=["POST"])
def handle_request():
    global request_count
    conn = sqlite3.connect("bd_ia_generated_images.db")
    cursor = conn.cursor()
    choice = fetch_random_entry(cursor)
    image_string1 = choice[0][1]
    image_string2 = choice[1][1]
    country1 = choice[0][3]
    country2 = choice[1][3]
    selected = choice[random.choice([0,1])][3]
    message = f"Where is the {selected} ?"
    conn.close()
    try:
        data = request.get_json()
        if data["message"] == "are you ok ?":
            return jsonify({"message": message, "image_string1": image_string1, 
                "image_string2": image_string2, "country1":country1, "country2":country2})
        else:
            return jsonify({"message": "Invalid request"})
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "An error occurred on the server"}), 500


if __name__ == "__main__":
    app.run(debug=True)
