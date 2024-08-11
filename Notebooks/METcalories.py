# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 15:25:02 2024

@author: gregm
"""

# METs Calories Calculator
# https://media.hypersites.com/clients/1235/filemanager/MHC/METs.pdf
# Calories = (MET level of activity * 3.5 * Weight(kg) x minutes of activity) / 200

# Results showed that the gross energy cost of stair climbing is 8.6 METs,
# and that of stair descending is 2.9 METs. Thus, for a 70-kg person the
# Bicycling, <10mph, general, leisure, to work/for pleasure	4.0
# Bicycling, 10-12 mph, leisure, slow, light effort	6.0
# Bicycling, 12-14 mph, leisure, moderate effort	8.0
# Bicycling, 14-16 mph, racing or leisure, fast, vigorous effort	10.0
import pandas as pd

def calories(start_time_str, end_time_str, weight_kg, activitylab):
    # Input start time, end time, weight, and activity
    # Return calories burned
    from datetime import datetime
    # MET Levels (Metabolic EquivalenT) estimated for HARTH dataset activities
    activity_MET = {
        1: 2.5,  # Walking
        2: 10,   # Running
        3: 2.9,  # Shuffling
        4: 8.6,  # Stairs (Ascending)
        5: 2.9,  # Stairs (Descending)
        6: 2.5,  # Standing
        7: 1,    # Sitting
        8: 1,    # Lying
        13: 8,   # Cycling (Sit)
        14: 10,  # Cycling (Stand)
        130: 4,  # Cycling (Sit, Inactive)
        140: 6,  # Cycling (Stand, Inactive)
    }
    
    # Truncate start time to milliseconds
    parts = start_time_str.split('.')
    if len(parts[1]) > 3:
        # Keep only the first 3 digits of the decimal
        start_time_str = f"{parts[0]}.{parts[1][:3]}"
    # Truncate end time to milliseconds
    parts = end_time_str.split('.')
    if len(parts[1]) > 3:
        # Keep only the first 3 digits of the decimal
        end_time_str = f"{parts[0]}.{parts[1][:3]}"
    # Set time format
    time_form = "%Y-%m-%d %H:%M:%S.%f"
    # Extract start time
    start = datetime.strptime(start_time_str, time_form)
    # Extract end time of activity
    end = datetime.strptime(end_time_str, time_form)
    # Subtract end time from start time
    duration = end - start
    # Convert seconds to minutes for MET calculations
    duration_minutes = duration.total_seconds() / 60
    # MET value for activity
    MET = activity_MET[activitylab]
    # calories = (MET level of activity * 3.5 * Weight(kg) x minutes of activity) / 200
    calories_burned = (MET * 3.5 * weight_kg * duration_minutes) / 200
    return calories_burned

############################################
# # Example to process sensor data from one file and generate MET Total Calories
# sensor_data = pd.read_csv('S021.csv')
# # extract the annotated activity using the label numbers
# act_label = sensor_data['label']
# # extract the timestamp data
# timestamp = sensor_data['timestamp']
# # Assume 70kg weight for application
# weight = 70
# # Initialize variables
# total_cals = 0
# start_time = timestamp[0]
# end_time = timestamp[0]
# activity = act_label[0]
# for i in range(len(timestamp)):
#     # if activity label changes then find the calories for activity
#     if (activity != act_label[i]):
#         # Add to MET Total Calories
#         total_cals = total_cals + calories(start_time, end_time, weight, activity)
#         # Reset for next activity in sensor data
#         activity = act_label[i]
#         start_time = timestamp[i]
#         end_time = timestamp[i]
#     else:
#         # Set end time to next value
#         end_time = timestamp[i]

# print('\nTotal MET Calories: %5.2f' % total_cals)
