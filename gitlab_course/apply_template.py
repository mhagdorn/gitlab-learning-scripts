from .glc import GitlabCourse
import yaml
from pathlib import Path
import argparse
from jinja2 import Environment, FileSystemLoader, select_autoescape, meta
import datetime


def format_date(value, fmt="%A, %d %B %Y"):
    if isinstance(value, datetime.date):
        dt = value
    else:
        dt = datetime.date.fromisoformat(value)
    if fmt == "EN":
        d = str(dt.day)
        if d[-1] == '1':
            s = 'st'
        elif d[-1] == '2':
            s = 'nd'
        elif d[-1] == '3':
            s = 'rd'
        else:
            s = 'th'
        return d + s
    else:
        return dt.strftime(fmt)


def apply_template(glc, cfg, tname, session=1):
    if session < 1 or session > len(cfg["sessions"]):
        raise RuntimeError(
            f"number of sessions outside range [1:{len(cfg['sessions'])}]")

    env = Environment(
        loader=FileSystemLoader(tname.parent),
        autoescape=select_autoescape())
    env.filters["datetime"] = format_date

    template = env.get_template(tname.name)

    users = glc.getUserList(cfg['participants'])
    if len(users) == 0:
        users = None
    out = template.render(**cfg, snr=session - 1, users=users)

    return out


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("course", type=Path,
                        help="the course description file")
    parser.add_argument("-t", "--template", type=Path,
                        required=True,
                        help="the template to apply")
    parser.add_argument("-s", "--session", type=int, default=1,
                        help="the session number")
    parser.add_argument("-o", "--output", type=Path,
                        help="write to results to file")
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

    try:
        out = apply_template(glc, config, args.template, session=args.session)
    except Exception as e:
        parser.error(e)

    if args.output is None:
        print(out)
    else:
        args.output.write_text(out)


if __name__ == "__main__":
    main()
