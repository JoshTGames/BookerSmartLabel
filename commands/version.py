import commands.command_base as command_base
import screen as s

import os, sys
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from lib import json as j

version = j.read_file(os.getcwd() + '/version.json')['version']

class Version(command_base.Command):
    name: str = "version"
    description: str = "returns this software version"

    def usecase(self):
        return super().usecase()

    def run(self, *args, **kwargs):
        rslt = super().run(*args, **kwargs)

        print(version)
        s.Screen.instance.set_text(0, (version, "h1", "center"))
        return rslt