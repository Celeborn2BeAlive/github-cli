import github
import sys
import argparse
import os
import logging
import urllib

TOKEN_ENV_VAR = 'C2BA_GITHUB_TOKEN'
GITHUB_BASE_URL = 'https://github.com/'


def main():
    args, args_parser = parse_cli_args()

    init_logging(args.log_file)
    if not args.token and TOKEN_ENV_VAR in os.environ:
        args.token = os.environ[TOKEN_ENV_VAR]

    if not args.token:
        logging.error(
            f'No github API token provided, please fill {TOKEN_ENV_VAR} env var of provide it on the command line with --token')
        exit(1)

    if not args.action:
        args_parser.print_help()
        exit(1)

    g = github.Github(args.token)
    user = g.get_user()

    if args.action == 'create-repo':
        try:
            repo = user.create_repo(args.name, description=args.desc)
        except Exception as e:
            logging.error(f"Unable to create repository {args.name}: {e}")
            exit(1)
        logging.info(
            f'Succesfully created repository {urllib.parse.urljoin(GITHUB_BASE_URL, repo.full_name)}')
    if args.action == 'delete-repo':
        try:
            repo = user.get_repo(args.name)
            repo.delete()
        except Exception as e:
            logging.error(f"Unable to delete repository {args.name}: {e}")
            exit(1)
        logging.info(f'Succesfully deleted repository {args.name}')


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description='Command line interface for github.')
    parser.add_argument(
        '--token', type=str, help=f'Github OAuth token. Override environment variable {TOKEN_ENV_VAR}.')
    parser.add_argument('-l', '--log-file', help='Path to log file.')

    commands = parser.add_subparsers(title='commands', dest='action')

    action_parser = commands.add_parser('create-repo')
    action_parser.add_argument('name', help='Name of the repository')
    action_parser.add_argument(
        '--desc', help='Description for the repository')

    action_parser = commands.add_parser('delete-repo')
    action_parser.add_argument('name', help='Name of the repository')

    return parser.parse_args(), parser


def init_logging(log_file=None):
    if log_file:
        if os.path.splitext(log_file)[1] == '.html':
            logging.basicConfig(filename=log_file, filemode='w',
                                format='%(asctime)s - %(levelname)s - %(message)s<br>', level=logging.INFO)
        else:
            logging.basicConfig(filename=log_file, filemode='w',
                                format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
        logging.debug(f'Logging to file {log_file}')
    else:
        logging.basicConfig(
            format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
        logging.debug('Logging to standard output')


if __name__ == "__main__":
    main()
