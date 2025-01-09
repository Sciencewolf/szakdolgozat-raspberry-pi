class LED{
    static async onRedLed() {
        const onRedLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-red-led")
        const response = await onRedLed.json()

        console.log(response)
        
    }

    static async offRedLed() {
        const offRedLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-red-led")
        const response = await offRedLed.json()

        console.log(response)
        

    }

    static async onGreenLed() {
        const onGreenLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-green-led")
        const response = await onGreenLed.json()

        console.log(response)
        

    }

    static async offGreenLed() {
        const offGreenLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-green-led")
        const response = await offGreenLed.json()

        console.log(response)
        

    }

    static async onBlueLed() {
        const onBlueLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-blue-led")
        const response = await onBlueLed.json()

        console.log(response)
        

    }

    static async offBlueLed() {
        const offBlueLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-blue-led")
        const response = await offBlueLed.json()

        console.log(response)
        

    }

    static async onYellowLed() {
        const onYellowLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-yellow-led")
        const response = await onYellowLed.json()

        console.log(response)
        

    }

    static async offYellowLed() {
        const offYellowLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-yellow-led")
        const response = await offYellowLed.json()

        console.log(response)
        

    }

    static async onWhiteLed() {
        const onWhiteLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-white-led")
        const response = await onWhiteLed.json()

        console.log(response)
        

    }

    static async offWhiteLed() {
        const offWhiteLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-white-led")
        const response = await offWhiteLed.json()

        console.log(response)
        

    }

    static async onOrangeLed() {
        const onOrangeLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-orange-led")
        const response = await onOrangeLed.json()

        console.log(response)
        

    }

    static async offOrangeLed() {
        const offOrangeLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-orange-led")
        const response = await offOrangeLed.json()

        console.log(response)
        

    }

    static async onPurpleLed() {
        const onPurpleLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-purple-led")
        const response = await onPurpleLed.json()

        console.log(response)
        

    }

    static async offPurpleLed() {
        const offPurpleLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-purple-led")
        const response = await offPurpleLed.json()

        console.log(response)
        

    }
}

class Motor{
    static async onDcMotorForward() {
        const onDcMotorForward = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-dc-motor-forward")
        const response = await onDcMotorForward.json()

        console.log(response)
        

    }

    static async offDcMotorForward() {
        const offDcMotorForward = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-dc-motor-forward")
        const response = await offDcMotorForward.json()

        console.log(response)
        

    }

    static async onDcMotorBackward() {
        const onDcMotorBackward = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-dc-motor-backward")
        const response = await onDcMotorBackward.json()

        console.log(response)
        

    }

    static async offDcMotorBackward() {
        const offDcMotorBackward = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-dc-motor-backward")
        const response = await offDcMotorBackward.json()

        console.log(response)
        

    }
}

class Sensor {
    static async getTemperatureAndHumidity() {
        const getTemperatureAndHumidity = await fetch("https://hippo-immense-plainly.ngrok-free.app/get-temp-hum")
        const response = await getTemperatureAndHumidity.json()

        console.log(response)
        


        return [response.temp, response.hum]
    }

    static async getLidStatus() {
        const getLidStatus = await fetch("https://hippo-immense-plainly.ngrok-free.app/get-lid-status")
        const response = await getLidStatus.json()

        console.log(response)
        


        return response.lid
    }

}

class Cooler {
    static async onCooler() {
        const onCooler = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-cooler")
        const response = await onCooler.json()

        console.log(response)
        

    }

    static async offCooler() {
        const offCooler = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-cooler")
        const response = await offCooler.json()

        console.log(response)
        

    }
}

class HeatingElement {
    static async onHeatingElement() {
        const onHeatingElement = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-heating-element")
        const response = await onHeatingElement.json()

        console.log(response)
        

    }

    static async offHeatingElement() {
        const offHeatingElement = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-heating-element")
        const response = await offHeatingElement.json()

        console.log(response)
        

    }
}

class Humidifier {
    static async onHumidifier() {
        const onHumidifier = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-humidifier")
        const response = await onHumidifier.json()

        console.log(response)
        

    }

    static async offHumidifier() {
        const offHumidifier = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-humidifier")
        const response = await offHumidifier.json()

        console.log(response)
        

    }
}

class Health {
    static async getAll() {
        const get = await fetch("https://hippo-immense-plainly.ngrok-free.app/health")
        const response = await get.json()

        console.log(response)

        return [response.cpu, response.total_ram, response.ram, response.vram]
    }
}

export {LED, Motor, Sensor, Cooler, HeatingElement, Humidifier, Health}