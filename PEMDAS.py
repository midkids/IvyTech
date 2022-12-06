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
12/5/2022 - Added parentheses logic, reset game button
12/5/2022 - Added timer
"""
# imports
from breezypythongui import EasyFrame
from tkinter import PhotoImage
from tkinter.font import Font
from random import randint
from time import sleep
from threading import Timer

# PEMDAS class
class PEMDAS(EasyFrame):

    def __init__(self):
        EasyFrame.__init__(self, title = "PEMDAS+")
        self.setResizable(False)
        self.setBackground("lightyellow")

        # instance variables not associated with window components
        self.nbrOperators = 1   # the number of operators in expression
        self.expresssion = ""   # the expression being presented to user
        self.evaluation = 0     # the evaluation expression (solution)
        self.attempts = 0       # the number of user attempts to solve expression
        self.timing = False     # Boolean to start and stop time

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
        self.addLabel(text = "Timer",
            font = normalFont,
            background = "lightyellow",
            row = 1, column = 1,
            sticky = "NS")
        self.addLabel(text = "Lives",
            font = normalFont,
            background = "lightyellow",
            row = 1, column = 2,
            sticky = "W")
        self.score = self.addIntegerField(value = 0,    # user score
            row = 2, column = 0,
            width = 7, sticky = "NS",
            state = "readonly")
        self.timer = self.addIntegerField(value = 0,    # timer between get expressions
            row = 2, column = 1,
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
        self.addButton(text = "RESET", # reset game
            row = 10, column = 1,
            state = "normal",
            command = self.resetGame)
        self.addLabel(text = "Press RESET to completely reset game",
            font = normalFont,
            background = "lightyellow",
            row = 11, column = 1, 
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

        # Boolean to ensure only one exponentiation operator is 
        # added to expression to keep resolution simple
        usedExponent = False   

        buildExpression = str(randint(1,5)) # expression contents
        # add the appropriate number of operators base on past results
        for build in range(self.nbrOperators):  
            operator = operators[randint(0,3)]  # get random operator
            # if operator is exponentation, make the exponent 2
            # to keep the solution manageable for user
            # other wise select an integer from 1-5, again to keep
            # the solution manageable for the user
            while operator == "**" and usedExponent:
                operator = operators[randint(0,3)]
            buildExpression += operator 
            if operator == "**":    
                buildExpression += "2"
                usedExponent = True
            else:    
                buildExpression += str(randint(1,5))
                evenOdd = randint(1,2)
                print("evenOdd", evenOdd)
                if evenOdd % 2 == 0 and \
                    self.nbrOperators > 1 and \
                    buildExpression[-3] != ")" and \
                    buildExpression[-5:-3] != "**":
                    expressionSlice1 = buildExpression[0:len(buildExpression)-3:]
                    print("exp1", expressionSlice1)
                    expressionSlice2 = buildExpression[-3:]
                    print("exp2", expressionSlice2)
                    buildExpression = expressionSlice1 + "(" + expressionSlice2 + ")"
        self.expressionText.setText(buildExpression)
        self.expression = buildExpression
        self.getButton["state"] = "disabled"
        self.submitButton["state"] = "normal"
        self.locked = PhotoImage(file = "lock2b.gif")   # display locked lock
        self.imageLabel["image"] = self.locked
        self.timing = True
        self.secondCount = 0
        
        # call timerLoop to time user between GET and SUBMIT
        self.timerLoop()    # start timer
        
        
    def timerLoop(self):
        self.timer.setNumber(self.secondCount)  # set timer
        self.secondCount += 1
        self.ticker = Timer(1, self.timerLoop)
        self.ticker.start()
            

    def checkAnswer(self):
        """
        The checkAnswer method evaluates the expression
        presented to the user and then determines if the 
        user correctly solved the expresssion.
        """
        # eval function solves string expression
        self.evaluation = eval(self.expression)
        try:
            userAnswer = self.answer.getNumber()    # get user solution
        except ValueError:
            self.messageBox(title = "ERROR",
                message = "Answer must be an integer.")
        # if user solution correct
        if self.evaluation == userAnswer:
            self.correct()
        else:
            self.incorrect()
    
    def correct(self):
        """
        The correct method awards the user points based
        on the number of attempts it took them to solve
        the expression. It calls the resetExpression method to reset
        the application for presenting the next expression
        to the user. It determines if the user has won
        the game.
        """
        self.ticker.cancel()  # stop timer in timerLoop
        self.locked = PhotoImage(file = "lock2a.gif")   # display unlocked lock
        self.imageLabel["image"] = self.locked
        self.messageBox(title = "CORRECT", 
            message = "Solution is correct!")
        self.attempts += 1  # increment number of user attempts  
        getScore = self.score.getNumber()   # get current user score
        if self.attempts == 3:
            getScore += 10
        elif self.attempts == 2:
            getScore += 25
        else:
            getScore += 50
        self.score.setNumber(getScore)  # set updated user score
        self.resetExpression()    # reset expression
        # user wins game
        if self.nbrOperators == 4:
            self.messageBox(title = "APPRENTICE", 
                message = "You are now a PEMDAS+ apprentice!\nKeep going!")
        if self.nbrOperators == 8:
            self.messageBox(title = "EXPERT", 
                message = "You are now a PEMDAS+ expert!\nWill you be a master?")
        if self.nbrOperators > 10:
            self.messageBox(title = "MASTER", 
                message = "You are a PEMDAS+ master!\nGame will now reset!")
            self.resetGame()
        self.nbrOperators += 1

    def incorrect(self):
        """
        The incorrect method increments the number of user
        attempts. If the user has more than the allowed 
        number of unsuccessful attempts, it decrements the
        number of user lives, it decrements the number of
        operators to be included in the next expression, and 
        it calls the resetExpression method to reset the 
        expression for presentation to the user. It 
        determines if the user has lost the game.
        """
        self.attempts += 1  # increment number of user attempts  
        # user hit limit of incorrect solutions 
        if self.attempts == 3:
            self.messageBox(title = "SOLUTION",
            message = "The correct answer was: " + str(self.evaluation))
            getLives = self.lives.getNumber()
            getLives -= 1  
            self.lives.setNumber(getLives)
            self.resetExpression()    # reset expression
            if self.nbrOperators > 1:   # decrement number of operators
                self.nbrOperators -= 1
            if getLives < 1:    # user lost game
                self.messageBox(title = "NOVICE", 
                message = "Study up and try again!")
        else:
            if 3 - self.attempts > 1:
                self.messageBox(title = "INCORRECT", 
                    message = "Solution is incorrect. You have " + 
                    str(3 - self.attempts) + " attempts left.")
            else:
                self.messageBox(title = "INCORRECT", 
                    message = "Solution is incorrect. You have 1 attempt left.")
    
    def resetExpression(self):
        """
        The resetExpression method resets the 
        expression for presentation to the user.
        """
        self.timer.setNumber(0)
        self.getButton["state"] = "normal"
        self.submitButton["state"] = "disabled"
        self.expression = ""
        self.expressionText.setText("")
        self.answer.setNumber(0)
        self.attempts = 0

    def resetGame(self):
        """
        The resetGame method resets the application
        to allow the user to start completely over.
        """
        self.score.setNumber(0)
        self.lives.setNumber(3)
        self.nbrOperators = 1
        self.resetExpression()

    def _close(self):
        self.ticker.cancel()  # stop timer in timerLoop
        print("made it")
        self.master.destroy()



# main method
def main():
 
    BR = PEMDAS()
    BR.mainloop()
       

if __name__ == "__main__":  # check to see if module being called 
    main()