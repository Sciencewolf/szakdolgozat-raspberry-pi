import os
import subprocess
from datetime import datetime
import signal
from flask import jsonify
import psutil
import time
import json


def log(reason: str = "", description: str = "", api_url: str = "", headers: str = "") -> None:
    """ Keep logging the event's into a file """

    today = datetime.now().strftime("%Y-%B-%d")

    log_directory = "/home/aron/szakdolgozat-raspberry-pi/log"
    log_file_path = f"{log_directory}/{today}-log-system.txt"

    os.makedirs(log_directory, exist_ok=True)

    with open(log_file_path, 'a+') as file:
        file.write("reason: " + reason + '\n')
        file.write("description: " + description + '\n')
        file.write("api_url: " + api_url + '\n')
        file.write("headers: " + headers + '\n')
        file.write("timestamp: " + datetime.now().__str__() + '\n')
        file.write("--------\n")


LED_PINS: dict = {
    "red": 17,
    "green": 27,
    "white": 22,
    
    "yellow": 6,
    "cold_white": 13,
    "blue": 19
}

RELAY_PINS: dict = {
    "cooler": 24,
    "heating_element": 23,
    "humidifier": 25, 
}

class Mode:
    """ Defines modes for led [blink or hold]  """

    blink = "blink"
    hold = "hold"

class LEDs:
    """ Defines led colors """

    red = "red"
    green = "green"
    white = "white"
    
    yellow = "yellow"
    cold_white = "cold_white"
    blue = "blue"


class Utils:
    """
        All actions inside csibekelteto will be implemented here.
        Call webserver endpoint to run certain action.
    """

    def __init__(self):
        self.base_dir: str = os.path.dirname(os.path.abspath(__file__))
        self.lid_file_path: str = os.path.join(self.base_dir, "lid_status.txt")
        self.processes: dict = {}
        self.led_panel: dict = {}
        self.hatching = False

    # __private methods

    def start_process(self, name: str, script: str="led.py", led: str="", mode: str="") -> None:
        """Start a subprocess in a new session and track it by name."""

        if datetime.now().hour not in range(8, 20, 1) and script == 'led.py':
            print('led is not running between 19:00 and 8:00(night)')
            return

        if name in self.processes and self.processes[name].poll() is None:
            print(f"Process {name} is already running with PID {self.processes[name].pid}.")
            return

        try:
            process = subprocess.Popen(
                [os.path.join(self.base_dir, f"hardware-code/{script}")] + [led, mode],
                start_new_session=True  # Start in a new session
            )
            self.processes[name] = process
            print(f"Process {name} started with PID {process.pid}.")
        except Exception as e:
            print(f"Failed to start process {name}: {e}")


    def stop_process(self, name: str) -> None:
        """Stop a running subprocess by name."""

        if name in self.processes:
            process = self.processes[name]
            if process.poll() is None:  # Process is still running
                try:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)  # Send SIGTERM to process group
                    process.wait()  # Wait for process to terminate
                    print(f"Process {name} stopped.")
                except Exception as e:
                    print(f"Error stopping process {name}: {e}")
            else:
                print(f"Process {name} has already stopped.")
            del self.processes[name]  # Remove from tracking
        else:
            print(f"{name} is not running.")


    def __update_config(self, updates: dict) -> None:
            with open('csibekelteto_config.json', 'r+') as file:
                data = json.load(file)
                data.update(updates)
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()


    def __str__(self) -> str:
        return (f"---Utils--- "
                f"\n\tHealth: {self.health()} "
                f"\n\tLast Emergency Shutdown: {self.last_emergency_shutdown()}"
                f"\n---Utils---")

    """ Utils method's """

    def get_temp_and_hum(self) -> dict:
        result = subprocess.run(
            [os.path.join(self.base_dir, "hardware-code/temp_hum_sensor.py")],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                "temp": -1,
                "hum": -1,
                "status_code": 404,
                "content": "not found response",
                "timestamp": timestamp
            }

        with open(os.path.join(self.base_dir, "temp_hum.txt"), 'r') as file:
            temp = file.readline().strip().split(' ')[0]
            hum = file.readline().strip().split(' ')[0]
            timestamp = file.readline().strip()

            return {
                "temp": temp,
                "hum": hum,
                "timestamp": timestamp
            }

    def get_day(self) -> int:
        try:
            with open("hatching_date.txt", 'r') as file:
                hatching_date_str = file.readline().strip()
            
            hatching_date = datetime.strptime(hatching_date_str, "%Y-%m-%d %H:%M:%S")
            return (datetime.now() - hatching_date).days
        except (FileNotFoundError, ValueError):
            log("Error", "Invalid or missing hatching_date.txt")
            return -1

    def is_temperature_normal(self, day: int, temp: float) -> bool:
        temp_data = {
            **dict.fromkeys(range(1, 4), 38.1),
            **dict.fromkeys(range(4, 11), 37.8),
            **dict.fromkeys(range(11, 18), 37.5),
            **dict.fromkeys(range(19, 22), 37.2),
        }

        if temp == -1:
            return True  # Turn off hardware

        value = temp_data.get(day, None)
        return value is not None and float(str(temp).split(' ')[0]) - 1.0 > value # -1.0C bc of hot heating element

    def is_humidity_normal(self, day: int, hum: float) -> bool:
        hum_data = {

            **dict.fromkeys(range(1, 19), [60.0, 70.0]),
            **dict.fromkeys(range(19, 22), [70.0, 80.0])
        }

        if hum == -1:
            return True # return True to turning off hw

        min_value, max_value = hum_data.get(day, [None, None]) # if day is not in hum_data -> None

        return min_value is not None and min_value - 1.0 <= hum <= max_value + 1.0 # +- 1.0 % 

    def is_rotate_eggs(self, day: int) -> bool:
        rotate_data: dict[int, bool] = {
            1: True,
            2: True,
            3: True,
            4: True,
            5: True,
            6: True,
            7: True,
            8: True,
            9: True,
            10: True,
            11: True,
            12: True,
            13: True,
            14: True,
            15: True,
            16: True,
            17: True,
            18: True,
            19: False,
            20: False,
            21: False
        }

        value: bool | None = rotate_data.get(day, None)

        return value is not None and value

    def is_lid_closed(self) -> bool:
        status: str = self.lid_status().get('lid')
        
        return status == 'Close'
    
    def is_hatching(self) -> bool:
        return self.hatching

    def prepare_hatching(self) -> None:
        """
        Prepare the incubator for hatching by ensuring proper temperature and humidity.
        """
        while True:
            current_temp = float(self.get_temp_and_hum().get('temp', -1))
            current_hum = float(self.get_temp_and_hum().get('hum', -1))
            current_day = self.get_day()
            config = self.get_config()
            target_temp = float(config.get('manual_temp', self.get_target_temp(current_day)))
            target_hum = float(config.get('manual_hum', self.get_target_hum(current_day)))

            if not self.is_lid_closed():
                self.off_heating_element()
                self.off_cooler()
                self.off_humidifier()
                self.__update_config({'alertOnLidOpen': 1, 'app_alertOnLidOpen': 1})
                log("Lid Open", "Hatching preparation stopped due to lid being open.")
                break

            if current_temp >= target_temp:
                self.off_heating_element()
                self.off_cooler()
            else:
                self.on_heating_element()
                self.on_cooler()

            if current_hum >= target_hum:
                self.off_humidifier()
            else:
                self.on_humidifier()

            log("Hatching Prep", f"Temp: {current_temp}, Humidity: {current_hum}, Target Temp: {target_temp}, Target Hum: {target_hum}")
            time.sleep(10)

    def start_hatching(self) -> None:
        """
        Start the hatching process by setting the hatching date and preparing the incubator.
        """
        with open("hatching_date.txt", 'w') as file:
            file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        log("Hatching Started", "Eggs are now in the hatching phase.")

        self.hatching = True
        
        while True:
            self.prepare_hatching()
            self.rotate_eggs()
            time.sleep(14400)  # Rotate eggs every 4 hours
        
    def stop_hatching(self) -> None:
        """
        Stop all incubation processes.
        """
        self.off_heating_element()
        self.off_cooler()
        self.off_humidifier()

        self.hatching = False
        
        log("Hatching Stopped", "All hatching-related processes have been turned off.")

    def set_temp(self, temp: float) -> None:
        """
        Manually set the incubator temperature and update hatching target values.
        """
        self.off_heating_element()
        self.on_heating_element()

        while True:
            current_temp = float(self.get_temp_and_hum().get('temp', -1))
            if current_temp >= temp:
                self.off_heating_element()
                break
            time.sleep(10)
        
        self.__update_config({'manual_temp': temp})
        log("Manual Temp Set", f"Temperature set to {temp}C")

    def set_hum(self, hum: float) -> None:
        """
        Manually set the incubator humidity and update hatching target values.
        """
        self.off_humidifier()
        self.on_humidifier()

        while True:
            current_hum = float(self.get_temp_and_hum().get('hum', -1))
            if current_hum >= hum:
                self.off_humidifier()
                break
            time.sleep(10)
        
        self.__update_config({'manual_hum': hum})
        log("Manual Humidity Set", f"Humidity set to {hum}%")

    def get_config(self) -> dict:
        """ Retrieve the current configuration. """
        try:
            with open('csibekelteto_config.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def get_target_temp(self, day: int) -> float:
        """ Retrieve the recommended temperature for the given day. """
        temp_data = {
            **dict.fromkeys(range(1, 4), 38.1),
            **dict.fromkeys(range(4, 11), 37.8),
            **dict.fromkeys(range(11, 18), 37.5),
            **dict.fromkeys(range(19, 22), 37.2),
        }
        return temp_data.get(day, 37.5)

    def get_target_hum(self, day: int) -> float:
        """ Retrieve the recommended humidity for the given day. """
        hum_data = {
            **dict.fromkeys(range(1, 19), 65.0),
            **dict.fromkeys(range(19, 22), 75.0)
        }
        return hum_data.get(day, 65.0)

    """ Lid """

    def lid_status(self) -> dict:
        result = subprocess.run(
            [os.path.join(self.base_dir, "hardware-code/switch.py")],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            log(
                reason="error at switch",
                description=result.stderr
            )

            return jsonify({
                "status_code": 404,
                "content": "error at lid",
                "timestamp": datetime.now().__str__()
            })

        if not os.path.exists(self.lid_file_path):
            log(description="lid status file does not exists")

            return jsonify({
                "status_code": 404,
                "timestamp": datetime.now().__str__()
            })

        with open(self.lid_file_path, 'r') as file:
            log(description="access lid status file")

            lines = file.readlines()
            for line in lines:
                if line.startswith("!"):
                    status: str = line.split(" ")[1]

                    return {
                        "status_code": 200,
                        "lid": status,
                        "timestamp": datetime.now().__str__()
                    }

    """ Cooler """

    def on_cooler(self) -> None:
        self.start_process(name="cooler", script="cooler.py")
        self.on_cold_white_led()

    def off_cooler(self) -> None:
        self.stop_process(name="cooler")
        self.off_cold_white_led()

    """ Heating element """

    def on_heating_element(self) -> None:
        self.start_process(name="heating_element", script="heating_element.py")
        self.on_green_led()

    def off_heating_element(self) -> None:
        self.stop_process("heating_element")
        self.off_green_led()

    """ Engine """

    def on_engine_forward(self) -> None:
        self.start_process(name="engine_forward", script="engine_forward.py")
        self.on_yellow_led()

    def off_engine_forward(self) -> None:
        self.stop_process("engine_forward")
        self.off_yellow_led()

    def on_engine_backward(self) -> None:
        self.start_process(name="engine_backward", script="engine_backward.py")
        self.on_yellow_led()

    def off_engine_backward(self) -> None:
        self.stop_process("engine_backward")
        self.off_yellow_led()

    def rotate_eggs(self) -> None:
        with open('last_egg_rotation.txt', 'w') as file:
            file.write(datetime.now().__str__())

        for _ in range(3):
            self.on_engine_forward()
            time.sleep(2)
            self.off_engine_forward()
            time.sleep(2)
            self.on_engine_backward()
            time.sleep(2)
            self.off_engine_backward()
            time.sleep(5)

    def get_last_eggs_rotation(self) -> None:
        with open('last_egg_rotation.txt', 'r') as file:
            return file.readlines()

    """ Humidifier """

    def on_humidifier(self) -> None:
        # self.start_process(name="humidifier", script="humidifier.py")
        self.on_blue_led()

    def off_humidifier(self) -> None:
        # self.stop_process("humidifier")
        self.off_blue_led()

    """ LED """

    def on_red_led(self, mode: str=Mode.hold) -> None:
        self.start_process(
            name="red_led",
            led=LEDs.red,
            mode=mode
        )

    def off_red_led(self) -> None:
        self.stop_process("red_led")

    def on_green_led(self, mode: str=Mode.hold) -> None:
        self.start_process(
            name="green_led",
            led=LEDs.green,
            mode=mode
        )

    def off_green_led(self) -> None:
        self.stop_process("green_led")

    def on_white_led(self, mode: str=Mode.hold) -> None:
        self.start_process(
            name="white_led",
            led=LEDs.white,
            mode=mode
        )

    def off_white_led(self) -> None:
        self.stop_process("white_led")

    def on_yellow_led(self, mode: str=Mode.hold) -> None:
        self.start_process(
            name="yellow_led",
            led=LEDs.yellow,
            mode=mode
        )

    def off_yellow_led(self) -> None:
        self.stop_process("yellow_led")

    def on_cold_white_led(self, mode: str=Mode.hold) -> None:
        self.start_process(
            name="cold_white_led",
            led=LEDs.cold_white,
            mode=mode
        )

    def off_cold_white_led(self) -> None:
        self.stop_process("cold_white_led")

    def on_blue_led(self, mode: str=Mode.hold) -> None:
        self.start_process(
            name="blue_led",
            led=LEDs.blue,
            mode=mode
        )

    def off_blue_led(self) -> None:
        self.stop_process("blue_led")


    """ Other """

    def shutdown(self) -> None:
        shutdown_command = "sudo shutdown -h now"
        os.system(shutdown_command)

    def health(self) -> list:
        cpu = psutil.cpu_percent()
        all_memory = psutil.virtual_memory()
        process = psutil.Process(os.getpid())
        app_mem_usage = process.memory_info().rss / 1024 ** 2
        app_vmem_usage = process.memory_info().vms / 1024 ** 2


        return [
            ["cpu", cpu],
            ["all memory %", all_memory.percent],
            ["memory by app rss", app_mem_usage],
            ["memory by app vms", app_vmem_usage]
        ]
