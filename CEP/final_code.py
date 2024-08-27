import tkinter as tk
from tkinter import messagebox, PhotoImage, Toplevel, Label, Button
from time import ctime
from abc import ABC,abstractmethod
# creates frames for Login and signup forms and displays them
class LoginSignup(ABC):  # here we used abstract class
    def __init__(self, root):
        self.root = root
        self.root.title("Login/Signup Window")
        self.root.geometry("400x400")
        
        self.login_frame = tk.Frame(self.root)
        self.signup_frame = tk.Frame(self.root)
        self.set_log_frame()
        self.set_sign_frame()
        self.login_frame.pack(pady=20)
        
    def set_log_frame(self):
        login_label = tk.Label(self.login_frame, text="Login", font=("Helvetica", 40))
        login_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(self.login_frame, text="Username:", font=30).grid(row=1, column=0)
        self.login_username = tk.Entry(self.login_frame)
        self.login_username.grid(row=1, column=1)
        
        tk.Label(self.login_frame, text="Password:", font=30).grid(row=2, column=0)
        self.login_password = tk.Entry(self.login_frame)
        self.login_password.grid(row=2, column=1)
        
        login_button = tk.Button(self.login_frame, text="Login", command=self.login, width=20, height=2)
        login_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.signup_button = tk.Button(self.root, text="Don't have an account? Sign up here", command=self.show_signup, width=30, height=3)
        self.signup_button.pack(side='bottom')

    def set_sign_frame(self):
        signup_label = tk.Label(self.signup_frame, text="Signup", font=("Helvetica", 40))
        signup_label.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.signup_frame, text="Full Name:", font=30).grid(row=1, column=0)
        self.signup_name = tk.Entry(self.signup_frame)
        self.signup_name.grid(row=1, column=1)

        tk.Label(self.signup_frame, text="Username:", font=30).grid(row=2, column=0)
        self.signup_username = tk.Entry(self.signup_frame)
        self.signup_username.grid(row=2, column=1)
        
        tk.Label(self.signup_frame, text="Password:", font=30).grid(row=3, column=0)
        self.signup_password = tk.Entry(self.signup_frame)
        self.signup_password.grid(row=3, column=1)

        tk.Label(self.signup_frame, text="Confirm Password:", font=30).grid(row=4, column=0)
        self.signup_password2 = tk.Entry(self.signup_frame)
        self.signup_password2.grid(row=4, column=1)
        
        signup_button = tk.Button(self.signup_frame, text="Signup", command=self.create_account, width=20, height=2)
        signup_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.log_button = tk.Button(self.root, text="Already have an account? Login here", command=self.show_login, width=30, height=3)
        self.log_button.pack(side='bottom')

    @abstractmethod
    def login(self):
        pass
    
    @abstractmethod
    def create_account(self):
        pass
        
    def show_signup(self):
        self.login_frame.pack_forget()
        self.signup_frame.pack(pady=20)
        
    def show_login(self):
        self.signup_frame.pack_forget()
        self.login_frame.pack(pady=20)


# a class that takes inputs from loginSignup class and creates an acc or logs in as required
class Customer(LoginSignup):   #here we used inheritence
    def __init__(self,login_signup_window):
        super().__init__(login_signup_window)
        self.name = None
        self.username = None
        self.password = None
        self.password2 = None

    def create_account(self):
        self.name = self.signup_name.get()
        self.username = self.signup_username.get()
        self.password = self.signup_password.get()
        self.password2 = self.signup_password2.get()
        Customer.username=self.signup_username.get()
        if self.password != self.password2:
            messagebox.showerror("Error", "Passwords do not match, please try again.")
            return
        elif len(self.password) <= 8:
            messagebox.showerror("Error", "Password too short, please try again.")
            return

        username_exists = False
        with open('datas.txt', 'r') as f:
            for line in f:
                user = eval(line.strip())
                if self.username in user:
                    messagebox.showerror("Error", "Username already exists, please choose a different one.")
                    username_exists = True
                    break
        f.close()

        if not username_exists:
            with open('datas.txt', 'a') as f:
                f.write(str({self.username: self.password}) + "\n")
            f.close()
            messagebox.showinfo("Success", "Account creation successful")
            OptionWindow(self.root)  

    def login(self):
        self.username = self.login_username.get()
        self.password = self.login_password.get()
        Customer.username= self.login_username.get()

        login_successful = False
        try:
            with open('datas.txt', 'r') as f:
                for line in f:
                    user = eval(line.strip())
                    if self.username in user and user[self.username] == self.password:
                        messagebox.showinfo("info", "Login successful")
                        login_successful = True
                        OptionWindow(self.root)  
                        break
        except FileNotFoundError:    #HERE WE USED EXCEPTION
            messagebox.showerror("Error", "No accounts found. Please create an account first.")

        if not login_successful:
            messagebox.showerror("Error", "Invalid username or password")

class ShoppingHistory(Customer):
    def __init__(self):
        self.username = Customer.username
        self.filename = "shopping_history.txt"
        self.cart = []  # List to hold books before recording the purchase
        self.order_time = ctime()

    def record_purchase(self,books):
        for book in books: 
            self.cart_item = [self.order_time, book['Book'], book['Price']]
            self.cart_d = {self.username: self.cart_item}
            with open(self.filename, 'a+') as f:
                f.write(str(self.cart_d) + '\n')
        self.cart.clear()

    def display_history(self):
        history_text = str(self)
        if not history_text.strip():
            history_text = "No orders found for this user"
        return history_text

    def view_history(self):
        history_window = tk.Tk()
        history_window.title("Shopping History")

        history_text = self.display_history()

        history_label1 = tk.Label(history_window, text='YOUR HISTORY', font=("Arial", 12, "bold"))
        history_label1.pack(padx=10, pady=10)

        history_label2 = tk.Label(history_window, text=history_text, justify='left', font=("Arial", 8))
        history_label2.pack(padx=10, pady=10)

    def __str__(self):   #here we used operator overloading
        history_text = ""
        try:
            with open(self.filename, 'r') as history_file:
                history_content = history_file.read()
                count = 1
                
                for line in history_content.split('\n'):
                    if line:
                        try:
                            history_data = eval(line.strip())
                            if self.username in history_data:
                                order_details = history_data[self.username]
                                history_text += f'Order No. {count}\n'
                                history_text += f'Order Date: {order_details[0]}\t'
                                history_text += f'Product: {order_details[1]}\t'
                                history_text += f'Price: {order_details[2]}\n\n'
                                count += 1
                        except SyntaxError:
                            print(f"Error: Invalid data format in line: {line.strip()}")
        except FileNotFoundError:
            history_text = "No history file found."
        
        return history_text        
    

#a class which takes all the inputs from user for removing or adding to cart, and checking out 
class Cart(Customer):
    def __init__(self):
        self.username=Customer.username
        self.books = []
        self.cart_window = None
        self.prices = {
            'Good Girls Guide to do a Murder(Triology Available)': 1999,
            'Six of Crows(Duology Available)': 1545,
            'Five Survive': 985,
            'The Kite Runner': 999,
            'A Thousand Splendid Suns': 985,
            'The Inheritance Games(Triology available)': 2000,
            'The book thief': 785,
            'They Both die at the End': 750,
            'The alchemist': 690,
            'The Night Circus': 987,
            'Without Merit': 787,
            'Tuesdays with Morrie': 900,
            'Little Women': 1097,
            'Verity': 765
        }
        self.history = ShoppingHistory()

    def add_book(self, book):
        for item in self.books:
            if item['Book'] == book:
                messagebox.showinfo(title='ERROR', message="Cannot add book more than once")
                return
        self.books.append({'Book': book, 'Price': self.get_price(book)})
    def view_cart(self):
        if not self.books:
            messagebox.showinfo(title='ERROR', message="There's nothing to show here\nCART IS EMPTY")
        else:
            if self.cart_window is not None:
                self.cart_window.destroy()
            
            self.cart_window = Toplevel()
            self.cart_window.title("Cart")
            l = Label(self.cart_window, text='CART CONTENTS', font='bold')
            l.grid(row=0, column=0, columnspan=2)

            self.row = 1
            for item in self.books:
                item_name = Label(self.cart_window, text=f"Book: {item['Book']}, Price: {item['Price']}")
                item_name.grid(row=self.row, column=0, padx=10, pady=5)
                remove_button = Button(self.cart_window, text="Remove", command=lambda item=item: self.remove_book(item))
                remove_button.grid(row=self.row, column=1, padx=10, pady=5)
                self.row += 1

            checkout_button = Button(self.cart_window, text="Checkout", command=self.checkout, width=20, height=2, bg="#4CAF50", fg="white")
            checkout_button.grid(row=self.row, column=0, columnspan=2, pady=20)

    def remove_book(self, item):
        self.books.remove(item)
        self.cart_window.destroy()
        self.view_cart()

    def get_price(self, book):
        return self.prices.get(book, self.prices[book])
    

    def checkout(self):
        self.row += 1
        tk.Label(self.cart_window, text="Enter contact no.:", font=30).grid(row=self.row, column=0)
        self.contact_info = tk.Entry(self.cart_window)
        self.contact_info.grid(row=self.row, column=1)
        self.row += 1
        tk.Label(self.cart_window, text="Enter address:", font=30).grid(row=self.row, column=0)
        self.address = tk.Entry(self.cart_window)
        self.address.grid(row=self.row, column=1)
        self.row += 1
        self.amount = sum(item['Price'] for item in self.books)
        label = tk.Label(self.cart_window, text=f'Your total bill is PKR {self.amount}')
        label.grid(row=self.row, column=0, columnspan=2, pady=10)
        self.row += 1
        confirm = tk.Button(self.cart_window, text='Confirm Purchase', command=self.confirm_purchase)
        confirm.grid(row=self.row, column=0, columnspan=2, pady=10)

    def confirm_purchase(self):
        user_info1=self.contact_info.get() 
        user_info2=self.address.get()
        if user_info1.strip() == "" and  user_info2.strip() == "":
            messagebox.showerror("Error", "Please enter required details!")
        else:
            self.history.record_purchase(self.books) 
            messagebox.showinfo("Purchase Confirmed", "YOUR PURCHASE HAS BEEN CONFIRMED\n\nTHANK YOU FOR SHOPPING!! ENJOY :)")
            self.books = [] 
            self.cart_window.destroy()  
            OptionWindow.menu_window.destroy()

# Function to load image or return a placeholder used in menu
def load_image(path):
    try:
        return PhotoImage(file=path)
    except Exception:
        return None

# creating a Window to display options
class OptionWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Tk()
        self.window.title("Options")

        self.label = Label(self.window, text="What would you like to do next?")
        self.label.pack(pady=10)

        self.history_button = Button(self.window, text="View History", command=self.call_history)
        self.history_button.pack(pady=5)

        self.menu_button = Button(self.window, text="Go to Menu", command=self.go_to_menu)
        self.menu_button.pack(pady=5)
    
    def call_history(self):
        self.window.destroy()
        self.parent.destroy()
        h=ShoppingHistory()    #HERE WE USED COMPOSITION
        h.view_history()
        

    def go_to_menu(self):
        self.window.destroy()
        self.parent.destroy()
        menu_window = tk.Tk()
        menu_window.title("OUR MENU")
        OptionWindow.menu_window=menu_window
        cart = Cart()

        photo1 = load_image('gggtm.png')
        l1 = Label(menu_window, image=photo1)
        l1.grid(row=0, column=0, padx=10, pady=(10, 5))
        b = Button(menu_window, text='ADD', command=lambda: cart.add_book('Good Girls Guide to do a Murder(Triology Available)'), width=15, height=2)
        b.grid(row=1, column=0, padx=10, pady=(5, 10))
        l2 = Label(menu_window, text='Good Girls Guide to do a Murder(Triology Available)')
        l2.grid(row=2, column=0, padx=10, pady=5)
        l3 = Label(menu_window, text='PKR 1999')
        l3.grid(row=3, column=0, padx=10, pady=(0, 10))

        photo2 = load_image('6crows.png')
        m = Label(menu_window, image=photo2)
        m.grid(row=0, column=1, padx=10, pady=(10, 5))
        b1 = Button(menu_window, text='ADD', command=lambda: cart.add_book('Six of Crows(Duology Available)'), width=15, height=2)
        b1.grid(row=1, column=1, padx=10, pady=(5, 10))
        m1 = Label(menu_window, text='Six of Crows(Duology Available)')
        m1.grid(row=2, column=1, padx=10, pady=5)
        m2 = Label(menu_window, text='PKR 1545')
        m2.grid(row=3, column=1, padx=10, pady=(0, 10))

        photo3 = load_image('5survive.png')
        n = Label(menu_window, image=photo3)
        n.grid(row=0, column=2, padx=10, pady=(10, 5))
        b2 = Button(menu_window, text='ADD', command=lambda: cart.add_book('Five Survive'), width=15, height=2)
        b2.grid(row=1, column=2, padx=10, pady=(5, 10))
        n1 = Label(menu_window, text='Five Survive')
        n1.grid(row=2, column=2, padx=10, pady=5)
        n2 = Label(menu_window, text='PKR 985')
        n2.grid(row=3, column=2, padx=10, pady=(0, 10))

        photo4 = load_image('kiter.png')
        p = Label(menu_window, image=photo4)
        p.grid(row=0, column=3, padx=10, pady=(10, 5))
        b3 = Button(menu_window, text='ADD', command=lambda: cart.add_book('The Kite Runner'), width=15, height=2)
        b3.grid(row=1, column=3, padx=10, pady=(5, 10))
        p1 = Label(menu_window, text='The Kite Runner')
        p1.grid(row=2, column=3, padx=10, pady=5)
        p2 = Label(menu_window, text='PKR 999')
        p2.grid(row=3, column=3, padx=10, pady=(0, 10))

        photo5 = load_image('atssuns.png')
        v = Label(menu_window, image=photo5)
        v.grid(row=0, column=4, padx=10, pady=(10, 5))
        b4 = Button(menu_window, text='ADD', command=lambda: cart.add_book('A Thousand Splendid Suns'), width=15, height=2)
        b4.grid(row=1, column=4, padx=10, pady=(5, 10))
        v1 = Label(menu_window, text='A Thousand Splendid Suns')
        v1.grid(row=2, column=4, padx=10, pady=5)
        v2 = Label(menu_window, text='PKR 985')
        v2.grid(row=3, column=4, padx=10, pady=(0, 10))

        photo6 = load_image('inhgame.png')
        h = Label(menu_window, image=photo6)
        h.grid(row=0, column=5, padx=10, pady=(10, 5))
        b5 = Button(menu_window, text='ADD', command=lambda: cart.add_book('The Inheritance Games(Triology available)'), width=15, height=2)
        b5.grid(row=1, column=5, padx=10, pady=(5, 10))
        h1 = Label(menu_window, text='The Inheritance Games(Triology available)')
        h1.grid(row=2, column=5, padx=10, pady=5)
        h2 = Label(menu_window, text='PKR 2000')
        h2.grid(row=3, column=5, padx=10, pady=(0, 10))

        photo7 = load_image('thebookthief.png')
        k = Label(menu_window, image=photo7)
        k.grid(row=0, column=6, padx=10, pady=(10, 5))
        b5 = Button(menu_window, text='ADD', command=lambda: cart.add_book('The book thief'), width=15, height=2)
        b5.grid(row=1, column=6, padx=10, pady=(5, 10))
        k1 = Label(menu_window, text='The book thief')
        k1.grid(row=2, column=6, padx=10, pady=5)
        k2 = Label(menu_window, text='PKR 785')
        k2.grid(row=3, column=6, padx=10, pady=(0, 10))

        photo8 = load_image('tbdate.png')
        i = Label(menu_window, image=photo8)
        i.grid(row=4, column=0, padx=10, pady=(10, 5))
        b6 = Button(menu_window, text='ADD', command=lambda: cart.add_book('They Both die at the End'), width=15, height=2)
        b6.grid(row=5, column=0, padx=10, pady=(5, 10))
        i1 = Label(menu_window, text='They Both die at the End')
        i1.grid(row=6, column=0, padx=10, pady=5)
        i2 = Label(menu_window, text='PKR 750')
        i2.grid(row=7, column=0, padx=10, pady=(0, 10))

        photo9=load_image('alchem.png')
        t=Label(menu_window,image=photo9)
        t.grid(row=4, column=1, padx=10, pady=(10,5))
        b7=Button(menu_window,text='ADD',command=lambda: cart.add_book('The alchemist'), width=15,height=2)
        b7.grid(row=5, column=1, padx=10, pady=(5,10))
        t1=Label(menu_window,text='The Alchemist')
        t1.grid(row=6, column=1, padx=10, pady=5)
        t2=Label(menu_window,text='PKR 690')
        t2.grid(row=7, column=1, padx=10, pady=(0,10))

        photo10=load_image('nightc.png')
        j=Label(menu_window,image=photo10)
        j.grid(row=4, column=2, padx=10, pady=(10,5))
        b8=Button(menu_window,text='ADD',command=lambda: cart.add_book('The Night Cirus'), width=15,height=2)
        b8.grid(row=5, column=2, padx=10, pady=(5,10))
        j1=Label(menu_window,text='The Night Circus')
        j1.grid(row=6, column=2, padx=10, pady=5)
        j2=Label(menu_window,text='PKR 987')
        j2.grid(row=7, column=2, padx=10, pady=(0,10))

        photo11=load_image('wmerit.png')
        f=Label(menu_window,image=photo11)
        f.grid(row=4, column=3, padx=10, pady=(10,5))
        b9=Button(menu_window,text='ADD',command=lambda: cart.add_book('without merit'), width=15,height=2)
        b9.grid(row=5, column=3, padx=10, pady=(5,10))
        f1=Label(menu_window,text='Without Merit')
        f1.grid(row=6, column=3, padx=10, pady=5)
        f2=Label(menu_window,text='PKR 787')
        f2.grid(row=7, column=3, padx=10, pady=(0,10))

        photo12=load_image('tuesdays.png')
        z=Label(menu_window,image=photo12)
        z.grid(row=4, column=4, padx=10, pady=(10,5))
        b10=Button(menu_window,text='ADD',command=lambda: cart.add_book('Tuesdays with Morrie'), width=15,height=2)
        b10.grid(row=5, column=4, padx=10, pady=(5,10))
        z1=Label(menu_window,text='Tuesdays with Morrie')
        z1.grid(row=6, column=4, padx=10, pady=5)
        z2=Label(menu_window,text='PKR 900')
        z2.grid(row=7, column=4, padx=10, pady=(0,10))

        photo13=load_image('littlewm.png')
        z=Label(menu_window,image=photo13)
        z.grid(row=4, column=5, padx=10, pady=(10,5))
        b10=Button(menu_window,text='ADD',command=lambda: cart.add_book('Little Women'), width=15,height=2)
        b10.grid(row=5, column=5, padx=10, pady=(5,10))
        z1=Label(menu_window,text='Little Women')
        z1.grid(row=6, column=5, padx=10, pady=5)
        z2=Label(menu_window,text='PKR 1097')
        z2.grid(row=7, column=5, padx=10, pady=(0,10))

        photo14=load_image('verity.png')
        z=Label(menu_window,image=photo14)
        z.grid(row=4, column=6, padx=10, pady=(10,5))
        b10=Button(menu_window,text='ADD',command=lambda: cart.add_book('verity'), width=15,height=2)
        b10.grid(row=5, column=6, padx=10, pady=(5,10))
        z1=Label(menu_window,text='Verity')
        z1.grid(row=6, column=6, padx=10, pady=5)
        z2=Label(menu_window,text='PKR 765')
        z2.grid(row=7, column=6, padx=10, pady=(0,10))

        view_cart_button = Button(menu_window, text='View Cart', command=cart.view_cart, width=15, height=2)
        view_cart_button.grid(row=8, column=0, padx=10, pady=(10, 10))
        menu_window.mainloop()
      

# Create the main window for login/signup page 
def on_click():
    root.destroy()
    login_signup_window = tk.Tk()
    log_sign = Customer(login_signup_window)
    login_signup_window.mainloop()

root = tk.Tk()
root.title("Bookstore Welcome Page")
root.geometry("600x400")
root.configure(bg="#E5E5E5")

# to Display the image if it is loaded
image_path = "logo.png"
logo = load_image(image_path)
try:
    logo_label = tk.Label(root, image=logo, bg="#e5e5e5")
except:
    logo_label = tk.Label(root, text="[Bookstore Logo]", font=("Helvetica", 14, "italic"), bg="#f0f8ff", fg="#5a7d9a")

logo_label.pack(pady=10)

# a welcome label 
welcome_label = tk.Label(
    root,
    text="WELCOME TO THE LITTLE LANTERN LIBRARY!",
    font=("Helvetica", 22, "bold"),
    fg="#365f6b",
    bg="#e5e5e5",
)
welcome_label.pack()

#a description label about our program
description_label = tk.Label(
    root,
    text="Discover a world of books with us. Please login or signup to continue.",
    font=("Helvetica", 14),
    fg="#5a7d9a",
    bg="#e5e5e5",
    wraplength=400,
    justify="center",
)
description_label.pack(pady=20)

# a button to go to the sign up login window
login_signup_button = tk.Button(
    root,
    text="Login OR Sign Up",
    command=on_click,
    font=("Helvetica", 16, "bold"),
    bg="#365f6b",
    fg="white",
    width=20,
    height=2,
)
login_signup_button.pack(pady=40)

root.mainloop()

