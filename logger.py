from datetime import datetime
import os
import shutil
import glob


class Logger:
    def __init__(self, filetype: str, remove_log: bool = False) -> None:
        self.filetype = filetype
        self.remove_log = remove_log

        # private field's
        self.__main_path = '/app'
        print(self.__main_path)
        self.__logger_writer = "off"
        self.__logger_level = "off"  # info, warn, error, debug, all, off

        with open(f"{self.__main_path}/settings.txt", "r") as file:
            """ in future find better way to read settings file """
            writer = file.readline().split("=")[1].strip()
            if writer == "on":
                self.__logger_writer = writer

            level = file.readline().split("=")[1].strip()
            if level != "off":
                self.__logger_level = level

        if self.remove_log:
            shutil.rmtree(f"{self.__main_path}/log", ignore_errors=True)  # Remove non-empty directory
            return

        if not os.path.isdir(f"{self.__main_path}/log"):
            os.mkdir(f"{self.__main_path}/log")

    def info(self, *args: str | Exception | None) -> None:
        if self.__logger_writer == "on" and self.__logger_level in ["info", "all"]:
            with open(f"{self.__main_path}/log/{self.filetype}info.txt", "a+") as file:
                for arg in args:
                    file.write(f"INFO: [{datetime.now()}] {arg}  \n")

    def warn(self, *args: str | Exception | None) -> None:
        if self.__logger_writer == "on" and self.__logger_level in ["warn", "all"]:
            with open(f"{self.__main_path}/log/{self.filetype}warn.txt", "a+") as file:
                for arg in args:
                    file.write(f"WARN: [{datetime.now()}] {arg}  \n")

    def error(self, *args: str | Exception | None) -> None:
        if self.__logger_writer == "on" and self.__logger_level in ["error", "all"]:
            with open(f"{self.__main_path}/log/{self.filetype}error.txt", "a+") as file:
                for arg in args:
                    file.write(f"ERROR: [{datetime.now()}] {arg}  \n")

    def debug(self, *args: str | Exception | None) -> None:
        """ print's out *args to sys.stdout """
        if self.__logger_level in ["debug", "all"]:
            print(f"DEBUG: [{datetime.now()}] {args} \n")

    def close(self) -> None:
        """ Close logger with writing 'end of session' """
        txt_files = glob.glob(f"{self.__main_path}/log/*.txt")
        for file in txt_files:
            with open(file, 'a+') as f:
                f.write(f"--- End of session --- @ {datetime.now()}\n")
