#!/usr/bin/env python3


import datetime
import json

def main():
    input_filename = "/home/aron/szakdolgozat-raspberry-pi/stats/statistics.json"
    output_filename = f"/home/aron/szakdolgozat-raspberry-pi/stats/filtered_statistics_{datetime.datetime.now().strftime('%Y-%m-%d')}.json"

    filtered_data = []

    with open(input_filename, 'r') as file:
        for index, line in enumerate(file):
            try:
                obj = json.loads(line.strip())
                if index % 3 == 0 and not any(key in obj for key in ["Close", "Open"]):
                    filtered_data.append(obj)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line {index + 1}: {line}")

    with open(output_filename, 'w') as filtered_statistics:
        json.dump(filtered_data, filtered_statistics, indent=4)

if __name__ == "__main__":
    main()
