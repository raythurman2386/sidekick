from dotenv import load_dotenv
from db.database import add_message, get_chat_log
from openai import OpenAI
from utils.utils import handle_error

load_dotenv()
client = OpenAI()


def img_generation(prompt, quality, size):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            n=1,
        )

        img_url = response.data[0].url
        return img_url
    except Exception as e:
        return handle_error(e)


def ask_gpt(question, model, temperature):
    models = {
        "GPT 3.5 Turbo": "gpt-3.5-turbo",
        "GPT 4": "gpt-4",
        "GPT 4 Turbo": "gpt-4-1106-preview",
    }
    try:
        # Insert the user's message into the database
        add_message("user", question)

        # Retrieve the chat log from the database
        chat_log = get_chat_log()

        return client.chat.completions.create(
            model=models[model],
            messages=chat_log,
            temperature=temperature,
            max_tokens=500,
            stream=True,
        )

    except Exception as e:
        return handle_error(e)
