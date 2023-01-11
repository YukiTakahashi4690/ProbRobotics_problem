import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import SubplotZero
import japanize_matplotlib

class compare_node:
    def __init__(self):
        self.t = []
        self.before_no = []
        self.after_no = []
        for data in range(0, 101, 1):
            self.t.append(data/100)

    #事前分布
    def prior_distribution(self):
        return np.full(101, 1/101)

    #p(a|t)
    #成功を"1" 失敗を"0"とする
    def pat(self, a, finish_rate):
        if a == "1":
            return finish_rate
        elif a == "0":
            return np.ones(101) - finish_rate

    #事後分布
    def posterior_distribution(self, pat, prior_distribution):
        return pat * prior_distribution / sum(pat * prior_distribution)

    #各試行の分布
    def find_distribution(self, list, posterior_distribution_list):
        prior = self.prior_distribution()
        posterior_distribution_list.append(prior)

        for i, j in enumerate(list):
            pat1 = self.pat(j, self.t)
            posterior = self.posterior_distribution(pat1, prior)
            prior = posterior
            posterior_distribution_list.append(posterior)

class draw_fig:
    def __init__(self):
        self.posterior_distribution_list = []
        self.ax = [0]*6

    def plot(self, x, graph_title, name):
        fig = plt.figure(figsize=(14, 10))

        for k in range(6):
            self.ax[k] = SubplotZero(fig, 2, 3, k+1)
            fig.add_subplot(self.ax[k])

            y = self.posterior_distribution_list[k]
            self.ax[k].plot(x, y)
            plt.grid()
            self.ax[k].set_xlabel('t')
            self.ax[k].set_ylabel('確率')
            self.ax[k].set_title(graph_title[k], y = -0.15)
            self.ax[k].set_xlim(0, 1)
            self.ax[k].set_ylim(0, 0.09)
        
        fig.tight_layout()
        fig.savefig("/home/y-takahashi/ProbRobotics_problem/fig/" + name + ".png", bbox_inches="tight")

class compare_node2:
    def __init__(self):
        self.before_no = []
        self.after_no = []

    def plot2(self, x2, name2):
        fig2 = plt.figure()
        ax1 = SubplotZero(fig2, 111)
        fig2.add_subplot(ax1)

        ax1.plot(x2, self.before_no[-1], label="改良前")
        ax1.plot(x2, self.after_no[-1], label="改良後")
        ax1.set_xlabel("t")
        ax1.set_ylabel("確率")
        ax1.legend(loc=0)
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 0.09)

        fig2.tight_layout()
        fig2.savefig("/home/y-takahashi/ProbRobotics_problem/fig/" + name2 + ".png", bbox_inches="tight")

#成功を"1" 失敗を"0"とする
def main():
    before = ["1", "0", "0", "1", "1"]
    after = ["1", "1", "1", "1", "1"]
    title = ["実験前", "最初の試行", "2回目の試行", "3回目の試行", "4回目の試行", "5回目の試行"]

    compe = compare_node()

    #改良前を各施行で計算
    p_1 = draw_fig()
    compe.find_distribution(before, p_1.posterior_distribution_list)
    p_1.plot(compe.t, title, "before")

    #改良後を各施行で計算
    p_2 = draw_fig()
    compe.find_distribution(after, p_2.posterior_distribution_list)
    p_2.plot(compe.t, title, "after")

    plt.show()

def main2():
	before2 = ["1", "0", "0", "1", "1"]
	after2 = ["1", "1", "1", "1", "1"]

	compe2 = compare_node()

	p1 = compare_node2()

	# 改良前と改良後の分布
	compe2.find_distribution(before2, p1.before_no)
	compe2.find_distribution(after2, p1.after_no)

	p1.plot2(compe2.t, "試行5回")

	# 改良前での50回の試行
	before_50 = ["1", "0", "0", "1", "1"]*10

	# 改良後での50回の試行
	after_50 = ["1", "1", "1", "1", "1"]*10

	p2 = compare_node2()

	# 改良前と改良後の分布を計算
	compe2.find_distribution(before_50, p2.before_no)
	compe2.find_distribution(after_50, p2.after_no)

	p2.plot2(compe2.t, "試行50回")
    

if __name__ == "__main__":
    main()
    main2()