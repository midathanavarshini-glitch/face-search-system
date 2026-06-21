from insightface.app import FaceAnalysis
import cv2
import os
import numpy as np

app = FaceAnalysis()
app.prepare(ctx_id=0, det_size=(640, 640))

def process_faces(video_name):

    frames_folder = os.path.join(
        "frames",
        video_name
    )

    embeddings_folder = os.path.join(
        "embeddings",
        video_name
    )

    os.makedirs(
        embeddings_folder,
        exist_ok=True
    )

    total_faces = 0

    for file in os.listdir(frames_folder):

        if not file.endswith(".jpg"):
            continue

        image_path = os.path.join(
            frames_folder,
            file
        )

        img = cv2.imread(image_path)

        faces = app.get(img)

        for i, face in enumerate(faces):

            save_name = (
                file.replace(
                    ".jpg",
                    f"_face_{i}.npy"
                )
            )

            save_path = os.path.join(
                embeddings_folder,
                save_name
            )

            np.save(
                save_path,
                face.embedding
            )

            total_faces += 1

    return total_faces