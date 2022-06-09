
class Computer:
    def __init__(self, id, type, N, A):
        self.id = id
        self.type = type
        self.failed = False
        self.value = None
        self.p_id = 1
        self.network = N
        self.acceptors = A
        self.prior = None

    def deliver_message(self, m, tick):
        if m.type == "PROPOSE" and m.dst.type == "PROPOSER":
            print(f"00{tick}:    -> {m.dst.id} | {m.type} v={m.value}")
            m.dst.value = m.value
            m.dst.p_id = m.dst.id[1]

            for a_c in self.acceptors:
                self.network.queue_message(Message(m.dst, a_c, "PREPARE", m.value))
                a_c.p_id = m.dst.id[1]

        elif m.type == "PREPARE" and m.dst.type == "ACCEPTOR":
            if m.dst.p_id >= m.src.id[1]:
                print(f"00{tick}: {m.src.id} -> {m.dst.id} | {m.type} n={m.src.id[1]}")

                self.network.queue_message(Message(m.dst, m.src, "PROMISE", m.value))
            else:
                print("Acceptor ignored proposal, proposer_id was too small")

        elif m.type == "PROMISE" and m.dst.type == "PROPOSER":
            print(f"00{tick}: {m.src.id} -> {m.dst.id} | {m.type} n={m.dst.id[1]} | Prior: {self.prior}")
            self.network.queue_message(Message(m.dst, m.src, "ACCEPT", m.value))

        elif m.type == "ACCEPT" and m.dst.type == "ACCEPTOR":
            print(f"00{tick}: {m.src.id} -> {m.dst.id} | {m.type} n={m.src.id[1]} v={m.src.value}")
            self.network.queue_message(Message(m.dst, m.src, "ACCEPTED", m.value))
            m.dst.value = m.src.value

        elif m.type == "ACCEPTED" and m.dst.type == "PROPOSER":
            print(f"00{tick}: {m.src.id} -> {m.dst.id} | {m.type} n={m.src.id[1]} v={m.src.value}")

        else:
            raise RuntimeError(f"Error, combination of {m.type} and {m.dst.type} does not match")

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

        if message.src is None or not message.src.failed and not message.dst.failed:
            self.queue.pop(0)
            return message
        else:
            return None

    def __str__(self):
        print(f"Network: {self.id}")
        for i in range(len(self.queue)):
            print(f"{i}: {self.queue[i]}")
        return ""
