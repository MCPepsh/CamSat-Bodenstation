var attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
var tileUrlNative = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var tileUrlGoogle = 'http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}';
var mymap = L.map('mapid');
mymap.setMaxZoom(18);
//var marker = L.marker([0, 0]).addTo(mymap);
var marker;
var CamSatLinie;
var CamSatIcon = L.icon({
  iconUrl: "./Camsat.png",
  iconSize: [40, 40],
  iconAnchor: [12, 20]
});
var CamSatIconKlein = L.icon({
  iconUrl: "./Camsat.png",
  iconSize: [20, 20],
  iconAnchor: [6, 10]
});

var telePos = L.latLng([51.86180087076521, 7.70742416381836]); //51.85465448129371, 7.660903930664063
var teleskop = L.marker(telePos).addTo(mymap);
var teleVec = [1, 1];
var startZeit = Date.now();
L.polyline([telePos, L.latLng([51.86180087076521, 8.70742416381836])], {
  weight: 1
}).addTo(mymap);
L.polyline([telePos, L.latLng([52.86180087076521, 7.70742416381836])], {
  weight: 1
}).addTo(mymap);
L.polyline([telePos, L.latLng([52.86180087076521, 8.70742416381836])], {
  weight: 1
}).addTo(mymap);
var teleLinie;


/*ehemalige Mapssachen*/
/*const mymap = L.map('mapid').setView(pre_latlng, 17);
var tiles = L.tileLayer(tileUrlNative, {
  attribution
});
//tiles = L.tileLayer(tileUrlGoogle, {
//  maxZoom: 20,
//  subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
//});
tiles.addTo(mymap);
*/

var zoomIn = document.getElementById("zoomIn");
var zoomOut = document.getElementById("zoomOut");
zoomOut.innerHTML = zoomIn.value;
zoom = zoomIn.value;
zoomIn.oninput = function () {
  zoomOut.innerHTML = this.value;
  zoom = this.value;
  mymap.setZoom(zoom);
};

var tilesIn = document.getElementById("tilesIn");
var tilesOut = document.getElementById("tilesOut");
switch (tilesIn.value) {
  case "0":
    tilesOut.innerHTML = "OSM";
    tiles = L.tileLayer(tileUrlNative, {
      attribution
    });
    tiles.addTo(mymap);
    break;
  case "1":
    tilesOut.innerHTML = "Google Maps";
    tiles = L.tileLayer(tileUrlGoogle, {
      maxZoom: 20,
      subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    });
    tiles.addTo(mymap);
    break;
}
tilesIn.oninput = function () {
  switch (this.value) {
    case "0":
      tilesOut.innerHTML = "OSM";
      tiles = L.tileLayer(tileUrlNative, {
        attribution
      });
      tiles.addTo(mymap);
      mymap.setZoom(zoom);
      break;
    case "1":
      tilesOut.innerHTML = "Google Maps";
      tiles = L.tileLayer(tileUrlGoogle, {
        maxZoom: 18,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
      });
      tiles.addTo(mymap);
      mymap.setZoom(zoom);
      break;
  }
};

var locationOut = document.getElementById("location");
var DASOut = document.getElementById("distanceAndSpeed");
var winkelOut = document.getElementById("winkel");


setInterval(getGPS, 1000);

async function getGPS() {
  var resp = await fetch("./aktuelledaten.txt");
  var data = await resp.text();
  //console.log(data);
  data = data.split("\n");
  data[0] = data[0].split(",");
  data[1] = data[1].split(",");
  //console.log(data);
  var pre_latlng = L.latLng(data[0]);
  var akt_latlng = L.latLng(data[1]);
  var pre_height = data[0][2];
  var akt_height = data[1][2];
  locationOut.innerHTML = data[0] + "<br>" + data[1];
  console.log(toHEX(akt_height));


  mymap.setView(pre_latlng, zoom);


  //var latlng = L.latLng(data);
  //console.log(latlng);
  //mymap.setView(latlng, 11);
  //var marker = L.marker(akt_latlng).addTo(mymap);
  mymap.panTo(akt_latlng, {
    animate: true,
    duration: 0.5,
    easeLinearity: 0.5
  });
  if (marker != null) {
    marker.setOpacity(0.0); //0.75
    marker.setIcon(CamSatIconKlein);
  }
  marker = L.marker(akt_latlng, {
    icon: CamSatIcon
  }).addTo(mymap);

  CamSatLinie = L.polyline([pre_latlng, akt_latlng], {
    weight: 2,
    color: toHEX(akt_height)
  }).addTo(mymap);

  var aktZeit = Date.now();
  var millis = aktZeit - startZeit;
  startZeit = aktZeit;

  var dist = telePos.distanceTo(akt_latlng);
  var speed = (akt_latlng.distanceTo(pre_latlng)) / (millis / 1000);
  //console.log(millis);
  DASOut.innerHTML = "distance: " + dist + " m<br>" + "speed: " + speed + " m/s";

  var vector = [akt_latlng["lat"] - telePos["lat"], akt_latlng["lng"] - telePos["lng"]];
  //var winkel = (vector[0] * teleVec[0] + vector[1] * teleVec[1]) / (Math.sqrt(vector[0] * vector[0] + vector[1] * vector[1]) * Math.sqrt(teleVec[0] * teleVec[0] + teleVec[1] * teleVec[1]));
  var winkel = Math.atan2(vector[1], vector[0]) - Math.atan2(teleVec[1], teleVec[0]);
  if (teleLinie != null) {
    teleLinie.setLatLngs([telePos, akt_latlng]);
  } else {
    teleLinie = L.polyline([telePos, akt_latlng]).addTo(mymap);
  }
  //console.log(vector, teleVec);
  winkelOut.innerHTML = (winkel / (2 * Math.PI)) * 360 + "°";

  //pre_latlng = latlng;
  //mymap.panTo(L.latLng(["51 55.7080", "7 42.4452"]), 11);
  //marker.setLatLng(L.latLng(["51 55.7080", "7 42.4452"]));
  //return resp[resp.length - 1];

}

//var marker = L.marker([41.40338, 2.17403]).addTo(mymap);

/*fetch("../Daten/aktuelledaten.txt")
  .then(function(resp) {
    return resp.text()
      .then(function(data) {
        //console.log(data);
        data = data.split("\n");
        //console.log(data);
        var pre_latlng = convert(data[0]);
        var akt_latlng = convert(data[1]);
        /* //data[data.length - 3] = data[data.length - 3].split(", ");
        //data[data.length - 2] = data[data.length - 2].split(", ");
        pre_latlng = pre_latlng.split(", ");
        akt_latlng = akt_latlng.split(", ");
        //console.log(data);
        pre_latlng[0] = pre_latlng[0].split(" ");
        pre_latlng[1] = pre_latlng[1].split(" ");
        akt_latlng[0] = akt_latlng[0].split(" ");
        akt_latlng[1] = akt_latlng[1].split(" ");
        //data[0] = data[0].split(" ");
        //data[1] = data[1].split(" ");
        //console.log(data);
        data[0][1] /= 60;
        data[1][1] /= 60;
        data[0] = Number(data[0][0]) + Number(data[0][1]);
        data[1] = Number(data[1][0]) + Number(data[1][1]);
        //console.log(data);
        //console.log(data[data.length - 2]);
        //console.log(data[data.length - 2]);
        //var latlng_pre = L.latLng(data[data.length - 3]);
        //var latlng = L.latLng(data[data.length - 2]);* /



        mymap.setView(pre_latlng, zoom);
        /*var tiles = L.tileLayer(tileUrlNative, {
          attribution
        });
        tiles.addTo(mymap);* /



        //var latlng = L.latLng(data);
        //console.log(latlng);
        //mymap.setView(latlng, 11);
        var marker = L.marker(akt_latlng).addTo(mymap);
        mymap.panTo(akt_latlng);
        marker.setLatLng(akt_latlng);
        //pre_latlng = latlng;
        //mymap.panTo(L.latLng(["51 55.7080", "7 42.4452"]), 11);
        //marker.setLatLng(L.latLng(["51 55.7080", "7 42.4452"]));
        //return resp[resp.length - 1];
      });
  });*/


function convert(data) {
  //console.log(data);
  data = data.split(",");
  //console.log(data[0] + " " + data[1]);
  return L.latLng(data);
}


function onMapClick(e) {
  //alert("You clicked the map at " + e.latlng);
  //marker = L.marker(e.latlng).addTo(mymap);
  console.log(e.latlng["lat"] + ", " + e.latlng["lng"]);
  console.log(e.latlng);
  marker.setLatLng(e.latlng);
}

mymap.on('click', onMapClick);

function toHEX(height) {
  r = Math.round((height / 1000.0) * 255);
  g = Math.round((1 - (height / 1000.0)) * 255);
  b = 0;
  r = componentToHex(r);
  g = componentToHex(g);
  b = componentToHex(b);
  return "#" + r + g + b;
}

function componentToHex(c) {
  var hex = c.toString(16);
  return hex.length == 1 ? "0" + hex : hex;
}

//var marker = L.marker("[" + getDaten() + "]").addTo(mymap);