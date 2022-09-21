# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Daisuke Sato

class Room(object):
    def __init__(self, api) -> None:
        """room endpoint
        :param api:
        """
        self.api = api

    def get_room_list(self):
        """get chat room list
        https://developer.chatwork.com/reference/get-rooms

        Returns:
            list: Response
        """
        _uri = "rooms"
        _method = "GET"

        headers = {
            "Accept": "application/json",
            "x-chatworktoken": self.api.api_key
        }
        resp = self.api.invoke_method(_method, _uri, headers=headers)

        return resp.json()

    def get_contact_list(self) -> list:
        rooms = self.get_room_list()
        return list(filter(lambda x: x["type"] == "direct", rooms))

    def get_room_info(self, room_id: int) -> list:
        """get chat room information
        https://developer.chatwork.com/reference/get-rooms-room_id

        Args:
            room_id (int): room_id

        Returns:
            list: Response
        """
        _uri = f"rooms/{room_id}"
        _method = "GET"

        headers = {
            "Accept": "application/json",
            "x-chatworktoken": self.api.api_key
        }
        resp = self.api.invoke_method(_method, _uri, headers=headers)

        return resp.json()

    def get_message(self, room_id: int, force=False) -> list:
        """get messages from chat
        https://developer.chatwork.com/reference/get-rooms-room_id-messages

        Args:
            room_id (int): room_id
            force (bool, optional): if true, the latest 100 items will be acquired 
                regardless of whether or not they have been acquired.
                Defaults to False.

        Returns:
            list: Response
        """
        _uri = f"rooms/{room_id}/messages"
        _method = "GET"
        query_param = {}
        if force:
            query_param.update({"force": "1"})

        headers = {
            "Accept": "application/json",
            "x-chatworktoken": self.api.api_key
        }
        resp = self.api.invoke_method(_method, _uri, headers=headers, query_param=query_param)

        if resp.status_code == 204:  # empty message
            ret = []
        elif resp.status_code == 200:
            ret = resp.json()
        return ret

    def post_message(self, room_id: int, message: str, self_unread=False) -> list:
        """post a message to chat
        https://developer.chatwork.com/reference/post-rooms-room_id-messages

        Args:
            room_id (int): room_id
            message (str): message body
            self_unread (bool, optional): if true, the posted message is marked as unread. Defaults to False.

        Returns:
            list: Response
        """
        _uri = f"rooms/{room_id}/messages"
        _method = "POST"
        payload = {}
        if self_unread:
            payload.update({"self_unread": "1"})
        else:
            payload.update({"self_unread": "0"})
        payload.update({"body": message})

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "x-chatworktoken": self.api.api_key
        }
        resp = self.api.invoke_method(_method, _uri, request_param=payload, headers=headers)

        return resp.json()
