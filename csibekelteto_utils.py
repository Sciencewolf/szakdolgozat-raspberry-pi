import os
import subprocess
from datetime import datetime
import signal
import threading
from flask import jsonify
import psutil
import time
from datetime import datetime, timedelta
import json


def log(reason: str = "", description: str = "", api_url: str = "", headers: str = "") -> None:
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

def stats(info: dict) -> None:
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {"timestamp": today, "data": info}
    
    stats_file = '/home/aron/szakdolgozat-raspberry-pi/stats/statistics.json'
    
    with open(stats_file, 'a+') as file:
        json.dump(log_entry, file)
        file.write('\n')


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
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.lid_file_path = os.path.join(self.base_dir, "lid_status.txt")
        self.hatching_date_file = "/home/aron/szakdolgozat-raspberry-pi/hatching_date.txt"
        self.last_rotation_file = "/home/aron/szakdolgozat-raspberry-pi/last_egg_rotation.txt"
        self.hatching_status_file = "/home/aron/szakdolgozat-raspberry-pi/hatching_status.txt"

        self.processes = {}
        self.hatching = False
        self.heating_on = False
        self.humidifier_on = False
        self.cooler_on = False
        self.last_rotation = datetime.now()



    # __private methods

    def start_process(self, name: str, script: str="led.py", led: str="", mode: str="") -> None:
        """Start a subprocess in a new session and track it by name."""

        if datetime.now().hour not in range(8, 20, 1) and script == 'led.py':
            log(
                reason="LED off at night",
                description="LED is not working at night."
            )
            return

        if name in self.processes and self.processes[name].poll() is None:
            log(
                reason="process is running",
                description=f"Process {name} is already running with PID {self.processes[name].pid}."
                )
            return

        try:
            process = subprocess.Popen(
                [os.path.join(self.base_dir, f"hardware-code/{script}")] + [led, mode],
                start_new_session=True  # Start in a new session
            )
            self.processes[name] = process
            log(
                reason="process started",
                description=f"Process {name} started with PID {process.pid}."
            )
        except Exception as e:
            log(
                reason="process error",
                description=f"Failed to start process {name}: {e}"
            )


    def stop_process(self, name: str) -> None:
        """Stop a running subprocess by name."""

        if name in self.processes:
            process = self.processes[name]
            if process.poll() is None:  # Process is still running
                try:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)  # Send SIGTERM to process group
                    process.wait()  # Wait for process to terminate
                    log(
                        reason="process stopped",
                        description=f"Process {name} stopped."
                    )
                except Exception as e:
                    log(
                    reason="stop process error", 
                    description=f"Error stopping process {name}: {e}"
                    )
            else:
                log(
                    reason="process is stopped previously",
                    description=f"Process {name} has already stopped."
                )
            del self.processes[name]  # Remove from tracking
        else:
            log(
                reason="process does not exists",
                description=f"{name} is not running."
            )


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
        """ Get current temperature and humidity from sensor. """
        result = subprocess.run(
            [os.path.join(self.base_dir, "hardware-code/temp_hum_sensor.py")],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {"temp": "-1", "hum": "-1"}

        try:
            with open(os.path.join(self.base_dir, "temp_hum.txt"), 'r') as file:
                temp = file.readline().strip().split(' ')[0]
                hum = file.readline().strip().split(' ')[0]
        except FileNotFoundError:
            return {"temp": "-1", "hum": "-1"}

        stats({"temp": temp, "hum": hum})
        return {"temp": float(temp), "hum": float(hum)}


    def get_day(self) -> int:
        try:
            with open("hatching_date.txt", 'r') as file:
                hatching_date_str = file.readline().strip()
            
            hatching_date = datetime.strptime(hatching_date_str, "%Y-%m-%d %H:%M:%S")
            return (datetime.now() - hatching_date).days + 1
        except (FileNotFoundError, ValueError):
            log("Error", "Invalid or missing hatching_date.txt")
            return -1

    def is_temperature_normal(self, day: int, temp: float) -> bool:
        """Ensures temperature stays within ±0.5°C."""
        target_temp = self.get_target_temp(day)
        return target_temp - 0.5 <= temp <= target_temp + 0.5

    def is_humidity_normal(self, day: int, hum: float) -> bool:
        """Ensures humidity stays within ±1%."""
        min_hum, max_hum = self.get_target_hum(day)
        return min_hum - 1.0 <= hum <= max_hum + 1.0

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

    def start_hatching(self) -> None:
        if self.hatching:
            log("Hatching Already Running", "Process already active.")
            return

        log("Hatching Start", "Launching hatching process in background.")
        self.hatching = True 

        hatching_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.hatching_date_file, 'w') as file:
            file.write(hatching_start_time)

        thread = threading.Thread(target=self.prepare_hatching, daemon=True)
        thread.start()

        time.sleep(2)
        if not thread.is_alive():
            log("Thread Failed", "Hatching thread did not start properly.")
        else:
            log("Thread Running", "Hatching process started successfully.")


    def prepare_hatching(self) -> None:
        log("Hatching Started", "Entering hatching loop.")

        try:
            with open(self.hatching_status_file, 'w') as file:
                file.write("1")
        except Exception as e:
            log("error at hatching status file writing")
            
        self.on_heating_element()
        self.on_cooler()
        self.cooler_on = True
        self.heating_on = True
        self.humidifier_on = False 
        last_humidifier_time = 0  
        log("Prepare Hatching", "Heating and Cooler turned ON at the start.")

        while self.hatching:
            if not self.is_lid_closed():
                log("Lid Open", "Stopping all operations until lid is closed.")
                self.off_heating_element()
                self.off_humidifier()
                time.sleep(5)
                continue 

            log("Lid Closed", "Resuming hatching process.")

            temp_data = self.get_temp_and_hum()
            current_day = self.get_day()

            if temp_data["temp"] == -1 or temp_data["hum"] == -1:
                log("Sensor Error", "Invalid sensor readings, retrying in 10s.")
                time.sleep(10)
                continue 

            current_temp = temp_data["temp"]
            current_hum = temp_data["hum"]
            target_temp = self.get_target_temp(current_day)

            hum_range = self.get_target_hum(current_day)
            if not isinstance(hum_range, tuple) or len(hum_range) != 2:
                log("Humidity Error", f"Unexpected humidity format: {hum_range}")
                hum_range = (60.0, 70.0)

            min_hum, max_hum = hum_range

            log("Temp Check", f"Current: {current_temp}C | Target: {target_temp}C")
            log("Humidity Check", f"Current: {current_hum}% | Target Range: {min_hum}-{max_hum}%")

            if current_temp < target_temp - 0.2: 
                log("Action", "Heating ON.")
                if not self.heating_on:
                    self.on_heating_element()
                    self.heating_on = True

            elif target_temp - 0.2 <= current_temp <= target_temp + 0.2: 
                log("Action", "Temperature Normal, Heating OFF.")
                if self.heating_on:
                    self.off_heating_element()
                    self.heating_on = False

            if not self.cooler_on:
                self.on_cooler()
                self.cooler_on = True
                log("Action", "Ensuring cooler stays ON.")

            current_time = time.time()
            if current_hum < min_hum and (current_time - last_humidifier_time > 30):  
                log("Action", "Humidifier ON (Less frequent activation).")
                self.on_humidifier()
                self.humidifier_on = True
                time.sleep(10) 
                self.off_humidifier()
                self.humidifier_on = False
                last_humidifier_time = current_time 
                log("Action", "Humidifier OFF after 10s, waiting 30s before next activation.")

            elif current_hum > max_hum:
                log("Action", "Humidifier OFF due to high humidity.")
                if self.humidifier_on:
                    self.off_humidifier()
                    self.humidifier_on = False

            if self.humidifier_on and current_temp < target_temp - 0.6:
                log("Action", "Temperature dropping too fast due to humidifier. Turning on heating.")
                if not self.heating_on:
                    self.on_heating_element()
                    self.heating_on = True

            if current_temp > target_temp + 1.0:
                log("Action", "Temperature too high, using humidifier for cooling.")
                self.on_humidifier()
                time.sleep(10)
                self.off_humidifier()
                log("Action", "Humidifier OFF after cooling cycle.")

            self.rotate_eggs()

            log("Hatching Status", f"Day {current_day}: Temp {current_temp}C, Hum {current_hum}%")
            time.sleep(10)

        log("Hatching Stopped", "Exiting hatching loop.")

    def stop_hatching(self) -> None:
        self.hatching = False
        self.off_heating_element()
        self.off_cooler()
        self.off_humidifier()
        self.heating_on = False
        self.cooler_on = False
        self.humidifier_on = False

        log("Hatching Stopped", "All processes stopped")


    def resume_hatching(self) -> bool | None:
        if self.hatching:
            log("Hatching Already Running", "No action needed.")
            return False
        
        log("Hatching Resumed", "Restarting hatching process.")
        self.start_hatching()



    def set_temp(self, temp: float) -> None:
        """
        Manually set the incubator temperature and update hatching target values.
        """
        self.off_heating_element()
        self.on_heating_element()
        self.off_cooler()
        self.on_cooler()

        while True:
            current_temp = float(self.get_temp_and_hum().get('temp', -1))
            if current_temp >= temp:
                self.off_heating_element()
                self.off_cooler()
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
        self.off_cooler()
        self.on_cooler()

        while True:
            current_hum = float(self.get_temp_and_hum().get('hum', -1))
            if current_hum >= hum:
                self.off_humidifier()
                self.off_cooler()
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

    def get_target_hum(self, day: int) -> tuple[float, float]:
        """Retrieve the recommended humidity range (min_hum, max_hum) for the given day."""
        hum_data = {
            **dict.fromkeys(range(1, 19), (60.0, 70.0)),  # ✅ Always return (min, max)
            **dict.fromkeys(range(19, 22), (70.0, 80.0))  # ✅ Tuple format
        }
        return hum_data.get(day, (60.0, 70.0))  # ✅ Ensuring a tuple is always returned




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

            return {
                "status_code": 404,
                "content": "error at lid",
                "lid": "undefined",
                "timestamp": datetime.now().__str__()
            }

        if not os.path.exists(self.lid_file_path):
            log(description="lid status file does not exists")

            return {
                "status_code": 404,
                "lid": "undefined",
                "timestamp": datetime.now().__str__()
            }

        with open(self.lid_file_path, 'r') as file:
            log(description="access lid status file")

            lines = file.readlines()
            for line in lines:
                if line.startswith("!"):
                    status: str = line.split(" ")[1]

                    stats(info={"lid": status})

                    return {
                        "status_code": 200,
                        "lid": status,
                        "timestamp": datetime.now().__str__()
                    }

    """ Cooler """

    def on_cooler(self) -> None:
        self.start_process(name="cooler", script="cooler.py")
        self.on_cold_white_led()
        log("Cooler ON", "Cooler activated")


    def off_cooler(self) -> None:
        self.stop_process(name="cooler")
        self.off_cold_white_led()
        log("Cooler OFF", "Cooler deactivated.")

    """ Heating element """

    def on_heating_element(self) -> None:
        self.start_process(name="heating_element", script="heating_element.py")
        self.on_green_led()
        log("Heating ON", "Heating element activated.")

    def off_heating_element(self) -> None:
        self.stop_process("heating_element")
        self.off_green_led()
        log("Heating OFF", "Heating element deactivated.")

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
        try:
            with open("last_egg_rotation.txt", "r") as file:
                last_rotation_str = file.readline().strip()
                if last_rotation_str:
                    self.last_rotation = datetime.strptime(last_rotation_str, "%Y-%m-%d %H:%M:%S")
                else:
                    log("Egg Rotation", "File exists but empty, forcing rotation now.")
                    self.last_rotation = datetime.now() - timedelta(hours=6)  # Force immediate rotationtimedelta
        except FileNotFoundError:
            log("Egg Rotation", "Rotation file missing, forcing rotation now.")
            self.last_rotation = datetime.now() - timedelta(hours=6)  # Force immediate rotation

        if (datetime.now() - self.last_rotation).total_seconds() >= 6 * 3600:
            log("Egg Rotation", "Rotating eggs.")
            for _ in range(3):
                self.on_engine_forward()
                time.sleep(4)
                self.off_engine_forward()
                time.sleep(4)
                self.on_engine_backward()
                time.sleep(4)
                self.off_engine_backward()
                time.sleep(5)

            self.last_rotation = datetime.now()
            with open("last_egg_rotation.txt", "w") as file:
                file.write(self.last_rotation.strftime("%Y-%m-%d %H:%M:%S"))
            log("Egg Rotation", "Rotation completed and timestamp updated.")



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