import os
from datetime import datetime
from deprecated import deprecated

import requests as re


def log(reason: str="", description: str="", api_url: str="", headers: str="") -> None:
    """ Keep logging the event's into a file """

    with open("log_system.txt", 'a+') as file:
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
        pass

    def __str__(self) -> str:
        return (f"---Utils--- "
                f"\n\tHealth: {self.health()} "
                f"\n\tLast Emergency Shutdown: {self.last_emergency_shutdown()}"
                f"\n---Utils---")

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

    @deprecated(reason="no reason to use this method")
    def is_webserver_alive(self) -> bool:
        r = re.get(os.getenv("API_URL_ALIVE"))
        return r.status_code == re.codes.ok

    def is_lid_closed(self) -> bool:
        r = re.get(os.getenv("API_URL_LID"))
        return r.status_code == re.codes.ok

    def is_temperature_normal(self) -> bool:
        pass

    def is_humidity_normal(self) -> bool:
        pass

    def error(self) -> None:
        """ Red LED """
        pass

    def last_error(self) -> str | None:
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
