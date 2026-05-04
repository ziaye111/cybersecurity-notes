# Cryptography: The "Explain It Like I'm 5" Guide

Do not be the person in an interview who calls Base64 "encryption." Here is the actual difference between the three big concepts, minus the textbook jargon:

## 1. Encoding (The Translator)
**Goal:** Make data safe to travel across systems.
- Think of encoding like translating English to Morse code. It looks like gibberish, but **there is no secret key**. Anyone with a Morse code chart can translate it back instantly. 
- **Base64** is the most common. You'll see it everywhere in web traffic. It usually ends in an `=` sign. It is NOT for security; it just prevents special characters from breaking web requests.

## 2. Hashing (The Meat Grinder)
**Goal:** Verify data hasn't changed without storing the original data.
- Think of hashing like putting a steak into a meat grinder. It comes out as ground beef. You can **never** put the ground beef back together to make a steak. It is a one-way street.
- We hash passwords. If your password is "hunter2", the server stores the hash. When you log in, it hashes what you typed and compares the two hashes. If a hacker steals the database, they just get useless ground beef.
- **Common grinders**: MD5 (broken, don't use), SHA-1 (weak), SHA-256 (the current good stuff).

## 3. Encryption (The Safe)
**Goal:** Hide data so only the right person can read it.
- Think of encryption like putting a document in a heavy steel safe. It is completely secure, **but it can be reversed if you have the key**. 
- Unlike hashing, we *want* to get the original data back. This is how your credit card safely travels to Amazon when you buy something.
- **Symmetric**: One key locks and unlocks the safe (fast).
- **Asymmetric**: Two keys. A public one anyone can use to drop files in the safe, and a private one only you hold to open it (slower, but safer for the internet).
