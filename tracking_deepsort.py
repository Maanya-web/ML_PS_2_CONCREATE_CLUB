from ultralytics import YOLO
import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort
import pickle

model = YOLO("best.pt")

tracker = DeepSort(max_age=25)

cap = cv2.VideoCapture("C:\\Users\\proga\\Downloads\\LIG Square Evening 5.30-5.45PM.mp4")

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(
    "tracked_output.mp4",
    fourcc,
    30.0,
    (int(cap.get(3)), int(cap.get(4)))
)

trajectories = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]

    dets = []
    for box in results.boxes:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        conf = float(box.conf.cpu().numpy())
        cls = int(box.cls.cpu().numpy())

        dets.append(([x1, y1, x2-x1, y2-y1], conf, cls))

    tracks = tracker.update_tracks(dets, frame=frame)

    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, r, b = track.to_ltrb()
        cx = int((l + r) / 2)
        cy = int((t + b) / 2)

        if track_id not in trajectories:
            trajectories[track_id] = []
        trajectories[track_id].append((cx, cy))

        cv2.rectangle(frame, (int(l), int(t)), (int(r), int(b)), (255,0,0), 2)
        cv2.putText(frame, f"ID {track_id}", (int(l), int(t)-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    out.write(frame)

    display = cv2.resize(frame, (1280, 720))
    cv2.imshow("Tracking", display)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

with open("trajectories.pkl", "wb") as f:
    pickle.dump(trajectories, f)

print("Trajectories Saved")
