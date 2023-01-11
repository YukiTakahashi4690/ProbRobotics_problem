# ProbRobotics_problem  
確率ロボティクス課題リポジトリ  

## 開発環境  
* OS:Ubuntu20.04  
* python:3.8.10  
* numpy:1.17.4  
* matplotlib:3.1.2  

## 結果及び計算から帰結されること  
C君が改良前と改良後のそれぞれで行った5回の試行において, 事前分布と事後分布を求めて, 実験結果を比較した.  
結果は以下のようになった.  

改良前  
<img src="https://github.com/YuukiTakahashi4690/ProbRobotics_problem/blob/master/fig/before.png" width="50%">  
<br>  
改良後  
<img src="https://github.com/YuukiTakahashi4690/ProbRobotics_problem/blob/master/fig/after.png" width="50%">  
<br>  
改良前と改良後を重ねて比較(5回目)  
<img src="https://github.com/YuukiTakahashi4690/ProbRobotics_problem/blob/master/fig/%E8%A9%A6%E8%A1%8C5%E5%9B%9E.png" width="50%">  
<br>  

|| 完走率p(t) |  
| ---- | ---- |  
| 改良前 | 0.6 |  
| 改良後 | 1.0 |  

重ねて比較したグラフから, 改良前の完走率は0.6, 改良後の完走率は1.0であり, 改良後の方が0.4高い.  
このことから, 改良後のほうが完走率が高いと言える.  
しかし, 分布の重なりがあるため, 改良前と改良後のそれぞれで, 6回目以降の試行を行うと, "成功", "失敗"のどちらかになるかで, 結果が変わる可能性があると考えられる.  
そこで, 試行回数をそれぞれ10倍してみることで, 変化があるか検証した.  
結果は, 以下のようになった.  
<br>  
改良前と改良後を重ねて比較(50回目)  
<img src="https://github.com/YuukiTakahashi4690/ProbRobotics_problem/blob/master/fig/%E8%A9%A6%E8%A1%8C50%E5%9B%9E.png" width="50%">  
<br>  

|| 完走率p(t) |  
| ---- | ---- |  
| 改良前 | 0.6 |  
| 改良後 | 0.95 |  

試行を50回に増やした場合, 改良前の完走率は0.6前後, 改良後の完走率は0.95前後となり, 改良後の方が0.35前後高いと言える.  
このことから, 改良後の方が完走する可能性が高い可能性がある.  
また, 改良前と改良後での分布の重なりがなくなり, 完走率tの値が逆転する可能性は低いと考えられる.  

## 開発したプログラム  
* [compe.py](https://github.com/YuukiTakahashi4690/ProbRobotics_problem/blob/master/compe.py)   
成功を"1", 失敗を"0"として改良前と改良後をそれぞれ次のように定義した.  
* 改良前 = ["1", "0", "0", "1", "1"]  
* 改良後 = ["1", "1", "1", "1", "1"]  
<br>

以下に, コードを示す.  
``` python  
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import SubplotZero
import japanize_matplotlib
```  
↑&ensp;必要なライブラリのインポート  

``` python  
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
```  
↑&ensp;施行後の確率分布を算出  

``` python  
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
```  
↑&ensp;改良前と改良後それぞれを別々に描画  

``` python  
class compare_node2:
    def __init__(self):
        self.before_no = []
        self.after_no = []

    def plot2(self, x2, name2):
        fig2 = plt.figure()
        ax1 = SubplotZero(fig2, 111)
        fig2.add_subplot(ax1)

        ax1.plot(x2, self.before_no[-1], label="before")
        ax1.plot(x2, self.after_no[-1], label="after")
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
```  
↑&ensp;改良前と改良後を比較と描画(試行回数5回と50回)
