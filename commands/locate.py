import commands.command_base as command_base
import command_handler as ch

class Locate(command_base.Command):
    name: str = "locate"
    description: str = "returns information about a business"

    def usecase(self):
        return super().usecase() + " {BusinessName}"

    def run(self, *args, **kwargs):
        rslt = super().run(*args, **kwargs)
        cache: ch.CommandCache = ch.CommandHandler.lastCommand 
        if(cache is None or cache.command == self): return rslt
        
        cache.command.run(*cache.args, *cache.kwargs)
        return rslt