from .glc import GitlabCourse
from .apply_template import apply_template
import yaml
from pathlib import Path
import argparse
from email.message import EmailMessage
import smtplib


def arg_parser():
    mail_type = ["participants", "waiting", "instructors", "helpers"]
    parser = argparse.ArgumentParser()
    parser.add_argument("course", type=Path,
                        help="the course description file")
    parser.add_argument("-t", "--template", type=Path,
                        required=True,
                        help="the template to apply")
    parser.add_argument("-s", "--session", type=int, default=1,
                        help="the session number")
    parser.add_argument("-g", "--mail-group", choices=mail_type,
                        action="append", default=[],
                        help="select the group of email recipiants")
    parser.add_argument("-m", "--mail", action="append", default=[],
                        help="individual email addresses")
    parser.add_argument("-f", "--from-email",
                        help="the email address of the sender, "
                        "use the organiser email address if not specified")
    parser.add_argument('-S', "--subject", help="the email subject")
    parser.add_argument('-e', '--mail-server',
                        help='the SMTP server to be used')
    return parser


def main():
    parser = arg_parser()
    args = parser.parse_args()

    config = yaml.safe_load(args.course.read_text())

    if args.mail_server is not None:
        smtp_server = smtplib.SMTP(args.mail_server)
    else:
        smtp_server = None

    if 'gitlab' in config:
        gitlab_id = config['gitlab']
    else:
        gitlab_id = None
    glc = GitlabCourse(gitlab_id=gitlab_id)

    stem = args.template.parent / Path(args.template.stem)
    templates = {}
    for t in ["txt", "html"]:
        if stem.suffix == t:
            templates[t] = args.template
    for t in ["txt", "html"]:
        if t not in templates:
            check = stem.with_suffix(f".{t}.j2")
            if check.exists():
                templates[t] = check

    recipients = set()
    for mt in ["instructors", "helpers"]:
        if mt in args.mail_group and mt in config:
            for u in config[mt]:
                recipients.add(u["email"])
    for mt in ["participants", "waiting"]:
        if mt in args.mail_group and mt in config:
            for u in config[mt]:
                recipients.add(u)
    for m in args.mail:
        if '@' not in m:
            parser.error(f"{m} is not an email address")
        recipients.add(m)

    organiser = None
    if "organiser" in config:
        organiser = config["organiser"]["email"]
    if args.from_email is None:
        args.from_email = organiser
    if args.from_email is None:
        parser.error(
            "no from-email specified and config contains no organiser")

    msg = EmailMessage()
    if args.subject is not None:
        msg['Subject'] = args.subject
    else:
        msg['Subject'] = config["series"]
    msg['From'] = args.from_email
    msg['To'] = ','.join(recipients)
    if organiser is not None:
        msg['Cc'] = organiser
    if 'txt' in templates:
        try:
            content = apply_template(glc, config, templates['txt'],
                                     session=args.session)
        except Exception as e:
            parser.error(e)
        msg.set_content(content, "plain")
    if 'html' in templates:
        try:
            content = apply_template(glc, config, templates['html'],
                                     session=args.session)
        except Exception as e:
            parser.error(e)
        msg.add_alternative(content, "html")

    if smtp_server is not None:
        smtp_server.send_message(msg)
    else:
        print(msg)


if __name__ == "__main__":
    main()
