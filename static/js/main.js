const checkboxOnOffRedLed = document.getElementById("checkbox-on-off-red-led")
const checkboxOnOffGreenLed = document.getElementById("checkbox-on-off-green-led")
const checkboxOnOffBlueLed = document.getElementById("checkbox-on-off-blue-led")
const checkboxOnOffAllLed = document.getElementById("checkbox-on-off-all-led")
const temperature = document.getElementById("temp")
const humidity = document.getElementById("hum")

window.addEventListener("load", async () => {
    const getTemperatureAndHumidity = await fetch("http://192.168.1.46:8080/get-temp-hum")
    const response = await getTemperatureAndHumidity.json()
    console.log(response)
    temperature.innerHTML = response.temp
    humidity.innerHTML = response.hum
})

checkboxOnOffRedLed.addEventListener('click', async () => {
    if (checkboxOnOffRedLed.checked) {
        checkboxOnOffGreenLed.disabled = true
        checkboxOnOffBlueLed.disabled = true
        checkboxOnOffAllLed.disabled = true
        const onRedLed = await fetch("http://192.168.1.46:8080/on-red-led")
        const response = await onRedLed.json()
        console.log(response)
    }
    else {
        checkboxOnOffGreenLed.disabled = false
        checkboxOnOffBlueLed.disabled = false
        checkboxOnOffAllLed.disabled = false
        const offRedLed = await fetch("http://192.168.1.46:8080/off-red-led")
        const response = await offRedLed.json()
        console.log(response)
    }
})

checkboxOnOffGreenLed.addEventListener('click', async () => {
    if (checkboxOnOffGreenLed.checked) {
        checkboxOnOffRedLed.disabled = true
        checkboxOnOffBlueLed.disabled = true
        checkboxOnOffAllLed.disabled = true
        const onGreenLed = await fetch("http://192.168.1.46:8080/on-green-led")
        const response = await onGreenLed.json()
        console.log(response)
    }
    else {
        checkboxOnOffRedLed.disabled = false
        checkboxOnOffBlueLed.disabled = false
        checkboxOnOffAllLed.disabled = false
        const offGreenLed = await fetch("http://192.168.1.46:8080/off-green-led")
        const response = await offGreenLed.json()
        console.log(response)
    }
})

checkboxOnOffBlueLed.addEventListener('click', async () => {
    if (checkboxOnOffBlueLed.checked) {
        checkboxOnOffRedLed.disabled = true
        checkboxOnOffGreenLed.disabled = true
        checkboxOnOffAllLed.disabled = true
        const onBlueLed = await fetch("http://192.168.1.46:8080/on-blue-led")
        const response = await onBlueLed.json()
        console.log(response)
    }
    else {
        checkboxOnOffRedLed.disabled = false
        checkboxOnOffGreenLed.disabled = false
        checkboxOnOffAllLed.disabled = false
        const offBlueLed = await fetch("http://192.168.1.46:8080/off-blue-led")
        const response = await offBlueLed.json()
        console.log(response)
    }
})

checkboxOnOffAllLed.addEventListener('click', async () => {
    if (checkboxOnOffAllLed.checked) {
        checkboxOnOffRedLed.disabled = true
        checkboxOnOffGreenLed.disabled = true
        checkboxOnOffBlueLed.disabled = true
        const onAllLed = await fetch("http://192.168.1.46:8080/on-all-led")
        const response = await onAllLed.json()
        console.log(response)
    }
    else {
        checkboxOnOffRedLed.disabled = false
        checkboxOnOffGreenLed.disabled = false
        checkboxOnOffBlueLed.disabled = false
        const offAllLed = await fetch("http://192.168.1.46:8080/off-all-led")
        const response = await offAllLed.json()
        console.log(response)
    }
})
