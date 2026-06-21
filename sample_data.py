from process import Process

def case_1():
    return [
        Process("P1", 0, 5, 2),
        Process("P2", 1, 3, 1),
        Process("P3", 2, 8, 4)
    ]


def case_2():
    return [
        Process("P1", 0, 10, 3),
        Process("P2", 0, 4, 1),
        Process("P3", 0, 6, 2),
        Process("P4", 0, 2, 4)
    ]


def case_3():
    return [
        Process("P1", 7, 8, 2),
        Process("P2", 5, 2, 2),
        Process("P3", 0, 8, 5),
        Process("P4", 0, 4, 5),
        Process("P5", 2, 8, 1)
    ]