#include <bits/stdc++.h>
using namespace std;

string encryptSimpleColumnTransposition(const string& plainText, const string& key) {
    string encryptedText;
    int keyLength = key.length();
    int textLength = plainText.length();
    int numRows = (textLength + keyLength - 1) / keyLength;

    char matrix[numRows][keyLength];

    int index = 0;
    for (int i = 0; i < numRows; i++) {
        for (int j = 0; j < keyLength; j++) {
            if (index < textLength) {
                matrix[i][j] = plainText[index++];
            } else {
                matrix[i][j] = ' ';
            }
        }
    }

    string sortedKey = key;
    sort(sortedKey.begin(), sortedKey.end());

    int permutationIndex[keyLength];
    for (int i = 0; i < keyLength; i++) {
        permutationIndex[i] = key.find(sortedKey[i]);
    }

    for (int i = 0; i < keyLength; i++) {
        for (int j = 0; j < numRows; j++) {
            encryptedText += matrix[j][permutationIndex[i]];
        }
    }

    return encryptedText;
}

string decryptSimpleColumnTransposition(const string& encryptedText, const string& key) {
    string decryptedText;
    int keyLength = key.length();
    int textLength = encryptedText.length();
    int numRows = (textLength + keyLength - 1) / keyLength;

    char matrix[numRows][keyLength];

    string sortedKey = key;
    sort(sortedKey.begin(), sortedKey.end());

    int permutationIndex[keyLength];
    for (int i = 0; i < keyLength; i++) {
        permutationIndex[i] = key.find(sortedKey[i]);
    }

    int index = 0;
    for (int i = 0; i < keyLength; i++) {
        for (int j = 0; j < numRows; j++) {
            matrix[j][permutationIndex[i]] = encryptedText[index++];
        }
    }

    for (int i = 0; i < numRows; i++) {
        for (int j = 0; j < keyLength; j++) {
            decryptedText += matrix[i][j];
        }
    }

    return decryptedText;
}

int main() {
    string plainText;
    string key;

    cout << "Enter the plain text: ";
    getline(cin, plainText);

    cout << "Enter the key: ";
    getline(cin, key);

    string encryptedText = encryptSimpleColumnTransposition(plainText, key);
    cout << "Encrypted Text: " << encryptedText << endl;

    string decryptedText = decryptSimpleColumnTransposition(encryptedText, key);
    cout << "Decrypted Text: " << decryptedText << endl;

    return 0;
}

