import VKWrapper
import vk
import json


def read_config(config_name="settings.json"):
    with open(config_name) as f:
        config = json.load(f)
    return config


def count_post_likes(wrapper, user_id, target_id):
    posts = wrapper.get_user_posts_ids(user_id)
    likes_total = 0
    for num, post in enumerate(posts):
        post_likes = wrapper.get_likes(user_id, post, item_type="post")
        if target_id in post_likes:
            likes_total += 1
        print(f"\r{num} checked out of {len(posts)} posts.", end="")
    print()
    print("Posts done.")

    total_posts = len(posts)
    return likes_total, total_posts


def count_photo_likes(wrapper, user_id, target_id):
    likes_total = 0
    photos = []
    profile = wrapper.get_photo_ids(user_id, "profile")
    photos.extend(profile)
    print("Got profile photos.")

    wall = wrapper.get_photo_ids(user_id, "wall")
    photos.extend(wall)
    print("Got wall photos.")

    try:
        saved_memes = wrapper.get_photo_ids(user_id, "saved")
        photos.extend(saved_memes)
        print("Got memes.")
    except vk.exceptions.VkAPIError as e:
        print("It appears that this user tries to hide his memes.")

    for num, photo in enumerate(photos):
        photo_likes = wrapper.get_likes(user_id, photo, item_type="photo")
        if target_id in photo_likes:
            likes_total += 1
        print(f"\r{num} checked out of {len(photos)} photos.", end="")
    print()
    print("Photos done.")

    total_photos = len(photos)
    return likes_total, total_photos


def write_top(wrapper, liked_friends):
    friends_names = {}
    # Get friends names.
    for friend in liked_friends:
        user_info = wrapper.get_user(friend)
        friends_names[friend] = f"{user_info['first_name']} {user_info['last_name']}"

    f = open("output.txt", "w")
    f.write("Sorted by photo ratio:\n")
    by_photo_ratio = sorted(liked_friends.items(), key=lambda x: x[1]["photo_ratio"], reverse=True)
    for num, results in enumerate(by_photo_ratio):
        friend_id = results[0]
        friend_name = friends_names[friend_id]

        photo_likes = results[1]["photo_likes"]
        total_photos = results[1]["total_photos"]
        photo_ratio = results[1]["photo_ratio"]

        post_likes = results[1]["post_likes"]
        total_posts = results[1]["total_posts"]
        post_ratio = results[1]["post_ratio"]

        total_likes = results[1]["total_likes"]
        total_ratio = results[1]["total_ratio"]

        f.write(f"{num}) [id{friend_id}|{friend_name}]: \n"
                f"    Photo likes: {photo_likes}; Total photos: {total_photos}; Ratio: {photo_ratio}\n"
                f"    Post likes: {post_likes}; Total posts: {total_posts}; Ratio: {post_ratio};\n"
                f"    Total likes: {total_likes}; Ratio: {total_ratio}.\n")
    f.write("\n-----------------------------------------------------------\n\n")

    f.write("Sorted by photo likes:\n")
    by_photo_ratio = sorted(liked_friends.items(), key=lambda x: x[1]["photo_likes"], reverse=True)
    for num, results in enumerate(by_photo_ratio):
        friend_id = results[0]
        friend_name = friends_names[friend_id]

        photo_likes = results[1]["photo_likes"]
        total_photos = results[1]["total_photos"]
        photo_ratio = results[1]["photo_ratio"]

        post_likes = results[1]["post_likes"]
        total_posts = results[1]["total_posts"]
        post_ratio = results[1]["post_ratio"]

        total_likes = results[1]["total_likes"]
        total_ratio = results[1]["total_ratio"]

        f.write(f"{num}) [id{friend_id}|{friend_name}]: \n"
                f"    Photo likes: {photo_likes}; Total photos: {total_photos}; Ratio: {photo_ratio}\n"
                f"    Post likes: {post_likes}; Total posts: {total_posts}; Ratio: {post_ratio};\n"
                f"    Total likes: {total_likes}; Ratio: {total_ratio}.\n")
    f.write("\n-----------------------------------------------------------\n\n")

    f.write("Sorted by post likes:\n")
    by_photo_ratio = sorted(liked_friends.items(), key=lambda x: x[1]["post_likes"], reverse=True)
    for num, results in enumerate(by_photo_ratio):
        friend_id = results[0]
        friend_name = friends_names[friend_id]

        photo_likes = results[1]["photo_likes"]
        total_photos = results[1]["total_photos"]
        photo_ratio = results[1]["photo_ratio"]

        post_likes = results[1]["post_likes"]
        total_posts = results[1]["total_posts"]
        post_ratio = results[1]["post_ratio"]

        total_likes = results[1]["total_likes"]
        total_ratio = results[1]["total_ratio"]

        f.write(f"{num}) [id{friend_id}|{friend_name}]: \n"
                f"    Photo likes: {photo_likes}; Total photos: {total_photos}; Ratio: {photo_ratio}\n"
                f"    Post likes: {post_likes}; Total posts: {total_posts}; Ratio: {post_ratio};\n"
                f"    Total likes: {total_likes}; Ratio: {total_ratio}.\n")
    f.write("\n-----------------------------------------------------------\n\n")

    f.write("Sorted by post ratio:\n")
    by_photo_ratio = sorted(liked_friends.items(), key=lambda x: x[1]["post_ratio"], reverse=True)
    for num, results in enumerate(by_photo_ratio):
        friend_id = results[0]
        friend_name = friends_names[friend_id]

        photo_likes = results[1]["photo_likes"]
        total_photos = results[1]["total_photos"]
        photo_ratio = results[1]["photo_ratio"]

        post_likes = results[1]["post_likes"]
        total_posts = results[1]["total_posts"]
        post_ratio = results[1]["post_ratio"]

        total_likes = results[1]["total_likes"]
        total_ratio = results[1]["total_ratio"]

        f.write(f"{num}) [id{friend_id}|{friend_name}]: \n"
                f"    Photo likes: {photo_likes}; Total photos: {total_photos}; Ratio: {photo_ratio}\n"
                f"    Post likes: {post_likes}; Total posts: {total_posts}; Ratio: {post_ratio};\n"
                f"    Total likes: {total_likes}; Ratio: {total_ratio}.\n")
    f.write("\n-----------------------------------------------------------\n\n")

    f.write("Sorted by total ratio:\n")
    by_photo_ratio = sorted(liked_friends.items(), key=lambda x: x[1]["total_ratio"], reverse=True)
    for num, results in enumerate(by_photo_ratio):
        friend_id = results[0]
        friend_name = friends_names[friend_id]

        photo_likes = results[1]["photo_likes"]
        total_photos = results[1]["total_photos"]
        photo_ratio = results[1]["photo_ratio"]

        post_likes = results[1]["post_likes"]
        total_posts = results[1]["total_posts"]
        post_ratio = results[1]["post_ratio"]

        total_likes = results[1]["total_likes"]
        total_ratio = results[1]["total_ratio"]

        f.write(f"{num}) [id{friend_id}|{friend_name}]: \n"
                f"    Photo likes: {photo_likes}; Total photos: {total_photos}; Ratio: {photo_ratio}\n"
                f"    Post likes: {post_likes}; Total posts: {total_posts}; Ratio: {post_ratio};\n"
                f"    Total likes: {total_likes}; Ratio: {total_ratio}.\n")
    f.write("\n-----------------------------------------------------------\n\n")

    f.write("Sorted by total likes:\n")
    by_photo_ratio = sorted(liked_friends.items(), key=lambda x: x[1]["total_likes"], reverse=True)
    for num, results in enumerate(by_photo_ratio):
        friend_id = results[0]
        friend_name = friends_names[friend_id]

        photo_likes = results[1]["photo_likes"]
        total_photos = results[1]["total_photos"]
        photo_ratio = results[1]["photo_ratio"]

        post_likes = results[1]["post_likes"]
        total_posts = results[1]["total_posts"]
        post_ratio = results[1]["post_ratio"]

        total_likes = results[1]["total_likes"]
        total_ratio = results[1]["total_ratio"]

        f.write(f"{num}) [id{friend_id}|{friend_name}]: \n"
                f"    Photo likes: {photo_likes}; Total photos: {total_photos}; Ratio: {photo_ratio}\n"
                f"    Post likes: {post_likes}; Total posts: {total_posts}; Ratio: {post_ratio};\n"
                f"    Total likes: {total_likes}; Ratio: {total_ratio}.\n")
    f.write("\n-----------------------------------------------------------\n\n")

    f.close()


def main():
    config = read_config()

    app_id = config["app_id"]
    login = config["login"]
    password = config["password"]
    target = config["target"]

    wrapper = VKWrapper.VKWrapper(user_login=login, user_password=password, app_id=app_id)

    user_info = wrapper.get_user(target)
    target_name = f"{user_info['first_name']} {user_info['last_name']}"
    print(f"Being jealous to {target_name}.")

    liked_friends = {}
    friends = wrapper.get_friends(target)
    for num, friend in enumerate(friends):
        user_info = wrapper.get_user(friend)
        friend_name = f"{user_info['first_name']} {user_info['last_name']}"

        print(f"Checking out [id{friend}|{friend_name}] ({num}/{len(friends)}).")
        post_likes, total_posts = (0, 0)
        photo_likes, total_photos = (0, 0)
        try:
            post_likes, total_posts = count_post_likes(wrapper, friend, target)
            photo_likes, total_photos = count_photo_likes(wrapper, friend, target)
        except vk.exceptions.VkAPIError as e:
            # Error 15 stands for "Access denied."
            if "ERROR 15" in e.message:
                print(f"Cannot access {friend}")
        total_likes = post_likes+photo_likes
        if total_likes == 0:
            continue
        total_items = total_posts+total_photos
        liked_friends[friend] = {
                                 "photo_likes": photo_likes,
                                 "total_photos": total_photos,
                                 "photo_ratio": 0 if total_photos == 0 else photo_likes / total_photos,

                                 "post_likes": post_likes,
                                 "total_posts": total_posts,
                                 "post_ratio": 0 if total_posts == 0 else post_likes / total_posts,

                                 "total_likes": total_likes,
                                 "total_ratio": 0 if total_items == 0 else total_likes / total_items,
                                 }


    print("Writing tops.")
    write_top(wrapper, liked_friends)
    print("Done.")


if __name__ == "__main__":
    # import random
    # import pprint
    # import operator
    #
    # liked_friends = {}
    # for i in range(0, 10):
    #     post_likes = random.randint(0, 100)
    #     photo_likes = random.randint(0, 100)
    #     total_likes = post_likes + photo_likes
    #     liked_friends[i] = {
    #         "photo_likes": photo_likes,
    #         "post_likes": post_likes,
    #         "total_likes": total_likes,
    #     }
    # pprint.pprint(liked_friends)
    # for i in sorted(liked_friends.items(), key=lambda x: x[1]["photo_likes"], reverse=True):
    #     print(i[1]["photo_likes"])
    main()

