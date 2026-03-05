import tkinter as tk
import pandas as pd
import difflib
import datetime
import os

# -------- SAFE CSV LOAD --------
if not os.path.exists("qa.csv"):
    df = pd.DataFrame(columns=["question", "answer"])
    df.to_csv("qa.csv", index=False)

data = pd.read_csv("qa.csv")

root = tk.Tk()
root.title("Smart Chatbot")
root.resizable(True, True)
root.configure(bg="#111b21")

# -------- CENTER WINDOW --------
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

title = tk.Label(
    header,
    text="🤖 Smart Chatbot",
    bg="#202c33",
    fg="white",
    font=("Segoe UI", 14, "bold")
)
title.pack(side=tk.LEFT, padx=15)

menu_btn = tk.Button(
    header,
    text="⋮",
    bg="#202c33",
    fg="white",
    border=0,
    font=("Segoe UI", 16, "bold"),
    cursor="hand2"
)
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

    if sender == "user":
        bubble_color = "#005c4b"
        anchor_pos = "e"
    else:
        bubble_color = "#202c33"
        anchor_pos = "w"

    wrap_length = root.winfo_width() - 160

    bubble = tk.Label(
        msg_frame,
        text=message,
        wraplength=wrap_length,
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

# Welcome Message
add_message("Hello 👋 I'm SmartBot!\nHow can I help you today?", "bot")

# -------- SMART COMMANDS --------
def handle_commands(text):
    if text == "/time":
        return f"⏰ Current Time: {datetime.datetime.now().strftime('%H:%M:%S')}"
    elif text == "/date":
        return f"📅 Today's Date: {datetime.date.today()}"
    elif text == "/help":
        return "Available Commands:\n/time\n/date\n/clear\n/help"
    elif text == "/clear":
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        return "Chat cleared ✅"
    return None

# -------- MOOD MODE (Day 26) --------
def detect_mood(text):
    text = text.lower()

    if any(word in text for word in ["sad", "upset", "depressed", "cry"]):
        return "😔 I'm here for you. Things will get better."
    elif any(word in text for word in ["happy", "excited", "great"]):
        return "😊 That's amazing! Keep smiling!"
    elif any(word in text for word in ["angry", "mad", "irritated"]):
        return "😌 Take a deep breath. Stay calm."
    return None

# -------- SEND FUNCTION --------
def send(event=None):
    global data

    user_input = entry.get().strip()
    if user_input == "":
        return

    add_message(user_input, "user")
    entry.delete(0, tk.END)

    # Smart Commands
    command_response = handle_commands(user_input.lower())
    if command_response:
        root.after(400, lambda: add_message(command_response, "bot"))
        return

    # Mood Detection
    mood_response = detect_mood(user_input)
    if mood_response:
        root.after(400, lambda: add_message(mood_response, "bot"))
        return

    # Normal QA
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