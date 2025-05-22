import tkinter as tk
import customtkinter as ctk
import random
from PIL import Image
from customtkinter import CTkImage
import requests
import csv
import unicodedata

# SYSTEM  -----------------------------------------------------------------

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
root = ctk.CTk(fg_color='#212121')  # creates window
root.title("passNerd")  # window title
root.resizable(False, False)
root.iconbitmap(r'')

clipboard_big = CTkImage(Image.open(r'icons/copy_clipboard.png'), size=(26, 26))
plus_big = CTkImage(Image.open(r'icons/plus_icon.png'), size=(25, 25))
checkmark = CTkImage(Image.open(r'icons/checkmark_icon.png'), size=(26, 26))
a_to_z = CTkImage(Image.open(r'icons/a_to_z.png'), size=(20, 20))
z_to_a = CTkImage(Image.open(r'icons/z_to_a.png'), size=(20, 20))
plus_small = CTkImage(Image.open(r'icons/plus_icon.png'), size=(20, 20))
minus_big = CTkImage(Image.open(r'icons/minus_icon.png'), size=(20, 20))
hidden = CTkImage(Image.open(r'icons/hidden_icon.png'), size=(20, 20))
visible = CTkImage(Image.open(r'icons/visible_icon.png'), size=(20, 20))

# FRAMES  ------------------------------------------------------------------

# LEFT PANE
left_pane = ctk.CTkScrollableFrame(root,
                                   fg_color='#212121',
                                   height=450,
                                   width=200,  # normally 200
                                   label_text='Stored Passwords',
                                   label_font=('Calibri', 18, 'bold'),
                                   label_fg_color='#212121',
                                   corner_radius=0)
left_pane.grid(row=0, column=0, sticky='nw')

# MAINFRAME
main_frame = ctk.CTkFrame(root, bg_color='transparent')
main_frame.grid(row=0, column=1, padx=40, pady=80)

# TOP FRAME
top_level = ctk.CTkFrame(main_frame,
                         width=0,
                         bg_color='transparent')
top_level.grid(row=0, column=1, sticky='n')

# CHAR LENGTH LABEL
char_length_label = ctk.CTkLabel(main_frame,
                                 width=0,
                                 padx=0,
                                 pady=10,
                                 anchor='nw',
                                 text='Character Length',
                                 font=('Calibri', 18),
                                 bg_color='transparent')
char_length_label.grid(row=1, column=1, sticky='w')

# CHAR NUMBER LABEL
slider_var = ctk.IntVar(value=14)
char_number_label = ctk.CTkLabel(char_length_label,
                                 padx=2,
                                 pady=10,
                                 anchor='ne',
                                 textvariable=slider_var,
                                 font=('Calibri', 18),
                                 bg_color='transparent')
char_number_label.grid(row=0, column=0, sticky='e')

# CHECKMARK LABEL
include_label = ctk.CTkLabel(main_frame,
                             height=0,
                             width=0,
                             padx=0,
                             pady=10,
                             anchor='nw',
                             text='Include',
                             font=('Calibri', 18),
                             fg_color='transparent',
                             bg_color='transparent')
include_label.grid(row=2, column=1, sticky='w')

# GEN BTN FRAME
generate_frame = ctk.CTkFrame(main_frame,
                              width=200,
                              fg_color='transparent')
generate_frame.grid(row=3, column=1, sticky='n')


# PASSWORD GENERATOR BACKEND --------------------------------------------------------------------


class PasswordGenerator:
    def __init__(self):
        self.password = ""
        self.include_lower = False
        self.include_upper = False
        self.include_numbers = False
        self.include_symbols = False
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                      'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                      'U', 'V', 'W', 'X', 'Y', 'Z']
        self.lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                      'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                      'u', 'v', 'w', 'x', 'y', 'z']
        self.symbols = ['~', '`', '!', '@', '#', '$', '%', '^', '&', '*',
                        '(', ')', '_', '-', '+', '=', '{', '[', ']', '}',
                        '|', ':', ';', '"', "'", '<', ',', '>', '.', '?',
                        '/']

    def create_password(self, length, include_lower, include_upper, include_numbers, include_symbols):
        # Clear past password generations
        self.password = ""

        # Calculate the number of characters needed for each character type

        num_characters_per_type = sum([include_numbers, include_upper, include_lower, include_symbols])
        if num_characters_per_type == 0:
            return print("Must check at least 1 box")
        characters_needed = length // num_characters_per_type

        # Shuffle the character lists
        random.shuffle(self.numbers)
        random.shuffle(self.upper)
        random.shuffle(self.lower)
        random.shuffle(self.symbols)

        # Add characters from each character type to the password
        for i in range(characters_needed):
            if include_numbers == 1:
                self.password += random.choice(self.numbers)
            if include_upper == 1:
                self.password += random.choice(self.upper)
            if include_lower == 1:
                self.password += random.choice(self.lower)
            if include_symbols == 1:
                self.password += random.choice(self.symbols)

        # Add any remaining characters to fulfill the requested password length
        remaining_length = length - len(self.password)
        if remaining_length > 0:
            counter_numbers = 0
            counter_upper = 0
            counter_lower = 0
            counter_symbols = 0
            while remaining_length > 0:
                if include_numbers == 1:
                    self.password += self.numbers[counter_numbers]
                    counter_numbers = (counter_numbers + 1) % len(self.numbers)
                    remaining_length -= 1
                if include_upper == 1 and remaining_length > 0:
                    self.password += self.upper[counter_upper]
                    counter_upper = (counter_upper + 1) % len(self.upper)
                    remaining_length -= 1
                if include_lower == 1 and remaining_length > 0:
                    self.password += self.lower[counter_lower]
                    counter_lower = (counter_lower + 1) % len(self.lower)
                    remaining_length -= 1
                if include_symbols == 1 and remaining_length > 0:
                    self.password += self.symbols[counter_symbols]
                    counter_symbols = (counter_symbols + 1) % len(self.symbols)
                    remaining_length -= 1

        # Shuffle the final password
        password_characters = list(self.password)
        random.shuffle(password_characters)
        self.password = ''.join(password_characters)


# SAVE PASSWORD BACKEND  -----------------------------------------------------------


class NewButton:
    def __init__(self):
        self.password_label = None
        self.website_label = None
        self.hidden = None
        self.website_name = None
        self.password = None
        self.count = 0
        self.visibility_button = None

        # Icon minis
        self.clipboard_mini = CTkImage(Image.open(r'icons/copy_clipboard.png'), size=(12, 12))
        self.minus_mini = CTkImage(Image.open(r'icons/minus_icon.png'), size=(12, 12))
        self.checkmark_mini = CTkImage(Image.open(r'icons/checkmark_icon.png'), size=(12, 12))
        self.edit = CTkImage(Image.open(r'icons/edit_icon.png'), size=(12, 12))
        self.trash = CTkImage(Image.open(r'icons/trash_icon.png'), size=(12, 12))
        self.visible_icon = CTkImage(Image.open(r'icons/visible_icon.png'), size=(12, 12))
        self.hidden_icon = CTkImage(Image.open(r'icons/hidden_icon.png'), size=(12, 12))

    def copy_stored_to_clipboard(self):
        """
        Copies the stored password to the clipboard
        """
        root.clipboard_clear()
        root.clipboard_append(self.password)

        if self.visibility_button:
            self.visibility_button.configure(image=self.checkmark_mini,
                                             fg_color='#0e6301')

        print(f"\ncopied: '{self.password}'")

    def delete_button(self):
        """
        Deletes button and all of its information from GUI and backend
        :return:
        """
        # Creates confirmation box to delete
        dialog = ctk.CTkInputDialog(text='ARE YOU SURE?\n\nType "Yes" to DELETE',
                                    title="Delete Password")
        response = dialog.get_input().upper()

        if response == "YES":
            # Clean up the associated references
            self.website_name = ""
            self.password = ""
            self.password_label = None
            self.website_label = None
            count_to_delete = self.count  # Store the count to be deleted

            # Remove the button from the list
            buttons[:] = [button for button in buttons if button.count != count_to_delete]

            # Clear the existing buttons on the GUI
            for widget in left_pane.grid_slaves():
                widget.grid_forget()

            # Update the self.count values based on the new order after deletion
            for index, button in enumerate(buttons):
                button.count = index

            # Place the sorted buttons back into the left_pane
            for button in buttons:
                button.create_btn_func()

            # Print the array of buttons
            print("Array of buttons after deletion:")
            for button in buttons:
                print(button.website_name, button.password, button.count)

    def edit_website_name(self):
        """
        Edits a stored website name via prompted user input
        :return:
        """
        print(f"Old name: {self.website_name}")

        # Creates dialog box to edit website name
        dialog = ctk.CTkInputDialog(text="New website name:",
                                    title="Edit")
        new_name = dialog.get_input()

        if new_name is not None:
            self.website_name = new_name.upper()
            self.website_label.configure(text=self.website_name)

            print(f"New name: {self.website_name}")
            print("")
        else:
            print("Editing canceled.")
            print("")

    def send_conversion_request(self):
        """
        Microservice that hides/shows the password in the left pane
        :return:
        """
        url = 'http://127.0.0.1:5000/passnerd'
        data = {'password': self.password, 'hidden': self.hidden}

        try:
            response = requests.post(url, json=data)

            if response.status_code == 200:
                response_json = response.json()
                if response_json['converted_hidden']:
                    self.password_label.configure(text=response_json['converted_password'])
                    self.hidden = response_json['converted_hidden']
                else:
                    self.password_label.configure(text=response_json['converted_password'])
                    self.hidden = response_json['converted_hidden']

                print(f"Converted Password: {self.password_label.cget('text')}")
                print(f"Converted Hidden: {self.hidden}")

            else:
                print(f"Error: {response.json()}")

        except Exception as e:
            print(f"Error: {str(e)}")

    def create_btn_func(self):
        """
        Adds the generated password to the saved website/password list
        """
        # If no password has been generated yet, return
        if not password.password:
            return

        # Creates dialog box to enter website name
        dialog = ctk.CTkInputDialog(text="Type in a website name:", title="Website Name")
        self.website_name = dialog.get_input().upper()

        # If no website name is provided, set a default name
        if not self.website_name:
            self.website_name = "New Website"

        # Puts an ellipsis if website name is +13 chars
        short_name = self.website_name
        if len(self.website_name) >= 13:
            short_name = self.website_name[:12] + '...'

        # Saved password button colors (alternating)
        button_color = "#343638"
        if self.count != 0:
            if self.count % 2 == 1:
                button_color = "#212121"

        # Creates button that stores website/password/other buttons
        button = ctk.CTkButton(left_pane,
                               text='',
                               height=71,
                               width=198,
                               font=('Calibri', 18),
                               anchor='w',
                               hover=True,
                               fg_color=button_color,
                               command=self.copy_stored_to_clipboard)
        button.grid(row=self.count, column=0, sticky='ew', padx=(3, 0), pady=2)

        # Website name label
        self.website_label = ctk.CTkLabel(button,
                                          text=short_name.upper(),
                                          font=('Calibri', 20, 'bold'),
                                          bg_color='transparent',
                                          padx=0,
                                          pady=0)
        self.website_label.place(relx=0.02,
                                 rely=0.2)

        # Password text label
        self.password_label = ctk.CTkLabel(button,
                                           text=password.password,
                                           font=('Calibri', 16),
                                           bg_color='transparent',
                                           padx=0)
        self.password_label.place(relx=0.02,
                                  rely=0.5)

        # Delete (trash) button
        delete_button = ctk.CTkButton(button,
                                      height=5,
                                      width=5,
                                      text='',
                                      fg_color='#1F538D',
                                      corner_radius=10,
                                      image=self.trash,
                                      command=self.delete_button)
        delete_button.place(relx=0.875,
                            rely=0.03)

        # Edit website button
        edit_button = ctk.CTkButton(button,
                                    height=5,
                                    width=5,
                                    text='',
                                    fg_color='#1F538D',
                                    corner_radius=10,
                                    image=self.edit,
                                    command=self.edit_website_name)
        edit_button.place(relx=0.875,
                          rely=0.35)

        # Visibility Button
        self.visibility_button = ctk.CTkButton(button,
                                               height=5,
                                               width=5,
                                               text='',
                                               fg_color='#1F538D',
                                               corner_radius=10,
                                               image=self.visible_icon,
                                               command=self.send_conversion_request)
        self.visibility_button.place(relx=0.875,
                                     rely=0.67)
        print("New Entry:")
        print(self.website_name, self.password, self.count)
        print("")

        root.after(100, self.update_visible)

    def update_visible(self):
        """
        Dynamically updates clipboard mini icon once successfully copied
        :return:
        """
        button_password = self.password

        try:
            clipboard_content = root.clipboard_get()
            if clipboard_content == button_password:
                self.visibility_button.configure(image=self.visible_icon,
                                                 fg_color="#0e6301",
                                                 hover_color="#083601")
            else:
                self.visibility_button.configure(image=self.visible_icon,
                                                 fg_color='#1F538D')
        except tk.TclError:
            # Handle the error when clipboard doesn't contain data or is empty
            self.visibility_button.configure(image=self.visible_icon,
                                             fg_color='#1F538D')  # Set the button image to clipboard icon

        root.after(100, self.update_visible)  # Run itself again after 10 ms

# GUI FUNCTIONS -------------------------------------------------------------------


password = PasswordGenerator()  # Creates a new password object
buttons = []


def generate_btn_func():
    """
    Generates a password into text box at top of app
    """
    password.create_password(int(slider_var.get()),
                             int(lower_check_var.get()),
                             int(upper_check_var.get()),
                             int(num_check_var.get()),
                             int(symbol_check_var.get()))
    password_text.set(password.password)
    clipboard_btn.configure(image=clipboard_big)


def copy_gen_to_clipboard():
    """
    Copies generated password into clipboard
    """
    root.clipboard_clear()
    root.clipboard_append(password.password)

    clipboard_btn.configure(image=checkmark, fg_color="#0e6301", hover_color="#083601")


def add_to_pane():
    """
    Adds new button object to left pane and adds it to list
    :return:
    """
    # If there is no password generated: return
    if password.password == "":
        return

    button = NewButton()                    # Initializes new button object
    button.password = password.password     # Initializes new password
    button.count = len(buttons)             # Set the count based on the number of existing buttons

    # Add the button to the list
    buttons.append(button)

    # Executes placing the button and all of its elements into the left pane
    button.create_btn_func()

    # Clears generated password
    password_entry.delete(0, 'end')
    password.password = ""


def sort_toggle():
    """
    Sorts buttons by website name from a to z or from z to a
    :return:
    """
    # Clear the existing buttons on the GUI
    for widget in left_pane.grid_slaves():
        widget.grid_forget()

    # Sorts buttons by website a -> z
    buttons.sort(key=lambda x: x.website_name)

    # Update the self.count values based on the new sorted order
    for index, button in enumerate(buttons):
        button.count = index

# WIDGETS -------------------------------------------------------------------------------


# Password text box
password_text = ctk.StringVar()  # StringVar to hold the password value
password_entry = ctk.CTkEntry(master=top_level,
                              height=50,
                              width=350,
                              textvariable=password_text,
                              font=('Calibri', 30),
                              state='normal')

# Copy to clipboard button
clipboard_btn = ctk.CTkButton(master=password_entry,
                              height=30,
                              width=30,
                              text='',
                              command=copy_gen_to_clipboard,
                              image=clipboard_big)

# Password length slider
char_slider = ctk.CTkSlider(master=char_length_label,
                            variable=slider_var,
                            width=350,
                            from_=8,
                            to=16)

# lowercase checkmark
lower_check_var = ctk.IntVar(value=1)
lower_check = ctk.CTkCheckBox(master=include_label,
                              text="  Lowercase Letters",
                              font=('Calibri', 16),
                              variable=lower_check_var,
                              onvalue=1,
                              offvalue=0)

# uppercase checkmark
upper_check_var = ctk.IntVar(value=1)
upper_check = ctk.CTkCheckBox(master=include_label,
                              text="  Uppercase Letters",
                              font=('Calibri', 16),
                              variable=upper_check_var,
                              onvalue=1,
                              offvalue=0)

# numbers checkmark
num_check_var = ctk.IntVar(value=1)
num_check = ctk.CTkCheckBox(master=include_label,
                            text="  Numbers",
                            font=('Calibri', 16),
                            variable=num_check_var,
                            onvalue=1,
                            offvalue=0)

# symbols checkmark
symbol_check_var = ctk.IntVar(value=1)
symbol_check = ctk.CTkCheckBox(master=include_label,
                               text="  Symbols",
                               font=('Calibri', 16),
                               variable=symbol_check_var,
                               onvalue=1,
                               offvalue=0)

# Generate password button
generate_btn = ctk.CTkButton(master=generate_frame,
                             text="Generate Password",
                             command=generate_btn_func,
                             width=290,
                             height=50,
                             font=('Calibri', 20, 'bold'))

# Plus button (saves website/password)
add_btn = ctk.CTkButton(master=generate_frame,
                        width=50,
                        height=50,
                        text='',
                        command=add_to_pane,
                        image=plus_big)

# LOWER LEFT PANE BUTTONS
visible = ctk.CTkButton(root,
                        height=38,
                        width=100,
                        text="",
                        fg_color='#212121',
                        image=visible)
visible.grid(row=0, column=0, sticky='sw', padx=(0, 0))

hidden = ctk.CTkButton(root,
                       height=38,
                       width=100,
                       text="",
                       fg_color='#212121',
                       image=hidden)
hidden.grid(row=0, column=0, sticky='sw', padx=(100, 0))
# STYLING -----------------------------------------------------------------------------


password_entry.grid(row=0,
                    column=0,
                    padx=0,
                    pady=(0, 0))

clipboard_btn.place(relx=0.855,
                    rely=0.15)

char_slider.grid(row=1,
                 column=0,
                 padx=0,
                 pady=(0, 0),
                 sticky='w')

lower_check.grid(row=1,
                 column=0,
                 padx=0,
                 pady=(0, 10),
                 sticky='w')

upper_check.grid(row=2,
                 column=0,
                 padx=0,
                 pady=(0, 10),
                 sticky='w')

num_check.grid(row=3,
               column=0,
               padx=0,
               pady=(0, 10),
               sticky='w')

symbol_check.grid(row=4,
                  column=0,
                  padx=0,
                  pady=(0, 30),
                  sticky='w')

generate_btn.grid(row=1,
                  column=0,
                  padx=0,
                  pady=(0, 0),
                  sticky='w')

add_btn.grid(row=1,
             column=1,
             padx=10,
             pady=(0, 0),
             sticky='e')


# REALTIME UPDATES  ---------------------------------------------------------------------------------------


def update_clipboard_big():
    """
    Dynamically updates clipboard icon once successfully copied
    :return:
    """
    current_password = password.password  # Assuming you have defined password somewhere

    try:
        clipboard_content = root.clipboard_get()
        if clipboard_content == current_password:
            clipboard_btn.configure(image=checkmark, fg_color="#0e6301", hover_color="#083601")
        else:
            clipboard_btn.configure(image=clipboard_big, fg_color="#1F538D")
    except tk.TclError:
        # Handle the error when clipboard doesn't contain data or is empty
        clipboard_btn.configure(image=clipboard_big, fg_color="#1F538D")  # Set the button image to clipboard icon

    root.after(10, update_clipboard_big)  # Run itself again after 10 ms


update_clipboard_big()  # Start the update process
root.mainloop()  # Runs app
