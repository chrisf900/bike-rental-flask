async function reloadMap(latitude, longitude) {
    const formData = new FormData();
    formData.append("latitude", latitude);
    formData.append("longitude", longitude);
    let data = await sendCoordinates(formData);
    loadMap(data);
}

async function getCurrentPosition() {
    let response = await fetch("https://api.geoapify.com/v1/ipinfo?&apiKey=33ef07b629534cadad433b073ae0b1b6", { method: "GET" });
    if (response.ok) {
        return response.json();
    } else {
        console.error("error", response.error);
    }
}