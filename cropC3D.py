# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 23:33:53 2024

@author: Harald Penasso
"""

from ezc3d import c3d
import numpy as np
import sys

# Related posts:
# https://github.com/pyomeca/ezc3d/issues/321
# https://github.com/pyomeca/ezc3d/issues/221

def cropC3D(path, start_time, end_time):
    """
    Crop a C3D file to a specified time period.

    Parameters:
    path (str): Path to the C3D file.
    start_time (float): Start time in seconds for cropping.
    end_time (float): End time in seconds for cropping.

    Returns:
    Saves the cropped C3D file at the original patch as *_cropped.c3d
    """
    # Print the filename being processed
    print("... cropping: " + path)

    # Load the C3D file
    c3d_file = c3d(path)
    
    # Remove meta points
    del c3d_file["data"]["meta_points"]

    # Crop markers to the selected period
    point_rate = c3d_file['parameters']['POINT']['RATE']['value'][0]
    orig_first_frame = c3d_file["header"]["points"]["first_frame"]
    start_point_idx = int(np.floor(start_time * point_rate)) - orig_first_frame
    end_point_idx = int(np.ceil(end_time * point_rate)) - orig_first_frame + 1
    print(f"... ... keep data from {start_time} s to {end_time} s, becoming index {start_point_idx} to {end_point_idx}.")
    cropped_points_data = c3d_file["data"]["points"][:, :, start_point_idx:end_point_idx]
    
    # Update C3D file parameters and headers
    c3d_file['parameters']['POINT']['FRAMES']['value'] = np.array([cropped_points_data.shape[2]])
    c3d_file["header"]["points"]["first_frame"] = start_point_idx
    c3d_file["header"]["points"]["last_frame"] = end_point_idx
    c3d_file["data"]["points"] = cropped_points_data

    # Calculate analog data indices and crop analog data
    analog_rate = c3d_file['parameters']['ANALOG']['RATE']['value'][0]
    ratio = int(analog_rate / point_rate)
    start_analog_idx = start_point_idx * ratio
    end_analog_idx = end_point_idx * ratio
    analog_data = c3d_file["data"]["analogs"]
    cropped_analog_data = analog_data[:, :, start_analog_idx:end_analog_idx]

    # Update C3D file headers for analog data
    c3d_file['header']['analogs']['first_frame'] = start_analog_idx
    c3d_file['header']['analogs']['last_frame'] = end_analog_idx
    c3d_file["data"]["analogs"] = cropped_analog_data

    # Fix potential bug in ezc3d
    c3d_file["parameters"]["ANALOG"]["UNITS"]["value"] = []

    # Update trial start and end fields
    c3d_file['parameters']['TRIAL']['ACTUAL_START_FIELD']['value'][0] = start_point_idx + orig_first_frame + 2 # not sure if +2 is actually correct
    c3d_file['parameters']['TRIAL']['ACTUAL_END_FIELD']['value'][0] = end_point_idx + orig_first_frame + 1 # not sure if +1 is actually correct

    # Remove POINT.LABELS2 if POINT.LABELS has less than 255 labels
    if len(c3d_file["parameters"]["POINT"]["LABELS"]["value"]) < 255:
        del c3d_file["parameters"]["POINT"]["LABELS2"]

    # Save the patched C3D file with a new name
    output_path = path[0:-4] + '_cropped.c3d'
    c3d_file.write(output_path)

    # Final message
    print(f"... cropped C3D file saved to {output_path}")

if __name__ == "__main__":
    # Use the path, start_time, and end_time from the command line
    path, start_time, end_time = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    
    # For testing purposes, use the hardcoded path and times (comment-out the line above)
    # path = "C:\\Users\\User\\OneDrive - FH Campus Wien\\Documents\\GitHub\\cropC3D\\c3dfile.c3d"
    # start_time = 5.1
    # end_time = 6.2

    cropC3D(path, start_time, end_time)
