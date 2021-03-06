from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from src.algorithm import dpo
from src.parse import parse
from kivy.uix.popup import Popup
from copy import deepcopy

"""
class GraphProd(BoxLayout):
    def __init__(self, prod, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.add_widget(Button(text='Choose', font_size=14,size_hint=(0.4,1)))
        self.add_widget(Label(text="P:", size_hint=(0.1, 1)))
        self.add_widget(Label(text="L:", size_hint=(0.1, 1)))
        self.add_widget(FigureCanvasKivyAgg(prod.left.visualize()))
        self.add_widget(Label(text="K:", size_hint=(0.1, 1)))
        self.add_widget(FigureCanvasKivyAgg(prod.connector.visualize()))
        self.add_widget(Label(text="R:", size_hint=(0.1, 1)))
        self.add_widget(FigureCanvasKivyAgg(prod.right.visualize()))
"""


class Matty(BoxLayout):

    def __init__(self, filename, **kwargs):
        super().__init__(**kwargs)
        with open(filename) as f:
            grammar = parse(f)
            self.main_graph = grammar.input_graph
            self.previous_graph = deepcopy(self.main_graph)
            self.prod_list = grammar.production_list
        lay1 = BoxLayout(orientation='horizontal')
        self.prod_choice = 0  # which production
        self.buttons = []  # button list
        self.add_widget(lay1)
        self.box1 = BoxLayout()
        self.box2 = BoxLayout(orientation='vertical')
        self.prodlabel = Label(text="Production: 1")
        self.indexinput = TextInput(size_hint=(1, 0.3))  # indexes separated with commas 3,4,2,1
        self.submitbuttton = Button(text="Submit", font_size=14)
        self.submitbuttton.bind(on_press=self.submit)
        lay1.add_widget(self.box1)
        lay1.add_widget(self.box2)
        self.previousbutton = Button(text="Previous graph", font_size=14)
        self.previousbutton.bind(on_press=self.previous)
        self.box2.add_widget(self.prodlabel)
        self.box2.add_widget(self.indexinput)
        self.box2.add_widget(self.submitbuttton)
        self.box2.add_widget(self.previousbutton)
        self.graphplot = FigureCanvasKivyAgg(self.main_graph.visualize())
        self.box1.add_widget(self.graphplot)
        self.lay2 = BoxLayout(orientation='vertical')
        self.add_widget(self.lay2)
        self.prodboxes = []
        self.alert = Popup(title='Error',
                           content=Label(text="Could not perform the production."),
                           size_hint=(None, None), size=(400, 400))
        for cnt, prod in enumerate(self.prod_list):
            self.buttons.append(Button(text="Choose " + str(cnt + 1), font_size=14, size_hint=(0.4, 1)))
            self.prodboxes.append(BoxLayout(orientation='horizontal'))
            self.lay2.add_widget(self.prodboxes[-1])
            self.buttons[-1].prod_num = cnt
            self.buttons[-1].bind(on_press=self.press)
            self.prodboxes[-1].add_widget(self.buttons[-1])
            self.prodboxes[-1].add_widget(Label(text="P:", size_hint=(0.1, 1)))
            self.prodboxes[-1].add_widget(Label(text="L:", size_hint=(0.1, 1)))
            self.prodboxes[-1].add_widget(FigureCanvasKivyAgg(prod.left.visualize()))
            self.prodboxes[-1].add_widget(Label(text="K:", size_hint=(0.1, 1)))
            self.prodboxes[-1].add_widget(FigureCanvasKivyAgg(prod.connector.visualize()))
            self.prodboxes[-1].add_widget(Label(text="R:", size_hint=(0.1, 1)))
            self.prodboxes[-1].add_widget(FigureCanvasKivyAgg(prod.right.visualize()))

    def press(self, instance):
        self.prod_choice = instance.prod_num
        self.prodlabel.text = "Production: " + str(instance.prod_num + 1)

    def submit(self, instance):
        try:
            indexes = list(map(int, self.indexinput.text.split(',')))
            temp = deepcopy(self.main_graph)
            dpo(self.main_graph, self.prod_list[self.prod_choice], indexes)
            self.previous_graph = temp
            self.box1.remove_widget(self.graphplot)
            self.graphplot = FigureCanvasKivyAgg(self.main_graph.visualize())
            self.box1.add_widget(self.graphplot)
        except ValueError:
            self.alert.open()
        # updategui()

    def previous(self, instance):
        if self.previous_graph != self.main_graph:
            self.main_graph = self.previous_graph
            self.box1.remove_widget(self.graphplot)
            self.graphplot = FigureCanvasKivyAgg(self.main_graph.visualize())
            self.box1.add_widget(self.graphplot)


class GraphApp(App):
    def __init__(self, filename, **kwargs):
        super().__init__(**kwargs)
        self.filename = filename

    def build(self):
        return Matty(self.filename)


if __name__ == '__main__':
    GraphApp('../ex1.txt').run()
