# How to quickly build an API with Python

## Introduction

If you’re reading this article then you already have said this to yourself: I need to quickly build an API, with the least amount of code possible, but how? And I’m guessing you know a bit of Python too. As DevOps Engineers we’re often faced with the need to build, [among other things](https://intellipaat.com/blog/wp-content/uploads/2017/11/DevOps-01.jpg), automation tools [[1]](https://newrelic.com/devops/what-is-devops#Chapter5HowDoesDevOpsWork)[[2]](https://landing.google.com/sre/workbook/chapters/eliminating-toil/#automate-toil-response) and have it exposed using an API[[3]](https://landing.google.com/sre/workbook/chapters/reaching-beyond/#everything-important-eventually-becomes-a-platform) to be used later by other software components (Jira, Jenkins, services, applications,… ). So, in this tutorial we’re going to propose building a simple API, and have it automate few tasks for us. In a second article we’ll show how to add HTTPS support and authentication mechanisms so it can pass security requirements of enterprises and organisations.

# Table of Contents
1. [Requirements](#requirements)
2. [Let's Start](#letsstart)
   1. [Hello World](#helloworld)
   2. [Log My Messages](#logmymessages)
3. *[&#x1F536;Conclusion](#conclusion)*

## Requirements <a name="requirements"></a>

To build our API we will be using Python programming language in its 3rd version and we’ll use the Connexion framework to handle our HTTP requests and interactions.

- [Python 3](https://www.python.org/downloads/)
- &#x1F536; [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Connexion](https://github.com/zalando/connexion)

## Let's Start <a name="letsstart"></a>

I presume you have installed Python on your plateform. If you didn't, I suggest you those awsome tutorials by [....]()

if you haven't installed connexion yet you can do so by running:

```bash
$ pip install connexion
```

### Hello World <a name="helloworld"></a>

*&#x1F536; Suggestion: show a Hello world with Falsk and then switch to Connexion to show its benefits.*

let's start with an old fashioned *Hello* *World* :

In our app folder let's create a new file `helloworld.py`:

```````python
import connexion

def greeting(name: str) -> str:
    return 'Hello {name}'.format(name=name)

if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, port=8080, specification_dir='swagger/')
    app.add_api('helloworld.yaml', arguments={'title': 'Hello World'})
    app.run()
```````

In the code above, we have the main code that will render our specifications for the API and load the arguments, and the operation method `greeting` which will be executed when we run the api server. 

*&#x1F536; it's not clear how the  the operation method `greeting` will be executed when we'll run the server may be it will be more clear by introduicing breifly swagger and what is a "swagger specification", "contract first" etc.*

Next, we will write the specifications of the API, for this we will create a new folder called `swagger` and we will add a new file `swagger/helloworld.yaml`:

``````yaml
swagger: "2.0"

info:
  title: "{{title}}"
  version: "1.0"

basePath: /v1.0

paths:
  /greeting/{name}:
    post:
      summary: Generate greeting
      description: Generates a greeting message.
      operationId: helloworld.greeting
      produces:
        - text/plain;
      responses:
        200:
          description: greeting response
          schema:
            type: string
          examples:
            "text/plain": "Hello John"
      parameters:
        - name: name
          in: path
          description: Name of the person to greet.
          required: true
          type: string
``````
*&#x1F536; this file needs more explanation IMO; the global configuration part, the API URL endpoints configuration part, the methods, the responses, the successfull one, the parameters, etc. or add more details in the **So what just happened ?** section * 

And that's it, we are ready to go &#x1F60A; :

To run the API server:

``````bash
$ python helloworld.py
``````

You should be faced with a warning message saying that "*The swagger_ui directory could not be found.*" this library is used to generate the swagger documention for the defined specifications. to fix this you can run:

``````python
$ pip install 'connexion[swagger-ui]'
``````
*&#x1F536; why not add this to the requirements?*

This UI is accessible at : <http://localhost:8080/v1.0/ui>

To test the endpoint that we just created you can run:

``````bash
$ curl --request POST 'http://localhost:8080/v1.0/greeting/john'
``````

***So what just happened ?***  

the connexion framework rendered our specifictions defined in our yaml file  to create the API server and linked the greeting endpoint with the greeting method in the `helloworld.py` using the object `operationId: helloworld.greeting` where we passed a parameter called `name` to the method.

### Log My Messages <a name="logmymessages"></a>

Now that we got around the basic let's do somehting that is not a _Hello World_, We're going to build an API that will receive a POST request with a json body and write the text in a file and then return the lines count in this file, so let's dive right to it!

In a new app folder, let's call it logmymessages, once again we'll create main file called app.py

```python
import connexion

if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, port=8080, specification_dir='swagger/')
    app.add_api('swagger.yaml', arguments={'title': 'Log My Messages'})
    app.run()
```

And then let's create the swagger specifications for this API:

```yaml
swagger: "2.0"

info:
  title: "{{title}}"
  version: "1.0"

basePath: /v1.0

paths:
  /log:
    post:
      summary: Log the messages
      description: Write the recieved message to a log file.
      operationId: api.log.write
      produces:
        - application/json;
      responses:
        200:
          description: number of received messages
          schema:
            type: object
      parameters:
        - name: message
          in: body
          description: the JSON text object.
          schema:
            type: object
            required:
            - sender
            - message
            properties:
              sender:
                type: string
              message:
                type: string
```
To define the behaviour of the end point we are going to create a new file called log.py where we will implement the operation `api.log.write`. To do so, we'll create a folder called `api` and inside this folder we will create the `log.py` file as follows

```python
from datetime import datetime


def write(message):
    # GET JSON object attributes
    sender = message['sender']
    message = message['message']
    # Write attributes to file
    with open("log.txt", "a") as logfile:
        logfile.write("[%s][%s] : %s\n" % (
            datetime.now().strftime('%Y%m%d-%H%M%S'), sender, message))
    # Count line if file
    num_lines = sum(1 for line in open('log.txt'))
    # Return a JSON object with the count of messages in the log file
    return {
        "count_messages": num_lines
    }
```
*&#x1F536; needs more explanation IMO in a style like: "In this code, we created a write function that will receive as parameter a  `message` dictionary data structure… it will open … the count and return…"*

Let's run the API server and test our new app:

```bash
$ python app.py
```

We will send a POST request with the content of our message to the API server:

```bash
$ curl --request POST 'http://localhost:8080/v1.0/log' \
--header 'Content-Type: application/json' \
-d '{
  "message": "Hi, I am Matt. I am a radar technician",
  "sender": "Matt"
}'
```

Output:

```bash
{
  "count_messages": 1
}
```

We will send a second POST request with another message:

```bash
$ curl --request POST 'http://localhost:8080/v1.0/log' \
--header 'Content-Type: application/json' \
-d '{
  "message": "I am 90% sure Matt is Kylo Ren!",
  "sender": "Stormtrooper"
}'

```

Output:

```bash
{
  "count_messages": 2
}
```

If everything is working fine we should be able to see a new file created in our app folder called `log.txt` with two lines in it:

```bash
$ cat log.txt
[20210101-101001][Matt] : Hi, I am Matt. I am a radar technician
[20210101-101010][Stormtrooper] : I am 90% sure Matt is Kylo Ren!
```

For our second operation we will try to read this file and get back the messages logged in by send a GET request to our `/log` endpoint.

In the `swagger/swagger.yaml` file we will add:

``` yaml
    get:
      summary: Read the received messages
      description: Read the recieved message to a log file.
      operationId: api.log.read
      produces:
        - application/json;
      responses:
        200:
          description: number of received messages
          schema:
            type: object
```

And in the `api/log.py` file we will add:

```python
def read():
    messages = []
    with open('log.txt', "r") as file:
        for line in file.read().splitlines():
            timestamp = [x.split(']')[0]
                         for x in line.split('[') if ']' in x][0]
            sender = [x.split(']')[0]
                      for x in line.split('[') if ']' in x][1]
            message = line.split(':')[1]
            messages.append({
                "timestamp": timestamp,
                "sender": sender,
                "message": message
            })
    return messages
```

And that's it!

we just created a second endpoint for our api and implemented it's operation method:

Let's re-run the api server now by executing:

```bash
$ python app.py
```

```bash
$ curl --request GET 'http://localhost:8080/v1.0/log'
```

Output:

```python
[
  {
    "message": " Hi, I am Matt. I am a radar technician",
    "sender": "Matt",
    "timestamp": "20210101-101001"
  },
  {
    "message": " I am 90% sure Matt is Kylo Ren!",
    "sender": "Stormtrooper",
    "timestamp": "20210101-101010"
  }
]
```
*&#x1F536; It'll be nice to have so swagger UI screenshots. *

*&#x1F536; ## Conclusion <a name="conclusion"></a>*

In this tutorial, you saw how fast and easy it is to create a REST API with Python …

In Part 2 of this series, you’ll learn how to … 

