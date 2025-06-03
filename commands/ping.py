import commands.command_base as command_base
import screen as s

class Ping(command_base.Command):
    name: str = "ping"
    description: str = "responds if working"

    def usecase(self):
        return super().usecase()

    def run(self, *args, **kwargs):
        rslt = super().run(*args, **kwargs)
        print("pong!")
        s.Screen.instance.set_text(0, ("Pong!", "h1", "center"))
        return rslt