from flask import Flask, render_template, request, redirect, send_file
import numpy as np
import cv2
import random
import os
import pickle
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def upload_file():
    # Get uploaded file
    uploaded_file = request.files['file']
    
    # Read image
    img_array = np.frombuffer(uploaded_file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)
    
    # Encrypt image
    encrypted_img = encrypt(img)
    
    # Create file-like object to store image
    file_object = io.BytesIO()
    
    # Save encrypted image to file-like object
    cv2.imencode('.png', encrypted_img)[1].tofile(file_object)
    file_object.seek(0)
    
    # Send encrypted image to user for download
    return send_file(file_object, mimetype='image/png', as_attachment=True, attachment_filename='encrypted_image.png')

def encrypt(img):
    height, width = img.shape[:2]
    part1 = img[0:height//2,0:width//2]
    part2 = img[0:height//2,width//2:width]
    part3 = img[height//2:height,0:width//2]
    part4 = img[height//2:height,width//2:width]
    parts = [part1,part2,part3,part4]
    key_og_positin = [part1,part2,part3,part4]
    data = pickle.dumps(key_og_positin)
    password = "password".encode()
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    key_pos = base64.urlsafe_b64encode(kdf.derive(password))
    cipher = Fernet(key_pos)
    encrypted_data = cipher.encrypt(data)
    pickled_data = Fernet.decrypt(encrypted_data)
    numerical_array = pickle.loads(pickled_data)
    random.shuffle(parts)
    key="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    symbols="ABCDEFGH"
    mapping=dict(zip(symbols,parts))
    original_position = "".join([symbols[i] for i in range(len(parts))])
    encrypted_position = "".join([key[key.index(c)] for c in original_position])
    shuffled_image = np.hstack((np.vstack((mapping[encrypted_position[0]],mapping[encrypted_position[1]])),np.vstack((mapping[encrypted_position[2]],mapping[encrypted_position[3]]))))
    key = np.random.randint(256, size=(height,width,3), dtype=np.uint8)
    encrypted_img = cv2.bitwise_xor(shuffled_image,key)
    return encrypted_img, numerical_array

@app.route('/decrypt', methods=['POST'])

def decrypt_file():
    # Get uploaded file
    uploaded_file = request.files['file']
    # Read encrypted image
    img_list = np.frombuffer(uploaded_file.read(), np.uint8)
    #encrypted_img = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    encrypted_img = cv2.imdecode(img_list, cv2.IMREAD_UNCHANGED)
    # Get encrypted data
    encrypted_data = request.form['encrypted_data']
    # Decrypt image
    decrypted_img, height, width = decrypt(encrypted_img, encrypted_data)
    # Save decrypted image
    cv2.imwrite('decrypted_image.png', decrypted_img)
    # Send decrypted image to user for download
    return send_file('decrypted_image.png', mimetype='image/png', as_attachment=True, attachment_filename='decrypted_image.png')

def decrypt(encrypted_img, encrypted_data):
    # Decrypt data
    password = "password".encode()
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    key_pos = base64.urlsafe_b64encode(kdf.derive(password))
    cipher = Fernet(key_pos)
    decrypted_data = pickle.loads(cipher.decrypt(encrypted_data))
    # Get original positions of image parts
    key_og_positin = decrypted_data
    part1, part2, part3, part4 = key_og_positin
    # Rebuild image based on encrypted positions
    key="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    symbols="ABCDEFGH"
    mapping=dict(zip(key, [part1,part2,part3,part4]))
    height, width = encrypted_img.shape[:2]
    original_position = "".join([key[symbols.index(c)] for c in encrypted_img[height//2:, width//2]])
    shuffled_image = np.vstack((np.hstack((mapping[original_position[0]],mapping[original_position[1]])),np.hstack((mapping[original_position[2]],mapping[original_position[3]]))))
    # Get key used for encryption
    key = np.random.randint(256, size=(height,width,3), dtype=np.uint8)
    # Decrypt image
    decrypted_img = cv2.bitwise_xor(shuffled_image,key)
    return decrypted_img, height, width

if __name__ == '__main__':
    app.run()
