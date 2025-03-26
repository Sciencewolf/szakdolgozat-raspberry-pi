import {Cooler, HeatingElement, LED, Motor, Sensor, Health} from "./utils.mjs";

const checkboxOnOffRedLed = document.getElementById("checkbox-on-off-red-led")
const checkboxOnOffGreenLed = document.getElementById("checkbox-on-off-green-led")
const checkboxOnOffWhiteLed = document.getElementById("checkbox-on-off-white-led")
const checkboxOnOffYellowLed = document.getElementById("checkbox-on-off-yellow-led")
const checkboxOnOffColdWhiteLed = document.getElementById("checkbox-on-off-cold-white-led")
const checkboxOnOffBlueLed = document.getElementById("checkbox-on-off-blue-led")

const temperature = document.getElementById("temp")
const humidity = document.getElementById("hum")
const lid = document.getElementById("lid")
const cpu = document.getElementById("cpu")
const totalRam = document.getElementById("total-ram")
const ramApp = document.getElementById("ram-app")
const vram = document.getElementById("vram")

const checkboxOnOffCooler = document.getElementById("checkbox-on-off-cooler")
const checkboxOnOffHeatingElement = document.getElementById("checkbox-on-off-heating-element")
const checkboxOnOffEngineForward = document.getElementById("checkbox-on-off-dc-motor-forward")
const checkboxOnOffEngineBackward = document.getElementById("checkbox-on-off-dc-motor-backward")

const btnEndpoints = document.getElementById("btn-endpoints")
const divEndpoints = document.getElementById("div-endpoints")

const shutdown = document.getElementById("btn-shutdown")


const tempHumSensor = async () => {
    try {
        const [temp, hum] = await Sensor.getTemperatureAndHumidity()
        temperature.innerHTML = await temp
        humidity.innerHTML = await hum
        sessionStorage.setItem("error", "false")
    } catch (error) {
        sessionStorage.setItem('error', 'true')
        console.log(error);
    }
}

const lidStatus = async () => {
    try {
        const _lid = await Sensor.getLidStatus()
        lid.innerHTML = await _lid
        sessionStorage.setItem("error", "false")
    } catch (error) {
        sessionStorage.setItem('error', 'true')
        console.log(error);
    }
}

const isAlive = async () => {
    try {
        const response = await Health.isRaspiAlive()

        if(response) {
            window.location.href = "/"
        }
    } catch (err) {
        console.log(err);
    }
}

const getHealth = async () => {
    try {
        const getAllData = await Health.getAll()

        cpu.innerHTML = getAllData[0] + " %"
        totalRam.innerHTML = getAllData[1] + " %"
        ramApp.innerHTML = getAllData[2] + " MB"
        vram.innerHTML = getAllData[3] + " MB"
    } catch (err) {
        console.log(err)
    }
}

const changeTitle = (title, iconType = "d") => {
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
            await LED.onRedLed()
            changeTitle("RedLED is ON", 'r')
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    } else {
        try {
            await LED.offRedLed()
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
            await LED.onGreenLed()
            changeTitle("GreenLED is ON", 'g')
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    } else {
        try {
            await LED.offGreenLed()
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
            await LED.onWhiteLed()
            changeTitle("WhiteLED is ON")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    } else {
        try {
            await LED.offWhiteLed()
            changeTitle("WhiteLED is OFF")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    }
})

checkboxOnOffYellowLed.addEventListener('click', async () => {
    if (checkboxOnOffYellowLed.checked) {
        try {
            await LED.onYellowLed()
            changeTitle("YellowLed is ON")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    } else {
        try {
            await LED.offYellowLed()
            changeTitle("YellowLED is OFF")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    }
})

checkboxOnOffColdWhiteLed.addEventListener('click', async () => {
    if (checkboxOnOffColdWhiteLed.checked) {
        try {
            await LED.onColdWhiteLed()
            changeTitle("ColdWhiteLed is ON")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    } else {
        try {
            await LED.offColdWhiteLed()
            changeTitle("ColdWhiteLED is OFF")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    }
})

checkboxOnOffBlueLed.addEventListener('click', async () => {
    if (checkboxOnOffBlueLed.checked) {
        try {
            await LED.onBlueLed()
            changeTitle("BlueLED is ON", 'b')
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    } else {
        try {
            await LED.offBlueLed()
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
            await Cooler.onCooler()
        } catch (error) {
            console.log(error)
        }
    } else {
        try {
            await Cooler.offCooler()
        } catch (error) {
            console.log(error)
        }
    }
})

checkboxOnOffHeatingElement.addEventListener('click', async () => {
    if (checkboxOnOffHeatingElement.checked) {
        try {
            await HeatingElement.onHeatingElement()
        } catch (error) {
            console.log(error)
        }
    } else {
        try {
            await HeatingElement.offHeatingElement()
        } catch (error) {
            console.log(error)
        }
    }
})

checkboxOnOffEngineForward.addEventListener('click', async () => {
    if (checkboxOnOffEngineForward.checked) {
        checkboxOnOffEngineBackward.disabled = true
        try {
            await Motor.onEngineForward()
        } catch (error) {
            console.log(error)
        }
    } else {
        checkboxOnOffEngineBackward.disabled = false
        try {
            await Motor.offEngineForward()
        } catch (error) {
            console.log(error)
        }
    }
})

checkboxOnOffEngineBackward.addEventListener('click', async () => {
    if (checkboxOnOffEngineBackward.checked) {
        checkboxOnOffEngineForward.disabled = true
        try {
            await Motor.onEngineBackward()
        } catch (error) {
            console.log(error)
        }
    } else {
        checkboxOnOffEngineForward.disabled = false
        try {
            await Motor.offEngineBackward()
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
            const shutdownRaspberryPi = await fetch("https://harmless-toad-remarkably.ngrok-free.app/shutdown")
            const response = await shutdownRaspberryPi.json()
            console.log(response)
        } catch (err) {
            console.log(err)
        }
    }
})

btnEndpoints.addEventListener('click', async () => {
    try {
        const getAllAPIEndpoints = await fetch("https://harmless-toad-remarkably.ngrok-free.app/endpoints")
        const response = await getAllAPIEndpoints.json()
        console.log(response)

        document.getElementById("h3-endpoints").style.display = 'none'
        btnEndpoints.style.display = 'none'

        for (let item of response.other) {
            let api_url = `https://harmless-toad-remarkably.ngrok-free.app/${item}`
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

setInterval(() => {
    if(sessionStorage.getItem('error') === 'true') {
        document.body.style.cssText = "display: flex;justify-content: center;align-items: center;font-size: 40px;"
        document.body.innerHTML = ""
        const div = document.createElement('div')
        div.className = "div-disconnected"
        div.innerHTML = "RasPi/webserver is offline"
        document.body.appendChild(div)  
    }

}, 2_000)

setInterval(async () => {
    if (document.querySelector('.div-disconnected')) {
        await isAlive()
    }
}, 5_000)


setInterval(async () => {
    if (!document.querySelector(".div-disconnected")) {
        await tempHumSensor()
    }
}, 2_000)
setInterval(async () => {
    if (!document.querySelector(".div-disconnected")) {
        await lidStatus()
    }
}, 2_000)
setInterval(async() => {
    if (!document.querySelector(".div-disconnected")) {
        await getHealth()
    }
}, 5_000)
