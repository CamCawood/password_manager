from widget_toolkit import widget_factory
import customtkinter as ct
import json 
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import add_account as add_account
import edit_account as edit_account
import delete_account as delete_account
from cryptography.fernet import Fernet
import os

class EncryptionManager:
    """Handles password encryption and decryption."""

    def __init__(self, key_file="Password_manager/secret.key"):
        self.key_file = key_file
        self.key = self._load_or_create_key()
        self.fernet = Fernet(self.key)

    def _load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as file:
                return file.read()

        key = Fernet.generate_key()

        with open(self.key_file, "wb") as file:
            file.write(key)

        return key

    def encrypt(self, text):
        return self.fernet.encrypt(text.encode()).decode()

    def decrypt(self, encrypted_text):
        return self.fernet.decrypt(encrypted_text.encode()).decode()
    
    
class FileManager:
    """Class for managing the files such as opening and writing"""
    def __init__(self,file_path):
        self.file_path = file_path
    
    def open_file(self):
        """Opens the with file with json and returns the contents"""
        with open(file = self.file_path, mode = "r") as file:
            return json.load(file)
    
    def write_file(self,contents):
        """Writes the contents to the file"""
        with open(file = self.file_path, mode="w") as file:
            json.dump(contents,file,indent=4)


class Settings:
    """Class for managing the settings such as fonts and colours"""
    def __init__(self):
        self.BG_COLOUR = "#0F172A"  
        self.TREEVIEW_COLOUR = "#1E293B"
        self.TITLE_COLOUR = "#F8FAFC"
        self.BUTTON_COLOUR = "#3B82F6"
        self.BUTTON_HOVER_COLOUR = "#2563EB"
        
        self.INPUT_BG = "#111827"
        self.INPUT_BORDER = "#334155"
        self.PLACEHOLDER_TEXT_COLOUR = "#94A3B8"
        
        
class Main:
    """Class for running the main instance"""
    def __init__(self):
        self.root = ct.CTk()
    
        self.encryption_manager = EncryptionManager()
        self.settings = Settings()
        self.root.configure(fg_color = self.settings.BG_COLOUR)
        self.ACCOUNT_FIELDS = ["id","website", "username", "password", "notes"]
        self.file_manager = FileManager(file_path="Password_manager/data.json")
        self.widgets = widget_factory.CreateWidgets()
        self.load_image = widget_factory.ImageLoader()
        
        self.add_account = add_account.AddAccount(self)
        self.edit_account = edit_account.EditAccount(self)
        self.delete_account = delete_account.DeleteAccount(self)
        
        
    def authenticate(self):
        """Makes the login screen page."""
        self.login_widgets = []
        self.root.title("Password Manager")
        self.login_frame = self.widgets.create_ct_frame(
            master=self.root,
            grid_position=(0, 0),
            width=360,
            height=260,
            fg_color="#1E293B",
            border_color="#334155",
            border_width=2,
            padx=40,
            pady=40
        )

        login_title = self.widgets.create_ct_label(
            master=self.login_frame,
            grid_position=(0, 0),
            text="Password Vault",
            font=ct.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="#F8FAFC",
            pady=(20, 5)
        )

        login_subtitle = self.widgets.create_ct_label(
            master=self.login_frame,
            grid_position=(1, 0),
            text="Enter your master password",
            font=ct.CTkFont(family="Arial", size=16),
            text_color="#94A3B8",
            pady=(0, 20)
        )

        self.master_password_entry = self.widgets.create_ct_entry(
            master=self.login_frame,
            grid_position=(2, 0),
            width=260,
            placeholder_text="Master password",
            fg_color="#111827",
            border_color="#334155",
            border_width=2,
            text_color="#F8FAFC",
            placeholder_text_color="#94A3B8",
            pady=(0, 15)
        )
        self.master_password_entry.configure(show="*")

        enter_button = self.widgets.create_ct_button(
            master=self.login_frame,
            grid_position=(3, 0),
            width=260,
            text="Unlock Vault",
            command=self.login,
            fg_color=self.settings.BUTTON_COLOUR,
            hover_color=self.settings.BUTTON_HOVER_COLOUR,
            text_color="#F8FAFC",
            pady=(5, 20)
        )

        self.login_widgets.append(self.login_frame)
        
    
    def login(self):
        """Method for checking if login is successful."""
        if self.master_password_entry.get() == "password":
            self.login_frame.destroy()
            self.create_home_page()
            self.load_in_data()
        else:
            messagebox.showerror("Login failed", "Incorrect master password.")
                
    
    def run_gui(self):
        """Method called for running the gui"""
        self.authenticate()
        
        self.root.mainloop()
    
    def create_home_page(self):
        """Method for creating the main home page"""
        self.widgets.create_ct_label(
            master = self.root, text = "Password Manager", grid_position = (0,0),
            font = ct.CTkFont(family="Arial",size=50),columnspan = 3, padx = 10, pady = 30,
            text_color = self.settings.TITLE_COLOUR
        )
        
        self.create_action_buttons()
        
        self.make_tree()
        
        
    def create_action_buttons(self):
        """Creates the action buttons for adding, deleting and editing accounts"""
        button_details_dict = {
            "add_button":{"command":self.add_account.add_command,"image":"add_icon"},
            "edit_button":{"command":self.edit_account.edit_command,"image":"edit_icon"},
            "delete_button":{"command":self.delete_account.delete_command,"image":"delete_icon"}
        }
        
        for column,button_details in enumerate(button_details_dict.items()):
            details = button_details[1]
            image = self.load_image.load_image(file=f"Password_manager/images/{details.get('image')}.png",size=(50,50))
            self.add_password_button = self.widgets.create_ct_button(
                master = self.root, grid_position = (1,column), text = "",
                pady = 20, command = details.get("command"),
                image = image,width =40,hover_color = self.settings.BUTTON_HOVER_COLOUR,
                fg_color = self.settings.BUTTON_COLOUR
            )
        
    
    
    def load_in_data(self):
        """Loads in the data into the treeview from the file"""
        for account in self.file_manager.open_file()["data"]:
            self.tree.insert(
                "",
                tk.END,
                iid=str(account.get("id")),  # hidden ID
                values=(
                    account.get("website"),
                    account.get("username"),
                    self.encryption_manager.decrypt(account.get("password")),
                    account.get("notes")
                )
            )
    
    
    def make_tree(self):
        """Makes the tree view"""
         # Define columns
        columns = self.ACCOUNT_FIELDS[1:]
        
        # Make tree
        self.tree = ttk.Treeview(
            self.root,
            columns= columns,
            show= "headings"
        )
        # Display column titles
        for c in columns:
            self.tree.heading(c, text=c)
        self.tree.grid(row = 2, column=0, columnspan=3,padx=10,pady=10)
    
    def update_tree(self):
        """Updates the tree by deleting it and making it again"""
        self.tree.destroy()
        self.make_tree()
        self.load_in_data()
        
        


main = Main()
main.run_gui()