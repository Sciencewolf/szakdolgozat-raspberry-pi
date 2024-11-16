import os
import sys
from datetime import datetime
import requests as re


class Utils:
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

    def indicate_egg_rotating(self) -> None:
        """ Green LED if engine is rotating the egg's. Do not touch the lid """
        pass

    def log(self, content: str) -> None:
        """ Keep logging the event's into a file """

        with open("log_system.txt", 'a+') as file:
            file.write(content + '\n')
            file.write(datetime.now().__str__() + '\n')


    def run_prediction_algorithm(self) -> None:
        """
        Run szakdolgozat-algorithm to predict the normal temp and hum range.
        java code will be called
        """
        pass


    def run(self) -> None:
        """ Main function for Utils class """
        self.run_prediction_algorithm()
        self.




def main() -> None:
    utils: Utils = Utils()
    import time

    while True:
        utils.run()
        time.sleep(10)



if __name__ == "__main__":
    main()
