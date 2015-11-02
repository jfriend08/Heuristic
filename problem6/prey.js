var WebSocket = require('ws')

var mainSocket = new WebSocket('ws://localhost:1990');
var socketH = new WebSocket('ws://localhost:1991');
var socketP = new WebSocket('ws://localhost:1992');

//some important factors for prey
var preyPos = [230, 200];
var hunterPos = [0, 0];
var hunterDirection = [0, 0];
var walls = [];
var publisherMsg = false;

//for mainSocket
mainSocket.onmessage = function(e){
  console.log("Publisher: " + e.data);
  publisherMsg = true;
};

mainSocket.onerror = socketH.onerror = socketP.onerror = function (error) {
  console.log('WebSocket error: ' + error);
};

//for Hunter
socketH.onopen = function(e){
  console.log("socketH OPEN");
};

//for Prey
socketP.onmessage = function(e){
  console.log("Prey: " + e.data);
  if (e.data.command == 'P') {
    preyPos = e.data.prey;
    hunterPos = e.data.hunter;
  } else if (e.data.command == 'W') {
    walls = e.data.walls;
  }
};


// socketP.onopen = function (e) {
//   console.log("socketP OPEN");
//   // var moveCount = 1;
//   // while (moveCount < 100) {
//   //   socketP.send(JSON.stringify({command:'P'}));
//   //   socketP.send(JSON.stringify({command:'W'}));
//   //   if (moveCount%2 == 1) {
//   //     socketP.send(JSON.stringify( {command:'M', direction: 'N'}) );
//   //   }
//   //   socketH.send(JSON.stringify({command:'M'}));
//   //   while(!publisherMsg) {}

//   //   moveCount++;
//   //   publisherMsg = false;
//   // }
// }
socketP.on('open', function(e) {
  console.log('hi');
  console.log(socketP.readyState)
})

// console.log(socketP.readyState)
if(socketP) {
  console.log('yo')
  // socketP.send(JSON.stringify( {command:'M', direction: 'N'}));
}
// if(socketP.readyState != socketP.OPEN){
//   console.error('Client state is ' + socketP.readyState);
// }else {
//   socketP.send(JSON.stringify( {command:'M', direction: 'N'}));
// }
// socketP.send(JSON.stringify( {command:'M', direction: 'N'}), function(err) {
//   console.log('err');
// });


