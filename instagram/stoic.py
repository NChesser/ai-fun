'''
    About: Stoic Quote Generator Using Open AI Assistants
    Author: Nick Chesser
'''

# Imports
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
        assistant_id='asst_h0fg8EPinwjHOsrnkXa1zeQN'
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
    

def main():
    # Create Quote
    quote = get_quote()
    quote = quote.data[0].content[0].text.value
    print('Quote', quote)    

    # Create Image Prompt
    key_words = create_image_prompt(quote)
    image_prompt = f'Create a sketch of a stoic on a linen paper-color background using {key_words} as the theme'
    print(image_prompt)
    
    # Create Image
    # image_prompt = 'create a stoic based picture using embrace, adversity, character as the theme.'
    # image_prompt = 'Create a sketch of a stoic on a linen paper-color background using embrace, adversity, character as the theme.'
    # image_prompt = 'Create a sketch of a stoic on a linen paper-color background using experience, wisdom, soil, growth as the theme. Include the following quote in the image "From every experience, extract wisdom, for in its soil blooms the flower of personal growth."'
    # Cinzel
    image_url = create_image(image_prompt)
    
    # # Download Image
    image_name = 'stoic_2.png'
    image_path = download_image(image_url, image_name)
    
    # quote = '"Amid chaos and disorder, be the tranquil soul accepting the way of the world, not asking for it to bend to your will."'
    # quote = '"Embrace adversity, for it is within its crucible that our true character is forged."'
    # quote = '"True tranquility comes not from silencing the world, but from silencing the turmoil within."'
    # Add text to the image
    add_image_text(image_path=image_name, text=quote)
    
    
    
if __name__ == "__main__":
    main()