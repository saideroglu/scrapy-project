from tkinter import *
from tkinter import ttk
import csv
import webbrowser

root = Tk()
root.title('WebScraper')
root.geometry("1100x600")

#Update the treeview with striped rows
def update(search_results):
    my_tree.delete(*my_tree.get_children())

    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    count = 0
    for record in search_results:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text="", values=(record.seller, record.name, record.price, record.url), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text="", values=(record.seller, record.name, record.price, record.url), tags=('oddrow',))
        count += 1

#Create function to search the treeview by name
def search(event):
    search_term = my_entry.get()
    search_results = []
    for record in data:
        if search_term.lower() in record.name.lower():
            search_results.append(record)
    update(search_results)

#Sort the table by the column specified
reverse = False
def sort_table(event, col):
    search_term = my_entry.get()
    search_results = []

    for record in data:
        if search_term.lower() in record.name.lower():
            search_results.append(record)

    #toggle the reverse flag
    global reverse
    reverse = not reverse

    search_results.sort(key=lambda x: getattr(x, col), reverse=reverse)
    update(search_results)

#Go to link
def go_link():
	webbrowser.open_new(url_box.get())

#Clear URL
def clear():
	url_box.delete(0, END)

#Select Record
def select_record():
	url_box.delete(0, END)
	selected = my_tree.focus()
	values = my_tree.item(selected, 'values')
	url_box.insert(0, values[3])

#Create Binding Click function
def clicker(e):
	select_record()

#Read CSV
def read_csv(file_name, data):
    with open(file_name, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(f)
        for row in reader:
            data.append(my_class(row[0], row[1], row[2], row[3]))

#Create a label and an entry box
my_label = Label(root, text="Search by Name")
my_label.pack(pady=10) 
my_entry = Entry(root, width=50)
my_entry.pack()

#Add some style
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", 
	background="#D3D3D3",
	foreground="black",
	rowheight=35,
	fieldbackground="#D3D3D3"
	)
style.map('Treeview', 
	background=[('selected', 'darkblue')])
style.configure("TButton", 
    background="#D3D3D3",
    foreground="#333333")

#Create treeview frame
tree_frame = Frame(root)
tree_frame.pack(pady=30)

#Treeview scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

#Create treeview
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()

#Configure the scrollbar
tree_scroll.config(command=my_tree.yview)

#Define and format our columns
my_tree['columns'] = ("Seller", "Name", "Price","URL")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Seller", anchor=W, width=200)
my_tree.column("Name", anchor=W, width=600)
my_tree.column("Price", anchor=W, width=200)
my_tree.column("URL", anchor=W, width=0, stretch=NO)

#Create headings 
my_tree.heading("Seller", text="Seller", anchor=W, command=lambda: sort_table(None, 'seller'))
my_tree.heading("Name", text="Name", anchor=W, command=lambda: sort_table(None, 'name'))
my_tree.heading("Price", text="Price", anchor=W, command=lambda: sort_table(None, 'price'))
#my_tree.heading("URL", text="URL", anchor=W)

#Create a class
class my_class:
    def __init__(self, seller, name, price, url):
        self.seller = seller
        self.name = name
        self.price = int(price)
        self.url = url

#Add data
data = []
read_csv("scraper\\mediamarkt.csv", data)
read_csv("scraper\\teknosa.csv", data)
read_csv("scraper\\vatan.csv", data)

update(data)

#Frame for URL
add_frame = Frame(root)
add_frame.pack()

#Labels, entry boxes and buttons
ll = Label(add_frame, text="URL:")
ll.grid(row=1, column=1)
url_box = Entry(add_frame, width=80)
url_box.grid(row=1, column=3)
link_button = ttk.Button(add_frame, text="Go to Link", width=10, command=go_link)
link_button.grid(row=1, column=5, padx=10)
clear_button = ttk.Button(add_frame, text="Clear", width=10, command=clear)
clear_button.grid(row=1, column=6)

# Bindings
my_tree.bind("<ButtonRelease-1>", clicker)
my_entry.bind("<KeyRelease>", search)

root.mainloop()