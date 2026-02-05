# GestureDJ
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv&logoColor=white" />
  <img src="https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/pygame-Audio%20Engine-purple?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Author-Sarthak%20Bhopale-gray?style=for-the-badge&logo=github&logoColor=white" />
  <img src="https://img.shields.io/badge/Role-Aspiring%20AI%20%26%20Computer%20Vision%20Developer-darkblue?style=for-the-badge" />
</p>

<p align="center">
  <b>Gesture-controlled DJ mixing using computer vision and real-time audio processing</b>
</p>

> **Author:** Sarthak Bhopale  
> **Domain:** Computer Vision · Human–Computer Interaction · Audio Processing  
> **Project Type:** Portfolio Project


## 1. Project Overview

GestureDJ is a contactless, gesture‑controlled audio mixing application developed in Python. It leverages computer vision techniques to track hand movements in real time and maps spatial coordinates and hand configurations to DJ style mixing controls.

Using a standard webcam, the system detects hand landmarks, computes geometric relationships between key points, and converts these measurements into continuous audio control signals. This enables hands free control of volume, crossfading, and digital signal processing (DSP) effects without the need for physical DJ hardware or keyboard interaction.

---

## 2. Key Features

### UI & Interaction Components

* **DJ‑Style Crossfader Bar**
  A horizontal animated slider rendered on the webcam feed that visually represents the real‑time mix ratio between Track A and Track B.

* **Dynamic Volume Meter**
  A vertical volume bar that smoothly responds to pinch gesture input, providing immediate visual feedback of master volume levels.

* **Effect Status Indicators**
  On‑screen labels and highlights indicate when effects such as *Scratch*, *Echo*, or *Filter* are active.

* **Hand Skeleton Overlay**
  MediaPipe landmark connections are drawn in real time, allowing users to visually understand gesture recognition accuracy.

* **Minimal, High‑Contrast UI Design**
  The interface is intentionally clean and readable, ensuring visibility under different lighting conditions without distracting from gesture control.

---

## 2. Key Features

<p align="left">
  <img src="https://img.shields.io/badge/Real--Time-Processing-black?style=flat-square" />
  <img src="https://img.shields.io/badge/Hands--Free-Control-black?style=flat-square" />
  <img src="https://img.shields.io/badge/Computer--Vision-black?style=flat-square" />
  <img src="https://img.shields.io/badge/Digital--Audio-black?style=flat-square" />
</p>

* **Real‑time Hand Tracking**
  Uses MediaPipe Hands to detect and track up to two hands simultaneously with low latency.

* **Dual‑Track Audio Mixing**
  Supports synchronized playback and live mixing of two independent audio tracks.

* **Smooth Crossfading**
  Implements linear interpolation combined with signal smoothing for stable, click‑free transitions.

* **Gesture‑Driven Audio Effects**
  Recognizes complex gestures such as fist clenching and circular hand motion to trigger DJ effects.

* **Interactive Visual UI Overlay**
  Displays hand skeletons, animated sliders, volume meters, crossfader bars, and active effect indicators directly on the webcam feed.

* **Signal Stabilization**
  Applies Exponential Moving Average (EMA) filtering to reduce jitter in raw landmark data and ensure precise audio control.

---

## 3. Gesture Mapping Table

| Hand    | Gesture / Movement                 | Control Function                               |
| ------- | ---------------------------------- | ---------------------------------------------- |
| Right   | Horizontal movement (Left ↔ Right) | Crossfader between Track A and Track B         |
| Right   | Thumb–Index finger distance        | Master volume control                          |
| Left    | Vertical movement (Up ↔ Down)      | Audio filter (low‑pass / high‑pass simulation) |
| Left    | Open palm                          | Play / Pause playback                          |
| Left    | Closed fist                        | Bass boost / beat‑drop effect                  |
| Left    | Circular motion                    | Vinyl scratch simulation                       |
| General | Swipe left / swipe right           | Previous / next track                          |

---

## 4. System Architecture

GestureDJ follows a real time processing pipeline composed of three primary layers:

### Input & Perception Layer

* **Video Capture**: OpenCV captures frames from the system webcam.
* **Landmark Detection**: MediaPipe identifies 21 hand landmarks per detected hand.
* **Normalization**: Landmark coordinates are normalized relative to frame dimensions.

### Logic & Control Layer

* **Gesture Recognition**: Euclidean distances, motion variance, and trajectory history are analyzed to detect gestures such as pinches, fists, and circular motion.
* **Signal Processing**: EMA filters smooth raw input values to eliminate jitter.
* **State Management**: Maintains audio states (volume, crossfader position, active effects) and enforces cooldown timers to prevent accidental retriggers.

### Output & Rendering Layer

* **Audio Engine**: pygame.mixer updates channel volumes and effect states in real time.
* **UI Overlay**: OpenCV renders an animated DJ‑style interface including crossfader bars, volume meters, effect indicators, and hand skeletons.

---

## 5. Project Directory Structure

```
GestureDJ/
│
├── songs/
│   ├── track_a.mp3         # Primary audio track
│   └── track_b.mp3         # Secondary audio track
│
├── effects/
│   ├── scratch.py          # Scratch simulation logic
│   ├── echo.py             # Echo / reverb effects
│   └── filters.py          # High‑pass / low‑pass filter logic
│
├── gestures/
│   ├── hand_tracker.py     # MediaPipe initialization and hand tracking
│   ├── gesture_logic.py    # Gesture recognition and state mapping
│
├── ui/
│   ├── overlay.py          # OpenCV‑based UI rendering components
│
├── main.py                 # Application entry point and main loop
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 6. Installation & Environment Setup

### Prerequisites

* **Python**: Version 3.10 (recommended for MediaPipe stability)
* **Webcam**: Any functional USB or built‑in webcam
* **Operating System**: Windows, macOS, or Linux

### Setup Instructions

1. **Clone or download the repository**

2. **Create a virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Add audio files**
   Place two MP3 files inside the `songs/` directory and name them:

* `track_a.mp3`
* `track_b.mp3`

---

## 7. How to Run the Project

From the project root directory, run:

```bash
python main.py
```

After launch, a window titled **GestureDJ** will display the live webcam feed with the DJ UI overlay. Initial startup may take a few seconds while audio and hand‑tracking modules initialize.

To exit the application, press **Q** while the window is in focus.

---

## 8. Controls & Gesture Details

### Visual UI Components (On‑Screen)

* **Animated Crossfader Slider** – Moves fluidly based on right‑hand X‑axis position
* **Live Volume Bar** – Scales smoothly with pinch distance
* **Effect Toggles** – Text and color cues for Scratch, Echo, and Filter states
* **Hand Landmark Visualization** – Real‑time skeletal tracking for transparency and debugging

---

### Crossfader (Right Hand – X Axis)

<p align="center">
  <img src="https://img.shields.io/badge/UI-Animated%20Crossfader-blueviolet?style=flat-square" />
  <img src="https://img.shields.io/badge/UI-Volume%20Meter-blueviolet?style=flat-square" />
  <img src="https://img.shields.io/badge/UI-Effect%20Indicators-blueviolet?style=flat-square" />
  <img src="https://img.shields.io/badge/UI-Hand%20Skeleton%20Overlay-blueviolet?style=flat-square" />
</p>

### Crossfader (Right Hand – X Axis)

* Leftmost position: 100% Track A
* Rightmost position: 100% Track B
* Center: Equal mix

### Volume Control (Right Hand Pinch)

* Fingers touching: Mute
* Fingers apart: Maximum volume

### Filters (Left Hand – Y Axis)

* Higher position: Treble emphasis
* Lower position: Bass emphasis

### Visual UI Components

* Animated crossfader bar
* Dynamic volume meter
* Active effect indicators (Scratch / Echo / Filter)
* Real‑time hand skeleton overlay

---

## 9. Known Limitations

* **Lighting Sensitivity**: Hand tracking accuracy decreases in low‑light or high‑contrast environments.
* **Audio Latency**: Minor latency exists due to buffering requirements in Python audio playback.
* **Occlusion**: Overlapping or hidden hands may temporarily disrupt gesture detection.

---

## 10. Future Enhancements

* MIDI output support for integration with professional DAWs
* FFT‑based equalizer for real‑time frequency manipulation
* User‑configurable gesture mappings via JSON or YAML
* Recording and exporting mixed output as an audio file

---

## 11. License

this Project is Open sourced and can be used anywhere

