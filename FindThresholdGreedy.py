from DataGeneration import *


# Attacker is smart, will pick the best voters for deletion.
# Defender decision is to protect those voters with minimum expense so that attacker objective to win does not meet
# So, here we apply the greedy approach
# First, we need to know how many votes we have to protect

def get_threshold(cndt, atkr, dfndr):
    already_spent = 0
    plt.figure()
    threshold = 10 ** 10

    # step 1: know the threshold by greedy method
    for i in cndt[:-1]:

        dist = dfndr.find_dist(i)
        av = atkr.atkr_cndt_vote
        print("Defender need to save at least {} for candidate {}".format(av, i.cid))
        distc = dist
        print("Gap between candidate {} and attacker candidate is {}".format(i.cid, dist))
        ranked_vtr = dfndr.rank_em_up(candidate=i)
        db = [0]
        ab = [atkr.find_min_cost(i, already_spent, distc + 1)]
        # print(ab)
        k = 0
        for j in ranked_vtr:

            if av >= 0:
                j.x = 1

                av = av - j.wt
                print(
                    "Defender defends voter {} to protect candidate {} and it total worth is {} votes. def cost is {} and "
                    "atk cost is {}".format(
                        j.vid, i.cid, j.wt, j.vdc, j.vac))
                db.append(db[k] + j.vdc)
                k += 1
                ab.append(atkr.find_min_cost(i, already_spent, distc + 1))
            else:
                break

        print("attacker axis values are {}".format(ab))
        print("defender axis values are {}".format(db))

        minab_index = ab.index(math.inf)
        mindb = db[minab_index]
        if mindb < threshold:
            threshold = mindb
        print("threshold value is {}".format(threshold))

    return threshold

    # plt.plot(db, ab)
# plt.show()
