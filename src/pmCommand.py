#!/usr/bin/env python3
#
# Copyright 2014 Mendix
# MIT license, see LICENSE

import argparse
import cmd
import logging
import sys
import pmCommand
import getpass


class CLI(cmd.Cmd):
    def __init__(self, baseurl, username):
        cmd.Cmd.__init__(self)
        self._baseurl = baseurl
        self._username = username
        self._pmCommand = pmCommand.PMCommand()
        self._sort = True
        self.prompt = "pmCommand# "

    def cmdloop_handle_ctrl_c(self):
        quit = False
        while quit is not True:
            try:
                self.cmdloop()
                quit = True
            except KeyboardInterrupt:
                print()

    def onecmd(self, line):
        try:
            return super(CLI, self).onecmd(line)
        except pmCommand.Error as e:
            logging.error(e)

    def do_login(self, args):
        password = getpass.getpass("Enter password for {}: ".format(self._username))
        self._pmCommand.login(self._baseurl, self._username, password)
        logging.debug("Session idle timeout: {}".format(
            self._pmCommand.get_session_idle_timeout()))
        logging.info("{} - {}".format(self._pmCommand.product, self._pmCommand.welcome))

    def do_logout(self, args):
        self._pmCommand.logout()

    def do_sort(self, args):
        self._sort = not self._sort
        logging.info("Sorted output is now {}.".format("on" if self._sort else "off"))

    def do_listipdus(self, args):
        pdus = self._pmCommand.listipdus()
        fields, headers = self._pmCommand.listipdus_table_info()
        self._print_table(fields, headers, pdus)

    def do_status(self, args):
        if args == "" or args == "all":
            outlets = self._pmCommand.status()
        else:
            outlets = self._pmCommand.status(self.parse_outlet_args(args))
        fields, headers = self._pmCommand.status_table_info()
        self._print_table(fields, headers, outlets)

    def outlet_action(self, action, args):
        for pdu_id, outlet_id in self.parse_outlet_args(args):
            self._pmCommand.outlet_action(action, pdu_id, outlet_id)

    def parse_outlet_args(self, args):
        # split arg text into list of tuples with pdu_id, outlet_id
        # e.g.  'power3[7],power5[7]' -> [('power3', '7'), ('power5', '7')]
        pdu_outlet_tuples = []  # list of tuples (pdu_id, outlet_id)
        if args != '':
            pdu_outlets = [x.strip() for x in args.split(',')]
            for pdu_outlet in pdu_outlets:
                pdu_outlet_tuples.append(pmCommand.util.parse_outlet(pdu_outlet))
        else:
            logging.error("No outlet specified.")
        return pdu_outlet_tuples

    def do_on(self, args):
        self.outlet_action("on", args)

    def do_off(self, args):
        self.outlet_action("off", args)

    def do_lock(self, args):
        self.outlet_action("lock", args)

    def do_unlock(self, args):
        self.outlet_action("unlock", args)

    def do_cycle(self, args):
        self.outlet_action("cycle", args)

    def do_save(self, args):
        self._pmCommand.save()

    def _print_table(self, fields, headers, rows):
        if self._sort:
            rows = sorted(rows)

        print()

        output = ['']
        maxlen = {}
        for field in fields:
            maxlen[field] = max(len(headers[field]),
                                max([len(row.label[field]) for row in rows]))
            output.append(headers[field].ljust(maxlen[field]))
        print('  '.join(output))

        output = ['']
        for field in fields:
            output.append('=' * maxlen[field])
        print('  '.join(output))

        for row in rows:
            output = ['']
            for field in fields:
                output.append(row.label[field].ljust(maxlen[field]))
            print('  '.join(output))

        print()

    def do_exit(self, args):
        self.do_logout(None)
        return -1

    def do_quit(self, args):
        self.do_logout(None)
        return -1

    def do_EOF(self, args):
        print("exit")
        self.do_logout(None)
        return -1

    # if the emptyline function is not defined, Cmd will automagically
    # repeat the previous command given, and that's not what we want
    def emptyline(self):
        pass

    def do_help(self, args):
        print("""pmCommand strikes back!

Available commands:
 login              Provide password to get a new session at the appliance.
 logout             Logout from the appliance.
 sort               Toggle sorted output for pdu and outlet list
 exit               Exits from the application.
 help               Displays the list of commands.
 listipdus          Lists the IPDUs connected to the appliance.
 on                 Turns on outlets defined in <outlet list>.
 off                Turns off outlets defined in <outlet list>.
 cycle              Power cycles outlets defined in <outlet list>.
 lock               Locks outlets defined in <outlet list> in current state.
 unlock             Unlocks outlets define in <outlet list>.
 status             Displays status of outlets defined in <outlet list>.
 save               Saves configuration to flash.
""")

        print("Hint: use tab autocompletion for commands!")


def start_logging(verbose, quiet):
    verbosity = quiet - verbose
    verbosity = verbosity * 10 + 20
    if verbosity > 50:
        verbosity = 100
    if verbosity < 5:
        verbosity = 5

    class LogFilter(logging.Filter):
        def __init__(self, level, ge):
            self.level = level
            # log levels greater than and equal to (True), or below (False)
            self.ge = ge

        def filter(self, record):
            if self.ge:
                return record.levelno >= self.level
            return record.levelno < self.level

    logformatting = "%(levelname)s - %(message)s"
    consolelogformatter = logging.Formatter(logformatting)

    # log everything below ERROR to to stdout
    stdoutlog = logging.StreamHandler(sys.stdout)
    stdoutlog.setFormatter(consolelogformatter)
    stdoutfilter = LogFilter(logging.ERROR, False)
    stdoutlog.addFilter(stdoutfilter)
    stdoutlog.setLevel(verbosity)

    # log everything that's ERROR and more serious to stderr
    stderrlog = logging.StreamHandler(sys.stderr)
    stderrlog.setFormatter(consolelogformatter)
    stderrfilter = LogFilter(logging.ERROR, True)
    stderrlog.addFilter(stderrfilter)
    stderrlog.setLevel(verbosity)

    rootlogger = logging.getLogger()
    rootlogger.setLevel(0)
    rootlogger.addHandler(stdoutlog)
    rootlogger.addHandler(stderrlog)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase verbosity of output (-vv to be even more verbose)"
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="count",
        default=0,
        help="decrease verbosity of output (-qq to be even more quiet)"
    )
    parser.add_argument(
        '-u',
        '--user',
        default='admin',
        help="username to log in with",
    )
    parser.add_argument(
        'baseurl',
        help="Base url of the appliance, e.g. http://10.13.3.7",
    )
    args = parser.parse_args()
    start_logging(args.verbose, args.quiet)

    cli = CLI(args.baseurl, args.user)
    cli.onecmd("login")
    cli.cmdloop_handle_ctrl_c()


if __name__ == '__main__':
    main()
