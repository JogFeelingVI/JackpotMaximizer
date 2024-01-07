# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2024-01-07 14:18:41
# @Last Modified by:   Your name
# @Last Modified time: 2024-01-07 16:51:37

import itertools, re


def find_same_numbers(list_of_lists, num_of_same_numbers):
    """
  Finds all the sublists in a list that have the same numbers.

  Args:
    list_of_lists: A list of lists, where each sublist contains a set of numbers.
    num_of_same_numbers: The number of numbers that must be the same in each sublist.

  Returns:
    A list of all the sublists that have the same numbers.
  """

    # Create a dictionary to store the sublists that have the same numbers.
    same_numbers_dict = {}

    # Iterate over the list of lists.
    for i, sublist in enumerate(list_of_lists):
        sub, line = sublist
        if sub == None:
            continue
        combinations_sublist = itertools.combinations(sub,
                                                      num_of_same_numbers)
        for com_sublist in combinations_sublist:
            sort_com_sublist = sorted(com_sublist)
            # Sort the sublist.

            # Convert the sorted sublist to a tuple.
            tuple_sublist = tuple(sort_com_sublist)

            # Add the tuple sublist to the dictionary, along with the original sublist.
            if tuple_sublist not in same_numbers_dict:
                same_numbers_dict[tuple_sublist] = [i]
            else:
                if i not in same_numbers_dict[tuple_sublist]:
                    same_numbers_dict[tuple_sublist].append(i)

    # Create a list to store the sublists that have the same numbers.
    same_numbers_list = []

    # Iterate over the dictionary.
    for tuple_sublist, sublists in same_numbers_dict.items():
        # If the number of sublists is greater than or equal to the number of same numbers, then add the sublists to the list.
        if len(sublists) >= 5:
            same_numbers_list.extend(sublists)

    # Return the list of sublists that have the same numbers.
    return same_numbers_list


def fromat_line(line: str):
    recs = [(re.compile(r'^(date|args).*'), lambda x: None),
             (re.compile(r'^\[-\]\s[ 0-9]+'), lambda x:[int(gz) for gz in x])]
    result = None
    for r, handle in recs:
        match = r.match(line)
        if match:
            result = handle(match.group(0).split()[1::])
            break
    return (result, line)


def main():
    print("Hello, World!")
    # Read the list of lists from the file.
    with open('save.log', 'r') as f:
        list_of_lists = [fromat_line(line=line) for line in f]

    # Find all the sublists that have 5 same numbers.
    same_numbers_list = find_same_numbers(list_of_lists, 5)

    # Print the sublists that have 5 same numbers.
    for i, index in enumerate(same_numbers_list):
        print(f'{i:>3}: {list_of_lists[index][1]}')


if __name__ == "__main__":
    main()
