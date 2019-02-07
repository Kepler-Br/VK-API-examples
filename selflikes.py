import VKWrapper
import vk
import json


def read_config(config_name="settings.json"):
    with open(config_name) as f:
        config = json.load(f)
    return config


def check_posts(wrapper, target):
    posts = wrapper.get_user_posts_ids(target)
    print("Got posts.")

    liked_posts = []
    for num, post in enumerate(posts):
        if post == 0:
            continue
        likes = wrapper.get_likes(target, post, "post")
        if target in likes:
            liked_posts.append(post)
        print(f"{num} out of {len(posts)} posts.")

    print("Got posts likes.")
    return liked_posts


def check_photos(wrapper, target):
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

    liked_photos = []
    for num, photo in enumerate(photos):
        likes = wrapper.get_likes(target, photo, "photo")
        if target in likes:
            liked_photos.append(post)
        print(f"{num} out of {len(photos)} photos.")
    print("Got photo likes.")
    return liked_photos


def print_selflikes(target_name, liked_posts, liked_photos):
    print(f"Here's self liked posts of [id{target}|{target_name}]:")
    for post in liked_posts:
        print(f"https://vk.com/wall{target}_{post}")

    print(f"Here's self liked photos of [id{target}|{target_name}]:")
    for photo in liked_photos:
        print(f"https://vk.com/photo{target}_{photo}")


def main():
    config = read_config()

    app_id = config["app_id"]
    login = config["login"]
    password = config["password"]
    target = config["target"]

    wrapper = VKWrapper.VKWrapper(user_login=login, user_password=password, app_id=app_id)
    liked_posts = check_posts(wrapper, target)
    liked_photos = check_photos(wrapper, target)

    user_info = wrapper.get_user(target)
    target_name = f"{user_info['first_name']} {user_info['last_name']}"
    print_selflikes(target_name, liked_posts, liked_photos)

    print("Done.")


if __name__ == "__main__":
    main()

