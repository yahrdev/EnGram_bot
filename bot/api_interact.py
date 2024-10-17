"""The module for interacting with the API."""

import json
import aiohttp
from config import settings
import const
from error_handlers import global_error_handler_async, WrongStatusError, global_error_handler_sync
import requests
from datetime import timezone, datetime

@global_error_handler_async
async def get_test(level):
    if settings.ASYNC_API:   
        response_status, response_dict = await get_test_async(level)  #async api
    else:
        response_status, response_dict = get_test_sync(level)   #sync api

    if response_status == 200:
        return response_dict
    else:
        if response_dict['message'] == const.NoTestsMsg:  #the case when there are no tests for the level
            return const.NoTestsAnswer
        else:
            raise WrongStatusError(const.WrongStatus.format(response_status, response_dict))
        

@global_error_handler_async
async def update_test(level, id):
    datetime_shown = datetime.now(timezone.utc).isoformat()
    test_json={
        "Level": level,
        "ID": id,
        "datetime_shown": datetime_shown
        }
    if settings.ASYNC_API:
        response_status, response_dict = await update_test_async(test_json)   #async api
    else:
        response_status, response_dict = update_test_sync(test_json)  #sync api

    if response_status != 200:
        raise WrongStatusError(const.WrongStatus.format(response_status, response_dict))
    


@global_error_handler_async
async def get_test_async(level):

    """Get a test from the API"""

    response = ''
    response_dict = {}
    async with aiohttp.ClientSession() as session:
        response = await session.get(settings.API_ASYNC_URL + '/gettests?Level=' + str(level))
        resp = await response.text()
        response_dict = json.loads(resp) 
        return response.status, response_dict



@global_error_handler_async
async def update_test_async(test_json):

    """Update the test in the API"""

    response = ''
    response_dict = {}
    async with aiohttp.ClientSession() as session:
        response = await session.post(settings.API_ASYNC_URL + "/updatestatus", json=test_json)
        resp = await response.text()
        response_dict = json.loads(resp) 
        return response.status, response_dict
        


@global_error_handler_sync
def get_test_sync(level):

    """Get a test from the API"""

    response = ''
    response_dict = {}
    response = requests.get(settings.API_SYNC_URL + '/testsapi/gettests?Level=' + str(level))
    response_dict = response.json()
    return response.status_code, response_dict



@global_error_handler_sync
def update_test_sync(test_json):

    """Update the test in the API"""

    response = ''
    response_dict = {}
    response = requests.post(settings.API_SYNC_URL + "/testsapi/updatestatus", json=test_json)
    response_dict = response.json()
    return response.status_code, response_dict
    