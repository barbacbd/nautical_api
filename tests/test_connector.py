from nautical_api.connector import find_wait_time, NauticalDatabase
import pytest
from uuid import UUID, uuid4


GOOD_UUID = str(uuid4())


@pytest.mark.run(order=1)
def test_wait_time_low():
    """
    The wait time has an offset of 5 minutes from the 30 minute markers (5, 35) to
    provide a buffer for information to be uploaded. 

    Test the number just above the lower indicator
    """
    assert find_wait_time(6) == 29


@pytest.mark.run(order=2)
def test_wait_time_high():
    """
    The wait time has an offset of 5 minutes from the 30 minute markers (5, 35) to
    provide a buffer for information to be uploaded. 

    Test the number just under the upper indicator
    """
    assert find_wait_time(34) == 1


@pytest.mark.run(order=3)
def test_wait_time_low_even():
    """
    The wait time has an offset of 5 minutes from the 30 minute markers (5, 35) to
    provide a buffer for information to be uploaded. 

    Test the lower number indicator
    """
    assert find_wait_time(5) == 30


@pytest.mark.run(order=4)
def test_wait_time_low_high():
    """
    The wait time has an offset of 5 minutes from the 30 minute markers (5, 35) to
    provide a buffer for information to be uploaded. 

    Test the number just above the high indicator
    """
    assert find_wait_time(36) == 29

    
@pytest.mark.run(order=5)
def test_wait_time_high_high():
    """
    The wait time has an offset of 5 minutes from the 30 minute markers (5, 35) to
    provide a buffer for information to be uploaded. 

    Test the number just under the max minutes in an hour
    """
    assert find_wait_time(59) == 6

    
@pytest.mark.run(order=6)
def test_wait_time_high_even():
    """
    The wait time has an offset of 5 minutes from the 30 minute markers (5, 35) to
    provide a buffer for information to be uploaded. 

    Test the high indicator
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

    
@pytest.mark.run(order=7)
def test_db_subscribe():
    """
    Test a good subscription. This includes getting the UUID that is used for
    tracking the subscription. The GOOD UUID is passed in and should be returned
    """

    def callback():
        pass

    output = NauticalDatabase().subscribe(callback, GOOD_UUID)

    assert output == GOOD_UUID
    assert is_uuid_valid(output)

    
@pytest.mark.run(order=8)
def test_db_unsubscribe():
    """
    The unsubscribe function works by using the UUID that should have been saved
    from the subscription call. The GOOD UUID should be applicable here since the 
    tests are run in order.
    """
    assert NauticalDatabase().unsubscribe(GOOD_UUID)


@pytest.mark.run(order=9)
def test_db_unsubscribe_bad():
    """
    The unsubscribe function works by using the UUID that should have been saved
    from the subscription call. The uuid here is a newly generated string, and 
    this is not currently saved, thus False will be returned
    """
    assert not NauticalDatabase().unsubscribe(str(uuid4()))
    

@pytest.mark.run(order=10)
def test_db_get_all_sources_empty():
    """
    The database has not been started yet, and the sources are controlled within the 
    class, so the sources should be empty.
    """
    assert len(NauticalDatabase().get_all_source_ids()) == 0


@pytest.mark.run(order=11)
def test_db_get_all_buoys_empty():
    """
    The database has not been started yet, and the buoys are controlled within the 
    class, so the buoys should be empty.
    """
    assert len(NauticalDatabase().get_all_buoy_ids()) == 0

    
@pytest.mark.run(order=16)
def test_start_db():
    """
    Start the database, and assuming that no errors occur, the simple test will
    return be correct.
    """
    NauticalDatabase().run()
    assert True


@pytest.mark.run(order=17)
def test_db_get_all_sources():
    """
    The database has been started, and the data should be saved internally.
    We never know how many this will return in the future, so just make sure that
    some data was present.
    """
    sources = NauticalDatabase().get_all_source_ids()

    assert len(sources) > 0


@pytest.mark.run(order=18)
def test_db_get_source():
    """
    Making a similar call to the one in the test for get all sources, 
    use one of the sources to grab the specific information from the
    database.
    """
    sources = NauticalDatabase().get_all_source_ids()
    if sources:
        source_id = sources[0]

        source = NauticalDatabase().get_source(source_id)

        assert source is not None
    else:
        assert True == False

        
@pytest.mark.run(order=19)
def test_db_get_all_buoys():
    """
    The database has been started, and the data should be saved internally.
    We never know how many this will return in the future, so just make sure that
    some data was present.
    """
    buoys = NauticalDatabase().get_all_buoy_ids()

    assert len(buoys) > 0


@pytest.mark.run(order=20)
def test_db_get_buoy():
    """
    Making a similar call to the one in the test for get all buoys, 
    use one of the buoys to grab the specific information from the
    database.
    """
    buoys = NauticalDatabase().get_all_buoy_ids()
    if buoys:
        buoy_id = buoys[0]

        buoy = NauticalDatabase().get_buoy(buoy_id)

        assert buoy is not None
    else:
        assert True == False


@pytest.mark.run(order=21)
def test_db_get_aliases():
    """
    The aliases will ALWAYS be generated for the sources. As long as the sources exist
    then this should be present.
    """
    assert len(NauticalDatabase().get_aliases()) > 0


@pytest.mark.run(order=24)
def test_db_stop():
    """
    Stop the database to kill the threads and ensure that stop works. If the
    stop works the tests will end and assertion will be valid.
    """
    NauticalDatabase().stop()
    assert True
