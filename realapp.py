import tkinter as tk
import pandas as pd
import difflib

data = pd.read_csv("qa.csv")

root = tk.Tk()
root.title("Smart Chatbot")
root.geometry("400x600")
root.resizable(False, False)

# --------- HEADER ---------

header = tk.Frame(root, bg="#075e54", height=50)
header.pack(fill=tk.X)

title = tk.Label(
    header,
    text="Smart Chatbot",
    bg="#075e54",
    fg="white",
    font=("Arial", 14, "bold")
)
title.pack(side=tk.LEFT, padx=10)


# Three dots menu
menu_btn = tk.Button(
    header,
    text="⋮",
    bg="#075e54",
    fg="white",
    border=0,
    font=("Arial", 18, "bold")
)
menu_btn.pack(side=tk.RIGHT, padx=10)

# --------- CHAT AREA ---------

chat_frame = tk.Frame(root)
chat_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(chat_frame, bg="#e5ddd5")
scrollbar = tk.Scrollbar(chat_frame, command=canvas.yview)

scrollable_frame = tk.Frame(canvas, bg="#e5ddd5")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=380)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# --------- MESSAGE FUNCTION ---------

def add_message(message, sender):
    msg_frame = tk.Frame(scrollable_frame, bg="#e5ddd5")
    msg_frame.pack(fill=tk.X, pady=5, padx=5)

    bubble = tk.Label(
        msg_frame,
        text=message,
        wraplength=250,
        padx=10,
        pady=6,
        font=("Arial", 10)
    )

    if sender == "user":
        bubble.config(bg="#dcf8c6")
        bubble.pack(anchor="e")
    else:
        bubble.config(bg="white")
        bubble.pack(anchor="w")

    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

# --------- SEND FUNCTION ---------

def send(event=None):
    global data

    user_input = entry.get().lower()
    if user_input == "":
        return

    add_message(user_input, "user")

    questions = data["question"].str.lower().tolist()
    matches = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.5)

    if matches:
        index = questions.index(matches[0])
        response = data["answer"][index]
    else:
        response = "I don't know yet."

    add_message(response, "bot")

    entry.delete(0, tk.END)

# --------- BOTTOM BAR ---------

bottom_frame = tk.Frame(root, bg="#f0f0f0", height=70)
bottom_frame.pack(fill=tk.X)
bottom_frame.pack_propagate(False)  # keeps height fixed
bottom_frame.config(bg="#202c33")

# Attachment button
attach_btn = tk.Button(bottom_frame, text="📎")
attach_btn.pack(side=tk.LEFT, padx=5, pady=10)

# Entry
entry = tk.Entry(bottom_frame, font=("Arial", 14),bg="white",fg="black",insertbackground="black")
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

# Mic button
mic_btn = tk.Button(bottom_frame, text="🎤")
mic_btn.pack(side=tk.LEFT, padx=5)
mic_btn.config(font=("Arial",10,"bold"))

# Send button (pack FIRST)
send_btn = tk.Button(bottom_frame, text="Send", width=7, command=send)
send_btn.pack(side=tk.RIGHT, padx=8, pady=10)
send_btn.config(font=("Arial",10,"bold"))

# Camera button (pack AFTER send)
camera_btn = tk.Button(bottom_frame, text="📷", width=7)
camera_btn.pack(side=tk.RIGHT, padx=5, pady=10)
camera_btn.config(font=("Arial",10,"bold"))

# ENTER key works
root.bind("<Return>", send)

root.mainloop()