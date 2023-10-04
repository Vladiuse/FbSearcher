from pprint import pprint


def devine_array(array, parts_count):
    if parts_count <= 1 or parts_count > len(array):
        raise TypeError('invalid param')
    result_len = len(array) // parts_count
    fix_num = len(array) % parts_count
    parts = []
    part = []
    for elem in array:
        part.append(elem)
        curr_array_len = result_len + (1 if len(parts) < fix_num else 0)
        if len(part) == curr_array_len:
            parts.append(part)
            part = []
    return parts



if __name__ == '__main__':
    li = [1,2,3,4,5,6]
    pprint(devine_array(li,5))
