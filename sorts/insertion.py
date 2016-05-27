def sort(items):
    sorted_items = [i for i in items]

    for i in range(1, len(sorted_items)):
        k = i
        while(k >= 1 and sorted_items[k] < sorted_items[k - 1]):
            pom = sorted_items[k]
            sorted_items[k] = sorted_items[k - 1]
            sorted_items[k - 1] = pom
            k -= 1

    return sorted_items


items = [3, 4, 7, 4, 5, 7]
print(sort(items))

items = [3, 4, 7, -4, 0, 87, -98, 5, 7]
print(sort(items))

items = [1, 1, 1]
print(sort(items))

items = [1]
print(sort(items))

items = []
print(sort(items))
