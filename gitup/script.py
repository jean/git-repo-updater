# -*- coding: utf-8  -*-
#
# Copyright (C) 2011-2014 Ben Kurtovic <ben.kurtovic@gmail.com>
# See the LICENSE file for details.

from __future__ import print_function

import argparse

from colorama import init as color_init, Style

from . import __version__, __email__
from .config import (get_bookmarks, add_bookmarks, delete_bookmarks,
                     list_bookmarks)
from .update import update_bookmarks, update_directories

def main():
    """Parse arguments and then call the appropriate function(s)."""
    parser = argparse.ArgumentParser(
        description="""Easily update multiple git repositories at once.""",
        epilog="""
            Both relative and absolute paths are accepted by all arguments.
            Questions? Comments? Email the author at {0}.""".format(__email__),
        add_help=False)

    group_u = parser.add_argument_group("updating repositories")
    group_b = parser.add_argument_group("bookmarking")
    group_m = parser.add_argument_group("miscellaneous")
    rebase_or_merge = group_u.add_mutually_exclusive_group()

    group_u.add_argument(
        'directories_to_update', nargs="*", metavar="path",
        help="""update all repositories in this directory (or the directory
                itself, if it is a repo)""")
    group_u.add_argument(
        '-u', '--update', action="store_true", help="""update all bookmarks
        (default behavior when called without arguments)""")
    group_u.add_argument(
        '-c', '--current-only', action="store_true", help="""only fetch the
        remote tracked by the current branch instead of all remotes""")
    rebase_or_merge.add_argument(
        '-r', '--rebase', action="store_true", help="""always rebase upstream
        branches instead of following `pull.rebase` and `branch.<name>.rebase`
        in git config (like `git pull --rebase=preserve`)""")
    rebase_or_merge.add_argument(
        '-m', '--merge', action="store_true", help="""like --rebase, but merge
        instead""")

    group_b.add_argument(
        '-a', '--add', dest="bookmarks_to_add", nargs="+", metavar="path",
        help="add directory(s) as bookmarks")
    group_b.add_argument(
        '-d', '--delete', dest="bookmarks_to_del", nargs="+", metavar="path",
        help="delete bookmark(s) (leaves actual directories alone)")
    group_b.add_argument(
        '-l', '--list', dest="list_bookmarks", action="store_true",
        help="list current bookmarks")
    group_m.add_argument(
        '-h', '--help', action="help", help="show this help message and exit")
    group_m.add_argument(
        '-v', '--version', action="version",
        version="gitup version " + __version__)

    color_init(autoreset=True)
    args = parser.parse_args()
    update_args = args.current_only, args.rebase, args.merge

    print(Style.BRIGHT + "gitup" + Style.RESET_ALL + ": the git-repo-updater")
    print()

    acted = False
    if args.bookmarks_to_add:
        add_bookmarks(args.bookmarks_to_add)
        acted = True
    if args.bookmarks_to_del:
        delete_bookmarks(args.bookmarks_to_del)
        acted = True
    if args.list_bookmarks:
        list_bookmarks()
        acted = True
    if args.directories_to_update:
        update_directories(args.directories_to_update, update_args)
        acted = True
    if args.update or not acted:
        update_bookmarks(get_bookmarks(), update_args)

def run():
    """Thin wrapper for main() that catches KeyboardInterrupts."""
    try:
        main()
    except KeyboardInterrupt:
        print("Stopped by user.")
