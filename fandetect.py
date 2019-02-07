import VKWrapper
import vk
import json
import collections


def read_config(config_name="settings.json"):
    with open(config_name) as f:
        config = json.load(f)
    return config


def get_post_likes(wrapper, target):
    print("Getting posts.")
    posts = wrapper.get_user_posts_ids(target)
    print("Got posts.")

    post_likes = []

    for num, post in enumerate(posts):
        if post == 0:
            continue
        likes = wrapper.get_likes(target, post, "post")
        post_likes.extend(likes)
        print(f"{num} out of {len(posts)} posts.")

    print("Got posts likes.")
    return post_likes


def get_photo_likes(wrapper, target):
    print("Getting photos.")
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

    photo_likes = []
    for num, photo in enumerate(photos):
        likes = wrapper.get_likes(target, photo, "photo")
        photo_likes.extend(likes)
        print(f"{num} out of {len(photos)} photos.")
    print("Got photo likes.")
    return photo_likes


def print_top_likers(counted_likes, wrapper, target, top_count=5):
    user_info = wrapper.get_user(target)
    target_name = f"{user_info['first_name']} {user_info['last_name']}"
    most_likers = counted_likes.most_common(top_count)

    print(f"Most likers of [id{target}|{target_name}] are:")
    for liker in most_likers:
        liker_id = liker[0]
        likes = liker[1]
        user_info = wrapper.get_user(liker_id)
        liker_name = f"{user_info['first_name']} {user_info['last_name']}"
        print(f"[id{liker_id}|{liker_name}]: {likes} likes.")
    print("Done.")


def main():
    config = read_config()

    app_id = config["app_id"]
    login = config["login"]
    password = config["password"]
    target = config["target"]

    wrapper = VKWrapper.VKWrapper(user_login=login, user_password=password, app_id=app_id)

    counted_likes = collections.Counter()
    post_likes = get_post_likes(wrapper, target)
    counted_likes.update(post_likes)
    photo_likes = get_photo_likes(wrapper, target)
    counted_likes.update(photo_likes)

    print_top_likers(counted_likes, wrapper, target)


if __name__ == "__main__":
    main()
