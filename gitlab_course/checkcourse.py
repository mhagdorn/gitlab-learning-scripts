import yaml
from pathlib import Path
import argparse


def check_for_doubles(list1, list2=[]):
    sorted_list = sorted([p.strip().lower() for p in list1 + list2])
    doubles = []
    if len(sorted_list) != len(set(sorted_list)):
        for i in range(1, len(sorted_list)):
            if sorted_list[i] == sorted_list[i - 1]:
                doubles.append(sorted_list[i])
    return doubles


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("course", type=Path,
                        help="the course description file")
    parser.add_argument("--verbose", default=False,
                        action="store_true", help="show course info")
    args = parser.parse_args()

    config = yaml.safe_load(args.course.read_text())

    lists = {}
    for ul in ["participants", "waiting", "cancelled"]:
        if ul in config:
            lists[ul] = config[ul]
        else:
            lists[ul] = []
    if 'max_participants' in config:
        maxp = config['max_participants']
    else:
        maxp = None

    nump = len(lists["participants"])
    numw = len(lists["waiting"])
    numc = len(lists["cancelled"])

    if args.verbose:
        if 'series' in config:
            print(f"series: {config['series']}")
        print(f"name: {config['name']}")
        print(f"number of participants: {nump}", end="")
        if maxp is not None:
            print(f"/{maxp}")
            print(f"number waiting: {numw}")
            print(f"number cancelled: {numc}")
        else:
            print()

    # check for doubles
    errors = ""
    for ul in ["participants", "waiting", "cancelled"]:
        doubles = check_for_doubles(lists[ul])
        if len(doubles) > 0:
            errors += f"List of {ul} is not unique.\n"
            errors += f"{', '.join(doubles)} occur multiple times.\n"
    if len(errors) > 0:
        parser.error(errors[:-1])
    for ul in ["waiting", "cancelled"]:
        doubles = check_for_doubles(lists["participants"], lists[ul])
        if len(doubles) > 0:
            errors += f"people occur in both lists of participants and {ul}.\n"
            errors += f"sort out {', '.join(doubles)}.\n"
    if len(errors) > 0:
        parser.error(errors[:-1])
    doubles = check_for_doubles(lists["waiting"], lists["cancelled"])
    if len(doubles) > 0:
        errors += "people occur in both lists of waiting and cancelled.\n"
        errors += f"sort out {', '.join(doubles)}.\n"
    if len(errors) > 0:
        parser.error(errors[:-1])

    if nump > maxp:
        parser.error(f"More than {maxp} in course. Move "
                     f"the {nump - maxp} "
                     "participants to the waiting list")
    elif nump < maxp and numw > 0:
        parser.error("Some spaces available. Move "
                     f"{min(maxp - nump, numw)} "
                     "participants to participants list")


if __name__ == '__main__':
    main()
