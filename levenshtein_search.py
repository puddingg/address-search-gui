import Levenshtein as Shtein
import pandas as pd
from collections import defaultdict


class Levenshtein_Search():
    def __init__(self):
        # tolerance
        self.tolerance = 5

        # read csv file into pandas.DataFrame
        path = './resources/zenkoku.csv'
        self.df = pd.DataFrame
        with open(path, 'r') as f:
            self.df = pd.read_csv(f, index_col='住所CD', na_filter=False)

        # create address string by concatenating each component
        # better if 通り名 was taken into consideration on this operation here
        self.df.loc[:, '住所文字列'] = ''
        self.df.loc[self.df.事業所フラグ == 0, '住所文字列'] = self.df['都道府県'] + \
            self.df['市区町村'] + self.df['町域'] + self.df['字丁目']
        self.df.loc[self.df.事業所フラグ == 1, '住所文字列'] = self.df['都道府県'] + \
            self.df['市区町村'] + self.df['事業所住所']

        # drop unneeded columns/rows
        self.df = self.df.loc[:, ['住所文字列']]
        self.df.drop_duplicates(inplace=True)

        # make sure there is no empty row left
        # print(self.df.loc[self.df.住所文字列 == ''])
        # print(self.df)

    def distance(self, str1, str2):
        """just call Levenshtein.distance() """

        return Shtein.distance(str1, str2)

    def norm_distance(self, str1, str2):
        """return Levenshtein distance normalized by the length of the given string (longer one)

        :param str1: string1
        :type str1: str
        :param str2: string2
        :type str2: str
        :return: normalized Levenshtein distance
        :rtype: float
        """

        dis = self.distance(str1, str2)
        n1 = len(str1)
        n2 = len(str2)
        if n1 >= n2:
            return dis / n1
        else:
            return dis / n2

    def search(self, input):
        """do address search using normalized Levenshtein Distance

        :param input: full or a part of address attempt to search
        :type input: str
        :return: dict of most similar address strings with normalized Levenshtein distance as those keys  
        :rtype: defaultdict
        """

        rslt = defaultdict(list)
        for address in self.df.loc[:, '住所文字列']:
            dis = self.norm_distance(address, input)

            # initial append until tolerance
            if len(rslt) < self.tolerance:
                rslt[str(dis)].append(address)
                continue

            # collect the minimum distances
            largest = max(rslt.keys())
            if dis < float(largest):
                rslt[str(dis)].append(address)
                del rslt[str(largest)]

        return rslt


if __name__ == '__main__':
    LS = Levenshtein_Search()
    result = LS.search('東大阪川俣')
    for dis, lst in result.items():
        print(dis)
        for address in lst:
            print(address)
