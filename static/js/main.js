const checkboxOnOffRedLed = document.getElementById("checkbox-on-off-red-led")
const checkboxOnOffGreenLed = document.getElementById("checkbox-on-off-green-led")
const checkboxOnOffWhiteLed = document.getElementById("checkbox-on-off-white-led")
const checkboxOnOffOrangeLed = document.getElementById("checkbox-on-off-orange-led")
const checkboxOnOffYellowLed = document.getElementById("checkbox-on-off-yellow-led")
const checkboxOnOffPurpleLed = document.getElementById("checkbox-on-off-purple-led")
const checkboxOnOffBlueLed = document.getElementById("checkbox-on-off-blue-led")

const temperature = document.getElementById("temp")
const humidity = document.getElementById("hum")
const lid = document.getElementById("lid")

const checkboxOnOffCooler = document.getElementById("checkbox-on-off-cooler")
const checkboxOnOffHeatingElement = document.getElementById("checkbox-on-off-heating-element")
const checkboxOnOffDcMotorForward = document.getElementById("checkbox-on-off-dc-motor-forward")
const checkboxOnOffDcMotorBackward = document.getElementById("checkbox-on-off-dc-motor-backward")
const checkboxOnOffHumidifier = document.getElementById("checkbox-on-off-humidifier")

const btnEndpoints = document.getElementById("btn-endpoints")
const divEndpoints = document.getElementById("div-endpoints")

const shutdown = document.getElementById("btn-shutdown")


const tempHumSensor = async () => {
    try {
        const getTemperatureAndHumidity = await fetch("https://hippo-immense-plainly.ngrok-free.app/get-temp-hum")
        const response = await getTemperatureAndHumidity.json()
        console.log(response)
        temperature.innerHTML = response.temp
        humidity.innerHTML = response.hum
    } catch (error) {
        console.log(error);
    }
}

const lidStatus = async () => {
    try {
        const getLidStatus = await fetch("https://hippo-immense-plainly.ngrok-free.app/get-lid-status")
        const response = await getLidStatus.json()
        console.log(response)
        lid.innerHTML = response.lid
    } catch (error) {
        console.log(error);
    }
}

const changeTitle = (title, iconType="d") => {
    const titleElement = document.querySelector("title")
    const iconElement = document.getElementById("icon")

    const values = new Map()
    values.set("r", "../static/images/red-led.png")
    values.set("g", "../static/images/green-led.png")
    values.set("b", "../static/images/blue-led.png")
    values.set("y", "../static/images/yellow-led.png")
    values.set("e", "../static/images/error.png")
    values.set("d", "../static/images/favicon.png")

    titleElement.innerHTML = title
    iconElement.href = values.get(iconType)
    
    setInterval(() => {
        titleElement.innerText = "Csibekeltető"
        iconElement.href = values.get("d")
    }, 5_000)
}

window.addEventListener("load", async () => {
    await tempHumSensor()
    await lidStatus()
})

checkboxOnOffRedLed.addEventListener('click', async () => {
    if (checkboxOnOffRedLed.checked) {
        try {
            const onRedLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-red-led")
            const response = await onRedLed.json()
            console.log(response)
            changeTitle("RedLED is ON", 'r')
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    } else {
        try {
            const offRedLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-red-led")
            const response = await offRedLed.json()
            console.log(response)
            changeTitle("RedLED is OFF")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    }
})

checkboxOnOffGreenLed.addEventListener('click', async () => {
    if (checkboxOnOffGreenLed.checked) {
        try {
            const onGreenLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-green-led")
            const response = await onGreenLed.json()
            console.log(response)
            changeTitle("GreenLED is ON", 'g')
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    } else {
        try {
            const offGreenLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-green-led")
            const response = await offGreenLed.json()
            console.log(response)
            changeTitle("GreenLED is OFF")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    }
})

checkboxOnOffWhiteLed.addEventListener('click', async () => {
    if (checkboxOnOffWhiteLed.checked) {
        try {
            const onWhiteLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-white-led")
            const response = await onWhiteLed.json()
            console.log(response)
            changeTitle("WhiteLED is ON")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    } else {
        try {
            const offWhiteLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-white-led")
            const response = await offWhiteLed.json()
            console.log(response)
            changeTitle("WhiteLED is OFF")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    }
})

checkboxOnOffOrangeLed.addEventListener('click', async () => {
    if (checkboxOnOffOrangeLed.checked) {
        try {
            const onOrangeLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-orange-led")
            const response = await onOrangeLed.json()
            console.log(response)
            changeTitle("OrangeLED is ON")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    } else {
        try {
            const offOrangeLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-orange-led")
            const response = await offOrangeLed.json()
            console.log(response)
            changeTitle("OrangeLED is OFF")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    }
})

checkboxOnOffYellowLed.addEventListener('click', async () => {
    if (checkboxOnOffYellowLed.checked) {
        try {
            const onYellowLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-yellow-led")
            const response = await onYellowLed.json()
            console.log(response)
            changeTitle("YellowLed is ON")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    } else {
        try {
            const offYellowLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-yellow-led")
            const response = await offYellowLed.json()
            console.log(response)
            changeTitle("YellowLED is OFF")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    }
})

checkboxOnOffPurpleLed.addEventListener('click', async () => {
    if (checkboxOnOffPurpleLed.checked) {
        try {
            const onPurpleLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-purple-led")
            const response = await onPurpleLed.json()
            console.log(response)
            changeTitle("PurpleLed is ON")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    } else {
        try {
            const offPurpleLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-purple-led")
            const response = await offPurpleLed.json()
            console.log(response)
            changeTitle("PurpleLED is OFF")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    }
})

checkboxOnOffBlueLed.addEventListener('click', async () => {
    if (checkboxOnOffBlueLed.checked) {
        try {
            const onBlueLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-blue-led")
            const response = await onBlueLed.json()
            console.log(response)
            changeTitle("BlueLED is ON", 'b')
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    } else {
        try {
            const offBlueLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-blue-led")
            const response = await offBlueLed.json()
            console.log(response)
            changeTitle("BlueLED is OFF")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    }
})

checkboxOnOffCooler.addEventListener('click', async () => {
    if (checkboxOnOffCooler.checked) {
        try {
            const onCooler = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-cooler")
            const response = await onCooler.json()
            console.log(response)
        } catch (error) {
            console.log(error)
        }
    } else {
        try {
            const offCooler = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-cooler")
            const response = await offCooler.json()
            console.log(response)
        } catch (error) {
            console.log(error)
        }
    }
})

checkboxOnOffHeatingElement.addEventListener('click', async () => {
    if (checkboxOnOffHeatingElement.checked) {
        try {
            const onHeatingElement = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-heating-element")
            const response = await onHeatingElement.json()
            console.log(response)
        } catch (error) {
            console.log(error)
        }
    } else {
        try {
            const offHeatingElement = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-heating-element")
            const response = await offHeatingElement.json()
            console.log(response)
        } catch (error) {
            console.log(error)
        }
    }
})

checkboxOnOffDcMotorForward.addEventListener('click', async () => {
    if (checkboxOnOffDcMotorForward.checked) {
        checkboxOnOffDcMotorBackward.disabled = true
        try {
            const onDcMotorForward = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-dc-motor-forward")
            const response = await onDcMotorForward.json()
            console.log(response)
        } catch (error) {
            console.log(error)
        }
    } else {
        checkboxOnOffDcMotorBackward.disabled = false
        try {
            const offDcMotorForward = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-dc-motor-forward")
            const response = await offDcMotorForward.json()
            console.log(response)
        } catch (error) {
            console.log(error)
        }
    }
})

checkboxOnOffDcMotorBackward.addEventListener('click', async () => {
    if (checkboxOnOffDcMotorBackward.checked) {
        checkboxOnOffDcMotorForward.disabled = true
        try {
            const onDcMotorBackward = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-dc-motor-backward")
            const response = await onDcMotorBackward.json()
            console.log(response)
        } catch (error) {
            console.log(error)
        }
    } else {
        checkboxOnOffDcMotorForward.disabled = false
        try {
            const offDcMotorBackward = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-dc-motor-backward")
            const response = await offDcMotorBackward.json()
            console.log(response)
        } catch (error) {
            console.log(error)
        }
    }
})

checkboxOnOffHumidifier.addEventListener('click', async () => {
    if (checkboxOnOffHumidifier.checked) {
        try {
            const onHumidifier = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-humidifier")
            const response = await onHumidifier.json()
            console.log(response)
        } catch (error) {
            console.log(error)
        }
    } else {
        try {
            const offHumidifier = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-humidifier")
            const response = await offHumidifier.json()
            console.log(response)
        } catch (error) {
            console.log(error)
        }
    }
})

shutdown.addEventListener('click', async () => {
    if (window.confirm('Are you sure?')) {
        document.body.style.cssText = "display: flex;justify-content: center;align-items: center;font-size: 40px;"
        document.body.innerHTML = ""
        const div = document.createElement('div')
        div.className = "div-disconnected"
        div.innerHTML = `Disconnected at ${new Date().toISOString().split('T')[0]} ${new Date().toTimeString().split(' ')[0]}`
        document.body.appendChild(div)
        try {
            const shutdownRaspberryPi = await fetch("https://hippo-immense-plainly.ngrok-free.app/shutdown")
            const response = await shutdownRaspberryPi.json()
            console.log(response)
        } catch (err) {
            console.log(err)
        }
    }
})

btnEndpoints.addEventListener('click', async () => {
    try {
        const getAllAPIEndpoints = await fetch("https://hippo-immense-plainly.ngrok-free.app/endpoints")
        const response = await getAllAPIEndpoints.json()
        console.log(response)

        const h3Endpoints = document.getElementById("h3-endpoints").style.display = 'none'
        btnEndpoints.style.display = 'none'

        for (let item of response.routes) {
            let api_url = `https://hippo-immense-plainly.ngrok-free.app${item}`
            const url = document.createElement('a')
            url.setAttribute('href', `${api_url}`)
            url.target = '_blank'
            url.innerHTML = item
            divEndpoints.appendChild(url)
        }
    } catch (err) {
        console.log(err)
    }
})

setInterval(async () => {
    if (!document.querySelector(".div-disconnected")) {
        await tempHumSensor()
    }
}, 10_000)
setInterval(async () => {
    if (!document.querySelector(".div-disconnected")) {
        await lidStatus()
    }
}, 10_000)
