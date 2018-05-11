function createMap(mapObj) {
    var mapID = mapObj.bindto.slice(1); // without #
    var myDiv = document.getElementById(mapID);

    document.getElementById(mapID).style.height = mapObj.data.mapstyle.height;

    var mymap = L.map(mapID).setView([mapObj.data.mapview.lat, mapObj.data.mapview.lng], mapObj.data.mapview.zoom);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoid3V5bTA0MDQiLCJhIjoiY2pmb3U2emI3MDI4YzJ3cGhnMXZtcGdzNyJ9.T1hePH1dt3y5s85vb2PJEw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
            '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="http://mapbox.com">Mapbox</a>',
        id: 'mapbox.comic'
    }).addTo(mymap);

    var airplane = L.marker([38.990895, -76.942331])
    airplane.addTo(mymap)

    chartMap.set(mapObj.bindto, new chartWrapper(mapObj, mymap, {marker: airplane}));
}

function updateMarker(updateWrapper, updateObj) {
    var mymap = updateWrapper.c3chart;
    var marker = updateWrapper.dataCol.marker

    var newlatlng = L.latLng(updateObj.data.lat, updateObj.data.lng);
    marker.setLatLng(newlatlng);
}