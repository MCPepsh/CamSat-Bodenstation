const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
const tileUrlNative = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const tileUrlGoogle = 'http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}';
const mymap = L.map('mapid');
mymap.setMaxZoom(18);

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
zoomIn.oninput = function() {
  zoomOut.innerHTML = this.value;
  zoom = this.value;
  mymap.setZoom(zoom);
}

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
tilesIn.oninput = function() {
  switch (this.value) {
    case "0":
      tilesOut.innerHTML = "OSM";
      tiles = L.tileLayer(tileUrlNative, {
        attribution
      });
      tiles.addTo(mymap);
      mymap.setZoom(zoom)
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
}


//var marker = L.marker([41.40338, 2.17403]).addTo(mymap);

fetch("../Daten/aktuelledaten.txt")
  .then(function(resp) {
    return resp.text()
      .then(function(data) {
        //console.log(data);
        data = data.split("\n");
        //console.log(data);
        var pre_latlng = convert(data[0]);
        var akt_latlng = convert(data[1]);
        /*//data[data.length - 3] = data[data.length - 3].split(", ");
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
        //var latlng = L.latLng(data[data.length - 2]);
        */


        mymap.setView(pre_latlng, zoom);
        /*var tiles = L.tileLayer(tileUrlNative, {
          attribution
        });
        tiles.addTo(mymap);*/



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
  });


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

//mymap.on('click', onMapClick);

//var marker = L.marker("[" + getDaten() + "]").addTo(mymap);
