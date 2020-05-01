import sys

class cardline(object):
    def __init__(self, alpha, left, top, right, bottom, page):
        self.alpha = alpha
        self.right = int(right)
        self.left = int(left)
        self.top = int(top)
        self.bottom = int(bottom)
        self.page = int(page)

    @staticmethod
    def parse_line(line):
        try:
            alpha, left, bottom, right, top, page = line.split(' ')
        except ValueError as e:
            sys.stderr.write('line is disorted: "%s"' % line)
            raise e
        return cardline(alpha, right, left, top, bottom, page)

    def __repr__(self):
        return ' '.join(str(x) for x in [
            self.alpha,
            self.left,
            self.bottom,
            self.top,
            self.page])


def load_card_file(path):
    output = []
    for line in open(path):
        output.append(cardline.parse_line(line))
    return output