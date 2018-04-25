# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

"""linebot.http_client_async module."""

from __future__ import unicode_literals

import asyncio

import aiohttp

from .http_client import HttpClient, HttpResponse


class AioHttpClient(HttpClient):
    """HttpClient implemented by aiohttp."""

    def __init__(self, timeout=HttpClient.DEFAULT_TIMEOUT, loop=None):
        """__init__ method.

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is :py:attr:`DEFAULT_TIMEOUT`
        :type timeout: float | tuple(float, float)
        """
        super(AioHttpClient, self).__init__(timeout)

        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

        self.session = aiohttp.ClientSession(loop=loop)

    @asyncio.coroutine
    def get(self, url, headers=None, params=None, stream=False, timeout=None):
        """GET request.

        :param str url: Request url
        :param dict headers: (optional) Request headers
        :param dict params: (optional) Request query parameter
        :param bool stream: (optional) get content as stream
        :param timeout: (optional), How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is :py:attr:`self.timeout`
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`RequestsHttpResponse`
        :return: RequestsHttpResponse instance
        """
        if timeout is None:
            timeout = self.timeout

        response = yield from self.session.get(
            url, headers=headers, params=params, stream=stream, timeout=timeout
        )

        return AioHttpResponse(response)

    @asyncio.coroutine
    def post(self, url, headers=None, data=None, timeout=None):
        """POST request.

        :param str url: Request url
        :param dict headers: (optional) Request headers
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body
        :param timeout: (optional), How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is :py:attr:`self.timeout`
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`RequestsHttpResponse`
        :return: RequestsHttpResponse instance
        """
        if timeout is None:
            timeout = self.timeout

        response = yield from self.session.post(
            url, headers=headers, data=data, timeout=timeout
        )

        return AioHttpResponse(response)

    @asyncio.coroutine
    def delete(self, url, headers=None, data=None, timeout=None):
        """DELETE request.

        :param str url: Request url
        :param dict headers: (optional) Request headers
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body
        :param timeout: (optional), How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is :py:attr:`self.timeout`
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`RequestsHttpResponse`
        :return: RequestsHttpResponse instance
        """
        if timeout is None:
            timeout = self.timeout

        response = yield from self.session.delete(
            url, headers=headers, data=data, timeout=timeout
        )

        return AioHttpResponse(response)


class AioHttpResponse(HttpResponse):
    """HttpResponse implemented by requests lib's response."""

    def __init__(self, response):
        """__init__ method.

        :param response: requests lib's response
        """
        self.response = response

    @property
    def status_code(self):
        """Get status code."""
        return self.response.status

    @property
    def headers(self):
        """Get headers."""
        return self.response.headers

    @property
    @asyncio.coroutine
    def text(self):
        """Get request body as text-decoded."""
        return (yield from self.response.text())

    @property
    @asyncio.coroutine
    def content(self):
        """Get request body as binary."""
        return (yield from self.response.read())

    @property
    @asyncio.coroutine
    def json(self):
        """Get request body as json-decoded."""
        return (yield from self.response.json())

    def iter_content(self, chunk_size=1024):
        """Get request body as iterator content (stream).

        :param int chunk_size:
        :param bool decode_unicode:
        """
        return self.response.content.iter_chunked(chunk_size)
