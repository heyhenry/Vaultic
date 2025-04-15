<p align="center">
    <img src="img/main_logo.png" width="250">
</p>
<h1 align="center"><b>Vaultic</b></h1>
<h3 align="center">A light-weight, local and secure minty-fresh password manager built with a Tkinter-Based GUI.</h3>

<p align="center" >
  <a href="#technology-stack">Tech Stack</a> &bull; <a href="#features">Features</a> &bull; <a href="#how-secure-is-my-data">Security</a> &bull; <a href="#%EF%B8%8F-vaultic-trello-board-%EF%B8%8F">Trello Board</a> &bull; <a href="#-key-snapshots">Snapshots</a> &bull; <a href="#resources">Resources</a> &bull; <a href="#future-features">Future Features</a> &bull; <a href="#how-do-i-use-it">Installation</a> &bull; <a href="#license">License</a> &bull; <a href="#author">Author</a>
</p>

<h2 align="center">Technology Stack</h2>
<p align="center">
    <a href="https://github.com/heyhenry/Vaultic/blob/main/LICENSE" alt="License: MIT"><img src="https://img.shields.io/badge/License-MIT-lightgrey"></a>
    <a href="https://www.python.org/" alt="Programming Language: Python"><img src="https://img.shields.io/badge/Python-3.12.2-blue"></a>
    <a href="https://github.com/israel-dryer/ttkbootstrap" alt="Tkinter: ttkbootstrap"><img src="https://img.shields.io/badge/ttkbootstrap-styled%20Tkinter-%236f42c1"></a>
    <a href="https://sqlite.org/" alt="Database: SQLite"><img src="https://img.shields.io/badge/SQLite-DB-%2320c997"></a>
</p>

<p align="center">
  <a href="https://github.com/heyhenry/Vaultic/releases/download/v1.0.0-vaultic/Vaultic_v1.0.0.zip"><img src="img/combo_download_logo.png" width="250"></a>
</p>

## Features
- User registration and login system
- Password encryption
- Add, edit and delete saved credentials
- Modern UI and fresh aesthetic with ttkbootstrap
- Multi-page navigation (Register, Login, Home, Edit Account Info, New Entry)
- Multi-level on-demand password generation following NIST guidelines

## How secure is my data?
<p>Vaultic uses <a href="https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html">Argon2id</a> (<a href="https://tuta.com/blog/best-encryption-with-kdf">winner of the 2013-2015 Password Hashing Competition</a>), to hash your master password and derive the encryption key for your data. When you're logged out, your data is fully encrypted - the SQLite database is dumped and encrypted using <a href="https://cryptography.io/en/latest/fernet/">Fernet symmetric encryption</a>. On successful login, the encryption key is regenerated using your master password and a uniquely randomised salt. In addition, the SQLite database is stored locally on your device, minimising your digital footprint and reducing exposure to online threats.</p>

<h2>🗂️ <a href="https://trello.com/b/lMPEAwc6/vaultic">Vaultic Trello Board</a> 🗂️</h2>

### 🌟 Key Snapshots

#### 🖊️ Register 
[![Register](img/snapshots/register.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/register.png)

#### 🏁 Login 
[![Login](img/snapshots/login_masked.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/login_masked.png)

#### 🏠 Home
[![Home](img/snapshots/home.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/home.png)

#### 📜 Home - Account Details Display
[![Account Details](img/snapshots/account_details.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/account_details.png)

#### ➕ Add New Account Entry
[![New Entry](img/snapshots/empty_new_entry.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/empty_new_entry.png)

#### ✏️ Edit Account Info
[![Edit Account Info](img/snapshots/edit_account_info.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/edit_account_info.png)

#### 🔔 Login - Startup Notification
[![Toast](img/snapshots/toast_login.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/toast_login.png)

---

<details>
  <summary>📸 Full Snapshot Gallery (Click to expand)</summary>

### 🖊️ Register 
[![Register](img/snapshots/register.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/register.png)

### 🖊️ Register - Error State - Mismatch
[![Register Error Mismatch](img/snapshots/error_register_mismatch.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/error_register_mismatch.png)

### 🖊️ Register - Error State - Whitespaces Only
[![Register Error Whitespaces Only](img/snapshots/error_register_whitespace.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/error_register_whitespace.png)

### 🖊️ Register - Error State - Minimum Length
[![Register Error Minimum Length](img/snapshots/error_register_length.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/error_register_length.png)

### 🖊️ Register - Error State - Empty Input
[![Register Error Empty Input](img/snapshots/error_register_empty.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/error_register_empty.png)

### 🔐 Login - Masked
[![Login Masked](img/snapshots/login_masked.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/login_masked.png)

### 🔐 Login - Unmasked
[![Login Unmasked](img/snapshots/login_unmasked.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/login_unmasked.png)

### 🔐 Login - Startup Notification
[![Login Startup Notification](img/snapshots/toast_login.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/toast_login.png)

### 🔐 Login - Error State
[![Login Error](img/snapshots/error_login.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/error_login.png)

### 🏠 Home - Populated
[![Home Populated](img/snapshots/home.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/home.png)

### 🏠 Home - Account Details Display
[![Home Account Details](img/snapshots/account_details.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/account_details.png)

### 🏠 Home - Copied Username 
[![Home Username](img/snapshots/toast_home.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/toast_home.png)

### ➕ New Account Entry
[![New Entry](img/snapshots/empty_new_entry.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/empty_new_entry.png)

### ➕ New Account Entry - Error State
[![New Entry Error](img/snapshots/error_new_entry.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/error_new_entry.png)

### ✏️ Edit Account Info
[![Edit Account Info](img/snapshots/edit_account_info.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/edit_account_info.png)

### ✏️ Edit Account Info - Error State
[![Edit Account Info Error](img/snapshots/error_edit_account_info.png)](https://raw.githubusercontent.com/heyhenry/Vaultic/128a47c14d6bc4e7dbb7153af3d2db738f2ace22/img/snapshots/error_edit_account_info.png)

</details>

## Resources
<p>📚 <a href="https://github.com/heyhenry/Vaultic/blob/main/resources.md" target="_blank">Resources I used for Vaultic</a> 📚</p>

## Future Features
- Dark Theme (Likely Darkly from ttkbootstrap)
> Suggestions are welcomed via email.

## How Do I Use It?
1. Download the zip folder (Vaultic_v1.0.1.zip) via the download icons at the top of this file or here <a href="https://github.com/heyhenry/Vaultic/releases/download/v1.0.1-vaultic/Vaultic_v1.0.1.zip">📥</a>.
2. Extract the contents from the zip folder.
3. Refer to readme.txt for detailed usage instructions and setup guidance.
4. Enjoy!

> Note: It is best to not alter or remove any files as it may affect the function of the application.

## License
Vaultic is licensed under <a href="https://tlo.mit.edu/understand-ip/exploring-mit-open-source-license-comprehensive-guide">MIT</a>, so feel free to use, modify, share the software however you want. You can even distribute it, aslong as you adhere to the condition of including the original copyright and permission notices in all copies or substantial portions of the Software. See <a href="https://github.com/heyhenry/Vaultic/blob/main/LICENSE">here</a> for the attached official license for Vaultic.

## Author
> Built with ❤️ by [Henry Han](https://github.com/heyhenry)