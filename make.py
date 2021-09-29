"""
essentially compiles the application.
finds out SHA and name from git and
creates an config.ini file for the application to use.
"""

import json

import git


def create_app_info():
    repo = git.Repo(search_parent_directories=True)
    config_dict = {'SHA': repo.head.object.hexsha,
                   'ProjectName': repo.remotes.origin.url.split('.git')[0].split('/')[-1]}
    with open('config.ini', 'w+') as config_file:
        json.dump(config_dict, config_file)


if __name__ == '__main__':
    create_app_info()
