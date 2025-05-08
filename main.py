from tkinter import *
import pandas
import random

timer = None

current_card = {}
to_learn = {}
BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pandas.read_csv('data/to_learn.csv')
except FileNotFoundError:
    original = pandas.read_csv('data/french_words.csv')
    to_learn = original.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')



def next_card():
    global current_card, flip_timer

    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title_text, text='French', fill='black')
    canvas.itemconfig(word_text, text=current_card['French'], fill='black')
    canvas.itemconfig(image_card, image=card_front)
    flip_timer = window.after(3000, func=count_down)


def count_down():
    canvas.itemconfig(title_text, text='English', fill='white')
    canvas.itemconfig(word_text, text=current_card['English'], fill='white')
    canvas.itemconfig(image_card, image=card_back)


def remove_card():
    to_learn.remove(current_card)
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv('data/to_learn.csv', index=False)
    next_card()
    return new_data








#----------------------------- UI -------------------------------------#
window = Tk()
window.title('Flash card app')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, count_down)

canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness= 0)
card_front = PhotoImage(file='images/card_front.png')
card_back = PhotoImage(file='images/card_back.png')
image_card = canvas.create_image(400, 265, image=card_front)
title_text = canvas.create_text(400, 150, text='language', fill='black', font=('Ariel', 40, 'italic'))
word_text = canvas.create_text(400, 263, text='title', fill='black', font=('Ariel', 60, 'bold'))
canvas.grid(column=0, row=0, columnspan=2)


right_btn_image = PhotoImage(file='images/right.png')
right_button = Button(image=right_btn_image, borderwidth=0, bg=BACKGROUND_COLOR, highlightthickness= 0, command=remove_card)
right_button.grid(column=1, row=1)

wrong_btn_image = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_btn_image, borderwidth=0, bg=BACKGROUND_COLOR, highlightthickness= 0, command=next_card)
wrong_button.grid(column=0, row=1)


next_card()

window.mainloop()