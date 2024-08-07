import json
import csv
from collections import defaultdict

# Update the file paths as per your local environment
json_file_path = r"C:\Users\SAMSUNG\OneDrive\Documents\qafile\Fnd_perf2\performance_data.json"
csv_file_path = r"C:\Users\SAMSUNG\OneDrive\Documents\qafile\Fnd_perf2\average_performance_data.csv"

# Load the performance data from the JSON file
with open(json_file_path, 'r') as json_file:
    performance_data = json.load(json_file)

# Initialize a dictionary to store total durations and counts
durations = defaultdict(lambda: {'total_duration': 0, 'count': 0})

# Process each entry in the performance data
for entry in performance_data:
    if 'name' in entry and 'duration' in entry:
        name = entry['name']
        duration = entry['duration']
        durations[name]['total_duration'] += duration
        durations[name]['count'] += 1

# Calculate the average duration for each URL
average_durations = [
    {'name': name, 'average_duration': info['total_duration'] / info['count']}
    for name, info in durations.items()
]

# Write the average durations to a CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["name", "average_duration"])
    for entry in average_durations:
        csv_writer.writerow([entry['name'], entry['average_duration']])

print(f"Average performance data written to '{csv_file_path}'")
