def _merge(left_items, right_items, items):
    i = 0
    j = 0
    k = 0

    while (i < len(left_items) and j < len(right_items)):
        if (left_items[i] < right_items[j]):
            items[k] = left_items[i]
            i += 1
        else:
            items[k] = right_items[i]
            j += 1
        k += 1

    while (i < len(left_items)):
        items[k] = left_items[i]
        i += 1
        k += 1

    while (j < len(right_items)):
        items[k] = right_items[j]
        j += 1
        k += 1


def _merge_sort(items):
    if (len(items) < 2):
        return
    else:
        middle = len(items) // 2
        left_items = items[:middle]
        right_items = items[middle:]
        _merge_sort(left_items)
        _merge_sort(right_items)
        _merge(left_items, right_items, items)


def sort(items):
    new_items = list(items)
    _merge_sort(new_items)
    return new_items

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
