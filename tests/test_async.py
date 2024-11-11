# tests/test_async.py

import pytest
from httpx import AsyncClient
import sys
import os

# Append the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now you can import main without using relative import
import main


@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=main.app, base_url="http://testserver") as ac:
        response = await ac.get("/async-endpoint")
        assert response.status_code == 200
