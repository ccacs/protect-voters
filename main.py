from FindThresholdGreedy import *
from itertools import chain, combinations


def main(instance=3, prob="CPP"):
    color = ['r', 'g', 'b', 'm']
    itern = 1
    protection_rate = []
    while itern <= instance:

        cndt, vtr, national, atkr, dfndr = data_gen(prob)
        pvw, threshold = get_threshold(cndt, atkr, dfndr)

        # Step 2 start here
        def powerset(iterable):
            "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
            s = list(iterable)
            # return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))
            return chain.from_iterable(combinations(s, r) for r in range(len(s) // len(cndt)))

        oppv = []
        for x in vtr:
            if x.vfc != m:
                x.x = 0
                oppv.append(x)

        psv = list(powerset(oppv))
        # print(psv[1])

        cnt = 0
        X = []
        Y = []
        for s in psv:
            sumdb = 0

            for v in s:
                v.x = 0
                sumdb += v.vdc
            if sumdb < threshold:
                cnt += 1

                sumac = 0
                vlist = []

                if len(s) == 0:
                    for ci in cndt[:-1]:
                        dist2 = dfndr.find_dist(ci)
                        sumac += atkr.find_min_cost(ci, 0, dist2 + 1)
                        if sumac == math.inf:
                            break
                else:

                    for v in s:
                        v.x = 1
                        vlist.append(v.vid)

                        for ci in cndt[:-1]:
                            dist2 = dfndr.find_dist(ci)
                            sumac += atkr.find_min_cost(ci, 0, dist2 + 1)
                            if sumac == math.inf:
                                break
                if sumac != math.inf:
                    print("Defender is defending voter {}, which cost him {} ".format(vlist, sumdb))
                    X.append(sumdb)
                    print("The attacker needs {} to make this attack".format(sumac))
                    Y.append(sumac)

        print("Total number of point in solution space is {}".format(len(psv)))
        print("Total number of look up point in reduced search space is {},"
              "which is {}% of actual space.".format(cnt, 100 * (cnt / len(psv))))

        print(Y)
        print(X)

        record = np.column_stack((X, Y))
        record = record[record[:, 1].argsort()]
        record = record[record[:, 0].argsort()]
        try:
            max_val = record[0, 1]

            lr = len(record)
            del_row = []
            for i in range(1, lr):
                if record[i, 0] == record[i - 1, 0]:
                    del_row.append(i)
            record = np.delete(record, del_row, 0)

            lr = len(record)
            del_row = []
            for i in range(1, lr):
                # print(record[i, 1], max_val)
                if record[i, 1] <= max_val:
                    del_row.append(i)
                else:
                    max_val = record[i, 1]

            record = np.delete(record, del_row, 0)

            with plt.style.context("seaborn"):
                plt.figure(1)

                for i in range(1, len(record)):
                    plt.hlines(record[i, 1], record[i - 1, 0], record[i, 0], colors=color[itern])
                    try:
                        plt.vlines(record[i, 0], record[i, 1], record[i + 1, 1], colors=color[itern])
                    except:
                        pass

                plt.hlines(record[i, 1], record[-1, 0], threshold, colors=color[itern], label="instance {}".format(itern))

                # plt.plot(record[:, 0], record[:, 1], linestyle='dashed', marker='s', markersize=5)
                # plt.vlines(threshold, 0, max(record[:, 1]) + 100, linestyles="dashed")
            itern += 1
            protection_rate.append(pvw / national.total_wt())
        except:

            pass

    print("protection rate is {}".format(protection_rate))
    plt.title(prob)
    plt.xlabel("defense budget")
    plt.ylabel("threshold attack budget")
    plt.legend(loc='lower right')
    plt.show()


if __name__ == '__main__':
    main(prob="CPP")
