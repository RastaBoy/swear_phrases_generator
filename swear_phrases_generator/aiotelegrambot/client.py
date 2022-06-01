import asyncio
from json import dumps, loads
from typing import Callable, List, Optional, Union


import aiohttp
from .errors import TelegramApiError
from loguru import logger as log


class Client:
    base_url = "https://api.telegram.org/bot"

    def __init__(self, token: str, json_loads: Callable = loads, raise_exceptions: bool = False, **kwargs):
        self._url = "{}{}/".format(self.base_url, token)
        self.raise_exceptions = raise_exceptions
        self._json_loads = json_loads

        kwargs["timeout"] = aiohttp.ClientTimeout(total=kwargs.get("timeout", 10))

        self._json_loads = json_loads
        self._session = aiohttp.ClientSession(**kwargs)

    async def close(self):
        await self._session.close()

    async def get_updates(
        self,
        offset: Optional[Union[int, str]] = None,
        limit: Optional[Union[int, str]] = None,
        timeout: Optional[Union[int, str]] = None,
    ) -> Optional[dict]:
        params = {}
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if timeout:
            params["timeout"] = timeout
        
        log.debug(f'Method "get_updates()": {params}')
        # print(f'Method "get_updates()": {params}')
        # Log.debug(f'Method "get_updates()": {params}')
        return await self.request("get", "getUpdates", raise_exception=True, params=params)

    async def set_commands(self, data):
        params = dict()
        params["commands"] = data
        return await self.request("post", "setMyCommands", json=params, raise_exception=True)

    async def set_webhook(
        self,
        url: str,
        certificate: Optional[str] = None,
        max_connections: Optional[int] = None,
        allowed_updates: Optional[List[str]] = None,
    ) -> Optional[dict]:
        kwargs = {"params": [("url", url)]}
        if certificate:
            kwargs["data"] = {"certificate": open(certificate, "r")}
        if max_connections is not None:
            kwargs["params"].append(("max_connections", max_connections))
        if allowed_updates is not None:
            kwargs["params"].append(("allowed_updates", dumps(allowed_updates)))
        return await self.request("post", "setWebhook", **kwargs)

    async def get_webhook_info(self) -> Optional[dict]:
        return await self.request("get", "getWebhookInfo")

    async def delete_webhook(self) -> Optional[dict]:
        return await self.request("get", "deleteWebhook")

    async def send_message(self, text: str, chat_id: Union[int, str], reply_to_message_id: Optional[int] = None):
        params = {"chat_id": chat_id, "text": text}
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        await self.request("get", "sendMessage", params=params)
    
    async def edit_message(self, text:str, chat_id:Union[int, str], message_id, reply_markups=None, parse_mode=None):
        params = {'chat_id': chat_id, 'message_id': message_id, 'text' : text}
        if reply_markups:
            params['reply_markup'] = reply_markups
        if parse_mode:
            params['parse_mode'] = parse_mode
        await self.request("post", "editMessageText", json=params)

    async def delete_message(self, chat_id, message_id):
        params = {'chat_id' : chat_id, 'message_id' : message_id}
        await self.request("post", "deleteMessage", json=params)

    async def send_message_by_post(self, text: str, chat_id: Union[int, str], reply_to_message_id: Optional[int] = None, reply_markups=None, parse_mode='HTML'):
        params = {"chat_id": chat_id, "text": text}
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if reply_markups:
            params['reply_markup'] = reply_markups
        if parse_mode:
            params['parse_mode'] = parse_mode
        return await self.request("post", "sendMessage", json=params)

    async def request(self, method: str, api: str, raise_exception: bool = None, **kwargs) -> Optional[dict]:
        raise_exception = raise_exception if raise_exception is not None else self.raise_exceptions

        try:
            return await self._request(method, api, raise_exception, **kwargs)
        except asyncio.TimeoutError:
            if raise_exception:
                raise
            log.exception("Timeout")
            # print("Timeout")
            # Log.error("Timeout")
        except aiohttp.ClientError:
            if raise_exception:
                raise
            log.exception("Telegram API connection error")
            # print("Telegram API connection error")
            # Log.error("Telegram API connection error")

    async def _request(self, method: str, api: str, raise_exception, **kwargs) -> Optional[dict]:
        url = self._url + api
        try:
            response = await self._session.request(method=method, url=url, **kwargs)
            if response.status >= 500:
                self.process_error("Server error", response, None, raise_exception)
            else:
                data = self._json_loads(await response.text())
                if response.status == 200:
                    if data["ok"]:
                        return data
                    else:
                        self.process_error("Unsuccessful request", response, data, raise_exception)
                elif response.status == 401:
                    self.process_error("Invalid access token provided", response, data, raise_exception)
                else:
                    self.process_error(f"Telegram error: {response.status} {response.text}", response, data, raise_exception)
        except Exception as e:
            log.error(str(e))


    @staticmethod
    def process_error(msg: str, response: aiohttp.ClientResponse, data: Optional[dict], raise_exception: bool):
        if raise_exception:
            raise TelegramApiError(msg, data, response)
        else:
            extra = {"status": response.status}
            if data:
                extra["description"] = data["description"]
            log.error(msg, extra=extra)
