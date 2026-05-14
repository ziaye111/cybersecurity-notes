# OWASP Top 10 Overview

The OWASP Top 10 is the standard awareness document for developers and web application security.

## 1. Broken Access Control
Users can access resources outside of their intended permissions. This is often how administrative panels or sensitive user data are leaked.

## 2. Cryptographic Failures
Focuses on failures related to cryptography which often leads to sensitive data exposure. As noted in my **Crypto Basics**, using broken algorithms like MD5 for passwords falls under this category.

## 3. Injection
Occurs when untrusted data is sent to an interpreter as part of a command or query (e.g., SQLi, Command Injection). The **Buffer Overflow** used in my Mindgames exploit is a form of memory injection.

## 4. Insecure Design
A broad category focusing on flaws related to design and architectural flaws, with a call for more "shift left" security.

## 5. Security Misconfiguration
The most common issue, including default passwords, open cloud storage, or overly verbose error messages that leak system info.
