import customtkinter as ct
import string
import random
from tkinter import messagebox
class AddAccount:
    """Class for adding a password"""
    def __init__(self,main):
        self.main = main
        self.widgets = self.main.widgets
        self.file_manager = self.main.file_manager
        self.settings = self.main.settings
        self.generate_random_data = GenerateRandomData()
        
        self.show_password_button_clicked = False
        self.first_time_textbox_clicked = False
    
    def add_command(self):
        """Method for running the add ommand"""
        self.toplevel = ct.CTkToplevel(
            self.main.root, fg_color=self.settings.BG_COLOUR
        )
        
        self.toplevel.title("Add Password")
        self.toplevel.transient(self.main.root) 
        self.toplevel.grab_set()                 
        self.toplevel.lift()                     
        self.toplevel.focus_force()

        self._create_add_password_page()
        
        
        
    
    def _create_add_password_page(self):
        """Creates the add password home page"""
        self.add_password_title = self.widgets.create_ct_label(
            master = self.toplevel, text = "Add Password", grid_position = (0,0),
            font = ct.CTkFont(family="Arial",size=30), padx = 10, pady = 30,text_color = self.settings.TITLE_COLOUR,
            
        )
        
        self._create_entry_boxes()
        
        # Save button 
        last_row = int(self.entry_boxes[-1].grid_info()["row"])
        self.save_button = self.widgets.create_ct_button(
            master = self.toplevel, grid_position = (last_row+1,0), text = "Save",
            pady = 10,command = lambda:self._save_button_command(),
            fg_color = self.settings.BUTTON_COLOUR, hover_color = self.settings.BUTTON_HOVER_COLOUR
        )
    
    
    def _create_entry_boxes(self):
        """Creates the entry boxes for entering account info"""
        self.entry_boxes = []
        row = 1
        for i in self.main.ACCOUNT_FIELDS[1:]:
            i = i.title()
            if i.lower() == "notes":
                notes_textbox = self.widgets.create_ct_textbox(
                    master = self.toplevel,grid_position = (row,0),
                    width = 300, height = 150,pady =10, fg_color = self.settings.INPUT_BG,
                    border_color = self.settings.INPUT_BORDER,border_width = 2, text_color = self.settings.PLACEHOLDER_TEXT_COLOUR
                )
                notes_textbox.insert("end",i)
                notes_textbox.bind("<Button-1>",lambda event:self._clear_notes_textbox(notes_textbox))
                self.entry_boxes.append(notes_textbox)
                
            else:
                entry = self.widgets.create_ct_entry(
                    master = self.toplevel, placeholder_text = i, grid_position = (row,0),
                    width = 300, pady = 5, padx = 5,fg_color = self.settings.INPUT_BG,
                    border_color = self.settings.INPUT_BORDER,border_width = 2, text_color = self.settings.PLACEHOLDER_TEXT_COLOUR,
                    placeholder_text_color = self.settings.PLACEHOLDER_TEXT_COLOUR
                )
                
                if i.lower() == "username" or i.lower() == "password":
                    generate_button_image = self.main.load_image.load_image(file = "Password_manager/images/generate_icon.png",size = (30,30))
                    if i.lower() == "username":
                        generate_column = 1
                        generate_type = "username"
                    if i.lower() == "password":
                        generate_column = 2
                        generate_type = "password"
                        
                        show_password_button_image = self.main.load_image.load_image(file = "Password_manager/images/show_password_icon.png",size = (30,30))
                        self.visable_password_button = self.widgets.create_ct_button(
                        master = self.toplevel, grid_position = (row,1), text = "",
                        width = 20,height = 20,command = lambda e = entry:self._show_password(e),
                        image = show_password_button_image,padx = 2,fg_color = self.settings.BUTTON_COLOUR, hover_color = self.settings.BUTTON_HOVER_COLOUR
                        )
                    self.generate_button = self.widgets.create_ct_button(
                    master = self.toplevel, grid_position = (row,generate_column), text = "",
                    width = 20,height = 20,command = lambda e = entry, g = generate_type:self._generate_random_button_command(g,e),
                    image = generate_button_image,
                    fg_color = self.settings.BUTTON_COLOUR, hover_color = self.settings.BUTTON_HOVER_COLOUR
                    )
                self.entry_boxes.append(entry)
            row += 1
        
    
    
    def _generate_random_button_command(self,generation_type,entry):
        """Generates a random username or password"""
        entry.delete("0","end")
        if generation_type == "username":
            
            random_username = self.generate_random_data.generate_random_username()
            entry.insert("0",random_username)
        else:
            random_password = self.generate_random_data.generate_random_password()
            entry.insert("0",random_password)
        self.show_password_button_clicked = False
    
    def _show_password(self,entry):
        """Shows the current password"""
        if not self.show_password_button_clicked:
            if entry.get().strip():
                # show the password
                entry.delete("0","end")
                entry.insert("0",self.generate_random_data.current_password)
                self.show_password_button_clicked = True
        else:
            entry.delete("0","end")
            entry.insert("0","******************")
            self.show_password_button_clicked = False
    
    def _clear_notes_textbox(self,textbox):
        """Clears the notes textbox upon first click"""
        if not self.first_time_textbox_clicked and textbox.get("0.0","end").strip() == "Notes":
            textbox.delete("0.0","end")
            self.first_time_textbox_clicked = True
        else:
            self.first_time_textbox_clicked = False
            
    
    def _get_entry_box_text(self):
        """Gets all the entry box text and returns it in a list"""
        entry_texts = []
        for entry in self.entry_boxes:
            if isinstance(entry,ct.CTkTextbox):
                entry_texts.append(entry.get("0.0","end").strip())
            else:
                entry_texts.append(entry.get())
        return entry_texts
    
    def _check_enteries(self):
        """Checks all the enteries if they are empy and returns False if they are. Returns True if all have text"""
        check_list = []
        for entry in self._get_entry_box_text():
            if not entry or entry == "Notes":
                check_list.append(False)
            else:
                check_list.append(True)
        return all([i for i in check_list])
    
    
    def _save_button_command(self):
        """Command for checking if the enteries are valid and saving them"""
        if not self._check_enteries():
            # message box saying cant be saved needs all enteries filled
            messagebox.showinfo(
                title = "Not saved", message = "All enteries need to be filled."
            )
            
        else:
            self._save_enteries()
    
    
    
    def _save_enteries(self):
        """Saves the entries."""
        contents = self.file_manager.open_file()["data"]
        entries = self._get_entry_box_text()

        if contents:
            new_id = max(account["id"] for account in contents) + 1
        else:
            new_id = 1

        account_to_save = {
            "id": new_id,
            "website": entries[0],
            "username": entries[1],
            "password": entries[2],
            "notes": entries[3]
        }

        if account_to_save["password"] == "******************":
            account_to_save["password"] = str(self.generate_random_data.current_password)

        account_to_save["password"] = self.main.encryption_manager.encrypt(
            account_to_save["password"]
            )
        
        contents.append(account_to_save)
        self.file_manager.write_file({"data": contents})
        messagebox.showinfo(title="Account Saved", message="The account has been saved.")
        self.toplevel.destroy()
        self.main.update_tree()
    
    
        
class GenerateRandomData:
    """Generates random data that is used for the username and password"""
    def __init__(self):
        letters = list(string.ascii_letters)
        self.digits = list(string.digits)
        punctuation = list(string.punctuation)
        punctuation.remove("\\")
        self.usable_strings = letters + self.digits + punctuation
        
        self.adjectives = [
            "Swift", "Silent", "Clever", "Brave", "Fierce",
            "Mighty", "Shadow", "Golden", "Crimson", "Iron",
            "Stormy", "Frozen", "Wild", "Lone", "Dark",
            "Bright", "Rapid", "Sharp", "Ghostly", "Noble",
            "Savage", "Ancient", "Electric", "Mystic", "Solar",
            "Lunar", "Cosmic", "Vivid", "Stealthy", "Fearless"
        ]
        
        self.nouns = [
            "Tiger", "Wolf", "Falcon", "Hawk", "Panther",
            "Dragon", "Phoenix", "Viper", "Shark", "Raven",
            "Knight", "Ninja", "Samurai", "Hunter", "Warrior",
            "Guardian", "Ranger", "Assassin", "Sniper", "Warden",
            "Blade", "Arrow", "Hammer", "Shield", "Spear",
            "Shadow", "Storm", "Flame", "Frost", "Thunder"
        ]
        
    def generate_random_username(self):
        """Generates a random username"""
        random.shuffle(self.adjectives)
        random.shuffle(self.nouns)
        random.shuffle(self.digits)
        username = random.choice(self.adjectives) + random.choice(self.nouns) + "".join([random.choice(self.digits) for i in range(2)])
        return username
        
    def generate_random_password(self):
        """Generates a random password"""
        random.shuffle(self.usable_strings)
        password_list = [random.choice(self.usable_strings) for i in range(18)]
        random.shuffle(password_list)
        password_string = "".join(password_list)
        self.current_password = password_string
        return "******************"