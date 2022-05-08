"""
This file will act as the connector script that will be used to pull all
of the data using the nautical library and put the information into
a database

"""
from nautical.io.sources import get_buoy_sources
from nautical.io.buoy import create_buoy
from nautical.noaa.buoy.buoy_data import BuoyData
from nautical.noaa.buoy.source import Source
from json import dumps
from typing import List, Dict, Union, Any
from datetime import datetime
from threading import Event, Timer, Lock
from uuid import uuid4
from logging import getLogger
from singleton_decorator import singleton
from copy import copy
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor, as_completed


log = getLogger()
SOURCE_INDEX = "source_index"
BUOY_INDEX = "buoy_index"


def jsonify_buoy_data(data: Union[List[BuoyData], BuoyData]):
    """

    """
    def _jsonify(_data):
        output = {}
        for x, y in _data:
            if isinstance(y, (int, float, str)):
                output[x] = y
            else:
                output[x] = str(y)
        return output

    if isinstance(data, list):
        return [_jsonify(bd) for bd in data]
    elif data is not None:
        return _jsonify(data)

    
def find_wait_time(t=None):
    """
    Use the current time (minutes) passed the hour to determine the wait time until
    the next expected period. This function should only be needed once as each interval
    will be 30 minutes after the last lookup.

    :param t: Time in minutes currently past the hour, When `None` use datatime
    """
    
    if t is None:
        _t = int(datetime.now().minute)
    else:
        _t = t
    
    m = abs(int(_t) - 65) % 30
    if m == 0:
        return 30
    return m
    
    
@singleton
class NauticalDatabase:
    """Singleton class that will hold the current nautical
    information retrieved through the nautical library.
    """

    def __init__(self):
        self._sources: Dict[str, Any] = {}
        self._buoys: Dict[str, Any] = {}
        self._pull_lock = Lock()
        self._retrieve_lock = Lock()

        self._aliases = {}
        
        self._stop_event = Event()
        self._stop_event.clear()  # force clear the event (if it's set we have a bg problem)
        self._timer = None

        # dict containing the callbacks associated with the hash 
        self._callbacks = {}
        self._callback_lock = Lock()

    def subscribe(self, callback, hsh = str(uuid4())):
        """
        If hash (hsh) does not already exist in the updated callback, the callback will be 
        added assuming it is a function. When an instance of this class updates the information
        stored in the instance, then the registered callbacks will be triggered, notifying a
        reciever to grab the new data.

        :param callback: Callable function in the form of `func()`.
        :param hsh: Hash or unique identifier that is used for this callback
        :return: The hash or unique identifier for the callback, None on failure.
        """
        with self._callback_lock:
            if hsh not in self._callbacks and callable(callback):
                log.debug("{} adding callback with ID {}".format(self.__class__.__name__, hsh))
                self._callbacks[hsh] = callback
                return hsh
        return None

    def unsubscribe(self, hsh):
        """
        Remove a an existing subscription of the hsh matches an entry save in this instance.

        :param hsh: hash or unique identifier of a saved callback
        :return: True when the callback was successfully removed
        """
        with self._callback_lock:
            if hsh in self._callbacks:
                log.debug("{} removing callback with ID {}".format(self.__class__.__name__, hsh))
                self._callbacks.pop(hsh)
                return True
            
        return False
        
    
    def stop(self):
        """
        Stopp the execution of the singleton
        """
        log.debug("Stopping {}".format(self.__class__.__name__))
        self._stop_event.set()

        if self._timer is not None:
            if self._timer.is_alive():
                self._timer.cancel()

            self._timer = None

    def _run(self):
        """
        Internal execution interval for the singleton
        """
        if self._stop_event.is_set():
            log.debug("{} should be stopped, not executing ...".format(self.__class__.__name__))
        else:
            self._pull_all()
            
            # find the next time to run this function
            num_seconds = find_wait_time() * 60.0

            self._timer = Timer(num_seconds, self._run)
            self._timer.start()
        
    def run(self):
        """
        Start and run the Database that will pull the nautical information. The 
        database should run asynchronously.
        """
        log.debug("Starting {}".format(self.__class__.__name__))
        if self._stop_event.is_set():
           log.warning("{} is already running ...".format(self.__class__.__name__))
        else:
            self._run()

    def _pull_all(self):
        """ 
        Convenience function, see `_pull_sources` and `_pull_buoys` for more information.
        """
        self._pull_sources()
        self._pull_buoys()
    
    def _pull_sources(self):
        """
        Pull all source data using the nautical library. The sources
        will NOT include 'SHIPS'.
        """
        log.debug("{} Updating sources".format(self.__class__.__name__))

        sources = get_buoy_sources()
        if "Ships" in sources:
            sources.pop("Ships")
        
        with self._pull_lock:
            log.debug("{} deleting current source data".format(self.__class__.__name__))
            self._sources.clear()
            self._aliases.clear()
            self._sources = sources

            for s in self._sources.keys():
                alias = str(s).replace("/", "_").replace(" ", "_")
                self._aliases[alias] = str(s)
            
            log.debug("{} Updated sources -> {}".format(self.__class__.__name__, self._sources.keys()))

    def _pull_buoys(self):
        """
        Pull all buoy information from the database and add the
        information to the databsae.
        """        
        log.debug("{} Updating buoys".format(self.__class__.__name__))
        if not self._sources:
            self._pull_sources

        with self._pull_lock:
            sources = self._sources.values()

        buoy_ids = []
        # get the flat list of buoy ids
        for s in sources:
            buoy_ids.extend([str(b.station) for b in list(s.buoys.values())])

        with self._pull_lock:
            # this will clear the dict, this will cause us to loose cache which is intended
            self._buoys = dict.fromkeys(buoy_ids, None)
        
        log.debug("{} Updated buoys".format(self.__class__.__name__))

    def get_all_source_ids(self):
        """
        Get all of the IDs of the sources.

        :return: List of all source IDs
        """
        with self._retrieve_lock:
            return list(self._sources.keys())

    def get_aliases(self):
        """
        Get the aliases for the source names. Source names are not in a format that can
        be used for urls, so the aliases are used to match the actual source name to the
        external URL.

        :return: Aliases which include the endpoint name with the source original name
        """
        with self._retrieve_lock:
            return copy(self._aliases)
            
    def get_source(self, source):
        """
        Get the source information for a specific source. The information will include the buoy ids 
        that are a part of the source.

        :param source: ID of the source to retrieve the information from.        
        :return: List of all buoy IDs in the source.
        """
        if source in self._sources:
            with self._retrieve_lock:
                return self._sources[source]

    def get_all_buoy_ids(self):
        """
        Get all of the IDs of the buoys.

        :return: List of all buoy IDs
        """
        with self._retrieve_lock:
            return list(self._buoys.keys())

    def get_buoy(self, buoy):
        """
        Get the buoy object information for a specific buoy. For more detail on the buoy, please
        see `nautical.noaa.buoy.buoy_data`

        :param buoy: ID of the buoy
        :return: nautical.noaa.buoy.BuoyData object
        """
        if buoy in self._buoys:
            with self._retrieve_lock:
                if self._buoys[buoy] is None:

                    try:
                        b = create_buoy(buoy)
                        self._buoys[buoy] = b.present
                    except HTTPError as e:
                        log.warning(e)

                # This will either be None, a buoy (which could be cached
                # if looked up more than once in a time period)
                return self._buoys[buoy]
        return None  # Buoy does not exist
