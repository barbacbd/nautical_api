from flask import Flask
from flask_restful import Api
from ..connector import NauticalDatabase
from logging import getLogger
from threading import Lock
from copy import copy
from .resources import *

log = getLogger()


class NauticalApp(Flask):

    def __init__(self, import_name="NauticalRestApi"):
        """
        See `flask.Flask` for more information.

        :param import_name: Name of the application name
        """
        super().__init__(import_name)

        self.resources = {}
        self._database = NauticalDatabase()
        self._saved_callback_id = self._database.subscribe(self._database_updated_callback)

        if self._saved_callback_id is None:
            log.error("Failed to register callback")

        self._init_resources()

        NauticalDatabase().run()

    def _init_resources(self):
        """

        """
        self.resources["/sources"] = AllSourcesGetter()
        self.resources["/sources/<string:source_id>"] = SpecificSourceGetter()
        self.resources["/buoys"] = AllBuoysGetter()
        self.resources["/buoys/<string:buoy_id>"] = SpecificBuoyGetter()
        
    def _database_updated_callback(self):
        """
        Callback function used to receive notifications that the database has been updated.
        Get all public information from the database and update
        """
        pass

    def run(self, debug=False):
        """
        Override of the run method from the base class.
        """
        super().run(debug=debug)

        
class NauticalRestApi(Api):

    def __init__(self, app):
        """
        See `flask_restful.Api` for more information 

        :param app: The Flask Application Object
        """
        super().__init__(app)
        
        for link, resource in app.resources.items():
            self.add_resource(copy(resource), link)
