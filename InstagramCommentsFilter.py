import sys
import csv
import collections

__author__ = 'mfv'


class FilterCoveyor:
    def __init__(self):
        self.wordModifyFilters = []  # f(str) -> iterable
        self.wordReplaceFilters = []  # f(str) -> bool
        self.messageFilters = []  # f(str) -> str

    def apply_whole_filters_on_message(self, message):
        tokens = message.split()
        modified = []
        for f in self.wordModifyFilters:
            for token in tokens:
                currentResult = f(token)
                if isinstance(currentResult, collections.Iterable):
                    modified.extend(currentResult)
                else:
                    modified.append(currentResult)
        tokens = modified
        modified = []
        for f in self.wordReplaceFilters:
            for token in tokens:
                if f(token):
                    modified.append(token)
        modified = " ".join(modified)
        for f in self.messageFilters:
            modified = f(modified)
        return modified


def filter_person_link(word) -> bool:
    return True if not word.startswith("@") else False


def filter_hashtag_link(word) -> iter:
    words = word.split("#")
    return filter(lambda s: True if len(s) > 0 else False, words)


def filter_add_endline(message) -> str:
    return message + "\n"


def main():
    sourceFileFolder = sys.argv[1]  # file-path to csv comments
    destFileFolder = sys.argv[2]  # file-path to clear comments
    filters = FilterCoveyor()
    filters.wordModifyFilters.append(filter_hashtag_link)
    filters.wordReplaceFilters.append(filter_person_link)
    filters.messageFilters.append(filter_add_endline)
    with open(sourceFileFolder, "rt") as source:
        with open(destFileFolder, "w") as dest:
            csvReader = csv.reader(source)
            csvReader.__next__()
            counter = 0
            for row in csvReader:
                dest.write(filters.apply_whole_filters_on_message(row[2]))
                counter += 1
                if counter == 100:
                    break


if __name__ == '__main__':
    l = []
    l.extend([2])
    l.extend([[4, 5, 6]])
    print(isinstance(l, collections.Iterable))
    main()
