from app_utils import load_json, save_json
from pathlib import Path

class ConfigManager:
    """
    Manage configuration and preferences of an application.
    Attributes:
        config_file (str or Path): the pathname of the json file which stores the configuration.
        config_default (dict): a default configuration.
        config (dict): the current configuration.
    """

    def __init__(self, config_file:None|str|Path, config_default:dict=None):
        """
        The constructor.
        :param config_file: the json file that stores the configuration.
        :param config_default: a default configuration.
        """
        self.config_file = config_file
        self.config_default = config_default
        self.config = None
        self.load()

    def load(self):
        """
        Loads in a dictionary configuration data from the current configuration file.
        """
        if self.config_file and self.config_file.exists() :
            self.config=load_json(self.config_file, self.config_default)
        else :
            self.config = self.config_default
            self.save()
            print("Create config file with defaults...")

    def save(self):
        """
        Saves the configuration dictionary in the current configuration file.
        """
        save_json(self.config, self.config_file)

    def get(self, key):
        """
        Gets the value associated to the key in the configuration dictionary.
        :param key: the key.
        :return: the value.
        """
        return self.config.get(key, self.config_default[key])

    def set(self, key, value):
        """
        Sets the key-value pair in the configuration dictionary.
        :param key: the key.
        :param value: the value.
        """
        self.config[key] = value

