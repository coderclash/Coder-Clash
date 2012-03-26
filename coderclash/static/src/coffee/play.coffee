

Player = Backbone.Model.extend
  dispatch: (command) ->
    window.socket.emit 'command', { command: command }

  move: (code) ->
    window.socket.emit 'move', { code: code }


PlayerWindow = Backbone.View.extend
  initialize: (options) ->
    # set default .on() context
    _.bindAll(@)

    # compile the template for later
    source = $('#player-template').html()
    @template = Handlebars.compile(source)

    # set up player for view
    @player = options.player
    @player.on('change', @render)

    @render()

  render: () ->
    context = @player.toJSON()
    context.inGame = context.state == 'in_game'
    @$el.html @template(context)

    if context.inGame
      console.log 'in game'
      @editor = ace.edit 'editor'
      @editor.setTheme 'ace/theme/twilight'
      PythonMode = require('ace/mode/python').Mode
      @editor.getSession().setMode new PythonMode()

  events:
    'click *[data-player-command]': 'dispatch'
    'click *[data-player-move]': 'move'

  dispatch: (e) ->
    # various commands like: ready, not_ready, and leave
    @player.dispatch $(e.currentTarget).attr('data-player-command')

  move: (code) ->
    # send your code to the server and game
    @player.move @editor.getSession().getValue()



$(document).ready ->
  window.socket = io.connect 'http://localhost:8001'

  # initialize player and view
  player = new Player 
    state: 'not_ready'

  player_view = new PlayerWindow
    el: $('div[data-player-canvas=true]')
    player: player

  window.player = player
  window.player_view = player_view

  window.socket.on 'message', (message) ->
    $('.message').text message

  window.socket.on 'state', (state) ->
    player.set state.player

    if state.game
      $('.message').text state.game.challenge.time

  window.socket.on 'results', (data) ->
    console.log data.score, data.results, data.errors
