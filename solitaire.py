"""Game Logic.

info on events/binds http://www.python-course.eu/tkinter_events_binds.php

card images from http://jbfilesarchive.com/phpBB3/viewtopic.php?t=1003

"""
from Tkinter import *
from PIL import Image
from PIL import ImageTk
import random

def donothing():
   filewin = Toplevel(game)
   button = Button(filewin, text="Do nothing button")
   button.pack()
def about():
   filewin = Toplevel(game)
   button = Button(filewin, text="Game made by Turese Anderson 2017")
   button.pack()
def helpmenu():
   filewin = Toplevel(game)
   button = Button(filewin, text="<game rules go here>")
   button.pack()
#change color of the window
def changecolor(newcolor):
   game.configure(bg=newcolor)
   board.configure(bg=newcolor)
#tells game to reset
def reset():
   g.new_game()
   
game = Tk()
game.configure(bg='#0b7d28', width=800, height=500)
game.wm_title("Solitaire")


################
##### MENU #####
################
''' Creates menus to call commands above '''
menubar = Menu(game)

#File Menu
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New Game", command=reset)

colormenu = Menu(filemenu, tearoff=0)
filemenu.add_cascade(label="Change Game Color", menu=colormenu)
colormenu.add_command(label="Classic Green", command=lambda: changecolor('#0b7d28'))
colormenu.add_command(label="Red", command=lambda: changecolor('#7d0b0b'))
colormenu.add_command(label="Orange", command=lambda: changecolor('#d6690f'))
colormenu.add_command(label="Yellow", command=lambda: changecolor('#dec41d'))
colormenu.add_command(label="Green", command=lambda: changecolor('#0b7d4e'))
colormenu.add_command(label="Blue", command=lambda: changecolor('#0b597d'))
colormenu.add_command(label="Purple", command=lambda: changecolor('#6a0b7d'))
colormenu.add_command(label="Pink", command=lambda: changecolor('#d113ae'))
colormenu.add_command(label="Brown", command=lambda: changecolor('#8c420d'))


filemenu.add_command(label="Exit", command=game.quit)

filemenu.add_separator()

#Help Menu
helpmenu = Menu(menubar, tearoff=1)
helpmenu.add_command(label="Help Index", command=helpmenu)
helpmenu.add_command(label="About...", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)

#makes the menu show up
game.config(menu=menubar)

################
#### IMAGES ####
################
''' loads all images to be used in game '''

#load image of board background
bgimg = ImageTk.PhotoImage(file = 'background.png')

#load image of overturned card
cardback = ImageTk.PhotoImage(Image.open('cards/back.bmp'))

"""loaded images are a list of lists"""
## 0 = hearts
## 1 = diamonds
## 2 = clubs
## 4 = spades
"""inside the lists"""
### 0 = (nothing, just the number 0)
### 1 = ace
### 2 = two
### 3 = three
#...
### 10 = ten
### 11 = jack
### 12 = queen
### 13 = king
cards = [[0],[0],[0],[0]]
#load images of all cards into list
for i in range(1,14):
	if i < 10:
		cards[0].append(ImageTk.PhotoImage(Image.open('cards/h0' + str(i) + '.bmp')))
		cards[1].append(ImageTk.PhotoImage(Image.open('cards/d0' + str(i) + '.bmp')))
		cards[2].append(ImageTk.PhotoImage(Image.open('cards/c0' + str(i) + '.bmp')))
		cards[3].append(ImageTk.PhotoImage(Image.open('cards/s0' + str(i) + '.bmp')))
	else:
		cards[0].append(ImageTk.PhotoImage(Image.open('cards/h' + str(i) + '.bmp')))
		cards[1].append(ImageTk.PhotoImage(Image.open('cards/d' + str(i) + '.bmp')))
		cards[2].append(ImageTk.PhotoImage(Image.open('cards/c' + str(i) + '.bmp')))
		cards[3].append(ImageTk.PhotoImage(Image.open('cards/s' + str(i) + '.bmp')))

################
# VALUE TABLES #
################

# card values

values = {1: 'Ace', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six',
   7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Jack', 12: 'Queen', 13: 'King'}
suits = {0: 'Hearts', 1: 'Diamonds', 2: 'Clubs', 3: 'Spades'}
colors = {0: 'black', 1: 'red'}
sides = {0: 'facedown', 1: 'faceup'}

#x and y values on canvas

#[0] = x value, [1] = y value

"""
order for locations is
[0]: stack1
[1]: stack2
...
[6]: stack7
[7]:acepiles1 (hearts)
[8]:acepiles1 (diamonds)
[9]:acepiles1 (clubs)
[10]:acepiles1 (spades)
[11]:unflipped reserves
[12]:flipped reserves
"""

""" Reserve Piles """

locations = [[150, 60], [230, 60], [310, 60], [390, 60], [470, 60], 
[550, 60], [630, 60], [750, 90], [750, 190], [750, 290], [750, 390], [50, 340], [50, 450]]

""" stack y position is 60 + 30 * (position in stack) """

################
# GAME CLASSES #
################

#Class for individual cards
class Card(object):
   def __init__(self, value, suit):
      self.value = value
      self.suit = suit
      self.xpos=locations[11][0]
      self.ypos=locations[11][1]
      self.image = board.create_image(self.xpos, self.ypos, image = cardback)
      self.stack = 0
      self.index = 0
      if self.suit > 1:
         self.color = 0
      else:
         self.color = 1
      self.side = 0
   def name(self):
      return self.pValue() + ' of ' + self.pSuit()

   #functions that return various attributes of the cards. functions 
   #with lowercase p in front of them return the 'printable' string versions
   def set_side(self, num):
      self.side = num
      board.delete(self.image)
      if num == 0:
         self.image = board.create_image(self.xpos, self.ypos, image = cardback)
      else:
         self.image = board.create_image(self.xpos, self.ypos, image = cards[self.suit][self.value])
   def Xposition(self):
      return self.xpos
   def Yposition(self):
      return self.ypos
   def movecard(self,x,y):
      board.move(self.image, x - self.xpos,y - self.ypos)
      self.xpos = x
      self.ypos = y
   # calculates where to move based on stack it has been moved to
   def stackmove(self,stack,index):
   	self.stack = stack
   	self.index = index
   	if stack < 7:
   		self.movecard(locations[stack][0], locations[stack][1] + 30 * index)
   	else:
   		self.movecard(locations[stack][0], locations[stack][1])
      

#-x-#

#Class for a Deck of cards
class Deck(object):
	def __init__(self):
		self.deck = []
		for i in range(1,14):
			for j in range(0,4):
				self.deck.append(Card(i,j))

	#Flips all cards facedown
	def flip_down_all(self):
		for card in self.deck:
			card.set_side(0)

	def shuffle(self):
		random.shuffle(self.deck)

	#prints the names of all cards in deck in whatever order they're currently in
	def list(self):
		for card in self.deck:
			print(card.name() + " ")

#Class for game logic
class Game(object):
	def __init__(self):
		self.d = Deck()
		self.stacks = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
		self.nummoves = 0
		self.timer = 0
		self.clear()

	def clear(self):
		for i in range(0, len(self.stacks) - 1):
			for j in range (0, len(self.stacks[i]) - 1):
				board.delete(self.stacks[i][j].image)
		self.stacks = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
		self.nummoves = 0
		self.timer = 0
		self.d.flip_down_all()

	def new_game(self):
		self.d.shuffle()
		self.clear()
		self.fill_stack(0, 0, 1)
		self.fill_stack(1, 1, 2)
		self.fill_stack(2, 3, 3)
		self.fill_stack(3, 6, 4)
		self.fill_stack(4, 10, 5)
		self.fill_stack(5, 15, 6)
		self.fill_stack(6, 21, 7)
		self.fill_reserve(28)
		self.flip_fronts()

	#Retrieves stack
	def get_stack(self, stacknum):
		return self.stacks[stacknum]


	#Fills a stack with numcards cards from the deck starting at deckindex 
	def fill_stack(self,stacknumber,deckindex,numcards):
		for i in range(deckindex, deckindex + numcards):
			currcard = self.d.deck[i]
			self.stacks[stacknumber].append(self.d.deck[i])
			currcard.stackmove(stacknumber,len(self.stacks[stacknumber]) - 1)

	#Fills reserve with all remaining cards in the deck 
	def fill_reserve(self,deckindex):
		for i in range(deckindex, 52):
			card = self.d.deck[i]
			self.stacks[11].append(card)
			card.stackmove(11,len(self.stacks[11]) - 1)

	#Goes through all cards on the front of the stacks, and flips them if they are facedown.
	def flip_fronts(self):
		for i in range(7):
			if len(self.stacks[i]) > 0:
				if self.stacks[i][len(self.stacks[i]) - 1].side == 0:
					self.stacks[i][len(self.stacks[i]) - 1].set_side(1)

	#checks validity of a move of a single card
	def attempt_move(self,stackfrom,indexfrom,stackto):
		if self.stacks[stackfrom][indexfrom].side == 0:
			return False
		elif stackto > 10:
			return False
		cardfrom = self.stacks[stackfrom][indexfrom]
		if stackto == 7 and cardfrom.suit != 0:
			return False
		elif stackto == 8 and cardfrom.suit != 1:
   			return False
		elif stackto == 9 and cardfrom.suit != 2:
   			return False
		elif stackto == 10 and cardfrom.suit != 3:
   			return False
   		#checks if moving multiple cards not into the first 7 stacks
   		if stackto >= 7 and indexfrom < (len(self.stacks[stackfrom]) - 1):
   			return False
		elif len(self.stacks[stackto]) == 0:
			#if moved to an empty slot, check if card is a king
			if stackto < 7 and cardfrom.value != 13:
				return False
			#do checks on moving to empty acepiles
			elif stackto >= 7 and stackto <= 10:
				if cardfrom.value != 1:
					return False
		else:
			cardto = self.stacks[stackto][len(self.stacks[stackto]) - 1]
			if stackto < 7:
				if cardfrom.color == cardto.color:
					return False
				if cardfrom.value != cardto.value - 1:
					return False
			if stackto >= 7 and stackto <= 10:
				if cardfrom.value != cardto.value + 1:
					return False	
			#checks if placing a too high or low card into the acepiles, given at least an ace has been placed
		return True

	#completes a move
	def move(self,stackfrom,indexfrom,stackto):
		#check if moving multiple cards
		card = self.stacks[stackfrom][indexfrom]
		if self.attempt_move(stackfrom, indexfrom, stackto):
			for i in range(indexfrom, len(self.stacks[stackfrom])):
				card = self.stacks[stackfrom][indexfrom]
				self.stacks[stackto].append(card)
				self.stacks[stackfrom].pop(indexfrom)
				card.stackmove(stackto, len(self.stacks[stackto]) - 1)
				board.tag_raise(card.image)
		else:
			for i in range(indexfrom, len(self.stacks[stackfrom])):
				card = self.stacks[stackfrom][i]
				card.stackmove(card.stack, card.index)
				board.tag_raise(card.image)
		self.flip_fronts()

	#completes a move without checking for validity
	def reserve_move(self, stackfrom, indexfrom, stackto):
		card = self.stacks[stackfrom][indexfrom]
		self.stacks[stackto].append(card)
		self.stacks[stackfrom].pop(indexfrom)
		card.stackmove(stackto, len(self.stacks[stackto]) - 1)

	#moves through the reserves
	def turn_reserves(self):
		if len(self.stacks[11]) > 0:
			self.stacks[11][len(self.stacks[11]) - 1].set_side(1)
			g.reserve_move(11, len(self.stacks[11]) - 1, 12)
		elif len(self.stacks[12]) > 0:
			for card in self.stacks[12]:
				card.set_side(0)
			while len(self.stacks[12]) > 0:
				g.reserve_move(12,len(self.stacks[12]) - 1, 11)
		else: 
			return

################
## BACKGROUND ##
################

#create frame to put background on
frame = Frame(game)
frame.pack()

#create canvas to be used as gameboard
board = Canvas(bg='#0b7d28', width=800, height=500, bd=0, highlightthickness=0)
board.create_image(3, 3, image = bgimg, anchor=NW) 

board.pack()

g = Game()

g.new_game()

#################
### DRAG/DROP ###
#################

#https://stackoverflow.com/questions/44887576/how-make-drag-and-drop-interface
class DragManager():
	def __init__(self, widget, game):
		self.notdrag = True
		self.game = game
		self.card = ""
		self.widget = widget

	def add_dragable(self):
		self.widget.bind("<ButtonPress-1>", self.on_start)
		self.widget.bind("<B1-Motion>", self.on_drag)
		self.widget.bind("<ButtonRelease-1>", self.on_drop)
		self.widget.configure(cursor="hand1")

	def on_start(self, event):
        # you could use this method to create a floating window
        # that represents what is being dragged.
        #print "clicked at", event.x, event.y
   		#first, if clicked on reserve pile, flips over the last card and makes it useable
		stack = self.find_stack(event.x, event.y)
		if stack == 11:
			self.notdrag = True
			self.game.turn_reserves()
		elif stack != 11:
			if len(self.game.stacks[stack]) == 0:
				self.notdrag = True
			else:
				self.card = self.find_card(stack, event.y)
				self.notdrag = False

    #returns what number stack the x pos and y pos fall within
	def find_stack(self, xpos, ypos):
		if xpos > 116 and xpos < 186 and ypos > 5 and ypos < 485:
			return 0
		elif xpos > 196 and xpos < 266 and ypos > 5 and ypos < 485:
			return 1
		elif xpos > 276 and xpos < 346 and ypos > 5 and ypos < 485:
			return 2
		elif xpos > 356 and xpos < 426 and ypos > 5 and ypos < 485:
			return 3
		elif xpos > 436 and xpos < 506 and ypos > 5 and ypos < 485:
			return 4
		elif xpos > 516 and xpos < 586 and ypos > 5 and ypos < 485:
			return 5
		elif xpos > 596 and xpos < 666 and ypos > 5 and ypos < 485:
			return 6
		elif xpos > 718 and xpos < 785 and ypos > 45 and ypos < 138:
			return 7
		elif xpos > 718 and xpos < 785 and ypos > 145 and ypos < 238:
			return 8
		elif xpos > 718 and xpos < 785 and ypos > 245 and ypos < 338:
			return 9
		elif xpos > 718 and xpos < 785 and ypos > 345 and ypos < 438:
			return 10
		elif xpos > 17 and xpos < 86 and ypos > 294 and ypos < 390:
			return 11
		elif xpos > 17 and xpos < 86 and ypos > 405 and ypos < 495:
			return 12

	def on_drag(self, event):
		if not self.notdrag:
			counter = 0
			for i in range(self.card.index, len(self.game.stacks[self.card.stack])):
				card = self.game.stacks[self.card.stack][i]
				card.movecard(event.x, event.y + 30 * counter)
				counter += 1
				board.tag_raise(card.image)

	# find the stack under the cursor
	def on_drop(self, event):
		if not self.notdrag:
			x,y = event.x, event.y
			movestack = self.find_stack(x, y)
			if movestack is not None:
				self.game.move(self.card.stack, self.card.index, movestack)
			else:
				self.card.stackmove(self.card.stack,self.card.index)

	#the stack it's in and the y position, find out which card in the stack was clicked on
	def find_card(self, stacknum, ypos):
		#fix so it can drag whole stacks
		y = ypos
		index = -1
		stack = self.game.stacks[stacknum]
		if stacknum < 7:
			while y > 12:
				y -= 30
				index += 1
		if index != -1 and len(stack) - 1 > index:
			card = stack[index]
			return card
		else:
			return stack[len(stack) - 1]

dragger = DragManager(board, g)
dragger.add_dragable()

game.mainloop()
