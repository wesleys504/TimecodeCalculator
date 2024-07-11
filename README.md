Timecode Calculator/Converter
The Timecode Calculator/Converter is a Python script designed to help you calculate and convert timecodes for feature films and TV shows. It handles both drop frame and non-drop frame timecodes and provides a user-friendly interface to input the required data.

Features
- Converts timecodes to frames and vice versa.
- Supports both drop frame and non-drop frame formats.
- Calculates total run time (TRT) for TV shows with multiple acts.
- Determines if the current timecode is over or under the target duration.

Requirements
- Python 3.x

Usage
Running the Script
To run the script, simply execute it in your Python environment:
python timecode_calculator.py


Script Prompts

1. Type of Content:

- The script will ask if the content is a "Feature Film" or a "TV Show".

2. For Feature Films:

- Enter the current frame rate (e.g., 24, 25, 30).
- Specify if the current timecode is drop frame or non-drop frame.
- Enter the current sequence timecode (HH:MM:SS or MM:SS).

3. For TV Shows:

- Enter the number of acts.
- Enter the current frame rate (e.g., 24, 25, 30).
- Specify if the current timecode is drop frame or non-drop frame.
- Enter the timecode for each act (HH:MM:SS or MM:SS).
- The script will calculate and print the Total Run Time (TRT) of all acts.

4. Delivery Specifications:

- Enter the delivery frame rate (e.g., 24, 25, 30).
- Specify if the delivery timecode is drop frame or non-drop frame.
- Enter the target duration timecode (HH:MM:SS or MM:SS).

Output
The script will calculate whether the current timecode is over or under the target duration and display the result.


Contributing
If you find any issues or have suggestions for improvements, feel free to submit an issue or a pull request.

License
This project is licensed under the MIT License.

