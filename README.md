# Jump Cloud Automation


The current project is developed using Python 

You can download the latest version of Python for Windows from [Here](https://www.python.org/downloads/release/)


## Python pip modules needed

<pre><code>

python -m pip install requests

python -m pip install urllib3 

</code></pre>

## Executing tests ##


Clone Git repository https://github.com/Sirisha-Gutta/JCloud

Python Script can be run from windows command prompt  

```
example:

 c:\Users\SomeOne> python C:\MyProjectRepo\HashCompare.py
```

or use IDE **Pycharm**


## Endpoints being tested ##

1. Sets the environment variable Port
1. Launches the application
1. POST /hash - Hash and encode a password string. The request to accept password and returns the id of Base64 encoded string of the password that’s been hashed with SHA512
1. GET /hash/:id - Retrieve a generated hash with the id  
1. GET /stats - accepts no data. Returns a JSON object with the total count of the number of password hash requests made since the server started and the average time in milliseconds it has taken to process all of the requests
1. POST /shutdown - allows any in-flight password hashing to complete, reject any new requests and
shutdown.

