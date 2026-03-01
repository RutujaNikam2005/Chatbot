import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
import difflib

# Load data
data = pd.read_csv("qa.csv")

# Create window
root = tk.Tk()
root.title("My Chatbot")
root.geometry("400x500")

# Chat area with scroll
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
chat_area.pack(pady=10)

# Input box
entry = tk.Entry(root, width=30)
entry.pack(side=tk.LEFT, padx=10)

# Chat function
def send():
    user_input = entry.get().lower()
    
    if user_input == "":
        return
    
    chat_area.insert(tk.END, "You: " + user_input + "\n")

    questions = data["question"].str.lower().tolist()
    matches = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.5)

    if matches:
        index = questions.index(matches[0])
        response = data["answer"][index]
    else:
        response = "I don't know. Teach me!"

    chat_area.insert(tk.END, "Bot: " + response + "\n\n")

    # Auto scroll
    chat_area.yview(tk.END)

    entry.delete(0, tk.END)

# Clear chat
def clear_chat():
    chat_area.delete("1.0", tk.END)

# Buttons
send_btn = tk.Button(root, text="Send", command=send)
send_btn.pack(side=tk.LEFT)

clear_btn = tk.Button(root, text="Clear", command=clear_chat)
clear_btn.pack(side=tk.LEFT, padx=5)

# Run app
root.mainloop()