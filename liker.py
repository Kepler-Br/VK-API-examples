import VKWrapper
import vk
import random
from time import sleep
import json


def read_config(config_name="settings.json"):
    with open(config_name) as f:
        config = json.load(f)
    return config


def like_posts(wrapper, target, min_waiting=1, max_waiting=3):
    posts = wrapper.get_user_posts_ids(target)
    print("Got posts.")
    for num, post in enumerate(posts):
        try:
            wrapper.leave_like(target, "post", post)
        except vk.exceptions.VkAPIError as e:
            # Error 15 stands for "Access denied."
            if "ERROR 15" in e.message:
                wait = random.randint(min_waiting, max_waiting) + random.random()
                print(f"Access denied on post #{num}/{len(posts)}. Waiting {wait}")
                sleep(wait)
                continue
        wait = random.randint(min_waiting, max_waiting) + random.random()
        print(f"{num} liked out of {len(posts)} posts. Waiting for {wait} seconds.")
        sleep(wait)
    print("Posts done.")


def like_photos(wrapper, target, min_waiting=1, max_waiting=3):
    photos = []
    profile = wrapper.get_photo_ids(target, "profile")
    photos.extend(profile)
    print("Got profile photos.")

    wall = wrapper.get_photo_ids(target, "wall")
    photos.extend(wall)
    print("Got wall photos.")

    try:
        saved_memes = wrapper.get_photo_ids(target, "saved")
        photos.extend(saved_memes)
        print("Got memes.")
    except vk.exceptions.VkAPIError as e:
        print("It appears that this user tries to hide their memes.")

    for num, photo in enumerate(photos):
        try:
            wrapper.leave_like(target, "photo", photo)
        except vk.exceptions.VkAPIError as e:
            # Error 15 stands for "Access denied."
            if "ERROR 15" in e.message:
                wait = random.randint(min_waiting, max_waiting) + random.random()
                print(f"Access denied on photo #{num}/{len(photos)}. Waiting {wait}")
                sleep(wait)
                continue
        wait = random.randint(min_waiting, max_waiting) + random.random()
        print(f"{num} liked out of {len(photos)} photos. Waiting for {wait} seconds.")
        sleep(wait)

    print("Photos done.")


def main():
    config = read_config()

    app_id = config["app_id"]
    login = config["login"]
    password = config["password"]
    target = config["target"]

    wrapper = VKWrapper.VKWrapper(user_login=login, user_password=password, app_id=app_id)

    user_info = wrapper.get_user(target)
    target_name = f"{user_info['first_name']} {user_info['last_name']}"
    print(f"Making up with {target_name}")

    like_posts(wrapper, target)
    like_photos(wrapper, target)

    print("Done.")


if __name__ == "__main__":
    main()

