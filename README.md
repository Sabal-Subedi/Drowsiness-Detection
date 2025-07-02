# Drowsiness Detection using Embedded System
Author: Sabal Subedi
Institution: Idaho State University, Department of Computer Science
Contact: sabalsubedi@isu.edu

### Overview
This is a real-time drowsiness detection system that combines computer vision with embedded Bluetooth Low Energy (BLE) communication. It leverages Python-based facial landmark analysis and an Arduino-based feedback system to proactively alert users to signs of fatigue.

When drowsiness is detected—based on prolonged eye closure or head nodding—a BLE signal is sent from the computer vision system to the Arduino. The Arduino then activates a buzzer, LED, and LCD to provide immediate auditory and visual feedback. A reset button allows the user to silence the alert and reset the system.

### Features
- Real-time facial monitoring using webcam
- Drowsiness detection via Eye Aspect Ratio (EAR) and head nodding
- BLE-based communication with embedded system
- Visual (LED, LCD) and auditory (buzzer) driver alerts
- Reset functionality with a physical button
- Modular and portable design

### Technologies Used
- Python (OpenCV, MediaPipe, sockets, BLE communication)
- Arduino (BLE module, buzzer, LED, LCD, push button)
- Hardware: Webcam, Arduino board (e.g., Uno with BLE support), peripherals

### System Architecture
+--------------------+      BLE       +-----------------------------+
|  Python CV Module  | <------------> | Arduino BLE Alert System    |
| - MediaPipe        |                | - Buzzer                    |
| - Eye/Head Tracking|                | - LED                       |
| - EAR Detection    |                | - LCD Display               |
| - Head Nod Logic   |                | - Reset Button              |
+--------------------+                +-----------------------------+

### Drowsiness Detection Logic
- EAR (Eye Aspect Ratio) is computed to track eye closure.
- Head nodding is detected using vertical displacement of nose landmarks.
- If either condition persists for a threshold number of frames, drowsiness is assumed.
- An "ALERT" is sent to Arduino; a "RESET" can be triggered by user.

### Getting Started
#### Prerequisites
- Python 3.8+
- Arduino IDE
- Webcam
- BLE-compatible Arduino board (e.g., with HM-10 or built-in BLE)

#### Required Python packages:
- pip install opencv-python mediapipe bleak
- Python Computer Vision Setup
- Clone the repository:
- git clone https://github.com/yourusername/drowsiness-detection-system.git
- cd drowsiness-detection-system

#### Run the drowsiness detection script:
- python drowsiness_detector.py
- Make sure Arduino is paired and BLE server is running.

- Arduino Setup
    - Open the Arduino sketch (ble_alert_system.ino) in the Arduino IDE.
    - Upload it to your Arduino board.
    - Connect buzzer, LED, LCD, and button according to defined pins in the sketch.

#### Hardware Connections
Component	Arduino Pin
Buzzer	    D3
LED	        D4
LCD	        I2C (SDA/SCL)
Button	    D2

### Usage
- Launch the Python detection script.
- Sit in front of the webcam.
- When drowsiness is detected:
    - LED turns on
    - Buzzer beeps
    - LCD shows alert message
    - Press the button on the Arduino to reset the alert.

### Applications
- Driver fatigue monitoring
- Industrial worker safety
- Operator alert systems
- Personal health tracking

### Future Improvements
- Implement automatic logging of drowsiness events
- Improve accuracy with more landmarks or ML models
- Integrate GPS for automotive use
- Support multiple users or multi-face detection

### License
This project is for educational purposes.