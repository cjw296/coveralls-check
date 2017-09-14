from __future__ import print_function
from argparse import ArgumentParser
import requests
import sys

url = 'https://coveralls.io/builds/{}.json'


def message(args, covered, template):
    print(template.format(
        args.commit, covered, args.fail_under
    ))


def get_coverage(commit):
    response = requests.get(url.format(commit))
    data = response.json()
    return data['covered_percent']


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('commit', help='the commit hash to check')
    parser.add_argument('--fail-under', type=float, default=100,
                        help='Exit with a status of 2 if the total coverage is '
                             'less than MIN.')
    return parser.parse_args()


def main():
    args = parse_args()
    covered = get_coverage(args.commit)

    if covered < args.fail_under:
        message(args, covered, 'Failed coverage check for {} as {} < {}')
        sys.exit(2)
    else:
        message(args, covered, 'Coverage OK for {} as {} >= {}')

