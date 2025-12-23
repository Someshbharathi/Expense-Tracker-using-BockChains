# Expense-Tracker-using-BlockChains

# 📌 Overview

This project is a Blockchain-based Expense and Balance Tracker built using Python and Tkinter.
It records every transaction as a block in a blockchain, ensuring data integrity, transparency, and tamper detection while providing a simple and user-friendly graphical interface.

Instead of storing expenses in a traditional database, this application uses blockchain principles such as hashing and block linking to maintain a secure transaction ledger.

# 🚀 Features

Add income and expense transactions

Blockchain-style transaction storage

SHA-256 hashing for data integrity

Linked blocks using previous hash references

Automatic balance calculation

Persistent storage using JSON

Graphical User Interface (GUI) using Tkinter

Tamper detection using blockchain validation

Refresh and reset functionality

# 🧱 How Blockchain is Used

Each transaction is stored as a block containing:

Transaction index

Timestamp

Description

Amount

Hash of the previous block

Current block hash

Blocks are linked together using cryptographic hashes, forming a chain.
If any transaction data is modified, the blockchain validation fails, indicating tampering.

This project represents a private, single-node blockchain designed for learning and demonstration purposes.

# 🖥️ Tech Stack

Language: Python 3

GUI: Tkinter

Hashing Algorithm: SHA-256

Data Storage: JSON

Concepts Used: Blockchain, Cryptography, OOP

# 📂 Project Structure

main.py – Main application logic and GUI

blockchain.json – Persistent storage for blockchain data (auto-generated)

# ▶️ How to Run

Ensure Python 3 is installed

Clone the repository

Run the application:

python main.py


The GUI window will open for managing transactions

# 💡 Usage Instructions

Enter a description for the transaction

Enter the amount:

Positive value → Income

Negative value → Expense

Click Add Transaction

View all transactions in the table

Balance updates automatically

Use Refresh to reload data

Use Reset to clear all transactions

# 🔐 Blockchain Validation

The application includes blockchain validation logic to:

Verify block hashes

Ensure correct linking between blocks

Detect any unauthorized data modification

# 🎯 Learning Outcomes

Understanding blockchain fundamentals

Hands-on experience with cryptographic hashing

GUI development using Tkinter

File handling and persistent storage

Object-Oriented Programming in Python

Applying blockchain concepts beyond cryptocurrency

# ⚠️ Disclaimer

This is a blockchain-inspired educational project.
It does not include features like distributed nodes, mining, or consensus mechanisms used in public blockchains like Bitcoin or Ethereum.

# 📌 Future Enhancements

Multi-user support

Encryption for stored data

Export transactions to CSV

Graphical expense analytics

Network-based distributed blockchain

# 👤 Author
=> Arun Vasanth Selwyn Sudhaker

=> Somesh Barathi

=> Geethika R

Developed as an academic and learning project to demonstrate blockchain concepts applied to real-world use cases.
