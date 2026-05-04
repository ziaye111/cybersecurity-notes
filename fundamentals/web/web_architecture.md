# Web Architecture Basics

Modern web applications are complex ecosystems. Knowing where things live helps you know where to attack.

## 1. The Client-Server Model
- **Frontend (Client-Side)**: What the user sees and interacts with (HTML, CSS, JavaScript). Runs in the browser. *Common attacks: XSS, CSRF.*
- **Backend (Server-Side)**: The logic, database interactions, and server processing (Python, Node.js, PHP, Java). *Common attacks: SQL Injection, Command Injection, SSRF.*

## 2. APIs (Application Programming Interfaces)
APIs allow different software systems to communicate. Most modern web apps use REST or GraphQL APIs to fetch data dynamically without reloading the page. Unsecured API endpoints are a massive target for attackers (e.g., Broken Object Level Authorization).

## 3. DNS (Domain Name System)
The phonebook of the internet. Translates human-readable domain names (like `github.com`) into IP addresses.
- **A Record**: Points a domain to an IPv4 address.
- **CNAME**: Points a domain to another domain name. Subdomain takeovers often happen when CNAMEs point to unclaimed resources.
