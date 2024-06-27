from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

random_word = {}
updated_dict = []


def right():
    global random_word, updated_dict
    updated_dict.remove(random_word)
    learn_df = pandas.DataFrame(updated_dict)
    learn_df.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def next_card():
    global random_word, flip_timer, updated_dict
    window.after_cancel(flip_timer)
    try:
        df = pandas.read_csv("data/words_to_learn.csv")
    except FileNotFoundError:
        df = pandas.read_csv("data/french_words.csv")
    finally:
        updated_dict = df.to_dict(orient="records")
        random_word = random.choice(updated_dict)

        canvas.itemconfigure(canvas_image, image=card_front_img)
        canvas.itemconfigure(title_text, text="French", fill="black")
        canvas.itemconfigure(word_text, text=f"{random_word['French']}", fill="black")
        flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfigure(canvas_image, image=card_back_img)
    canvas.itemconfigure(title_text, text="English", fill="white")
    canvas.itemconfigure(word_text, text=f"{random_word['English']}", fill="white")


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)

title_text = canvas.create_text(400, 150, text="Title", font=("Ariel", 20, "italic"))
word_text = canvas.create_text(400, 253, text="Word", font=("Ariel", 30, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_btn_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_btn_img, highlightthickness=0, command=lambda: [next_card(), right()])
right_button.grid(row=1, column=1)

left_btn_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=left_btn_img, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()

window.mainloop()


