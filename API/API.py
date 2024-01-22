# Using the import and from functions below for the process.
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from urllib import request
import json
import sqlite3
import os
# Using the class function below and naming  it my class as   MyCocktailAPI.
class MyCocktailAPI:# This is the BASE_URL link below for my api
    BASE_URL = "https://www.thecocktaildb.com/api/json/v1/1"

    @classmethod
    def search_cocktail(cls, mycocktail_name):
        #Using the try function below.
        try:
            myurl = f"{cls.BASE_URL}/search.php?s={mycocktail_name}"
            #Using the with function below.
            with request.urlopen(myurl) as response:
                mydata = json.loads(response.read().decode())
                #Using the return and else function below.
                return mydata['drinks'][0] if mydata['drinks'] else None
        except Exception as e:
            return None
# Using the class function below and naming it  as a class of MyCocktailAPI.
class MyDatabase:
    #Using the def function below.
    def __init__(myself):
        myself.conn = sqlite3.connect("cocktails.db")
        myself.cursor = myself.conn.cursor()
        myself.create_table()
    #Using the def function below.
    def create_table(myself):
        myself.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cocktails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                category TEXT,
                instructions TEXT,
                image_url TEXT
            )
        ''')
        myself.conn.commit()
    #Using the def function below.
    def insert_cocktail(myself, myname, mycategory, myinstructions, myimage_url):
        myself.cursor.execute('''
            INSERT INTO cocktails (name, category, instructions, image_url)
            VALUES (?, ?, ?, ?)
        ''', (myname, mycategory, myinstructions, myimage_url))
        myself.conn.commit()
# Using the class function below and naming it  as a class of MyAdvancedCocktailApp.
class MyAdvancedCocktailApp(tk.Tk):
    def __init__(myself):
        super().__init__()
        myself.title("TheCocktailDB Explorer")
        myself.geometry("800x600")  # Set your desired window size

        # Now below I am setting background color for the entire page as maroon
        myself.configure(bg="maroon")

        # Now below I am creating the header for my api.
        myheader_label = tk.Label(myself, text="TheCocktailDB Explorer", font=('Arial', 20, 'bold'), bg="maroon", fg="white")
        myheader_label.place(relx=0.5, rely=0.05, anchor="n")

        # # Now below I am creating the welcome information for  my api page.
        mywelcome_info = ("Welcome to TheCocktailDB API\n")
        mywelcome_label = tk.Label(myself, text=mywelcome_info, font=('Arial', 12), bg="maroon", fg="white", justify="center", padx=10, pady=10)
        mywelcome_label.place(relx=0.5, rely=0.1, anchor="n")

        #  Now below I am using a code to create the mainframe for my api.
        myself.main_frame = tk.Frame(myself, bg="maroon", bd=5)  # We can change its background color from here.
        myself.main_frame.place(relx=0.5, rely=0.15, relwidth=0.75, relheight=0.6, anchor="n")

        # Creating  widgets for my parts below.
        myself.label = tk.Label(myself.main_frame, text="Enter Cocktail Name:", font=('Arial', 14, 'bold'), bg="maroon", fg="white")
        myself.label.pack(pady=10)
        # Creating a button.
        myself.upload_button = tk.Button(myself.main_frame, text="Upload Image", command=myself.upload_image, font=('Arial', 12, 'bold'), bg="white", fg="black")
        myself.upload_button.pack(pady=10)
        # Creating the entry.
        myself.entry = tk.Entry(myself.main_frame, font=('Arial', 12))
        myself.entry.pack(pady=10)
        # Creating a button for search.
        myself.search_button = tk.Button(myself.main_frame, text="Search", command=myself.search_cocktail, font=('Arial', 12, 'bold'), bg="white", fg="black")
        myself.search_button.pack(pady=10)
        # Creating a result text box here.
        myself.result_text = tk.Text(myself.main_frame, height=8, width=50, font=('Arial', 12), bg="white", wrap=tk.WORD)
        myself.result_text.pack(pady=20)

        myself.cocktail_image_label = tk.Label(myself.main_frame, bg="white")
        myself.cocktail_image_label.pack(pady=20)

        # Creating a  variable to store the uploaded image path from folder.
        myself.uploaded_image_path = None

        #  The list of the  image paths are mentioned here.
        myself.image_paths = [
            "C:\\Users\\Ibrar\\OneDrive\\Desktop\\API\\apple.jpg",
            "C:\\Users\\Ibrar\\OneDrive\\Desktop\\API\\lemon.jpg",
            "C:\\Users\\Ibrar\\OneDrive\\Desktop\\API\\Bluebird.jpg",
            # Add more paths if needed here.
        ]

        # Now I am goingg to  initialize the Database here.
        myself.database = MyDatabase()

# Using the def function below.
    def upload_image(myself):
        myfile_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if myfile_path:
            myself.uploaded_image_path = myfile_path
            messagebox.showinfo("Upload Success", "Image path set successfully!")
# Using the def function below.
    def go_home(myself):
        # Now I am going to reset uploaded image path and clear the entry field for it.
        myself.uploaded_image_path = None
        myself.entry.delete(0, tk.END)
# Using the def function below.
    def search_cocktail(myself):
        mycocktail_name = myself.entry.get()
        #Using the if function below.
        if not mycocktail_name:
            #Using the return function below.
            messagebox.showinfo("Error", "Please enter a cocktail name.")
            return

        mycocktail_data = MyCocktailAPI.search_cocktail(mycocktail_name)
        #Using the if function below.
        if mycocktail_data:
            myself.display_cocktail_info(mycocktail_data)
            myself.display_cocktail_image(mycocktail_data['strDrinkThumb'])
            myself.save_cocktail_to_database(mycocktail_data)
            #Using the else function below.
        else:
            messagebox.showinfo("Error", "Cocktail not found.")
        # Using the def function below.
    def save_cocktail_to_database(myself, mycocktail_data):
        myname = mycocktail_data['strDrink']
        mycategory = mycocktail_data['strCategory']
        myinstructions = mycocktail_data['strInstructions']
        myimage_url = mycocktail_data['strDrinkThumb']

        # Now at first download and save the image locally.
        mylocal_image_path = f"images/{myname}.jpg"  
        request.urlretrieve(myimage_url, mylocal_image_path)

        # Now insert cocktail into the database with the local image path.
        myself.database.insert_cocktail(myname, mycategory, myinstructions, mylocal_image_path)

    def display_cocktail_info(myself, mycocktail_data):
        myinfo = f"Name: {mycocktail_data['strDrink']}\n"
        myinfo += f"Category: {mycocktail_data['strCategory']}\n"
        myinfo += f"Instructions: {mycocktail_data['strInstructions']}\n"

        # Now here we are requestion to display information about the cocktails.
        myself.result_text.delete(1.0, tk.END)
        myself.result_text.insert(tk.END, myinfo)
        # Now we are using the def function below.
    def display_cocktail_image(myself, image_url):
        if myself.uploaded_image_path:
            # Also kindly note if an image is uploaded, use the uploaded image for the solution.
            myimage_path = myself.uploaded_image_path
            #Using the else function below.
        else:
            # Other wise we can use the image URL from the API
            myimage_path = image_url

        image = myself.load_image(myimage_path)
        if image:
            myself.cocktail_image_label.configure(image=image)
            myself.cocktail_image_label.image = image  # Keep a reference to prevent garbage collection
# Using the def function below.
    def myload_image(myself, myimage_path):
        # Using the try function below.
        try:
            myimg = Image.open(myimage_path)
            myimg = myimg.resize((myself.winfo_screenwidth(), myself.winfo_screenheight()), Image.ANTIALIAS)
            return ImageTk.PhotoImage(myimg)
        except Exception as e:
            return None
# Now using the if function below.
if __name__ == "__main__":
    # Kindly note also  the "images" folder exists in my main folder.
    os.makedirs("images", exist_ok=True)
    myapp = MyAdvancedCocktailApp()
    myapp.mainloop()# Now start the mainloop.
