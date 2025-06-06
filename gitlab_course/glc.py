__all__ = ["GitlabCourse"]

import gitlab


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

    def getUser(self, name):
        user = self.gl.users.list(username=name)
        if len(user) == 0:
            user = self.gl.search(gitlab.const.SearchScope.USERS, name)
            if len(user) > 0:
                user = self.gl.users.list(username=user[0]["username"])
        if len(user) > 0:
            return user[0]
