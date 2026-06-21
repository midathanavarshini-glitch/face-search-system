import os
import base64
from datetime import datetime

def generate_report(matches):

    os.makedirs(
        "results",
        exist_ok=True
    )

    current_time = datetime.now()

    report_name = (
        f"Face_Report_"
        f"{current_time.strftime('%Y-%m-%d_%H-%M-%S')}"
        f".html"
    )

    html = """
    <html>
    <head>
        <title>Face Search Report</title>
    </head>
    <body>

    <h1>Face Search Report</h1>
    <hr>
    """

    for video, frame, frame_number, timestamp, score in matches:

        frame_image = (
            frame.split("_face_")[0]
            + ".jpg"
        )

        image_path = os.path.join(
            "frames",
            video,
            frame_image
        )

        if os.path.exists(image_path):

            with open(
                image_path,
                "rb"
            ) as img_file:

                encoded = base64.b64encode(
                    img_file.read()
                ).decode()

            image_html = f"""
            <img
                src="data:image/jpeg;base64,{encoded}"
                width="400"
            >
            """

        else:

            image_html = "<p>Image not found</p>"

        html += f"""
        <div style="
            margin-bottom:40px;
        ">

            {image_html}

            <p>
            Video: {video}
            <br>
            Match File: {frame}
            <br>
            Frame Number: {frame_number}
            <br>
            Timestamp: {timestamp}
            <br>
            Score: {score:.4f}
            </p>

        </div>

        <hr>
        """

    html += """
    </body>
    </html>
    """

    report_path = os.path.join(
        "results",
        report_name
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)

    return report_name