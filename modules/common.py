#
# Contains pretty print functions
#

def status_print(prop, line1, line2):
    """
    Print a 'current progress' line.
    """
    if prop.packaging:
        return

    if prop.verbose:
        print(line1, line2)
        return

    print("\033[K-> " + line1)
    print("\033[K   " + line2, end="\r")
    print("\033[F\033[F")


def status_clear(prop):
    """
    Clear the 'current progress' line.
    """
    if prop.verbose or prop.packaging:
        return

    print("\033[K                                         ")
    print("\033[K                                         ", end="\r")
