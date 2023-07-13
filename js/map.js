
const map = L.map('map').setView([39.8376017, -4.3978819], 6);
L.tileLayer.provider('CartoDB.Voyager').addTo(map);

const markers = [];

d3.csv("/data/data-geocoded.csv", (data) => {
    const marker = L.marker([data.lat, data.lng]).addTo(map);
    markers.push(marker);
})