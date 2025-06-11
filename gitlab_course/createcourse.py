from .glc import GitlabCourse
import gitlab
import yaml
from pathlib import Path
import argparse
from jinja2 import Environment, BaseLoader, PackageLoader, select_autoescape


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("course", type=Path,
                        help="the course description file")
    return parser


def main():
    parser = arg_parser()
    args = parser.parse_args()

    config = yaml.safe_load(args.course.read_text())

    if 'gitlab' in config:
        gitlab_id = config['gitlab']
    else:
        gitlab_id = None
    glc = GitlabCourse(gitlab_id=gitlab_id)

    course_group = glc.get_group(config["name"], create=True)
    year_group = glc.get_group(
        config["year"], parent_group=course_group, create=True)
    personal_group = glc.get_group(
        "personal", parent_group=year_group, create=True)

    # the template for the README.md
    if 'readme' in config:
        readme = Environment(loader=BaseLoader()).from_string(config['readme'])
    else:
        env = Environment(
            loader=PackageLoader("gitlab_course"),
            autoescape=select_autoescape())
        readme = env.get_template("README.md")

    # handle personal projects
    projects = {}
    for p in personal_group.projects.list():
        projects[p.name] = p

    for u in config['students']:
        # create project if it does not exist
        if u not in projects:
            projects[u] = glc.gl.projects.create(
                {'name': u, 'namespace_id': personal_group.id})
        project = glc.gl.projects.get(projects[u].id)

        # add user to project
        user = glc.getUser(u, raw=True)
        if user is not None:
            try:
                project.members.get(user.id)
            except gitlab.exceptions.GitlabGetError:
                project.members.create(
                    {'user_id': user.id, 'access_level':
                     gitlab.const.AccessLevel.MAINTAINER})

        # add readme to repo
        try:
            project.files.get(file_path='README.md', ref='main')
            have_readme = True
        except gitlab.exceptions.GitlabGetError:
            have_readme = False
        if not have_readme:
            project.files.create({'file_path': 'README.md',
                                  'branch': 'main',
                                  'content': readme.render(**config),
                                  'commit_message': 'Create Readme'})


if __name__ == '__main__':
    main()
