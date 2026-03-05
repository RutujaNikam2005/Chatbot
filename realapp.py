import tkinter as tk
import pandas as pd
import difflib
import datetime
import os
import json

# -------- SAFE CSV LOAD --------
if not os.path.exists("qa.csv"):
    df = pd.DataFrame(columns=["question", "answer"])
    df.to_csv("qa.csv", index=False)

data = pd.read_csv("qa.csv")

# -------- MEMORY FILE --------
if not os.path.exists("memory.json"):
    with open("memory.json", "w") as f:
        json.dump({}, f)

def load_memory():
    with open("memory.json", "r") as f:
        return json.load(f)

def save_memory(memory):
    with open("memory.json", "w") as f:
        json.dump(memory, f)

memory = load_memory()

# -------- WINDOW --------
root = tk.Tk()
root.title("Smart Chatbot")
root.resizable(True, True)
root.configure(bg="#111b21")

window_width = 420
window_height = 650
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# -------- HEADER --------
header = tk.Frame(root, bg="#202c33", height=55)
header.pack(fill=tk.X)

title = tk.Label(header, text="🤖 Smart Chatbot",
                 bg="#202c33", fg="white",
                 font=("Segoe UI", 14, "bold"))
title.pack(side=tk.LEFT, padx=15)

menu_btn = tk.Button(header, text="⋮",
                     bg="#202c33", fg="white",
                     border=0,
                     font=("Segoe UI", 16, "bold"),
                     cursor="hand2")
menu_btn.pack(side=tk.RIGHT, padx=15)

# -------- CHAT AREA --------
chat_frame = tk.Frame(root, bg="#111b21")
chat_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(chat_frame, bg="#111b21", highlightthickness=0)
scrollbar = tk.Scrollbar(chat_frame, command=canvas.yview)

scrollable_frame = tk.Frame(canvas, bg="#111b21")
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def resize_canvas(event):
    canvas.itemconfig(window_id, width=event.width)

canvas.bind("<Configure>", resize_canvas)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# -------- MESSAGE FUNCTION --------
def add_message(message, sender):
    msg_frame = tk.Frame(scrollable_frame, bg="#111b21")
    msg_frame.pack(fill=tk.X, pady=6, padx=10)

    bubble_color = "#005c4b" if sender == "user" else "#202c33"
    anchor_pos = "e" if sender == "user" else "w"

    bubble = tk.Label(
        msg_frame,
        text=message,
        wraplength=root.winfo_width() - 160,
        justify="left",
        bg=bubble_color,
        fg="white",
        font=("Segoe UI", 10),
        padx=12,
        pady=8
    )

    bubble.pack(anchor=anchor_pos)
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

# Welcome
add_message("Hello 👋 I'm SmartBot!\nHow can I help you today?", "bot")

# -------- MEMORY HANDLER --------
def handle_memory(user_input):
    global memory
    text = user_input.lower()

    if "my name is" in text:
        name = user_input.split("is")[-1].strip()
        memory["name"] = name
        save_memory(memory)
        return f"Nice to meet you, {name} 😊"

    if "i like" in text:
        like = user_input.split("like")[-1].strip()
        memory["likes"] = like
        save_memory(memory)
        return f"Got it! You like {like} 👍"

    if "remember that" in text:
        fact = user_input.replace("remember that", "").strip()
        memory["fact"] = fact
        save_memory(memory)
        return "I'll remember that 💾"

    if "what is my name" in text:
        return f"Your name is {memory.get('name', 'I don’t know yet.')}"

    if "what do i like" in text:
        return f"You like {memory.get('likes', 'I don’t know yet.')}"

    return None

# -------- SEND FUNCTION --------
def send(event=None):
    global data

    user_input = entry.get().strip()
    if user_input == "":
        return

    add_message(user_input, "user")
    entry.delete(0, tk.END)

    # Memory Feature
    memory_response = handle_memory(user_input)
    if memory_response:
        root.after(400, lambda: add_message(memory_response, "bot"))
        return

    # QA System
    questions = data["question"].astype(str).str.lower().tolist()
    matches = difflib.get_close_matches(user_input.lower(), questions, n=1, cutoff=0.5)

    if matches:
        index = questions.index(matches[0])
        response = data["answer"][index]
    else:
        response = "🤖 I don't know yet."

    root.after(500, lambda: add_message(response, "bot"))

# -------- BOTTOM FRAME (UNCHANGED UI) --------
bottom_frame = tk.Frame(root, bg="#202c33", height=75)
bottom_frame.pack(fill="x", side="bottom")

chat_bar = tk.Frame(bottom_frame, bg="#2a3942", bd=0)
chat_bar.pack(fill="x", padx=12, pady=12)

def open_attachment():
    print("Attachment clicked")

def open_camera():
    print("Camera clicked")

def start_voice():
    print("Voice started")

attach_btn = tk.Button(chat_bar, text="📎", font=("Segoe UI Emoji", 14),
                       bg="#2a3942", fg="white", bd=0,
                       cursor="hand2", activebackground="#36454f",
                       command=open_attachment)
attach_btn.pack(side="left", padx=6)

camera_btn = tk.Button(chat_bar, text="📷", font=("Segoe UI Emoji", 14),
                       bg="#2a3942", fg="white", bd=0,
                       cursor="hand2", activebackground="#36454f",
                       command=open_camera)
camera_btn.pack(side="left", padx=6)

entry = tk.Entry(chat_bar, font=("Segoe UI", 11),
                 bg="#111b21", fg="white",
                 insertbackground="white", bd=0)
entry.pack(side="left", fill="x", expand=True, padx=10, ipady=6)

mic_btn = tk.Button(chat_bar, text="🎤", font=("Segoe UI Emoji", 14),
                    bg="#2a3942", fg="white", bd=0,
                    cursor="hand2", activebackground="#36454f",
                    command=start_voice)
mic_btn.pack(side="right", padx=6)

send_btn = tk.Button(chat_bar, text="➤",
                     font=("Segoe UI", 12, "bold"),
                     bg="#00a884", fg="white",
                     activebackground="#019875",
                     activeforeground="white",
                     bd=0, padx=14, pady=6,
                     cursor="hand2", command=send)
send_btn.pack(side="right", padx=6)

root.bind("<Return>", send)
root.mainloop()