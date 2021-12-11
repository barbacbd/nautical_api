from os.path import dirname, exists, abspath
from json import load
from threading import Timer
from logging import getLogger
from time import sleep
from datetime import datetime
from mysql.connector import Error as MySQLError
from mysql.connector import connect


# Create the base logging instance.
log = getLogger()


def get_wait_time():
    """                                                                                                                                                                                                     
    Find how long to wait until the next update                                                                                                                                                             
    """
    d = datetime.now()
    return get_wait_seconds(d.minute)


def get_wait_seconds(minutes):
    """                                                                                                                                                                                                     
    In order to give NOAA's buoys time to ping back their information, a 5 minute buffer will be provided                                                                                                   
    at the top of the hour and the midhour points. Every 5th minute and 35th minute should be used to                                                                                                       
    scrape some of the data from NOAA and provide the information.                                                                                                                                          
                                                                                                                                                                                                            
    :param minutes: Current minutes or a minutes value that will be converted to seconds to wait                                                                                                            
    :return: Integer number of seconds to wait                                                                                                                                                              
    """
    if 35 > minutes >= 5:
        return (35 - minutes) * 60
    elif minutes > 35:
         return (65 - minutes) * 60
    else:
        return (5 - minutes) * 60


class DatabaseAuthentication:

    username: str = None
    password: str = None
    host: str = None
    database: str = None

    def __init__(self, filename=None):
        """
        :filename: JSON encoded file with a `username` and `password`
        """
        if filename is None:
            # default to using the json file installed with the module
            filename = dirname(abspath(__file__)) + "/authentication.json"
        
        if exists(filename):
            with open(filename, 'r') as f:
                json_data = load(f)

            for k, v in json_data.items():
                setattr(self, k, v)
        else:
            raise FileExistsError(filename)
    
    @property
    def json(self):
        """
        :return: dictionary representation of the data
        """
        json_data = {
            "username": self.username,
            "password": self.password,
            "host": self.host,
            "database": self.database
        }


class NauticalDatabase():

    retry_interval_seconds: int = 60

    def __init__(self):

        self.connection = None
        self.authentication_info: DatabaseAuthentication()
        self._auto_query_timer: Timer = None

        self._sql_file_data = None
        sql_file = dirname(abspath(__file__))+"/nautical.mysql"
        if exists(sql_file):
            with open(sql_file, 'r') as f:
                self._sql_file_data = f.read()

        # alias and allow the users to call shutdown to stop the current thread from
        # executing - THIS WILL NOT DELETE THE DATABASE
        self.shutdown = self._cancel_timer
        # alias for the normal/intended execution sequence
        self.start = self._bihourly_transactions

    def create_connection(self, overwrite_database=False):
        """
        Create a database connection to the SQLite database (if the db_file does not exist, create it.)
        """
        if not self.connection:
            config = self.authentication_info.json
            try:
                self.connection = connect(**config)

                if overwrite_database and self._sql_file_data is not None:
                    self.connection.cursor().execute(self._sql_file_data)

            except MySQLError as e:
                log.error(e)
                raise  # keep error stack

    def close_connection(self):
        # If the connection is valid, close the connection
        if self.connection is not None:
            self.connection.close()

    def _start_timer(self, force_wait_time=None):
        """
        Attempt to start the timer. Will warn if the timer is currently executing.

        :param force_wait_time: if provided this time will be used not the `get_wait_time`.
        Time in seconds to wait.
        """
        if self._auto_query_timer is None or \
            (hasattr(self._auto_query_timer, "is_alive") and not self._auto_query_timer.is_alive()):
                delay = force_wait_time if force_wait_time is not None else get_wait_time()
                log.debug("Timer will wait {} seconds before executing".format(delay))
                self._auto_query_timer = Timer(delay, self._bihourly_transactions)
                self._auto_query_timer.start()
        else:
            log.warning("Timer is already executing or has an unknown type")
    
    def _cancel_timer(self):
        """
        Make sure that any running threads are shutdown.
        """
        if isinstance(self._auto_query_timer, Timer):
            if self._auto_query_timer.is_alive():
                log.debug("{} cancelling timer".format(self.__class__.__name__))
                self._auto_query_timer.cancel()
                self._auto_query_timer = None  # explicitly reset
    
    def _bihourly_transactions(self):
        """
        Run through the transactions that should occur roughly every half-hour (with the 
        5 minute interval added).
        """
        self._cancel_timer()

        # get all sources
        # get all buoys

        try:
            #self.create_connection()
            force_wait_time = None
            # add all sources
            # add all buoy information
        except MySQLError as e:
            force_wait_time = NauticalDatabase.retry_interval_seconds
            #self.close_connection()
        finally:
            self._start_timer(force_wait_time=force_wait_time)

    def insert_source(self, source):
        """
        Insert all of the data that is currently filling out the source.
        :param source: Source object that contains buoys categorized by the source.
        """
        """
        c = self.connection.cursor()

        with self._db_connection:
            for buoy in source:
                sql = '''INSERT INTO buoy_sources VALUES(?,?,?)'''
                buoy_source = (str(buoy.station), int(hash(buoy)), str(source.name))
                c.execute(sql, tuple(buoy_source))

                self.insert_buoy(buoy)
        """
        pass

    def insert_buoy(self, buoy):
        """
        Insert all of the data that is currently filling out the buoy.
        :param buoy: Buoy object that contains past and present data
        """
        
        """
        c = self._db_connection.cursor()

        with self._db_connection:
            if buoy.present:

                t_time = None

                fields = ['buoy']
                values = [buoy.station]
                for field_data in buoy.present:

                    if "time" in field_data:
                        t_time = copy(field_data[1])

                        # convert to 24 hour format, NO EFFECT if already in this format
                        t_time.fmt = TimeFormat.HOUR_24

                        fields.append("hour")
                        values.append(t_time.hours)
                        fields.append("minutes")
                        values.append(t_time.minutes)
                    else:
                        fields.append(field_data[0])
                        values.append(field_data[1])

                if not t_time:
                    return  # no time, no need to do anything

                find = '''SELECT * from buoys WHERE buoy=? AND year=? AND mm=? AND dd=? AND hour=? and minutes=?'''
                query = (buoy.station, buoy.present.year, buoy.present.mm, buoy.present.dd, t_time.hours, t_time.minutes)
                c.execute(find, tuple(query))

                if len(c.fetchall()) > 0:
                    sql = "UPDATE buoys SET {} WHERE buoy=? AND year=? AND mm=? AND dd=? AND hour=? and minutes=?".format(
                        ' ,'.join(["{} = ?".format(fields[i]) for i in range(len(fields))])
                    )
                    values.extend(query)
                    c.execute(sql, tuple(values))
                else:
                    sql = '''INSERT INTO buoys({}) VALUES({})'''.format(",".join(fields), ",".join(['?'] * len(values)))
                    c.execute(sql, tuple(values))

        # Let's go ahead and add in the location of this buoy whether or not the above statements took place
        self.insert_buoy_location(buoy)
        """
        pass

    def insert_buoy_location(self, buoy):
        """
        :param buoy: buoy whos location shall be inserted if it exists
        """
        """
        if not buoy.location:
            return

        c = self._db_connection.cursor()

        with self._db_connection:
            find = '''SELECT * from buoy_location WHERE buoy_hash=? AND latitude_deg=? AND longitude_deg=? AND altitude_m=?'''
            row = (int(hash(buoy)), buoy.location.latitude, buoy.location.longitude, buoy.location.altitude)
            c.execute(find, row)

            if len(c.fetchall()) <= 0:
                sql = '''INSERT INTO buoy_location VALUES(?,?,?,?)'''
                c.execute(sql, row)
        """
        pass
    

