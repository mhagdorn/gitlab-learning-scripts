__all__ = ["GitlabCourse"]

import gitlab
from dataclasses import dataclass, field


@dataclass
class GLCMergeRequest:
    author: str
    title: str
    state: str
    draft: bool
    approved: list[str] = field(default_factory=list)

    @classmethod
    def from_gl(cls, mr):
        glcMR = cls(mr.author["username"], mr.title, mr.state, mr.draft)
        for a in mr.approvals.get().approved_by:
            glcMR.approved.append(a["user"]["username"])
        return glcMR


@dataclass
class GLCUser:
    sysID: str
    glID: str = ''
    _ID: int = -1
    name: str = ''
    status: str = ''
    hasKeys: bool = False

    @classmethod
    def from_gl(cls, user, glu=None):
        glcUser = cls(user)
        if glu is not None:
            glcUser._ID = glu.id
            glcUser.glID = glu.username
            glcUser.name = glu.name
            glcUser.status = glu.state
            glcUser.hasKeys = len(glu.keys.list()) > 0
        return glcUser


def name2path(name):
    """normalise a name

    normalise a name by replacing spaces with dashes and
    making it all lower case.
    """
    return name.lower().replace(" ", "-")


class GitlabCourse:
    def __init__(self, gitlab_id=None):
        self._gl = gitlab.Gitlab.from_config(gitlab_id=gitlab_id)
        self.gl.auth()

    @property
    def gl(self):
        return self._gl

    def get_group(self, group_name, parent_group=None, create=False):
        group_name = str(group_name)
        for group in self.gl.groups.list(
                search=group_name, include_subgroups=False, iterator=True):
            if group.name == group_name:
                if parent_group is not None:
                    if group.parent_id != parent_group.id:
                        continue
                break
        else:
            if create:
                new_group = {
                    "name": group_name,
                    "path": name2path(group_name),
                    "default_branch": "main",
                    "request_access_enabled": False,
                    "visibility": "private",
                    "default_branch_protection_defaults": {
                        "allowed_to_push": [
                            {'access_level': 30},
                            {'access_level': 40}],
                        "allow_force_push": False,
                        "allowed_to_merge": [
                            {'access_level': 30},
                            {'access_level': 40}]},
                }
                if parent_group is not None:
                    new_group["parent_id"] = parent_group.id
                group = self.gl.groups.create(new_group)
            else:
                raise RuntimeError(f"no such group {group_name}")
        return group

    def getUser(self, name, raw=False):
        user = self.gl.users.list(username=name)
        if len(user) == 0:
            user = self.gl.search(gitlab.const.SearchScope.USERS, name)
            if len(user) > 0:
                user = self.gl.users.list(username=user[0]["username"])
        if len(user) > 0:
            user = user[0]
        else:
            user = None
        if raw:
            return user
        else:
            return GLCUser.from_gl(name, user)

    def getUserList(self, users, raw=False):
        user_list = []
        for u in users:
            user = self.getUser(u, raw=raw)
            if raw:
                if user is None:
                    user_list.append((None, u))
                else:
                    user_list.append((user.name, user.username))
            else:
                user_list.append(user)
        return user_list

    def getMergeRequests(self, project):
        for mr in project.mergerequests.list():
            yield GLCMergeRequest.from_gl(mr)
