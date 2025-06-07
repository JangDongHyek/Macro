from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # 처음 학습이면 .pt 모델 사용

model.train(
    data="./monster_dataset/data.yaml",
    epochs=50,
    imgsz=640,
    batch=8,
    project="monster_train",
    name="yolov8_model",
    exist_ok=True
)

#  yolo는 느리기떄문에 학습된 파일 만들고 터미널 에서
#  yolo export model=monster_train/yolov8_model/weights/best.pt format=onnx nms=True
#  onnx 파일로 변환후 서치시작해야함

# CUDA Toolkit 12.x 설치 필수
