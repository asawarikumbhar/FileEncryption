
from flask import Flask, request, render_template, send_file
from cryptography.fernet import Fernet

app = Flask(__name__)

# Generate a secret key for encryption/decryption

key = Fernet.generate_key()

cipher_suite = Fernet(key)

import os


@app.route("/", methods=["GET", "POST"])
def file_operation():
    if request.method == "POST":
        operation = request.form["operation"]

        # Check if a file is uploaded
        if "file" not in request.files:
            return "No file uploaded."

        file = request.files["file"]

        # Check if the file has a name
        if file.filename == "":
            return "No file selected."

        # Read the uploaded file
        file_content = file.read()

        if operation == "encrypt":
            # Encrypt the file
            encrypted_content = cipher_suite.encrypt(file_content)

            # Save the encrypted content to a new file
            with open("encrypted_file", "wb") as encrypted_file:
                encrypted_file.write(encrypted_content)
            
            return render_template('result.html',data = "File encrypted successfully.",filename ="encrypted_file") 
        

        elif operation == "decrypt":
            try:
                # Decrypt the file
                decrypted_content = cipher_suite.decrypt(file_content)

                # Save the decrypted content to a new file
                with open("decrypted_file", "wb") as decrypted_file:
                    decrypted_file.write(decrypted_content)

                return render_template('result.html',data = "File decrypted successfully.",filename ="decrypted_file")
            except Exception as e:
                return f"Decryption error: {e}"
    return render_template("index.html")

@app.route("/download/<filename>")
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
