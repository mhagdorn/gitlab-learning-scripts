import yaml
from pathlib import Path
import argparse
from jinja2 import Environment, FileSystemLoader, select_autoescape
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
        return d+s
    else:
        return dt.strftime(fmt)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("course", type=Path,
                        help="the course description file")
    parser.add_argument("-t", "--template", type=Path,
                        help="the template to apply")
    parser.add_argument("-o", "--output", type=Path,
                        help="write to results to file")
    args = parser.parse_args()

    config = yaml.safe_load(args.course.read_text())

    env = Environment(
        loader=FileSystemLoader(args.template.parent),
        autoescape=select_autoescape())
    env.filters["datetime"] = format_date

    template = env.get_template(args.template.name)
    out = template.render(**config)

    if args.output is None:
        print(out)
    else:
        args.output.write_text(out)


if __name__ == "__main__":
    main()
