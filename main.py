############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
from tkinter import filedialog
import cv2
import os
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import threading
from pathlib import Path
import json

############################################# ENHANCED ATTENDANCE SYSTEM ################################################

class AttendanceSystem:
    def __init__(self):
        self.window = tk.Tk()
        self.setup_window()
        self.camera_active = False
        self.recognition_active = False
        self.auto_attendance = False
        self.recognized_today = set()  # Track who was recognized today
        self.attendance_threshold = 50  # Confidence threshold
        self.setup_styles()
        self.setup_ui()
        
    def setup_window(self):
        """Setup main window properties"""
        self.window.geometry("1400x800")
        self.window.resizable(True, True)
        self.window.title("Advanced Face Recognition Attendance System")
        self.window.configure(background='#1a1a2e')
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.window.winfo_screenheight() // 2) - (800 // 2)
        self.window.geometry(f"1400x800+{x}+{y}")

    def setup_styles(self):
        """Setup modern styling"""
        self.colors = {
            'primary': '#16213e',
            'secondary': '#0f3460', 
            'accent': '#e94560',
            'success': '#0abd14',
            'warning': '#ffa500',
            'info': '#17a2b8',
            'light': '#f8f9fa',
            'dark': '#1a1a2e',
            'text': '#ffffff'
        }
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure treeview style
        style.configure("Treeview", 
                       background=self.colors['light'],
                       foreground=self.colors['dark'],
                       fieldbackground=self.colors['light'])
        style.configure("Treeview.Heading",
                       background=self.colors['primary'],
                       foreground=self.colors['text'],
                       font=('Arial', 11, 'bold'))

    def setup_ui(self):
        """Setup the user interface"""
        self.create_header()
        self.create_status_bar()
        self.create_main_content()
        self.start_clock()

    def create_header(self):
        """Create modern header with title and controls"""
        header_frame = tk.Frame(self.window, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame, 
                              text="🎯 Advanced Face Recognition Attendance System", 
                              font=('Arial', 24, 'bold'),
                              bg=self.colors['primary'], 
                              fg=self.colors['text'])
        title_label.pack(side='left', padx=20, pady=20)
        
        # Clock and date frame
        datetime_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        datetime_frame.pack(side='right', padx=20, pady=10)
        
        self.clock_label = tk.Label(datetime_frame, 
                                   font=('Arial', 16, 'bold'),
                                   bg=self.colors['primary'], 
                                   fg=self.colors['warning'])
        self.clock_label.pack()
        
        self.date_label = tk.Label(datetime_frame,
                                  font=('Arial', 12),
                                  bg=self.colors['primary'], 
                                  fg=self.colors['text'])
        self.date_label.pack()

    def create_main_content(self):
        """Create main content area with tabs"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_attendance_tab()
        self.create_registration_tab()
        self.create_reports_tab()
        self.create_settings_tab()

    def create_attendance_tab(self):
        """Create attendance tracking tab"""
        attendance_frame = tk.Frame(self.notebook, bg=self.colors['dark'])
        self.notebook.add(attendance_frame, text="📋 Attendance")
        
        # Left panel - Camera and controls
        left_panel = tk.Frame(attendance_frame, bg=self.colors['secondary'], width=600)
        left_panel.pack(side='left', fill='both', padx=5, pady=5)
        left_panel.pack_propagate(False)
        
        # Camera frame
        camera_frame = tk.LabelFrame(left_panel, text="📷 Camera View", 
                                   font=('Arial', 12, 'bold'),
                                   bg=self.colors['secondary'], 
                                   fg=self.colors['text'])
        camera_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Video display
        self.video_label = tk.Label(camera_frame, 
                                   text="Camera Off\n\nClick 'Start Camera' to begin",
                                   font=('Arial', 14),
                                   bg=self.colors['dark'], 
                                   fg=self.colors['text'])
        self.video_label.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Camera controls
        controls_frame = tk.Frame(left_panel, bg=self.colors['secondary'])
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        self.start_camera_btn = tk.Button(controls_frame, 
                                         text="📹 Start Camera",
                                         command=self.toggle_camera,
                                         font=('Arial', 12, 'bold'),
                                         bg=self.colors['success'], 
                                         fg=self.colors['text'],
                                         activebackground=self.colors['info'],
                                         width=15)
        self.start_camera_btn.pack(side='left', padx=5, pady=5)
        
        self.auto_attendance_btn = tk.Button(controls_frame,
                                           text="🤖 Auto Attendance: OFF",
                                           command=self.toggle_auto_attendance,
                                           font=('Arial', 12, 'bold'),
                                           bg=self.colors['warning'], 
                                           fg=self.colors['text'],
                                           width=20)
        self.auto_attendance_btn.pack(side='left', padx=5, pady=5)
        
        # Manual attendance button for testing
        self.manual_attendance_btn = tk.Button(controls_frame,
                                             text="✋ Manual Mark",
                                             command=self.manual_attendance,
                                             font=('Arial', 10, 'bold'),
                                             bg=self.colors['info'], 
                                             fg=self.colors['text'],
                                             width=12)
        self.manual_attendance_btn.pack(side='left', padx=5, pady=5)
        
        # Recognition status and info
        status_info_frame = tk.Frame(left_panel, bg=self.colors['secondary'])
        status_info_frame.pack(fill='x', pady=5)
        
        self.status_label = tk.Label(status_info_frame,
                                   text="Status: Camera Off",
                                   font=('Arial', 11, 'bold'),
                                   bg=self.colors['secondary'], 
                                   fg=self.colors['text'])
        self.status_label.pack()
        
        # Face detection info
        self.face_info_label = tk.Label(status_info_frame,
                                      text="No faces detected",
                                      font=('Arial', 10),
                                      bg=self.colors['secondary'], 
                                      fg=self.colors['info'])
        self.face_info_label.pack()
        
        # Recognition threshold display
        self.threshold_info_label = tk.Label(status_info_frame,
                                           text="Recognition Threshold: 50%",
                                           font=('Arial', 9),
                                           bg=self.colors['secondary'], 
                                           fg=self.colors['text'])
        self.threshold_info_label.pack()
        
        # Right panel - Attendance table and stats
        right_panel = tk.Frame(attendance_frame, bg=self.colors['secondary'])
        right_panel.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Attendance stats frame
        stats_frame = tk.Frame(right_panel, bg=self.colors['secondary'], height=60)
        stats_frame.pack(fill='x', padx=10, pady=(10,5))
        stats_frame.pack_propagate(False)
        
        # Attendance counters
        self.total_students_label = tk.Label(stats_frame, text="Total Students: 0", 
                                           font=('Arial', 11, 'bold'),
                                           bg=self.colors['secondary'], fg=self.colors['text'])
        self.total_students_label.pack(side='left', padx=10)
        
        self.present_today_label = tk.Label(stats_frame, text="Present Today: 0", 
                                          font=('Arial', 11, 'bold'),
                                          bg=self.colors['success'], fg=self.colors['text'])
        self.present_today_label.pack(side='left', padx=10)
        
        self.last_recognized_label = tk.Label(stats_frame, text="Last: None", 
                                            font=('Arial', 10),
                                            bg=self.colors['secondary'], fg=self.colors['warning'])
        self.last_recognized_label.pack(side='right', padx=10)
        
        # Attendance table frame
        table_frame = tk.LabelFrame(right_panel, text="📊 Today's Attendance Log", 
                                  font=('Arial', 12, 'bold'),
                                  bg=self.colors['secondary'], 
                                  fg=self.colors['text'])
        table_frame.pack(fill='both', expand=True, padx=10, pady=(5,10))
        
        # Treeview for attendance
        self.attendance_tree = ttk.Treeview(table_frame, 
                                          columns=('Name', 'ID', 'Time', 'Confidence', 'Status'),
                                          show='tree headings', height=15)
        
        # Configure columns with better sizing
        self.attendance_tree.column('#0', width=40, minwidth=40)
        self.attendance_tree.column('Name', width=120, minwidth=100)
        self.attendance_tree.column('ID', width=80, minwidth=60)
        self.attendance_tree.column('Time', width=100, minwidth=80)
        self.attendance_tree.column('Confidence', width=80, minwidth=60)
        self.attendance_tree.column('Status', width=80, minwidth=60)
        
        # Configure headings
        self.attendance_tree.heading('#0', text='#')
        self.attendance_tree.heading('Name', text='Student Name')
        self.attendance_tree.heading('ID', text='ID')
        self.attendance_tree.heading('Time', text='Time')
        self.attendance_tree.heading('Confidence', text='Confidence')
        self.attendance_tree.heading('Status', text='Status')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.attendance_tree.yview)
        self.attendance_tree.configure(yscrollcommand=scrollbar.set)
        
        self.attendance_tree.pack(side='left', fill='both', expand=True, padx=(10,0), pady=10)
        scrollbar.pack(side='right', fill='y', pady=10, padx=(0,10))
        
        # Load today's attendance
        self.load_todays_attendance()

    def create_registration_tab(self):
        """Create student registration tab"""
        registration_frame = tk.Frame(self.notebook, bg=self.colors['dark'])
        self.notebook.add(registration_frame, text="👤 Registration")
        
        # Main container
        main_container = tk.Frame(registration_frame, bg=self.colors['dark'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left side - Registration form
        form_frame = tk.LabelFrame(main_container, text="📝 New Student Registration",
                                 font=('Arial', 14, 'bold'),
                                 bg=self.colors['secondary'], 
                                 fg=self.colors['text'])
        form_frame.pack(side='left', fill='y', padx=(0,10), pady=10)
        
        # Student ID
        tk.Label(form_frame, text="Student ID:", 
                font=('Arial', 12, 'bold'),
                bg=self.colors['secondary'], 
                fg=self.colors['text']).pack(anchor='w', padx=20, pady=(20,5))
        
        self.student_id_entry = tk.Entry(form_frame, font=('Arial', 12), width=25)
        self.student_id_entry.pack(padx=20, pady=(0,10))
        
        # Student Name
        tk.Label(form_frame, text="Student Name:", 
                font=('Arial', 12, 'bold'),
                bg=self.colors['secondary'], 
                fg=self.colors['text']).pack(anchor='w', padx=20, pady=(10,5))
        
        self.student_name_entry = tk.Entry(form_frame, font=('Arial', 12), width=25)
        self.student_name_entry.pack(padx=20, pady=(0,10))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=self.colors['secondary'])
        button_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Button(button_frame, text="📸 Capture Images",
                 command=self.capture_training_images,
                 font=('Arial', 12, 'bold'),
                 bg=self.colors['info'], 
                 fg=self.colors['text'],
                 width=20).pack(pady=5)
        
        tk.Button(button_frame, text="🎓 Train Model",
                 command=self.train_model,
                 font=('Arial', 12, 'bold'),
                 bg=self.colors['success'], 
                 fg=self.colors['text'],
                 width=20).pack(pady=5)
        
        tk.Button(button_frame, text="🧹 Clear Fields",
                 command=self.clear_registration_fields,
                 font=('Arial', 12, 'bold'),
                 bg=self.colors['warning'], 
                 fg=self.colors['text'],
                 width=20).pack(pady=5)
        
        # Registration status
        self.reg_status_label = tk.Label(form_frame,
                                       text="Ready for new registration",
                                       font=('Arial', 10),
                                       bg=self.colors['secondary'], 
                                       fg=self.colors['text'],
                                       wraplength=250)
        self.reg_status_label.pack(padx=20, pady=10)
        
        # Right side - Student list
        list_frame = tk.LabelFrame(main_container, text="📋 Registered Students",
                                 font=('Arial', 14, 'bold'),
                                 bg=self.colors['secondary'], 
                                 fg=self.colors['text'])
        list_frame.pack(side='right', fill='both', expand=True, padx=(10,0), pady=10)
        
        # Student list treeview
        self.student_tree = ttk.Treeview(list_frame, 
                                       columns=('ID', 'Name', 'Images'),
                                       show='tree headings', height=20)
        
        self.student_tree.column('#0', width=50, minwidth=50)
        self.student_tree.column('ID', width=100, minwidth=80)
        self.student_tree.column('Name', width=150, minwidth=100)
        self.student_tree.column('Images', width=80, minwidth=60)
        
        self.student_tree.heading('#0', text='#')
        self.student_tree.heading('ID', text='Student ID')
        self.student_tree.heading('Name', text='Name')
        self.student_tree.heading('Images', text='Images')
        
        # Scrollbar for student list
        student_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.student_tree.yview)
        self.student_tree.configure(yscrollcommand=student_scrollbar.set)
        
        self.student_tree.pack(side='left', fill='both', expand=True, padx=(10,0), pady=10)
        student_scrollbar.pack(side='right', fill='y', pady=10, padx=(0,10))
        
        # Load registered students
        self.load_registered_students()

    def create_reports_tab(self):
        """Create reports and analytics tab"""
        reports_frame = tk.Frame(self.notebook, bg=self.colors['dark'])
        self.notebook.add(reports_frame, text="📊 Reports")
        
        # Reports content will be implemented
        tk.Label(reports_frame, 
                text="📈 Reports & Analytics\n\nComing Soon...", 
                font=('Arial', 18, 'bold'),
                bg=self.colors['dark'], 
                fg=self.colors['text']).pack(expand=True)

    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = tk.Frame(self.notebook, bg=self.colors['dark'])
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Settings container
        settings_container = tk.Frame(settings_frame, bg=self.colors['dark'])
        settings_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Recognition settings
        recog_frame = tk.LabelFrame(settings_container, text="🔍 Recognition Settings",
                                  font=('Arial', 14, 'bold'),
                                  bg=self.colors['secondary'], 
                                  fg=self.colors['text'])
        recog_frame.pack(fill='x', pady=10)
        
        # Confidence threshold
        tk.Label(recog_frame, text="Recognition Confidence Threshold:",
                font=('Arial', 12),
                bg=self.colors['secondary'], 
                fg=self.colors['text']).pack(anchor='w', padx=20, pady=(10,5))
        
        self.threshold_var = tk.IntVar(value=50)
        threshold_scale = tk.Scale(recog_frame, from_=30, to=80, 
                                 variable=self.threshold_var,
                                 orient='horizontal',
                                 font=('Arial', 10),
                                 bg=self.colors['secondary'], 
                                 fg=self.colors['text'],
                                 command=self.update_threshold)
        threshold_scale.pack(padx=20, pady=(0,10))
        
        # Password management
        pass_frame = tk.LabelFrame(settings_container, text="🔒 Password Management",
                                 font=('Arial', 14, 'bold'),
                                 bg=self.colors['secondary'], 
                                 fg=self.colors['text'])
        pass_frame.pack(fill='x', pady=10)
        
        tk.Button(pass_frame, text="🔑 Change Password",
                 command=self.change_password,
                 font=('Arial', 12, 'bold'),
                 bg=self.colors['accent'], 
                 fg=self.colors['text'],
                 width=20).pack(padx=20, pady=10)

    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = tk.Frame(self.window, bg=self.colors['primary'], height=30)
        self.status_bar.pack(side='bottom', fill='x')
        self.status_bar.pack_propagate(False)
        
        self.status_text = tk.Label(self.status_bar,
                                   text="Ready - System initialized",
                                   font=('Arial', 10),
                                   bg=self.colors['primary'], 
                                   fg=self.colors['text'])
        self.status_text.pack(side='left', padx=10, pady=5)
        
        # System info
        system_info = tk.Label(self.status_bar,
                             text="Advanced Attendance System v2.0",
                             font=('Arial', 10),
                             bg=self.colors['primary'], 
                             fg=self.colors['text'])
        system_info.pack(side='right', padx=10, pady=5)

    def start_clock(self):
        """Start the clock display"""
        self.update_clock()

    def update_clock(self):
        """Update clock and date display"""
        now = datetime.datetime.now()
        time_str = now.strftime('%H:%M:%S')
        date_str = now.strftime('%A, %B %d, %Y')
        
        self.clock_label.config(text=time_str)
        self.date_label.config(text=date_str)
        
        self.window.after(1000, self.update_clock)

    def toggle_camera(self):
        """Toggle camera on/off"""
        if not self.camera_active:
            self.start_camera()
        else:
            self.stop_camera()

    def start_camera(self):
        """Start camera feed"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                mess.showerror("Camera Error", "Could not open camera!")
                return
            
            self.camera_active = True
            self.start_camera_btn.config(text="🛑 Stop Camera", bg=self.colors['accent'])
            self.status_label.config(text="Status: Camera Active")
            self.update_status("Camera started successfully")
            
            # Load face recognizer
            self.load_recognizer()
            
            # Start video feed
            self.update_video()
            
        except Exception as e:
            mess.showerror("Error", f"Failed to start camera: {str(e)}")

    def stop_camera(self):
        """Stop camera feed"""
        self.camera_active = False
        self.recognition_active = False
        
        if hasattr(self, 'cap'):
            self.cap.release()
        
        self.start_camera_btn.config(text="📹 Start Camera", bg=self.colors['success'])
        self.status_label.config(text="Status: Camera Off")
        self.video_label.config(image="", text="Camera Off\n\nClick 'Start Camera' to begin")
        self.update_status("Camera stopped")

    def load_recognizer(self):
        """Load the trained face recognizer"""
        try:
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            
            if os.path.exists("TrainingImageLabel/Trainner.yml"):
                self.recognizer.read("TrainingImageLabel/Trainner.yml")
                self.recognition_active = True
                self.update_status("Face recognizer loaded successfully")
            else:
                self.recognition_active = False
                self.update_status("No trained model found - recognition disabled")
                
            # Load face detector
            self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            
        except Exception as e:
            self.update_status(f"Error loading recognizer: {str(e)}")
            self.recognition_active = False

    def update_video(self):
        """Update video feed"""
        if self.camera_active and hasattr(self, 'cap'):
            ret, frame = self.cap.read()
            if ret:
                # Process frame for face recognition
                processed_frame = self.process_frame(frame)
                
                # Get the current size of the video label
                self.video_label.update_idletasks()  # Ensure label is properly sized
                label_width = self.video_label.winfo_width()
                label_height = self.video_label.winfo_height()
                
                # Use reasonable default if label not sized yet
                if label_width <= 1:
                    label_width = 480
                if label_height <= 1:
                    label_height = 360
                
                # Calculate aspect ratio preserving resize
                frame_height, frame_width = processed_frame.shape[:2]
                aspect_ratio = frame_width / frame_height
                
                # Calculate target size while maintaining aspect ratio
                if label_width / label_height > aspect_ratio:
                    # Label is wider than frame aspect ratio
                    target_height = label_height - 20  # Leave some padding
                    target_width = int(target_height * aspect_ratio)
                else:
                    # Label is taller than frame aspect ratio
                    target_width = label_width - 20  # Leave some padding
                    target_height = int(target_width / aspect_ratio)
                
                # Ensure minimum size
                target_width = max(320, target_width)
                target_height = max(240, target_height)
                
                # Convert frame to display format
                frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                frame_pil = Image.fromarray(frame_rgb)
                frame_pil = frame_pil.resize((target_width, target_height), Image.Resampling.LANCZOS)
                frame_tk = ImageTk.PhotoImage(frame_pil)
                
                self.video_label.config(image=frame_tk, text="")
                self.video_label.image = frame_tk
            
            # Schedule next update
            self.window.after(10, self.update_video)

    def process_frame(self, frame):
        """Process frame for face detection and recognition"""
        if not self.recognition_active:
            # Update face info for no recognition
            self.face_info_label.config(text="Face recognition not loaded", fg=self.colors['warning'])
            return frame
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Update face detection info
        if len(faces) == 0:
            self.face_info_label.config(text="No faces detected", fg=self.colors['info'])
        else:
            self.face_info_label.config(text=f"{len(faces)} face(s) detected", fg=self.colors['success'])
        
        recognized_faces = 0
        for (x, y, w, h) in faces:
            # Draw different colored rectangles based on recognition status
            rect_color = (0, 255, 0)  # Green by default
            
            try:
                # Recognize face
                face_roi = gray[y:y+h, x:x+w]
                id_, confidence = self.recognizer.predict(face_roi)
                
                if confidence < self.attendance_threshold:
                    # Get student info
                    name = self.get_student_name(id_)
                    if name:
                        recognized_faces += 1
                        rect_color = (0, 255, 0)  # Green for recognized
                        
                        # Check if already marked today
                        if id_ in self.recognized_today:
                            cv2.putText(frame, f"{name} - Already Present", 
                                      (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                            cv2.putText(frame, f"Confidence: {confidence:.1f}%", 
                                      (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        else:
                            cv2.putText(frame, f"{name}", 
                                      (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            cv2.putText(frame, f"Confidence: {confidence:.1f}%", 
                                      (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                            
                            # Auto attendance
                            if self.auto_attendance:
                                self.mark_attendance(id_, name, confidence)
                                self.recognized_today.add(id_)
                                # Add visual indicator for attendance marking
                                cv2.putText(frame, "ATTENDANCE MARKED!", 
                                          (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    else:
                        cv2.putText(frame, f"Unknown ID: {id_}", 
                                  (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                        cv2.putText(frame, f"Confidence: {confidence:.1f}%", 
                                  (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                        rect_color = (0, 255, 255)  # Yellow for unknown ID
                else:
                    cv2.putText(frame, "Unknown Person", 
                              (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    cv2.putText(frame, f"Low Confidence: {confidence:.1f}%", 
                              (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    rect_color = (0, 0, 255)  # Red for unknown
                    
            except Exception as e:
                cv2.putText(frame, "Recognition Error", 
                          (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 0, 128), 2)
                rect_color = (128, 0, 128)  # Purple for errors
            
            # Draw rectangle with appropriate color
            cv2.rectangle(frame, (x, y), (x+w, y+h), rect_color, 2)
        
        # Update recognition status
        if len(faces) > 0:
            if recognized_faces > 0:
                self.face_info_label.config(text=f"{recognized_faces}/{len(faces)} faces recognized", 
                                          fg=self.colors['success'])
            else:
                self.face_info_label.config(text=f"{len(faces)} faces detected, none recognized", 
                                          fg=self.colors['warning'])
        
        return frame

    def get_student_name(self, student_id):
        """Get student name from ID"""
        try:
            if os.path.exists("StudentDetails/StudentDetails.csv"):
                df = pd.read_csv("StudentDetails/StudentDetails.csv")
                student_row = df[df['SERIAL NO.'] == student_id]
                if not student_row.empty:
                    return student_row.iloc[0]['NAME']
        except Exception as e:
            pass
        return None

    def mark_attendance(self, student_id, name, confidence):
        """Mark attendance for a student"""
        try:
            now = datetime.datetime.now()
            date_str = now.strftime('%d-%m-%Y')
            time_str = now.strftime('%H:%M:%S')
            
            # Create attendance record
            attendance_file = f"Attendance/Attendance_{date_str}.csv"
            self.assure_path_exists(attendance_file)
            
            # Check if attendance already marked
            attendance_exists = False
            if os.path.exists(attendance_file):
                try:
                    df = pd.read_csv(attendance_file)
                    if not df.empty and student_id in df['Id'].values:
                        attendance_exists = True
                        self.update_status(f"{name} already marked present today")
                        return
                except:
                    pass
            
            if not attendance_exists:
                # Add to CSV
                file_exists = os.path.exists(attendance_file)
                with open(attendance_file, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    if not file_exists:
                        writer.writerow(['Id', 'Name', 'Date', 'Time', 'Confidence'])
                    writer.writerow([student_id, name, date_str, time_str, f"{confidence:.1f}"])
                
                # Get current count for display
                current_count = len(self.attendance_tree.get_children()) + 1
                
                # Add to treeview with better formatting
                self.attendance_tree.insert('', 0, 
                                          text=str(current_count),
                                          values=(name, student_id, time_str, f"{confidence:.1f}%", "✅ Present"))
                
                # Update counters
                self.update_attendance_stats()
                self.last_recognized_label.config(text=f"Last: {name} at {time_str}")
                
                # Flash recognition success
                self.flash_recognition_success(name)
                
                self.update_status(f"✅ Attendance marked for {name} (Confidence: {confidence:.1f}%)")
            
        except Exception as e:
            self.update_status(f"❌ Error marking attendance: {str(e)}")

    def toggle_auto_attendance(self):
        """Toggle automatic attendance marking"""
        self.auto_attendance = not self.auto_attendance
        
        if self.auto_attendance:
            self.auto_attendance_btn.config(text="🤖 Auto Attendance: ON", bg=self.colors['success'])
            self.update_status("Auto attendance enabled")
            # Reset recognized today set
            self.recognized_today.clear()
        else:
            self.auto_attendance_btn.config(text="🤖 Auto Attendance: OFF", bg=self.colors['warning'])
            self.update_status("Auto attendance disabled")

    def update_attendance_stats(self):
        """Update attendance statistics display"""
        try:
            # Count total registered students
            total_students = 0
            if os.path.exists("StudentDetails/StudentDetails.csv"):
                df = pd.read_csv("StudentDetails/StudentDetails.csv")
                total_students = len(df) - 1 if len(df) > 0 else 0  # Subtract header
            
            # Count present today
            present_today = len(self.attendance_tree.get_children())
            
            # Update labels
            self.total_students_label.config(text=f"Total Students: {total_students}")
            self.present_today_label.config(text=f"Present Today: {present_today}")
            
            # Update attendance percentage
            if total_students > 0:
                percentage = (present_today / total_students) * 100
                self.present_today_label.config(text=f"Present Today: {present_today}/{total_students} ({percentage:.1f}%)")
            
        except Exception as e:
            pass

    def flash_recognition_success(self, name):
        """Flash visual feedback when attendance is marked"""
        try:
            # Change status label color temporarily
            original_bg = self.status_label.cget('bg')
            self.status_label.config(bg=self.colors['success'], 
                                   text=f"✅ ATTENDANCE MARKED: {name}")
            
            # Reset after 2 seconds
            self.window.after(2000, lambda: self.status_label.config(
                bg=original_bg, 
                text="Status: Auto attendance active"))
                
        except Exception as e:
            pass

    def load_todays_attendance(self):
        """Load today's attendance records"""
        try:
            # Clear existing items
            for item in self.attendance_tree.get_children():
                self.attendance_tree.delete(item)
            
            date_str = datetime.datetime.now().strftime('%d-%m-%Y')
            attendance_file = f"Attendance/Attendance_{date_str}.csv"
            
            if os.path.exists(attendance_file):
                df = pd.read_csv(attendance_file)
                for index, row in df.iterrows():
                    self.attendance_tree.insert('', 'end', 
                                              text=str(index+1),
                                              values=(row.get('Name', ''), 
                                                     row.get('Id', ''), 
                                                     row.get('Time', ''),
                                                     f"{row.get('Confidence', '0')}%",
                                                     '✅ Present'))
                    
                    # Add recognized IDs to today's set
                    if 'Id' in row:
                        self.recognized_today.add(row['Id'])
            
            # Update stats
            self.update_attendance_stats()
            
            # Update last recognized if there are records
            if len(self.attendance_tree.get_children()) > 0:
                last_item = self.attendance_tree.get_children()[0]
                last_values = self.attendance_tree.item(last_item)['values']
                if len(last_values) >= 3:
                    self.last_recognized_label.config(text=f"Last: {last_values[0]} at {last_values[2]}")
                                                     
            self.update_status(f"Loaded {len(self.attendance_tree.get_children())} attendance records for today")
            
        except Exception as e:
            self.update_status(f"Error loading attendance: {str(e)}")

    def capture_training_images(self):
        """Capture training images for a new student"""
        student_id = self.student_id_entry.get().strip()
        student_name = self.student_name_entry.get().strip()
        
        if not student_id or not student_name:
            mess.showerror("Input Error", "Please enter both Student ID and Name!")
            return
        
        if not student_name.replace(' ', '').isalpha():
            mess.showerror("Input Error", "Please enter a valid name (letters only)!")
            return
        
        try:
            # Check if student already exists
            if self.student_exists(student_id):
                if not mess.askyesno("Student Exists", 
                                    f"Student with ID {student_id} already exists. Continue anyway?"):
                    return
            
            # Start image capture in separate thread
            threading.Thread(target=self._capture_images_thread, 
                           args=(student_id, student_name), daemon=True).start()
            
        except Exception as e:
            mess.showerror("Error", f"Failed to start image capture: {str(e)}")

    def _capture_images_thread(self, student_id, student_name):
        """Thread function for capturing images"""
        try:
            self.update_status("Starting image capture...")
            
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                mess.showerror("Camera Error", "Could not open camera!")
                return
            
            face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            
            # Get serial number
            serial = self.get_next_serial()
            
            sample_count = 0
            max_samples = 100
            
            self.reg_status_label.config(text=f"Capturing images for {student_name}...\nPress 'q' to stop")
            
            while sample_count < max_samples:
                ret, img = cap.read()
                if not ret:
                    continue
                
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    sample_count += 1
                    
                    # Save the face
                    face_img = gray[y:y+h, x:x+w]
                    img_name = f"TrainingImage/{student_name}.{serial}.{student_id}.{sample_count}.jpg"
                    cv2.imwrite(img_name, face_img)
                    
                    # Show progress
                    progress_text = f"Captured: {sample_count}/{max_samples}"
                    cv2.putText(img, progress_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.imshow('Capturing Training Images', img)
                
                if cv2.waitKey(1) & 0xFF == ord('q') or sample_count >= max_samples:
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            
            if sample_count > 0:
                # Save student details
                self.save_student_details(serial, student_id, student_name)
                self.reg_status_label.config(text=f"Successfully captured {sample_count} images for {student_name}")
                self.load_registered_students()
                mess.showinfo("Success", f"Successfully captured {sample_count} images for {student_name}!")
            else:
                self.reg_status_label.config(text="No face detected. Please try again.")
                mess.showwarning("Warning", "No face was detected. Please try again.")
                
        except Exception as e:
            mess.showerror("Error", f"Error during image capture: {str(e)}")
            self.reg_status_label.config(text="Error occurred during capture")

    def student_exists(self, student_id):
        """Check if student ID already exists"""
        try:
            if os.path.exists("StudentDetails/StudentDetails.csv"):
                df = pd.read_csv("StudentDetails/StudentDetails.csv")
                return student_id in df['ID'].astype(str).values
        except:
            pass
        return False

    def get_next_serial(self):
        """Get next serial number for student"""
        try:
            if os.path.exists("StudentDetails/StudentDetails.csv"):
                df = pd.read_csv("StudentDetails/StudentDetails.csv")
                if not df.empty:
                    return df['SERIAL NO.'].max() + 1
        except:
            pass
        return 1

    def save_student_details(self, serial, student_id, student_name):
        """Save student details to CSV"""
        try:
            self.assure_path_exists("StudentDetails/StudentDetails.csv")
            
            # Check if file exists and has headers
            file_exists = os.path.exists("StudentDetails/StudentDetails.csv")
            
            with open("StudentDetails/StudentDetails.csv", 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(['SERIAL NO.', '', 'ID', '', 'NAME'])
                writer.writerow([serial, '', student_id, '', student_name])
                
        except Exception as e:
            raise Exception(f"Error saving student details: {str(e)}")

    def train_model(self):
        """Train the face recognition model"""
        try:
            if not os.path.exists("TrainingImage") or len(os.listdir("TrainingImage")) == 0:
                mess.showerror("No Training Data", "No training images found! Please capture some images first.")
                return
            
            self.reg_status_label.config(text="Training model... Please wait...")
            self.update_status("Training face recognition model...")
            
            # Train in separate thread to avoid blocking UI
            threading.Thread(target=self._train_model_thread, daemon=True).start()
            
        except Exception as e:
            mess.showerror("Error", f"Error starting model training: {str(e)}")

    def _train_model_thread(self):
        """Thread function for model training"""
        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            
            faces, ids = self.get_images_and_labels("TrainingImage")
            
            if len(faces) == 0:
                mess.showerror("No Training Data", "No valid training images found!")
                self.reg_status_label.config(text="Training failed - no valid images")
                return
            
            recognizer.train(faces, np.array(ids))
            
            # Save the model
            self.assure_path_exists("TrainingImageLabel/Trainner.yml")
            recognizer.save("TrainingImageLabel/Trainner.yml")
            
            self.reg_status_label.config(text=f"Model trained successfully with {len(faces)} images!")
            self.update_status("Model training completed successfully")
            mess.showinfo("Success", f"Model trained successfully with {len(faces)} images!")
            
        except Exception as e:
            mess.showerror("Error", f"Error during model training: {str(e)}")
            self.reg_status_label.config(text="Training failed")

    def get_images_and_labels(self, path):
        """Get images and labels for training"""
        image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
        faces = []
        ids = []
        
        for image_path in image_paths:
            try:
                # Load image
                pil_image = Image.open(image_path).convert('L')
                image_np = np.array(pil_image, 'uint8')
                
                # Extract ID from filename
                filename = os.path.basename(image_path)
                parts = filename.split('.')
                if len(parts) >= 2:
                    student_serial = int(parts[1])  # Use serial number as ID
                    faces.append(image_np)
                    ids.append(student_serial)
                    
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
                continue
        
        return faces, ids

    def load_registered_students(self):
        """Load registered students into the treeview"""
        try:
            # Clear existing items
            for item in self.student_tree.get_children():
                self.student_tree.delete(item)
            
            if os.path.exists("StudentDetails/StudentDetails.csv"):
                df = pd.read_csv("StudentDetails/StudentDetails.csv")
                for index, row in df.iterrows():
                    if pd.notna(row['ID']) and pd.notna(row['NAME']):
                        # Count training images
                        image_count = self.count_training_images(row['SERIAL NO.'])
                        
                        self.student_tree.insert('', 'end',
                                               text=str(row['SERIAL NO.']),
                                               values=(str(row['ID']), 
                                                      str(row['NAME']), 
                                                      str(image_count)))
                                                      
        except Exception as e:
            self.update_status(f"Error loading students: {str(e)}")

    def count_training_images(self, serial_no):
        """Count training images for a student"""
        try:
            if os.path.exists("TrainingImage"):
                count = 0
                for filename in os.listdir("TrainingImage"):
                    if filename.endswith('.jpg'):
                        parts = filename.split('.')
                        if len(parts) >= 2 and parts[1] == str(serial_no):
                            count += 1
                return count
        except:
            pass
        return 0

    def clear_registration_fields(self):
        """Clear registration form fields"""
        self.student_id_entry.delete(0, tk.END)
        self.student_name_entry.delete(0, tk.END)
        self.reg_status_label.config(text="Ready for new registration")

    def update_threshold(self, value):
        """Update recognition threshold"""
        self.attendance_threshold = int(value)
        if hasattr(self, 'threshold_info_label'):
            self.threshold_info_label.config(text=f"Recognition Threshold: {value}%")
        self.update_status(f"Recognition threshold set to {value}%")

    def manual_attendance(self):
        """Manually mark attendance for testing"""
        try:
            # Get available students
            if not os.path.exists("StudentDetails/StudentDetails.csv"):
                mess.showwarning("No Students", "No students registered yet!")
                return
            
            df = pd.read_csv("StudentDetails/StudentDetails.csv")
            if df.empty:
                mess.showwarning("No Students", "No students registered yet!")
                return
            
            # Create selection dialog
            student_names = []
            for index, row in df.iterrows():
                if pd.notna(row.get('NAME')):
                    student_names.append(f"{row['NAME']} (ID: {row.get('ID', 'N/A')})")
            
            if not student_names:
                mess.showwarning("No Students", "No valid student records found!")
                return
            
            # Simple selection (you could make this a proper dialog)
            selected = tsd.askstring("Manual Attendance", 
                                   f"Available students:\n" + "\n".join(student_names[:5]) + 
                                   "\n\nEnter student name to mark attendance:")
            
            if selected:
                # Find matching student
                for index, row in df.iterrows():
                    if selected.lower() in str(row.get('NAME', '')).lower():
                        self.mark_attendance(row.get('SERIAL NO.', 0), 
                                           row.get('NAME', 'Unknown'), 
                                           95.0)  # High confidence for manual
                        return
                
                mess.showwarning("Not Found", f"Student '{selected}' not found!")
                        
        except Exception as e:
            mess.showerror("Error", f"Manual attendance error: {str(e)}")

    def change_password(self):
        """Change system password"""
        # This would open a password change dialog
        mess.showinfo("Change Password", "Password change functionality will be implemented")

    def update_status(self, message):
        """Update status bar message"""
        self.status_text.config(text=message)
        print(f"Status: {message}")  # Also log to console

    def assure_path_exists(self, path):
        """Ensure directory exists"""
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def run(self):
        """Start the application"""
        try:
            # Check required files
            if not os.path.exists("haarcascade_frontalface_default.xml"):
                mess.showerror("Missing File", 
                             "haarcascade_frontalface_default.xml not found!\n"
                             "Please ensure this file is in the same directory.")
                return
            
            # Create necessary directories
            for directory in ["StudentDetails", "TrainingImage", "TrainingImageLabel", "Attendance"]:
                if not os.path.exists(directory):
                    os.makedirs(directory)
            
            self.update_status("System ready - Welcome to Advanced Attendance System!")
            self.window.mainloop()
            
        except Exception as e:
            mess.showerror("Startup Error", f"Failed to start application: {str(e)}")
        finally:
            # Cleanup
            if hasattr(self, 'cap') and self.cap.isOpened():
                self.cap.release()
            cv2.destroyAllWindows()

# Run the application
if __name__ == "__main__":
    app = AttendanceSystem()
    app.run()