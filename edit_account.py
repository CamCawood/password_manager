import customtkinter as ct
class EditAccount:
    """Class for editing the selected password"""
    def __init__(self,main):
        """Initaliszes the attibutes for editing an account"""
        self.main = main 
        self.add_account = self.main.add_account
        self.file_manager = self.main.file_manager
        
    def edit_command(self):
        """Method for editing the selected account"""
        # get the selected item in tree view
        seleted = self.main.tree.selection()
        
        if seleted:
            # get the selected item values
            self.tree_id = seleted[0]
            self.selected_item = self.main.tree.item(self.tree_id)["values"]
            self.add_account.add_command()
            self.add_account.add_password_title.configure(text = "Edit Password")
            self.add_account.toplevel.title("Edit Password")
            self.add_account.generate_random_data.current_password = self.selected_item[2]
            
            # fill the enteries with those values
            for i,entry in enumerate(self.add_account.entry_boxes):
                if isinstance(entry,ct.CTkTextbox):
                    entry.delete("0.0","end")
                if i == 2:
                    entry.insert("end","******************")
                else:
                    entry.insert("end",self.selected_item[i])
            
            
            # Edit the save command in add password to remove it before
            self.add_account.save_button.configure(
                command = lambda:self._update_account()
            )

    
    
    def _update_account(self):
        """Updates the selected account in the file."""
        contents = self.file_manager.open_file()["data"]
        entries = self.add_account._get_entry_box_text()
        
        selected_id = int(self.tree_id)

        for account in contents:
            if account["id"] == selected_id:
                account["website"] = entries[0]
                account["username"] = entries[1]

                if entries[2] == "******************":
                    plain_password = self.add_account.generate_random_data.current_password
                else:
                    plain_password = entries[2]

                account["password"] = self.main.encryption_manager.encrypt(plain_password)

                account["notes"] = entries[3]
                break

        self.file_manager.write_file({"data": contents})
        self.add_account.toplevel.destroy()
        self.main.update_tree()
        
        
    
