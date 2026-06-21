from insightface.app import FaceAnalysis
import cv2
import numpy as np
import os

app = FaceAnalysis()
app.prepare(ctx_id=0, det_size=(640, 640))


def find_matches(query_image_path, selected_videos):

    query_img = cv2.imread(query_image_path)

    if query_img is None:
        return []

    faces = app.get(query_img)

    if len(faces) == 0:
        return []

    query_embedding = faces[0].embedding

    strong_matches = []
    possible_matches = []

    for video_name in selected_videos:

        embedding_folder = os.path.join(
            "embeddings",
            video_name
        )

        if not os.path.exists(
            embedding_folder
        ):
            continue

        for file in os.listdir(
            embedding_folder
        ):

            if not file.endswith(".npy"):
                continue

            stored_embedding = np.load(
                os.path.join(
                    embedding_folder,
                    file
                )
            )

            score = np.dot(
                query_embedding,
                stored_embedding
            ) / (
                np.linalg.norm(query_embedding)
                * np.linalg.norm(stored_embedding)
            )

            
            frame_number = int(
                file.split("_")[1]
            )

            
            FRAME_SKIP = 30

            with open(
                os.path.join(
                    "frames",
                    video_name,
                    "fps.txt"
                ),
                "r"
            ) as f:

                FPS = float(f.read())
            timestamp_seconds = (
                frame_number * FRAME_SKIP
            ) / FPS

            hours = int(
                timestamp_seconds // 3600
            )

            minutes = int(
                (timestamp_seconds % 3600) // 60
            )

            seconds = int(
                timestamp_seconds % 60
            )

            timestamp = (
                f"{hours:02d}:"
                f"{minutes:02d}:"
                f"{seconds:02d}"
            )
            #print(file, "->", round(float(score), 4))
            if score >= 0.50:

                strong_matches.append(
                    (
                        video_name,
                        file,
                        frame_number,
                        timestamp,
                        float(score)
                    )
                )

            elif score >= 0.35 and score < 0.5 :

                possible_matches.append(
                    (
                        video_name,
                        file,
                        frame_number,
                        timestamp,
                        float(score)
                    )
                )

    strong_matches.sort(
        key=lambda x: x[4],
        reverse=True
    )

    possible_matches.sort(
        key=lambda x: x[4],
        reverse=True
    )

    return strong_matches, possible_matches