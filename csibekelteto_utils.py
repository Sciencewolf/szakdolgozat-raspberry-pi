import os
import subprocess
from datetime import datetime
import signal
from flask import jsonify
import psutil
import time


def log(
        reason: str = "",
        description: str = "",
        api_url: str = "",
        headers: str = ""
) -> None:
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
        self.lid_file_path: str = os.path.join(self.base_dir, "lid-status.txt")
        self.processes: dict = {}
        self.led_panel: dict = {}

    # __private methods

    def __start_process(self, name: str, script: str="led.py", led: str="", mode: str="") -> None:
        """Start a subprocess in a new session and track it by name."""

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


    def __stop_process(self, name: str) -> None:
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
                "status_code": 404,
                "content": "not found response",
                "timestamp": timestamp
            }

        with open(os.path.join(self.base_dir, "temp_hum.txt"), 'r') as file:
            temp = file.readline().strip()
            hum = file.readline().strip()
            timestamp = file.readline().strip()

            return {
                "temp": temp,
                "hum": hum,
                "timestamp": timestamp
            }
    

    def set_temp(self, temp: float) -> None:
        self.on_heating_element()

        while True:
            temp, _, day = self.get_temp_and_hum()

            if self.is_temperature_normal(day, temp):
                self.off_heating_element()
                break

            time.sleep(20)
    

    def set_hum(self, hum: float) -> None:
        self.on_humidifier()

        while True:
            _, hum, day = self.get_temp_and_hum()

            if self.is_humidity_normal(day, hum):
                self.off_humidifier()
                break

            time.sleep(20)


    def is_temperature_normal(self, day: int, temp: float) -> bool:
        temp_datas = {
            0: 37.5
        }

        return temp_datas[day] == temp

    def is_humidity_normal(self, day: int, hum: float) -> bool:
        hum_datas = {
            0: 66.7
        }

        return hum_datas[day] == hum

    def prepare_hatching(self) -> str | None:
        """ before hatching eggs check if hardware is okay """
        pass

    def start_hatching(self) -> None:
        """
        Call this method when egg is ready to hatching.
        TODO: check if everything is working fine
        """
        with open("hatching_date.txt", 'w') as file:
            file.write(datetime.now().__str__())

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
                "lid": "undefined",
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
        self.__start_process(name="cooler", script="cooler.py")
        self.on_cold_white_led()

    def off_cooler(self) -> None:
        self.__stop_process(name="cooler")
        self.off_cold_white_led()

    """ Heating element """

    def on_heating_element(self) -> None:
        self.__start_process(name="heating_element", script="heating_element.py")
        self.on_green_led()

    def off_heating_element(self) -> None:
        self.__stop_process("heating_element")
        self.off_green_led()

    """ DC Motor """

    def on_engine_forward(self) -> None:
        self.__start_process(name="engine_forward", script="engine_forward.py")
        self.on_yellow_led()

    def off_engine_forward(self) -> None:
        self.__stop_process("engine_forward")
        self.off_yellow_led()

    def on_engine_backward(self) -> None:
        self.__start_process(name="engine_backward", script="engine_backward.py")
        self.on_yellow_led()

    def off_engine_backward(self) -> None:
        self.__stop_process("engine_backward")
        self.off_yellow_led()


    """ Humidifier """

    def on_humidifier(self) -> None:
        self.__start_process(name="humidifier", script="humidifier.py")
        self.on_cold_white_led()

    def off_humidifier(self) -> None:
        self.__stop_process("humidifier")
        self.off_cold_white_led()

    """ LED """

    def on_red_led(self, mode: str=Mode.hold) -> None:
        self.__start_process(
            name="red_led",
            led=LEDs.red,
            mode=mode
        )

    def off_red_led(self) -> None:
        self.__stop_process("red_led")

    def on_green_led(self, mode: str=Mode.hold) -> None:
        self.__start_process(
            name="green_led",
            led=LEDs.green,
            mode=mode
        )

    def off_green_led(self) -> None:
        self.__stop_process("green_led")

    def on_white_led(self, mode: str=Mode.hold) -> None:
        self.__start_process(
            name="white_led",
            led=LEDs.white,
            mode=mode
        )

    def off_white_led(self) -> None:
        self.__stop_process("white_led")

    def on_yellow_led(self, mode: str=Mode.hold) -> None:
        self.__start_process(
            name="yellow_led",
            led=LEDs.yellow,
            mode=mode
        )

    def off_yellow_led(self) -> None:
        self.__stop_process("yellow_led")

    def on_cold_white_led(self, mode: str=Mode.hold) -> None:
        self.__start_process(
            name="cold_white_led",
            led=LEDs.cold_white,
            mode=mode
        )

    def off_cold_white_led(self) -> None:
        self.__stop_process("cold_white_led")

    def on_blue_led(self, mode: str=Mode.hold) -> None:
        self.__start_process(
            name="blue_led",
            led=LEDs.blue,
            mode=mode
        )

    def off_blue_led(self) -> None:
        self.__stop_process("blue_led")


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

    def emergency_shutdown(self) -> None:
        """
            1. heating element -> off
            2. dc engine if its running -> off
            3. humidifier if its running -> off
            4. cooler -> off
            5. LED if someone is running -> off
        """

        with open("emergency.txt", 'a+') as file:
            file.write(datetime.now().__str__())


    def last_emergency_shutdown(self) -> str:
        with open('emergency.txt', 'r') as file:
            return file.readlines()[-1]


def main() -> None:
    utils: Utils = Utils()
    print(utils.processes)


if __name__ == "__main__":
    main()
