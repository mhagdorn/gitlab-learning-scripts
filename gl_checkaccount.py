import gitlab
import yaml
from pathlib import Path


def getUser(gl, name):
    user = gl.users.list(username=name)
    if len(user) > 0:
        return user[0]


def main():
    cname = "spacemed-2025.yml"
    config = yaml.safe_load(Path(cname).read_text())

    if 'gitlab' in config:
        gitlab_id = config['gitlab']
    else:
        gitlab_id = None
    gl = gitlab.Gitlab.from_config(gitlab_id=gitlab_id)
    gl.auth()

    for u in config['students']:
        user = getUser(gl, u)
        if user is not None:
            print(user.username, user.state)
        else:
            print(u)


if __name__ == '__main__':
    main()
