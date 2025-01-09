import gitlab
import yaml
from pathlib import Path


def name2path(name):
    """normalise a name

    normalise a name by replacing spaces with dashes and
    making it all lower case.
    """
    return name.lower().replace(" ", "-")


def get_group(gl, group_name, parent_group=None, create=False):
    group_name = str(group_name)
    for group in gl.groups.list(
            search=group_name, include_subgroups=False, iterator=True):
        if group.name == group_name:
            if parent_group is not None:
                if group.parent_id != parent_group.id:
                    raise RuntimeError(
                        f"the parent id {group.parent_id} does not match the "
                        f"id of the parent group {parent_group.name}")
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
                    "allowed_to_merge":  [
                        {'access_level': 30},
                        {'access_level': 40}]},
            }
            if parent_group is not None:
                new_group["parent_id"] = parent_group.id
            group = gl.groups.create(new_group)
        else:
            raise RuntimeError(f"no such group {group_name}")
    return group


def main():
    cname = "course.yml"
    config = yaml.safe_load(Path(cname).read_text())
    print(config)

    if 'gitlab' in config:
        gitlab_id = config['gitlab']
    else:
        gitlab_id = None
    gl = gitlab.Gitlab.from_config(gitlab_id=gitlab_id)
    gl.auth()

    course_group = get_group(gl, config["name"])
    year_group = get_group(gl, config["year"], parent_group=course_group)

    print(course_group)
    print(year_group)


if __name__ == '__main__':
    main()
