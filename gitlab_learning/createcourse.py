from .gl import GitlabLearning
import gitlab
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
    year_group = gl.get_group(
        config["year"], parent_group=course_group, create=True)
    personal_group = gl.get_group(
        "personal", parent_group=year_group, create=True)

    # handle personal projects
    projects = {}
    for p in personal_group.projects.list():
        projects[p.name] = p

    for u in config['students']:
        if u not in projects:
            projects[u] = gl.gl.projects.create(
                {'name': u, 'namespace_id': personal_group.id})
        project = gl.gl.projects.get(projects[u].id)

        user = gl.getUser(u)
        if user is not None:
            try:
                member = project.members.get(user.id)
            except gitlab.exceptions.GitlabGetError:
                member = project.members.create(
                    {'user_id': user.id, 'access_level':
                     gitlab.const.AccessLevel.MAINTAINER})

        # need to add some files to repo


if __name__ == '__main__':
    main()
