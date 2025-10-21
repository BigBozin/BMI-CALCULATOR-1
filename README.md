BMI Calculator GUI (Tkinter + Pillow)

A beautifully designed, animated BMI Calculator built with Python’s Tkinter library for the GUI and Pillow for image support. It allows users to input their height and weight, calculates their Body Mass Index (BMI), and visually displays the result with dynamic animation and a custom scale gauge.

Features

1. User-friendly and responsive GUI layout
2. Real-time BMI calculation with animated transitions
3. Interactive weight scale gauge
4. Dynamic category detection (Underweight, Normal, Overweight, Obese, etc.)
5. Health advice based on BMI range
6. Custom placeholder images if actual images are missing
7. Responsive resizing support

Technologies Used

1. Python 3
2. Tkinter – GUI toolkit
3. Pillow (PIL) – Image handling
4. Threading – For non-blocking animation
5. Canvas – For dynamic drawing of weight scale

📂 Project Structure
GROUP WORK/
│
├── images/
│   ├── bmiICON3.png
│   ├── bmiCAL.png
│   └── BMI Chart African Boy-D2.jpg
│
├── bmi@.py       # Main Python file
└── README.md               # This file

How to Run

1. Clone the repository or download the script:
git clone 
cd bmi-calculator-gui

2. Install dependencies (if not already installed):
pip install pillow

3. Run the app:
python bmi_calculator.py

Image Requirements

1. Place your custom images in the images/ directory with the following names:
2. bmiICON3.png – Icon/image shown in the center column
3. bmiCAL.png – Title/header image
4. BMI Chart African Boy-D2.jpg – BMI reference chart at the bottom
5. If these are missing, the app will use placeholder graphics automatically.

BMI Categories

1. Category	BMI Range
2. Underweight	< 18.5
3. Normal Weight	18.5 – 24.9
4. Overweight	25 – 29.9
5. Obese	30 – 34.9
6. Extremely Obese	35+

Animation Details

1. Animated scale needle that moves up to current weight.
2. Animated BMI value counter with percentage calculation feedback.
3. Smooth and responsive canvas drawing during window resize.
4. Validation & Error Handling
5. Height must be between 1.0 and 2.5 meters
6. Weight must be between 0 and 200 kg
7. Real-time error messages using tkinter.messagebox

To-Do / Ideas for Future

1. Add unit conversion (e.g., feet/inches, lbs)
2. Export BMI report as PDF
3. Add dark/light theme toggle
4. Save user history or session
5. Add voice feedback or accessibility features

Authors

Linus247 and BigBozin
GitHub: 1. https://github.com/Linus247/BMI-CALCULATOR.git
         
