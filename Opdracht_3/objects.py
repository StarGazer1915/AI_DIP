
class Proposer:
    def __init__(self, id):
        self.id = id
        self.failed = False

    def __str__(self):
        return f"Proposer: {self.id}"


class Acceptor:
    def __init__(self, id):
        self.id = id
        self.failed = False

    def __str__(self):
        return f"Acceptor: {self.id}"


class Message:
    def __init__(self, msrc, mdst, mtype):
        self.src = msrc
        self.dst = mdst
        self.type = mtype

        # TYPES:
        # - PROPOSE
        # - PREPARE
        # - PROMISE
        # - ACCEPT
        # - ACCEPTED
        # - REJECTED

    def __str__(self):
        return f"Message: {self.src}, {self.dst}, {self.type}"


class Network:
    def __init__(self, id, proposers, acceptors):
        self.id = id
        self.prop = proposers
        self.accept = acceptors
        self.failed = False

    def __str__(self):
        return f"Acceptor: {self.id}"
