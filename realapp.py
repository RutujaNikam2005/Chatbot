import tkinter as tk
import pandas as pd
import difflib

# Load CSV data
data = pd.read_csv("qa.csv")

# Create window
root = tk.Tk()
root.title("Chatbot")
root.geometry("400x500")

# Chat display
chat_area = tk.Text(root, height=20, width=50)
chat_area.pack(pady=10)

# Input box
entry = tk.Entry(root, width=30)
entry.pack(side=tk.LEFT, padx=10)

# Send function
def send():
    global data

    user_input = entry.get().lower()

    if user_input == "":
        return

    chat_area.insert(tk.END, "You: " + user_input + "\n")

    questions = data["question"].str.lower().tolist()

    matches = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.5)

    # If match found
    if matches:
        index = questions.index(matches[0])
        response = data["answer"][index]
        chat_area.insert(tk.END, "Bot: " + response + "\n\n")

    # If not found → learn
    else:
        chat_area.insert(tk.END, "Bot: I don't know. Teach me!\n")
        
        new_answer = entry.get()  # you can modify if needed
        
        # Ask in terminal (simple version)
        new_answer = input("Enter answer in terminal: ")

        if new_answer.lower() in ["exit", "show"]:
            chat_area.insert(tk.END, "Bot: Not saved (reserved word)\n\n")
        else:
            new_data = pd.DataFrame({
                "question": [user_input],
                "answer": [new_answer]
            })

            data = pd.concat([data, new_data], ignore_index=True)
            data.to_csv("qa.csv", index=False)

            chat_area.insert(tk.END, "Bot: Learned successfully!\n\n")

    entry.delete(0, tk.END)

# Send button
send_btn = tk.Button(root, text="Send", command=send)
send_btn.pack(side=tk.LEFT)

# Run app
root.mainloop()