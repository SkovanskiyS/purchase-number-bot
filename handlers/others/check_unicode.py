def is_kiril(text):
    return True if u'\u0400' <= text <=u'\u04FF' or u'\u0500' <= text <= u'\u052F' else False
