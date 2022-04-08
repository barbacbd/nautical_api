from flask import Flask
from flask_restful import Resource, Api


_AppName = "NauticalRestApi"


class AllSourcesGetter(Resource):

    """
    The class implements the ability or resource that will GET all sources.
    Each source is a contains the IDs of all buoys or stations reported as part of
    the group or source. Please see `nautical.noaa.buoy.source` for more information.
    
    """
    
    def get(self):
        """
        Get the IDs of all sources that have been retrieved from NOAA.

        :return: JSON object in the format {"sources": [] }, where the 
        object will contain a list of ALL Ids of the sources that have been
        retrieved. 
        """



class NauticalRestApi(Api):

    def __init__(self, app):
        """
        

        """

        
    
