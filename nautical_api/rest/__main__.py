import argparse
from signal import signal, SIGINT, SIGTERM
from threading import Event
from time import sleep
from . import NauticalRestApi, NauticalApp
from logging import getLogger, DEBUG, INFO, WARNING, CRITICAL, ERROR, StreamHandler, Formatter
from sys import stdout
from os import environ


h = StreamHandler(stdout)
# provide a bit more detail on output                                                                                                                                                                   
h.setFormatter(Formatter('[%(levelname)s] [%(asctime)s]: %(message)s'))
getLogger().addHandler(h)


def main():
    """
    Main Entry Point
    """
    parser = argparse.ArgumentParser("")
    parser.add_argument(
        '-l', '--log_level',
        help="Logging level for the application",
        default="WARNING",
        choices=["ERROR", "CRITICAL", "INFO", "DEBUG", "WARNING"]
    )
    parser.add_argument('-p', '--port', help='Port where the app is executed.', default=5000)
    parser.add_argument('-a', '--host', help='Host where the app is executed.', default="localhost")

    args = parser.parse_args()

    getLogger().setLevel({
        "WARNING": WARNING,
        "ERROR": ERROR,
        "CRITICAL": CRITICAL,
        "INFO": INFO,
        "DEBUG": DEBUG
    }.get(args.log_level, WARNING))

    e = Event()
    app = NauticalApp()
    api = NauticalRestApi(app)

    def _stop(*_):
        e.set()

    signal(SIGINT, _stop)
    signal(SIGTERM, _stop)


    port = environ.get("NAUTICAL_REST_API_PORT", args.port)
    
    app.run(debug=args.log_level=="DEBUG", host=args.host, port=port)

    while not e.is_set():
        sleep(1.0)


if __name__ == '__main__':
    main()
