from datetime import datetime
import RP


class Logger:
    @staticmethod
    def info(*args: str | Exception | None):
        with open("info.txt", "a+") as file:
            for arg in args:
                file.write(f"INFO: [{datetime.now()}] {arg} \n")

    @staticmethod
    def warn(*args: str | Exception | None):
        with open("warn.txt", "a+") as file:
            for arg in args:
                file.write(f"WARN: [{datetime.now()}] {arg} \n")

    @staticmethod
    def error(*args: str | Exception | None):
        with open("error.txt", "a+") as file:
            for arg in args:
                file.write(f"ERROR: [{datetime.now()}] {arg} \n")

