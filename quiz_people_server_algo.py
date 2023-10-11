import requests
from io import BytesIO
import base64
from PIL import Image
import os
import openai
import random
import datetime
import sqlite3


openai.api_key = "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"

def generate_IA_image(description):
  try:
    image_b64_json = openai.Image.create(
      prompt=description,
      n=1,
      response_format="b64_json",
      size="256x256"
    )
    return image_b64_json
  except:
    return "None"

def convert_str_to_png(str_image):
  image_data = base64.b64decode(str_image)
  image_io = BytesIO(image_data)
  img = Image.open(image_io)
  return img

important_country_adjectives = [
    "American", "Chinese", "Russian", "Indian", "Japanese", "German", "British", "French",
    "Brazilian", "Canadian", "Australian", "South Korean", "Italian", "Spanish", "Mexican",
    "Indonesian", "Dutch", "Turkish", "Swiss", "Swedish", "Norwegian", "Danish", "Belgian",
    "Austrian", "Finnish", "Singaporean", "Hong Kong", "Israeli", "Irish", "New Zealand",
    "Polish", "South African", "Argentinian", "Chilean", "Thai", "Malaysian", "Greek", "Portuguese"
]

def random_country_sex(country_list):
    selected_country = random.choice(country_list)
    selected_sex = random.choice(["man", "woman"])
    if selected_sex == "man":
      description = "a young and handsome "
    else :
      description = "a young and beautiful "
    description += f"{selected_country} {selected_sex}"
    return [selected_country, selected_sex, description]


def insert_data_into_db(cursor_insertion, image_str, sex, country, description):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor_insertion.execute(
        "INSERT INTO generated_images (image_str, sex, country,description, date) VALUES (?, ?, ?, ?,?)",
        (image_str, sex, country,description, current_date)
    )

def fetch_random_entry(cursor_fetch):
  cursor_fetch.execute("SELECT * FROM generated_images ORDER BY RANDOM() LIMIT 1;")
  first_row = cursor_fetch.fetchone()
  country = first_row[3]

  cursor_fetch.execute("SELECT DISTINCT country FROM generated_images;")
  countries = cursor_fetch.fetchall()
  other_countries = [row[0] for row in countries]
  other_countries.remove(country)
  second_country = random.choice(other_countries)

  cursor_fetch.execute("SELECT * FROM generated_images WHERE country = ? ORDER BY RANDOM() LIMIT 1;", (second_country,))
  second_row = cursor_fetch.fetchone()

  return first_row, second_row


def generate_bd(cursor_generation):
  cursor_generation.execute('''
      CREATE TABLE IF NOT EXISTS generated_images (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          image_str TEXT,
          sex TEXT,
          country TEXT,
          description TEXT,
          date TEXT
      )
  ''')

  cursor_generation.execute(f"SELECT COUNT(*) FROM generated_images;")
  size = cursor_generation.fetchone()[0]

  if size < 20:
    for _ in range(20):
        country, sex, description = random_country_sex(important_country_adjectives)  # Replace with your country list
        print(description)
        image_b64 = generate_IA_image(description)
        if image_b64 == "None":
          pass
        image_str = image_b64.data[0]["b64_json"]
        insert_data_into_db(cursor_generation, image_str, sex, country, description)



if __name__ == "__main__":
  conn = sqlite3.connect("bd_ia_generated_images.db")
  cursor = conn.cursor()


  generate_bd(cursor)
  conn.commit()

  choice = fetch_random_entry(cursor)
  #print(choice[0][2:], choice[1][2:], choice[0][0])

  conn.close()