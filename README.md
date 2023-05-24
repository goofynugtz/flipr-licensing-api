# Python Library Licensing API

To deploy the api, just do a 
```bash
sudo docker-compose up --build
```

# Exposed endpoints:  

For issueing a license  
## ```POST /api/issue/```
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

##  ```GET /api/actions/validate```
  
```javascript
body:
{ 
  "email": "admin@example.com", 
  "key": "DlsKc4PD2vM...j34fPxk03enSw=="
}
```
##  ```PATCH /api/actions/suspend```
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

##  ```PATCH /api/actions/revoke```
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
##  ```PATCH /api/actions/resume```
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
##  ```GET/ api/metrics/```