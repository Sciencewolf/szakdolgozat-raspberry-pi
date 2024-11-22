const checkboxOnOffRedLed = document.getElementById("checkbox-on-off-red-led")
const checkboxOnOffGreenLed = document.getElementById("checkbox-on-off-green-led")
const checkboxOnOffBlueLed = document.getElementById("checkbox-on-off-blue-led")
const checkboxOnOffYellowLed = document.getElementById("checkbox-on-off-yellow-led")
const checkboxOnOffAllLed = document.getElementById("checkbox-on-off-all-led")
const temperature = document.getElementById("temp")
const humidity = document.getElementById("hum")
const lid = document.getElementById("lid")
const checkboxOnOffCooler = document.getElementById("checkbox-on-off-cooler")
const checkboxOnOffHeatingElement = document.getElementById("checkbox-on-off-heating-element")
const shutdown = document.getElementById("btn-shutdown")
const btnEndpoints = document.getElementById("btn-endpoints")
const divEndpoints = document.getElementById("div-endpoints")

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
    values.set("a", "../static/images/all-led.png")
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
        checkboxOnOffGreenLed.disabled = true
        checkboxOnOffBlueLed.disabled = true
        checkboxOnOffAllLed.disabled = true

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
        checkboxOnOffGreenLed.disabled = false
        checkboxOnOffBlueLed.disabled = false
        checkboxOnOffAllLed.disabled = false

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
        checkboxOnOffRedLed.disabled = true
        checkboxOnOffBlueLed.disabled = true
        checkboxOnOffAllLed.disabled = true

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
        checkboxOnOffRedLed.disabled = false
        checkboxOnOffBlueLed.disabled = false
        checkboxOnOffAllLed.disabled = false

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

checkboxOnOffBlueLed.addEventListener('click', async () => {
    if (checkboxOnOffBlueLed.checked) {
        checkboxOnOffRedLed.disabled = true
        checkboxOnOffGreenLed.disabled = true
        checkboxOnOffAllLed.disabled = true

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
        checkboxOnOffRedLed.disabled = false
        checkboxOnOffGreenLed.disabled = false
        checkboxOnOffAllLed.disabled = false

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

checkboxOnOffYellowLed.addEventListener('click', async () => {
    if (checkboxOnOffYellowLed.checked) {
        try {
            const onYellowLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-yellow-led")
            const response = await onYellowLed.json()
            console.log(response)
            changeTitle("YellowLed is ON", 'y')
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    } else {
        try {
            const offAllLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-yellow-led")
            const response = await offAllLed.json()
            console.log(response)
            changeTitle("YellowLED is OFF")
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    }
})

checkboxOnOffAllLed.addEventListener('click', async () => {
    if (checkboxOnOffAllLed.checked) {
        checkboxOnOffRedLed.disabled = true
        checkboxOnOffGreenLed.disabled = true
        checkboxOnOffBlueLed.disabled = true

        try {
            const onAllLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-all-led")
            const response = await onAllLed.json()
            console.log(response)
            changeTitle("AllLed is ON", 'a')
        } catch (error) {
            console.log(error)
            changeTitle("Error", 'e')
        }
    } else {
        checkboxOnOffRedLed.disabled = false
        checkboxOnOffGreenLed.disabled = false
        checkboxOnOffBlueLed.disabled = false

        try {
            const offAllLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-all-led")
            const response = await offAllLed.json()
            console.log(response)
            changeTitle("AllLED is OFF")
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
            const onCooler = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-heating-element")
            const response = await onCooler.json()
            console.log(response)
        } catch (error) {
            console.log(error)
        }
    } else {
        try {
            const offCooler = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-heating-element")
            const response = await offCooler.json()
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
    await tempHumSensor()
}, 10_000)
setInterval(async () => {
    await lidStatus()
}, 10_000)
