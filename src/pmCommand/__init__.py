import logging
import pmCommand.client  # noqa
import pmCommand.util  # noqa
from pmCommand.core import PMCommand  # noqa


def monkeypatch_logging():
    # register trace logging possibility
    TRACE = 5
    logging.addLevelName(TRACE, 'TRACE')
    setattr(logging, 'TRACE', TRACE)

    def loggerClassTrace(self, msg, *args, **kwargs):
        if self.isEnabledFor(TRACE):
            self._log(TRACE, msg, args, **kwargs)

    setattr(logging.getLoggerClass(), 'trace', loggerClassTrace)

    def rootTrace(msg, *args, **kwargs):
        if logging.root.isEnabledFor(TRACE):
            logging.root._log(TRACE, msg, args, **kwargs)
    setattr(logging, 'trace', rootTrace)


if not hasattr(logging, 'trace'):
    monkeypatch_logging()
