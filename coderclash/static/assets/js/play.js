var Game, GameWindow, Player, PlayerWindow;

Game = Backbone.Model.extend({
  nothing: function() {}
});

GameWindow = Backbone.View.extend({
  /*
    Once game is going, will have the following attributes:
  
    challenge:
      
    players: ['Player 1', 'Player 2']
  */
  initialize: function(options) {
    var source;
    _.bindAll(this);
    source = $('#game-template').html();
    this.template = Handlebars.compile(source);
    this.player = options.player;
    this.game = options.game;
    this.editor = null;
    this.game.on('change', this.render);
    return this.render();
  },
  events: {
    'click *[data-player-move]': 'move'
  },
  render: function() {
    var context;
    if (this.game.get('in_progress')) {
      context = this.game.toJSON();
      console.log(context);
      this.$el.html(this.template(context));
      if (this.editor === null) return this.createEditor();
    } else {
      if (this.editor) {
        this.killEditor();
        return this.$el.html('');
      }
    }
  },
  createEditor: function() {
    var PythonMode;
    $('#editor').removeClass('hide');
    this.editor = ace.edit('editor');
    this.editor.setTheme('ace/theme/twilight');
    PythonMode = require('ace/mode/python').Mode;
    return this.editor.getSession().setMode(new PythonMode());
  },
  killEditor: function() {
    this.editor.destroy();
    this.editor = null;
    return $('#editor').addClass('hide');
  },
  move: function(code) {
    return this.player.move(this.editor.getSession().getValue());
  }
});

Player = Backbone.Model.extend({
  dispatch: function(command) {
    return window.socket.emit('command', {
      command: command
    });
  },
  move: function(code) {
    console.log('sending code');
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
  var game, game_view, player, player_view;
  window.socket = io.connect('http://localhost:8001');
  player = new Player({
    state: 'not_ready'
  });
  player_view = new PlayerWindow({
    el: $('div[data-player-canvas=true]'),
    player: player
  });
  game = new Game({
    in_progress: false
  });
  game_view = new GameWindow({
    el: $('div[data-game-canvas=true]'),
    player: player,
    game: game
  });
  window.socket.on('message', function(message) {
    return $('.message').text(message);
  });
  window.socket.on('state', function(state) {
    player.set(state.player);
    if (state.game) {
      game.set({
        in_progress: true
      });
      return game.set(state.game);
    } else {
      return game.set({
        in_progress: false
      });
    }
  });
  return window.socket.on('results', function(data) {
    return game.set(data);
  });
});
