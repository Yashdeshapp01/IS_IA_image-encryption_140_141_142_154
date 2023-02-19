# IS_IA_image-encryption_140_141_142_154
We basically try to implement a basic image encryption tool by random key, image shuffling and password and also try to decrypt it

As images can also sometimes contain confidential information, we developed a basic image encryption tool
The basic functionalities decided were:

•	User will upload an image file from his file explorer
•	Our tool will simply generate a file containing the encrypted image and store I the same directory as the original file.
•	Then if the user wants to get back the original image file he can choose the option of "decrypt file" and the tool will generate a file identical to the original file uploaded by the user.

To achieve high level of encryption we decided to implement the encryption in the following way:

I.	The image is read.
II.	After obtaining the height and width of the image we divide it into 4 parts.
III.	The parts of the image are shuffled and put in a list.
IV.	That list is encrypted using a password.
V.	A random key is generated.
VI.	And using that key the shuffled image is further encrypted.
VII.	Now when we decrypt the image, first the key is matched.
VIII.	So, we get the shuffled image.
IX.	By putting the generated password, the shuffled image list is put in correct order as it was in the original image. 
X.	That list is Converted back to image in file format and hence we obtain the original file.

For interactive user interface we used flask

Our basic Tech Stack for developing this tool was:
	Python: It included various libraries like OpenCV, cryptography, pickle, NumPy, and random
	Flask: A web application framework for front-end. Developing front end also included the usage of HTML and CSS too. 

With this tech Stack we were able to perform encryption of images with high accuracy and perfection The decryption part the image was distorted a bit So decryption using our tool requires further research and has a scop for improvement.

