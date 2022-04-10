from flask import Flask
from flask_restful import Resource, Api
from .connector import NauticalDatabase
from logging import getLogger


log = getLogger()


class _BaseNauticalResource(Resource):

    def __init__(self, db):
        """
        :param db: The instance of the NauticalDatabase that is used by the Flask App
        """
        self.callback_id = None
        if db is not None:
            self.callback_id = db.subscribe(self.resource_update)

    def resource_update(self):
        """
        Base function to receive updates from the database. Each child class should
        implement this function to receive updates and handle the updates appropriately.
        """
        raise NotImplementedError("{} does not implement resource_update".format(self.__class__.__name__))


class _AllSourcesGetter(_BaseNauticalResource):

    """
    The class implements the ability or resource that will GET all sources.
    Each source is a contains the IDs of all buoys or stations reported as part of
    the group or source. Please see `nautical.noaa.buoy.source` for more information.
    """
    
    def __init__(self, db):

        # make sure these exist before super() in the unlikely event that
        # the update occurs immediately.
        self._source_ids = []
        
        super().__init__(db)
        
        
    def resource_update(self):
        pass
    
    def get(self):
        """
        Get the IDs of all sources that have been retrieved from NOAA.

        :return: JSON object in the format {"sources": [] }, where the 
        object will contain a list of ALL Ids of the sources that have been
        retrieved. 
        """
        pass

class _AllBuoysGetter(Resource):

    """ 
    The class implements the ability or resource that will GET all buoys.
    Each buoy contains the current information registered at the buoy. The
    current information will vary based buoy. The information is updated
    roughly twice/hour. Please see `nautical.noaa.buoy.buoy_data` for 
    more information.
    """

    def get(self):
        """
        Get the IDs of all buoys that have been retrievedfrom NOAA.

        :return: JSON object in the format {"buoys": [] }, where the
        object will contain a list of ALL Ids of the buoys that have 
        been retrieved.
        """
        pass
        

class NauticalApp(Flask):

    def __init__(self, import_name="NauticalRestApi"):
        """
        See `flask.Flask` for more information.

        :param import_name: Name of the application name
        """
        super().__init__(import_name)

        self._resources = []
        self._database = NauticalDatabase()
        self._saved_callback_id = self._database.subscribe(self._database_updated_callback)

        if self._saved_callback_id is None:
            log.error("Failed to register callback")

    def _database_updated_callback(self):
        """
        Callback function used to receive notifications that the database has been updated.
        Get all public information from the database and update
        """
        pass

    @property
    def resources(self):
        """
        Get all of the resources that have been generated.

        See `flask_restful.Resource` for more information about resources.

        :return: The currently available resources
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
        
