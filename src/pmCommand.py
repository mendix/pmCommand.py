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


class CLI(cmd.Cmd, object):

    def __init__(self, user_at_host):
        logging.debug("Using pmCommand version {}".format(pmCommand.__version__))
        cmd.Cmd.__init__(self)
        (self._username, self._host) = user_at_host.split('@')
        self._pmCommand = pmCommand.PMCommand()
        self._sort = True

    def onecmd(self, line):
        try:
            return super(CLI, self).onecmd(line)
        except RuntimeError as re:
            logging.error(re.message)
        except KeyboardInterrupt:
            print

    def do_login(self, args):
        password = getpass.getpass("Enter password for %s@%s: " %
                                   (self._username, self._host))
        success = self._pmCommand.login(self._host,
                                        self._username,
                                        password)
        if success:
            logging.debug("Session idle timeout: {}".format(
                self._pmCommand.get_session_idle_timeout()))
            self.prompt = "pmCommand(%s): " % self._host

    def do_logout(self, args):
        self._pmCommand.logout()

    def do_sort(self, args):
        self._sort = not self._sort
        logging.info("Sorted output is now {}.".format("on" if self._sort else "off"))

    def do_listipdus(self, args):
        pdus = self._pmCommand.listipdus()
        (fields, headers) = self._pmCommand.listipdus_table_info()
        self._print_table(fields, headers, pdus)

    def do_status(self, args):
        if args == "" or args == "all":
            outlets = self._pmCommand.status()
        else:
            outlets = self._pmCommand.status(self.parse_outlet_args(args))
        (fields, headers) = self._pmCommand.status_table_info()
        self._print_table(fields, headers, outlets)

    def outlet_action(self, action, args):
        for (pdu_id, outlet_id) in self.parse_outlet_args(args):
            self._pmCommand.outlet_action(action, pdu_id, outlet_id)

    def parse_outlet_args(self, args):
        pdu_outlet_tuples = []
        if args != '':
            pdu_outlets = [x.strip() for x in args.split(',')]
            for pdu_outlet in pdu_outlets:
                (pdu_id, outlet_id) = pmCommand.util.parse_outlet(pdu_outlet)
                if pdu_id is not None and outlet_id is not None:
                    pdu_outlet_tuples.append((pdu_id, outlet_id))
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

        print

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

        print

    def do_exit(self, args):
        self.do_logout(None)
        return -1

    def do_quit(self, args):
        self.do_logout(None)
        return -1

    def do_EOF(self, args):
        self.do_logout(None)
        print
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
        'user_host',
        help="<user>@<host>, e.g. admin@10.13.3.7"
    )
    args = parser.parse_args()
    start_logging(args.verbose, args.quiet)

    cli = CLI(args.user_host)
    try:
        cli.onecmd("login")
        cli.cmdloop()
    except KeyboardInterrupt:
        print("^C")
        sys.exit(130)  # 128 + SIGINT


if __name__ == '__main__':
    main()
