import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import END

from Search import execute_search, SearchObject


input_background_color = '#B5AE96'
input_font = 'Verdana 8 bold'
search_button_color = '#718E67'
search_font = 'Verdana 18 bold'
response_background_color = '#212128'


class StandardInput:
    def __init__(self, master, label_text):
        self.frame = tk.Frame(
            master=master,
            background=input_background_color
        )
        self.frame.grid(column=0, padx=4, pady=2)
        self.label = tk.Label(master=self.frame, text=label_text, background=input_background_color,
                              foreground=response_background_color, font=input_font)
        self.label.grid(sticky='w')
        self.entry = tk.Entry(master=self.frame)
        self.entry.grid()


class MinMaxInput:
    def __init__(self, master, label_text, row):
        self.min_frame = tk.Frame(
            master=master,
            background=input_background_color
        )
        self.min_frame.grid(row=row, column=0, padx=4, pady=2)
        self.min_label = tk.Label(master=self.min_frame, text=f'{label_text} Min', background=input_background_color,
                                  foreground=response_background_color, font=input_font)
        self.min_label.grid(sticky='w')
        self.min_entry = tk.Entry(master=self.min_frame)
        self.min_entry.grid()
        self.max_frame = tk.Frame(
            master=master,
            background=input_background_color
        )
        self.max_frame.grid(row=row, column=1, padx=4, pady=2)
        self.max_label = tk.Label(master=self.max_frame, text=f'{label_text} Max', background=input_background_color,
                                  foreground=response_background_color, font=input_font)
        self.max_label.grid(sticky='w')
        self.max_entry = tk.Entry(master=self.max_frame)
        self.max_entry.grid()


class SearchInput:
    def __init__(self, input_frame_left, input_frame_right):
        self.hp = MinMaxInput(input_frame_left, 'HP', 0)
        self.attack = MinMaxInput(input_frame_left, 'Atk', 1)
        self.defense = MinMaxInput(input_frame_left, 'Def', 2)
        self.special_attack = MinMaxInput(input_frame_left, 'SpA', 3)
        self.special_defense = MinMaxInput(input_frame_left, 'SpD', 4)
        self.speed = MinMaxInput(input_frame_left, 'Spe', 5)
        self.bst = MinMaxInput(input_frame_left, 'BST', 6)
        self.point_value = MinMaxInput(input_frame_left, 'Pts', 7)
        self.type_1 = StandardInput(input_frame_right, 'Type 1')
        self.type_2 = StandardInput(input_frame_right, 'Type 2')
        self.ability = StandardInput(input_frame_right, 'Ability')
        self.move = StandardInput(input_frame_right, 'Move')
        self.special_move_category = StandardInput(input_frame_right, 'Move Category')
        self.type_effective_resist_1 = StandardInput(input_frame_right, 'Resist 1')
        self.type_effective_resist_2 = StandardInput(input_frame_right, 'Resist 2')
        self.type_effective_immune = StandardInput(input_frame_right, 'Immunity')


def search(search_input: SearchInput):
    search_object = SearchObject()
    search_object.hp.maximum = search_input.hp.max_entry.get() or 999
    search_object.hp.minimum = search_input.hp.min_entry.get() or 0
    search_object.attack.maximum = search_input.attack.max_entry.get() or 999
    search_object.attack.minimum = search_input.attack.min_entry.get() or 0
    search_object.defense.maximum = search_input.defense.max_entry.get() or 999
    search_object.defense.minimum = search_input.defense.min_entry.get() or 0
    search_object.special_attack.maximum = search_input.special_attack.max_entry.get() or 999
    search_object.special_attack.minimum = search_input.special_attack.min_entry.get() or 0
    search_object.special_defense.maximum = search_input.special_defense.max_entry.get() or 999
    search_object.special_defense.minimum = search_input.special_defense.min_entry.get() or 0
    search_object.speed.maximum = search_input.speed.max_entry.get() or 999
    search_object.speed.minimum = search_input.speed.min_entry.get() or 0
    search_object.bst.maximum = search_input.bst.max_entry.get() or 999
    search_object.bst.minimum = search_input.bst.min_entry.get() or 0
    search_object.point_value.maximum = search_input.point_value.max_entry.get() or 20
    search_object.point_value.minimum = search_input.point_value.min_entry.get() or 0
    search_object.type_1 = search_input.type_1.entry.get() or None
    search_object.type_2 = search_input.type_2.entry.get() or None
    search_object.ability = search_input.ability.entry.get() or None
    search_object.move = search_input.move.entry.get() or None
    search_object.special_move_category = search_input.special_move_category.entry.get() or None
    search_object.type_effective_resist_1 = search_input.type_effective_resist_1.entry.get() or None
    search_object.type_effective_resist_2 = search_input.type_effective_resist_2.entry.get() or None
    search_object.type_effective_immune = search_input.type_effective_immune.entry.get() or None
    pokemon = execute_search(search_object)
    pokemon.sort(key=lambda x: x['point_value'], reverse=True)
    response_text = ''
    if len(pokemon) == 0:
        response_text = 'No results'
    for p in pokemon:
        response_text += f'{p['point_value']} pts: {p['name']} ({p['speed']} Spe)\n'
        response_text += f'        Moves: {p['moves']}\n' if p['moves'] is not None else ''
    text_area.configure(state='normal')
    text_area.delete('1.0', END)
    text_area.insert(tk.INSERT, response_text)
    text_area.configure(state='disabled')


window = tk.Tk()
window.title('Pokemon Search')
window.configure(background=input_background_color)
input_frame_left = tk.Frame(
    master=window,
    background=input_background_color
)
input_frame_left.grid(row=0, column=0, sticky='ns')
input_frame_right = tk.Frame(
    master=window,
    background=input_background_color
)
input_frame_right.grid(row=0, column=1, sticky='ns')
search_input = SearchInput(input_frame_left, input_frame_right)
search_button = tk.Button(
    text='Search',
    background=search_button_color,
    foreground=response_background_color,
    font=search_font,
    command=lambda: search(search_input)
)
search_button.grid(row=1, column=0, columnspan=2, sticky='we', pady=6)
response_frame = tk.Frame(
    master=window,
    relief=tk.SUNKEN,
    borderwidth=3,
    background=response_background_color,
    height=100,
    width=300
)
response_frame.grid(row=2, column=0, columnspan=2, sticky='we')
text_area = st.ScrolledText(master=response_frame, background=response_background_color,
                            foreground=input_background_color, font=input_font, height=10, width=50)
text_area.grid()
text_area.insert(tk.INSERT, 'No results')
text_area.configure(state='disabled')
