from flask_restful import Resource
from .connector import NauticalDatabase, jsonify_buoy_data
from logging import getLogger
from threading import Lock
from copy import copy


log = getLogger()


class AllSourcesGetter(Resource):

    """
    The class implements the ability or resource that will GET all sources.
    Each source is a contains the IDs of all buoys or stations reported as part of
    the group or source. Please see `nautical.noaa.buoy.source` for more information.
    """

    __name__ = "sources"

    def get(self):
        """
        Get the IDs of all sources that have been retrieved from NOAA.
                                                                     
        :return: JSON object including all sources and their endpoints
        """
        data = NauticalDatabase().get_aliases()
        return {"sources": [{"id": str(value), "endpoint": str(key)} for key, value in data.items()]}


class SpecificSourceGetter(Resource):

    """
    The class implements the ability or resource that will GET a specific sources.
    Each source is a contains the IDs of all buoys or stations reported as part of
    the group or source. Please see `nautical.noaa.buoy.source` for more information.
    """

    __name__ = "specific_source"

    def get(self, source_id):
        """
        Get the buoys grouped together by this source.
        
        :param source_id: Source to retrieve the information about.
        :return: JSON object including all sources.
        """
        data = NauticalDatabase().get_aliases()
        if source_id not in data:
            log.warning("Specific source queried, no matching data ...")
            return {source_id: []}
        else:
            s = NauticalDatabase().get_source(data[source_id])
            return {str(s): [str(buoy.station) for buoy in s]}

class AllBuoysGetter(Resource):

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

        :return: JSON object including all buoy ids.
        """
        data = NauticalDatabase().get_all_buoy_ids()
        return {"buoys": [bid for bid in data]}


class SpecificBuoyGetter(Resource):

    """
    The class implements the ability or resource that will GET all buoys.
    Each buoy contains the current information registered at the buoy. The
    current information will vary based buoy. The information is updated
    roughly twice/hour. Please see `nautical.noaa.buoy.buoy_data` for
    more information.
    """

    __name__ = "specific_buoy"

    def get(self, buoy_id):
        """
        Get the IDs of all buoys that have been retrievedfrom NOAA.

        :param buoy_id: ID of the buoy to retrieve information about.
        :return: JSON object with all buoy information for a buoy
        """
        data = NauticalDatabase().get_buoy(buoy_id)
        if data is None:
            return {buoy_id: {}}
        else:
            return {buoy_id: jsonify_buoy_data(data)}

