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
from typing import List, Dict


SOURCE_INDEX = "source_index"


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

my_es = Elasticsearch()
print(add_sources_to_db(my_es))





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

    buoy_info = {}
    # turn all of the buoy ids into data that was searchable from the web

    # Add json properties to all classes in Nautical


    # index the information and add to elastic search database
    result = es.index(index=SOURCE_INDEX, document=source_info)
    return result['result']


# determine if sources already exist