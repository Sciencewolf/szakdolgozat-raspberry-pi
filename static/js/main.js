const checkboxOnOffRedLed = document.getElementById("checkbox-on-off-red-led")
const checkboxOnOffGreenLed = document.getElementById("checkbox-on-off-green-led")
const checkboxOnOffBlueLed = document.getElementById("checkbox-on-off-blue-led")
const checkboxOnOffAllLed = document.getElementById("checkbox-on-off-all-led")
const temperature = document.getElementById("temp")
const humidity = document.getElementById("hum")

const tempHumSensor = async () => {
    const getTemperatureAndHumidity = await fetch("https://hippo-immense-plainly.ngrok-free.app/get-temp-hum")
    const response = await getTemperatureAndHumidity.json()
    console.log(response)
    temperature.innerHTML = response.temp
    humidity.innerHTML = response.hum
}

window.addEventListener("load", async () => {
    await tempHumSensor()
})

checkboxOnOffRedLed.addEventListener('click', async () => {
    if (checkboxOnOffRedLed.checked) {
        checkboxOnOffGreenLed.disabled = true
        checkboxOnOffBlueLed.disabled = true
        checkboxOnOffAllLed.disabled = true
        const onRedLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-red-led")
        const response = await onRedLed.json()
        console.log(response)
    }
    else {
        checkboxOnOffGreenLed.disabled = false
        checkboxOnOffBlueLed.disabled = false
        checkboxOnOffAllLed.disabled = false
        const offRedLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-red-led")
        const response = await offRedLed.json()
        console.log(response)
    }
})

checkboxOnOffGreenLed.addEventListener('click', async () => {
    if (checkboxOnOffGreenLed.checked) {
        checkboxOnOffRedLed.disabled = true
        checkboxOnOffBlueLed.disabled = true
        checkboxOnOffAllLed.disabled = true
        const onGreenLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-green-led")
        const response = await onGreenLed.json()
        console.log(response)
    }
    else {
        checkboxOnOffRedLed.disabled = false
        checkboxOnOffBlueLed.disabled = false
        checkboxOnOffAllLed.disabled = false
        const offGreenLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-green-led")
        const response = await offGreenLed.json()
        console.log(response)
    }
})

checkboxOnOffBlueLed.addEventListener('click', async () => {
    if (checkboxOnOffBlueLed.checked) {
        checkboxOnOffRedLed.disabled = true
        checkboxOnOffGreenLed.disabled = true
        checkboxOnOffAllLed.disabled = true
        const onBlueLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-blue-led")
        const response = await onBlueLed.json()
        console.log(response)
    }
    else {
        checkboxOnOffRedLed.disabled = false
        checkboxOnOffGreenLed.disabled = false
        checkboxOnOffAllLed.disabled = false
        const offBlueLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-blue-led")
        const response = await offBlueLed.json()
        console.log(response)
    }
})

checkboxOnOffAllLed.addEventListener('click', async () => {
    if (checkboxOnOffAllLed.checked) {
        checkboxOnOffRedLed.disabled = true
        checkboxOnOffGreenLed.disabled = true
        checkboxOnOffBlueLed.disabled = true
        const onAllLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/on-all-led")
        const response = await onAllLed.json()
        console.log(response)
    }
    else {
        checkboxOnOffRedLed.disabled = false
        checkboxOnOffGreenLed.disabled = false
        checkboxOnOffBlueLed.disabled = false
        const offAllLed = await fetch("https://hippo-immense-plainly.ngrok-free.app/off-all-led")
        const response = await offAllLed.json()
        console.log(response)
    }
})

setInterval(async () => {
    await tempHumSensor()
    console.log("interval")
}, 10000)
