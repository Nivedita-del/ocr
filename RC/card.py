import sys

class cardline(object):
    def __init__(self, text, left, up, right, down, page):
        self.text = text
        self.right = int(right)
        self.left = int(left)
        self.up = int(up)
        self.down = int(down)
        self.page = int(page)

    @staticmethod
    def parse_line(line):
        try:
            text, left, down, right, up, page = line.split(' ')
        except ValueError as e:
            sys.stderr.write('line is disorted: "%s"' % line)
            raise e
        return cardline(text, left, down, right, up, page)

    def __repr__(self):
        return ' '.join(str(x) for x in [
            self.text,
            self.left,
            self.down,
            self.up,
            self.page])


def load_card_file(path):
    output = []
    for line in open(path):
        output.append(cardline.parse_line(line))
    return output