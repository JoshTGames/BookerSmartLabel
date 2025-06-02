import commands.command_base as command_base

import os, sys
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

class Ping(command_base.Command):
    name: str = "ping"
    description: str = "responds if working"

    def usecase(self):
        return super().usecase()

    def run(self, *args, **kwargs):
        rslt = super().run(*args, **kwargs)
        print("pong!")
        return rslt