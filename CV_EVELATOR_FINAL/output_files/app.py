import os
from pathlib import Path
from google import genai
from google.genai import types
import config

if not config.API_KEY:
    raise ValueError("❌ Nav ievadīts API_KEY failā config.py!")

client = genai.Client(api_key=config.API_KEY)

Path(config.OUTPUTS).mkdir(exist_ok=True)

def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def evaluate_cv(cv_filename):
    jd_text = read_file(f"{config.INPUTS}/jd.txt")
    cv_text = read_file(f"{config.INPUTS}/{cv_filename}")
    prompt_template = read_file(config.PROMPT_FILE)

    prompt = prompt_template.replace("<<JD_PLACEHOLDER>>", jd_text)
    prompt = prompt.replace("<<CV_PLACEHOLDER>>", cv_text)

    print(f"🧠 Analizēju {cv_filename} ...")

    response = client.models.generate_content(
        model=config.MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=config.TEMPERATURE
        )
    )

    result_text = str(response.text).strip()

    # Saglabā rezultātus
    json_path = f"{config.OUTPUTS}/{cv_filename.replace('.txt', '.json')}"
    with open(json_path, "w", encoding="utf-8") as output:
        output.write(result_text.replace("```json", "").replace("```", "").strip())

    print(f"✅ Saglabāts: {json_path}")

# Izpilde
if __name__ == "__main__":
    for file in os.listdir(config.INPUTS):
        if file.startswith("cv") and file.endswith(".txt"):
            evaluate_cv(file)
