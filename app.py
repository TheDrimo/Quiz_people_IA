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


@app.route("/api", methods=["GET"])
def handle_request():
    conn = sqlite3.connect("bd_ia_generated_images.db")
    cursor = conn.cursor()
    choice = fetch_random_entry(cursor)
    image_string1 = choice[0][1]
    image_string2 = choice[1][1]
    country1 = choice[0][3]
    country2 = choice[1][3]
    conn.close()
    
    return jsonify({
        "image1": image_string1,
        "image2": image_string2, 
        "country1": country1,
        "country2": country2
    })

@app.route("/api/response", methods=["POST"])
def handle_response():
    data = request.get_json()
    selectedAnswer = data.get("selectedAnswer")
    correctAnswer = data.get("correctAnswer")
    wrongAnswer = data.get("wrongAnswer")

    # Do something with the received data...
    
    return jsonify({"message": "Data received successfully"})



if __name__ == "__main__":
    app.run(debug=True)
