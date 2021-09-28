"""

essentially compiles the application.

"""

import git
import json


def create_app_info():
    repo = git.Repo(search_parent_directories=True)
    config_dict = {'SHA': repo.head.object.hexsha,
                   'ProjectName': repo.remotes.origin.url.split('.git')[0].split('/')[-1]}
    with open('app/config.ini', 'w+') as config_file:
        json.dump(config_dict, config_file)


if __name__ == '__main__':
    create_app_info()