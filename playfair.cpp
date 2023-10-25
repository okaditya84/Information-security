#include <iostream>
#include <string>
#include <vector>

using namespace std;

// Function to prepare the Playfair matrix
vector<vector<char>> prepareMatrix(string key) {
    vector<vector<char>> matrix(5, vector<char>(5, ' '));
    string uniqueChars = "";

    // Fill the matrix with the key (omitting duplicates and 'J')
    for (char c : key) {
        if (c != ' ' && uniqueChars.find(c) == string::npos) {
            if (c == 'J') {
                uniqueChars += 'I';
            } else {
                uniqueChars += c;
            }
        }
    }

    int row = 0, col = 0;

    // Fill the matrix with the unique characters
    for (char c : uniqueChars) {
        matrix[row][col] = c;
        col++;
        if (col == 5) {
            col = 0;
            row++;
        }
    }

    // Fill the remaining empty cells with the alphabet (except 'J')
    char ch = 'A';
    while (row < 5) {
        while (col < 5) {
            if (uniqueChars.find(ch) == string::npos) {
                matrix[row][col] = ch;
                col++;
            }
            ch++;
        }
        col = 0;
        row++;
    }

    return matrix;
}

// Function to encrypt a pair of characters using the Playfair matrix
string encryptPair(vector<vector<char>> matrix, char a, char b) {
    int row1, col1, row2, col2;

    // Find the positions of characters 'a' and 'b' in the matrix
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            if (matrix[i][j] == a) {
                row1 = i;
                col1 = j;
            }
            if (matrix[i][j] == b) {
                row2 = i;
                col2 = j;
            }
        }
    }

    string encryptedPair = "";

    // Case 1: Same row
    if (row1 == row2) {
        encryptedPair += matrix[row1][(col1 + 1) % 5];
        encryptedPair += matrix[row2][(col2 + 1) % 5];
    }
    // Case 2: Same column
    else if (col1 == col2) {
        encryptedPair += matrix[(row1 + 1) % 5][col1];
        encryptedPair += matrix[(row2 + 1) % 5][col2];
    }
    // Case 3: Rectangle
    else {
        encryptedPair += matrix[row1][col2];
        encryptedPair += matrix[row2][col1];
    }

    return encryptedPair;
}

// Function to encrypt plaintext using the Playfair cipher
string playfairEncrypt(string plaintext, vector<vector<char>> matrix) {
    string encryptedText = "";
    int length = plaintext.length();

    for (int i = 0; i < length; i += 2) {
        char a = plaintext[i];
        char b = (i + 1 < length) ? plaintext[i + 1] : 'X'; // Append 'X' if plaintext has odd length

        if (a == b) {
            b = 'X';
            i--; // Repeat the same character
        }

        encryptedText += encryptPair(matrix, a, b);
    }

    return encryptedText;
}

int main() {
    string key, plaintext;

    // Input the key and plaintext
    cout << "Enter the key (no spaces, all uppercase): ";
    cin >> key;
    cout << "Enter the plaintext (uppercase letters only): ";
    cin >> plaintext;

    // Remove spaces and convert to uppercase
    for (char &c : key) {
        if (c == 'J') {
            c = 'I'; // Replace 'J' with 'I'
        }
        c = toupper(c);
    }
    for (char &c : plaintext) {
        if (c == 'J') {
            c = 'I'; // Replace 'J' with 'I'
        }
        c = toupper(c);
    }

    // Prepare the Playfair matrix
    vector<vector<char>> matrix = prepareMatrix(key);

    // Encrypt the plaintext
    string ciphertext = playfairEncrypt(plaintext, matrix);

    // Output the encrypted text
    cout << "Encrypted Text: " << ciphertext << endl;

    return 0;
}
