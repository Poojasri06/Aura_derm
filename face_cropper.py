import cv2
import numpy as np
from PIL import Image
import cvlib as cv

def crop_face_from_pil(pil_img):
    """
    Detect and crop the first face from a PIL image using cvlib.
    Returns cropped face or original image if no face found.
    """
    img_np = np.array(pil_img)
    faces, _ = cv.detect_face(img_np)

    if not faces:
        return pil_img  # No face detected

    # Take first face only
    (startX, startY, endX, endY) = faces[0]
    face_crop = img_np[startY:endY, startX:endX]

    return Image.fromarray(face_crop)
