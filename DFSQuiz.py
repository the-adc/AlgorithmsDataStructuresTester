import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import string

NUM_NODES = 8
NUM_EDGES = 12

class DFSQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random DFS Quiz Game")
        self.score = 0
        self.round = 0

        self.instruction_label = tk.Label(root, text="🧠 DFS Quiz:\nClick the nodes in the order you think a DFS traversal would visit them, starting from the alphabetically first node.", font=("Arial", 12), justify="center", wraplength=400)
        self.instruction_label.pack(pady=10)

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack()

        self.graph_canvas = None
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=10)

        # Labels
        self.order_label = tk.Label(self.control_frame, text="Selected Order: []", font=("Arial", 12))
        self.order_label.grid(row=0, column=0, columnspan=3)
        self.score_label = tk.Label(self.control_frame, text="Score: 0", font=("Arial", 12, 'bold'))
        self.score_label.grid(row=1, column=0, columnspan=3)

        # Buttons
        self.submit_btn = tk.Button(self.control_frame, text="Submit", bg="lightgreen", font=("Arial", 12), command=self.submit)
        self.submit_btn.grid(row=2, column=0, padx=10)

        self.reset_btn = tk.Button(self.control_frame, text="Next Round", bg="lightblue", font=("Arial", 12), command=self.new_round)
        self.reset_btn.grid(row=2, column=1, padx=10)

        self.solution_btn = tk.Button(self.control_frame, text="Show Solution", bg="lightyellow", font=("Arial", 12), command=self.show_solution)
        self.solution_btn.grid(row=2, column=2, padx=10)

        self.selected_order = []
        self.buttons = {}

        self.new_round()

    def new_round(self):
        self.round += 1
        self.selected_order = []
        self.G = self.generate_random_graph()
        self.start_node = sorted(self.G.nodes())[0]
        self.correct_order = self.dfs(self.G, self.start_node)
        self.pos = nx.spring_layout(self.G, seed=42)
        self.draw_graph()

        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        self.buttons = {}
        for i, node in enumerate(sorted(self.G.nodes())):
            btn = tk.Button(self.buttons_frame, text=node, width=4, height=2, font=('Arial', 12),
                            command=lambda n=node: self.select_node(n))
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            self.buttons[node] = btn

        self.order_label.config(text="Selected Order: []")

    def generate_random_graph(self):
        nodes = list(string.ascii_uppercase[:NUM_NODES])
        G = nx.Graph()
        G.add_nodes_from(nodes)

        # Ensure connectivity
        connected = set()
        available = set(nodes)
        current = random.choice(nodes)
        connected.add(current)
        available.remove(current)

        while available:
            next_node = random.choice(list(available))
            connect_to = random.choice(list(connected))
            G.add_edge(current, next_node)
            connected.add(next_node)
            available.remove(next_node)

        # Add extra random edges
        while G.number_of_edges() < NUM_EDGES:
            u, v = random.sample(nodes, 2)
            if not G.has_edge(u, v):
                G.add_edge(u, v)

        return G

    def draw_graph(self, highlight_nodes=None):
        if self.graph_canvas:
            self.graph_canvas.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(5, 4))
        node_colors = ['lightgreen' if highlight_nodes and node in highlight_nodes else 'skyblue' for node in self.G.nodes()]
        nx.draw(self.G, pos=self.pos, with_labels=True, node_color=node_colors, edge_color='gray',
                node_size=1000, font_size=12, ax=ax)
        self.graph_canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack()

    def dfs(self, graph, start):
        visited = []
        stack = [start]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.append(node)
                neighbors = sorted([n for n in graph.neighbors(node) if n not in visited], reverse=True)
                stack.extend(neighbors)
        return visited

    def select_node(self, node):
        if node in self.selected_order:
            self.selected_order.remove(node)
            self.order_label.config(text=f"Selected Order: {self.selected_order}")
            self.buttons[node].config(state="normal")
        else:
            self.selected_order.append(node)
            self.order_label.config(text=f"Selected Order: {self.selected_order}")
            #self.buttons[node].config(state="disabled")

    def submit(self):
        if self.selected_order == self.correct_order:
            self.score += 1
            messagebox.showinfo("Correct!", "Great job! You found the correct DFS order.")
        else:
            messagebox.showerror("Incorrect", f"Wrong order!\nCorrect: {self.correct_order}")
        self.score_label.config(text=f"Score: {self.score}")

    def show_solution(self):
        self.animate_solution(self.correct_order)

    def animate_solution(self, order):
        for i in range(len(order) + 1):
            self.root.after(500 * i, lambda i=i: self.draw_graph(highlight_nodes=order[:i]))

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = DFSQuizApp(root)
    root.mainloop()
