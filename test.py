import cv2

stream_url = 'rtmp://1.92.135.70:9090/live/1'

cap = cv2.VideoCapture(stream_url)
print('打开状态:', cap.isOpened())  # True表示成功打开流

ret, frame = cap.read()
print('读取状态:', ret)  # True表示成功读取到一帧

if ret:
    cv2.imwrite('test.jpg', frame)
    print('已保存一帧图片到 test.jpg')
else:
    print('没有读取到视频帧')

cap.release()