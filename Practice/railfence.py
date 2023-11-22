def rail_fence_encrypt(plaintext, depth):
    # Remove any whitespace from the plaintext
    plaintext = plaintext.replace(" ", "")
    
    # Create the rail fence pattern
    rail_fence = [[] for _ in range(depth)]
    rail = 0
    direction = 1
    
    for char in plaintext:
        rail_fence[rail].append(char)
        
        # Change direction when reaching the top or bottom rail
        if rail == 0:
            direction = 1
        elif rail == depth - 1:
            direction = -1
        
        rail += direction
    
    # Concatenate the rails to form the encrypted text
    ciphertext = ""
    for rail in rail_fence:
        ciphertext += "".join(rail)
    
    return ciphertext


def rail_fence_decrypt(ciphertext, depth):
    # Calculate the length of each rail
    rail_lengths = [0] * depth
    rail = 0
    direction = 1
    
    for _ in range(len(ciphertext)):
        rail_lengths[rail] += 1
        
        # Change direction when reaching the top or bottom rail
        if rail == 0:
            direction = 1
        elif rail == depth - 1:
            direction = -1
        
        rail += direction
    
    # Create the rail fence pattern
    rail_fence = [[] for _ in range(depth)]
    rail = 0
    direction = 1
    
    for char in ciphertext:
        rail_fence[rail].append(None)
        
        # Change direction when reaching the top or bottom rail
        if rail == 0:
            direction = 1
        elif rail == depth - 1:
            direction = -1
        
        rail += direction
    
    # Fill in the rail fence pattern with the ciphertext characters
    index = 0
    for rail in rail_fence:
        for i in range(len(rail)):
            rail[i] = ciphertext[index]
            index += 1

    
    # Read the plaintext from the rail fence pattern
    plaintext = ""
    rail = 0
    direction = 1
    
    for _ in range(len(ciphertext)):
        plaintext += rail_fence[rail].pop(0)
        
        # Change direction when reaching the top or bottom rail
        if rail == 0:
            direction = 1
        elif rail == depth - 1:
            direction = -1
        
        rail += direction
    
    return plaintext


# Get user input for plaintext and depth
plaintext = input("Enter the plaintext: ")
depth = int(input("Enter the depth: "))

# Encrypt the plaintext using Rail Fence Cipher
ciphertext = rail_fence_encrypt(plaintext, depth)
print("Encrypted ciphertext:", ciphertext)

# Decrypt the ciphertext using Rail Fence Cipher
decrypted_plaintext = rail_fence_decrypt(ciphertext, depth)
print("Decrypted plaintext:", decrypted_plaintext)
