"""
PROGRAM: PEMDAS.py    
AUTHOR: Myron Snelson
CREATION DATE VERSION 1: 12/2/2022
PURPOSE: The purpose of this application is to challenge 
new computer science students to resolve expressions 
using correct operator precedence. Its goal is to 
make the learning of operator precedence fun yet 
challenging for new computer science students. Note, 
to keep the emphasis on order of operations and not 
math, the integers used are limited and the 
generated exponents are always 2.
MODIFICATIONS BY VERSION:
12/2/2022 - Laid out main window (no logic)
12/3/2022 - Added essential logic
12/4/2022 - Added comments, background color
"""
# imports
from breezypythongui import EasyFrame
from tkinter import PhotoImage
from tkinter.font import Font
from random import randint

# PEMDAS class
class PEMDAS(EasyFrame):

    def __init__(self):
        EasyFrame.__init__(self, title = "PEMDAS+")
        self.setResizable(False)
        self.setBackground("lightyellow")

        # instance variables not associated with window components
        self.nbrOperators = 1   # the number of operators in expression
        self.expresssion = ""   # the expression being presented to user
        self.attempts = 0       # the number of user attempts to solve expression

        # fonts
        titleFont = Font(family = "Verdana", size = 20, slant = "italic")
        instructionsFont = Font(family = "Verdana", size = 12, slant = "italic")
        normalFont = Font(family = "Verdana", size = 12)

        # window layout
        self.addLabel(text = "PEMDAS+", 
            font = titleFont,
            foreground = "red",
            background = "lightyellow",
            row = 0, column = 1,
            sticky = "NSEW")
        self.addLabel(text = "Score",
            font = normalFont,
            background = "lightyellow",
            row = 1, column = 0,
            sticky = "W")
        self.addLabel(text = "Lives",
            font = normalFont,
            background = "lightyellow",
            row = 1, column = 2,
            sticky = "W")
        self.score = self.addIntegerField(value = 0,    # user score
            row = 2, column = 0,
            width = 7, sticky = "NS",
            state = "readonly")
        self.lives = self.addIntegerField(value = 3,    # user lives
            row = 2, column = 2,
            width = 1, sticky = "NS",
            state = "readonly")
        self.imageLabel = self.addLabel(text = "", row = 3, column = 1, # image label
            sticky = "NSEW")
        self.addLabel(text = 
            "GET expression - solve - enter answer - SUBMIT",
            font = instructionsFont,
            foreground = "red",
            background = "lightyellow",
            row = 4, column = 1, 
            sticky = "NSEW")
        self.addLabel(text = "expression",
            font = normalFont,
            background = "lightyellow",
            row = 5, column = 1, 
            sticky = "NSEW")
        self.expressionText = self.addTextField(text = "",  # expression presented to user
            row = 6, column = 1, sticky = "EW",
            state = "readonly") 
        self.getButton = self.addButton(text = "GET",   # get expression
            row = 7, column = 0,
            command = self.getExpression)
        self.answer = self.addIntegerField(value = 0,   # user solution to expression
            row = 7, column = 1, width = 20, sticky = "NS")
        self.submitButton = self.addButton(text = "SUBMIT", # check user solution
            row = 7, column = 2,
            state = "disabled",
            command = self.checkAnswer)
        self.addLabel(text = "answer",
            font = normalFont,
            background = "lightyellow",
            row = 8, column = 1, 
            sticky = "NSEW")
    
        # add initial image - must be a GIF
        self.locked = PhotoImage(file = "lock2b.gif")   # create locked instance variable
        self.imageLabel["image"] = self.locked

    # class methods
    def getExpression(self):
        """
        The getExpression method builds the expression that the user
        will be asked to solve.
        """
        # operators to include in expression
        # no division operator to avoid decimals
        operators = ["+", "-", "*", "**"]

        buildExpression = str(randint(1,5)) # expression contents
        # add the appropriate number of operators base on past results
        for build in range(self.nbrOperators):  
            operator = operators[randint(0,3)]  # get random operator
            # if operator is exponentation, make the exponent 2
            # to keep the solution manageable for user
            # other wise select an integer from 1-5, again to keep
            # the solution manageable for the user
            buildExpression += operator
            if operator == "**":    
                buildExpression += "2"
            else:    
                buildExpression += str(randint(1,5))
        self.expressionText.setText(buildExpression)
        self.expression = buildExpression
        self.getButton["state"] = "disabled"
        self.submitButton["state"] = "normal"
        self.locked = PhotoImage(file = "lock2b.gif")   # display locked lock
        self.imageLabel["image"] = self.locked

    def checkAnswer(self):
        """
        The checkAnswer method evaluates the expression
        presented to the user and then determines if the 
        user correctly solved the expresssion.
        """
        # eval function solves string expression
        evaluation = eval(self.expression)
        try:
            userAnswer = self.answer.getNumber()    # get user solution
        except ValueError:
            self.messageBox(title = "ERROR",
                message = "Answer must be an integer.")
        # if user solution correct
        if evaluation == userAnswer:
            self.locked = PhotoImage(file = "lock2a.gif")   # display unlocked lock
            self.imageLabel["image"] = self.locked
            self.messageBox(title = "CORRECT", 
                message = "You solution is correct!")
            self.correct()
        else:
            self.messageBox(title = "INCORRECT", 
                message = "You solution is incorrect.")
            self.incorrect()
    
    def correct(self):
        """
        The correct method awards the user points based
        on the number of attempts it took them to solve
        the expression. It calls the reset method to reset
        the application for presenting the next expression
        to the user. It determines if the user has won
        the game.
        """
        self.attempts += 1  # increment number of user attempts  
        getScore = self.score.getNumber()   # get current user score
        if self.attempts == 3:
            getScore += 10
        elif self.attempts == 2:
            getScore += 25
        else:
            getScore += 50
        self.score.setNumber(getScore)  # set updated user score
        self.reset()    # reset application
        self.nbrOperators += 1
        # user wins game
        if self.nbrOperators > 5:
            self.messageBox(title = "WINNER", 
                message = "You are now a PEMDAS expert!")

    def incorrect(self):
        """
        The incorrect method increments the number of user
        attempts. If the user has more than the allowed 
        number of unsuccessful attempts, it decrements the
        number of user lives, it decrements the number of
        operators to be included in the next expression, and 
        it calls the reset method to reset the application for 
        presenting the next expression to the user. It 
        determines if the user has lost the game.
        """
        self.attempts += 1  # increment number of user attempts  
        # user hit limit of incorrect solutions 
        if self.attempts > 2:
            getLives = self.lives.getNumber()
            getLives -= 1  
            self.lives.setNumber(getLives)
            self.reset()    # reset application
            if self.nbrOperators > 1:   # decrement number of operators
                self.nbrOperators -= 1
            if getLives < 1:    # user lost game
                self.messageBox(title = "BEGINNER", 
                message = "Study up and try again!")
    
    def reset(self):
        """
        The reset method resets the application in
        preparation for presenting the next expression
        to the user.
        """
        self.getButton["state"] = "normal"
        self.submitButton["state"] = "disabled"
        self.expression = ""
        self.expressionText.setText("")
        self.answer.setNumber(0)
        self.attempts = 0        


# main method
def main():
    PEMDAS().mainloop()

if __name__ == "__main__":  # check to see if module being called 
    main()