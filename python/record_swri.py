#!/usr/bin/env python

import rospy
import csv
import os
from swri_profiler_msgs.msg import ProfileDataArray

csv_file_path = '/home/dev/lio_test_ws/src/lio_sam_gpu_test/python/profile_xavier.csv'

# Initialize the data storage
data_storage = {}

def update_csv():
    with open(csv_file_path, mode='w') as file:
        writer = csv.writer(file)
        # Write header
        header = ['key']
        max_columns = max(len(durations) for durations in data_storage.values())
        header.extend(['rel_total_duration_nsecs_{}'.format(i) for i in range(max_columns)])
        #writer.writerow(header)
        
        # Write rows
        for label, durations in data_storage.items():
            row = [label] + durations
            writer.writerow(row)

def callback(data_array):
    for data in data_array.data:
        if data.label not in data_storage:
            data_storage[data.label] = []
        data_storage[data.label].append(data.rel_total_duration.nsecs)
    update_csv()
    rospy.loginfo("Updated CSV for keys: %s", ", ".join(str(data.key) for data in data_array.data))

def listener():
    rospy.init_node('profiler_data_listener', anonymous=True)
    rospy.Subscriber('/profiler/data', ProfileDataArray, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()