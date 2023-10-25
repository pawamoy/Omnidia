import asyncio
import time
import traceback
from base64 import b64encode
from concurrent import futures

import httpx
from loguru import logger
from neo4j import READ_ACCESS, GraphDatabase
from neo4j.exceptions import ServiceUnavailable

RETRY_WAITS = [0, 1, 4]  # How long to wait after each successive failure.
MAX_WORKERS = 30


class Neo4jBolt:
    """Neo4j database API."""

    def __init__(self, user, password, url, loop):
        self.loop = loop
        self.executor = futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
        for retry_wait in RETRY_WAITS:
            try:
                self.driver = GraphDatabase.driver(url, auth=(user, password))
            except Exception:
                if retry_wait == RETRY_WAITS[-1]:
                    raise
                # print("WARNING: retrying to Init DB; error:")
                traceback.print_exc()
                time.sleep(retry_wait)
            else:
                break

    async def fetch_start(self, query):
        session = self.driver.session(access_mode=READ_ACCESS)
        iterator = await self.loop.run_in_executor(self.executor, lambda: session.run(query).records())
        return session, iterator

    async def fetch_iterate(self, iterator):
        while True:
            try:
                res = await self.loop.run_in_executor(self.executor, lambda: next(iterator))
            except StopIteration:
                break
            else:
                yield dict(res)

    async def fetch(self, query):
        for retry_wait in RETRY_WAITS:
            try:
                session, iterator = await self.fetch_start(query)
            except (BrokenPipeError, ServiceUnavailable):
                if retry_wait == RETRY_WAITS[-1]:
                    raise
                await asyncio.sleep(retry_wait)
            else:
                break

        async for record in self.fetch_iterate(iterator):
            yield record

        await self.loop.run_in_executor(self.executor, session.close)

    async def fetch_one(self, query):
        async for record in self.fetch(query):
            return record
        return None

    async def exec(self, query):
        async for _ in self.fetch(query):
            ...


class Neo4jHTTP:
    def __init__(self, url, user, password) -> None:
        encoded = b64encode(f"{user}:{password}".encode()).decode()
        headers = {"Authorization": f"Basic {encoded}"}
        self.client = httpx.Client(base_url=url, headers=headers)
        self.async_client = httpx.AsyncClient(base_url=url, headers=headers)

    def _payload(self, query, parameters):
        parameters = parameters or {}
        return {
            "statements": [
                {
                    "statement": query,
                    "parameters": parameters,
                }
            ]
        }

    def _post(self, client, payload):
        return client.post("db/neo4j/tx/commit", json=payload)

    def _response(self, response):
        data = response.json()

        if "errors" in data:
            for error in data["errors"]:
                logger.error(error)
            return []

        return data["results"]

    def exec(self, query, parameters=None):
        logger.info(query)
        with self.client as client:
            return self._response(self._post(client, self._payload(query, parameters)))

    async def aexec(self, query, parameters=None):
        logger.info(query)
        with self.async_client as client:
            return self._response(await self._post(client, self._payload(query, parameters)))
