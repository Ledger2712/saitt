# counter/utils.py
import cv2
import torch
import numpy as np
from .tracker import Tracker   # скопируйте сюда tracker.py из вашего PythonProject

# загружаем модель
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def gen_frames(source='2.mp4'):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError("Не удалось открыть видеофайл")

    tracker = Tracker()
    area = [(465, 494),(465, 250),(490, 250),(490, 494)]
    seen_ids = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (1020, 500))
        cv2.polylines(frame, [np.array(area, np.int32)], True, (255,255,255), 3)

        # детекция
        results = model(frame)
        persons = []
        for *box, conf, cls in results.xyxy[0].cpu().numpy():
            if int(cls) == 0:  # класс person
                x1,y1,x2,y2 = map(int, box)
                persons.append([x1,y1,x2,y2])

        # трекинг + подсчёт
        boxes_ids = tracker.update(persons)
        for x1,y1,x2,y2,oid in boxes_ids:
            if cv2.pointPolygonTest(np.array(area, np.int32),(x2,y2),False) > 0:
                seen_ids.add(oid)
            cv2.rectangle(frame, (x1,y1), (x2,y2), (255,0,255), 2)

        cnt = len(seen_ids)
        # overlay
        ovr = frame.copy()
        cv2.rectangle(ovr, (10,10), (200,70), (0,0,0), -1)
        cv2.addWeighted(ovr, 0.5, frame, 0.5, 0, frame)
        cv2.putText(frame, f'Count: {cnt}', (20,60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3)

        # JPEG и отдаём в поток
        ret2, jpg = cv2.imencode('.jpg', frame)
        if not ret2:
            continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() + b'\r\n')
