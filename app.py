from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

app = Flask(__name__)

# Create a new chat bot
bot = ChatBot('HistoricalPlacesBot')

# Define a list of historical places and their information
historical_places_info = {}
with open('places.txt', 'r') as file:
    for line in file:
        place, info = line.strip().split(':')
        historical_places_info[place.strip()] = info.strip()

# Create training data by pairing place names with their descriptions as individual entries
training_data = []
for place, info in historical_places_info.items():
    training_data.append(f"What is the history of {place}?")
    training_data.append(info)
    training_data.append(f"Tell me about {place}.")
    training_data.append(info)
    training_data.append(place)
    training_data.append(info)

# Train the chat bot with the historical places information
trainer = ListTrainer(bot)
trainer.train(training_data)

@app.route("/")
def home():
    initial_response = "Welcome! Please type the name of a place you are interested in learning about its history."
    return render_template("index.html", initial_response=initial_response)

@app.route("/get")
def get_bot_response():
    user_input = request.args.get('msg')
    response = bot.get_response(user_input)
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)