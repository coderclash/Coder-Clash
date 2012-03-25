
$(document).ready(function() {
  var socket;
  socket = io.connect('http://localhost:8001');
  socket.on('connect', function() {
    console.log('connected');
    return socket.send('connected!');
  });
  socket.on('message', function(message) {
    return console.log(message);
  });
  return socket.on('disconnect', function() {
    return console.log('disconnected');
  });
});
