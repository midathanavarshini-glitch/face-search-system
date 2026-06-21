from flask import Flask, request, redirect, send_from_directory
import os
from src.process_video import process_video
from src.process_faces import process_faces
from src.find_all_matches import find_matches
from flask import send_from_directory
app = Flask(__name__)

selected_videos = []

VIDEOS_FOLDER = "videos"

os.makedirs(VIDEOS_FOLDER, exist_ok=True)

QUERY_FOLDER = "query_images"

os.makedirs(
    QUERY_FOLDER,
    exist_ok=True
)

@app.route("/")
def home():

    videos = os.listdir(VIDEOS_FOLDER)

    html = """
    <h1>FACE SEARCH SYSTEM VERSION 999</h1>

    <h2>Upload Video</h2>

    <form action="/upload_video"
          method="post"
          enctype="multipart/form-data">

        <input type="file" name="video">
        <input type="submit" value="Upload">

    </form>

    <hr>

    <form action="/upload_query"
          method="post"
          enctype="multipart/form-data">

    <h2>Select Videos To Search</h2>

    <ul>
    """

    for video in videos:

        video_name = os.path.splitext(video)[0]

        html += f"""
        <li>
            <input
                type="checkbox"
                name="selected_videos"
                value="{video_name}"
            >
            {video}
        </li>
        """

    html += """
    </ul>

    <h2>Upload Query Image</h2>

    <input type="file" name="query">

    <br><br>

    <input type="submit" value="Upload Query">

    </form>
    """

    return html

@app.route("/upload_video", methods=["POST"])
def upload_video():

    file = request.files["video"]

    if file.filename != "":

        save_path = os.path.join(
            VIDEOS_FOLDER,
            file.filename
        )

        file.save(save_path)

        frames_created = process_video(save_path)

        print("TOTAL FRAMES:", frames_created)

        video_name = os.path.splitext(
            file.filename
        )[0]

        process_faces(video_name)
        print("VIDEO PROCESSING COMPLETE")

        

    return redirect("/")

@app.route(
    "/upload_query",
    methods=["POST"]
)
def upload_query():

    global selected_videos

    selected_videos = request.form.getlist(
        "selected_videos"
    )

    file = request.files["query"]

    if file.filename != "":

        save_path = os.path.join(
            QUERY_FOLDER,
            "person.jpg"
        )

        file.save(save_path)

        return redirect("/search")

    return redirect("/")

@app.route("/search")
def search():

    global selected_videos
    #print("Selected Videos =", selected_videos)
    strong_matches, possible_matches = find_matches(
        "query_images/person.jpg",
        selected_videos
    )

    from src.report_generator import generate_report

    report_file = generate_report(
        strong_matches + possible_matches
    )

    global latest_report
    latest_report = report_file
    total_strong = len(strong_matches)
    total_possible = len(possible_matches)
    
    if len(strong_matches) == 0 and len(possible_matches) == 0 :

        return """
        <h1>No Matches Found</h1>
        <a href="/">Back</a>
        """

    html = f"""
    <h1>Results</h1>
    

    <h2>Total Strong Matches: {total_strong}</h2>
    <h2>Total Possible Matches: {total_possible}</h2>
    """

    html += """
    <br>

    <a href="/download_report">
        <button>
            Download Report
        </button>
    </a>

    <br><br>
    """

    html += "<h2>Strong Matches</h2>"

    for video, frame, frame_number, timestamp, score in strong_matches:

        frame_image = (
            frame.split("_face_")[0]
            + ".jpg"
        )

        html += f"""
        <div style="
            margin-bottom:30px;
        ">

            <a href="/frames/{video}/{frame_image}" target="_blank">

                <img
                    src="/frames/{video}/{frame_image}"
                    width="300"
                >
                        
            </a>

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
    html += "<h2>Possible Matches</h2>"

    for video, frame, frame_number, timestamp, score in possible_matches:

        frame_image = (
            frame.split("_face_")[0]
            + ".jpg"
        )

        html += f"""
        <div style="
            margin-bottom:30px;
        ">

            <a href="/frames/{video}/{frame_image}" target="_blank">

                <img
                    src="/frames/{video}/{frame_image}"
                    width="300"
                >

            </a>

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
    return html

@app.route("/frames/<video>/<filename>")
def frame_image(video, filename):

    return send_from_directory(
        os.path.join("frames", video),
        filename
    )

latest_report = ""

@app.route("/download_report")
def download_report():

    global latest_report

    return send_from_directory(
        "results",
        latest_report,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)