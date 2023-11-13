package main

import (
	"bufio"
	"bytes"
	"crypto"
	"crypto/aes"
	"crypto/cipher"
	crytpRand "crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/x509"
	"encoding/json"
	"encoding/pem"
	"fmt"
	"io"
	"net/http"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"
)

type DesktopCreds struct {
	SymKey      []byte
	ServerPub   *rsa.PublicKey
	Username    string
	Ttl         time.Time
	DesktopPub  *rsa.PublicKey
	DesktopPriv *rsa.PrivateKey
}

type Input struct {
	Operation       string
	AccountUsername string
	AccountPassword string
	SiteUsername    string
	SitePassword    string
	Description     string
	Err             string
	DocID           string
}

type SendServer struct {
	SecretSym       []byte
	Msg             []byte
	AccountUsername string
	AccountPassword []byte
	Description     string
	Hash            []byte
	DesktopPub      *rsa.PublicKey
	SecretMsg       []byte
	SiteUsername    []byte
	SitePassword    []byte
	DocID           string
}

type ServerResponse struct {
	SecretMsg    []byte
	Msg          []byte
	SecretSym    []byte
	Status       string
	SiteUsername []byte
	SitePassword []byte
}

type AllPasswords struct {
	DocID       string `bson:"DocID"`
	Description string `bson:"Description"`
}

func main() {
	createKeyAndSave()
	C := DesktopCreds{
		[]byte{}, //32
		extractPubKey(pwd() + "/serverPublic.pem"),
		"",
		time.Now(),
		extractPubKey(pwd() + "/desktopPublic.pem"),
		extractPrivKey(pwd() + "/desktopPrivate.pem"),
	}
	welcomePage()
	var input Input
	var command string
	for {
		command = readUserInput()
		parseInput(&input, command)
		if input.Operation == "signup" {
			if C.Username != "" {
				fmt.Println("Already logged in please exit first")
				continue
			}
			signup(&C, input)
		}
		if input.Operation == "exit" {
			gracefulExit(&C)
		}
		if input.Operation == "testRSA" {
			testRSAConnection()
		}
		if input.Operation == "ping" {
			testConnection()
		}
		if input.Operation == "login" {
			if C.Username != "" {
				fmt.Println("Already logged in")
				continue
			}
			login(&C, input)
		}
		if input.Operation == "new" {
			createPasswordEntry(&C, input)
		}
		if input.Operation == "getall" {
			getAllEntries(&C)
		}
		if input.Operation == "getone" {
			getOnePassword(&C, input)
		}
		if input.Operation == "update" {
			updatePassword(&C, input)
		}
		if input.Operation == "delete" {
			deletePassword(&C, input)
		}
	}
}

func createKeyAndSave() {
	privatekey, err := rsa.GenerateKey(crytpRand.Reader, 2048)
	if err != nil {
		fmt.Printf("Cannot generate RSA key\n")
		os.Exit(1)
	}
	fmt.Printf("generating RSA key\n")
	publickey := &privatekey.PublicKey
	var privateKeyBytes []byte = x509.MarshalPKCS1PrivateKey(privatekey)
	privateKeyBlock := &pem.Block{
		Type:  "RSA PRIVATE KEY",
		Bytes: privateKeyBytes,
	}
	privatePem, err := os.Create("desktopPrivate.pem")
	if err != nil {
		fmt.Printf("error when create userPrivate.pem: %s \n", err)
		os.Exit(1)
	}
	err = pem.Encode(privatePem, privateKeyBlock)
	if err != nil {
		fmt.Printf("error when encode Private pem: %s \n", err)
		os.Exit(1)
	}
	publicKeyBytes, err := x509.MarshalPKIXPublicKey(publickey)
	if err != nil {
		fmt.Printf("error when dumping publickey: %s \n", err)
		os.Exit(1)
	}
	publicKeyBlock := &pem.Block{
		Type:  "RSA PUBLIC KEY",
		Bytes: publicKeyBytes,
	}
	publicPem, err := os.Create("desktopPublic.pem")
	if err != nil {
		fmt.Printf("error when create public.pem: %s \n", err)
		os.Exit(1)
	}
	err = pem.Encode(publicPem, publicKeyBlock)
	if err != nil {
		fmt.Printf("error when encode public pem: %s \n", err)
		os.Exit(1)
	}
}

func decryptRSA(encryptedBytes []byte, privateKey *rsa.PrivateKey) []byte {
	decryptedBytes, err := privateKey.Decrypt(nil, encryptedBytes, &rsa.OAEPOptions{Hash: crypto.SHA256})
	if err != nil {
		panic(err)
	}
	return decryptedBytes
}

func encryptRSA(publicKey *rsa.PublicKey, payload []byte) []byte {
	encryptedBytes, err := rsa.EncryptOAEP(
		sha256.New(),
		crytpRand.Reader,
		publicKey,
		payload,
		nil)
	if err != nil {
		panic(err)
	}
	return encryptedBytes
}

func encryptAES(text, key []byte) []byte {
	c, err := aes.NewCipher(key)

	if err != nil {
		fmt.Println(err)
	}
	gcm, err := cipher.NewGCM(c)
	if err != nil {
		fmt.Println(err)
	}
	nonce := make([]byte, gcm.NonceSize())
	if _, err = io.ReadFull(crytpRand.Reader, nonce); err != nil {
		fmt.Println(err)
	}
	return gcm.Seal(nonce, nonce, text, nil)
}

func decryptAES(key, ciphertext []byte) string {
	c, err := aes.NewCipher(key)
	if err != nil {
		fmt.Println(err)
	}
	gcm, err := cipher.NewGCM(c)
	if err != nil {
		fmt.Println(err)
	}
	nonceSize := gcm.NonceSize()
	if len(ciphertext) < nonceSize {
		fmt.Println(err)
	}
	nonce, ciphertext := ciphertext[:nonceSize], ciphertext[nonceSize:]
	plaintext, err := gcm.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		fmt.Println(err)
	}
	return string(plaintext)
}

func extractPubKey(location string) *rsa.PublicKey {
	key, err := os.ReadFile(location)
	if err != nil {
		fmt.Println(err)
	}
	pemBlock, _ := pem.Decode(key)
	parseResult, _ := x509.ParsePKIXPublicKey(pemBlock.Bytes)
	return parseResult.(*rsa.PublicKey)
}

func extractPrivKey(location string) *rsa.PrivateKey {
	key, err := os.ReadFile(location)
	if err != nil {
		fmt.Println(err)
	}
	pemBlock, _ := pem.Decode(key)
	parseResult, _ := x509.ParsePKCS1PrivateKey(pemBlock.Bytes)
	return parseResult
}

func post(data []byte, httpposturl string) []byte {
	request, _ := http.NewRequest("POST", httpposturl, bytes.NewBuffer(data))
	request.Header.Set("Content-Type", "application/json; charset=UTF-8")

	client := &http.Client{}
	response, error := client.Do(request)
	if error != nil {
		panic(error)
	}
	defer response.Body.Close()
	body, _ := io.ReadAll(response.Body)
	return body
}

func readUserInput() string {
	fmt.Print("::::: ")
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan() // use `for scanner.Scan()` to keep reading
	line := scanner.Text()
	return line
}

func parseInput(input *Input, command string) {
	split := strings.Split(command, " ")
	if split[0] == "signup" {
		input.Operation = "signup"
		input.AccountUsername = ""
		input.AccountPassword = ""
		return
	}
	if split[0] == "test" {
		input.Operation = "test"
		return
	}
	if split[0] == "getall" {
		input.Operation = "getall"
		return
	}
	if split[0] == "exit" {
		input.Operation = "exit"
		return
	}
	if split[0] == "testRSA" {
		input.Operation = "testRSA"
		return
	}
	if split[0] == "getone" {
		input.Operation = "getone"
		input.DocID = split[1]
		return
	}
	if split[0] == "ping" {
		input.Operation = "ping"
		return
	}
	if split[0] == "new" {
		input.Operation = "new"
		input.SiteUsername = split[1]
		input.SitePassword = split[2]
		input.Description = split[3]
		return
	}
	if split[0] == "login" {
		if len(split) != 3 {
			fmt.Println("Format: login username password")
			return
		}
		input.Operation = "login"
		input.AccountUsername = split[1]
		input.AccountPassword = split[2]
		return
	}
	if split[0] == "update" {
		input.Operation = "update"
		input.DocID = split[1]
		if len(split) == 4 {
			input.SiteUsername = split[2]
			input.SitePassword = split[3]
		} else {
			input.SitePassword = split[2]
		}
		return
	}
	if split[0] == "delete" {
		input.Operation = "delete"
		input.DocID = split[1]
		return
	}
	fmt.Println("Not a command")
}

func pwd() string {
	mydir, err := os.Getwd()
	if err != nil {
		fmt.Println(err)
	}
	return mydir
}

func welcomePage() {
	fmt.Println("Welcome to password manager")
}

func testRSAConnection() {
	C := DesktopCreds{
		[]byte{}, //32
		extractPubKey(pwd() + "/serverPublic.pem"),
		"",
		time.Now(),
		extractPubKey(pwd() + "/desktopPublic.pem"),
		extractPrivKey(pwd() + "/desktopPrivate.pem"),
	}
	var send SendServer
	send.SecretMsg = encryptRSA(C.ServerPub, []byte("Hello"))
	send.DesktopPub = C.DesktopPub
	jsonData, _ := json.Marshal(send)
	response := post(jsonData, "http://localhost:8000/testRSAConnection")
	var serverRes ServerResponse
	json.Unmarshal(response, &serverRes)
	res := decryptRSA(serverRes.SecretMsg, C.DesktopPriv)
	fmt.Println(string(res))
}

func testConnection() {
	C := DesktopCreds{
		[]byte{}, //32
		extractPubKey(pwd() + "/serverPublic.pem"),
		"",
		time.Now(),
		extractPubKey(pwd() + "/desktopPublic.pem"),
		extractPrivKey(pwd() + "/desktopPrivate.pem"),
	}
	var send SendServer
	send.DesktopPub = C.DesktopPub
	jsonData, _ := json.Marshal(send)
	response := post(jsonData, "http://localhost:8000/askForSym")
	var serverRes ServerResponse
	json.Unmarshal(response, &serverRes)
	C.SymKey = decryptRSA(serverRes.SecretSym, C.DesktopPriv)
	var testPrint SendServer
	testPrint.Hash = encryptAES([]byte("Connection"), C.SymKey)
	jsonData, _ = json.Marshal(testPrint)
	response = post(jsonData, "http://localhost:8000/checkAESConnection")
	var encrypted ServerResponse
	json.Unmarshal(response, &encrypted)
	rawMsg := decryptAES(C.SymKey, encrypted.Msg)
	fmt.Println(rawMsg)
}

func signup(C *DesktopCreds, input Input) {
	uniqueUsername := ""
	for uniqueUsername == "" {
		fmt.Println("*********\nProvide a username")
		var send SendServer
		send.AccountUsername = readUserInput()
		if send.AccountUsername == "exit" {
			os.Exit(0)
		}
		jsonData, _ := json.Marshal(send)
		resp := post(jsonData, "http://localhost:8000/checkIfUsernameAvailable")
		var serverRes ServerResponse
		json.Unmarshal(resp, &serverRes)
		fmt.Println(string(serverRes.Msg))
		if serverRes.Status == "success" {
			uniqueUsername = send.AccountUsername
		}
	}
	var send SendServer
	send.AccountUsername = uniqueUsername
	fmt.Println("*********\nProvide a secure password") //add validity checks
	userinput := readUserInput()
	if len(userinput) < 1 {
		fmt.Println("Password is too short")
		return
	}
	send.AccountPassword = encryptRSA(C.ServerPub, []byte(userinput))
	jsonData, _ := json.Marshal(send)
	response := post(jsonData, "http://localhost:8000/signup")
	var resp ServerResponse
	json.Unmarshal(response, &resp)
	fmt.Println(string(resp.Msg))
}

func login(C *DesktopCreds, input Input) {
	var send SendServer
	send.AccountUsername = input.AccountUsername
	send.AccountPassword = encryptRSA(C.ServerPub, []byte(input.AccountPassword))
	send.DesktopPub = C.DesktopPub
	jsonData, _ := json.Marshal(send)
	resp := post(jsonData, "http://localhost:8000/login")
	var serverRes ServerResponse
	json.Unmarshal(resp, &serverRes)
	if serverRes.Status == "Authenticated" {
		C.Ttl = time.Now().Add(time.Minute * 20)
		C.Username = input.AccountUsername
		C.SymKey = decryptRSA(serverRes.SecretSym, C.DesktopPriv)
		fmt.Println("Logged in")
	} else {
		fmt.Println("Not logged in")
	}
}

func createPasswordEntry(C *DesktopCreds, input Input) {
	checkttl(C)
	var send SendServer
	send.SiteUsername = encryptAES([]byte(input.SiteUsername), C.SymKey)
	send.SitePassword = encryptAES([]byte(input.SitePassword), C.SymKey)
	send.Description = input.Description
	send.AccountUsername = C.Username
	jsonData, _ := json.Marshal(send)
	resp := post(jsonData, "http://localhost:8000/createPasswordEntry")
	var serverRes ServerResponse
	json.Unmarshal(resp, &serverRes)
	fmt.Println(serverRes.Status)
}

func getAllEntries(C *DesktopCreds) {
	checkttl(C)
	var send SendServer
	send.AccountUsername = C.Username
	jsonData, _ := json.Marshal(send)
	resp := post(jsonData, "http://localhost:8000/getAllPasswords")
	var passes []AllPasswords
	json.Unmarshal(resp, &passes)
	sort.Slice(passes, func(i, j int) bool {
		num1, _ := strconv.Atoi(passes[i].DocID)
		num2, _ := strconv.Atoi(passes[j].DocID)
		return num1 < num2
	})
	fmt.Println("DocID			Description")
	for i := 0; i < len(passes); i++ {
		fmt.Println(passes[i].DocID + "\t\t\t" + passes[i].Description)
	}
}

func getOnePassword(C *DesktopCreds, input Input) {
	checkttl(C)
	var send SendServer
	send.DocID = input.DocID
	send.AccountUsername = C.Username
	jsonData, _ := json.Marshal(send)
	resp := post(jsonData, "http://localhost:8000/getOnePassword")
	var response ServerResponse
	json.Unmarshal(resp, &response)
	username := decryptAES(C.SymKey, response.SiteUsername)
	password := decryptAES(C.SymKey, response.SitePassword)
	fmt.Println(username + "\t" + password + "\t" + string(response.Msg))
}

func updatePassword(C *DesktopCreds, input Input) {
	checkttl(C)
	var send SendServer
	send.DocID = input.DocID
	send.AccountUsername = C.Username
	if input.SiteUsername != "" {
		send.SiteUsername = encryptAES([]byte(input.SiteUsername), C.SymKey)
	}
	if input.SitePassword != "" {
		send.SitePassword = encryptAES([]byte(input.SitePassword), C.SymKey)
	}
	if input.Description != "" {
		send.Description = input.Description
	}
	jsonData, _ := json.Marshal(send)
	resp := post(jsonData, "http://localhost:8000/updatePassword")
	var response ServerResponse
	json.Unmarshal(resp, &response)
	fmt.Println(string(response.Msg))
}

func deletePassword(C *DesktopCreds, input Input) {
	checkttl(C)
	var send SendServer
	send.DocID = input.DocID
	send.AccountUsername = C.Username
	jsonData, _ := json.Marshal(send)
	resp := post(jsonData, "http://localhost:8000/deletePassword")
	var response ServerResponse
	json.Unmarshal(resp, &response)
	fmt.Println(string(response.Msg))
}

func checkttl(C *DesktopCreds) {
	if C.Username == "" {
		fmt.Println("Attempting to access authorized route without logging in.")
	}
	if C.Ttl != time.Now() {
		return
	}
	gracefulExit(C)
}

func gracefulExit(C *DesktopCreds) {
	C.ServerPub = nil
	var send SendServer
	send.AccountUsername = C.Username
	send.SecretSym = C.SymKey
	C.SymKey = nil
	C.Username = ""
	jsonData, _ := json.Marshal(send)
	resp := post(jsonData, "http://localhost:8000/clearSymMap")
	var serverRes ServerResponse
	json.Unmarshal(resp, &serverRes)
	fmt.Println(serverRes.Status)
	os.Exit(0)
}
