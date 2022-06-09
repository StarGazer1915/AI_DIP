from objects import Computer, Message, Network


def create_computers(c_num, c_type):
    tmp = []
    for i in range(1, c_num+1):
        tmp.append(Computer(f"{c_type[0]}{i}", c_type))
    return tmp


def simulate(n_p, n_a, tmax, coms):
    global props

    P = create_computers(n_p, "PROPOSER")
    A = create_computers(n_a, "ACCEPTOR")
    N = Network("N1")

    for t in range(tmax):
        if len(N.queue) == 0 and len(coms) == 0:
            return

        try:
            com = coms[t]
        except:
            com = None

        if com is not None:
            e = com
            if "END" in com:
                continue

            elif "PROPOSE" in com:
                # Example: [0, "PROPOSE", 1, 42]
                e = [com[0], [], [], P[com[2] - 1], com[3]]

            elif "FAIL PROPOSER" in com:
                # Example: [8, "FAIL PROPOSER", 1]
                e = [com[0], [P[com[2] - 1]], [], None, None]

            elif "RECOVER PROPOSER" in com:
                # Example: [26, "RECOVER PROPOSER", 1]
                e = [com[0], [], [P[com[2] - 1]], None, None]

            coms.remove(com)
            (t, F, R, pi_c, pi_v) = e
            for c in F:
                c.failed = True
            for c in R:
                c.failed = False

            if pi_v is not None and pi_c is not None:  # PROPOSE
                m = Message(None, pi_c, "PROPOSE", pi_v)
                pi_c.deliver_message(m, t)
                for a_c in A:
                    m = Message(pi_c, a_c, "PREPARE", pi_v)
                    N.queue_message(m)
                props += 1
        else:
            pass
            m = N.extract_message()
            if m is not None:
                m.dst.deliver_message(m, t)

    return


# =============== EXECUTION =============== #
commands = [
    [0, "PROPOSE", 1, 42],
    [0, "END"]
]

props = 1

simulate(1, 3, 15, commands)