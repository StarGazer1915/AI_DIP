from objects import Proposer, Acceptor, Message, Network


proposers = []
acceptors = []

proposers.append(Proposer("p1"))
acceptors.append(Acceptor("a1"))

N = Network("Network1", proposers, acceptors)
