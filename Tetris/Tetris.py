from tkinter import *
from random import randint as rnd
import tkinter.messagebox as msgbox

data = {
    'vertical': 20,  # 縦マスの数 v
    'side': 10,  # 横マスの数 s
    'cell_size': 30,  # マスの大きさ size
    'tet_form': 0,  # ブロックの向き form
    'tet_size': 4,  # tet(ブロックの)のマス数・大きさ b_size
    'x': 4,  # ブロックのｘ軸
    'y': 0,  # ブロックのｙ軸
    'speed': 500,
    'n_tet_shape': None,  # ブロックの形 動画内n
    'tet_color': None,  # ブロックの色 color
    'win': None,  # ウィンドウ
    'cv': None,  # キャンパス
    'field': 0,  # ゲームフィールド f
}
colors = [
    '#00ffff',  # I:O
    '#0000ff',  # J:1
    '#ffa500',  # F 2
    '#ffff00',  # O 3
    '#008000',  # S 4
    '#800080',  # T 5
    '#ff0000',  # Z 6
    '#404040',  # 基盤:7
]



# ブロックの空数値データを2次元のリストで作成 4*4
data['block'] = [[7 for i in range(data['tet_size'])] for j in range(data['tet_size'])]

# ブロックのデータを4次元で作成
block_data = [[[[1,0],[1,1],[1,2],[1,3]],  # I
           [[0,2],[1,2],[2,2],[3,2]],
           [[2,0],[2,1],[2,2],[2,3]],
           [[0,1],[1,1],[2,1],[3,1]]],
          [[[0,0],[1,0],[1,1],[1,2]],  # J
           [[0,1],[0,2],[1,1],[2,1]],
           [[1,0],[1,1],[1,2],[2,2]],
           [[0,1],[1,1],[2,0],[2,1]]],
          [[[0,2],[1,0],[1,1],[1,2]],  # L
           [[0,1],[1,1],[2,1],[2,2]],
           [[1,0],[1,1],[1,2],[2,0]],
           [[0,0],[0,1],[1,1],[2,1]]],
          [[[0,0],[0,1],[1,0],[1,1]],  # O
           [[0,0],[0,1],[1,0],[1,1]],
           [[0,0],[0,1],[1,0],[1,1]],
           [[0,0],[0,1],[1,0],[1,1]]],
          [[[0,1],[0,2],[1,0],[1,1]],  # S
           [[0,1],[1,1],[1,2],[2,2]],
           [[1,1],[1,2],[2,0],[2,1]],
           [[0,0],[1,0],[1,1],[2,1]]],
          [[[0,1],[1,0],[1,1],[1,2]],  # T
           [[0,1],[1,1],[1,2],[2,1]],
           [[1,0],[1,1],[1,2],[2,1]],
           [[0,1],[1,0],[1,1],[2,1]]],
          [[[0,0],[0,1],[1,1],[1,2]],  # Z
           [[0,2],[1,1],[1,2],[2,1]],
           [[1,0],[1,1],[2,1],[2,2]],
           [[0,1],[1,0],[1,1],[2,0]]]]

# 2次元軸でリストを作る
data['field'] = [[7 for i in range(data['side'] + 2)] for j in range(data['vertical'] + 2)]
for i in range(data['vertical'] + 1):
    data['field'][i][0] = 9
    data['field'][i][data['side'] + 1] = 9
data['field'][data['vertical'] + 1] = [9 for i in range(data['side'] + 2)]



# ウィンドウキャンパスの作成
def create_window():
    win = Tk()
    w = data['side'] * data['cell_size']
    h = data['vertical'] * data['cell_size']
    data['cv'] = Canvas(win, width=w, height=h)
    data['cv'].pack()
    return win

# 基盤を描画
def draw_field():
    for y in range(data['vertical']):
        y1 = y * data['cell_size']
        y2 = y1 + data['cell_size']
        for x in range(data['side']):
            x1 = x * data['cell_size']
            x2 = x1 + data['cell_size']
            for i in range(len(image)):
                if data['field'][y + 1][x + 1] == 7:
                    color = colors[7]
                    data['cv'].create_rectangle(x1, y1, x2, y2, fill=color)
                elif data['field'][y + 1][x + 1] == i:
                    data['cv'].create_image(x1, y1, image=image[i], anchor=NW)

# ランダムでブロックを作成

def create_block():
    data['n_tet_shape'] = rnd(0, 6)  # 0~6までの数字を自動生成
    data['tet_color'] = image[data['n_tet_shape']]
    for i in range(len(block_data[data['n_tet_shape']][data['tet_form']])):
        y = block_data[data['n_tet_shape']][data['tet_form']][i][0]
        x = block_data[data['n_tet_shape']][data['tet_form']][i][1]
        data['block'][y][x] = data['n_tet_shape']

# ブロックを描画
def draw_block():
    for y in range(data['tet_size']):
        y1 = (y + data['y'] - 1) * data['cell_size']
        # y2 = y1 + data['cell_size']
        for x in range(data['tet_size']):
            x1 = (x + data['x'] - 1) * data['cell_size']
            # x2 = x1 + data['cell_size']
            if data['block'][y][x] == data['n_tet_shape']:
                data['cv'].create_image(x1, y1, image=image[data["n_tet_shape"]], anchor=NW)

# ブロックの稼働領域を設定
data["x_data"] = [0, 0, 0, 0]  # ブロック一片の現在座標x
data['y_data'] = [0, 0, 0, 0]  # ブロック一片の現在座標y
def area():
    data['f_data_up'] = [0, 0, 0, 0]
    data['f_data_left'] = [0, 0, 0, 0]
    data['f_data_right'] = [0, 0, 0, 0]
    for i in range(len(block_data[data['n_tet_shape']][data['tet_form']])):
        data['y_data'][i] = block_data[data['n_tet_shape']][data['tet_form']][i][0] + data['y']
        data['x_data'][i] = block_data[data['n_tet_shape']][data['tet_form']][i][1] + data['x']
        data['f_data_up'][i] = data['field'][data['y_data'][i] + 1][data['x_data'][i]]
        data['f_data_left'][i] = data['field'][data['y_data'][i]][data['x_data'][i] - 1]
        data['f_data_right'][i] = data['field'][data['y_data'][i]][data['x_data'][i] + 1]

# ブロックの左回転可能領域を設定
def left_turn():
    data['y_data_left_turn'] = [0, 0, 0, 0]
    data['x_data_left_turn'] = [0, 0, 0, 0]
    data['field_data_left_turn'] = [0, 0, 0, 0]
    if data['tet_form'] > 0:
        for i in range(len(block_data[data['n_tet_shape']][data['tet_form']])):
            data['y_data_left_turn'][i] = block_data[data['n_tet_shape']][data['tet_form'] - 1][i][0] + data['y']
            data['x_data_left_turn'][i] = block_data[data['n_tet_shape']][data['tet_form'] - 1][i][1] + data['x']
            data['field_data_left_turn'][i] = data['field'][data['y_data_left_turn'][i]][data['x_data_left_turn'][i]]
    else:
        for i in range(len(block_data[data['n_tet_shape']][data['tet_form']])):
            data['y_data_left_turn'][i] = block_data[data['n_tet_shape']][data['tet_form'] + 3][i][0] + data['y']
            data['x_data_left_turn'][i] = block_data[data['n_tet_shape']][data['tet_form'] + 3][i][1] + data['x']
            data['field_data_left_turn'][i] = data['field'][data['y_data_left_turn'][i]][data['x_data_left_turn'][i]]

# ブロックの右回転可能領域を設定
def right_turn():
    data['y_data_right_turn'] = [0, 0, 0, 0]
    data['x_data_right_turn'] = [0, 0, 0, 0]
    data['field_data_right_turn'] = [0, 0, 0, 0]
    if data['tet_form'] > 0:
        for i in range(len(block_data[data['n_tet_shape']][data['tet_form']])):
            data['y_data_right_turn'][i] = block_data[data['n_tet_shape']][data['tet_form'] - 1][i][1] + data['y']
            data['x_data_right_turn'][i] = block_data[data['n_tet_shape']][data['tet_form'] - 1][i][0] + data['x']
            data['field_data_right_turn'][i] = data['field'][data['y_data_right_turn'][i]][data['x_data_right_turn'][i]]
    else:
        for i in range(len(block_data[data['n_tet_shape']][data['tet_form']])):
            data['y_data_right_turn'][i] = block_data[data['n_tet_shape']][data['tet_form'] + 3][i][0] + data['y']
            data['x_data_right_turn'][i] = block_data[data['n_tet_shape']][data['tet_form'] + 3][i][1] + data['x']
            data['field_data_right_turn'][i] = data['field'][data['y_data_right_turn'][i]][data['x_data_right_turn'][i]]

# ゲームオーバー判定
def gudgment_game():
    top_field = [7 for i in range(data['side'] + 2)]
    top_field[0], top_field[data['side'] + 1] = 9, 9
    if data['field'][1] != top_field:
        msgbox.showinfo(message='GAME OVER')
        quit()

# ブロックが一列揃ったら消す
def delete_block():
    for y in range(20):
        # print(data['y'])
        # for i in range(data['vertical'] + 2):
        #     print(data['field'][i])
        # print('\n')
        if (7 in data['field'][y + 1]) == False:  # +1なのはdata[y]座標が1からだから？
            del data['field'][y + 1]
            add_field = [7 for i in range(data['side'] + 2)]
            add_field[0], add_field[data['side'] + 1] = 9, 9
            data['field'].insert(0, add_field)

            # for i in range(data['y']):
            #     print(data['field'][i])
            # print('\n')
            #

# ブロックを落とす
def drop_block():
    area()
    if data['f_data_up'] == [7, 7, 7, 7]:
        data['cv'].delete('all')
        data['y'] += 1
        draw_field()
        draw_block()
        if data['speed'] >= 201:
            data['speed'] -= 1
        # 空空間でなかったら、fieldにミノデータ上書きして、画面上で留める
    else:
        for i in range(len(data['y_data'])):
            data['field'][data['y_data'][i]][data['x_data'][i]] = data['n_tet_shape']
        gudgment_game()
        delete_block()

        data['block'] = [[7 for i in range(data['tet_size'])] for j in range(data['tet_size'])]
        data['x'] = 4
        data['y'] = 0
        data['tet_form'] = 0
        create_block()
        draw_field()
        draw_block()

    data['win'].after(data['speed'], drop_block)

# Enterキー押された時の処理
def return_key(e):
    area()
    if data['f_data_up'] == [7, 7, 7, 7]:
        data['cv'].delete('all')
        data['y'] += 1
        draw_field()
        draw_block()

# LEFTキーが押された時の処理
def left_key(e):
    area()
    if data['f_data_left'] == [7, 7, 7, 7]:
        data['x'] -= 1
        data['cv'].delete('all')
        draw_field()
        draw_block()

# RIGHTキーら押された時の処理
def right_key(e):
    area()
    if data['f_data_right'] == [7, 7, 7, 7]:
        data['x'] += 1
        data['cv'].delete('all')
        draw_field()
        draw_block()

# UPキーが押され他時の処理
def up_key(e):
    left_turn()
    if data['field_data_left_turn'] == [7, 7, 7, 7]:
        data['block'] = [[7 for i in range(data['tet_size'])] for j in range(data['tet_size'])]
        if data['tet_form'] > 0:
            data['tet_form'] -= 1
            for i in range(len(block_data[data['n_tet_shape']][data['tet_form']])):
                y = block_data[data['n_tet_shape']][data['tet_form']][i][0]
                x = block_data[data['n_tet_shape']][data['tet_form']][i][1]
                data['block'][y][x] = data['n_tet_shape']
        else:
            data['tet_form'] += 3
            for i in range(len(block_data[data['n_tet_shape']][data['tet_form']])):
                y = block_data[data['n_tet_shape']][data['tet_form']][i][0]
                x = block_data[data['n_tet_shape']][data['tet_form']][i][1]
                data['block'][y][x] = data['n_tet_shape']
        data['cv'].delete('all')
        draw_field()
        draw_block()

# DOWNキーが押され他時の処理
def down_key(e):
    right_turn()
    if data['field_data_right_turn'] == [7, 7, 7, 7]:
        data['block'] = [[7 for i in range(data['tet_size'])] for j in range(data['tet_size'])]
        if data['tet_form'] < 3:
            data['tet_form'] += 1
            for i in range(len(block_data[data['n_tet_shape']][data['tet_form']])):
                y = block_data[data['n_tet_shape']][data['tet_form']][i][0]
                x = block_data[data['n_tet_shape']][data['tet_form']][i][1]
                data['block'][y][x] = data['n_tet_shape']
        else:
            data['tet_form'] -= 3
            for i in range(len(block_data[data['n_tet_shape']][data['tet_form']])):
                y = block_data[data['n_tet_shape']][data['tet_form']][i][0]
                x = block_data[data['n_tet_shape']][data['tet_form']][i][1]
                data['block'][y][x] = data['n_tet_shape']
        data['cv'].delete('all')
        draw_field()
        draw_block()

data['win'] = create_window()

image = [
    PhotoImage(file='asset/dedetile1.png'),
    PhotoImage(file='asset/dedetile2.png'),
    PhotoImage(file='asset/dedetile3.png'),
    PhotoImage(file='asset/dedetile4.png'),
    PhotoImage(file='asset/dedetile5.png'),
    PhotoImage(file='asset/dedetile6.png'),
    PhotoImage(file='asset/dedetile7.png'),
    '#404040',  # 基盤:7
    ]

draw_field()
create_block()
draw_block()

data['win'].after(data['speed'], drop_block)
data['win'].bind('<Left>', left_key)
data['win'].bind('<Right>', right_key)
data['win'].bind('<Up>', up_key)
data['win'].bind('<Down>', down_key)
data['win'].bind('<Return>', return_key)

data['win'].mainloop()