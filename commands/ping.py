import commands.command_base as command_base

import os, sys
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import screen as s

class Ping(command_base.Command):
    name: str = "ping"
    description: str = "responds if working"

    def usecase(self):
        return super().usecase()

    def run(self, *args, **kwargs):
        rslt = super().run(*args, **kwargs)
        print("pong!")
        screen = s.Screen.instance
        screen.set(screen.TEXT.create_wrapper((screen.WIDTH, screen.HEIGHT), "scale", 0, ("Josh", "h1", "center"),("Stock Control", "h3", "center")))
        return rslt