var SerialPort = require("serialport");
var http = require("http");
var portName = process.argv[2];

var fs = require("fs");
//var database = require("nedb");

//var DB = new database("GPS-Daten2.db");
//DB.loadDatabase();


// var server = http.createServer(function(request, response) {
//   response.writeHead(200, {"Content-Type": "text/plain"})
//   response.write("none");
//   response.end();
// }).listen(8000);


var pre_latlng = convert("0 0, 0 0, 0");


var myPort = new SerialPort(portName, {
  baudRate: 9600,
  parser: new SerialPort.parsers.Readline("\r\n")
});

myPort.on('open', onOpen);
myPort.on('data', onData);

function onOpen() {
  console.log("Open connection");
}

function onData(data) {
  if (data != "") {
    var date = (new Date()).toJSON();
    console.log(data + "");
    data = convert(data + "");
    //console.log(data);
    var daten = date + "," + data[0] + "," + data[1] + "," + data[2];
    //console.log(daten);


    //DB.insert(daten);
    fs.appendFile("GPS-Daten.csv", daten + "\n", (err) => {
      if (err) throw err;
    });

    fs.writeFile("../Visualisierung/aktuelledaten.txt", pre_latlng + "\n" + data, (err) => {
      if (err) throw err;
    });

    // server.close();
    //console.log(date + " " + data);
    // server = http.createServer(function(request, response) {
    //   response.writeHead(200, {"Content-Type": "text/plain"})
    //   response.write(pre_latlng + "\n" + data);
    //   response.end();
    // }).listen(8000);
    pre_latlng = data;
  }
}



function convert(data) {
  //console.log(data);
  data = data.split(", ");
  //console.log(data);
  data[0] = data[0].split(" ");
  data[1] = data[1].split(" ");
  //console.log(data);
  data[0][1] /= 60;
  data[1][1] /= 60;
  //console.log(data);
  data[0] = Number(data[0][0]) + Number(data[0][1]);
  data[1] = Number(data[1][0]) + Number(data[1][1]);
  //console.log(data);
  //data = data[0] + ", " + data[1];
  return data;
}