# RSA Encryption and Decryption Program

A simple program for RSA encryption, decryption, and signature generation.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Encrypting a File](#encrypting-a-file)
  - [Decrypting a File](#decrypting-a-file)
- [Contributing](#contributing)
- [License](#license)

## Features

- Generate RSA key pairs for encryption and decryption.
- Encrypt files using the recipient's public key.
- Decrypt files using the recipient's private key.
- Generate digital signatures for files using the sender's private key.
- Verify digital signatures using the sender's public key.

## Getting Started

### Prerequisites

- Python 3.6 or above
- RSA, Pickle

### Installation

1. Clone the repository:
```shell
$ git clone https://github.com/arcaus/rsa.git
$ cd rsa
```
2. Install the required libraries:
  ```shell
  pip install rsa
  pip install pickle
  ```

## Usage

### Encrypting a File
1. Run the script and choose the encryption option.
2. Enter the path of the file you want to encrypt.
3. A new ciphertext.pkl file has been generated with the encrypted data and the signature.

### Decrypting a File
1. Run the script and choose the decryption option.
2. Enter the path of the file (ciphertext.pkl) you want to decrypt.
3. You should receive the plaintext along with the verification status.

## Contributing
Contributions are welcome! Here's how you can contribute:

1. Fork the repository.
2. Create a new branch for your feature/bugfix: git checkout -b feature-name
3. Commit your changes: git commit -m 'Add some feature'
4. Push to the branch: git push origin feature-name
5. Create a pull request.

Please ensure your pull request follows the project's coding conventions and style.

## License
This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it according to the terms of the license.
