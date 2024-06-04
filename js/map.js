
const map = L.map('map', {
}).setView([39.8376017, -4.3978819], 6);

L.tileLayer.provider('CartoDB.Voyager').addTo(map);

const markers = [];

let popup = null;

function onClick(e) {
   var popup = e.target.getPopup();
   var content = popup.getContent();
   console.log(content);
}

d3.csv("data/data-geocoded.csv", (data) => {
    const marker = L.marker([data.lat, data.lng])
    marker.addTo(map);
    marker.bindPopup(`<a href="${data.form}" target="_blank" rel="noopener noreferrer">Únete a este grupo de Amigas de Sumar</a>`);
    markers.push(marker);
})
