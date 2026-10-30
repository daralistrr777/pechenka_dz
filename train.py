from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO('yolov8n.pt')
    results = model.train(
        data='data.yaml',
        epochs=50,
        imgsz=640,
        batch=8,
        workers=0,
        name='cookie_detector',
        patience=20
    )