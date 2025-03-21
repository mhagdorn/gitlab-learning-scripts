from .glc import GitlabCourse
import yaml
from pathlib import Path
import argparse
import gitlab
from dataclasses import dataclass, field
from jinja2 import Environment, PackageLoader, select_autoescape


@dataclass
class GLCMergeRequest:
    title: str
    state: str
    draft: bool
    approved: list[str] = field(default_factory=list)


@dataclass
class GLCUser:
    sysID: str
    glID: str = ''
    name: str = ''
    status: str = ''
    hasKeys: bool = False
    hasPersonal: bool = False
    mergeRequests: list[GLCMergeRequest] = field(default_factory=list)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("course", type=Path,
                        help="the course description file")
    parser.add_argument("-m", "--merge-requests", default=False,
                        action="store_true", help="show merge requests")
    parser.add_argument("-c", "--comment-sheet", nargs="?", const=0,
                        type=int, metavar="SESSION",
                        help="print comment sheet")
    args = parser.parse_args()

    config = yaml.safe_load(args.course.read_text())

    if 'gitlab' in config:
        gitlab_id = config['gitlab']
    else:
        gitlab_id = None
    glc = GitlabCourse(gitlab_id=gitlab_id)

    env = Environment(
        loader=PackageLoader("gitlab_course"),
        autoescape=select_autoescape())

    course_group = glc.get_group(config["name"])
    year_group = glc.get_group(config["year"], parent_group=course_group)
    personal_group = glc.get_group("personal", parent_group=year_group)

    personal_projects = {}
    for p in personal_group.projects.list():
        personal_projects[p.name] = glc.gl.projects.get(p.id)

    users = []
    for u in config['students']:
        glcUser = GLCUser(u)
        user = glc.getUser(u)
        if user is not None:
            glcUser.glID = user.username
            glcUser.name = user.name
            glcUser.status = user.state
            glcUser.hasKeys = len(user.keys.list()) > 0
            try:
                personal_projects[u].members.get(user.id)
                glcUser.hasPersonal = True
            except gitlab.exceptions.GitlabGetError:
                glcUser.hasPersonal = False

            if glcUser.hasPersonal:
                for mr in personal_projects[u].mergerequests.list():
                    glcMR = GLCMergeRequest(mr.title, mr.state, mr.draft)
                    for a in mr.approvals.get().approved_by:
                        glcMR.approved.append(a["user"]["username"])
                    glcUser.mergeRequests.append(glcMR)
        users.append(glcUser)

    if args.merge_requests:
        for u in users:
            print(u.sysID, u.name)
            for mr in u.mergeRequests:
                if not mr.state == "merged":
                    print("  "+mr.title, mr.draft, mr.approved, sep="|")
            print()
    elif args.comment_sheet is not None:
        comments = env.get_template("comments.md")
        if args.comment_sheet > 0:
            try:
                session = config["sessions"][args.comment_sheet-1]
            except IndexError as e:
                parser.error(e)
        else:
            session = None
        print(comments.render(users=users, session=session))
    else:
        keys = ["glUser", "name", "status", "hasKeys", "hasPersonal"]
        print(":".join(keys))
        for u in users:
            print(u.glID, u.name, u.status, u.hasKeys, u.hasPersonal,
                  sep=":")


if __name__ == "__main__":
    main()
