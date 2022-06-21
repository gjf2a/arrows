from menus import menuManyOptions

labels = ['Default'] + ['S' + str(n) for n in range(1, 5)]
actions = ['Forward', 'Backward', 'Left', 'Right', 'Stop']

def setup(ev3, left, right):
    menuManyOptions(ev3, labels, [actions] * len(labels))