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

    log_directory = "log"
    log_file_path = f"{log_directory}/{today}-log_system.txt"

    os.makedirs(log_directory, exist_ok=True)

    with open(log_file_path, 'a+') as file:
        file.write("reason: " + reason + '\n')
        file.write("description: " + description + '\n')
        file.write("api_url: " + api_url + '\n')
        file.write("headers: " + headers + '\n')
        file.write("timestamp: " + datetime.now().__str__() + '\n')
        file.write("--------\n")


def safe_exit(signum, frame):
    """ provides safe exit from a program """
    exit(1)


class Utils:
    """
        All actions inside csibekelteto will be implemented here.
        Call webserver endpoint to run certain action.
    """

    def __init__(self):
        self.base_dir: str = os.path.dirname(os.path.abspath(__file__))
        self.lid_file_path: str = os.path.join(self.base_dir, "lid-status.txt")
        self.processes: dict = {}

    # __static methods

    def __start_process(self, name, script):
        """Start a subprocess in a new session and track it by name."""

        if name in self.processes and self.processes[name].poll() is None:
            print(f"{name} is already running.")
            return

        process = subprocess.Popen(
            [os.path.join(self.base_dir, script)],
            start_new_session=True  # Start in a new session
        )
        self.processes[name] = process

    def __stop_process(self, name):
        """Stop a running subprocess by name."""
        if name in self.processes and self.processes[name].poll() is None:
            os.killpg(os.getpgid(self.processes[name].pid), signal.SIGTERM)
            self.processes[name].wait()
            del self.processes[name]
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

    def run_prediction_algorithm(self) -> None:
        """
        Run szakdolgozat-algorithm to predict the normal temp and hum range.
        java code will be called
        """
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
        self.__start_process("cooler", "py-part/cooler.py")

    def off_cooler(self) -> None:
        self.__stop_process("cooler")


    """ Heating element """

    def on_heating_element(self) -> None:
        self.__start_process("heating_element", "py-part/heating_element.py")
        self.indicate_heating_element()

    def off_heating_element(self) -> None:
        self.__stop_process("heating_element")


    """ DC Motor """

    def on_dc_motor_forward(self):
        self.__start_process("dc_motor_forward", "py-part/dc_motor_forward.py")
        self.__start_process("blink_yellow_led_dc_forward", "py-part/blink_yellow_led.py")

    def off_dc_motor_forward(self):
        self.__stop_process("dc_motor_forward")
        self.__stop_process("blink_yellow_led_dc_forward")

    def on_dc_motor_backward(self):
        self.__start_process("dc_motor_backward", "py-part/dc_motor_backward.py")
        self.__start_process("blink_yellow_led_dc_backward", "py-part/blink_yellow_led.py")

    def off_dc_motor_backward(self):
        self.__stop_process("dc_motor_backward")
        self.__stop_process("blink_yellow_led_dc_backward")


    """ LED """
    # TODO: add for every component led indication


    def on_red_led(self) -> None:
        self.__start_process("blink_red_led", "py-part/blink_red_led.py")

    def off_red_led(self) -> None:
        self.__stop_process("blink_red_led")

    def on_green_led(self) -> None:
        self.__start_process("blink_green_led", "py-part/blink_green_led.py")

    def off_green_led(self) -> None:
        self.__stop_process("blink_green_led")

    def on_blue_led(self) -> None:
        self.__start_process("blink_blue_led", "py-part/blink_blue_led.py")

    def off_blue_led(self) -> None:
        self.__stop_process("blink_blue_led")

    def on_yellow_led(self) -> None:
        self.__start_process("blink_yellow_led", "py-part/blink_yellow_led.py")

    def off_yellow_led(self) -> None:
        self.__stop_process("blink_yellow_led")

    def on_all_led(self) -> None:
        self.__start_process("rgb_led", "py-part/blink_rgb_led.py")

    def off_all_led(self) -> None:
        self.__stop_process("rgb_led")


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
