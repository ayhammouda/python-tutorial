# How to quickly build an API with Python

## Introduction

If you’re reading this article then you already have said this to yourself: I need to quickly build an API, with the least amount of code possible, but how? And I’m guessing you know a bit of Python too. As DevOps Engineers we’re often faced with the need to build, [among other things](https://intellipaat.com/blog/wp-content/uploads/2017/11/DevOps-01.jpg), automation tools [[1]](https://newrelic.com/devops/what-is-devops#Chapter5HowDoesDevOpsWork)[[2]](https://landing.google.com/sre/workbook/chapters/eliminating-toil/#automate-toil-response) and have it exposed using an API[[3]](https://landing.google.com/sre/workbook/chapters/reaching-beyond/#everything-important-eventually-becomes-a-platform) to be used later by other software components (Jira, Jenkins, services, applications,… ). So, in this tutorial we’re going to propose building a simple API, and have it automate few tasks for us. In a second article we’ll show how to add HTTPS support and authentication mechanisms so it can pass security requirements of enterprises and organisations[[4]](https://securityboulevard.com/2020/10/4-approaches-to-securing-containerized-applications/).

## Table of Contents

1. [Requirements](#requirements)
2. [Let's Start](#letsstart)
   1. [Hello World](#helloworld)
   2. [Log My Messages](#logmymessages)
3. [Containerization](#containerization)
4. [Conclusion](#conclusion)

## Requirements <a name="requirements"></a>
4. [Conclusion](#conclusion)
ou have already Python set up on your platform. If you don't, I suggest to you those awsome tutorials to get you up and running:

- [Installing Python](https://realpython.com/installing-python/)
- [Awesome Python](https://github.com/vinta/awesome-python)

## Why connexion? <a name="why-connexion"></a>
As a DevOps, I have grown very fond of the declarative approach as more and more tools are adopting, [Kubernetes](https://kubernetes.io), [Terraform](https://www.terraform.io/), A code that documentates itself, built with the end result in mind, reusable and idempotent[[5]](https://www.toptal.com/software/declarative-programming) so when I first discovered Connexion, I saw its potential to take a huge chunk of the work off in a contract first approach where the API definition is interpreted from yaml file with all the necessary data structures and validations. I understand if some users would prefer using [Flask](https://flask.palletsprojects.com) in a more convential way for advanced use cases. But for most use cases I would rather use this contract first, and Connexion does a very good job at it. ([See also Why Connexion](https://github.com/zalando/connexion#why-connexion))
## Let's Start <a name="letsstart"></a>

if you haven't installed connexion yet you can do so by running:

```bash
$ pip install connexion
```

### Hello World <a name="helloworld"></a>

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

And that's it, we are ready to go 😀 :

To run the API server:

``````bash
$ python helloworld.py
``````

**Note:** If you're face with a warning message saying that "*The swagger_ui directory could not be found.*" this library is used to generate the swagger documention for the defined specifications. to fix this you can install the optional connexion swagger-ui: (Read more about optional dependencies [here](https://www.python.org/dev/peps/pep-0508/#extras))

``````python
$ pip install 'connexion[swagger-ui]'
``````

This UI is accessible at : <http://localhost:8080/v1.0/ui>

To test the endpoint that we just created you can run:

``````bash
$ curl --request POST 'http://localhost:8080/v1.0/greeting/john'
``````

***So what just happened ?***  

The `helloworld.py`'s main looked our yaml file and rendered our specifictions in a [spec first](https://apievangelist.com/2020/05/07/api-specfirst-development/) fashion to create the API server.
Under `paths` we will define the endpoint that will be exposed by the API, the first method defined is a `POST` to `/greeting/{name}` which means that my endpoint will take a in path variable called name to be used in our implementation.

This method is linked to operation `greeting` in the `helloworld.py` using the keyword and value pair `operationId:helloworld.greeting` : helloworld is the name of our python script and greeting is the method name ( which conviently takes a string parameter called `name`)

### Log My Messages <a name="logmymessages"></a>

Now that we got around the basic let's do somehting that is not a *_Hello World_*, We're going to build an API that will receive a POST request with a json body and write the text in a file and then return the lines count in this file, so let's dive right to it!

In a new app folder, let's call it logmymessages, once again we'll create main file called app.py

```python
import connexion

app = connexion.FlaskApp(__name__, port=8080, specification_dir='swagger/')
app.add_api('swagger.yaml', arguments={'title': 'Log My Messages'})


def health_check():
    return {}


if __name__ == '__main__':
    app.run(host="0.0.0.0")

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
  /health-check:
    get:
      operationId: app.health_check
      summary: Health check for the api
      responses:
        200:
          description: Empty 200 response
     
```

To define the behaviour of the end point we are going to create a new file called log.py where we will implement the operation `api.log.write`. To do so, we'll create a folder called `api` and inside this folder we will create the `log.py` file as follows:

`api/log.py`:

```python
from datetime import datetime

"""Writes messages from a JSON input in a file.

Retrieves a json body with receieved messages to logs them into a file
named log.txt. the received messages will be appened and formated in
in the log file.
Args:
    message: A json object with two fields: 'message' which contains the text
    of the received message and 'sender' which contains the author or the sender
    of the message.


Returns:
    A dict with the key/value pair count_messages and num_lines describing the number of lines
    in the log file.

Raises:
    IOError: An error occurred accessing the log file
"""

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

For our second operation we will try the read this file and get back the messages logged in this file by send a GET request to our `/log` endpoint:

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
"""Return the messages written to the log file.

Return a json array of the receieved messages logged in the log.txt
file parsed to a new format with each message containing the value of
the 'sender', 'message' of the 'timestanp'.
Args:

Returns:
    An array of dicts with information from the received messages :
    timestamp: The timestamp of the message received
    sender: The sender of message.
    message: The text of the message received.

Raises:
    IOError: An error occurred accessing the log file
"""


def read():
    try:
        # Init the messages array
        messages = []
        # Read the log file and get the lines from it
        with open('log.txt', "r") as file:
            for line in file.read().splitlines():
                # Retrieve the values of the different fields
                timestamp = [x.split(']')[0]
                             for x in line.split('[') if ']' in x][0]
                sender = [x.split(']')[0]
                          for x in line.split('[') if ']' in x][1]
                message = line.split(':')[1]
                # Add the JSON object corresponding to the message to the list
                messages.append({
                    "timestamp": timestamp,
                    "sender": sender,
                    "message": message
                })
        # Return the list of messages in the form of a array of dict 
        return messages
    except (IOError) as e:
        return {
            "Error": f"Error occured : {str(e)}",
        }
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

## Containerization  <a name="containerization"></a>

In the section we're going to make build a docker image of our Python API and run our service in a containerzied environment so we can we can prep our API to deployed on different platfoms.

For this we're going to use the logmymessages example to build our docker image which is fairly a simple task to do:

First we start by creating a `requirements.txt` file where we'll define all the dependencies that's will need for our API, and it should look something like this:

`requirements.txt:`

```
gunicorn >= 20.0.4
connexion >= 2.7.0
connexion[swagger-ui] >= 2.7.0
```
This will allow for out container to be shipped with all it's dependencies. As you can see it only requires two thing:
- the connexion framework and the optional extra swagger-ui 
- [gunicorn](https://gunicorn.org/) or Green Unicorn an opensource pyton production grade web server that we'll use to run our api on.
In case you're wondering what's a `requirements.txt` file, it's a text file which, by convention, contains a list of all the pypi dependencies required by a python application to build an run.[[6]](https://pip.pypa.io/en/stable/user_guide/#requirements-files) 

Next we'll create the Dockerfile 

`Dockerfile`: 

```dockerfile
FROM python:3.6

WORKDIR /opt/logmymessages

# copy project
COPY . .

# Installing dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]

HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8080/health-check || exit 1

```
To build the image of our container we're going to use `python:3.6` as a base image, which is a debian image preloaded with python 3.6, pip 20.

In the `WORKDIR` we copy our app and then `RUN` pip to install the required dependencies.

To run the server, we use the gunicorn command, specify and binding socket and the path for the server's main.

With the keyword `HEALTHCHECK` we tell the running container deamon to check perform a healthcheck every 30s, and if check fail, the container should exit.
 
To build our container, in the logmymessages app folder, we run:
```bash
$ docker build -t logmymessages .
```
As output we should have the log of image being built tailed by a line `Successfully tagged logmymessages:latest`.

Now we can run our container by executing the following command:
```bash
$ docker run -p 8080:8080 logmymessages
```
The API server should be up and running and available on the same URL.
you can test this by accessing http://localhost:8080/v1.0/ui to see the Swagger UI. 
## Conclusion <a name="conclusion"></a>

In this tutorial we saw how to rapidly and API service and build the container image that can be deployed on any supporting platform.

In the next tutorial we'll try to secure our application and prepare it for deploiment to prodution on a kuberntes cluster. 
