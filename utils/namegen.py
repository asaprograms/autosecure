import names

# generating random name for account

def random_first():
    return names.get_first_name()


def random_last():
    return names.get_last_name()


def random_name():
    return random_first(), random_last() 