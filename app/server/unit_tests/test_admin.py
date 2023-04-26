import pytest
from typing import Any
from app.server.database.collections import Collections
import app.server.service.core_data as model_service
from fastapi import APIRouter, Body, Request
from app.server.model.login import SignUp,SignIn
from app.server.utils.password import encrypt,decrypt
from bson import json_util
import json

non_existing_email='user@example.com'
existing_email='sidharthrashwana@yahoo.com'

@pytest.mark.asyncio
async def test_user_existence():
    '''
        Test case to check user existence.

        scenario :
            1.user which do not exist
            2.user which exist
    '''
    non_existing_user = await model_service.read_one(Collections.ACCOUNTS, {'email':non_existing_email})
    response = json.loads(json_util.dumps(non_existing_user))
    assert response['status'] == 404
    assert response['msg'] =='not found'
    existing_user = await model_service.read_one(Collections.ACCOUNTS, {'email':existing_email})
    response = json.loads(json_util.dumps(existing_user))
    assert response['email'] == 'sidharthrashwana@yahoo.com'
    assert response['status'] == 200
    assert response['isVerified'] == True