# Function to encrypt the message using columnar transposition cipher
def encrypt(message, key):
    # Remove any spaces from the message
    message = message.replace(" ", "")

    # Calculate the number of rows required
    rows = len(message) // len(key)
    if len(message) % len(key) != 0:
        rows += 1

    # Create an empty grid
    grid = [[''] * len(key) for _ in range(rows)]

    # Fill the grid with the message
    index = 0
    for col in range(len(key)):
        for row in range(rows):
            if index < len(message):
                grid[row][col] = message[index]
                index += 1

    # Create the encrypted message by reading the columns in the order specified by the key
    encrypted_message = ""
    for col in key:
        col_index = int(col) - 1
        for row in range(rows):
            encrypted_message += grid[row][col_index]

    return encrypted_message

# Function to decrypt the message using columnar transposition cipher
def decrypt(message, key):
    # Calculate the number of rows required
    rows = len(message) // len(key)
    if len(message) % len(key) != 0:
        rows += 1

    # Calculate the number of columns required
    cols = len(key)

    # Calculate the number of empty cells in the last row
    empty_cells = (rows * cols) - len(message)

    # Create an empty grid
    grid = [[''] * cols for _ in range(rows)]

    # Fill the grid with the message
    index = 0
    for col in key:
        col_index = int(col) - 1
        for row in range(rows):
            if row == rows - 1 and col_index >= cols - empty_cells:
                continue
            grid[row][col_index] = message[index]
            index += 1

    # Create the decrypted message by reading the rows in order
    decrypted_message = ""
    for row in range(rows):
        for col in range(cols):
            decrypted_message += grid[row][col]

    return decrypted_message

# Get user input for the message and key
message = input("Enter the message: ")
key = input("Enter the key: ")

# Encrypt the message
encrypted_message = encrypt(message, key)
print("Encrypted message:", encrypted_message)

# Decrypt the message
decrypted_message = decrypt(encrypted_message, key)
print("Decrypted message:", decrypted_message)
