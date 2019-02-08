import vk
from ratelimiter import RateLimiter

import requests
import time


class VKWrapper(object):
    def __init__(self, user_login, user_password, app_id="3265802", scope="wall"):
        self.session = vk.AuthSession(app_id=app_id, user_login=user_login, user_password=user_password, scope=scope)
        # self.session = vk.Session(access_token=token)
        self.api = vk.API(self.session, v='5.85')

    @RateLimiter(max_calls=3, period=1)
    def __execute_command(self, fun, **kwargs):
        captcha_needed = False
        captcha_answer = None
        captcha_sid = None
        while True:
            try:
                if captcha_needed:
                    result = fun(**kwargs, captcha_sid=captcha_sid, captcha_key=captcha_answer)
                    captcha_needed = False
                else:
                    result = fun(**kwargs)
                self.last_command_access = time.time()
                break
            except requests.exceptions.ReadTimeout:
                time.sleep(2)
                continue
            except requests.exceptions.RequestException:
                time.sleep(4)
                continue
            except vk.exceptions.VkAPIError as e:
                print(f"VKWrapper Error: {e.message}")
                # Error 6 stands for "Too many requests per second."
                if "ERROR 6" in e.message:
                    time.sleep(1)
                    continue
                # Error 14 stands for "Captcha needed"
                if "ERROR 14" in e.message.lower():
                    print(f"Please, answer this: {e.captcha_img}")
                    captcha_sid = e.captcha_sid
                    captcha_answer = input()
                    captcha_needed = True
                    time.sleep(10)
                raise
        return result

    def leave_like(self, user_id, type, item_id):
        return self.__execute_command(self.api.likes.add, owner_id=user_id, type=type, item_id=item_id)

    def delete_like(self, user_id, type, item_id):
        return self.__execute_command(self.api.likes.delete, owner_id=user_id, type=type, item_id=item_id)

    def get_user(self, user_id, fields=""):
        return self.__execute_command(self.api.users.get, user_ids=user_id, fields=fields)[0]

    def get_user_posts_ids(self, user_id):
        posts_total = self.__execute_command(self.api.wall.get, owner_id=user_id, filter="owner", count=1)["count"]
        posts_ids = []
        for offset in range(0, posts_total, 100):
            posts = self.__execute_command(self.api.wall.get, owner_id=user_id, filter="owner", count=100, offset=offset)["items"]
            for post in posts:
                posts_ids.append(post["id"])
        return posts_ids

    def get_likes(self, user_id, item_id, item_type = "post"):
        like_total = self.__execute_command(self.api.likes.getList, filter="likes", owner_id=user_id, skip_own=0, item_id=item_id, count=1, type=item_type)["count"]
        user_likes = []
        for offset in range(0, like_total, 100):
            likes = self.__execute_command(self.api.likes.getList, filter="likes", owner_id=user_id, skip_own=0, item_id=item_id, offset=offset, count=100, type=item_type)["items"]
            user_likes.extend(likes)
        return user_likes

    def get_friends(self, user_id):
        try:
            friends_total = \
                self.__execute_command(self.api.friends.get, user_id=user_id, order="name", count=1, offset=0,
                                   name_case="nom")
        except vk.exceptions.VkAPIError as e:
            return []
        friends_total = friends_total["count"]
        user_friends = []
        COUNT = 5000
        for offset in range(0, friends_total, COUNT):
            friends = self.__execute_command(self.api.friends.get, user_id=user_id, order="name", count=COUNT, offset=offset,
                                   name_case="nom")["items"]
            user_friends.extend(friends)
        return user_friends

    # photo_album = profile, wall, saved
    def get_photo_ids(self, user_id, photo_album):
        photos_total = self.__execute_command(self.api.photos.get, owner_id=user_id, album_id=photo_album, count=1)["count"]
        user_photos_id = []
        for offset in range(0, photos_total, 100):
            photos = self.__execute_command(self.api.photos.get, owner_id=user_id, album_id=photo_album, count=100)["items"]
            for photo in photos:
                user_photos_id.append(photo["id"])
        return user_photos_id

    def get_user_name(self, user_id):
        user_info = self.get_user(user_id)
        return f"{user_info['first_name']} {user_info['last_name']}"

    def send_message(self, user_id, text):
        answer = self.__execute_command(self.api.messages.send, user_id=user_id, message=text)
        return answer

    def remove_message(self, message_ids):
        self.__execute_command(self.api.messages.delete, message_ids=message_ids, delete_for_all=1)
