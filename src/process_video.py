import cv2
import os
def process_video(video_path):

    print("PROCESSING VIDEO:", video_path)

def process_video(video_path):

    video_name = os.path.splitext(
        os.path.basename(video_path)
    )[0]

    output_folder = os.path.join(
        "frames",
        video_name
    )

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    with open(
        os.path.join(output_folder, "fps.txt"),
        "w"
    ) as f:

        f.write(str(fps))
    frame_count = 0
    saved_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % 30 == 0:

            save_path = os.path.join(
                output_folder,
                f"frame_{saved_count}.jpg"
            )

            cv2.imwrite(
                save_path,
                frame
            )

            saved_count += 1

        frame_count += 1
    print("Frames Saved:", saved_count)
    cap.release()

    return saved_count