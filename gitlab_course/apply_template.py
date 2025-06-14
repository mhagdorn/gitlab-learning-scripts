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

    if args.session < 1 or args.session > len(config["sessions"]):
        parser.error(
            "number of sessions outside range "
            f"[1:{len(config['sessions'])}]")

    env = Environment(
        loader=FileSystemLoader(args.template.parent),
        autoescape=select_autoescape())
    env.filters["datetime"] = format_date

    if 'gitlab' in config:
        gitlab_id = config['gitlab']
    else:
        gitlab_id = None
    glc = GitlabCourse(gitlab_id=gitlab_id)

    template = env.get_template(args.template.name)

    # get variables from template, see https://stackoverflow.com/a/8284419
    template_vars = meta.find_undeclared_variables(
        env.parse(env.loader.get_source(env, args.template.name)))

    if "users" in template_vars:
        users = glc.getUserList(config['participants'])
    else:
        users = None
    out = template.render(**config, snr=args.session - 1, users=users)

    if args.output is None:
        print(out)
    else:
        args.output.write_text(out)


if __name__ == "__main__":
    main()
