from objects import Computer, Message, Network


def create_computers(c_num, c_type, N, A, L):
    """
    This function creates an array of computers for use in the paxos algorithm.
    This function can be used to create proposers, acceptors and learners.
    It assigns the Network queue to the computer so it is linked with it at all
    time and can queue new messages if needed.
    @param c_num: int
    @param c_type: str
    @param N: Network object
    @param A: list (Computer objects)
    @param L: list (Computer objects)
    @return:
    """
    tmp = []
    for i in range(1, c_num + 1):
        tmp.append(Computer(f"{c_type[0]}{i}", c_type, N, A, L))
    return tmp


def simulate(n_p, n_a, n_l, tmax, coms):
    """
    1. First the Network, lists with computers and proposer id counter are initialized.
    2. Then the simulation starts and it will loop until the max tick (tmax) has been reached.
    3. The tick is formatted to be used in print statements and the first command is taken from coms.
        3.1 If a command doesn't exist it gives com the value None instead.
    4. If the command exists it will format the command into the proper event.
    5. Now that the event is made the command is removed from the command list and the failed machines
       are put to sleep or the to be recovered machines are recovered.
    6. If the event is a PROPOSE event it will queue that message to propose the value.
    7. Then a message from the queue is extracted and delivered to it's destination if the message exists.
    8. Eventually (after the simulation loop) the majority is calculated and the consensus result is shown.
    @param n_p: int
    @param n_a: int
    @param n_l: int
    @param tmax: int
    @param coms: list
    @return: void
    """
    num_prop = 0

    #= 1 =#
    N = Network("N1")
    A = create_computers(n_a, "ACCEPTOR", N, [], [])
    L = create_computers(n_l, "LEARNER", N, A, [])
    P = create_computers(n_p, "PROPOSER", N, A, L)

    #= 2 =#
    for t in range(tmax):
        if len(N.queue) == 0 and len(coms) == 0:
            return

        #= 3 =#
        tick = str(t).zfill(len(str(tmax)))
        com = coms[0]
        if com[0] != t:
            com = None

        #= 4 =#
        if com:
            e = com
            if "END" in com:
                continue
            elif "PROPOSE" in com:
                e = [com[0], [], [], P[com[2] - 1], com[3]]
            elif "FAIL PROPOSER" in com:
                print(f"{tick}: ** P{com[2]}  kapot **")
                e = [com[0], [P[com[2] - 1]], [], None, None]
            elif "RECOVER PROPOSER" in com:
                print(f"{tick}: ** P{com[2]}  gerepareerd **")
                e = [com[0], [], [P[com[2] - 1]], None, None]

            #= 5 =#
            coms.remove(com)
            (t, F, R, pi_c, pi_v) = e
            for c in F:
                c.failed = True
            for c in R:
                c.failed = False

            #= 6 =#
            if pi_v and pi_c:
                num_prop += 1
                pi_c.p_id = num_prop
                N.queue_message(Message(None, pi_c, "PROPOSE", pi_v))

        #= 7 =#
        m = N.extract_message(tick)
        if m:
            m.dst.deliver_message(m, tick)

    #= 8 =#
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

commands3 = [
    [0, "PROPOSE", 1, "nl: g"],
    [100, "PROPOSE", 1, "nl:ga"],
    [200, "PROPOSE", 1, "nl:af"],
    [300, "PROPOSE", 1, "nl:f"],
    [400, "PROPOSE", 1, "en: g"],
    [500, "PROPOSE", 1, "en:gr"],
    [600, "PROPOSE", 1, "en:re"],
    [700, "PROPOSE", 1, "en:ea"],
    [800, "PROPOSE", 1, "en:at"],
    [900, "PROPOSE", 1, "en:t"],
    [0, "END"]
]

# simulate(1, 3, 0, 15, commands1)
simulate(2, 3, 0, 50, commands2)
# simulate(1, 3, 1, 10000, commands3)
