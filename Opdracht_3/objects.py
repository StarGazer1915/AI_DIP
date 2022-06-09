
class Computer:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.failed = False
        self.value = 0

    def deliver_message(self, m, tick):
        # m = [src, dst, type, value]
        if m.type == "PROPOSE":
            print(f"{tick}:   -> {m.dst.id} | {m.type} v={m.value}")
            m.dst.value = m.value
        elif m.type == "PREPARE":
            print(f"{tick}: {m.src.id} -> {m.dst.id} | {m.type} n={m.src.id[1]}")

        return

    def __str__(self):
        return f"Computer | ID: {self.id} | Type: {self.type} | Failed: {self.failed} | Value: {self.value}"


class Message:
    def __init__(self, msrc, mdst, mtype, value):
        self.src = msrc
        self.dst = mdst
        self.type = mtype
        self.value = value

    def __str__(self):
        return f"Message: {self.src}, {self.dst}, {self.type}, {self.value}"


class Network:
    def __init__(self, id):
        self.id = id
        self.queue = []

    def queue_message(self, message):
        self.queue.append(message)
        return self.queue

    def extract_message(self):
        try:
            message = self.queue[0]
        except:
            return None
        if not message.src.failed and not message.dst.failed:
            self.queue.pop(0)
            return message
        else:
            return None

    def __str__(self):
        return f"Acceptor: {self.id}"
