import sys

filename: str = ""

if str(sys.argv[1]).endswith(".py"):
    filename = str(sys.argv[1])
elif not str(sys.argv[1]).endswith('.py'):
    filename = str(sys.argv[1]) + ".py"
    

with open(filename, 'w') as file:
    file.write('#')
    file.write('!/usr/bin/env python\n\n')
    file.write("import RPi.GPIO as gpio\n")
    file.write("import time\n")
    file.write("from signal import signal, SIGTERM, SIGHUP\n\n")
    file.write("# define gpio pin's\n\n\n")
    file.write("# setmode\ngpio.setmode(gpio.BCM)\n\n")
    file.write("# setup\n")
    file.write("gpio.setup(, gpio.OUT)\n\n\n")
    file.write("def main() -> None:\n\t")
    file.write("try:\n\t\t")
    file.write("signal(SIGTERM, safe_exit)\n\t\t")
    file.write("signal(SIGHUP, safe_exit)\n\t\t")
    file.write("while True:\n\t\t\t")
    file.write("# your code goes here\n\t")
    file.write("except KeyboardInterrupt as ex:\n\t\t")
    file.write("print(ex)\n\t")
    file.write("finally:\n\t\t")
    file.write("gpio.cleanup()\n\n\n")
    file.write("def safe_exit(signum, frame) -> None:\n\t")
    file.write('""" Provides a safe shutdown of the program """\n\t')
    file.write("exit(1)\n\n")
    file.write('if __name__ == "__main__":\n\t')
    file.write("main()\n")
