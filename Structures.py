from gurobipy import *
import random
import knapsack
import math
import matplotlib.pyplot as plt
import numpy as np

'''
size = [21, 11, 15, 9, 34, 25, 41, 52] #size is equivalent to vac
weight = [22, 12, 16, 10, 35, 26, 42, 53] #weight is the equivalent to wt
capacity = 100 #capacity is equivalent to budget
a , b = (knapsack.knapsack(size, weight).solve(capacity))
print(a)
'''


class Voter:

    def __init__(self, vid, wt, vfc, vac, vdc, x=0, y=0):
        self.vid = vid  # voter id
        self.vfc = vfc  # voter favorite candidate
        self.vac = vac  # * wt // 10  # voter attacking cost
        self.vdc = vdc  # * wt // 10  # voter defending cost
        self.wt = wt  # voter weight
        self.x = x
        self.y = y


class Candidate:

    def __init__(self, cid):
        self.cid = cid  # candidate id

    def score(self, vtr):  # vtr is the list of all voters, it outputs the score for a candidate
        vcnt = 0  # voters count
        wcnt = 0  # weight or casted vote count

        for i in vtr:

            if i.x == 1 or i.y == 0:
                if i.vfc == self.cid:
                    wcnt += i.wt
                    vcnt += 1

        return wcnt, vcnt


class Election:

    def __init__(self, vtr, cndt):
        self.vtr = vtr  # vtr is the list of all voters
        self.cndt = cndt  # cndt is the list of all candidates including the attacker's candidate

    def winner(self):  # returns the winner candidate id 'cid' and his number of votes
        mcast = 0
        wnr = -1

        for i in self.cndt:

            cast, _ = i.score(self.vtr)

            if cast > mcast:
                mcast = cast
                wnr = i

        return wnr, mcast

    def stats(self):  # prints the number of votes for each candidate

        for i in self.cndt:
            wcnt, vcnt = i.score(self.vtr)

            print("candidate {} received {} votes from {} voters".format(i.cid, wcnt, vcnt))

    def total_wt(self):
        s = 0
        for i in self.vtr:
            s += i.wt

        return s


class Defender:

    def __init__(self, vtr, cndt):
        self.vtr = vtr
        self.cndt = cndt[:-1]
        self.atkr_cndt = cndt[-1]
        self.atkr_cndt_vote, _ = self.atkr_cndt.score(vtr)

    def find_dist(self, candidate):
        wcnt, vcnt = candidate.score(self.vtr)

        return wcnt - self.atkr_cndt_vote

    def rank_em_up(self, candidate):

        s = {}
        for i in self.vtr:

            if i.vfc == candidate.cid:
                s[i] = (i.vac / i.wt)

        si = dict(sorted(s.items(), key=lambda item: item[1]))

        return si.keys()


class Attacker:

    def __init__(self, vtr, cndt):
        self.vtr = vtr
        self.cndt = cndt[:-1]
        self.atkr_cndt = cndt[-1]
        self.atkr_cndt_vote, _ = self.atkr_cndt.score(vtr)

    def attack(self, atk_cndt, budget):
        # returns the minimum budget to win else infinity

        # find those voters weight and cost which are not defended by the defender

        cost = []
        weight = []

        for i in self.vtr:
            # print(i.x, i.vfc, atk_cndt.cid)
            if i.x == 0 and i.vfc == atk_cndt.cid:
                # print("in")
                cost.append(i.vac)
                weight.append(i.wt)
        # print(cost)
        # print(weight)
        # attacker has to attack atk_cndt at least min-vt amount votes

        total_attacked, _ = knapsack.knapsack(cost, weight).solve(budget)
        # print(_)

        return total_attacked

    def find_min_cost(self, atk_cndt, already_spent, target, epsilon=0):
        # print("Attacker target is at least {}".format(target))
        # find max budget
        maxB = []
        for i in self.vtr:
            if i.vfc == atk_cndt.cid:
                maxB.append(i.vac)
                minc = min(maxB)
        maxB = sum(maxB)

        maxB = maxB - already_spent

        result = math.inf
        atk_cndt_vote, _ = atk_cndt.score(self.vtr)
        if maxB < minc:

            pass

        else:
            wtgain = self.attack(atk_cndt, maxB)
            # print(wtgain, atk_cndt_vote -  gap)
            # wtgain < atk_cndt_vote - gap + 1:
            if wtgain < target:

                pass
            else:
                # print('here')
                # binary search
                left, right = minc, maxB

                while left < right:
                    # print(left, right, wtgain, target)
                    budget = left + (right - left) // 2
                    wtgain = self.attack(atk_cndt, budget)
                    if target - epsilon <= wtgain <= target + epsilon:

                        result = budget
                        break

                    else:
                        if wtgain > target + epsilon:
                            right = budget
                            result = budget
                        else:
                            left = budget + 1

                    budget = left + (right - left) // 2
        '''
        wtgain = self.attack(atk_cndt, result)
        
        if result < math.inf:
            print("Attacker total gain is {}, winning budget is {}".format(wtgain, result))
        else:
            print("Infeasible to attack")'''
        return result
