import cv2
import os

def detect_objects_yolo(frame_folder, output_folder, yolo_model, yolo_cfg, yolo_classes):
    """
    Detects objects in video frames using YOLO.
    """
    os.makedirs(output_folder, exist_ok=True)

    net = cv2.dnn.readNet(yolo_model, yolo_cfg)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    with open(yolo_classes, "r") as f:
        classes = [line.strip() for line in f.readlines()]

    for frame_file in os.listdir(frame_folder):
        frame_path = os.path.join(frame_folder, frame_file)
        image = cv2.imread(frame_path)
        height, width, channels = image.shape

        # YOLO preprocessing
        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Extract detected objects
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = scores.argmax()
                confidence = scores[class_id]
                if confidence > 0.5:
                    print(f"Detected: {classes[class_id]} in {frame_file}")

    print("Object detection complete.")
