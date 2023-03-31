# @Author: JogFeelingVi
# @Date: 2023-03-30 23:06:20
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2023-03-30 23:06:20


def is_uncorrelated(a, b):
    n = len(a)
    avg_a = (sum(a) / n)
    avg_b = (sum(b) / n)

    covariance = sum((a[i] - avg_a) * (b[i] - avg_b) for i in range(n))
    std_dev_a = ((sum([(x - avg_a)**2 for x in a]) / n))**0.5
    std_dev_b = ((sum([(x - avg_b)**2 for x in b]) / n))**0.5

    pearson_corr = covariance / (n * std_dev_a * std_dev_b)
    return abs(pearson_corr) < 0.4


if __name__ == '__main__':
    a = [1, 4, 9, 10, 20, 33]
    c = [1, 4, 19, 21, 25, 33]
    b = [2, 3, 9, 11, 12, 17]
    print(is_uncorrelated(c, b))