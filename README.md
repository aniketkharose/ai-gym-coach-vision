# 🏋️ AI Real-time GYM Coach

> A real-time AI-powered gym coach using computer vision, pose
> detection, repetition tracking, workout metrics, and AI voice
> coaching.

## 🚀 Live Demo

https://ai-gym-coach-vision.streamlit.app/

## 📌 Project Overview

AI Real-time GYM Coach is a computer-vision-based fitness application
built with Python and Streamlit.

The application uses a webcam to detect body pose in real time.
Exercise-specific detectors analyze body landmarks, calculate joint
angles, count repetitions, track sets, evaluate exercise form, and
provide AI-powered coaching feedback.

Completed workout activity is also stored and displayed as workout
history for the logged-in user.

## ✨ Features

-   🎥 Real-time webcam workout analysis
-   🧍 Real-time human pose detection
-   🔢 Automatic repetition counting
-   📊 Set and repetition progress tracking
-   📐 Real-time exercise metrics
-   ✅ Exercise form/status detection
-   🤖 AI-powered coaching feedback
-   🔊 AI voice coaching
-   📜 Workout history
-   🔐 User login
-   💾 Workout data persistence
-   🌐 WebRTC-based real-time camera streaming
-   ☁️ Streamlit Cloud deployment

## 🏋️ Supported Exercises

### 1. Squats

-   Knee angle
-   Back angle
-   Depth status

### 2. Push-ups

-   Elbow angle
-   Body alignment
-   Hip position

### 3. Biceps Curls (Dumbbell)

-   Elbow angle
-   Shoulder stability
-   Swing detection

### 4. Shoulder Press

-   Elbow angle
-   Arm extension
-   Back arch

### 5. Lunges

-   Front knee angle
-   Torso angle
-   Balance status

## 🧠 How It Works

``` text
Webcam
   ↓
MediaPipe Pose Detection
   ↓
Body Landmarks
   ↓
Exercise Detector
   ↓
Rep + Set Tracking
   ↓
Form / Angle Analysis
   ↓
Workout Progress
   ↓
AI Coach
   ↓
Voice Feedback
   ↓
Workout History
```

## 🛠️ Technology Stack

  Technology         Purpose
  ------------------ --------------------------------------
  Python             Core application development
  Streamlit          Web application UI
  MediaPipe          Human pose detection
  OpenCV             Computer vision and frame processing
  NumPy              Numerical calculations
  streamlit-webrtc   Real-time webcam streaming
  Groq               AI coaching responses
  Text-to-Speech     Voice feedback
  Twilio             WebRTC ICE server configuration
  SQLite             Workout data persistence
  Pandas             Workout history processing
  python-dotenv      Local environment configuration

## 📂 Project Structure

``` text
ai-gym-coach-vision/
│
├── .devcontainer/
├── .streamlit/
│
├── core/
│   └── Base exercise logic
│
├── detectors/
│   ├── squat.py
│   ├── pushup.py
│   ├── biceps_curl.py
│   ├── shoulder_press.py
│   └── lunges.py
│
├── ml_models/
│   └── pose_landmarker_full.task
│
├── services/
│   ├── auth/
│   ├── coaching/
│   ├── config/
│   ├── persistence/
│   ├── state/
│   ├── tracking/
│   ├── ui/
│   └── vision/
│
├── static/
│   ├── style.css
│   └── AdobeClean.otf
│
├── .gitignore
├── README.md
├── main.py
├── packages.txt
└── requirements.txt
```

## ⚙️ Local Setup

### 1. Clone the repository

``` bash
git clone https://github.com/aniketkharose/ai-gym-coach-vision.git
cd ai-gym-coach-vision
```

### 2. Create a virtual environment

#### Windows

``` bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

``` env
GROQ_API_KEY=your_groq_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
```

**Never commit `.env` or API keys to GitHub.**

### 5. Run the application

``` bash
streamlit run main.py
```

## 🔐 Configuration & Secrets

For local development, sensitive credentials are read from environment
variables.

For Streamlit Cloud, configure the required values using Streamlit
Secrets.

Sensitive values include:

``` text
GROQ_API_KEY
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
```

Do not place real credentials directly inside Python source files or
commit them to GitHub.

If a credential is accidentally exposed publicly, revoke or rotate it
immediately.

## ☁️ Deployment

The application is deployed using Streamlit Cloud.

### Deployment steps

1.  Push the project to GitHub.
2.  Open Streamlit Cloud.
3.  Create a new application.
4.  Select this GitHub repository.
5.  Set the main file to `main.py`.
6.  Add the required secrets in Streamlit Cloud.
7.  Deploy the application.

### Live Application

https://ai-gym-coach-vision.streamlit.app/

## 📸 Screenshots

Add screenshots of the following sections to this README:

### 🏠 Workout Setup

Show the exercise selection, sets, repetitions, and Start Workout
interface.

### 🎥 Real-time AI Coaching

Show the webcam feed with pose landmarks and the AI coaching message.

### 📊 Progress & Exercise Metrics

Show total repetitions, current set repetitions, completed sets, and
exercise-specific metrics.

### 📜 Workout History

Show the saved workout history table.

## 🎯 Workout Tracking

Before starting a workout, the user can select:

-   Exercise
-   Number of sets
-   Repetitions per set

During the workout, the application tracks:

``` text
Total Reps
Current Set Reps
Sets Completed
```

When a set is completed, workout data can be saved to the persistence
layer.

## 📐 Exercise Metrics

Different exercises use different metrics.

### Squats

``` text
Knee Angle
Back Angle
Depth Status
```

### Push-ups

``` text
Elbow Angle
Body Alignment
Hip Position
```

### Biceps Curls

``` text
Elbow Angle
Shoulder Stability
Swing Detection
```

### Shoulder Press

``` text
Elbow Angle
Arm Extension
Back Arch
```

### Lunges

``` text
Front Knee Angle
Torso Angle
Balance Status
```

## 🤖 AI Coaching

The application includes an AI coaching pipeline that generates
contextual feedback based on workout events and exercise metrics.

Coaching events include:

-   Workout started
-   Set completed
-   Workout completed
-   No pose detected
-   Ongoing form checks

Feedback can be displayed on screen and delivered through voice output.

## 🗃️ Workout History

Completed workout activity is persisted and displayed in the Workout
History section.

The history includes:

  Field        Description
  ------------ ---------------------------
  Exercise     Exercise performed
  Date         Workout date
  Reps         Repetitions performed
  Sets         Sets completed
  Time (sec)   Recorded workout/set time

## 🔒 Security Checklist

Before pushing changes to GitHub:

-   [ ] `.env` is not committed
-   [ ] API keys are not inside source code
-   [ ] Twilio credentials are stored securely
-   [ ] Groq API key is stored securely
-   [ ] No passwords are committed
-   [ ] No private tokens are committed
-   [ ] `.gitignore` is configured correctly
-   [ ] Streamlit Cloud secrets are configured separately

## 🧪 Testing

The deployed application has been tested for the main workout workflow,
including:

-   User login
-   Workout plan selection
-   Camera activation
-   Pose detection
-   Repetition tracking
-   Set tracking
-   Exercise metrics
-   AI coaching feedback
-   Workout history
-   Multiple supported exercises

## 🚧 Future Improvements

-   📈 Workout progress charts
-   📊 Advanced workout analytics
-   🏆 Fitness goals and achievements
-   🧠 Improved exercise/form classification
-   ➕ Additional exercises
-   👤 Personalized workout plans
-   📱 Improved mobile experience
-   🎯 More detailed form recommendations
-   💪 Personalized AI training programs
-   📅 Long-term workout progress tracking

## 📌 Project Status

**Status: Active / Working Prototype**

The core real-time workout coaching workflow is implemented and
deployed.

The project can be further improved with additional exercises,
analytics, personalization, and UI enhancements.

## 👨‍💻 Author

**Aniket Kharose**

GitHub:\
https://github.com/aniketkharose

Project:\
https://github.com/aniketkharose/ai-gym-coach-vision

Live Demo:\
https://ai-gym-coach-vision.streamlit.app/

## ⭐ Support

If you find the project useful or interesting, consider giving the
repository a ⭐ on GitHub.

## 📄 License

This project is available under the MIT License.

If you add a `LICENSE` file to the repository, keep the license text
consistent with the license declared here.
