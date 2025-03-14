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

    course_group = gl.get_group(config["name"], create=True)
    year_group = gl.get_group(config["year"], parent_group=course_group,
                              create=True)

    print(course_group)
    print(year_group)


if __name__ == '__main__':
    main()
