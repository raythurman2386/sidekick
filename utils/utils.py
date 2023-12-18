
from utils.logger import app_logger



async def format_response(response):
    """This function will be used to take the response from chat gpt and format it for Discord."""
    # Convert response to a string if it's not already
    response = str(response)

    # Discord uses markdown for formatting, I'm testing different system prompts to return the response in advance before implementing this fully
    formatted_response = f"{response}"

    return formatted_response


class CustomError(Exception):
    pass


def handle_error(e):
    if isinstance(e, CustomError):
        app_logger.warning(f"There has been an error: {e}")
        return str(e)
    else:
        # Log the error or handle it as needed
        app_logger.error(f"There has been an error: {e}")
        return "Blimey! Something went wrong: " + str(e)
