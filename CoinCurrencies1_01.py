"""Программа 'Крипта курс' получает текущие курсы популярных криптовалют
 к доллару США из открытого API агрегатора данных о криптовалютах CoinGecko
 и выводит их в удобную таблицу c возможностью посмотреть расширенную
 информацию о текущих показателях интересующей криптовалюты"""
import requests
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from PIL import Image, ImageTk
from io import BytesIO
from time import strftime, localtime


class MyToplevel(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        # код настройки окна

def clear_tree():
    """Процедура очистки таблицы курсов"""
    # Получаем все ID элементов и удаляем их
    items = rate_view.get_children()
    if items:  # Проверяем, есть ли элементы, чтобы не идти по пустому списку
        rate_view.delete(*items)

def show_coin_info(event):
    """Процедура вывода дополнительной информации по криптовалюте"""
    item_id = event.widget.focus()  # Или tree.selection()
    # Получаем идентификатор элемента, на который кликнули
    item_values = event.widget.item(item_id, 'values')
    if item_id:  # если что то выбрали
        top_card = MyToplevel(win)
        # top_card.geometry('300x200')
        top_card.title(f'Информация о {item_values[1].strip()}')

        frm_left = Frame(top_card, width=22)
        frm_left.pack(side=LEFT, padx=(10,0), fill=Y)

        l_img = Label(frm_left)
        l_img.pack(padx=10, pady=10)

        response = requests.get(item_values[9].strip(), stream=True)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content))
        img.thumbnail((50, 50))

        imgtk = ImageTk.PhotoImage(img)
        l_img.config(image=imgtk)
        l_img.image = imgtk

        frm_info = Frame(top_card)
        frm_info.pack(side=LEFT, padx=20, pady=10)

        label = ttk.Label(frm_info, text='Рейтинг капитализации:', anchor='w',
                          justify=LEFT, width=22)
        label.grid(row=0, column=0, pady=2)
        entry_n = ttk.Entry(frm_info, width=35, font="Arial 10 bold")
        entry_n.grid(row=0, column=1)
        entry_n.insert(0, item_values[0].strip())
        entry_n.config(state='readonly')

        label = ttk.Label(frm_info, text='Наименование:', anchor='w',
                          justify=LEFT, width=22)
        label.grid(row=1, column=0, pady=2)
        entry_n = ttk.Entry(frm_info, width=35, font="Arial 10 bold")
        entry_n.grid(row=1, column=1)
        entry_n.insert(0, item_values[1].strip())
        entry_n.config(state='readonly')

        label = ttk.Label(frm_info, text='Символьный код:', anchor='w',
                          justify=LEFT, width=22)
        label.grid(row=2, column=0, pady=2)
        entry_n = ttk.Entry(frm_info, width=35, font="Arial 10 bold")
        entry_n.grid(row=2, column=1)
        entry_n.insert(0, item_values[2].strip())
        entry_n.config(state='readonly')

        label = ttk.Label(frm_info, text='Текущая цена:', anchor='w',
                          justify=LEFT, width=22)
        label.grid(row=3, column=0, pady=2)
        entry_n = ttk.Entry(frm_info, width=35, font="Arial 10 bold")
        entry_n.grid(row=3, column=1)
        entry_n.insert(0, f'$ {item_values[3].strip()}')
        entry_n.config(state='readonly')

        label = ttk.Label(frm_info, text='Исторический максимум:', anchor='w',
                          justify=LEFT)
        label.grid(row=4, column=0, pady=2)
        entry_n = ttk.Entry(frm_info, width=35)
        entry_n.grid(row=4, column=1)
        entry_n.insert(0, f'$ {item_values[4].strip()}')
        entry_n.config(state='readonly')

        label = ttk.Label(frm_info, text='Исторический минимум:', anchor='w',
                          justify=LEFT, width=22)
        label.grid(row=5, column=0, pady=2)
        entry_n = ttk.Entry(frm_info, width=35)
        entry_n.grid(row=5, column=1)
        entry_n.insert(0, f'$ {item_values[5].strip()}')
        entry_n.config(state='readonly')

        label = ttk.Label(frm_info, text='Макс.цена за посл.24ч:', anchor=W,
                          justify=LEFT, width=22)
        label.grid(row=6, column=0, pady=2)
        entry_n = ttk.Entry(frm_info, width=35)
        entry_n.grid(row=6, column=1)
        entry_n.insert(0, f'$ {item_values[6].strip()}')
        entry_n.config(state='readonly')


        label = ttk.Label(frm_info, text='Мин.цена за посл. 24ч:', anchor=W,
                          justify=LEFT, width=22)
        label.grid(row=7, column=0, pady=2)
        entry_n = ttk.Entry(frm_info, width=35)
        entry_n.grid(row=7, column=1)
        entry_n.insert(0, f'$ {item_values[7].strip()}')
        entry_n.config(state='readonly')

        label = ttk.Label(frm_info, text='Общее кол. монет в обороте:', anchor=W,
                          justify=LEFT, width=22)
        label.grid(row=8, column=0, pady=2)
        entry_n = ttk.Entry(frm_info, width=35)
        entry_n.grid(row=8, column=1)
        entry_n.insert(0, item_values[8].strip())
        entry_n.config(state='readonly')


def fill_treeview(data):
    """Процедура заполнения таблицы курсов данными из json"""
    if not data:
        return
    # Очищаем таблицу для нового заполнения
    clear_tree()

    for coin in data:
        name = (f"{coin['name'].strip()} ({coin['id'].strip().title()})"
                if (coin['id'].strip() not in
                    coin['name'].strip().lower().replace(" ", "-")
                    and len(coin['id'].strip()) < 26
                    and coin['id'] != coin['symbol'])
                else coin['name'].strip()
                )

        # print(f"{coin['market_cap_rank'] if coin['market_cap_rank'] else '':<16}"
        #       f" : {coin['id'][:30].strip():<30} : {name[:62]:<62} : {coin['symbol'].upper():<13}"
        #       f" : {coin['current_price']:10,.2f}")
        rate_view.insert('', END,
                         values=(f'{coin['market_cap_rank'] 
                                    if coin['market_cap_rank'] else '':>3}',
                                 f'  {name}',
                                 f'{coin['symbol'].strip().upper():<10}',
                                 f'{coin['current_price']:12,.2f}',
                                 coin['ath'], coin['atl'],
                                 coin['high_24h'], coin['low_24h'],
                                 coin['circulating_supply'], coin['image']))
        rate_view.bind('<Double-Button-1>', show_coin_info)
        rate_view.bind('<Return>', show_coin_info)


def get_coin_rate():
    """Процедура подключения к агрегатору CoinGecko и получения данных топ-100
     по криптовалюте"""
    # url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&&per_page=250&page=1"
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc"
    try:
        response = requests.get(url, stream=True, timeout=1000)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            title_frame['text'] = (f'Курсы популярных криптовалют к $ доллару '
                               f'США на {strftime("%d.%m.%Y %H:%M", localtime())}')
            fill_treeview(data)
        else:
            mb.showwarning("Внимание",f"Ошибка API: код {response.status_code}")
    except requests.exceptions.RequestException as e:
        mb.showerror("Ошибка сети", f"Ошибка сети: {str(e)}")


win = Tk()
win.title('Крипта курс')
win.geometry('1024x750+10-50')

title_frame = LabelFrame(text=f'Курсы популярных криптовалют к $ доллару США ',
                         font="bold", fg='DarkRed')
title_frame.pack(padx=5, pady=5, fill=BOTH, expand=True)

style = ttk.Style()
# Cтиль для заголовков
style.configure("Treeview.Heading", font=('Calibri', 18, 'bold'),
                foreground="SeaGreen", rowheight=80)
# Общий стиль
style.configure("Treeview", font=('Courier new', 14, 'bold'), foreground="navy",
                rowheight=30)

rate_view = ttk.Treeview(title_frame, columns=('rank', 'name', 'symbol', 'price',
                            'ath', 'atl', 'high_24h', 'low_24h',
                            'circulating_supply', 'image'), show='headings',
                             style="mystyle.Treeview")

rate_view.column('rank', anchor=CENTER, width=10)  # Центрируем текст в ячейках колонки
rate_view.column('name', width=300)
rate_view.column('symbol', anchor=CENTER, width=40)
rate_view.column('price', anchor=CENTER, width=40)
rate_view.column('ath', width = 0, stretch = "no", anchor = "c")
rate_view.column('atl', width = 0, stretch = "no", anchor = "c")
rate_view.column('high_24h', width = 0, stretch = "no", anchor = "c")
rate_view.column('low_24h', width = 0, stretch = "no", anchor = "c")
rate_view.column('circulating_supply', width = 0, stretch = "no", anchor = "c")
rate_view.column('image', width = 0, stretch = "no", anchor = "c")
rate_view.heading(column='rank', text=f'№ в рейтинге')
rate_view.heading(column='name', text='Наименование')
rate_view.heading(column='symbol', text='Тикер')
rate_view.heading(column='price', text='Цена')


# # Заполняем Treeview
# # poke_ref = sorted(poke_names.items())
# for npp, (title, cat, rat, stock, price, img) in enumerate(prod_list, start=1):
#     rate_view.insert('', END, values=(f'{npp:>4}.',f'{title}', f'{cat}', f'{rat}',
#                                      f'{stock}',f'{price:>9}', img))
#     rate_view.bind('<Double-Button-1>', show_prod_card)
#     # Кортеж в values обязателен (val,)



scrollbar = ttk.Scrollbar(title_frame, orient="vertical",
                          command=rate_view.yview)
rate_view.configure(yscrollcommand=scrollbar.set)

rate_view.pack(side="left", expand=True, fill="both", padx=(10,0), pady=8)
scrollbar.pack(side="right", fill="y")

menu_bar = Menu(win)
win.config(menu=menu_bar)
# Создание подменю "Файл"
file_menu = Menu(menu_bar, tearoff=0, font='Verdana 10')
menu_bar.add_cascade(label="Файл", menu=file_menu)
# file_menu.add_separator()
file_menu.add_command(label="Выход", command=quit)
menu_bar.add_command(label="Актуализировать", command=get_coin_rate)
menu_bar.add_command(label="Справка", command=lambda :
                     mb.showinfo('Справка',
                                 'Программа "Крипта курс" показывает курсы по\n'
                                 'топ-100 рейтинга рыночной капитализации криптовалют.\n'
                                 'Программа не обновляет курсы автоматически.\n'
                                 'Чтобы получить курсы на текущий момент нажмите\n'
                                 'кнопку меню "Актуализировать".'
                                 'Для просмотра расширенной информации кликните \n'
                                 'мышкой по интересующей вас криптовалюте.'))

get_coin_rate()

win.mainloop()