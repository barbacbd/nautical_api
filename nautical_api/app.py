import argparse
from signal import signal, SIGINT, SIGTERM
from threading import Event
from time import sleep
from logging import getLogger, DEBUG, INFO, WARNING, CRITICAL, ERROR, StreamHandler, Formatter
from sys import stdout
from os import environ
from flask import Flask
from flask_restful import Api
from .resources import *
from .connector import NauticalDatabase


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

    def handle_shutdown(*_, has_shutdown=False):
        log.debug("Stopping database ...")
        NauticalDatabase().stop()
        log.debug("Exiting ...")
        # Ensure that the flask app is shutdown, this is the call that will
        # ultimately cause the reentrant
        exit(0)
            
        
    # only handle the Ctrl-C 
    signal(SIGINT, handle_shutdown)
    
    # Start the database that will run in the background
    NauticalDatabase().run()
    app = Flask("nautical_rest_api")
    api = Api(app)

    # Add all resources to the api
    api.add_resource(AllSourcesGetter(), "/sources")
    api.add_resource(SpecificSourceGetter(), "/sources/<string:source_id>")
    api.add_resource(AllBuoysGetter(), "/buoys")
    api.add_resource(SpecificBuoyGetter(), "/buoys/<string:buoy_id>")

    port = environ.get("NAUTICAL_REST_API_PORT", args.port)

    if args.log_level == "DEBUG":
        # this is redundant, but providing an extra level for other app uses
        app.run(debug=args.log_level=="DEBUG", host=args.host, port=port)
    else:
        from waitress import serve

        # name localhost is not support, causing OSError with sockets. use 0.0.0.0 in
        # place of localhost
        host = args.host if args.host.lower() != "localhost" else "0.0.0.0"
        serve(app, host=host, port=args.port)

if __name__ == '__main__':
    main()
