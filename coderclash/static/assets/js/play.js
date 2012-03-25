var Player, PlayerWindow;

Player = Backbone.Model.extend({
  dispatch: function(command) {
    return window.socket.emit('command', {
      command: command
    });
  }
});

PlayerWindow = Backbone.View.extend({
  initialize: function(options) {
    var source;
    _.bindAll(this);
    source = $('#player-template').html();
    this.template = Handlebars.compile(source);
    this.player = options.player;
    this.player.on('change', this.render);
    return this.render();
  },
  render: function() {
    var context;
    context = this.player.toJSON();
    context.inGame = context.state === 'in_game';
    return this.$el.html(this.template(context));
  },
  events: {
    'click *[data-player-command]': 'dispatch'
  },
  dispatch: function(e) {
    return this.player.dispatch($(e.currentTarget).attr('data-player-command'));
  }
});

$(document).ready(function() {
  var player, player_view;
  window.socket = io.connect('http://localhost:8001');
  player = new Player({
    state: 'not_ready'
  });
  player_view = new PlayerWindow({
    el: $('div[data-player-canvas=true]'),
    player: player
  });
  window.socket.on('message', function(message) {
    return $('.message').text(message);
  });
  return window.socket.on('state', function(state) {
    return player.set(state.player);
  });
});
