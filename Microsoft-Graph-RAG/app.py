from flask import Flask, render_template, request, jsonify, Response
import os
import requests
from pdf_image_extractor import make_text_file
from graph_util import run_graphrag_index, run_graphrag_query
from werkzeug.utils import secure_filename
from flask_cors import CORS
import yaml

cwd = os.getcwd()

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

venv_path = config['config']['venv_path'].replace("${cwd}", cwd)


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

INPUT_FOLDER = 'input'  # Ensure this folder exists
UPLOAD_FOLDER = 'uploads'
app.config['INPUT_FOLDER'] = config['config']['INPUT_FOLDER']
app.config['UPLOAD_FOLDER'] = config['config']['UPLOAD_FOLDER']

if not os.path.exists(INPUT_FOLDER):
    os.makedirs(INPUT_FOLDER)
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/fact-fusion')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the file is part of the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # Check if the file has a valid filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Secure the filename to avoid directory traversal attacks
    filename = secure_filename(file.filename)

    # Check if the uploaded file is a text file
    if filename.endswith('.txt'):
        # Save the text file to the /input folder
        file_path = os.path.join(INPUT_FOLDER, filename)
        file.save(file_path)
        return jsonify({'message': 'File saved successfully.', 'file_path': file_path}), 200
    else:
        # Call the predefined API
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        api_response = requests.post('http://127.0.0.1:5005/convert', json={'filename': filename})
        return jsonify(api_response.json()), api_response.status_code


@app.route('/analyze', methods=['POST'])
def analyze_query():
    data = request.json
    query = data.get('query')
    search_type = data.get('search_type')

    # Call the analysis API
    api_response = run_graphrag_query(query, search_type).strip()

    # Convert the response to bytes
    response_bytes = api_response.encode('utf-8')  # Convert string to bytes

    # Return the response as a binary buffer
    return Response(response_bytes, mimetype='text/plain')


@app.route('/train', methods=['POST'])
def train_model():
    data = request.json
    train_type = data.get('train_type')

    if train_type == 'train_latest':
        try:
            # Initialize variables to find the latest file
            latest_file = None
            latest_mod_time = 0

            # Find the latest file in the folder
            for filename in os.listdir(INPUT_FOLDER):
                file_path = os.path.join(INPUT_FOLDER, filename)
                if os.path.isfile(file_path):
                    # Get the last modification time
                    mod_time = os.path.getmtime(file_path)

                    # Check if this file is the latest one
                    if mod_time > latest_mod_time:
                        latest_mod_time = mod_time
                        latest_file = filename

            # Delete all files except the latest one
            for filename in os.listdir(INPUT_FOLDER):
                file_path = os.path.join(INPUT_FOLDER, filename)
                if os.path.isfile(file_path) and filename != latest_file:
                    os.remove(file_path)

            result = run_graphrag_index()

            return jsonify({'status': 'success', 'message': f'Training completed successfully.{result}'}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    else:
        result = run_graphrag_index()
        return jsonify({'status': 'success', 'message': f'Training completed successfully.{result}'}), 200


@app.route('/convert', methods=['POST'])
def convert_pdf_to_text():
    data = request.json
    pdf_filename = data.get('filename')

    if not pdf_filename:
        return jsonify({'error': 'No filename provided'}), 400

    pdf_path = os.path.join('uploads', pdf_filename)
    if not os.path.exists(pdf_path):
        return jsonify({'error': 'File not found'}), 404

    output_file = make_text_file(INPUT_FOLDER, pdf_filename)
    os.remove(pdf_path)
    return jsonify({'message': 'Text file created successfully', 'output_file': output_file}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
