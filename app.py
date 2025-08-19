from flask import Flask, request, send_from_directory, render_template_string
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
KEY = Fernet.generate_key()  # Save this securely in production
fernet = Fernet(KEY)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            data = file.read()
            encrypted_data = fernet.encrypt(data)
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            with open(filepath, 'wb') as f:
                f.write(encrypted_data)
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string('''
        <h1>Secure File Upload & Download</h1>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
        <h3>Files:</h3>
        {% for f in files %}
            {{ f }} - <a href="/download/{{ f }}">Download</a><br>
        {% endfor %}
    ''', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data  # for better UX, use send_file with BytesIO

if __name__ == '__main__':
    app.run(debug=True)
