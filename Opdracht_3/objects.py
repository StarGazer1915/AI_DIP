class Computer:
    def __init__(self, id, type, N, A, L):
        """
        Defining class values.
        @param id: str
        @param type: str
        @param N: Network object
        @param A: list (Computer objects)
        @param L: list (Computer objects)
        """
        self.id = id
        self.type = type
        self.failed = False
        self.value = None
        self.org_value = None
        self.p_id = None  # Proposer position_id (n=)
        self.N = N  # Network
        self.A = A  # Acceptors
        self.L = L  # Learners
        self.prior = None
        self.acc_count = 0
        self.rej_count = 0

    def deliver_message(self, m, tick):
        """
        This function handles all possible messages between computers.
        - PROPOSE
          The code updates the values in the PROPOSER and writes queue messages for
          the delivery of PREPARE messages to ACCEPTORS

        - PREPARE
          The code first checks if the p_id of the ACCEPTOR is lower or equal to
          the PROPOSER's p_id. If not then it's messages are ignored. If it is, then PROMISE
          messages are queued.

        - PROMISE
          The code first checks if the ACCEPTOR already has prior accepted values. If so then
          the value of the PROPOSER is updated with that correct value. Then the ACCEPT
          messages are queued.

        - ACCEPT
          The code first checks if the ACCEPTOR has a None value
          OR
          If the ACCEPTOR's value and PROPOSER's value are the same
          AND
          The PROPOSER's p_id is larger or equal to the ACCEPTOR's p_id.
          If so then the value can be accepted and ACCEPTED messages are queued, the prior values
          are also replaced with the new values. If not then the message is rejected which means
          that REJECTED messages are queued instead.

        - ACCEPTED
          The code first assigns the new accepted value to the ACCEPTOR. A PROPOSER's counter is updated
          to see if a majority of the acceptors have already ACCEPTED the value. If so then SUCCESS messages
          are queued for the LEARNER computers and the counter is set to zero to avoid problems with other proposals.

        - REJECTED
          Firstly the REJECTED counter is updated. Then it checks if the majority of the ACCEPTORS have
          REJECTED the messages. If so, then the PROPOSER tries again and PREPARE messages are queued under a new p_id.
          Here the counter is also reset to avoid problems with other proposals.

        - SUCCESS
          The code first updates the value of the LEARNER and shows what majority has been reached.

        @param m: Message object
        @param tick: int
        @return: void
        """
        if m.type == "PROPOSE" and m.dst.type == "PROPOSER":
            print(f"{tick}:    -> {m.dst.id} | {m.type} v={m.value}")
            m.dst.value, m.dst.org_value = m.value, m.value
            m.dst.acc_count, m.dst.rej_count = 0, 0
            for a_c in m.dst.A:
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

        elif m.type == "ACCEPTED" and m.dst.type == "PROPOSER":
            m.src.value = m.dst.value
            m.dst.acc_count += 1
            print(f"{tick}: {m.src.id} -> {m.dst.id} | {m.type} n={m.dst.p_id} v={m.src.value}")
            if m.dst.acc_count >= round(len(m.dst.A) / 2):
                for l_c in m.dst.L:
                    self.N.queue_message(Message(m.dst, l_c, "SUCCESS", m.dst.org_value))
                m.dst.acc_count = 0

        elif m.type == "REJECTED" and m.dst.type == "PROPOSER":
            print(f"{tick}: {m.src.id} -> {m.dst.id} | {m.type} n={m.dst.p_id}")
            m.dst.rej_count += 1
            if m.dst.rej_count >= round(len(m.dst.A)/2):
                for a_c in m.dst.A:
                    self.N.queue_message(Message(m.dst, a_c, "PREPARE", m.dst.org_value))
                    m.dst.p_id = a_c.p_id + 1
                m.dst.rej_count = 0

        elif m.type == "SUCCESS" and m.dst.type == "LEARNER":
            m.dst.value = m.src.value
            print(f"{tick}: {m.src.id} -> {m.dst.id} | {m.type} n={m.src.p_id} | Majority consensus reached on: "
                  f"{m.src.value}")

        else:
            raise RuntimeError(f"Error, combination of {m.type} and {m.dst.type} does not match")

    def __str__(self):
        return f"Computer | ID: {self.id} | Type: {self.type} | Prop_id: {self.p_id} | Failed: {self.failed} | " \
               f"Value: {self.value}"


class Message:
    def __init__(self, msrc, mdst, mtype, value):
        """
        Defining class values.
        @param msrc: Computer object or None
        @param mdst: Computer object or None
        @param mtype: str
        @param value: int or str
        """
        self.src = msrc
        self.dst = mdst
        self.type = mtype
        self.value = value

    def __str__(self):
        return f"Message: {self.src.id}, {self.dst.id}, {self.type}, {self.value}"


class Network:
    def __init__(self, id):
        """
        Defining class value.
        @param id: str
        """
        self.id = id
        self.queue = []

    def queue_message(self, message):
        """
        Places a message at the END of the queue.
        @param message: Message object
        @return: void
        """
        self.queue.append(message)

    def extract_message(self, t):
        """
        Extracts a message from the front of the queue where the source computer and desination computer
        haven't shut down (failed) OR if there is no source destination (then it is a proposal).
        After the message is extracted the message is removed from the queue. If there was no available
        message queued then the function will print a blank line with only the tick.
        @param t: int
        @return: Message object or None
        """
        if not self.queue:
            return None

        count = 0
        for i in self.queue:
            if not i.src or not i.src.failed and not i.dst.failed:
                self.queue.pop(count)
                return i
            count += 1

        print(f"{t}: ")
        return None

    def __str__(self):
        return f"Network: {self.id} | Queue:\n{self.queue}"
