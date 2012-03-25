$(document).ready ->
  socket = io.connect 'http://localhost:8001'

  socket.on 'connect', ->
    console.log 'connected'
    socket.send('connected!')

  socket.on 'message', (message) ->
    console.log message

  socket.on 'disconnect', ->
    console.log 'disconnected'

  # TODO: might make sense to do Backbone here?
  # that way state changes can just trigger .change events on
  # the models and rerender the views like nobody's business

  $(document).on 'click', '.player-status', ->
    socket.emit 'player_state', { state: 'ready' }