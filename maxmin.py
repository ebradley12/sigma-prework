def maxmin():
    numbers = input("Enter a list of numbers separated by a space: ").split()
    number_list = [int(num) for num in numbers]
    number_list.sort()
    return [number_list[-1], number_list[0]]

print(maxmin())