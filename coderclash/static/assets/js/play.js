var Player, PlayerWindow;

Player = Backbone.Model.extend({
  dispatch: function(command) {
    return window.socket.emit('command', {
      command: command
    });
  },
  move: function(code) {
    return window.socket.emit('move', {
      code: code
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
    var PythonMode, context;
    context = this.player.toJSON();
    context.inGame = context.state === 'in_game';
    this.$el.html(this.template(context));
    if (context.inGame) {
      console.log('in game');
      this.editor = ace.edit('editor');
      this.editor.setTheme('ace/theme/twilight');
      PythonMode = require('ace/mode/python').Mode;
      return this.editor.getSession().setMode(new PythonMode());
    }
  },
  events: {
    'click *[data-player-command]': 'dispatch',
    'click *[data-player-move]': 'move'
  },
  dispatch: function(e) {
    return this.player.dispatch($(e.currentTarget).attr('data-player-command'));
  },
  move: function(code) {
    return this.player.move(this.editor.getSession().getValue());
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
  window.player = player;
  window.player_view = player_view;
  window.socket.on('message', function(message) {
    return $('.message').text(message);
  });
  window.socket.on('state', function(state) {
    player.set(state.player);
    if (state.game) return $('.message').text(state.game.challenge.time);
  });
  return window.socket.on('results', function(data) {
    return console.log(data.score, data.results, data.errors);
  });
});
