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
    parser.add_argument("-s", "--session", type=int,
                        help="the session number")
    parser.add_argument("-l", "--lecture", type=int,
                        help="the session number")
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

    users = []
    for u in config['students']:
        user = glc.getUser(u)
        if user is not None:
            users.append((user.name, user.username))
        else:
            users.append((None, u))

    if args.session is not None:
        try:
            session = config["sessions"][args.session-1]
        except Exception as e:
            parser.error(e)
        sign_in = env.get_template("sign-in.tex")
        out = sign_in.render(**config, users=users, session=session)
    elif args.lecture is not None:
        try:
            session = config["sessions"][args.lecture-1]
        except Exception as e:
            parser.error(e)
        lecture = env.get_template("session.tex")
        out = lecture.render(**config, session=session)
    else:
        attendance = env.get_template("attendance.csv")
        out = attendance.render(**config, users=users)
    if args.output is None:
        print(out)
    else:
        args.output.write_text(out)


if __name__ == "__main__":
    main()
