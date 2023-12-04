from instagrapi import Client
from instagrapi.types import Usertag

# Credentials
from constants import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD


def upload_to_instagram(image_path: str, caption: str):
    # Initialize the client
    cl = Client()
    cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

    # Get user information
    user = cl.user_info_by_username(INSTAGRAM_USERNAME)

    # Upload the photo
    media = cl.photo_upload(
        path=image_path,
        caption=caption,
        usertags=[Usertag(user=user, x=0.5, y=0.5)]
    )
    
    print(media)

    
if __name__ == "__main__":
    upload_to_instagram('stoic_2_text.jpg', 'testing123')