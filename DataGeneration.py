from Structures import *

# Generate the data


n = 25  # number of voters
m = 2  # number of candidates (without the attacker's preference candidate)
pntg = .80  # percentage of votes attacker candidate(m+1) get
lwt = 1  # lower bound of weight
uwt = 3  # upper bound of weight
lvac = 10  # lower bound of weight
uvac = 100  # upper bound of weight
lvdc = 10  # lower bound of weight
uvdc = 100  # upper bound of weight
sd = random.randint(0, 25)  # seed
random.seed(sd)


def data_gen():
    cndt = []
    for i in range(m + 1):
        cndt.append(Candidate(i))

    validation = False

    while not validation:
        vtr = []
        for i in range(n):

            r = random.random()
            if r > pntg:
                vfc = m
            else:
                vfc = random.randint(0, m - 1)

            vtr.append(Voter(vid=i, wt=random.randint(lwt, uwt), vfc=vfc,
                             vac=random.randint(lvac, uvac), vdc=random.randint(lvdc, uvdc)))

            validation = True
            awc, avc = cndt[-1].score(vtr)
            for z in cndt[:-1]:
                wc, vc = z.score(vtr)
                if wc <= awc:
                    validation = False
                    print("Validation Failed. Running generating the voter list again -> -> ->")

    national = Election(vtr, cndt)
    national.stats()
    atkr = Attacker(vtr, cndt)
    dfndr = Defender(vtr, cndt)

    return cndt, vtr, national, atkr, dfndr
