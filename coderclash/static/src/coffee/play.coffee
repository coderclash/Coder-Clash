$(document).ready ->
  socket = io.connect 'http://localhost:8001'

  socket.on 'connect', ->
    console.log 'connected'
    socket.send('connected!')

  socket.on 'message', (message) ->
    console.log message

  socket.on 'disconnect', ->
    console.log 'disconnected'