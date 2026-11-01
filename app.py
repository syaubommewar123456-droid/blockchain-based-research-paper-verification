from datetime import datetime
from PyPDF2 import PdfReader

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import hashlib
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

uploaded_texts = []

existing_files = os.listdir(
    UPLOAD_FOLDER
)

for file_name in existing_files:

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file_name
    )

    try:

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

        uploaded_texts.append(text)

    except:
        pass

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def calculate_similarity(text1, text2):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [text1, text2]
    )

    similarity = cosine_similarity(
        vectors
    )[0][1]

    return round(similarity * 100, 2)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def home():

    files = os.listdir(
        app.config['UPLOAD_FOLDER']
    )

    return render_template(
        'index.html',
        files=files
    )

@app.route('/upload', methods=['POST'])

def upload():

    if 'paper' not in request.files:
        return "No file part in the request.", 400

    file = request.files['paper']

    if file.filename == '':
        return "No file selected.", 400

    filename = secure_filename(file.filename)

    if not allowed_file(filename):
        return "Only PDF files are allowed.", 400

    file_path = os.path.join(
        app.config['UPLOAD_FOLDER'],
        filename
    )

    file.save(file_path)

    # Read PDF text
    try:
        reader = PdfReader(file_path)
    except Exception as e:
        return f"Unable to read the PDF file: {e}", 400

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    plagiarism = 0

    # Compare with previous uploads
    for old_text in uploaded_texts:

        similarity = calculate_similarity(
            text,
            old_text
        )

        if similarity > plagiarism:
            plagiarism = similarity

    uploaded_texts.append(text)

    # Generate SHA256 hash
    with open(file_path, 'rb') as f:
        file_data = f.read()

        paper_hash = hashlib.sha256(
        file_data
    ).hexdigest()

    if plagiarism < 20:
        status = "Original Content"

    elif plagiarism < 50:
        status = "Moderate Similarity"

    else:
        status = "Possible Plagiarism"

    upload_time = datetime.now().strftime(
        "%d-%m-%Y %I:%M %p"
    )
    files = os.listdir(
        app.config['UPLOAD_FOLDER']
    )    
    return render_template(
        'result.html',
        filename=filename,
        paper_hash=paper_hash,
        files=files,
        plagiarism=plagiarism,
        status=status,
        upload_time=upload_time
    )

if __name__ == '__main__':
    app.run(debug=True)