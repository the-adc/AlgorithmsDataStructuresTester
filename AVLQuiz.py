import tkinter as tk
from tkinter import messagebox
import random
from math import sqrt
from AVLTree import AVLTree

class AVLQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AVL Tree Quiz")
        self.root.geometry("1200x800")
        
        self.avl = AVLTree()
        self.operations = []
        self.generate_question()
        self.setup_ui()
        
    def generate_question(self):
        """Generate a random sequence of insertions and build the AVL tree"""
        self.avl = AVLTree()
        self.operations = []
        num_operations = random.randint(5, 8)
        values = random.sample(range(1, 200), num_operations)
        
        for val in values:
            self.operations.append(f"Insert {val}")
            self.avl.insert(val)
        
    def setup_ui(self):
        self.clear_screen()
        
        # Title and instructions
        title_frame = tk.Frame(self.root)
        title_frame.pack(pady=10)
        
        tk.Label(title_frame, text="AVL Tree Quiz", font=("Arial", 20, "bold")).pack()
        tk.Label(title_frame, 
                text="Perform the following operations on an empty AVL tree:",
                font=("Arial", 12)).pack()
        
        # Display operations
        ops_frame = tk.Frame(self.root)
        ops_frame.pack(pady=10)
        
        for op in self.operations:
            tk.Label(ops_frame, text=op, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        
        # Canvas for tree visualization
        self.canvas = tk.Canvas(self.root, width=1000, height=600, bg="white")
        self.canvas.pack(pady=20)
        
        # Draggable nodes
        self.draggable_nodes = []
        self.node_values = [op.split()[1] for op in self.operations if op.startswith("Insert")]
        self.create_draggable_nodes()
        
        # Draw tree template based on actual AVL structure
        self.draw_tree_template()
        
        # Buttons
        tk.Button(self.root, text="Check Answer", command=self.check_answer, 
                 font=("Arial", 14), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self.root, text="New Question", command=self.new_question,
                 font=("Arial", 12)).pack()
    
    def create_draggable_nodes(self):
        """Create draggable nodes with text that move together"""
        start_x, start_y = 50, 50
        for i, val in enumerate(self.node_values):
            node_id = self.canvas.create_oval(
                start_x + i*70, start_y, 
                start_x + i*70 + 50, start_y + 50,
                fill="#2196F3", outline="black", tags=("draggable", f"node_{val}")
            )
            text_id = self.canvas.create_text(
                start_x + i*70 + 25, start_y + 25,
                text=val, font=("Arial", 12), tags=("draggable", f"text_{val}")
            )
            
            self.draggable_nodes.append({
                "val": val,
                "node": node_id,
                "text": text_id,
                "x": start_x + i*70 + 25,
                "y": start_y + 25
            })
            
            for item in [node_id, text_id]:
                self.canvas.tag_bind(item, "<ButtonPress-1>", lambda e, val=val: self.on_drag_start(e, val))
                self.canvas.tag_bind(item, "<B1-Motion>", lambda e, val=val: self.on_drag_motion(e, val))
    
    def draw_tree_template(self):
        """Dynamically draw tree structure based on actual AVL tree"""
        # Clear any existing template
        self.canvas.delete("template")
        
        # Calculate positions based on tree depth
        self.tree_positions = {}
        if self.avl.root:
            self.calculate_positions(self.avl.root, 500, 50, 150, 1)
            
            # Draw connecting lines
            self.draw_connecting_lines(self.avl.root)
            
            # Draw empty node positions
            for pos_name, (x, y) in self.tree_positions.items():
                self.canvas.create_oval(x-25, y-25, x+25, y+25, 
                                       outline="gray", dash=(2, 2), tags="template")
    
    def calculate_positions(self, node, x, y, x_offset, level):
        """Recursively calculate node positions based on AVL structure"""
        if not node:
            return
        
        # Store position with unique identifier
        pos_id = f"node_{node.key}"
        self.tree_positions[pos_id] = (x, y)
        
        # Calculate child positions
        y_offset = 100
        if node.left:
            self.calculate_positions(node.left, x - x_offset, y + y_offset, x_offset/2, level+1)
        if node.right:
            self.calculate_positions(node.right, x + x_offset, y + y_offset, x_offset/2, level+1)
    
    def draw_connecting_lines(self, node):
        """Draw lines between nodes based on actual tree structure"""
        if not node:
            return
        
        parent_pos = self.tree_positions.get(f"node_{node.key}")
        if parent_pos:
            if node.left:
                child_pos = self.tree_positions.get(f"node_{node.left.key}")
                if child_pos:
                    self.canvas.create_line(parent_pos, child_pos, dash=(2, 2), tags="template")
                    self.draw_connecting_lines(node.left)
            
            if node.right:
                child_pos = self.tree_positions.get(f"node_{node.right.key}")
                if child_pos:
                    self.canvas.create_line(parent_pos, child_pos, dash=(2, 2), tags="template")
                    self.draw_connecting_lines(node.right)
    
    def on_drag_start(self, event, val):
        node_data = next(n for n in self.draggable_nodes if n["val"] == val)
        self._drag_data = {
            "val": val,
            "start_x": event.x,
            "start_y": event.y,
            "initial_x": node_data["x"],
            "initial_y": node_data["y"]
        }
    
    def on_drag_motion(self, event, val):
        if not hasattr(self, '_drag_data') or self._drag_data["val"] != val:
            return
            
        dx = event.x - self._drag_data["start_x"]
        dy = event.y - self._drag_data["start_y"]
        
        node_data = next(n for n in self.draggable_nodes if n["val"] == val)
        self.canvas.move(node_data["node"], dx, dy)
        self.canvas.move(node_data["text"], dx, dy)
        
        node_data["x"] = self._drag_data["initial_x"] + dx
        node_data["y"] = self._drag_data["initial_y"] + dy
        
        self._drag_data["start_x"] = event.x
        self._drag_data["start_y"] = event.y
    
    def check_answer(self):
        """Validate the tree structure against user's placement"""
        # Map user's placements to tree positions
        user_placements = {}
        for node in self.draggable_nodes:
            closest_pos = None
            min_dist = float('inf')
            
            for pos_id, (pos_x, pos_y) in self.tree_positions.items():
                dist = sqrt((node["x"] - pos_x)**2 + (node["y"] - pos_y)**2)
                if dist < min_dist and dist < 30:  # 30 pixel threshold
                    min_dist = dist
                    closest_pos = pos_id
            
            if closest_pos:
                user_placements[closest_pos] = int(node["val"])
        
        # Validate each node in the AVL tree
        errors = []
        self.validate_node(self.avl.root, None, "root", user_placements, errors)
        
        # Check for extra nodes placed where they shouldn't be
        for pos_id in user_placements:
            if not pos_id.startswith("node_"):
                errors.append(f"Extra node placed at invalid position")
        
        if not errors:
            messagebox.showinfo("Correct!", "Perfect! Your AVL tree is correctly constructed.")
        else:
            messagebox.showerror("Incorrect", "\n".join(errors))
    
    def validate_node(self, node, parent, pos_id, user_placements, errors):
        """Recursively validate each node in the tree"""
        if not node:
            return
        
        expected_key = node.key
        user_key = user_placements.get(pos_id)
        
        if user_key is None:
            errors.append(f"Missing node for value {expected_key}")
        elif user_key != expected_key:
            errors.append(f"Position {pos_id.replace('node_', '')} should be {expected_key}, not {user_key}")
        
        # Validate children
        if node.left:
            self.validate_node(node.left, node, f"node_{node.left.key}", user_placements, errors)
        if node.right:
            self.validate_node(node.right, node, f"node_{node.right.key}", user_placements, errors)
    
    def new_question(self):
        self.generate_question()
        self.setup_ui()
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AVLQuizApp(root)
    root.mainloop()