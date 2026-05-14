# Advanced Web Exploitation Methodologies

Modern web security requires looking beyond basic injections into complex logical and structural flaws.

## 1. Cross-Site Request Forgery (CSRF)
Forcing a logged-in user to perform actions they didn't intend to. This is mitigated using unique **Anti-CSRF tokens**.

## 2. Server-Side Request Forgery (SSRF)
Abusing a server to make internal network requests. This is a high-impact vulnerability often used to leak metadata from cloud environments (AWS/Azure).

## 3. Insecure Deserialization
When an application takes user-provided serialized objects and converts them back into live objects. This can lead to **Remote Code Execution (RCE)**.

## 4. Cross-Origin Resource Sharing (CORS) Misconfigurations
Overly permissive CORS policies (e.g., `Access-Control-Allow-Origin: *`) allow malicious sites to steal data from a user's session.
