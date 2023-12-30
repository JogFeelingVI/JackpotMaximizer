# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2023-12-30 09:53:51
# @Last Modified by:   Your name
# @Last Modified time: 2023-12-30 11:12:51

from typing import List


class bayes:

    def __init__(
        self,
        histories: List[int],
    ) -> None:
        self.histories = histories
        self.n = [16, 33][max(histories) > 16.01]
        

    def PLM(self, EHL: List[int]):
        p_h = 1 / self.n
        p_e_given_h = sum(x in EHL
                          for x in self.histories) / len(self.histories)
        p_e = sum(x in range(1, self.n + 1)
                  for x in self.histories) / len(self.histories)
        p_h_given_e = (p_e_given_h * p_h) / p_e
        possible_lottery_numbers = list(range(1, self.n+1))
        probabilities = []
        for i in range(self.n):
            p_e_given_h_i = sum(x == possible_lottery_numbers[i] for x in self.histories) / len(self.histories)
            p_h_given_e_i = (p_e_given_h_i * p_h) / p_e
            probabilities.append(p_h_given_e_i)
            
        sorted_lottery_numbers = sorted(range(len(probabilities)), key=lambda k: probabilities[k], reverse=True)
        print('Possible lottery numbers:')
        for i in range(33):
            print(f"{i+1}. {possible_lottery_numbers[sorted_lottery_numbers[i]]}")



def main():
    print("Hello, World!")


if __name__ == "__main__":
    main()
