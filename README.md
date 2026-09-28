# Face Recognition Attendance using Python

A desktop attendance system that uses OpenCV face detection and recognition to enroll students, train a local model, and record attendance from a camera feed.

## Capabilities

- Student registration and automated training-image capture
- Local face-model training with OpenCV
- Real-time recognition and attendance marking
- Attendance logs with timestamps and confidence values
- Windows helper script and a documented Python setup

## Requirements

- Python 3.11 is recommended
- A webcam
- OpenCV, NumPy, Pandas, Pillow, and dlib dependencies from `requirements.txt`
- Windows users may use the included compatible dlib wheel when appropriate

## Setup and run

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

Use the registration workflow to capture a student’s images, train the recognizer, and then start attendance mode. Generated student records and training images should remain local and must not be committed to a public repository.

## Important privacy note

This project processes biometric data. Use it only with informed consent, protect captured images and attendance records, and follow the privacy rules that apply in your location. The bundled model and cascade are for demonstration and learning.

## License

Released under the MIT License. See [LICENSE](LICENSE).
