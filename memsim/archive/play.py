def find_and_remove(lst, n):
  result = [] 
  consec = 1
  prev = lst[0] - 1

  for i, num in enumerate(lst):
    if num == prev + 1:
      result.append(num)
      consec += 1
    else:
      consec = 2
      result = [num]
    
    if consec > n:
        return [result, list(set(lst)-set(result))]
    prev = num

nums = [1, 2, 3, 4, 5, 7, 9, 10, 12]