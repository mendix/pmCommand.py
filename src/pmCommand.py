#!/usr/bin/python
#
# Copyright (c) 2014, Mendix bv
# All Rights Reserved.
#
# http://www.mendix.com/
#

import cmd
import sys
import pprint
import pmCommand

from pmCommand import logger


class CLI(cmd.Cmd):

    def __init__(self, yaml_files=None):
        logger.debug('Using pmCommand version %s' % pmCommand.__version__)
        cmd.Cmd.__init__(self)
        self._pmCommand = pmCommand.PMCommand()

    def do_login(self, args):
        (username, password) = args.split()
        self._pmCommand.login(username, password)

    def do_listipdus(self, args):
        pdus = self._pmCommand.listipdus()
        pprint.pprint(pdus)

    def do_exit(self, args):
        return -1

    def do_quit(self, args):
        return -1

    def do_EOF(self, args):
        print
        return -1

    # if the emptyline function is not defined, Cmd will automagically
    # repeat the previous command given, and that's not what we want
    def emptyline(self):
        pass

    def do_help(self, args):
        print("""pmCommand strikes back!

Available commands:
 login <url> <username> <password>
""")

        print("Hint: use tab autocompletion for commands!")

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option(
        "-c",
        action="append",
        type="string",
        dest="yaml_files"
    )
    parser.add_option(
        "-v",
        "--verbose",
        action="count",
        dest="verbose",
        help="increase verbosity of output (-vv to be even more verbose)"
    )
    parser.add_option(
        "-q",
        "--quiet",
        action="count",
        dest="quiet",
        help="decrease verbosity of output (-qq to be even more quiet)"
    )
    (options, args) = parser.parse_args()

    # how verbose should we be? see
    # http://docs.python.org/release/2.7/library/logging.html#logging-levels
    verbosity = 0
    if options.quiet:
        verbosity = verbosity + options.quiet
    if options.verbose:
        verbosity = verbosity - options.verbose
    verbosity = verbosity * 10 + 20
    if verbosity > 50:
        verbosity = 100
    if verbosity < 5:
        verbosity = 5
    logger.setLevel(verbosity)

    cli = CLI(yaml_files=options.yaml_files)
    if args:
        cli.onecmd(' '.join(args))
    else:
        try:
            cli.cmdloop()
        except KeyboardInterrupt:
            print("^C")
            sys.exit(130)  # 128 + SIGINT
