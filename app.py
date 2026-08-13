import os 
from google import genai 
from dotenv import load_dotenv
import time

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

user_input = input("Ask Gemini: ")


def generate_with_retry(client, user_input, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            response = client.models.generate_content(
                model = "gemini-3.5-flash",
                contents=user_input
            )
            return response

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")

            #Don't retry after the final attempt
            if attempt == max_attempts:
                print("All attempts failed.")
                return None

            #For now, wait before trying again
            wait_time = 2 ** (attempt - 1)
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

response = generate_with_retry(client, user_input)

if response:
    print(response.text)