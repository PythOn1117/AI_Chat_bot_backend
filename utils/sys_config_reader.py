import os
from configparser import ConfigParser
from pathlib import Path

SYSTEM_CONFIG_FILE = os.path.join(Path(__file__).resolve().parent.parent, 'system.conf')


class SysConfigReader:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read(SYSTEM_CONFIG_FILE)
        self.config_sections = self.config.sections()

        self.config_items = {}
        for section in self.config_sections:
            self.config_items[section] = self.section_to_dict(section)

    def section_to_dict(self, section):
        if section in self.config_sections:
            return {_tuple[0]: _tuple[1] for _tuple in self.config.items(section)}
        else:
            raise KeyError(f'Section {section} does not exist')

    def get_mysql_config(self):
        return self.config_items['mysql']

    def get_redis_config(self):
        return self.config_items['redis']



