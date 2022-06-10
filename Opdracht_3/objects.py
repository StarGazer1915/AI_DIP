class Computer:
    def __init__(self, id, type, N, A):
        self.id = id
        self.type = type
        self.failed = False
        self.value = None
        self.org_value = None
        self.p_id = None
        self.N = N
        self.A = A
        self.prior = None
        self.rej_count = 0

    def deliver_message(self, m, tick):
        tick = str(tick).zfill(3)
        if m.type == "PROPOSE" and m.dst.type == "PROPOSER":
            print(f"{tick}:    -> {m.dst.id} | {m.type} v={m.value}")
            m.dst.value = m.value
            m.dst.org_value = m.value

            for a_c in self.A:
                self.N.queue_message(Message(m.dst, a_c, "PREPARE", m.value))
                a_c.p_id = m.dst.p_id

        elif m.type == "PREPARE" and m.dst.type == "ACCEPTOR":
            if m.dst.p_id <= m.src.p_id:
                print(f"{tick}: {m.src.id} -> {m.dst.id} | {m.type} n={m.src.p_id}")
                self.N.queue_message(Message(m.dst, m.src, "PROMISE", m.value))
            else:
                print("Acceptor ignored proposal, proposer_id was too small")

        elif m.type == "PROMISE" and m.dst.type == "PROPOSER":
            if m.src.prior:
                m.dst.value = m.src.prior[1]
            print(f"{tick}: {m.src.id} -> {m.dst.id} | {m.type} n={m.src.p_id} | Prior: {m.src.prior}")
            self.N.queue_message(Message(m.dst, m.src, "ACCEPT", m.value))

        elif m.type == "ACCEPT" and m.dst.type == "ACCEPTOR":
            print(f"{tick}: {m.src.id} -> {m.dst.id} | {m.type} n={m.src.p_id} v={m.src.value}")
            if not m.dst.value or m.dst.value == m.src.value and m.src.p_id >= m.dst.p_id:
                self.N.queue_message(Message(m.dst, m.src, "ACCEPTED", m.value))
                m.dst.prior = [m.src.p_id, m.src.value]
            else:
                self.N.queue_message(Message(m.dst, m.src, "REJECTED", m.value))

        elif m.type == "REJECTED" and m.dst.type == "PROPOSER":
            print(f"{tick}: {m.src.id} -> {m.dst.id} | {m.type} n={m.dst.p_id}")
            m.dst.rej_count += 1
            if m.dst.rej_count >= round(len(m.dst.A)/2):
                for a_c in m.dst.A:
                    self.N.queue_message(Message(m.dst, a_c, "PREPARE", m.dst.org_value))
                    m.dst.p_id = a_c.p_id + 1
                m.dst.rej_count = 0

        elif m.type == "ACCEPTED" and m.dst.type == "PROPOSER":
            m.src.value = m.dst.value
            print(f"{tick}: {m.src.id} -> {m.dst.id} | {m.type} n={m.dst.p_id} v={m.src.value}")

        else:
            raise RuntimeError(f"Error, combination of {m.type} and {m.dst.type} does not match")

        return

    def __str__(self):
        return f"Computer | ID: {self.id} | Type: {self.type} | Prop_id: {self.p_id} | Failed: {self.failed} | Value: {self.value}"


class Message:
    def __init__(self, msrc, mdst, mtype, value):
        self.src = msrc
        self.dst = mdst
        self.type = mtype
        self.value = value

    def __str__(self):
        return f"Message: {self.src.id}, {self.dst.id}, {self.type}, {self.value}"


class Network:
    def __init__(self, id):
        self.id = id
        self.queue = []

    def queue_message(self, message):
        self.queue.append(message)
        return self.queue

    def extract_message(self, t):
        if not self.queue:
            return None

        count = 0
        for i in self.queue:
            if not i.src or not i.src.failed and not i.dst.failed:
                self.queue.pop(count)
                return i
            count += 1

        print(f"{str(t).zfill(3)}: ")
        return None

    def __str__(self):
        print(f"Network: {self.id}")
        for i in range(len(self.queue)):
            print(f"{i}: {self.queue[i]}")
        return ""
