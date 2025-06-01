import commands.command_base as command_base
import command_handler

class Help(command_base.Command):
    name: str = "help"
    description: str = "shows commands"
    
    def usecase(self):
        return super().usecase() + " {CommandName}"

    def run(self, *args, **kwargs):
        rslt = super().run(*args, **kwargs)
        if(len(args) >0):
            cmd = command_handler.CommandHandler.retrieve(command_handler.CommandHandler.instance, args[0])
            msg = f"Usage: '{cmd.usecase()}'" if cmd is not None else f"The command \"{args[0]}\" doesn't exist!"
            print(msg)
            return rslt


        msg = """
##############
-- COMMANDS --
"""

        count: int = 0
        for _, c in command_handler.CommandHandler.commands.items():
            count+=1
            print(c)
            msg += f"{count}.{c.name} | Usage: '{c.usecase()}' | {c.description}\n"
        print(msg)
        return rslt