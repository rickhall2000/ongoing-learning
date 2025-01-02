import dotenv
import os
import openai


dotenv.load_dotenv()

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = """
Describe the following movie using emojis.

{movie}: """

# Few-show examples
examples = [
    { "input": "Titanic", "output": "🛳️🌊❤️🧊🎶🔥🚢💔👫💑" },
    { "input": "The Matrix", "output": "🕶️💊💥👾🔮🌃👨🏻‍💻🔁🔓💪" }
]


movie = "Toy Story"

# Sending the examples and then asking the question for Toy Story
movie = "Toy Story"
response = openai_client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt.format(movie=examples[0]["input"])},
        {"role": "assistant", "content": examples[0]["output"]},
        {"role": "user", "content": prompt.format(movie=examples[1]["input"])},
        {"role": "assistant", "content": examples[1]["output"]},
        {"role": "user", "content": prompt.format(movie=movie)},
  ]
)

print(response.choices[0].message.content)
