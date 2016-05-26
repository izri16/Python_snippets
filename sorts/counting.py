def _find_min_max(items):
    min_item = float('inf')
    max_item = -float('inf')

    for item in items:
        if (item < min_item):
            min_item = item
        if (item > max_item):
            max_item = item

    return (min_item, max_item)


def _get_occurencies(items, offset, items_range):
    occurencies = [0 for i in range(items_range + 1)]
    for item in items:
        occurencies[item - offset] += 1
    return occurencies


def _get_sum_count(occurencies):
    sum_count = []
    sum_count.append(occurencies[0])
    count = occurencies[0]

    for i in range(1, len(occurencies)):
        count += occurencies[i]
        sum_count.append(count)

    return sum_count


def sort(items):
    if (not len(items)):
        return items

    min_item, max_item = _find_min_max(items)
    occurencies = _get_occurencies(items, min_item, max_item - min_item)
    sum_count = _get_sum_count(occurencies)

    sorted_array = [0 for i in items]
    for item in reversed(items):
        sum_count[item - min_item] -= 1
        sorted_array[sum_count[item - min_item]] = item
    return sorted_array

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
