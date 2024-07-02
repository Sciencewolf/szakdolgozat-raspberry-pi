from datetime import datetime


class Logger:
    def __init__(self, filetype: str):
        self.filetype = filetype
        self.logger_writer = "off"
        self.logger_debug = "off"

        with open("settings.txt", "r") as file:
            """ in future find better way to read settings file """
            writer = file.readline().split("=")[1].rstrip()
            if writer == "on":
                self.logger_writer = "on"

            debugger = file.readline().split("=")[1].rstrip()
            if debugger == "on":
                self.logger_debug = "on"

    def info(self, *args: str | Exception | None):
        if self.logger_writer == "on":
            with open(f"log/{self.filetype}info.txt", "a+") as file:
                for arg in args:
                    file.write(f"INFO: [{datetime.now()}] {arg} ! \n")

    def warn(self, *args: str | Exception | None):
        if self.logger_writer == "on":
            with open(f"log/{self.filetype}warn.txt", "a+") as file:
                for arg in args:
                    file.write(f"WARN: [{datetime.now()}] {arg} ! \n")

    def error(self, *args: str | Exception | None):
        if self.logger_writer == "on":
            with open(f"log/{self.filetype}error.txt", "a+") as file:
                for arg in args:
                    file.write(f"ERROR: [{datetime.now()}] {arg} ! \n")

    def debug(self, *args: str | Exception | None):
        if self.logger_debug == "on":
            print(args)
