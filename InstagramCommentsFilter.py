import sys
import csv

__author__ = 'mfv'


class FilterCoveyor:
    def __init__(self):
        self.wordFilters = []
        self.messageFilters = []

    def apply_whole_filters_on_message(self, message):
        filtered = message
        for currentFilter in self.wordFilters:
            filtered = self.apply_word_filter_on_message(filtered, currentFilter)
        for currentFilter in self.messageFilters:
            filtered = self.apply_message_filter_on_message(filtered, currentFilter)
        return filtered

    @staticmethod
    def apply_word_filter_on_message(message, predicate):
        """
        apply predicate to each word if message
        :rtype : filtrated message
        :param message: some message to filter
        :param predicate: filter(str) -> bool
        """
        words = message.split()
        return " ".join(
            filter(lambda o: True if o is not None else False, map(lambda s: s if predicate(s) else None, words)))

    @staticmethod
    def apply_message_filter_on_message(message, f):
        """
        apply f to whole message
        :rtype : filtered message
        :param message: some message to filter
        :param f: filter(message) -> message
        """
        return f(message)


def filter_person_link(word) -> bool:
    return True if not word.startswith("@") else False


def filter_add_endline(message) -> str:
    return message + "\n"


def main():
    sourceFileFolder = sys.argv[1]  # file-path to csv comments
    destFileFolder = sys.argv[2]  # file-path to clear comments
    filters = FilterCoveyor()
    filters.messageFilters.append(filter_add_endline)
    filters.wordFilters.append(filter_person_link)
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
    main()
