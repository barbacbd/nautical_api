"""
This file will act as the connector script that will be used to pull all
of the data using the nautical library and put the information into
a database

"""
from nautical.io.sources import get_buoy_sources
from nautical.io.buoy import create_buoy
from nautical.noaa.buoy.buoy_data import BuoyData
from nautical.noaa.buoy.source import Source
from elasticsearch import Elasticsearch
from json import dumps
from pprint import pprint
from typing import List, Dict, Union, Any
from datetime import datetime

SOURCE_INDEX = "source_index"
BUOY_INDEX = "buoy_index"


def jsonify_buoy_data(data: Union[List[BuoyData], BuoyData]):
    """

    """
    def _jsonify(_data):
        return {x: y for x, y in _data}

    if isinstance(data, list):
        return [_jsonify(bd) for bd in data]
    else:
        return _jsonify(data)


def _pull_sources_wrapper() -> Dict[str, List[str]]:
    """
    Pull all source data using the nautical library. The sources
    will NOT include 'SHIPS'.

    :return: Dictionary of source IDs with a value of the list of buoy IDs
    associated with the source.
    """
    source_data = {}

    sources = get_buoy_sources()

    for id, source in sources.items():
        if "ships" in str(id).lower():
            # skip the ships
            continue

        source_data[str(id)] = [x.station for x in source.buoys.values()]

    return source_data


def add_sources_to_db(es: Elasticsearch, source_data: Dict[str, List[str]]=None):
    """
    Add the source information to the elastic search database.

    :param es: Elasticsearch object
    :param source_data: When provided, this is a dictionary of source ids with
    the buoy ids associated with the sources. Please see _pull_sources_wrapper()
    for more information.

    :return: The result of the elastic search index creation
    """
    if not source_data:
        source_info = _pull_sources_wrapper()
    else:
        source_info = source_data

    # index the information and add to elastic search database
    result = es.index(index=SOURCE_INDEX, document=source_info)
    return result['result']


def add_buoys_to_db(es: Elasticsearch, source_data: Dict[str, List[str]]=None):
    """
    Add the buoy information to the

    :param es: Elasticsearch object
    :param source_data: When provided, this is expected to be the same dictionary
    returned by _pull_sources_wrapper(). Please see the function for more information.
    The intended use is to get the Buoy IDs contained inside and pull all
    information for those buoys.

    :return: The result of the elastic search index creation
    """

    if not source_data:
        source_info = _pull_sources_wrapper()
    else:
        source_info = source_data

    buoy_ids = []
    # get the flat list of buoy ids
    for values in source_info.values():
        buoy_ids.extend(values)

    buoy_info = {}
    # turn all of the buoy ids into data that was searchable from the web
    for bid in buoy_ids:
        buoy = create_buoy(bid)
        buoy_info[bid] = buoy.present

    # index the information and add to elastic search database
    result = es.index(index=BUOY_INDEX, document=buoy_info)
    return result['result']


def _find_time_to_lookup_interval_minutes(current_minutes):
    """
    Find the time given the current minutes to the next lookup time (minutes).
    The intervals are set for 5 minutes after the hour and 35 minutes after the
    hour to provide NOAA with time to upload the data. NOAA is set to update the
    data every half-hour, but research shows that the data is not always available
    promptly at those intervals.
    """
    return abs(current_minutes - 65) % 30


def find_wait_time():
    """
    Use the current time (minutes) passed the hour to determine the wait time until
    the next expected period. This function should only be needed once as each interval
    will be 30 minutes after the last lookup.
    """
    return _find_time_to_lookup_interval_minutes(datetime.now().minute)



my_es = Elasticsearch()
print(add_sources_to_db(my_es))

# determine if sources already exist