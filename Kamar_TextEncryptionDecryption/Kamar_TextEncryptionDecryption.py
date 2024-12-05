from cryptography.fernet import Fernet # type: ignore
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC # type: ignore
from cryptography.hazmat.primitives import hashes  # type: ignore
from cryptography.hazmat.backends import default_backend   # type: ignore
import base64 
import os


def read_file_content(file_path):
#this will allow the user to supply a file path and read its content
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def write_to_file(file_path, content):
#this will allow the user to write the content to a file and create a file if the file path does not exist 
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True) 

        with open(file_path, 'w') as file:
            file.write(content)
            file.close()
    except Exception as e:
        print(f"Error writing to file: {e}")

def Generate_Key32_Length(key: str):
#this will generate a key from a user given string
   kdf = PBKDF2HMAC( 
       algorithm=hashes.SHA256(),
      length=32,
      salt=b'', 
      iterations=100000,
     backend=default_backend() ) 
   key = base64.urlsafe_b64encode(kdf.derive(key.encode())) 
   return key

def encrypt_text(text, key):
#this will encrypt the text by the given key
    fernet = Fernet(key)
    encoded_message = text.encode() 
    encrypted_message = fernet.encrypt(encoded_message) 
    return encrypted_message.decode()

def decrypt_text(text, key):
#this will decrypt the encrypted text by the given key
    fernet = Fernet(key)

    try: 
        decrypted_message = fernet.decrypt(text.encode('utf-8'))
        print(f"Decrypted message: {decrypted_message.decode()}") 
    except Exception as e:
        print(f"Decryption failed: {e}")
    return decrypted_message.decode()


if __name__ == "__main__":
    process = input("please enter 1 for encryption or 2 for decryption: ")
    while(process != "1" and process != "2"):
        print("sorry you can only input 1 or 2")
        process = input("please enter 1 for encryption or 2 for decryption: ")
    if(process == "1"):
        choice = input("please enter 1 if you want to input the text or 2 if you want to supply a file path: ")
        while(choice != "1" and choice != "2"):
            print("sorry you can only input 1 or 2")
            choice = input("please enter 1 if you want to input the text or 2 if you want to supply a file path: ")
        if(choice == "1"):
            text = input("please enter a text to encrypt: ")
            key = input("please enter a key value for encryption: ")
        elif(choice == "2"):
            file_path = input("please enter a file path for the text to encrypt: ")
            text = read_file_content(file_path)
            key = input("please enter a key value for encryption: ")

        key32 = Generate_Key32_Length(key)

        encrypted_text = encrypt_text(text, key32)

        save_result = input("do you want to save the message to a file yes/no? ")

        while (save_result != "yes" and save_result != "no"):
            print("only yes or no")
            save_result = input("do you want to save the message to a file yes/no? ")
        if(save_result == "yes"):
            File_path_to_save = input("please enter the file path to save the encrypted message: ")
            write_to_file(File_path_to_save, encrypted_text)
        print("the encrypted text is : " + encrypted_text)
    elif(process == "2"):
        choice = input("please enter 1 if you want to input the text or 2 if you want to supply a file path: ")
        while(choice != "1" and choice != "2"):
            print("sorry you can only input 1 or 2")
            choice = input("please enter 1 if you want to input the text or 2 if you want to supply a file path: ")
        if(choice == "1"):
            text = input("please enter a text to decrypt: ")
            key = input("please enter a key value for decryption: ")
        elif(choice == "2"):
            file_path = input("please enter a file path for the text to decrypt: ")
            text = read_file_content(file_path)
            key = input("please enter a key value for decryption: ")

        key32 = Generate_Key32_Length(key)

        decrypted_text = decrypt_text(text, key32)
        print("the decrypted text is: " ,decrypted_text)

