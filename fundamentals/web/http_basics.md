# HTTP & Web Communication

To break web applications, you first have to speak their language. HTTP (Hypertext Transfer Protocol) is the foundation of data communication on the web.

## 1. HTTP Methods (Verbs)
- **GET**: Requests data from a specified resource (parameters are in the URL).
- **POST**: Submits data to be processed to a specified resource (parameters are in the body).
- **PUT**: Updates a current resource with new data.
- **DELETE**: Removes the specified resource.
- **OPTIONS**: Returns the HTTP methods that the server supports for the specified URL (great for recon!).

## 2. Common Status Codes
- **200 OK**: The request succeeded.
- **301 / 302**: Redirection (Permanent / Temporary).
- **400 Bad Request**: The server couldn't understand the request (often due to malformed syntax).
- **401 Unauthorized**: Authentication is required and has failed or not yet been provided.
- **403 Forbidden**: You are authenticated, but you don't have permission to access the resource.
- **404 Not Found**: The server can't find the requested resource.
- **500 Internal Server Error**: The server encountered an unexpected condition (often a sign of a potential vulnerability!).

## 3. Critical HTTP Headers for Security
- **Host**: Specifies the domain name of the server. Changing this can sometimes lead to Host Header Injection.
- **Authorization**: Carries credentials (like Bearer tokens or Basic auth) to authenticate the user.
- **Cookie**: Sends stored session identifiers back to the server. Hijacking these is a primary goal for attackers.
