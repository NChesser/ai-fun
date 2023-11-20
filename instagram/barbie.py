'''
    About: Stoic Quote Generator Using Open AI Assistants
    Author: Nick Chesser
'''
import time
import requests

from openai import OpenAI
from constants import OPENAPI_KEY

# Open API Client
client = OpenAI(api_key=OPENAPI_KEY)

# Helper Modules
from text import add_image_text


def download_image(url: str, save_path: str):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Image downloaded successfully to {save_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        

def get_quote():
    # New Thread for Assistant
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Create a quote"
    )
    
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id='asst_UjDg9d4aU1ZO3CXMIYnnArpu'
    )
    
    time.sleep(10)
    
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    
    # print(run)
    
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    
    # print(messages)
    
    return messages
    

def create_image_prompt(quote: str):
    
    content = f'Pull out the 4 most key words from the following quote "{quote}"'
    
    messages = [{ "role": "user", "content": content}]
    
    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # model="gpt-4-1106-preview",
            messages=messages
        )
    
    response = response.choices[0].message.content
    
    return response


def create_image(prompt: str):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    
    return image_url
    

def create_profile():
   
    # prompt = "Design a dazzling Barbie profile picture that radiates glamour and fun! Envelop the iconic Barbie silhouette in a cascade of vibrant sparkles and an explosion of lively colors. Make sure to capture the essence of Barbie's timeless charm and playfulness. Let your creativity shine as you craft a profile picture that reflects the magic and joy synonymous with the Barbie brand"
    
    prompt = 'Cute colorful Barbie themed image'
    
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    print(response)
    


def main():
    # # Create Quote
    # quote = get_quote()
    # quote = quote.data[0].content[0].text.value
    # print('Quote', quote)
    
    # # Create Image Prompt
    # key_words = create_image_prompt(quote)
    # image_prompt = f'Create a cute colorful background with a Barbie silhouette using {key_words} as the theme'
    # print(image_prompt)
    
    # image_url = create_image(image_prompt)
    
    # # Download Image
    image_name = 'barbie_1.png'
    # image_path = download_image(image_url, image_name)
    quote = '"Smile, because your sparkling spirit can light up the world"'

    # Add text to the image
    add_image_text(image_path=image_name, text=quote, font_path='JustAnotherHand-Regular.ttf', color='pink', desaturated=False)
    
    
if __name__ == "__main__":
    main()
    # create_profile()