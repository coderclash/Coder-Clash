

Player = Backbone.Model.extend
  dispatch: (command) ->
    window.socket.emit 'command', { command: command }


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
    @player.dispatch $(e.currentTarget).attr('data-player-command')



$(document).ready ->
  window.socket = io.connect 'http://localhost:8001'

  # initialize player and view
  player = new Player 
    state: 'not_ready'

  player_view = new PlayerWindow
    el: $('div[data-player-canvas=true]')
    player: player


  window.socket.on 'message', (message) ->
    $('.message').text message

  window.socket.on 'state', (state) ->
    player.set state.player
