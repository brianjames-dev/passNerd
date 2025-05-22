import customtkinter as ctk


class SavePassword:
    def __init__(self):
        self.buttons = []

    def create_button(self, master, name, password):
        button = ctk.CTkButton(master,
                               text=name,
                               height=70,
                               width=200,
                               font=('Calibri', 12))

        button.password = password.password
        self.buttons.append(button)

