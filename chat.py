import pandas as pd
import difflib
import os

# Create file if not exists
if not os.path.exists("qa.csv"):
    data = pd.DataFrame({
        "question": ["hi", "hello", "bye"],
        "answer": ["Hello!", "Hi there!", "Goodbye!"]
    })
    data.to_csv("qa.csv", index=False)

# Load data
data = pd.read_csv("qa.csv")

print("Bot: Ask me anything (type 'exit' to quit, 'show' to view data)")

while True:
    user_input = input("You: ").lower().strip()

    # Exit
    if user_input == "exit":
        print("Bot: Goodbye!")
        break

    # Show data
    if user_input == "show":
        print(data)
        continue

    questions = data["question"].str.lower().tolist()

    # 🔥 Get top matches
    matches = difflib.get_close_matches(user_input, questions, n=3, cutoff=0.5)

    # 🔥 Calculate best score
    best_match = None
    highest_score = 0

    for question in questions:
        score = difflib.SequenceMatcher(None, user_input, question).ratio()
        if score > highest_score:
            highest_score = score
            best_match = question

    print("Confidence:", round(highest_score * 100, 2), "%")

    # If match found
    if matches:
        print("Top matches:", matches)

        for match in matches:
            index = questions.index(match)
            print("Bot:", data["answer"][index])

    # If no match → learn
    else:
        print("Bot: I don't know. Teach me!")
        new_answer = input("Enter answer: ").strip()

        # Avoid wrong inputs
        if new_answer.lower() in ["exit", "show"] or new_answer == "":
            print("Bot: Invalid answer. Not saved.")
            continue

        if user_input not in questions:
            new_data = pd.DataFrame({
                "question": [user_input],
                "answer": [new_answer]
            })

            data = pd.concat([data, new_data], ignore_index=True)
            data.to_csv("qa.csv", index=False)

            print("Bot: Learned successfully!")
        else:
            print("Bot: I already know this question!")