#!/usr/bin/env python3


from datetime import datetime
import json


def main():
    today = datetime.now().strftime('%Y-%m-%d')

    input_filename = "/home/aron/szakdolgozat-raspberry-pi/stats/statistics.json"
    output_filename = f"/home/aron/szakdolgozat-raspberry-pi/stats/filtered_statistics_{today}.json"

    filtered_data = []

    with open(input_filename, 'r') as file:
        for index, line in enumerate(file):
            try:
                obj = json.loads(line.strip())
                
                if str(obj['timestamp']).split(' ')[0] == str(today) and index % 3 == 0 and 'lid' not in obj['data']:
                    filtered_data.append(obj)
                    
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line {index + 1}: {line}")

    with open(output_filename, 'w') as filtered_statistics:
        json.dump(filtered_data, filtered_statistics, indent=4)


if __name__ == "__main__":
    import time

    while True:
        now = datetime.now().strftime("%H:%M")

        if now == "23:59":
            main()

        time.sleep(30)