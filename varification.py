import numpy as np
import matplotlib.pyplot as plt

#完走率p(t)を求める関数
#完走を"1" 失敗を"0"とする
def cb_finish_rate(list):
    count = 0
    for data in list:
        if data == "1":
            count += 1

    pt = count/len(list)
    return pt

def main():
    before = ["1", "0", "0", "1", "1"]
    after = ["1", "1", "1", "1", "1"]

    pt = cb_finish_rate(before)
    print("改良前の完走率p(t): ", pt)
    pt = cb_finish_rate(after)
    print("改良後の完走率p(t): ", pt)

    before.append("1")
    pt = cb_finish_rate(before)
    print("改良前の完走率(6回目成功): ", pt)
    after.append("1")
    pt = cb_finish_rate(after)
    print("改良後の完走率(6回目成功): ", pt)

    before.append("0")
    pt = cb_finish_rate(before)
    print("改良前の完走率(6回目失敗): ", pt)
    after.append("0")
    pt = cb_finish_rate(after)
    print("改良後の完走率(6回目失敗): ", pt)

if __name__ == "__main__":
    main()