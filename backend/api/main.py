"""
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2022 Marc Steele
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from fastapi import FastAPI, Request
from alldaydj.routers import artists, types
from alldaydj.services.logging import logger
from time import time

# Use a nested FastAPI instance to mount at /api/ as our base

app = FastAPI()

api_app = FastAPI(debug=True)
api_app.include_router(artists.router)
api_app.include_router(types.router)

app.mount("/api", api_app)

# Logging


@app.middleware("http")
async def log_requests(request: Request, call_next):

    # Note the timings and make the request

    start = time()
    response = await call_next(request)
    end = time()

    # Log the timings and response

    response_time = (end - start) * 1000
    logger.info(
        f"{request.method} {request.url.path} {response_time:.2f}ms {response.status_code}"
    )

    return response
