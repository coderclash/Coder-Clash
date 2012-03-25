
$(document).ready(function() {
  var socket;
  socket = io.connect('http://localhost:8001');
  socket.on('connect', function() {
    return console.log('connected');
  });
  return socket.on('disconnect', function() {
    return console.log('disconnected');
  });
});
