from flask import Flask
from flask_restful import Resource, Api
from .connector import NauticalDatabase
from logging import getLogger
from threading import Lock
from copy import copy


log = getLogger()


class _BaseNauticalResource(Resource):

    def __init__(self):
        self.callback_id = NauticalDatabase().subscribe(self.resource_update)
        self.resource_lock = Lock()

    def resource_update(self):
        """
        Base function to receive updates from the database. Each child class should
        implement this function to receive updates and handle the updates appropriately.
        """
        raise NotImplementedError("{} does not implement resource_update".format(self.__class__.__name__))


class _AllSourcesGetter(Resource):

    """
    The class implements the ability or resource that will GET all sources.
    Each source is a contains the IDs of all buoys or stations reported as part of
    the group or source. Please see `nautical.noaa.buoy.source` for more information.
    """

    __name__ = "sources"
    
    def get(self):
        """
        Get the IDs of all sources that have been retrieved from NOAA.

        :return: JSON object in the format {"sources": [] }, where the 
        object will contain a list of ALL Ids of the sources that have been
        retrieved. 
        """
        data = NauticalDatabase().get_aliases()        
        return {"sources": [{"id": str(value), "endpoint": str(key)} for key, value in data.items()]}

class _SpecificSourceGetter(Resource):

    """
    The class implements the ability or resource that will GET a specific sources.
    Each source is a contains the IDs of all buoys or stations reported as part of
    the group or source. Please see `nautical.noaa.buoy.source` for more information.
    """

    __name__ = "specific_source"
    
    def get(self, source_id):
        """
        Get the buoys grouped together by this source.

        :return: JSON object in the format {"source_id": [] }, where the 
        object will contain a list of ALL buoy Ids of the source that have been
        retrieved. 
        """
        data = NauticalDatabase().get_aliases()
        if source_id not in data:
            log.warning("Specific source queried, no matching data ...")
            return {source_id: []}
        else:
            s = NauticalDatabase().get_source(data[source_id])
            return {str(s): [str(buoy.station) for buoy in s]}

class _AllBuoysGetter(Resource):

    """ 
    The class implements the ability or resource that will GET all buoys.
    Each buoy contains the current information registered at the buoy. The
    current information will vary based buoy. The information is updated
    roughly twice/hour. Please see `nautical.noaa.buoy.buoy_data` for 
    more information.
    """

    __name__ = "buoys"
    
    def get(self):
        """
        Get the IDs of all buoys that have been retrievedfrom NOAA.

        :return: JSON object in the format {"buoys": [] }, where the
        object will contain a list of ALL Ids of the buoys that have 
        been retrieved.
        """
        data = NauticalDatabase().get_all_buoy_ids()
        return {"buoys": [b.station for b in data]}
        

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
        self.resources["/sources"] = _AllSourcesGetter()
        self.resources["/sources/<string:source_id>"] = _SpecificSourceGetter()
        self.resources["/buoys"] = _AllBuoysGetter()
        
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
