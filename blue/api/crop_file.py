import dlib
from PIL import Image
from scipy import io
import imageio


def detect_faces(image):

    # Create a face detector
    face_detector = dlib.get_frontal_face_detector()

    # Run detector and get bounding boxes of the faces on image.
    detected_faces = face_detector(image, 1)
    face_frames = [(x.left(), x.top(),
                    x.right(), x.bottom()) for x in detected_faces]

    return face_frames


def crop_save(image,id_image,path):
    # # Load image
    # img_path = 'data_test/friends1.jpg'
    # image = imageio.imread(img_path)

    # Detect faces
    detected_face = detect_faces(image)

    if len(detected_face)==1:
        for n, face_rect in enumerate(detected_face):
            face = Image.fromarray(image).crop(face_rect)

        #resize
        img = face.resize((280,280), Image.ANTIALIAS)
        img.save(path+id_image+".jpg")

    else:
        print('faces more than 1')
