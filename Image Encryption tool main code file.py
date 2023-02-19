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



img = cv2.imread("protect.png")
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
random.shuffle(parts)
key="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

symbols="ABCDEFGH"
mapping=dict(zip(symbols,parts))

original_position = "".join([symbols[i] for i in range(len(parts))])
encrypted_position = "".join([key[key.index(c)] for c in original_position])

shuffled_image = np.hstack((np.vstack((mapping[encrypted_position[0]],mapping[encrypted_position[1]])),np.vstack((mapping[encrypted_position[2]],mapping[encrypted_position[3]]))))

cv2.imshow(shuffled_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
key = np.random.randint(256, size=(height,width,3), dtype=np.uint8)

encrypted_img = cv2.bitwise_xor(shuffled_image,key)

cv2.imwrite("encryptedImage.png", encrypted_img)
decrypted_img = cv2.bitwise_xor(encrypted_img,key)
cv2.imwrite("decrypted_img.png",decrypted_img)
decrypted_data = cipher.decrypt(encrypted_data)
decrypted_list = pickle.loads(decrypted_data)
hor1 = np.hstack((decrypted_list[0],decrypted_list[1]))
hor2 = np.hstack((decrypted_list[2],decrypted_list[3]))
final_image = np.vstack((hor1,hor2))
cv2.imwrite("fimage.png",final_image)



