def numbered_strings_from_list(items: list):
    numbered_strings = []
    for index, item in enumerate(items):
        numbered_strings.append(f'{index+1}: {item}')
    return numbered_strings
