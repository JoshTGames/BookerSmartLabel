import commands.command_base as command_base
import screen as s

import os
import json_manager as j

version = j.read_file(os.getcwd() + '/version.json')['version']

class Version(command_base.Command):
    name: str = "version"
    description: str = "returns this software version"

    def usecase(self):
        return super().usecase()

    def run(self, *args, **kwargs):
        rslt = super().run(*args, **kwargs)

        print(f"Version: {version}")
        s.Screen.instance.set_text(0, ("Version", "h1", "center"),(version, "h3", "center"))
        return rslt