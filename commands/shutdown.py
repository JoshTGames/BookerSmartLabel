import commands.command_base as command_base
import os

class Shutdown(command_base.Command):
    name: str = "shutdown"
    description: str = "powers off the device"

    def usecase(self):
        return super().usecase()

    def run(self, *args, **kwargs):
        rslt = super().run(*args, **kwargs)
        os.system("shutdown now -h") # May need root permission (sudo shutdown...)
        return rslt