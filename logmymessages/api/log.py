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
