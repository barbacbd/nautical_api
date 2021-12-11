import argparse
from signal import signal, SIGINT, SIGTERM
from threading import Event
from time import sleep
from .db import NauticalDatabase
from logging import getLogger, DEBUG, INFO, WARNING, CRITICAL, ERROR, StreamHandler, Formatter
from sys import stdout

h = StreamHandler(stdout)
# provide a bit more detail on output                                                                                                                                                                   
h.setFormatter(Formatter('[%(levelname)s] [%(asctime)s]: %(message)s'))
getLogger().addHandler(h)


def main():
    """
    Main Entry Point
    """
    parser = argparse.ArgumentParser("Add nautical data to a backend database to construct the Nautical API.")
    parser.add_argument(
        "-i", "--retry_interval",
        type=int,
        help='Number of seconds to wait before retrying on failed database connections',
        default=60
    )
    parser.add_argument(
        '-l', '--log_level',
        help="Logging level for the application",
        default="WARNING",
        choices=["ERROR", "CRITICAL", "INFO", "DEBUG", "WARNING"]
    )

    args = parser.parse_args()

    getLogger().setLevel({
        "WARNING": WARNING,
        "ERROR": ERROR,
        "CRITICAL": CRITICAL,
        "INFO": INFO,
        "DEBUG": DEBUG
    }.get(args.log_level, WARNING))

    NauticalDatabase.retry_interval_seconds = args.retry_interval

    e = Event()
    app = NauticalDatabase()

    def _stop(*_):
        e.set()

    signal(SIGINT, _stop)
    signal(SIGTERM, _stop)

    app.start()

    while not e.is_set():
        sleep(1.0)

    app.shutdown()

if __name__ == '__main__':
    main()