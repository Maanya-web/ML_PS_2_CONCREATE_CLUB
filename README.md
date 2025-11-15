Drone-Based Multi-Vehicle Detection and Traffic Analysis



This project is a computer vision system designed to detect, track, and analyze the flow of traffic at a four-way intersection using drone footage. The system identifies different vehicles, tracks their trajectories, and classifies their direction (Straight, Right Turn, U-Turn) to generate a traffic flow report.

Core Components
**Object Detection: A YOLOv8 model fine-tuned on the JATAYU dataset for Indian road conditions.

**Object Tracking: DeepSORT (deep_sort_realtime) to track detected vehicles and assign unique IDs.

**Analysis Engine: A custom Python script (analyze_trajectories.py) that uses Region of Interest (ROI) zones to classify vehicle journeys.



How to Run


This project is split into two main parts: Tracking (which generates trajectory data) and Analysis (which processes that data).

Prerequisites:

Python 3.8+

A video file of the intersection.

Required libraries:

pip install ultralytics opencv-python-headless deep-sort-realtime pandas openpyxl



Step 1: Run Tracking

Place your test video in the main folder and update the video path inside 'tracking_deepsort.py.' Then, run the script:

This will run the detection and tracking on every frame of the video. It will produce two files:

***tracked_output.mp4: A video file showing the tracking boxes.

***trajectories.pkl: A data file containing the path for every unique vehicle ID.


Step 2: Run Analysis

Once the tracking is complete, run the analysis script to process the trajectories.pkl file:


python analyze_trajectories.py

This script will load the trajectory data, apply the zone logic from lanes.py, and generate the final report.

Output:

traffic_analysis_report2.xlsx: An Excel file with the final counts of vehicles per lane and direction.
