

## 🚀 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/Face_recognition_based_attendance_system.git
cd Face_recognition_based_attendance_system
```

### Step 2: Set Up Python Environment (Recommended)
```bash
# Create virtual environment
python -m venv attendance_env

# Activate virtual environment
# On Windows:
attendance_env\Scripts\activate
# On Linux/macOS:
source attendance_env/bin/activate
```

### Step 3: Install Dependencies

⚠️ **CRITICAL**: Remove any existing OpenCV installations first:
```bash
pip uninstall opencv-python opencv-contrib-python -y
```

Install required packages:
```bash
pip install -r requirements.txt
```

### Step 4: Windows-Specific dlib Installation
If dlib installation fails on Windows, use the pre-compiled wheel:
```bash
pip install dlib-19.24.1-cp311-cp311-win_amd64.whl
```

### Step 5: Verify Installation
```bash
python -c "import cv2, dlib, pandas, numpy, PIL; print('✅ All packages installed successfully!')"
```

## 🎮 How to Run

### Start the Application
```bash
python main.py
```

### Initial Setup Process
1. **Launch Application**: Run `python main.py`
2. **Register Students**:
   - Navigate to the "Registration" tab
   - Enter Student ID and Name
   - Click "Capture Images" (captures 100 training images)
   - Click "Train Model" to create the recognition model
3. **Start Attendance Tracking**:
   - Go to "Attendance" tab
   - Click "Start Camera"
   - Enable "Auto Attendance" for automatic marking
4. **Monitor Attendance**: View real-time statistics and attendance log

## 📚 Usage Guide

### 📋 Attendance Tab
- **Camera Controls**: Start/stop camera feed
- **Auto Attendance**: Toggle automatic attendance marking
- **Manual Marking**: Manually mark attendance for testing
- **Live Statistics**: View real-time attendance counts
- **Attendance Log**: See today's attendance records with timestamps and confidence scores

### 👤 Registration Tab
- **Student Enrollment**: Add new students with ID and name validation
- **Image Capture**: Automated capture of 100 training images per student
- **Model Training**: Train the face recognition model with captured data
- **Student Management**: View registered students and their training image counts

### ⚙️ Settings Tab
- **Recognition Threshold**: Adjust confidence level (30-80%) for optimal accuracy
- **System Configuration**: Customize system behavior and preferences

## 📁 Project Structure

```
Face_recognition_based_attendance_system/
├── main.py                       # Main application file
├── requirements.txt              # Python dependencies
├── haarcascade_frontalface_default.xml  # OpenCV face detection cascade
├── dlib-19.24.1-cp311-cp311-win_amd64.whl  # Pre-compiled dlib for Windows
├── LICENSE                       # Project license
├── .gitignore                   # Git ignore patterns
├── StudentDetails/
│   └── StudentDetails.csv        # Student information database
├── TrainingImage/                # Face training images storage
│   └── [StudentName].[SerialNo].[StudentId].[ImageNo].jpg
├── TrainingImageLabel/
│   └── Trainner.yml             # Trained face recognition model
└── Attendance/
    └── Attendance_DD-MM-YYYY.csv  # Daily attendance records
```

## 🔧 Troubleshooting

### Camera Issues
```bash
# Check camera availability
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera working:' if cap.isOpened() else 'Camera not found'); cap.release()"
```
**Solutions**:
- Ensure webcam is connected and not used by other applications
- Try different camera indices (0, 1, 2) if multiple cameras are available
- Check camera permissions in Windows Privacy Settings

### OpenCV Import Errors
```bash
# Complete reinstallation
pip uninstall opencv-python opencv-contrib-python -y
pip install opencv-contrib-python==4.8.1.78
```

### dlib Installation Problems
**For Windows**:
- Use the provided wheel: `pip install dlib-19.24.1-cp311-cp311-win_amd64.whl`
- Install Microsoft Visual C++ 14.0 Build Tools
- For other Python versions, download from [dlib releases](https://github.com/davisking/dlib/releases)

**For Linux**:
```bash
sudo apt-get install cmake libboost-python-dev
pip install dlib
```

### Recognition Accuracy Issues
- **Poor Lighting**: Ensure adequate, even lighting during image capture
- **Image Quality**: Capture images from multiple angles and expressions
- **Threshold Adjustment**: Lower threshold for stricter matching, higher for lenient matching
- **Retrain Model**: If accuracy is consistently poor, recapture images and retrain

### Memory Issues
- **Reduce Image Count**: Modify capture count from 100 to 50 images per student
- **Close Other Applications**: Free up system memory before running
- **Batch Processing**: Train model with fewer students at a time

## 🛠️ Advanced Configuration

### Customizing Recognition Parameters
```python
# In main.py, modify these parameters:
self.attendance_threshold = 50  # Recognition confidence threshold
max_samples = 100  # Number of training images per student
```

### Database Configuration
- **Student Data**: Modify `StudentDetails/StudentDetails.csv` structure if needed
- **Attendance Format**: Customize attendance CSV columns in the `mark_attendance()` function

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Commit Changes**: `git commit -m 'Add amazing feature'`
4. **Push to Branch**: `git push origin feature/amazing-feature`
5. **Create Pull Request**

### Development Guidelines
- Follow PEP 8 coding standards
- Add comments for complex algorithms
- Test thoroughly before submitting
- Update documentation for new features


## 🆘 Support & FAQ

### Common Questions

**Q: Can I use this for commercial purposes?**
A: Yes, under the MIT License, but ensure compliance with data privacy regulations.

**Q: How many students can the system handle?**
A: Tested with up to 100 students; performance may vary based on system specifications.

**Q: Can I integrate this with other systems?**
A: Yes, the CSV output format allows easy integration with other attendance systems.

### Getting Help
- **Issues**: Create an issue on GitHub with detailed error information
- **Documentation**: Check this README and inline code comments
- **Dependencies**: Ensure all requirements are correctly installed

---

**⚡ Quick Start**: `git clone` → `pip install -r requirements.txt` → `python main.py` → Register students → Start attendance!

---

*This system is designed for educational and small-scale attendance tracking. For production deployment, implement additional security measures and data protection protocols.*