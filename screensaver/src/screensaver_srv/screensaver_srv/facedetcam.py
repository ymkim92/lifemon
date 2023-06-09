"""detect number of faces from webcam
"""
import time

import cv2

FACE_CASCADE_FILE = 'haarcascade_frontalface_default.xml'

class FaceDetection:
    """class for face detection from webcam"""
    def __init__(self, threshold_no_face):
        # Load the cascade
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + FACE_CASCADE_FILE
            # FACE_CASCADE_FILE
        )

        self.num_faces = 0
        self.cnt_no_face = 0
        self.threshold_no_face = threshold_no_face

    def get_number_of_faces(self, show_image=False):
        """ To capture video from webcam. 
        """
        self.cap = cv2.VideoCapture(0)

        # Read the frame
        # This takes about 400ms
        _, img = self.cap.read()

        # Release the VideoCapture object
        self.cap.release()

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = self.face_cascade.detectMultiScale(gray, 1.2, 4)

        if show_image:
            # Draw the rectangle around each face
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Display
            cv2.imshow('img', img)

        self.num_faces = len(faces)
        return self.num_faces

    def get_face_detected(self, show_image):
        """ get the number of face detected"""
        num_faces = self.get_number_of_faces(show_image)
        print(f"num faces: {num_faces}")
        if num_faces > 0:
            self.cnt_no_face = 0
        else:
            if self.cnt_no_face < self.threshold_no_face:
                self.cnt_no_face += 1

        print(f"count for no face detected: {self.cnt_no_face}")
        return not (num_faces == 0 and self.cnt_no_face >= self.threshold_no_face)

def main():
    """ main """
    facedet = FaceDetection(5)
    prev_has_face = False
    while True:
        has_face = facedet.get_face_detected(show_image=True)
        if prev_has_face != has_face:
            print(f"has face: {has_face}")
            prev_has_face = has_face

        # time.sleep(1)
        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k==27:
            break

if __name__ == "__main__":
    main()