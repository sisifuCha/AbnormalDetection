from flask import Flask, Response
from flask_cors import CORS
import cv2
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


def generate_frames(stream_url):
    """增强版视频流生成器，包含自动重连"""
    while True:
        cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                frame = np.zeros((480, 640, 3), dtype=np.uint8)  # 黑帧

            frame = cv2.resize(frame, (640, 480))
            _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        cap.release()
        time.sleep(1)  # 断开后1秒重试


@app.route('/api/stream/<stream_id>')
def video_feed(stream_id):
    return Response(
        generate_frames(f"rtmp://1.92.135.70:9090/live/{stream_id}"),
        mimetype='multipart/x-mixed-replace; boundary=frame',
        headers={
            'Cache-Control': 'no-store',
            'X-Stream-Info': 'RTMP-Proxy'
        }
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)