# Python Library Licensing API

To deploy the api, just do a 
```bash
sudo docker-compose up --build
```

# Exposed endpoints:  

For issueing a license  
### POST ```/api/issue/```
```javascript
headers:
{ 
  "Authorization": "Bearer eyJhbGciOiJI...M3A90LCkxxtX9oNP9KZO"
}
body:
{ 
  "name": "name-of-the-license", 
  "policy": "selected-policy"
}
```

Validating license from user
### GET ```/api/actions/validate```
  
```javascript
body:
{ 
  "email": "someuser@example.com", 
  "key": "DlsKc4PD2vM...j34fPxk03enSw=="
}
```

A susperuser suspending the license
### PATCH ```/api/actions/suspend```

A susperuser revoking the license
### PATCH ```/api/actions/revoke```

A susperuser resuming the license after suspension
### PATCH ```/api/actions/resume```
The above all three [resume, revoke, suspend] endpoints have same header and body requirements.
```javascript
headers:
{ 
  "Authorization": "Bearer eyJhbGciOiJI...M3A90LCkxxtX9oNP9KZO"
}
body:
{ 
  "email": "admin@example.com"
}
```
Prometheus endpoint
### GET ```/api/metrics/```


# Accounts
###  POST ```/accounts/signup/```
```javascript
body: 
{ 
  "name": "Your Name", 
  "email": "someuser@example.com", 
  "password": "345yr3jh2hg4wet", 
  "organization": "organization-name-in-database", 
  "phone": "9565...123", // Can be empty 
  "address": "" // Can be empty
}
```

For account verification (can be used only once)
###GET ```/accounts/verify/<token>/```


For a password reset request:
###  POST ```/accounts/forgot-password/```
```javascript
body: 
{
  "email": "someuser@example.com"
}
```
For a resetting password confirmation:
###  POST ```/accounts/forgot-password/<token>/```
```javascript
body: 
{
  "password": "345yr3jh2hg4wet"
}
```

###  POST ```/accounts/login/```
```javascript
body: 
{
  "email": "someuser@example.com",
  "password": "345yr3jh2hg4wet"
}
```
This lo POSTgin request would return ```access_token``` and ```refresh_token``` as
```javascript
{
  "refresh": "eyJhbGciOiJ...ssQfLtQ7NUluc",
  "access": "eyJhbGciOiJ...ut_cfO3dI0XBQ"
}
```

###  POST ```/accounts/login/refresh/```
For providing another access token after it expires.
```javascript
{
  "refresh": "eyJhbGciOiJ...ssQfLtQ7NUluc"
}
```
Returns a new pair of access and refresh tokens.

