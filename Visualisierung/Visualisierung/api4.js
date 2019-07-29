var Stadtteile = [];
var Stadtteile_Poly = [];
var daten = [];
var min_CO2 = -1;
var max_CO2 = -1;
var min_NOx = -1;
var max_NOx = -1;
var min_Fei = -1;
var max_Fei = -1;
var deckkraftIn = document.getElementById("deckkraftIn");
var deckkraftOut = document.getElementById("deckkraftOut");
deckkraftOut.innerHTML = deckkraftIn.value;
deckkraft = deckkraftIn.value;

var anzeigeIn = document.getElementById("anzeigeIn");
var anzeigeOut = document.getElementById("anzeigeOut");
anzeige = anzeigeIn.value;
switch (anzeigeIn.value) {
  case "0":
    anzeigeOut.innerHTML = "CO2";
    break;
  case "1":
    anzeigeOut.innerHTML = "NOx";
    break;
  case "2":
    anzeigeOut.innerHTML = "Feinstaub";
    break;
  default:
    anzeigeOut.innerHTML = "none";
}


//var control = L.Control;
//control.setPosition("topright");
//mymap.addControl(control);
//control.onAdd("control");
//control.addTo(mymap);


deckkraftIn.oninput = function() {
  deckkraftOut.innerHTML = this.value;
  deckkraft = this.value;
  for (var i = 0; i < Stadtteile_Poly.length; i++) {
    Stadtteile_Poly[i].setStyle({
      fillOpacity: deckkraft / 100,
      opacity: deckkraft / 100
    });
  }
}


anzeigeIn.oninput = function() {
  anzeige = this.value;
  switch (anzeige) {
    case "0":
      anzeigeOut.innerHTML = "CO2";
      for (var i = 0; i < Stadtteile_Poly.length; i++) {
        Stadtteile_Poly[i].setStyle({
          color: getColor(daten[i].CO2, min_CO2, max_CO2)
        });
      }
      break;
    case "1":
      anzeigeOut.innerHTML = "NOx";
      for (var i = 0; i < Stadtteile_Poly.length; i++) {
        Stadtteile_Poly[i].setStyle({
          color: getColor(daten[i].NOx, min_NOx, max_NOx)
        });
      }
      break;
    case "2":
      anzeigeOut.innerHTML = "Feinstaub";
      for (var i = 0; i < Stadtteile_Poly.length; i++) {
        Stadtteile_Poly[i].setStyle({
          color: getColor(daten[i].Feinstaub, min_Fei, max_Fei)
        });
      }
      break;
    default:
      anzeigeOut.innerHTML = "none";
  }
  console.log(anzeigeOut.innerHTML);
}



fetch("./daten.json")
  .then(function(resp) {
    return resp.json();
  })
  .then(function(data) {
    console.log(data);
    daten = data.features;
    console.log(daten);
    for(var i = 0; i < daten.length; i++){
      daten[i].CO2 = Math.round(Math.random() * 100);
      daten[i].NOx = Math.round(Math.random() * 100);
      daten[i].Feinstaub = Math.round(Math.random() * 100);
    }
    for (var i = 0; i < daten.length; i++) {
      if (min_CO2 == -1 || min_CO2 > daten[i].CO2) min_CO2 = daten[i].CO2;
      if (max_CO2 == -1 || max_CO2 < daten[i].CO2) max_CO2 = daten[i].CO2;
      if (min_NOx == -1 || min_NOx > daten[i].NOx) min_NOx = daten[i].NOx;
      if (max_NOx == -1 || max_NOx < daten[i].NOx) max_NOx = daten[i].NOx;
      if (min_Fei == -1 || min_Fei > daten[i].Feinstaub) min_Fei = daten[i].Feinstaub;
      if (max_Fei == -1 || max_Fei < daten[i].Feinstaub) max_Fei = daten[i].Feinstaub;
    }
    console.log("CO2: " + min_CO2 + "-" + max_CO2);
    console.log("NOx: " + min_NOx + "-" + max_NOx);
    console.log("Feinstaub: " + min_Fei + "-" + max_Fei);
  });

fetch("./Ebene_2_Stadtteil.geojson")
  .then(function(resp) {
    return resp.json();
  })
  .then(function(data) {
    console.log(data);
    //var geoObject = JSON.parse(data);
    Stadtteile = data.features;
    console.log(Stadtteile);
    for (var i = 0; i < Stadtteile.length; i++) {
      //console.log(rgbToHex(i * 3, 0, 0));
      //var r = getColor(daten[i].CO2, min_CO2, max_CO2) * 255;
      //var r = Math.random() * 255; //i/Stadtteile.length oder Math.random()
      //var g = 255 - r;
      Stadtteile_Poly[i] = L.geoJSON(Stadtteile[i], {
        color: 'none',
        color: getColor(daten[i].CO2, min_CO2, max_CO2),
        fillOpacity: deckkraft / 100,
        opacity: deckkraft / 100
      }).addTo(mymap);
    }
  });

function getColor(value, min, max) {
  var red = map(value, min, max) * 255;
  var green = 255 - red;
  var blue = 0;
  //console.log(red, green, blue);
  return rgbToHex(red, green, blue);
}

function rgbToHex(r, g, b) {
  return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

function map(value, min, max) {
  return (value - min) / (max - min);
}
