from .glc import GitlabCourse
import yaml
from pathlib import Path
import sys
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("course", type=Path,
                        help="the course description file")
    parser.add_argument("-m", "--merge-requests", default=False,
                        action="store_true", help="show merge requests")
    parser.add_argument("-o", "--output", type=Path, metavar="OUT",
                        help="write output to OUT")
    args = parser.parse_args()

    config = yaml.safe_load(args.course.read_text())

    if 'gitlab' in config:
        gitlab_id = config['gitlab']
    else:
        gitlab_id = None
    glc = GitlabCourse(gitlab_id=gitlab_id)

    if args.output is not None:
        out = args.output.open("w")
    else:
        out = sys.stdout

    course_group = glc.get_group(config["name"])
    year_group = glc.get_group(config["year"], parent_group=course_group)
    personal_group = glc.get_group("personal", parent_group=year_group)

    personal_projects = {}
    for p in personal_group.projects.list():
        personal_projects[p.name] = glc.gl.projects.get(p.id)

    users = glc.getUserList(config['participants'])

    for i, u in enumerate(users):
        try:
            personal_projects[u.sysID].members.get(u._ID)
            users[i].hasPersonal = True
        except Exception:
            users[i].hasPersonal = False

    if args.merge_requests:
        for u in users:
            print(u.sysID, u.name, file=out)
            for mr in glc.getMergeRequests(personal_projects[u.sysID]):
                if not mr.state == "merged":
                    print("  "+mr.title, mr.draft, mr.approved,
                          sep="|", file=out)
            print(file=out)
    else:
        keys = ["glUser", "name", "status", "hasKeys", "hasPersonal"]
        print(":".join(keys), file=out)
        for u in users:
            print(u.glID, u.name, u.status, u.hasKeys, u.hasPersonal,
                  sep=":", file=out)
    out.close()


if __name__ == "__main__":
    main()
