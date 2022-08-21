from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
currentCard = {}
toLearn = {}

try:
    data = pandas.read_csv("data/wordsToLearn.csv")
except:
    originalData = pandas.read_csv("data/french_words.csv")
    toLearn = originalData.to_dict(orient="records")
else:
    toLearn = data.to_dict(orient="records")

# Read data
def nextCard():
    global currentCard, flipTimer
    window.after_cancel(flipTimer)
    currentCard = random.choice(toLearn)
    print(currentCard["French"])
    canvas.itemconfig(cardTitle, text="French", fill="black")
    canvas.itemconfig(cardWord, text=currentCard["French"], fill="black")
    canvas.itemconfig(cardBackground, image=frontImage)
    flipTimer = window.after(3000, func=flipCard)


# Flip the cards, switch language
def flipCard():
    global currentCard
    canvas.itemconfig(cardTitle, text="English", fill="white")
    canvas.itemconfig(cardWord, text=currentCard["English"], fill="white")
    canvas.itemconfig(cardBackground, image=backImage)

def isKnown():
    toLearn.remove(currentCard)
    nextCard()
    newData = pandas.DataFrame(toLearn)
    newData.to_csv("data/wordsToLearn.csv", index=False)

# Window setup
window = Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flipTimer = window.after(3000, func=flipCard)

# Canvas setup
canvas = Canvas(width=800, height=526)
frontImage = PhotoImage(file="images/card_front.png")
backImage = PhotoImage(file="images/card_back.png")

cardBackground = canvas.create_image(400, 263, image=frontImage)
cardTitle = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
cardWord = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Button setup
crossImage = PhotoImage(file="images/wrong.png")
unknownButton = Button(image=crossImage, highlightthickness=0, command=nextCard)
unknownButton.grid(row=1, column=0)

checkImage = PhotoImage(file="images/right.png")
knownButton = Button(image=checkImage, highlightthickness=0, command=isKnown)
knownButton.grid(row=1, column=1)

nextCard()




window.mainloop()