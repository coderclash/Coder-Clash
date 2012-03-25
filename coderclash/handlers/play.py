import tornadio2
import tornado.ioloop
from datetime import datetime

from coderclash.handlers.base import BaseHandler


class Play(BaseHandler):
    def get(self):
        user = self.get_current_user()
        self.write(self.render('play/play.html', user=user))


callback = None
participants = set()

class PlaySocket(tornadio2.SocketConnection):
    def __init__(self, *args, **kwargs):
        super(PlaySocket, self).__init__(*args, **kwargs)

        global callback
        if callback is None:
            callback = tornado.ioloop.PeriodicCallback(self.send_time, 5000)
            callback.start()

    def send_time(self):
        for p in participants:
            p.send(str(datetime.now()))

    def on_open(self, message):
        participants.add(self)

    def on_close(self):
        participants.remove(self)

    def on_message(self, message):
        self.send('hey!')
