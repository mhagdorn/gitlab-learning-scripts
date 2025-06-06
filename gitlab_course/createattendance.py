from .glc import GitlabCourse
import yaml
from pathlib import Path
import argparse
from jinja2 import Environment, PackageLoader, select_autoescape
import datetime


def format_date(value):
    if isinstance(value, datetime.date):
        dt = value
    else:
        dt = datetime.date.fromisoformat(value)
    return dt.strftime("%A, %d %B %Y")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("course", type=Path,
                        help="the course description file")
    parser.add_argument("-o", "--output", type=Path,
                        help="write to results to file")
    args = parser.parse_args()

    config = yaml.safe_load(args.course.read_text())

    env = Environment(
        loader=PackageLoader("gitlab_course"),
        autoescape=select_autoescape())
    env.filters["datetime"] = format_date

    if 'gitlab' in config:
        gitlab_id = config['gitlab']
    else:
        gitlab_id = None
    glc = GitlabCourse(gitlab_id=gitlab_id)

    users = glc.getUserList(config['participants'])

    attendance = env.get_template("attendance.csv")
    out = attendance.render(**config, users=users)

    if args.output is None:
        print(out)
    else:
        args.output.write_text(out)


if __name__ == "__main__":
    main()
