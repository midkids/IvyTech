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
12/7/2022 - Added exit button
12/10/2022 - Added ability to press enter key in place of SUBMIT button
12/10/2022 - Added dividing of score by rounded minutes
12/10/2022 - Added losing rating
12/10/2022 - Changed hard-code literals to class constants
12/12/2022 - Added additional comments
12/13/2022 - Added high score components and logic
"""
# imports
from breezypythongui import EasyFrame
from tkinter import PhotoImage
from tkinter.font import Font
from random import randint
from threading import Timer

# PEMDAS class
class PEMDAS(EasyFrame):
    
    # class constants
    POINTS2MISSES = 10  # Number of points awarded if user had two misses
    POINTS1MISS = 30    # Number of points awarded if user had one misses
    POINTS0MISSES = 50  # Number of points awarded if user had no misses
    APPRENTICE = 4      # Number of operators needed to attain apprentice message
    EXPERT = 7          # Number of operators needed to attain expert message
    MASTER = 10         # Number of operators needed to attain master message
    LOSERATING = 200    # Number of points needed to to determine lose message

    def __init__(self):
        """
        PEMDAS class constructor
        """
        EasyFrame.__init__(self, title = "PEMDAS+")
        self.setResizable(False)
        self.setBackground("lightyellow")

        # instance variables not associated with window components
        self.nbrOperators = 1   # the number of operators in expression
        self.expresssion = ""   # the expression being presented to user
        self.evaluation = 0     # the evaluation expression (solution)
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
            sticky = "NS")
        self.addLabel(text = "Timer",
            font = normalFont,
            background = "lightyellow",
            row = 1, column = 1,
            sticky = "NS")
        self.addLabel(text = "Lives",
            font = normalFont,
            background = "lightyellow",
            row = 1, column = 2,
            sticky = "NS")
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
            "GET expression - solve - enter answer - SUBMIT or press Return",
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
        self.answer.bind("<Return>",    # allow Return key to submit answer
             lambda event: self.checkAnswer())
        self.addLabel(text = "Get expression",
            font = normalFont,
            background = "lightyellow",
            row = 8, column = 0, 
            sticky = "NSEW")
        self.addLabel(text = "answer",
            font = normalFont,
            background = "lightyellow",
            row = 8, column = 1, 
            sticky = "NSEW")
        self.addLabel(text = "Submit expression",
            font = normalFont,
            background = "lightyellow",
            row = 8, column = 2, 
            sticky = "NSEW")
        self.addButton(text = "RESET", # reset game
            row = 10, column = 0,
            state = "normal",
            command = self.resetGame)
        self.highScore = self.addIntegerField(value = 0,    # user score
            row = 10, column = 1,
            width = 7, sticky = "NS",
            state = "readonly") 
        self.addButton(text = "EXIT", # exit game
            row = 10, column = 2,
            state = "normal",
            command = self._close)
        self.addLabel(text = "Reset game",
            font = normalFont,
            background = "lightyellow",
            row = 11, column = 0, 
            sticky = "NSEW")
        self.addLabel(text = "High Score",
            font = normalFont,
            background = "lightyellow",
            row = 11, column = 1, 
            sticky = "NSEW")
        self.addLabel(text = "Exit game",
            font = normalFont,
            background = "lightyellow",
            row = 11, column = 2, 
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
            # otherwise select an integer from 1-5, again to keep
            # the solution manageable for the user
            while operator == "**" and usedExponent: # keep getting operator until not exponent
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
        self.secondCount = 0
        ### self.ticker = Timer(1, self.timerLoop)  # the timer
        # call timerLoop to time user between GET and SUBMIT
        self.timerLoop()    # start timer
        
        
    def timerLoop(self):
        self.timer.setNumber(self.secondCount)  # set timer
        self.secondCount += 1
        self.ticker = Timer(1, self.timerLoop)  # the timer
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
        minutes = round(self.secondCount / 60) # compute minutes from timer seconds
        if minutes == 0:    # minimum minutes is 1
            minutes = 1
        if self.attempts == 3:
            getScore += round(PEMDAS.POINTS2MISSES/minutes)
        elif self.attempts == 2:
            getScore += round(PEMDAS.POINTS1MISS/minutes)
        else:
            getScore += round(PEMDAS.POINTS0MISSES/minutes)
        self.score.setNumber(getScore)  # set updated user score
        self.resetExpression()    # reset expression
        # user progresses or wins game
        if self.nbrOperators == PEMDAS.APPRENTICE:
            self.messageBox(title = "WIN", 
                message = "You are now a PEMDAS+ apprentice!\nKeep going!")
        if self.nbrOperators == PEMDAS.EXPERT:
            self.messageBox(title = "WIN", 
                message = "You are now a PEMDAS+ expert!\nWill you be a master?")
        if self.nbrOperators > PEMDAS.MASTER:
            self.messageBox(title = "WIN", 
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
        determines if the user has lost the game (lives < 1).
        """
        self.attempts += 1  # increment number of user attempts  
        # user hit limit of incorrect solutions 
        if self.attempts == 3:
            self.ticker.cancel()  # stop timer in timerLoop
            self.messageBox(title = "SOLUTION",
                message = "The correct answer was: " + str(self.evaluation))
            getLives = self.lives.getNumber()
            getLives -= 1  
            self.lives.setNumber(getLives)
            self.resetExpression()    # reset expression
            if self.nbrOperators > 1:   # decrement number of operators
                self.nbrOperators -= 1
            if self.lives.getNumber() < 1:    # user lost game
                if self.score.getNumber() < PEMDAS.LOSERATING:
                    self.messageBox(title = "LOSE", 
                    message = "Study up. Try again!\nResetting game.")
                else:
                    self.messageBox(title = "LOSE", 
                    message = "Nice effort. Try again!\nResetting game.")
                self.resetGame()
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
        The resetExpression method resets the game
        in preparation for presenting the next 
        expression to the user.
        """
        self.ticker.cancel()
        self.secondCount = 0
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
        Check for and set high score if applicable.
        """
        getScore = self.score.getNumber()
        getHighScore = self.highScore.getNumber()
        if getScore > getHighScore:     # update high score if applicable
            self.highScore.setNumber(getScore) 
        self.score.setNumber(0)
        self.lives.setNumber(3)
        self.nbrOperators = 1
        self.resetExpression()
        

    def _close(self):
        """
        Cancel the timer and destroy it.
        """
        try:
            self.ticker.cancel()  # stop timer in timerLoop
        except:
            print("user pressed exit without getting any expressions")
        self.master.destroy()


# main method
def main():
 
    BR = PEMDAS()   # instantiate PEMDAS object
    BR.mainloop()   # run program
       
# check to see if module being called 
if __name__ == "__main__":  
    main()