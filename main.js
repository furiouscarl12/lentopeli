"use strict";

const currNameTag = document.getElementById('name');
const currCountryTag = document.getElementById('current country');
const destNameTag = document.getElementById('name');
const destCountryTag = document.getElementById('country');
const turnTag = document.getElementById('turn');
const airportsTag = document.getElementById('airports');
const map = L.map('map').setView([0, 0], 2);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);




async function main() {
    const dest = await fetchTimes('dest', 3, 'destination');

    console.log('Destination:');
    console.dir(dest);

    destNameTag.innerText = dest['airport_name'];
    destCountryTag.innerText = dest['country_name'];


    const currentData = await fetchTimes('current', 3, 'current data');
    if (!currentData || Object.keys(currentData).length === 0) { return; }

    console.log('Current data:');
    console.dir(currentData);

    let {'current': curr, airports, dist, turn, 'total_km': totalKm,'total_co2': totalCO2} = currentData;

    updateHeader(curr, turn, totalKm, totalCO2);
    updateAirportsList(airports);

    map.panTo(([curr['lat'], curr['long']]));

    const markerCurr = L.marker([curr['lat'], curr['long']]).addTo(map);
    const markerDest = L.marker([dest['lat'], dest['long']]).addTo(map);

    airportsTag.addEventListener('mouseover', (event) => {
        map.zoomIn(3);
    }, {once : true});
}

main();


function fetchFrom(url, resource) {
    const promise = fetch(String(url))
        .then((response) => {
            return response.json();
        })
        .catch((error) => {
            console.error(`Failed to fetch ${String(resource)}. Error: ${error.message}`);
        });
    return promise;


}

function updateAirportsList(airports) {
    const frag = new DocumentFragment;
    const liItems = [];
    let marker, markersel;

function updateHeader(curr, turn, totalKm,) {
    currNameTag.innerText = curr['airport_name'];
    turnTag.innerText = ` ${turn}`;
    currCountryTag.innerText = curr['country_name'];




        name.classList.add('airport-name');
        type.classList.add('airport-type');
        country.classList.add('airport-country');
        direction.classList.add('airport-direction');
        dist.classList.add('airport-dist');
  Array.from(airports).forEach((airport) => {
        const name = document.createElement('span');
        const country = document.createElement('span');
        const direction = document.createElement('span');
        const type = document.createElement('span');
        const dist = document.createElement('span');
        name.innerText = airport['airport_name'];
        type.innerText = airport['type'].split('_').join(' ');
        country.innerText = 'in ' + airport['country_name'] + ',';
        direction.innerText = 'in ' + airport['direction'] + ' direction,';
        dist.innerText = String(Math.round(airport['distance'])) + ' km päässä.';

        li.addEventListener('mouseover', (event) => {
            marker = L.marker([airport['lat'], airport['long']]).addTo(map);
            marker._icon.style.filter = "hue-rotate(200deg)";
        });

        li.addEventListener('mouseout', (event) => {
            marker.remove();
        });


            if (markersel) {
                markersel.remove();
            }

        });

        li.append(name, type, country, direction, dist, co2);
        liItems.push(li);
        frag.append(li);}}
