import commands.command_base as command_base
import os

class Shutdown(command_base.Command):
    name: str = "shutdown"
    description: str = "powers off this device"

    def usecase(self):
        return super().usecase()

    def run(self, *args, **kwargs):
        rslt = super().run(*args, **kwargs)
        os.system("sudo shutdown now -h")
        return rslt