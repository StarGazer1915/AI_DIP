from objects import Computer, Message, Network


def create_computers(c_num, c_type, N, A):
    tmp = []
    for i in range(1, c_num + 1):
        tmp.append(Computer(f"{c_type[0]}{i}", c_type, N, A))
    return tmp


def simulate(n_p, n_a, tmax, coms):
    num_prop = 0

    N = Network("N1")
    A = create_computers(n_a, "ACCEPTOR", N, [])
    P = create_computers(n_p, "PROPOSER", N, A)

    for t in range(tmax):
        if len(N.queue) == 0 and len(coms) == 0:
            return

        com = coms[0]
        if com[0] != t:
            com = None

        if com:
            e = com
            if "END" in com:
                continue

            elif "PROPOSE" in com:
                e = [com[0], [], [], P[com[2] - 1], com[3]]
            elif "FAIL PROPOSER" in com:
                print(f"{str(t).zfill(3)}: ** P{com[2]}  kapot **")
                e = [com[0], [P[com[2] - 1]], [], None, None]
            elif "RECOVER PROPOSER" in com:
                print(f"{str(t).zfill(3)}: ** P{com[2]}  gerepareerd **")
                e = [com[0], [], [P[com[2] - 1]], None, None]

            coms.remove(com)
            (t, F, R, pi_c, pi_v) = e
            for c in F:
                c.failed = True
            for c in R:
                c.failed = False

            if pi_v and pi_c:
                num_prop += 1
                pi_c.p_id = num_prop
                N.queue_message(Message(None, pi_c, "PROPOSE", pi_v))

        m = N.extract_message(t)
        if m:
            m.dst.deliver_message(m, t)

    tmp = [a.value for a in A]
    print("")
    for p in P:
        if tmp.count(p.value) >= round(len(tmp) / 2):
            print(f"{p.id} heeft wel consensus (voorgesteld: {p.org_value}, geaccepteerd: {A[0].value})")
        else:
            print(f"{p.id} heeft geen consensus (voorgesteld: {p.org_value}, geaccepteerd: {A[0].value})")

    return


# =============== EXECUTION =============== #
commands1 = [
    [0, "PROPOSE", 1, 42],
    [0, "END"]
]

commands2 = [
    [0, "PROPOSE", 1, 42],
    [8, "FAIL PROPOSER", 1],
    [11, "PROPOSE", 2, 37],
    [26, "RECOVER PROPOSER", 1],
    [0, "END"]
]

# simulate(1, 3, 15, commands1)
simulate(2, 3, 50, commands2)
