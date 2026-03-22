from flask import Flask, render_template, request, jsonify
import pickle
import pdfplumber
from docx import Document
import os

app = Flask(__name__)

# ✅ Load trained model with error handling
try:
    model = pickle.load(open("model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
    print("✅ Model loaded successfully")
except FileNotFoundError as e:
    print(f"❌ Error: {e}")
    model = None
    vectorizer = None


# ✅ Home route
@app.route("/")
def home():
    return render_template("first.html")


# ✅ Extract text function
def extract_text(file):
    filename = file.filename.lower()

    # PDF
    if filename.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        return text

    # DOCX
    elif filename.endswith(".docx"):
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs if para.text])

    # TXT / other
    else:
        return file.read().decode("utf-8")


# ✅ Check route
@app.route("/check", methods=["POST"])
def check():
    try:
        # Check if model is loaded
        if model is None or vectorizer is None:
            return jsonify({"error": "Model not found. Make sure model.pkl and vectorizer.pkl exist"}), 500

        # Check if file provided
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]

        # Check if file selected
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        # Extract text
        text = extract_text(file)

        # ⚠️ Empty file check
        if not text or len(text.strip()) == 0:
            return jsonify({"error": "No text found in file"}), 400

        # Predict
        vec = vectorizer.transform([text])
        prediction = model.predict(vec)

        if prediction[0] == 1:
            result = "AI Generated Content"
        else:
            result = "Human Written Content"

        return jsonify({"result": result, "status": "success"}), 200
    
    except Exception as e:
        print(f"Error in check: {e}")
        return jsonify({"error": f"Error: {str(e)}"}), 500


# ✅ Run app
if __name__ == "__main__":
    app.run(debug=True)