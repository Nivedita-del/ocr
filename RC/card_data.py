import sys

from collections import defaultdict

from .card import load_card_file

def card_widths(cards, path):

    counts = defaultdict(int)
    for card in cards:
        width = card.right - card.left
        if 16 <= width and width <= 19:
            sys.stderr.write('%s: %s %s\n' % (width, path, card))
        counts[width] += 1
    return counts


def counts_to_list(counts):
    high_val = max(counts.keys())
    return [counts[x] for x in range(0, high_val + 1)]


if __name__ == '__main__':
    count_lists = []
    for path in sys.argv[1:]:
        cardpath = load_card_file(path)
        count_lists.append(counts_to_list(card_widths(cardpath, path)))

    max_width = max(len(x) for x in count_lists)

    print('\t'.join([''] + [str(x) for x in range(0, max_width)]))
    for path, counts in zip(sys.argv[1:], count_lists):
        print('%s\t%s' % (path, '\t'.join(str(x) for x in counts)))