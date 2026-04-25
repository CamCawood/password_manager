from tkinter import messagebox
class DeleteAccount:
    """Class for deleting the selected account"""
    def __init__(self,main):
        self.main = main 
        self.add_account = self.main.add_account
        self.file_manager = self.main.file_manager
        
    def delete_command(self):
        """Method for deleting the chosen account"""
        selected = self.main.tree.selection()

        if selected:
            self.tree_id = selected[0]
            self.selected_item = self.main.tree.item(self.tree_id)["values"]

            if self._check_delete():
                self._delete_account()
            
    def _check_delete(self):
        """Checks if this is to be deleted via a messagebox and returns True if yes is selected"""
        message_box = messagebox.askyesno(title="Delete Account?", message=f"Do you want to delete {self.selected_item[0]}")
        if message_box:
            return True
        else:
            return False
    
    def _delete_account(self):
        """Deletes the selected account using the hidden treeview ID."""
        contents = self.file_manager.open_file()["data"]

        selected_id = int(self.tree_id)

        contents = [
            account for account in contents
            if account["id"] != selected_id
        ]

        self.file_manager.write_file({"data": contents})
        self.main.update_tree()