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
    except (IOError) as e:
        return {
            "Error": f"Error occured : {str(e)}",
        }


"""Returns the messages written to the log file.

Returns a json array of the receieved messages logged in the log.txt
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
