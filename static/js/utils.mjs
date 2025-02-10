class LED{
    static async onRedLed() {
        const onRedLed = await fetch("https://willing-just-penguin.ngrok-free.app/on-red-led")
        const response = await onRedLed.json()

        console.log(response)
        
    }

    static async offRedLed() {
        const offRedLed = await fetch("https://willing-just-penguin.ngrok-free.app/off-red-led")
        const response = await offRedLed.json()

        console.log(response)
        

    }

    static async onGreenLed() {
        const onGreenLed = await fetch("https://willing-just-penguin.ngrok-free.app/on-green-led")
        const response = await onGreenLed.json()

        console.log(response)
        

    }

    static async offGreenLed() {
        const offGreenLed = await fetch("https://willing-just-penguin.ngrok-free.app/off-green-led")
        const response = await offGreenLed.json()

        console.log(response)
        

    }

    static async onBlueLed() {
        const onBlueLed = await fetch("https://willing-just-penguin.ngrok-free.app/on-blue-led")
        const response = await onBlueLed.json()

        console.log(response)
        

    }

    static async offBlueLed() {
        const offBlueLed = await fetch("https://willing-just-penguin.ngrok-free.app/off-blue-led")
        const response = await offBlueLed.json()

        console.log(response)
        

    }

    static async onYellowLed() {
        const onYellowLed = await fetch("https://willing-just-penguin.ngrok-free.app/on-yellow-led")
        const response = await onYellowLed.json()

        console.log(response)
        

    }

    static async offYellowLed() {
        const offYellowLed = await fetch("https://willing-just-penguin.ngrok-free.app/off-yellow-led")
        const response = await offYellowLed.json()

        console.log(response)
        

    }

    static async onWhiteLed() {
        const onWhiteLed = await fetch("https://willing-just-penguin.ngrok-free.app/on-white-led")
        const response = await onWhiteLed.json()

        console.log(response)
        

    }

    static async offWhiteLed() {
        const offWhiteLed = await fetch("https://willing-just-penguin.ngrok-free.app/off-white-led")
        const response = await offWhiteLed.json()

        console.log(response)
        

    }

    static async onColdWhiteLed() {
        const onColdWhiteLed = await fetch("https://willing-just-penguin.ngrok-free.app/on-cold-white-led")
        const response = await onColdWhiteLed.json()

        console.log(response)
        

    }

    static async offColdWhiteLed() {
        const offColdWhiteLed = await fetch("https://willing-just-penguin.ngrok-free.app/off-cold-white-led")
        const response = await offColdWhiteLed.json()

        console.log(response)
        

    }
}

class Motor{
    static async onEngineForward() {
        const onEngineForward = await fetch("https://willing-just-penguin.ngrok-free.app/on-dc-motor-forward")
        const response = await onEngineForward.json()

        console.log(response)
        

    }

    static async offEngineForward() {
        const offEngineForward = await fetch("https://willing-just-penguin.ngrok-free.app/off-dc-motor-forward")
        const response = await offEngineForward.json()

        console.log(response)
        

    }

    static async onEngineBackward() {
        const onEngineBackward = await fetch("https://willing-just-penguin.ngrok-free.app/on-dc-motor-backward")
        const response = await onEngineBackward.json()

        console.log(response)
        

    }

    static async offEngineBackward() {
        const offEngineBackward = await fetch("https://willing-just-penguin.ngrok-free.app/off-dc-motor-backward")
        const response = await offEngineBackward.json()

        console.log(response)
        

    }
}

class Sensor {
    static async getTemperatureAndHumidity() {
        const getTemperatureAndHumidity = await fetch("https://willing-just-penguin.ngrok-free.app/get-temp-hum")
        const response = await getTemperatureAndHumidity.json()

        console.log(response)
        


        return [response.response.temp, response.response.hum]
    }

    static async getLidStatus() {
        const getLidStatus = await fetch("https://willing-just-penguin.ngrok-free.app/get-lid-status")
        const response = await getLidStatus.json()

        console.log(response)
        


        return response.response.lid
    }

}

class Cooler {
    static async onCooler() {
        const onCooler = await fetch("https://willing-just-penguin.ngrok-free.app/on-cooler")
        const response = await onCooler.json()

        console.log(response)
        

    }

    static async offCooler() {
        const offCooler = await fetch("https://willing-just-penguin.ngrok-free.app/off-cooler")
        const response = await offCooler.json()

        console.log(response)
        

    }
}

class HeatingElement {
    static async onHeatingElement() {
        const onHeatingElement = await fetch("https://willing-just-penguin.ngrok-free.app/on-heating-element")
        const response = await onHeatingElement.json()

        console.log(response)
        

    }

    static async offHeatingElement() {
        const offHeatingElement = await fetch("https://willing-just-penguin.ngrok-free.app/off-heating-element")
        const response = await offHeatingElement.json()

        console.log(response)
        

    }
}

class Humidifier {
    static async onHumidifier() {
        const onHumidifier = await fetch("https://willing-just-penguin.ngrok-free.app/on-humidifier")
        const response = await onHumidifier.json()

        console.log(response)
        

    }

    static async offHumidifier() {
        const offHumidifier = await fetch("https://willing-just-penguin.ngrok-free.app/off-humidifier")
        const response = await offHumidifier.json()

        console.log(response)
        

    }
}

class Health {
    static async getAll() {
        const get = await fetch("https://willing-just-penguin.ngrok-free.app/health")
        const response = await get.json()

        console.log(response)

        return [response.cpu, response.total_ram, response.ram, response.vram]
    }

    static async isRaspiAlive() {
        const get = await fetch("https://willing-just-penguin.ngrok-free.app/alive")
        const response = await get.json()

        console.log(response);

        return response.status_code === 200
    }
}

export {LED, Motor, Sensor, Cooler, HeatingElement, Humidifier, Health}