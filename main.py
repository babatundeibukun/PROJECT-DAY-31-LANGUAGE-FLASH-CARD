from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pd.read_csv("data/words to learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = (random.choice(to_learn))
    current_word = current_card["French"]
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=current_word, fill="black")
    canvas.itemconfig(old_image, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    # The English part
    canvas.itemconfig(old_image, image=card_back_img)
    current_word = current_card["English"]
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_word, fill="white")


def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words to learn")
    next_card()


window = Tk()
window.title("Flash card")
flip_timer = window.after(3000, func=flip_card)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
canvas = Canvas(width=800, height=530)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
old_image = canvas.create_image(400, 265, image=card_front_img)
title = canvas.create_text(400, 150, text=" ", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text=" ", font=("Arial", 40, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, command=is_known)
right_button.grid(column=0, row=1)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, command=next_card)
wrong_button.grid(column=1, row=1)

next_card()
window.mainloop()
