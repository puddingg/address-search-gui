from A_dict import Address_Dict
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        # 画面表示用変数
        self.echo = tk.StringVar()

        tk.Frame.__init__(self, master)
        master.title('住所検索')
        master.geometry('400x800')
        self.pack()
        self.createWidgets()

        # create base database
        self.iMac_Pro = Address_Dict()

    def createWidgets(self):
        # generate input box
        self.input = tk.Entry()
        self.input.bind('<Return>', self.address_search)
        self.input.pack()

        # generate buttons
        self.button = tk.Button(text='検索')
        self.button.bind('<Button-1>', self.address_search)
        self.button.pack()

        self.button_random = tk.Button(text='ランダム抽出')
        self.button_random.bind('<Button-1>', self.random_address)
        self.button_random.pack()

        self.button_random = tk.Button(text='オフィス検索')
        self.button_random.bind('<Button-1>', self.office_search)
        self.button_random.pack()

        # generate label
        self.lbl = tk.Label(textvariable=self.echo)
        self.lbl.pack()

    def address_search(self, event):
        word = self.input.get()
        lst = self.iMac_Pro.address_search(word)
        title = '検索文字列：' + word + '\n' * 2
        rlt = title + '\n'.join(lst)
        self.echo.set(rlt)

    def office_search(self, event):
        word = self.input.get()
        lst = self.iMac_Pro.office_search(word)
        title = '検索文字列：' + word + '\n' * 2
        rlt = title + '\n'.join(lst)
        self.echo.set(rlt)

    def random_address(self, event):
        temp = self.iMac_Pro.random_sampling(40)
        self.echo.set('\n'.join(temp))


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
