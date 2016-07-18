from Tkinter import *
import urllib
import urllib2
import io
import base64
from BeautifulSoup import BeautifulSoup

class App:



	def __init__(self, master):
		frame = Frame(master)
		frame.pack()

		#Labels
		self.searchLabel = Label(frame, text="Search Book:")
		self.titleLabel = Label(frame, text="Title:")
		self.authorLabel = Label(frame, text="Author:")
		self.ISBNLabel = Label(frame, text="ISBN:")
		self.booksReadLabel = Label(frame, text="Books Read")

		
		#Entries
		self.searchBookEntry = Entry(frame)
		self.titleEntry = Entry(frame, state=DISABLED)
		self.authorEntry = Entry(frame, state=DISABLED)
		self.ISBNEntry = Entry(frame, state=DISABLED)
		self.descriptionEntry = Text(frame, height=10, width=50, state=DISABLED)
		
		#buttons
		self.searchBookButton = Button(frame, text="Search", command =self.searchForBook)
		self.addBookButton = Button(frame, text="Add to Completed", command =self.addToCompleted)
		self.clearButton = Button(frame, text="Clear", command =self.clearData)
		self.deleteButton = Button(frame, text="Delete", command =self.deleteFromList)

		#listbox
		self.listBox = Listbox(frame)



		#pack

		self.searchLabel.grid(row=0, column=0)
		self.searchBookEntry.grid(row=0, column=1)
		self.searchBookButton.grid(row=0, column=2)
		self.booksReadLabel.grid(row=0, column=3)



		self.titleLabel.grid(row=1, column=1)
		self.titleEntry.grid(row=1, column=2)
		self.listBox.grid(row=1, column=3, rowspan=6)

		#On selection of item in listbox
		def onselect(evt):
			w = evt.widget
			index = int(w.curselection()[0])
			value = w.get(index)
			self.searchBookEntry.delete(0, 'end')
			self.searchBookEntry.insert(END, w.get(index))
			

		fr = open('readbooks.txt', 'r')
		for line in fr:
			self.listBox.insert(END, line)
		fr.close()


		self.listBox.bind('<<ListboxSelect>>', onselect)

		self.authorLabel.grid(row=2, column=1)
		self.authorEntry.grid(row=2, column=2)

		self.ISBNLabel.grid(row=3, column=1)
		self.ISBNEntry.grid(row=3, column=2)


		self.descriptionEntry.grid(row=6, column=1, rowspan=1, columnspan=2)
		self.deleteButton.grid(row=7, column=3)

		self.addBookButton.grid(row=7, column=1)
		self.clearButton.grid(row=7, column=2)



	def searchForBook(self):
		self.titleEntry.configure(state="normal")
		self.authorEntry.configure(state="normal")
		self.ISBNEntry.configure(state="normal")
		self.descriptionEntry.configure(state="normal")
		print "Search!"
		print (self.searchBookEntry.get())
		bookName = self.searchBookEntry.get()
		bookName = bookName.replace(" ", "+")

		urlSearchToAppendTo = "https://www.worldcat.org/search?q=" + bookName


		bookSearchPage = urllib2.urlopen(urlSearchToAppendTo)

		soup = BeautifulSoup(bookSearchPage)
		a = soup.find(id="result-1")
		
		print urlSearchToAppendTo

		bookURL = "https://www.worldcat.org" + a['href']

		print bookURL

		book_page = urllib2.urlopen(bookURL)
		soup = BeautifulSoup(book_page)

		title = soup.find("h1", {"class": "title"})
		self.titleEntry.insert(END, title.text)

		author = soup.find("td", {"id": "bib-author-cell"})
		self.authorEntry.insert(END, author.text)

		isbn = soup.find("tr", {"id": "details-standardno"})
		self.ISBNEntry.insert(END, isbn.text.replace("ISBN:", ""))


		details = soup.find("div", {"id": "summary"})
		detailsToUse = details.getText().split(" --")
		self.descriptionEntry.insert(END, detailsToUse[0])

		self.titleEntry.configure(state="disabled")
		self.authorEntry.configure(state="disabled")
		self.ISBNEntry.configure(state="disabled")
		self.descriptionEntry.configure(state="disabled")


	def addToCompleted(self):
		print "Add to Completed!"
		title = ""
		author = ""
		title = self.titleEntry.get()
		author = self.authorEntry.get()

		f = open('readbooks.txt', 'a')
		fr = open('readbooks.txt', 'r')
		lineToWrite = (title + ", " + author + "\n")
		for line in fr:
			if lineToWrite == line:
				print "FOUND"
				f.close()
				return
		print "Not Found"
		f.write(lineToWrite.encode('utf8'))
		self.listBox.insert(END, lineToWrite)
		f.close()
		return
		
		
		

	def clearData(self):
		print "Clear Data!"
		self.titleEntry.configure(state="normal")
		self.authorEntry.configure(state="normal")
		self.ISBNEntry.configure(state="normal")
		self.descriptionEntry.configure(state="normal")
		self.searchBookEntry.delete(0, 'end')
		self.titleEntry.delete(0, 'end')
		self.authorEntry.delete(0, 'end')
		self.ISBNEntry.delete(0, 'end')
		self.descriptionEntry.delete('1.0', END)

		self.titleEntry.configure(state="disabled")
		self.authorEntry.configure(state="disabled")
		self.ISBNEntry.configure(state="disabled")
		self.descriptionEntry.configure(state="disabled")

	def deleteFromList(self):
		print "Delete From List!"
		itemSelected = self.listBox.curselection()
		

		fr = open('readbooks.txt', 'r+')
		d = fr.readlines()
		fr.seek(0)
		lineToSearch = self.listBox.get(itemSelected[0])
		self.listBox.delete(itemSelected)
		for line in d:
			if lineToSearch != line.decode('utf-8'):
				print "FOUND"
				fr.write(line)
		fr.truncate()
		fr.close()


	
	

	



root = Tk()

app = App(root)
root.mainloop()

root.destroy()