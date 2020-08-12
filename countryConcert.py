#coding:utf-8

from tkinter import *
import sqlite3

# After importing the module sqlite 3, I connect countryConcert.py file to the countryMusic.db database.
connection = sqlite3.connect("countryMusic.db")
cursor = connection.cursor()

# I created the subclass ConcertApp of the build-in parent class Tkinter.
class ConcertApp(Tk):
	def __init__(self):
		Tk.__init__(self)
# I set up a special font, the tittle and the three first line of my GUI in the constructor. 
		self.headerFont = ("Helvetica", "16", "bold italic")

		self.title("Country Concert Selector (Data provided by SeatGeek)")
		Label(self).grid(row = 0, column = 0)
		Label(self, text = "June in Country Music", font = self.headerFont).grid(row = 1, columnspan = 6)
		Label(self).grid(row = 2, column = 0)
		Label(self, width = 1).grid(row = 3, column = 0)

# I also gave control to the five following methods.
		self.stateMenu()
		self.dayMenu()
		self.priceMenu()
		self.addButton()
		self.outputText()

# In this method, I built the components of the GUI related to the selection of the state.
	def stateMenu(self):
# First, I set up a Menubutton for displaying my menu in the graphic interface.
		stateMenuButton = Menubutton(self, text = "Select your State", relief = "raised")
		stateMenuButton.grid(row = 3, column = 1)
# Then, I set up the menu.
		menuOfStateMenuButton = Menu(stateMenuButton, tearoff = 0)
		stateMenuButton["menu"] = menuOfStateMenuButton
# I created a second table directly in DB Browser (without converting a cvs file). I used a loop to fill my menu with one checkbutton 
# (labeled with the name of the state) for each state. I choose add_checkbutton rather than add_command so that in my resultDisplayer() method,
# I will be able to use the state (ON/OFF) of these checkbuttons to direct my branching structure (see next comment). However, I added to my checkbuttons
# a command directing the programm to the method selectionDisplayer(). This method will simply display the label of the checkbutton in the output text fiel
# named outputSate. Thus, the user will be able to see the parameters of its selection (state, date, price) before he directs the programm to the resultDisplayer()
# method pushing the button buttonShowsResults.
		cursor.execute("SELECT * FROM stateTable")
# I set up a control variable for my checkbuttons on the form of an integer (I started with StringVar() but I had difficulties with the offvalue that I need to be 0). 
# I kept my offvalue set up on the default value 0 and I also supllied an alternate value for the onvalue, which is the index of its respective state 
# in the stateTable of the database. Thus, if the checkbuttons are OFF, the resultDisplayer() method will retrieve the value 0. Inversely, if a checkbutton is ON,
# the resultDisplayer() method will retrieve the integer corresponding to the index of the table stateTable of the database countryMusic.db. Then, using SQL language,
# we first have to retrieve the respective state in the table stateTable. Lastly, using this result, we can retrieve all the data we need in the main table concertTable
# related to the previous result.
		self.stateVar = IntVar()
		for state in cursor:
			menuOfStateMenuButton.add_checkbutton(label = state[1], variable = self.stateVar, onvalue = state[0], command = self.selectionDisplayer)
# This output label field is designed for displaying the label of the checkbutton selected.
		self.outputSate = Label(self, bg = "#fff", anchor = "e", relief = "groove")
		self.outputSate.grid(row = 4, column = 1, sticky = "we") 
		Label(self).grid(row = 5, column = 1)

# This method works excatly the same way that the stateMenu() method but it is based on the table dayTable in the countryMusic.db database.
	def dayMenu(self):
		dayMenuButton = Menubutton(self, text = "Select your Date", relief = "raised")
		dayMenuButton.grid(row = 6, column = 1)

		menuOfDayMenuButton = Menu(dayMenuButton, tearoff = 0)
		dayMenuButton["menu"] = menuOfDayMenuButton

		cursor.execute("SELECT * FROM dayTable")
		self.dayVar = IntVar()
		for day in cursor:
			menuOfDayMenuButton.add_checkbutton(label = day[1], variable = self.dayVar, onvalue = day[0],  command = self.selectionDisplayer)

		self.outputDay = Label(self, bg = "#fff", anchor = "e", relief = "groove")
		self.outputDay.grid(row = 7, column = 1, sticky = "we")

# This method is designed to filter the database according a specific range price. Each checkbuttons cover a specific interval.
	def priceMenu(self):
		Label(self).grid(row = 8, column = 1)
		Label(self, text = "Price:", font = self.headerFont).grid(row = 9, column = 1)
# The variable control is still set up on its default value 0 when its respective checkbutton is OFF but this time the onvalue (still an integer) is the maximum value of the range price.
		self.priceVar = IntVar()

		priceCheckButton20 = Checkbutton(self, text = "less than $20", variable = self.priceVar, onvalue = 20)
		priceCheckButton20.grid(row = 10, column = 1, sticky = "w")

		priceCheckButton100 = Checkbutton(self, text = "$20-$99.99", variable = self.priceVar, onvalue = 100)
		priceCheckButton100.grid(row = 11, column = 1, sticky = "w")

		priceCheckButton200 = Checkbutton(self, text = "$100-$199.99", variable = self.priceVar, onvalue = 200)
		priceCheckButton200.grid(row = 12, column = 1, sticky = "w")

		priceCheckButton400 = Checkbutton(self, text = "$200-$399.99", variable = self.priceVar, onvalue = 400)
		priceCheckButton400.grid(row = 13, column = 1, sticky = "w")
		Label(self).grid(row = 14, column = 1)

# This method is designed to display the result of the resultDisplayer() method.
	def outputText(self):
		self.textConcert = Text(self, width = 80, height = 25)
		self.textConcert.grid(row = 5, column = 3, columnspan = 2, rowspan = 25)

# This method is designed to build and display on the GUI, all the buttons needed.
	def addButton(self):
		self.buttonShowResults = Button(self, text = "Show Results", height = 2, width = 30, command = self.resultDisplayer)
		self.buttonShowResults.grid(row = 3, column = 3, rowspan = 2)

		self.buttonClearResults = Button(self, text = "Clear Results", height = 2, width = 30, command = self.clearResult)
		self.buttonClearResults.grid(row = 3, column = 4, rowspan = 2)

		self.buttonClearSelection = Button(self, text = "Clear Selection", height = 2, command = self.clearSelection)
		self.buttonClearSelection.grid(row = 15, column = 1, rowspan = 2)
# These "empty label," are simply used to set the GUI appropriately.
		Label(self, height = 10).grid(row = 17, column = 1)
		Label(self, width = 1).grid(row = 3, column = 2)
		Label(self, width = 1).grid(row = 3, column = 5)

# This method, actioned by the button buttonCearResult, is designed to clear the output text field.
	def clearResult(self):
		self.textConcert.delete(1.0, END)

# This method, actioned by the button buttonClearSelection, is designed for clearing the output labels outputSate and outputDay. It is also designed for 
# setting the variable controls stateVar, dayVar and priceVar to 0. Thus, after pushing the button buttonClearSelection, all checkbuttons will be OFF.
	def clearSelection(self):
		self.stateVar.set(0)
		self.outputSate["text"] = ""

		self.dayVar.set(0)
		self.outputDay["text"] = ""

		self.priceVar.set(0)

# As said previously, this method is designed to display the label of the checkbutton selected, before the user send the program in the resultDisplayer().
# The state of the checkbuttons of the method priceMenu() are directly visible on the GUI.
# The body of this method will be decribed in the next method.
	def selectionDisplayer(self):
		indexState = self.stateVar.get()
		statePy = ""
		cursor.execute("SELECT * FROM stateTable WHERE id = ?", (indexState,))
		for i in cursor:
			statePy = i[1]
		self.outputSate["text"] = statePy

		indexDay = self.dayVar.get()
		dayPy = ""
		cursor.execute("SELECT * FROM dayTable WHERE id = ?", (indexDay,))
		for i in cursor:
			dayPy = i[1]
		self.outputDay["text"] = dayPy

# In this last method are done all search in the main table concertTable of the countryMusic.db database.
	def resultDisplayer(self):
# We start by retrieving the value of the variable control stateVar and assigning this value to the local variable indexState.
		indexState = self.stateVar.get()
# We set up the local variable statePy as an empty string.
		statePy = ""
# If the checkbuttons are OFF, the program display the following message.
		if indexState == 0:
			self.outputSate["text"] = "No state selected"
# Else, it assigns to the variable statePy the state according the index value retrieved.
		else:
# The cursor is filled with the row of the table stateTable corresponding of the value of the index.
			cursor.execute("SELECT * FROM stateTable WHERE id = ?", (indexState,))
# For each row in the cursor, the following loop assigns to the variable statePy the item of the second column of the table. 
# Because the index is unique and independent, only one string (the content of the box row = index, column = 1) will be retrieved.
			for i in cursor:
				statePy = i[1]

# Same process for the local variable dayPy.
		indexDay = self.dayVar.get()
		dayPy = ""
		if indexDay == 0:
			self.outputDay["text"] = "No date selected"
		else:
			cursor.execute("SELECT * FROM dayTable WHERE id = ?", (indexDay,))
			for i in cursor:
				dayPy = i[1]

# The value of the variable control priceVar is retrieved and assigned to the local variable maxPrice.
		maxPrice = self.priceVar.get()
# I created a list, listing the offvalue and all onvalues that could be retrieved fron the priceMenu() method.
		listMaxPrice = [0,20,100,200,400]
# In this loop, when the program recognizes the variable maxPrice in the list listMaxPrice, it returns the index of this value.
# Then, if one of the checkbutton of the priceMenu() method is ON, the search in the table concertTable will be done in the following interval:
# [listMaxPrice[indexList - 1], listMaxPrice[indexList]).
		for i in range(len(listMaxPrice)):
			indexList = listMaxPrice.index(maxPrice)

# From now, we know what state, day and range price the user selected or not selected. In other word, the ON or OFF state of all checkbuttons of the program
# are exploitable to filter the main table concertTable of the database. Thus, we filter the databse according this last branching.

# When the "day" checkbuttons and the "price" checkbuttons are OFF:
		if indexDay == 0 and maxPrice == 0:
# The cursor is filled with all rows containing the selected state.
			cursor.execute("SELECT * FROM concertTable WHERE state = ?", (statePy,))
# And we unload the cursor in the text field of the GIU according the following .format()
			for i in cursor:
				self.textConcert.insert(INSERT,"{} from {}.\n{} at {}, {}.\nLocation: {}.\nPrice is starting from ${}.\nTry your link: {}\n \n".format(i[5], i[7], i[1], i[4], i[3], i[6], i[2], i[8]))
# Same process when only one of the "day" checkbuttons is ON.
		elif indexState == 0 and maxPrice == 0:
			cursor.execute("SELECT * FROM concertTable WHERE day = ?", (dayPy,))
			for i in cursor:
				self.textConcert.insert(INSERT,"{} from {}.\n{} at {}, {}.\nLocation: {}.\nPrice is starting from ${}.\nTry your link: {}\n \n".format(i[5], i[7], i[1], i[4], i[3], i[6], i[2], i[8]))
# Same process when only one of the "price" checkbuttons is ON.
		elif indexState == 0 and indexDay == 0:
			cursor.execute("SELECT * FROM concertTable WHERE minPrice >= ? AND minPrice < ?", (listMaxPrice[indexList - 1], listMaxPrice[indexList],))
			for i in cursor:
				self.textConcert.insert(INSERT,"{} from {}.\n{} at {}, {}.\nLocation: {}.\nPrice is starting from ${}.\nTry your link: {}\n \n".format(i[5], i[7], i[1], i[4], i[3], i[6], i[2], i[8]))
# When only the "day" checkbuttons are OFF, in other words, when only one of the "state" checkbuttons is ON and only one of the "price" checkbuttons is ON, 
# the cursor is filled according to the following SQL language instruction.
		elif indexDay == 0:
			cursor.execute("SELECT * FROM concertTable WHERE minPrice >= ? AND minPrice < ? AND state = ?", (listMaxPrice[indexList - 1], listMaxPrice[indexList], statePy,))
# This time, the cursor is unloaded in the local variable called rows.
			rows = cursor.fetchall()
# If the variable rows is empty, the text field textConcert displays the following message.
			if not rows:
				self.textConcert.insert(INSERT, "No results found\n")
# Else, the variable "rows" is diplayed in the text field of the GIU according the following .format().
			else:
				for i in rows:
					self.textConcert.insert(INSERT,"{} from {}.\n{} at {}, {}.\nLocation: {}.\nPrice is starting from ${}.\nTry your link: {}\n \n".format(i[5], i[7], i[1], i[4], i[3], i[6], i[2], i[8]))
# Same process when the "state" checkbuttons are OFF.
		elif indexState == 0:
			cursor.execute("SELECT * FROM concertTable WHERE minPrice >= ? AND minPrice < ? AND day = ?", (listMaxPrice[indexList - 1], listMaxPrice[indexList], dayPy,))
			rows = cursor.fetchall()
			if not rows:
				self.textConcert.insert(INSERT, "No results found\n")
			else:
				for i in rows:
					self.textConcert.insert(INSERT,"{} from {}.\n{} at {}, {}.\nLocation: {}.\nPrice is starting from ${}.\nTry your link: {}\n \n".format(i[5], i[7], i[1], i[4], i[3], i[6], i[2], i[8]))
# Same process when the "price" checkbuttons are OFF.
		elif maxPrice == 0:
			cursor.execute("SELECT * FROM concertTable WHERE state = ? AND day = ?", (statePy, dayPy,))
			rows = cursor.fetchall()
			if not rows:
				self.textConcert.insert(INSERT, "No results found\n")
			else:
				for i in rows:
					self.textConcert.insert(INSERT,"{} from {}.\n{} at {}, {}.\nLocation: {}.\nPrice is starting from ${}.\nTry your link: {}\n \n".format(i[5], i[7], i[1], i[4], i[3], i[6], i[2], i[8]))
# This last instruction directs the program in the case of one of each type of checkbuttons are ON.
		else:
			cursor.execute("SELECT * FROM concertTable WHERE minPrice >= ? AND minPrice < ? AND day = ? AND state = ?", (listMaxPrice[indexList - 1], listMaxPrice[indexList], dayPy, statePy,))
			rows = cursor.fetchall()
			if not rows:
				self.textConcert.insert(INSERT, "No results found\n")
			else:
				for i in rows:
					self.textConcert.insert(INSERT,"{} from {}.\n{} at {}, {}.\nLocation: {}.\nPrice is starting from ${}.\nTry your link: {}\n \n".format(i[5], i[7], i[1], i[4], i[3], i[6], i[2], i[8]))



def main():
	app = ConcertApp()
	app.mainloop()

if __name__ == "__main__":
	main()





