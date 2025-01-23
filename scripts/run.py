import os
from dotenv import load_dotenv
from pyrogram import Client
from google import genai  # Assuming this is the correct import for the Gemini API

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key from the .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Initialize the Pyrogram client
app = Client("my_account")


def remove_formatting(text):
    """
    Remove any formatting (e.g., Markdown, HTML, or special characters) from the text.
    """
    # Remove Markdown formatting (e.g., **bold**, `code`, etc.)
    text = text.replace("**", "").replace("`", "").replace("__", "")

    # Remove HTML tags (if any)
    text = "".join([char for char in text if char.isalnum() or char.isspace() or char in [".", ",", "!", "?"]])

    # Remove extra spaces
    text = " ".join(text.split())

    return text


async def main():
    async with app:
        try:
            # Ask the user for a query
            user_query = input("Enter your query (e.g., 'Good morning message'): ")

            # Define the prompt for Gemini
            prompt = f"""
            I will share you a query of mine. Based on that you will generate the best message so that I can send it to a person whom I want directly. Do not need to show me options just give me the message in this format: {{}} `
            My query is: {user_query}.
            For more Context : Whom I am sending this messsage is my wife, Tyu.
            """

            # Generate the message using Gemini
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp', 
                contents=prompt
            )
            generated_message = response.text

            # Remove formatting from the generated message
            clean_message = remove_formatting(generated_message)

            # Print the generated message (for debugging)
            print("Generated Message:", clean_message)

            # Send the clean message to your wife's Telegram username
            await app.send_message("@tyucat", clean_message)
            print("Message sent to @tyucat!")
        except Exception as e:
            print(f"An error occurred: {e}")


# Run the Pyrogram client
app.run(main())