from collections import defaultdict, Counter
import re
import pandas as pd

pd.set_option('display.max_columns', 500)


class Address_Dict:
    def __init__(self):
        path = './resources/zenkoku.csv'
        self.df = pd.DataFrame
        with open(path, 'r') as f:
            self.df = pd.read_csv(f, index_col='住所CD', na_filter=False)
        # print(self.df.columns.values)

        # 住所文字列を生成
        self.df.loc[:, '住所文字列'] = ''
        self.df.loc[self.df.事業所フラグ == 0, '住所文字列'] = self.df['都道府県'] + \
            self.df['市区町村'] + self.df['町域'] + self.df['字丁目']
        self.df.loc[self.df.事業所フラグ == 1, '住所文字列'] = self.df['都道府県'] + \
            self.df['市区町村'] + self.df['事業所住所']

        # # すべての住所文字列ができたか確認
        print(self.df.loc[self.df.住所文字列 == ''])

        # 転置インデックスを作成
        self.inversed_index = self.make_index(self.df)

    @staticmethod
    def bigram(sentence):
        """一文のbigramと出現場所を返す

        :param sentence:
        :return:
        """
        term_list = []
        location_list = []
        for i in range(len(sentence)):
            term = sentence[i:i + 2].strip()
            if len(term) == 2:
                term_list.append(term)
                location_list.append(i)

        return term_list, location_list

    def make_index(self, df):
        """検索用のメインの辞書を作成する

        :param df:
        :return:
        """
        inversed_index = defaultdict(list)
        for index, sentence in df.住所文字列.items():
            term_list, location_list = self.bigram(sentence)
            for term, loc in zip(term_list, location_list):
                inversed_index[term].append((index, loc))
        return inversed_index

    def address_search(self, word):
        # 検索処理
        hit_list = []
        # 1文字の場合
        if len(word) == 1:
            for i in self.inversed_index.keys():
                if re.search('.*' + word + '.*', i):
                    hit_list.append(self.inversed_index[i])
        # 2文字以上の場合
        else:
            target, _ = self.bigram(word)
            for i in target:
                if i in self.inversed_index.keys():
                    hit_list.append(self.inversed_index[i])

        print(hit_list)

        # インデックス値のみ抽出
        result = []
        for i in hit_list:
            for j in i:
                result.append(j[0])

        print(result)

        # 最頻値の集計
        cnt = Counter(result)
        N = 10
        top_n = cnt.most_common(50)
        if len(cnt) > N:
            print('検索結果が' + str(N) + '件以上あります')

        print(top_n)

        # 結果出力
        rslt = []
        for index, _ in top_n:
            # print(self.df.at[index, '住所文字列'])
            if self.df.loc[index, '事業所フラグ'] == 1:
                continue
            rslt.append(self.df.loc[index, '住所文字列'])
            if len(rslt) >= 40:
                break
        return rslt

    def random_sampling(self, num):
        """ランダムに住所文字列を返す

        :param num: 抽出する数
        :return: ランダムに抽出した住所のリスト
        """
        return self.df.sample(num)['住所文字列'].values

    def office_search(self, word):
        """事業所を検索

        :param word: 入力文字列
        :type word: str
        """
        # 入力なし処理
        if word is '':
            return []

        # 検索処理
        # インデックスを抽出
        hit_list = self.df[self.df.事業所名.str.contains(word) == True]
        print(hit_list)
        N = 10
        if len(hit_list) > N:
            print('検索結果が' + str(N) + '件以上あります')

        # 結果出力
        rslt = []
        for index in hit_list.index.values:
            print(self.df.at[index, '住所文字列'])
            rslt.append(self.df.at[index, '事業所名'])
            if len(rslt) >= 40:
                break

        rslt = list(set(rslt))

        return rslt
