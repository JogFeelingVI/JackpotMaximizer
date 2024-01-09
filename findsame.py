# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2024-01-07 14:18:41
# @Last Modified by:   Your name
# @Last Modified time: 2024-01-09 16:58:17

import itertools, re, time
from codex import Tonji


def main():
    print(f'====== {time.time()} ======')
    tjone = Tonji.statistics()
    # Read the list of lists from the file.
    with open('fps.log', 'r') as f:
        list_of_lists = [tjone.parse_fps(line=line) for line in f]
    for lol in list_of_lists:
        tjone.add(lol)
    tjone.echo(lines=(33,976))

if __name__ == "__main__":
    main()
