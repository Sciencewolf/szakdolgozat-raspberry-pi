import os
import subprocess
from datetime import datetime
import signal
import requests as re


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


class Utils:
    """
        All actions inside csibekelteto will be implemented here.
        Call webserver endpoint to run certain action.
    """

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.processes = {}

    # __static methods
    def __on_led_factory(self, file_name: str) -> None:
        subprocess.Popen([os.path.join(self.base_dir, f"py-part/{file_name}.py")])

    def __off_led_factory(self, file_name: str) -> None:
        subprocess.run(["pkill", "-f", f"py-part/{file_name}.py"])

    def __start_process(self, name, script):
        """Start a subprocess and track it by name."""
        if name in self.processes and self.processes[name].poll() is None:
            print(f"{name} is already running.")
            return
        process = subprocess.Popen([os.path.join(self.base_dir, script)])
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

    def is_lid_closed(self) -> bool:
        r = re.get(os.getenv("API_URL_LID"))
        return r.status_code == re.codes.ok

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

    """ Cooler """

    def on_cooler(self) -> None:
        subprocess.Popen([os.path.join(self.base_dir, "py-part/cooler.py")])

    def off_cooler(self) -> None:
        subprocess.run(["pkill", "-f", "py-part/cooler.py"])


    """ Heating element """

    def on_heating_element(self) -> None:
        subprocess.Popen([os.path.join(self.base_dir, "py-part/heating_element.py")])

    def off_heating_element(self) -> None:
        subprocess.run(["pkill", "-f", "py-part/heating_element.py"])


    """ DC Motor """

    def on_dc_motor_forward(self):
        self.__start_process("dc_motor_forward", "py-part/dc_motor_forward.py")
        self.__start_process("blink_yellow_led", "py-part/blink_yellow_led.py")

    def off_dc_motor_forward(self):
        self.__stop_process("dc_motor_forward")
        self.__stop_process("blink_yellow_led")

    def on_dc_motor_backward(self):
        self.__start_process("dc_motor_backward", "py-part/dc_motor_backward.py")
        self.__start_process("blink_yellow_led", "py-part/blink_yellow_led.py")

    def off_dc_motor_backward(self):
        self.__stop_process("dc_motor_backward")
        self.__stop_process("blink_yellow_led")


    """ LED """
    # TODO: add for every component led indication


    def on_red_led(self) -> None:
        self.__on_led_factory("blink_rgb_red")

    def off_red_led(self) -> None:
        self.__off_led_factory("blink_rgb_red")

    def on_green_led(self) -> None:
        self.__on_led_factory("blink_rgb_green")

    def off_green_led(self) -> None:
        self.__off_led_factory("blink_rgb_green")

    def on_blue_led(self) -> None:
        self.__on_led_factory("blink_rgb_blue")

    def off_blue_led(self) -> None:
        self.__off_led_factory("blink_rgb_blue")

    def on_yellow_led(self) -> None:
        self.__on_led_factory("blink_yellow_led")

    def off_yellow_led(self) -> None:
        self.__off_led_factory("blink_yellow_led")

    def on_all_led(self) -> None:
        self.__on_led_factory("rgb_led")

    def off_all_led(self) -> None:
        self.__off_led_factory("rgb_led")


    """ Other """

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
    import time

    while True:
        utils.run()
        time.sleep(10)


if __name__ == "__main__":
    main()
