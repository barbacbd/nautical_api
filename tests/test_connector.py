from nautical_api.connector import find_wait_time, NauticalDatabase
import pytest
from uuid import UUID, uuid4

GOOD_UUID = str(uuid4())


def test_wait_time_low():
    """

    """
    assert find_wait_time(6) == 29

    
def test_wait_time_high():
    """

    """
    assert find_wait_time(34) == 1

    
def test_wait_time_low_even():
    """

    """
    assert find_wait_time(5) == 30

    
def test_wait_time_low_high():
    """

    """
    assert find_wait_time(36) == 29


def test_wait_time_high_high():
    """

    """
    assert find_wait_time(59) == 6


def test_wait_time_high_even():
    """

    """
    assert find_wait_time(35) == 30



def is_uuid_valid(t_uuid, version=4):
    """
    Attempt to verify the uuid against the suspected version.

    :param t_uuid: Test uuid or the UUID that should be tested/verified
    :param version: UUID version that the user believes was used to generate the uuid

    :return: True if the `t_uuid` could be verified against the uuid version
    """
    try:
        _uuid = UUID(t_uuid, version=version)
        return str(_uuid) == t_uuid
    except ValueError:
        return False


def test_db_subscribe():
    """

    """

    def callback():
        pass

    output = NauticalDatabase().subscribe(callback, GOOD_UUID)

    assert output == GOOD_UUID
    assert is_uuid_valid(output)

def test_db_unsubscribe():
    """

    """
    assert NauticalDatabase().unsubscribe(GOOD_UUID)

def test_db_unsubscribe_bad():
    """

    """
    assert not NauticalDatabase().unsubscribe(str(uuid4()))
    

def test_db_get_all_sources():
    """
    
    """
    pass


def test_db_get_source():
    """

    """
    pass


def test_db_get_all_buoys():
    """

    """
    pass


def test_db_get_buoy():
    """

    """
    pass


def test_db_get_aliases():
    """

    """

    pass
