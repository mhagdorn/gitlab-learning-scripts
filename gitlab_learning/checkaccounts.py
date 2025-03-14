from .gl import GitlabLearning
import yaml
from pathlib import Path
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("course", type=Path,
                        help="the course description file")
    args = parser.parse_args()

    config = yaml.safe_load(args.course.read_text())

    if 'gitlab' in config:
        gitlab_id = config['gitlab']
    else:
        gitlab_id = None
    gl = GitlabLearning(gitlab_id=gitlab_id)

    for u in config['students']:
        user = gl.getUser(u)
        if user is not None:
            print(user.username, user.state)
        else:
            print(u)


if __name__ == "__main__":
    main()
