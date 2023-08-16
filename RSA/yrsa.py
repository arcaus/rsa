import yaml
import rsa


def generateKeys():
    (publicKey, privateKey) = rsa.newkeys(2048)
    with open('keys/publicKey.pem', 'wb') as p:
        p.write(publicKey.save_pkcs1('PEM'))
    with open('keys/privateKey.pem', 'wb') as p:
        p.write(privateKey.save_pkcs1('PEM'))


def loadKeys():
    with open('keys/publicKey.pem', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open('keys/privateKey.pem', 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return privateKey, publicKey


def encrypt(plaintext, key):
    return rsa.encrypt(plaintext.encode(), key)


def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode()
    except:
        return False


def sign(plaintext, key):
    return rsa.sign(plaintext.encode(), key, 'SHA-256')


def verify(plaintext, signature, key):
    try:
        return rsa.verify(plaintext.encode(), signature, key, ) == 'SHA-256'
    except:
        return False


def main():
    while True:
        print("Operation Modes:\n1. Encrypt and Sign\n2. Decrypt and Verify\n3. Exit")
        choice = input('Choice: ')

        if choice == '1':
            path = input('Enter path to plaintext file: ')
            with open(path, 'r') as p:
                plaintext = p.read()

            generateKeys()
            privateKey, publicKey = loadKeys()
            ciphertext = encrypt(plaintext, publicKey)
            signature = sign(plaintext, privateKey)
            with open('ciphertext.txt', 'w') as f:
                yaml.dump({'Ciphertext': ciphertext, '\nSignature': signature}, f)

            print('File encrypted and stored in ciphertext.txt\n')

        elif choice == '2':
            try:
                path = input('Enter path to ciphertext file: ')
                with open(path, 'r') as f:
                    data = yaml.load(f, Loader=yaml.FullLoader)
                    ciphertext = data['Ciphertext']
                    signature = data['\nSignature']
                privateKey, publicKey = loadKeys()

                plaintext = decrypt(ciphertext, privateKey)
                verification = verify(plaintext, signature, publicKey)
                if plaintext and verification:
                    print('\nSuccessfully decrypted and stored in secret.txt\n')
                    with open('secret.txt', 'w') as s:
                        s.write('=============== SIGNATURE VERIFIED ===============\n')
                        s.write(plaintext)
                        s.write('\n=============== SIGNATURE VERIFIED ===============')
                else:
                    print('\nDecryption failed.\n')

            except FileNotFoundError:
                print('No encrypted data found.\n')

        elif choice == '3' or choice.lower() == 'exit':
            print('Thank you for using this program. Goodbye!')
            break

        else:
            print('Invalid choice.\n')


if __name__ == "__main__":
    main()
