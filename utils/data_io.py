from dataclasses import dataclass
import json
from pathlib import Path


# TODO: Refactor the IO and save/load so that id = guild ids, etc.
@dataclass
class BotSettings(object):
    id = 0
    prefixes = ['!']
    admin_role = 'Mods'
    live_role = 'Live'
    game_filter = []
    member_blacklist = []
    member_whitelist = []


default_settings = BotSettings()


def save_json(data, file_name: str):
    print(f'Saving to {file_name}.')
    with open(Path(file_name), mode='w') as outfile:
        return json.dump(data, outfile)


def save_settings(settings: BotSettings, file_name: str):
    data = {
        'id': settings.id,
        'prefixes': settings.prefixes,
        'admin_role': settings.admin_role,
        'live_role': settings.live_role,
        'game_filter': settings.game_filter,
        'member_blacklist': settings.member_blacklist,
        'member_whitelist': settings.member_whitelist
    }
    save_json(data, file_name)


def load_json(file_name: str):
    print(f'Loading from {file_name}.')
    with open(Path(file_name), mode="r") as infile:
        return json.load(infile)


def load_settings(file_name: str):
    data = load_json(file_name)
    # Put data into a structure for easy `.` access
    settings = BotSettings()
    settings.id = data['id']
    settings.prefixes = data['prefixes']
    settings.admin_role = data['admin_role']
    settings.live_role = data['live_role']
    settings.game_filter = data['game_filter']
    settings.member_blacklist = data['member_blacklist']
    settings.member_blacklist = data['member_whitelist']
    return settings


def generate_default_settings(file_name: str = '../data/settings.json'):
    save_settings(default_settings, file_name)


if __name__ == '__main__':
    default_relative_file_location = '../data/settings.json'
    generate_default_settings(default_relative_file_location)
