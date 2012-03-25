import tornadio2

from coderclash.handlers.base import BaseHandler


class Play(BaseHandler):
    def get(self):
        user = self.get_current_user()
        self.write(self.render('play/play.html', user=user))


class PlaySocket(tornadio2.SocketConnection):
    def on_message(self, message):
        pass
