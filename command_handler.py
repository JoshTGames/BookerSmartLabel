import os, importlib, inspect, commands.command_base as command_base
from timer import Timer as t
import json_manager
from screen import Screen as s

class CommandCache:
    """Means of carrying out a command again in the future"""
    def __init__(self, command, *args, **kwargs):
        self.command = command
        self.args = args
        self.kwargs = kwargs

class CommandHandler:
    """Manages all commands"""
    COMMANDS_FOLDER: str = "commands"
    commands = {}
    instance = None # singleton instance

    lastCommand: CommandCache = None

    def __init__(self):
        """Constructs this class, searching for commands in the commands directory"""

        self.instance = self
        #// Find commands
        located_files = [f[:-3] for f in os.listdir(self.COMMANDS_FOLDER) if f.endswith(".py")] # removes the last 3 characters (.py) from each file after accessing it

        count: int = 0
        
        for f in located_files:
            mod = importlib.import_module(f"commands.{f}")
            for _, obj in inspect.getmembers(mod, inspect.isclass):
                if issubclass(obj, command_base.Command) and obj is not command_base.Command:
                    self.register(obj())
                    count+=1
        print(f"Successfully located {count} command(s)!")

        self.timer = t(json_manager.read_file(f'{os.getcwd()}/settings.json')['screen-timer'], s.instance.set_default)
    
    def register(self, command: command_base.Command) -> command_base.Command:
        """Makes command usable
        Args:
            self (CommandHandler): This instance
            command (commands.Command): The command we want to register 

        Returns:
            command_base.Command: The same command we want to register

        Example:
            >>> manager.register(Ping())
        """

        CommandHandler.commands[command.name] = command
        return command

    def retrieve(self, name: str) -> command_base.Command:
        """Attempts to retrieve the command
        Args:
            self (CommandHandler): This instance
            name (str): Name of the command we want to retrieve
        
        Returns:
            command_base.Command: The command (if found) or None
        """
        return CommandHandler.commands.get(name, None)

    def execute(self, name: str, *args, **kwargs) -> bool:
        """Attempts to execute command
        Args:
            name (str): Name of the command we want to execute
            *args: List of arguments to parse
            **kwargs: Predefined variables to be parsed
        
        Returns:
            bool: True if successful
        """
        
        cmd = self.retrieve(name)
        if cmd is None:
            print(f"The command \"{name}\" doesn't exist!")
            return False
        
        success = cmd.run(*args, **kwargs) 
        if success and cmd.name != "repeat":
            CommandHandler.lastCommand = CommandCache(cmd, *args, **kwargs)

        # Timer for screen
        if success:
            self.timer.start()
        return success     