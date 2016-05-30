def _swap(x, y, items):
    pom = items[x]
    items[x] = items[y]
    items[y] = pom


def _partition(items, left, right):
    l = left
    r = right - 1
    pivot = left
    while (l != r):
        if (items[pivot] == items[l]):
            if (items[pivot] <= items[r]):
                r -= 1
            else:
                _swap(r, pivot, items)
                pivot = r
        else:
            if (items[pivot] >= items[l]):
                l += 1
            else:
                _swap(l, pivot, items)
                pivot = l
    return pivot


def _quicksort(items, l, r):
    if (l < r):
        pivot = _partition(items, l, r)
        _quicksort(items, l, pivot)
        _quicksort(items, pivot + 1, r)


def sort(items):
    new_items = list(items)
    _quicksort(new_items, 0, len(new_items))
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
