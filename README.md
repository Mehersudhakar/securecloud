# Secure File Transfer Using Hybrid Cryptography

**Published Paper**: [Click here to read the research paper](https://ijream.org/papers/IJREAMV08I1195010.pdf)

This project focuses on **secure file transfer** using a hybrid cryptographic system. By combining various encryption techniques such as **AES**, **DES**, **RSA**, and **LSB steganography**, it ensures safe storage and transmission of sensitive data over the cloud. The main purpose is to enhance security by applying multiple layers of encryption and using steganography to hide the encryption keys within images.

## Overview

Cloud computing provides immense storage and computing capabilities but poses significant security risks, especially with sensitive information stored offsite. To address this, the project employs hybrid cryptography, where files are encrypted using three different algorithms and the keys are concealed using **LSB steganography**. This way, even if one security layer is compromised, attackers still cannot access the full data or keys.

### Key Features:
- **Hybrid Encryption**: Utilizes AES, DES, and RSA algorithms to encrypt different parts of the file.
- **LSB Steganography**: Hides encryption keys within images for added security.
- **User & Owner Roles**: Owners can upload and split files, while users request access and decrypt files using provided keys.

## How to Run the Application

Below are the steps to set up and run the secure file transfer application.

### Prerequisites
- **Python 3.7 or higher**
- **Anaconda** (recommended for environment management)
- **SQLite** for managing the database

### Steps to Run the Application

1. **Open Anaconda Prompt**:
   - First, search and open the "Anaconda Prompt" from your system's search bar.

2. **Navigate to the Project Directory**:
   - Change the directory to the project folder by typing:
     ```bash
     cd Hybride_Cryptography
     ```

3. **Activate the Environment**:
   - Activate the required environment (assumed named `tf`):
     ```bash
     conda activate tf
     ```

4. **Run the Application**:
   - To start the application, type the following:
     ```bash
     python app.py
     ```

5. **Access the Application in Browser**:
   - After running the above command, you will receive an IP address in the terminal.
   - Copy this IP and paste it in your browser's address bar (Google Chrome recommended).
   - The application will open as a web interface where you can interact with the system.

6. **Database Management**:
   - For database management, you can use **DB Browser for SQLite** to view or modify the database tables.
   - This tool is useful for checking user registration and uploaded files.

### Key Functionalities:
- **User Registration**: New users can register through the web interface.
- **File Upload**: Owners can upload files, but ensure the file has a unique name each time to avoid conflicts.
- **File Encryption**: Files are encrypted using AES, DES, and RSA algorithms.
- **File Splitting**: Once uploaded, the files are split into three parts, with each part encrypted separately.
- **Key Management**: The keys generated during encryption are stored inside an image using LSB steganography.
- **Access Requests**: Users can request access to files, and owners can approve requests and share the keys.
- **Decryption**: Users can decrypt files using the keys provided by the owner.

### Important Notes:
- Once the encryption keys are generated, **do not click "Split" again**. This may cause errors in managing the keys.
- Always upload files with **new names** to prevent overwriting previously uploaded files.

---

## Conclusion

This project demonstrates a secure file transfer method using hybrid cryptography and steganography. By employing multiple encryption algorithms and concealing the keys within images, it ensures high security for sensitive data, making it very difficult for unauthorized users to access. The combination of encryption and steganography significantly strengthens the overall security system.
