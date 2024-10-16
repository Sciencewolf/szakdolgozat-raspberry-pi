import os
import sys


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
        pass

    def last_emergency_shutdown(self) -> None:
        pass

    def is_webserver_alive(self) -> bool:
        pass

    def is_lid_closed(self) -> bool:
        pass

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

    def run_prediction_algorithm(self) -> None:
        """
        Run szakdolgozat-algorithm to predict the normal temp and hum range.
        java code will be called
        """
        pass


def main() -> None:
    utils: Utils = Utils()


if __name__ == "__main__":
    main()
