import os
import subprocess
from datetime import datetime
import signal
from flask import jsonify, Response


def log(
        reason: str = "",
        description: str = "",
        api_url: str = "",
        headers: str = ""
) -> None:
    """ Keep logging the event's into a file """

    today = datetime.now().strftime("%Y-%B-%d")

    log_directory = "/home/aron/szakdolgozat-raspberry-pi/log"
    log_file_path = f"{log_directory}/{today}-log_system.txt"

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
    "orange": 5,
    "yellow": 6,
    "purple": 13,
    "blue": 19
}

class Mode:
    """ Defines modes for led [blink or hold]  """

    blink = "blink"
    hold = "hold"

class Leds:
    """ Defines led colors """

    red = "red"
    green = "green"
    white = "white"
    orange = "orange"
    yellow = "yellow"
    purple = "purple"
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
    # TODO: leds on start process

    def __start_process(self, name: str, script: str="led.py", led: str="", mode: str="") -> None:
        """Start a subprocess in a new session and track it by name."""

        if name in self.processes and self.processes[name].poll() is None:
            print(f"Process {name} is already running with PID {self.processes[name].pid}.")
            return

        try:
            process = subprocess.Popen(
                [os.path.join(self.base_dir, f"py-part/{script}")] + [led, mode],
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

    def get_temp_and_hum(self, api_base_url: str, timestamp: datetime, headers: str) -> Response:
        result = subprocess.run(
            [os.path.join(self.base_dir, "py-part/temp_hum_sensor.py")],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return jsonify({
                "status_code": 404,
                "content": "not found response",
                "timestamp": timestamp
            })

        try:
            with open(os.path.join(self.base_dir, "temp_hum.txt"), 'r') as file:
                temp = file.readline().strip()
                hum = file.readline().strip()
                timestamp = file.readline().strip()
        except FileNotFoundError as fnfe:
            log(
                reason="error at reading temp_hum.txt",
                description=f"file not found {fnfe.__str__()}",
                api_url=api_base_url,
                headers=headers
            )

            return jsonify({
                "status_code": 404,
                "content": "not found response",
                "timestamp": timestamp
            })

        return jsonify({
            "temp": temp,
            "hum": hum,
            "timestamp": timestamp
        })

    def is_temperature_normal(self) -> bool:
        pass

    def is_humidity_normal(self) -> bool:
        pass

    def indicate_heating_element(self) -> None:
        """ Blue LED if heating element is working. Do not touch the lid """
        pass

    def indicate_humidifier(self) -> None:
        """ Yellow LED if humidifier if working. Do not touch the lid """
        pass

    def indicate_eggs_rotating(self) -> None:
        """ Green LED if engine is rotating the egg's. Do not touch the lid """
        pass

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

    def lid_status(self, api_base_url: str, timestamp: datetime, headers: str) -> Response:
        result = subprocess.run(
            [os.path.join(self.base_dir, "py-part/switch.py")],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            log(
                reason="error at switch",
                description="not found",
                api_url=api_base_url,
                headers=headers
            )

            return jsonify({
                "status_code": 404,
                "content": "error at lid",
                "timestamp": timestamp
            })

        if not os.path.exists(self.lid_file_path):
            log(
                description="lid status file does not exists",
                api_url=api_base_url
            )

            return jsonify({
                "status_code": 404,
                "lid": "undefined",
                "timestamp": timestamp
            })

        with open(self.lid_file_path, 'r') as file:
            log(
                description="access lid status file",
                api_url=api_base_url,
                headers=headers
            )

            lines = file.readlines()
            for line in lines:
                if line.startswith("!"):
                    return jsonify({
                        "status_code": 200,
                        "lid": line.split(" ")[1],
                        "timestamp": timestamp
                    })

    """ Cooler """

    def on_cooler(self) -> None:
        self.__start_process(name="cooler", script="cooler.py")
        self.on_white_led()

    def off_cooler(self) -> None:
        self.__stop_process(name="cooler")
        self.off_white_led()

    """ Heating element """

    def on_heating_element(self) -> None:
        self.__start_process(name="heating_element", script="heating_element.py")
        self.on_green_led()

    def off_heating_element(self) -> None:
        self.__stop_process("heating_element")
        self.off_green_led()

    """ DC Motor """

    def on_dc_motor_forward(self) -> None:
        self.__start_process(name="dc_motor_forward", script="dc_motor_forward.py")
        self.on_yellow_led()

    def off_dc_motor_forward(self) -> None:
        self.__stop_process("dc_motor_forward")
        self.off_yellow_led()

    def on_dc_motor_backward(self) -> None:
        self.__start_process(name="dc_motor_backward", script="dc_motor_backward.py")
        self.on_yellow_led()

    def off_dc_motor_backward(self) -> None:
        self.__stop_process("dc_motor_backward")
        self.off_yellow_led()


    """ Humidifier """

    def on_humidifier(self) -> None:
        self.__start_process(name="humidifier", script="humidifier.py")
        self.on_purple_led()

    def off_humidifier(self) -> None:
        self.__stop_process("humidifier")
        self.off_purple_led()

    """ LED """

    def on_red_led(self, mode: str=Mode.hold) -> None:
        self.__start_process(
            name="red_led",
            led=Leds.red,
            mode=mode
        )

    def off_red_led(self) -> None:
        self.__stop_process("red_led")

    def on_green_led(self, mode: str=Mode.hold) -> None:
        self.__start_process(
            name="green_led",
            led=Leds.green,
            mode=mode
        )

    def off_green_led(self) -> None:
        self.__stop_process("green_led")

    def on_white_led(self, mode: str=Mode.hold) -> None:
        self.__start_process(
            name="white_led",
            led=Leds.white,
            mode=mode
        )

    def off_white_led(self) -> None:
        self.__stop_process("white_led")

    def on_orange_led(self, mode: str=Mode.hold) -> None:
        self.__start_process(
            name="orange_led",
            led=Leds.orange,
            mode=mode
        )

    def off_orange_led(self) -> None:
        self.__stop_process("orange_led")

    def on_yellow_led(self, mode: str=Mode.hold) -> None:
        self.__start_process(
            name="yellow_led",
            led=Leds.yellow,
            mode=mode
        )

    def off_yellow_led(self) -> None:
        self.__stop_process("yellow_led")

    def on_purple_led(self, mode: str=Mode.hold) -> None:
        self.__start_process(
            name="purple_led",
            led=Leds.purple,
            mode=mode
        )

    def off_purple_led(self) -> None:
        self.__stop_process("purple_led")

    def on_blue_led(self, mode: str=Mode.hold) -> None:
        self.__start_process(
            name="blue_led",
            led=Leds.blue,
            mode=mode
        )

    def off_blue_led(self) -> None:
        self.__stop_process("blue_led")


    """ Other """

    def shutdown(self) -> None:
        shutdown_command = "sudo shutdown -h now"
        os.system(shutdown_command)

    def health(self) -> None:
        """ Green LED """
        pass

    def emergency_shutdown(self) -> None:
        """
            1. heating element -> off
            2. dc engine if its running -> off
            3. humidifier if its running -> off
            4. cooler -> off
            5. LED if someone is running -> off
        """
        pass

    def last_emergency_shutdown(self) -> None:
        pass

    def error(self) -> None:
        """ Red LED """
        pass

    def last_error(self) -> str | None:
        pass

    def run(self) -> None:
        """ Main function for Utils class """
        self.run_prediction_algorithm()


def main() -> None:
    utils: Utils = Utils()
    print(utils.processes)


if __name__ == "__main__":
    main()
