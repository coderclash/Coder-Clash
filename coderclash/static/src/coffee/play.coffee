
Game = Backbone.Model.extend
  nothing: ->

GameWindow = Backbone.View.extend
  ###
  Once game is going, will have the following attributes:

  challenge:
    
  players: ['Player 1', 'Player 2']
  ###
  initialize: (options) ->
    _.bindAll(@)

    source = $('#game-template').html()
    @template = Handlebars.compile(source)

    @player = options.player
    @game = options.game
    @editor = null

    @game.on('change', @render)
    @render()

  events:
    'click *[data-player-move]': 'move'

  render: () ->
    if @game.get 'in_progress'
      context = @game.toJSON()
      console.log context
      @$el.html @template(context)

      if @editor is null
        @createEditor()
    else
      if @editor
        @killEditor()
        @$el.html ''

  createEditor: ->
    $('#editor').removeClass('hide')

    @editor = ace.edit 'editor'
    @editor.setTheme 'ace/theme/twilight'
    PythonMode = require('ace/mode/python').Mode
    @editor.getSession().setMode new PythonMode()

  killEditor: ->
    @editor.destroy()
    @editor = null
    $('#editor').addClass('hide')


  move: (code) ->
    # send your code to the server and game
    @player.move @editor.getSession().getValue()


Player = Backbone.Model.extend
  dispatch: (command) ->
    window.socket.emit 'command', { command: command }

  move: (code) ->
    console.log 'sending code'
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


  events:
    'click *[data-player-command]': 'dispatch'

  dispatch: (e) ->
    # various commands like: ready, not_ready, and leave
    @player.dispatch $(e.currentTarget).attr('data-player-command')




$(document).ready ->
  window.socket = io.connect 'http://localhost:8001'

  # initialize player and view
  player = new Player 
    state: 'not_ready'

  player_view = new PlayerWindow
    el: $('div[data-player-canvas=true]')
    player: player


  game = new Game {in_progress: false}

  game_view = new GameWindow
    el: $('div[data-game-canvas=true]')
    player: player
    game: game


  window.socket.on 'message', (message) ->
    # misc messages (game start countdown)
    $('.message').text message

  window.socket.on 'state', (state) ->
    # ticks the state for the player and the game (and its players)
    player.set state.player

    if state.game
      game.set in_progress: true
      game.set state.game
    else
      game.set in_progress: false

  window.socket.on 'results', (data) ->
    # contains score, results and errors from a code run
    game.set data
