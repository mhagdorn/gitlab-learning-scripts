import yaml
from pathlib import Path
import argparse


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

    participants = sorted([p.strip().lower() for p in config['participants']])

    if args.verbose:
        print(f"series: {config['series']}")
        print(f"name: {config['name']}")
        print(f"number of participants: {nump}/{maxp}")
        print(f"number waiting: {numw}")
        print(f"number cancelled: {numc}")

    if len(participants) != len(set(participants)):
        doubles = []
        for i in range(1, nump):
            if participants[i] == participants[i - 1]:
                doubles.append(participants[i])
        parser.error("List of participants is not unique.\n "
                     f"{', '.join(doubles)} occur multiple times.")
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
