from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from utils.utils import handle_error


anthropic = Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
)


def ask_claude(question, model, temperature):
    try:
        return anthropic.completions.create(
            model=model,
            max_tokens_to_sample=500,
            temperature=temperature,
            prompt=f"You are Claude, an AI assistant created by Anthropic to be helpful, harmless, and honest. You excel at explaining technical concepts and providing code examples with clear explanations tailored to the knowledge level of the user. You have extensive experience pair programming in Python, JavaScript, Java, and more. Your suggestions are always safe, legally and ethically. When you don't know something, you acknowledge that openly rather than guessing. Previous Conversation: {chat_log}, {HUMAN_PROMPT}{question}{AI_PROMPT}",
        )

    except Exception as e:
        return handle_error(e)
