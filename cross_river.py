from collections import OrderedDict


def can_cross(river, pos=0, speed=0):
    if pos > len(river) - 1:
        return True
    if river[pos] == '~':
        return False
    # For each rock, the set of speeds at which it is reachable
    riverdict = OrderedDict((rock_pos, set([])) \
                             for rock_pos in xrange(len(river)) \
                             if river[rock_pos] == '*')
    riverdict[pos].add(speed)
    for rock_pos in sorted(riverdict):
        possible_speeds = set([])
        for spd in riverdict[rock_pos]:
            possible_speeds.add(spd + 1)
            if spd > 0:
                possible_speeds.add(spd)
                if spd > 1:
                    possible_speeds.add(spd - 1)
        for spd in possible_speeds:
            new_pos = rock_pos + spd
            if new_pos >= len(river):
                return True
            if new_pos in riverdict:
                riverdict[new_pos].add(spd)
    return False


def can_cross_tests():
    crossable = ['',  # Empty string
                 '*',  # Single rock
                 # Pattern involving all combinations of speed changes,
                 # and water ending
                 '**~*~~*~~~*~~~~*~~~~*~~~~*~~~*~~*~~~*~~~~',
                 # Pattern involving all combinations of speed changes,
                 # and rock ending
                 '**~*~~*~~~*~~~~*~~~~*~~~~*~~~*~~*~~~*~~~~*',
                 # Long string of rocks
                 '*' * 10000]
    uncrossable = ['~',  # Start in water
                   '~*',  # Start in water with somewhere to go
                   '*~',  # Rock followed immediately by water
                   '**~*~~*~~~~',  # Pattern requiring too much acceleration
                   # # Pattern requiring too much deceleration
                   '**~*~~*~~~*~~~~*~~*~~~']

    for river in crossable:
        # Test successful rivers
        assert(can_cross(river))

        # Test same rivers when starting with non-zero speed
        assert(can_cross(river, 3, 3))

        # Test successful rivers when starting at non-zero position
        river = '~~~~~' + river
        assert(can_cross(river, 5))

    for river in uncrossable:
        # Test unsuccessful rivers
        assert not can_cross(river)

        # Test that rivers become crossable w/ the right nonzero initial speed
        if river[0] == '~':
            # Except when river starts in water
            assert(not can_cross(river, speed=15))
        else:
            assert(can_cross(river, speed=15))

        # Test unsuccessful rivers when starting at non-zero position
        river = '~~~~~' + river
        assert(not can_cross(river, 5))

    print "All tests pass"
