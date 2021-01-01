# How to quickly build an API with Python

## Introduction

If you’re here then you already have said this to yourself: I need to quickly build an API, with the least amount of code possible, but how?

As DevOps Engineers, we’re often faced with the need to build, [among other things](https://intellipaat.com/blog/wp-content/uploads/2017/11/DevOps-01.jpg), automation tools [[1](https://newrelic.com/devops/what-is-devops#Chapter5HowDoesDevOpsWork)][[2](https://landing.google.com/sre/workbook/chapters/eliminating-toil/#automate-toil-response)] and have them exposed using an API[[3](https://landing.google.com/sre/workbook/chapters/reaching-beyond/#everything-important-eventually-becomes-a-platform)] to be used later by other software components (Jira, Jenkins, services, applications,… ). So, in this tutorial, we’re going to propose building a simple API and have it automate a few tasks for us. In a second article, we’ll show how to add HTTPS support and authentication mechanisms so it can pass the security requirements of enterprises and organizations[[4](https://securityboulevard.com/2020/10/4-approaches-to-securing-containerized-applications/)]

## TL;DR

[What I needed to start](https://medium.com/devops-stuff/how-to-quickly-build-an-api-with-python-fe03959c21d3#73a4), [made a Hello Wold API](https://medium.com/devops-stuff/how-to-quickly-build-an-api-with-python-fe03959c21d3#3f5d), [something a little more complicated](https://medium.com/devops-stuff/how-to-quickly-build-an-api-with-python-fe03959c21d3#ca78), [and ran it in a container](https://medium.com/devops-stuff/how-to-quickly-build-an-api-with-python-fe03959c21d3#a9b3).

## Requirements <a name="requirements"></a>

To build our API we will be using Python 3 programming language and we’ll use the Connexion framework to handle our HTTP requests and interactions.

- [Python 3](https://www.python.org/downloads/)
- [Connexion](https://github.com/zalando/connexion)

I presume you have already Python set up on your platform. If you don’t, I suggest these awesome tutorials to get you up and running:

- [Installing Python](https://realpython.com/installing-python/)
- [Awesome Python](https://github.com/vinta/awesome-python)

## Connexion <a name="why-connexion"></a>

In my line of work, I have grown very fond of the declarative approach as more and more tools are adopting it such as [Kubernetes](https://kubernetes.io/) and [Terraform](https://www.terraform.io/); a code that it’s its own documentation, built with the end result in mind, reusable and idempotent[[5](https://www.toptal.com/software/declarative-programming)].So when I first discovered Connexion, I saw its potential to take a huge chunk of the work off in a contract-first approach where the API definition is interpreted from YAML file with all the necessary data structures and validations. I understand if some users would prefer using [Flask](https://flask.palletsprojects.com/) [[6](https://hotframeworks.com/frameworks/flask)]in a more conventional way for advanced use cases. But for the rest of use cases, I would rather use this contract first[[7](https://openpracticelibrary.com/practice/contract-first-development/)], and Connexion does a very good job at it. (See also [Why Connexion](https://github.com/zalando/connexion#why-connexion).)

## Let's Start <a name="letsstart"></a>

If you haven’t installed connexion yet you can do so by running:

```bash
$ pip install connexion
```

### Hello World <a name="helloworld"></a>

Let’s start with an old fashioned *Hello* *World* :

In our app folder let’s create a new file `helloworld.py`:

```````python
import connexion

def greeting(name: str) -> str:
    return 'Hello {name}'.format(name=name)

if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, port=8080, specification_dir='swagger/')
    app.add_api('helloworld.yaml', arguments={'title': 'Hello World'})
    app.run()
```````

In the code above, we have the main code that will render our specifications for the API and load the arguments, and the operation method `greeting` which will be executed when we run the API server.

Next, we will write the specifications of the API. For this, we will write a [Swagger](https://swagger.io/) definition file. If you never heard of Swagger, it’s not that complicated:
Swagger is a set of rules (in other words, a specification) describing REST APIs. These specifications are human-readable and machine-interpretable. As a result, it can be used as documentation for testers and developers, but can also be used by various tools to automate API-related processes.
Now, we will create a new folder called `swagger` and we will add a new file `swagger/helloworld.yaml`:

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

**Note:** If you’re faced with a warning message saying that “*The swagger_ui directory could not be found.*”, this is a library used to generate the swagger documentation for the defined specifications. To fix this, you can install the optional connexion swagger-ui: (Read more about optional dependencies [here](https://www.python.org/dev/peps/pep-0508/#extras))

``````python
$ pip install 'connexion[swagger-ui]'
``````

This UI is accessible at : <http://localhost:8080/v1.0/ui>

To test the endpoint that we just created you can run:

``````bash
$ curl --request POST 'http://localhost:8080/v1.0/greeting/john'
``````

***So what just happened ?***  

The `helloworld.py`'s main looked for our YAML file and rendered our specifications in a [spec first](https://apievangelist.com/2020/05/07/api-specfirst-development/) fashion to create the API server. Under `paths` we will define the endpoint that will be exposed by the API, the first method defined is a `POST` to `/greeting/{name}` which means that my endpoint will take an in-path variable called name to be used in our implementation.

This method is linked to the operation `greeting` in the `helloworld.py` using the keyword and value pair `operationId:helloworld.greeting` : helloworld is the name of our python script and greeting is the method name ( which conveniently takes a string parameter called `name`)

### Log My Messages <a name="logmymessages"></a>

Now that we got around the basic let’s do something that is not a *Hello World*, We’re going to build an API that will receive a POST request with a JSON body and write the text in a file and then return the lines count in this file, so let’s dive right to it!

In a new app folder, let’s call it logmymessages, once again we’ll create a main file called `app.py`:

```python
import connexion


def health_check():
    return {}

app = connexion.FlaskApp(__name__, port=8080, specification_dir='swagger/')
app.add_api('swagger.yaml', arguments={'title': 'Log My Messages'})


if __name__ == '__main__':
    app.run(host="0.0.0.0")

```

And then let’s create the swagger specifications for this API. In a `swagger` folder, create a new file `swagger.yaml`:

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
  /health-check:
    get:
      operationId: app.health_check
      summary: Health check for the api
      responses:
        200:
          description: Empty 200 response
```

To define the behavior of the endpoint we are going to create a new file called [log.py](http://log.py/) where we will implement the operation `api.log.write`. To do so, we'll create a folder called `api` and inside this folder, we will create the `log.py` file as follows:

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
    try:
        with open("log.txt", "a") as logfile:
            logfile.write("[%s][%s] : %s\n" % (
                datetime.now().strftime('%Y%m%d-%H%M%S'), sender, message))
        # Count line if file
        num_lines = sum(1 for line in open('log.txt'))
        # Return a JSON object with the count of messages in the log file
        return {
            "count_messages": num_lines
        }
    except (IOError) as error:
        return {
            "Error": f"Error occured : {str(error)}",
        }
```

Let’s run the API server and test our new app:

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

For our second operation, we will try the read this file and get back the messages logged in this file by sending a GET request to our `/log` endpoint:

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
    except IOError as error:
        return {
            "Error": f"Error occured : {str(error)}",
        }
```

And that’s it!

we just created a second endpoint for our API and implemented its operation method:

Let’s re-run the API server now by executing:

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

In the section, we’re going to create a docker image of our Python API and run our service in a containerized environment so we can prep our API to be deployed on different platforms.

For this we’re going to use the logmymessages example to build our docker image which is fairly a simple task to do:

First, we start by creating a `requirements.txt` file where we'll define all the dependencies needed for our API, and it should look something like this:

`requirements.txt:`

```
gunicorn >= 20.0.4
connexion >= 2.7.0
connexion[swagger-ui] >= 2.7.0
```

This will allow for our container to be shipped with all its dependencies. As you can see it only requires two things:

- the connexion framework and the optional extra swagger-ui
- [gunicorn](https://gunicorn.org/) or Green Unicorn an open-source Python production-grade web server that we’ll use to run our API on.

In case you’re wondering what’s a `requirements.txt` file, it's a text file that, by convention, contains a list of all the PyPI dependencies required by a python application to build and run.[[8\]](https://pip.pypa.io/en/stable/user_guide/#requirements-files)

Next, we’ll create the Dockerfile:

`Dockerfile`:

```dockerfile
FROM python:3.6

WORKDIR /opt/logmymessages

# copy project
COPY . .

# Installing dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt


CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]

HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8080/health-check || exit 1

```

To build the image of our container we’re going to use `python:3.6` as a base image, which is a Debian image preloaded with python 3.6, pip 20.

In `WORKDIR` we copy our app and then `RUN` pip to install the required dependencies.

To run the server, we use the gunicorn command, specify the binding socket and the path for the server’s main.

With the keyword `HEALTHCHECK` we tell the running container daemon to perform a health check every 30s, and if the check fails, the container should exit.

To build our container, in the logmymessages app folder, we run:

```bash
$ docker build -t logmymessages .
```

As output, we should have the log of the image being built tailed by a line `Successfully tagged logmymessages:latest`.

Now we can run our container by executing the following command:

```bash
$ docker run -p 8080:8080 logmymessages
```

The API server should be up and running and available on the same URL.
you can test this by accessing [http://localhost:8080/v1.0/ui](http://localhost:8080/v1.0/ui) to see the Swagger UI.

## Conclusion <a name="conclusion"></a>

In this tutorial, we saw how to rapidly build an API service using the contract first approach and build the container image that can be deployed on any supporting platform.

In the next tutorial, we’ll try to secure our application and prepare it for deployment to production on a Kubernetes cluster.
