"""
File Name: user_list_data.py
Original Author: Fis-chl
Creation Date: 07/12/2022
File Description: Holds data for a user's list temporarily so that people can scroll through them.
The data should get deleted after 2 minutes without being accessed, and have a maximum 5 minute lifespan.
"""

# TODO Destroy old data

import uuid


class UserListData:
    def __init__(self, username, mediatype, listname, entries):
        self.listid = uuid.uuid4()
        self.username = username
        self.mediatype = mediatype
        self.listname = listname
        self.entries = entries
        self.destroy = False


class UserListHandler:

    def __init__(self):
        self.user_list_data = []

    async def destroy_old_data(self):
        temp_list = self.user_list_data.copy()
        for x in range(0, len(temp_list) - 1):
            del(self.user_list_data[x])

    async def get_list(self, list_id):
        for x in self.user_list_data:
            if x.listid == list_id:
                return x
        return None

    async def get_list_and_index(self, userlistdata):
        for x in self.user_list_data:
            if x.listid == userlistdata.listid:
                return [x, self.user_list_data.index(x)]
        return None

    async def add_list(self, userlistdata):
        list_and_ind = await self.get_list_and_index(userlistdata)
        if list_and_ind is not None:
            self.user_list_data[list_and_ind[-1]] = userlistdata
        else:
            self.user_list_data.append(userlistdata)

    async def create_list(self, data, username, mediatype, listname):
        # Data is a list of media, so:
        entries = []
        counter = 1
        for media in data:
            media['index'] = counter
            entries.append(media)
            counter = counter + 1
        user_list_data = UserListData(username, mediatype, listname, entries)
        await self.add_list(user_list_data)
        return user_list_data.listid

    async def delete_list(self, list_id):
        for _list in self.user_list_data:
            if _list.listid == list_id:
                _list.destroy = True