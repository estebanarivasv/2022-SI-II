
#### Project Files

- app.py - the main program.
- db.py - importing and creating SQLAlchemy object.
- blacklist.py - set(object) of blocked user.
- requirements.txt - List of all libraries needed to run the app.
- models(folder) - OOP (Users).
- resource(folder) - Resources (Users).


#### Installation

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py
```

#### Postman

Register: POST http://localhost:5000/register

    {
    "username": "username",
    "password": "password"
    }

Login: POST http://localhost:5000/register

    {
    "username": "Ramirocicd",
    "password": "kozmic"
    }

Logout: POST http://localhost:5000/logout
    
    Bearer token required

Refresh token: POST http://localhost:5000/refresh

    Bearer token required

Get user by id: http://localhost:5000/user/<id>

    
    
    
