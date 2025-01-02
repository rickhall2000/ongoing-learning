import dotenv
import os
import openai

dotenv.load_dotenv()

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def translate_text(text: str) -> str:
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates English to French."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content


def main():
    print(translate_text("Good morning, how are you?"))

if __name__ == "__main__":
    main()
