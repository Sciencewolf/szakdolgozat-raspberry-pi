from gpiozero import LED
import time


def main() -> None:
    led = LED(20)

    led.on()
    time.sleep(2)
    led.off()


if __name__ == "__main__":
    main()
