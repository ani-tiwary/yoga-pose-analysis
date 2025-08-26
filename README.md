# 🧘‍♀️ Yoga Pose Analysis

A modern, real-time yoga pose analysis application that provides instant feedback on your form using computer vision and AI.

## ✨ Features

- **Real-time Pose Analysis**: Get instant feedback on Warrior II, Tree Pose, and Triangle Pose
- **Clean Video Feed**: Distraction-free camera view with pose landmarks
- **Large, Color-coded Feedback**: Easy-to-read feedback that's visible from a distance
- **Modern UI**: Beautiful gradient design with glass-morphism effects
- **Responsive Design**: Works on desktop and tablet devices
- **Visual Status Indicators**: Color-coded status showing pose accuracy

## 🎯 Key Improvements

### Feedback System
- ✅ **Moved feedback out of video feed** - No more messy text overlays
- ✅ **Large, readable text** - Perfect for users standing far from the computer
- ✅ **Color-coded feedback** - Green for good form, red for corrections needed
- ✅ **Real-time updates** - Feedback refreshes every second

### User Experience
- ✅ **Modern, intuitive interface** - Clean design with smooth animations
- ✅ **Clear pose instructions** - Detailed step-by-step guidance
- ✅ **Visual status indicators** - Pulsing dots show pose status
- ✅ **Responsive layout** - Works on different screen sizes

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Webcam
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd yoga-pose-analysis
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv yoga_env
   ```

3. **Activate the virtual environment**
   - Windows: `yoga_env\Scripts\activate`
   - macOS/Linux: `source yoga_env/bin/activate`

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 📱 How to Use

1. **Select a Pose**: Click on Warrior II, Tree Pose, or Triangle Pose
2. **Position Yourself**: Stand 6-8 feet from your computer for best results
3. **Follow Instructions**: Read the detailed pose instructions
4. **Get Feedback**: Watch the real-time feedback panel for guidance
5. **Perfect Your Form**: Adjust your pose based on the color-coded feedback

## 🎨 UI Features

### Color Coding
- 🟢 **Green**: Perfect form - keep it up!
- 🔴 **Red**: Corrections needed - follow the specific tips
- 🟡 **Yellow**: Analyzing pose - stand still

### Visual Elements
- **Glass-morphism cards**: Modern, translucent interface elements
- **Smooth animations**: Hover effects and transitions
- **Status indicators**: Pulsing dots show real-time status
- **Large typography**: Easy to read from a distance

## 🔧 Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Computer Vision**: MediaPipe Pose Detection
- **Real-time Processing**: WebSocket-like polling for instant feedback

## 🎯 Supported Poses

### Warrior II (Virabhadrasana II)
- Front knee at 90 degrees
- Back leg straight
- Hips facing side
- Arms parallel to ground

### Tree Pose (Vrksasana)
- Standing leg straight
- Raised foot on inner thigh
- Hips level
- Hands above head

### Triangle Pose (Trikonasana)
- Wide stance (3-4 feet)
- Straight legs
- Torso tilted to side
- Arms in vertical line

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.