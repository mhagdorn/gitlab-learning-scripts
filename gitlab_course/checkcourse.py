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

    maxp = config['max_participants']
    nump = len(config['participants'])
    numw = len(config['waiting'])
    numc = len(config['cancelled'])

    if args.verbose:
        print(f"series: {config['series']}")
        print(f"name: {config['name']}")
        print(f"number of participants: {nump}/{maxp}")
        print(f"number waiting: {numw}")
        print(f"number cancelled: {numc}")

    # check for doubles
    errors = ""
    for ul in ["participants", "waiting", "cancelled"]:
        doubles = check_for_doubles(config[ul])
        if len(doubles) > 0:
            errors += f"List of {ul} is not unique.\n"
            errors += f"{', '.join(doubles)} occur multiple times.\n"
    if len(errors) > 0:
        parser.error(errors[:-1])
    for ul in ["waiting", "cancelled"]:
        doubles = check_for_doubles(config["participants"], config[ul])
        if len(doubles) > 0:
            errors += f"people occur in both lists of participants and {ul}.\n"
            errors += f"sort out {', '.join(doubles)}.\n"
    if len(errors) > 0:
        parser.error(errors[:-1])
    doubles = check_for_doubles(config["waiting"], config["cancelled"])
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
