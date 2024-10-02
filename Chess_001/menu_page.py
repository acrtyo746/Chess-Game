import tkinter as tk
from PIL import Image, ImageTk  # Import Pillow library for image handling
import Board  # Import your chess game file
import webbrowser

def start_game():
    root.destroy()  # Close the Tkinter window
    try:
        Board.main1()  # Initialize Game window
        Board.main2()  # Call the function that starts your game
    except Exception as e:
        print(f"Error starting the game: {e}")

def show_about():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    tk.Label(about_window, text="Chess Game\nVersion 1.0\nDeveloped by Ajay Chauhan").pack(pady=20)

def show_help():
    help_window = tk.Toplevel(root)
    help_window.title("Help")
    
    # Create a Text widget with a hyperlink
    text_widget = tk.Text(help_window, bg='white', fg='black', borderwidth=0, height=10, width=50)
    text_widget.pack(pady=20)

    # Insert text and hyperlink
    text_widget.insert(tk.END, "Move pieces by clicking and dragging.\nCheckmate the opponent to win!\n\nFor more details visit this site below:\n")
    text_widget.insert(tk.END, "https://chess.com", 'link')

    # Configure the tag 'link'
    text_widget.tag_configure('link', foreground='blue', underline=True)
    
    # Bind the click event to the link
    text_widget.tag_bind('link', '<Button-1>', lambda e: webbrowser.open("https://chess.com"))

    # Make the Text widget read-only
    text_widget.config(state=tk.DISABLED)

def load_resized_image(image_path, size=(300, 300)):
    # Open an image file and resize it
    with Image.open(image_path) as img:
        img_resized = img.resize(size)
        return ImageTk.PhotoImage(img_resized)

# Initialize the main window
root = tk.Tk()
root.title("Chess")
root.geometry("500x500")
root.config(background='#191618')

# Load and resize image
bg_image = load_resized_image("/home/goku/Desktop/ROUGH/python/Chess_001/images/logo.jpeg")

bg_label = tk.Label(root, image=bg_image, bg='#000000')
bg_label.pack(anchor="center", pady=(35, 0))

# Creating a menubar
menubar = tk.Menu(root)

# Adding 'Menu' to the menubar
menu = tk.Menu(menubar, fg='Yellow', bg='White', tearoff=0)
menu.add_command(label="About", command=show_about)
menu.add_command(label="Help", command=show_help)

menubar.add_cascade(label="Menu", menu=menu)

# Display the menubar
root.config(menu=menubar)

# Start Button
start_button = tk.Button(root, text="Play", bg='#000000',
                         activebackground='white', command=start_game,
                         font=("#000000", 16))
start_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

root.mainloop()
