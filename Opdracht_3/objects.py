
class Computer:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.failed = False

    def deliver_message(self, c, message):
        return

    def __str__(self):
        return f"Computer | ID: {self.id} | Type: {self.type} | Failed: {self.failed}"


class Message:
    def __init__(self, msrc, mdst, mtype):
        self.src = msrc
        self.dst = mdst
        self.type = mtype

        # MESSAGE TYPES:
        # - PROPOSE
        # - PREPARE
        # - PROMISE
        # - ACCEPT
        # - ACCEPTED
        # - REJECTED

    def __str__(self):
        return f"Message: {self.src}, {self.dst}, {self.type}"


class Network:
    def __init__(self, id):
        self.id = id
        self.queue = []

    def queue_message(self, message):
        self.queue.append(message)
        return self.queue

    def extract_message(self):
        message = self.queue[0]
        if not message.src.failed and not message.dst.failed:
            self.queue.pop(0)
            return message
        else:
            return None

    def __str__(self):
        return f"Acceptor: {self.id}"
