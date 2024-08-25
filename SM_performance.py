import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def get_performance_data(driver):
    performance_data = driver.execute_script("return window.performance.getEntries();")
    return performance_data

def write_to_json(file_path, data):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def write_to_csv(file_path, data):
    with open(file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["name", "average_duration"])
        for entry in data:
            csv_writer.writerow([entry['name'], entry['duration']])

def measure_performance(url, iterations=10):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--no-sandbox")  # Bypass OS security model

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    aggregated_data = []

    for i in range(iterations):
        driver.get(url)
        time.sleep(5)  # wait for the page to fully load
        performance_data = get_performance_data(driver)
        aggregated_data.extend(performance_data)
        print(f"Iteration {i + 1} completed")

    driver.quit()
    return aggregated_data

def calculate_average_performance(data):
    sums = {}
    counts = {}
    results = []

    # Sums up all metrics and count entries for averaging
    for entry in data:
        if 'name' in entry and 'duration' in entry:
            name = entry['name']
            duration = entry['duration']
            if name in sums:
                sums[name] += duration
                counts[name] += 1
            else:
                sums[name] = duration
                counts[name] = 1

    # Calculates average duration for each entry
    for name in sums:
        average_duration = sums[name] / counts[name]
        results.append({'name': name, 'duration': average_duration})

    return results

# Main execution
url = 'https://en.wikipedia.org/wiki/Software_metric'
iterations = 10
performance_data = measure_performance(url, iterations)
write_to_json('performance_metrics.json', performance_data)

average_performance_data = calculate_average_performance(performance_data)
write_to_csv('performance_metrics.csv', average_performance_data)

print("Performance data collection and processing completed.")
