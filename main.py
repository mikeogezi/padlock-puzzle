'''
  Some people on my computer science group seem to have too much free time during this COVID-19
  pandemic.

  The following is an attempt to solve one of the questions set forth by one of the more idle members
  of the group.

  Enjoy!
'''

one_right_but_in_wrong_pos_1 = list(map(int, '147'))
one_right_but_in_wrong_pos_2 = list(map(int, '286'))
one_right_and_in_correct_pos = list(map(int, '189'))
all_wrong = list(map(int, '523'))

two_right_but_both_in_wrong_pos = list(map(int, '964'))

pin_len = 3

def get_init_search_space ():
  return list(map(lambda x: list(range(10)), range(pin_len)))

def remove (trimmed_search_space, jdx, i):
  try:
    trimmed_search_space[jdx].remove(i)
  except ValueError:
    pass

def collapse (search_space):
  vals = set()
  for i in search_space[0]:
    for j in search_space[1]:
      for k in search_space[2]:
        vals.add(''.join(list(map(str, [i, j, k]))))
  return list(vals)
  #   assert search_space[i].__len__() == 1
  # return ''.join(list(map(lambda x: str(x[0]), search_space)))

def flatten_and_dedup (search_space):
  vals = set()
  for i in search_space:
    for j in i:
      vals.add(j)
  return list(vals)

def main ():
  trimmed_search_space = get_init_search_space()

  # filter out all wrong => '523'
  for i in all_wrong:
    for jdx, _ in enumerate(trimmed_search_space):
      remove(trimmed_search_space, jdx, i)
  # right but in wrong position => '286', '147'
  print('Search space:', trimmed_search_space)

  # one_right_and_in_correct_pos, one_right_but_in_wrong_pos
  # print(list(one_right_and_in_correct_pos), list(one_right_but_in_wrong_pos_1))
  wrong_idxs = []
  for idx, i in enumerate(one_right_and_in_correct_pos):
    for jdx, j in enumerate(one_right_but_in_wrong_pos_1):
      # print(idx, jdx, i, j)
      if idx == jdx and i == j:
        remove(trimmed_search_space, idx, i)
        wrong_idxs.append(idx)
    for kdx, k in enumerate(one_right_but_in_wrong_pos_2):
      # print(idx, kdx, i, k)
      if idx == kdx and i == k:
        remove(trimmed_search_space, idx, i)
        wrong_idxs.append(idx)
  # recall that one is right and in right pos
  # it'll be the one that wasn't removed from `one_right_and_in_correct_pos`
  if wrong_idxs.__len__() == 2:
    diff_set = set(range(pin_len)) - set(wrong_idxs)
    # only one value here
    disc_pos = diff_set.pop()
    disc_val = one_right_and_in_correct_pos[disc_pos]
    trimmed_search_space[disc_pos] = [ disc_val ]
    # recall one_right_but_in_wrong_pos_1
    one_right_but_in_wrong_pos_set = set()
    one_right_but_in_wrong_pos_set.add(one_right_but_in_wrong_pos_1[disc_pos])
    one_right_but_in_wrong_pos_set.add(one_right_but_in_wrong_pos_2[disc_pos])
    # set to positions that haven't yet been discovered
    for i in range(pin_len):
      if disc_pos != i:
        trimmed_search_space[i] = list(one_right_but_in_wrong_pos_set)
  print('Search space:', trimmed_search_space)
  # reset
  wrong_idxs = []

  # find what is completely wrong in `two_right_but_both_in_wrong_pos`
  # it won't be in any of our currently trimmed choices
  for idx, i in enumerate(two_right_but_both_in_wrong_pos):
    # after isolating `removed_idx` we can be sure that the other two vals are correct but definitely in wrong positions
    if i not in flatten_and_dedup(trimmed_search_space):
      wrong_idxs.append(idx)
    else:
      # print(idx, i)
      remove(trimmed_search_space, idx, i)

  # print(wrong_idxs)
  print('Search space:', trimmed_search_space)
  
  # remove choices with repeating vals
  answer = list(filter(lambda x: set(x).__len__() == x.__len__(), collapse(trimmed_search_space)))
  
  assert answer.__len__() == 1
  print('Answer:', answer[0])

if __name__ == '__main__':
  main()