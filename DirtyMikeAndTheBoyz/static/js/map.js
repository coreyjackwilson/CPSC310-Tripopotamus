var time = 0;
var jsonObject = {};
var delay = 250;
var taxiPrice;
var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
var destinationIcon = 'https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=D|FF0000|000000';
var originIcon = 'https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=O|FFFF00|000000';
var lat;
var long;
var endLat;
var endLong;
var distance;
var map;
var geocoder;
var bounds = new google.maps.LatLngBounds();
var markersArray = [];


function initialize() {
    directionsDisplay = new google.maps.DirectionsRenderer();
    var opts = {
        scrollwheel: false,
        center: new google.maps.LatLng(47.619939, -122.323889),
        zoom: 13
    };
    map = new google.maps.Map(document.getElementById('map-canvas'), opts);

    directionsDisplay.setMap(map);

    geocoder = new google.maps.Geocoder();

    var control = document.getElementById('control');

    control.style.display = 'block';

    map.controls[google.maps.ControlPosition.TOP_CENTER].push(control);
}

function onClick() {
    geocodeAddress();
    geocodeEndAddress();
    calculateDistances();
    setTimeout(function () {
        showCars();
    }, delay); //to solve double click bug
}

function geocodeAddress() {
    var address = document.getElementById('curr').value;

    geocoder.geocode({'address': address},
        function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                map.setCenter(results[0].geometry.location);
                lat = Number(results[0].geometry.location.lat());
                long = Number(results[0].geometry.location.lng());
                var marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location
                });
                markersArray.push(marker);
            } else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
}

function geocodeEndAddress() {
    var address = document.getElementById('dest').value;

    geocoder.geocode({'address': address},
        function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                map.setCenter(results[0].geometry.location);
                endLat = Number(results[0].geometry.location.lat());
                endlong = Number(results[0].geometry.location.lng());
                var marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location
                });
                markersArray.push(marker);
            } else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
}

function calculateDistances() {
    var curr = document.getElementById('curr');
    var dest = document.getElementById('dest');
    start = String(curr.value);
    end = String(dest.value);
    var service = new google.maps.DistanceMatrixService();

    service.getDistanceMatrix({
        origins: [curr.value],
        destinations: [dest.value],
        travelMode: google.maps.TravelMode.DRIVING,
        unitSystem: google.maps.UnitSystem.METRIC,
        avoidHighways: false,
        avoidTolls: false,
        durationInTraffic: true,
    }, callback);

    var request = {
        origin: curr.value,
        destination: dest.value,
        travelMode: google.maps.TravelMode.DRIVING
    };

    directionsService.route(request,
        function (response, status) {
            if (status == google.maps.DirectionsStatus.OK) {
                directionsDisplay.setDirections(response);
            }
        });
}

function deleteOverlays() {
    if (markersArray) {
        for (i in markersArray) {
            markersArray[i].setMap(null);
        }
        markersArray.length = 0;
    }
}

function addMarker(location, isDestination) {
    var icon;
    if (isDestination) {
        icon = destinationIcon;
    } else {
        icon = originIcon;
    }
    geocoder.geocode({'address': location}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            bounds.extend(results[0].geometry.location);
            map.fitBounds(bounds);
            var marker = new google.maps.Marker({
                map: map,
                position: results[0].geometry.location,
                icon: icon
            });
            markersArray.push(marker);
        } else {
            alert('Geocode was not successful for the following reason: '
                + status);
        }
    });
}

function callback(response, status) {
    if (status != google.maps.DistanceMatrixStatus.OK) {
        alert('Error was: ' + status);
    } else {
        var origins = response.originAddresses;
        var destinations = response.destinationAddresses;
        deleteOverlays();

        for (var i = 0; i < origins.length; i++) {
            var results = response.rows[i].elements;
            addMarker(origins[i], false);
            for (var j = 0; j < results.length; j++) {
                addMarker(destinations[j], true);
                distance = results[j].distance.value;
                distance = distance * 0.000621371;
            }
        }
    }
}

google.maps.event.addDomListener(window, 'load', initialize);

