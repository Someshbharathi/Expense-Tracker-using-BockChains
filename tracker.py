import tkinter as tk
from tkinter import messagebox, ttk
import hashlib
import datetime
import json

# File to persist blockchain
BLOCKCHAIN_FILE = 'blockchain.json'

# Blockchain Components
class Block:
    def __init__(self, index, timestamp, description, amount, previous_hash, hash_value=None):
        self.index = index
        self.timestamp = timestamp
        self.description = description
        self.amount = amount
        self.previous_hash = previous_hash
        self.hash = hash_value or self.calculate_hash()

    def calculate_hash(self):
        data_string = f"{self.index}{self.timestamp}{self.description}{self.amount}{self.previous_hash}"
        return hashlib.sha256(data_string.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "description": self.description,
            "amount": self.amount,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

    @staticmethod
    def from_dict(data):
        return Block(
            data["index"],
            data["timestamp"],
            data["description"],
            data["amount"],
            data["previous_hash"],
            data["hash"]
        )


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now().isoformat(), "Genesis Block", 0.0, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, description, amount):
        latest_block = self.get_latest_block()
        new_block = Block(
            len(self.chain),
            datetime.datetime.now().isoformat(),
            description,
            amount,
            latest_block.hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def calculate_balance(self):
        balance = 0.0
        for block in self.chain[1:]:  # Skip the genesis block
            balance += block.amount
        return balance

    def to_dict(self):
        return [block.to_dict() for block in self.chain]

    @staticmethod
    def from_dict(data):
        blockchain = Blockchain()
        blockchain.chain = [Block.from_dict(block) for block in data]
        return blockchain


# Save and Load Blockchain from File
def save_blockchain(blockchain):
    with open(BLOCKCHAIN_FILE, 'w') as file:
        json.dump(blockchain.to_dict(), file, indent=4)


def load_blockchain():
    try:
        with open(BLOCKCHAIN_FILE, 'r') as file:
            data = json.load(file)
        return Blockchain.from_dict(data)
    except FileNotFoundError:
        return Blockchain()


# GUI Application
def setup_gui():
    global desc_entry, amount_entry, tree, balance_label, blockchain
    blockchain = load_blockchain()

    def add_transaction():
        description = desc_entry.get().strip()
        amount_str = amount_entry.get().strip()
        if not description:
            messagebox.showerror("Input Error", "Please enter a description.")
            return
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for amount.")
            return

        blockchain.add_block(description, amount)
        save_blockchain(blockchain)  # Save blockchain after adding a block
        load_transactions()
        update_balance()
        desc_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Transaction added successfully!")

    def load_transactions():
        # Clear the existing rows in the Treeview
        for item in tree.get_children():
            tree.delete(item)

        # Loop through blockchain and add non-Genesis blocks
        for block in blockchain.chain[1:]:  # Skip the Genesis Block (index 0)
            tree.insert(
                '',
                tk.END,
                values=(block.index, block.timestamp, block.description, block.amount, block.previous_hash, block.hash)
            )

    def update_balance():
        balance = blockchain.calculate_balance()
        balance_label.config(text=f"Balance: Rs. {balance:.2f}")

    def refresh_transactions():
        global blockchain
        blockchain = load_blockchain()  # Reload the blockchain from the file
        load_transactions()
        update_balance()
        messagebox.showinfo("Refresh", "Transactions reloaded successfully.")

    def reset_transactions():
        confirm = messagebox.askyesno("Confirm Reset", "Are you sure you want to delete all transactions?")
        if confirm:
            global blockchain
            blockchain = Blockchain()  # Create a new blockchain with only the Genesis Block
            save_blockchain(blockchain)  # Save the reset blockchain
            load_transactions()  # Reload the GUI
            update_balance()
            messagebox.showinfo("Reset", "All transactions have been deleted.")

    root = tk.Tk()
    root.title("Blockchain Expense and Balance Tracker")
    root.geometry("800x600")
    root.resizable(False, False)

    # Frame for adding transactions
    add_frame = tk.Frame(root, padx=10, pady=10)
    add_frame.pack(fill=tk.X)
    tk.Label(add_frame, text="Description:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    desc_entry = tk.Entry(add_frame, width=30)
    desc_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(add_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    amount_entry = tk.Entry(add_frame, width=30)
    amount_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Label(add_frame, text="(Use negative for expenses)").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
    add_button = tk.Button(add_frame, text="Add Transaction", command=add_transaction)
    add_button.grid(row=2, column=0, columnspan=3, pady=10)

    # Frame for displaying transactions
    display_frame = tk.Frame(root, padx=10, pady=10)
    display_frame.pack(fill=tk.BOTH, expand=True)
    columns = ('Index', 'Timestamp', 'Description', 'Amount', 'Previous Hash', 'Hash')
    tree = ttk.Treeview(display_frame, columns=columns, show='headings')
    tree.heading('Index', text='Index')
    tree.heading('Timestamp', text='Timestamp')
    tree.heading('Description', text='Description')
    tree.heading('Amount', text='Amount')
    tree.heading('Previous Hash', text='Previous Hash')
    tree.heading('Hash', text='Hash')
    tree.column('Index', width=50, anchor=tk.CENTER)
    tree.column('Timestamp', width=150)
    tree.column('Description', width=150)
    tree.column('Amount', width=100, anchor=tk.E)
    tree.column('Previous Hash', width=200)
    tree.column('Hash', width=200)
    tree.pack(fill=tk.BOTH, expand=True)

    # Frame for balance
    balance_frame = tk.Frame(root, padx=10, pady=10)
    balance_frame.pack(fill=tk.X)
    balance_label = tk.Label(balance_frame, text="Balance: Rs. 0.00", font=("Helvetica", 14))
    balance_label.pack()

    # Add Buttons
    button_frame = tk.Frame(root, padx=10, pady=10)
    button_frame.pack(fill=tk.X)

    refresh_button = tk.Button(button_frame, text="Refresh", command=refresh_transactions)
    refresh_button.pack(side=tk.LEFT, padx=5)

    reset_button = tk.Button(button_frame, text="Reset", command=reset_transactions)
    reset_button.pack(side=tk.RIGHT, padx=5)

    # Load initial transactions
    load_transactions()
    update_balance()

    root.mainloop()


if __name__ == "__main__":
    setup_gui()
