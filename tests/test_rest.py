import requests
from nautical_api.rest.resources import *
from nautical_api.connector import NauticalDatabase
import pytest
from flask import Flask
from flask_restful import Api


@pytest.mark.run(order=12)
def test_all_sources_empty():
    """
    Database has not been started, so the resource will have access to 
    the database which holds nothing.
    """
    x = AllSourcesGetter()
    resp = x.get()

    assert "sources" in resp

    assert len(resp['sources']) == 0


@pytest.mark.run(order=13)
def test_specific_sources_empty():
    """
    Database has not been started, so the resource will have access to 
    the database which holds nothing.
    """
    source_id = "Test_source_id"
    
    x = SpecificSourceGetter()
    resp = x.get(source_id=source_id)

    assert source_id in resp
    assert len(resp[source_id]) == 0


@pytest.mark.run(order=14)
def test_all_buoys_empty():
    """
    Database has not been started, so the resource will have access to 
    the database which holds nothing.
    """
    x = AllBuoysGetter()
    resp = x.get()

    assert "buoys" in resp

    assert len(resp['buoys']) == 0


@pytest.mark.run(order=15)
def test_specific_buoys_empty():
    """
    Database has not been started, so the resource will have access to 
    the database which holds nothing.
    """
    buoy_id = "Test_buoy_id"
    
    x = SpecificBuoyGetter()
    resp = x.get(buoy_id=buoy_id)

    assert buoy_id in resp
    assert len(resp[buoy_id]) == 0


@pytest.mark.run(order=22)
def test_sources_live():
    """
    NauticalDatabase has been started, so the resource will have access to all
    sources. Once the sources are pulled, select the first one and get all of
    the information for that source.
    """
    x = AllSourcesGetter()
    resp = x.get()

    assert "sources" in resp
    assert len(resp['sources']) > 0

    y = SpecificSourceGetter()
    source_id = resp["sources"][0]["id"]
    endpoint = resp["sources"][0]["endpoint"]
    
    resp = y.get(source_id=endpoint)

    assert source_id in resp
    assert len(resp[source_id]) > 0


@pytest.mark.run(order=23)
def test_buoys_live():
    """
    NauticalDatabase has been started, so the resource will have access to all
    buoys. Once the buoys are pulled, select the first one and get all of the 
    information for that buoy.
    """
    x = AllBuoysGetter()
    resp = x.get()

    assert "buoys" in resp
    assert len(resp['buoys']) > 0

    buoy_id = resp["buoys"][0]

    y = SpecificBuoyGetter()
    resp = y.get(buoy_id=buoy_id)

    assert buoy_id in resp
    assert len(resp[buoy_id]) > 0
    
    
