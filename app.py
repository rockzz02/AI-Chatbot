from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]
# print(openai.api_key)


# Setting up flask app
app = Flask(__name__)

# Home page route
@app.route("/")
def home():
    return render_template("index.html")


chat_history = []
# ChatBot Route
@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_input = request.form["message"]
    prompt = f"User: {user_input}\nChatbot: "
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        stop=["\nUser: ", "\nChatbot: "]
    )

    # Extracting the response text from the OpenAI API result
    bot_response = response.choices[0].text.strip()

    # Adding user input and bot response to the chat history
    chat_history.append([user_input, bot_response])

    # Render the Chatbot template with the response text
    return  render_template(
        "chatbot.html",
        chat_history=chat_history
    )

if __name__ == '__main__':
    app.run(debug=True)