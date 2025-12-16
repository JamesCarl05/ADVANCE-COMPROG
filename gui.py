import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Added for Treeview table
from export_pdf import export_to_pdf
from database import save_cleanup, get_all_cleanups, update_cleanup, delete_cleanup

# Ocean theme colors (updated for gradient background)
TOP_COLOR = "#02577A"    # Dark ocean blue for top
BOTTOM_COLOR = "#E0F6FF" # Very light blue (almost white) for bottom fade
BUTTON_COLOR = "#AFEEEE" # Pale turquoise for buttons (complements the gradient)
HOVER_COLOR = "#7FFFD4"  # Aquamarine for button hover indication
DARK_BLUE = "#0A0228"
WHITE = "#FFFFFF"

def calculate_impact(volunteers, bags):
    waste_kg = bags * 3.5           # avg trash bag weight
    plastic_reduction = waste_kg * 0.6
    animals_helped = int(waste_kg / 2.2)

    return {
        "volunteers": volunteers,
        "bags": bags,
        "waste_kg": waste_kg,
        "plastic_reduction": plastic_reduction,
        "animals_helped": animals_helped
    }

def create_gradient_canvas(parent, top_color, bottom_color):
    canvas = tk.Canvas(parent, bg=bottom_color)  # Set base background to bottom color for seamless fade
    canvas.pack(fill="both", expand=True)
    
    def draw_gradient(event=None):
        canvas.delete("gradient")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if height == 0:
            return
        for y in range(height):
            factor = y / height
            r1, g1, b1 = int(top_color[1:3], 16), int(top_color[3:5], 16), int(top_color[5:7], 16)
            r2, g2, b2 = int(bottom_color[1:3], 16), int(bottom_color[3:5], 16), int(bottom_color[5:7], 16)
            r = int(r1 + factor * (r2 - r1))
            g = int(g1 + factor * (g2 - g1))
            b = int(b1 + factor * (b2 - b1))
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, y, width, y, fill=color, tags="gradient")
    
    canvas.bind("<Configure>", draw_gradient)
    draw_gradient()  # Draw gradient immediately on creation
    return canvas

def style_button(btn):
    btn.config(bg=BUTTON_COLOR, fg=DARK_BLUE, font=("Times New Roman", 16, "bold"), bd=3)
    # Add hover indication
    btn.bind("<Enter>", lambda e: btn.config(bg=HOVER_COLOR))
    btn.bind("<Leave>", lambda e: btn.config(bg=BUTTON_COLOR))

def style_label(lbl):
    lbl.config(bg=TOP_COLOR, fg=DARK_BLUE, font=("Times New Roman", 16))  # Use top color for labels to blend with top of gradient

def welcome_screen(root):
    canvas = create_gradient_canvas(root, TOP_COLOR, BOTTOM_COLOR)
    
    # Bordered container for welcome elements to make it more visually appealing
    container = tk.Frame(root, bg=TOP_COLOR, relief="ridge", bd=8)
    container_window = canvas.create_window(0, 0, window=container, anchor="center")
    
    title = tk.Label(container, text="🌊🌊 Clean Impact for the Waves 🌊🌊",
                     font=("Times New Roman", 36, "bold"), bg=TOP_COLOR, fg=WHITE)
    title.pack(pady=(30, 10))
    
    subtitle = tk.Label(container, text="Join the movement to protect our oceans!\nCalculate your beach cleanup impact today.",
                        font=("Times New Roman", 18), bg=TOP_COLOR, fg=WHITE, justify="center")
    subtitle.pack(pady=(0, 20))
    
    start_btn = tk.Button(container, text="🚀 Start Your Journey", command=lambda: load_input(root, canvas))
    style_button(start_btn)
    start_btn.config(font=("Times New Roman", 20, "bold"))  # Make button text larger
    start_btn.pack(pady=30)
    
    def place_widgets(event=None):
        canvas.coords(container_window, canvas.winfo_width() / 2, canvas.winfo_height() / 2)
    
    canvas.bind("<Configure>", place_widgets)
    place_widgets()  # Initial placement

def load_input(root, old_canvas=None):
    if old_canvas:
        old_canvas.destroy()
    
    canvas = create_gradient_canvas(root, TOP_COLOR, BOTTOM_COLOR)
    
    # Bordered container for all input elements
    container = tk.Frame(root, bg=TOP_COLOR, relief="ridge", bd=5)
    container_window = canvas.create_window(0, 0, window=container, anchor="center")
    
    input_title = tk.Label(container, text="Beach Cleanup Input",
                           font=("Times New Roman", 26, "bold"), bg=WHITE, fg=DARK_BLUE)
    input_title.pack(pady=(20, 10))
    
    vol_label = tk.Label(container, text="Number of Volunteers:", bg=TOP_COLOR, fg=WHITE,
                         font=("Times New Roman", 16))
    vol_label.pack(pady=(10, 5))
    volunteers_entry = tk.Entry(container, font=("Times New Roman", 16))
    volunteers_entry.pack()
    
    bags_label = tk.Label(container, text="Trash Bags Collected:", bg=TOP_COLOR, fg=WHITE,
                          font=("Times New Roman", 16))
    bags_label.pack(pady=(10, 5))
    bags_entry = tk.Entry(container, font=("Times New Roman", 16))
    bags_entry.pack()
    
    # Button row for Calculate Impact and Exit buttons
    button_row = tk.Frame(container, bg=TOP_COLOR)
    button_row.pack(pady=20)
    
    submit_btn = tk.Button(button_row, text="Calculate Impact", command=lambda: compute())
    style_button(submit_btn)
    submit_btn.grid(row=0, column=0, padx=15)
    
    exit_btn = tk.Button(button_row, text="Exit", command=root.destroy)
    style_button(exit_btn)
    exit_btn.grid(row=0, column=1, padx=15)
    
    def compute():
        try:
            volunteers = int(volunteers_entry.get())
            bags = int(bags_entry.get())
            results = calculate_impact(volunteers, bags)
            
            save_cleanup(volunteers, bags, results["waste_kg"])
            load_results(root, canvas, results)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for volunteers and bags.")
    
    def place_widgets(event=None):
        canvas.coords(container_window, canvas.winfo_width() / 2, canvas.winfo_height() / 2)
    
    canvas.bind("<Configure>", place_widgets)
    place_widgets()  # Initial placement

def load_results(root, old_canvas, results):
    old_canvas.destroy()
    
    canvas = create_gradient_canvas(root, TOP_COLOR, BOTTOM_COLOR)
    
    # Bordered container for all results elements
    container = tk.Frame(root, bg=TOP_COLOR, relief="ridge", bd=5)
    container_window = canvas.create_window(0, 0, window=container, anchor="center")
    
    # Title
    title = tk.Label(container, text="Your Environmental Impact",
                     font=("Times New Roman", 32, "bold"),
                     bg=TOP_COLOR, fg=WHITE)
    title.pack(pady=(20, 10))
    
    # Table container (DARK_BLUE box)
    table_container = tk.Frame(container, bg=DARK_BLUE, bd=4, relief="ridge")
    table_container.pack(pady=10)
    
    table = tk.Frame(table_container, bg=DARK_BLUE)
    table.pack(padx=40, pady=40)
    
    labels = [
        "Volunteers:",
        "Trash Bags Collected:",
        "Total Waste Removed:",
        "Plastic Prevented From Ocean:",
        "Marine Animals Helped:"
    ]
    
    values = [
        results['volunteers'],
        results['bags'],
        f"{results['waste_kg']:.1f} kg",
        f"{results['plastic_reduction']:.1f} kg",
        results['animals_helped']
    ]
    
    # Table rows
    for i, (label_txt, val_txt) in enumerate(zip(labels, values)):
        lbl = tk.Label(table, text=label_txt, bg=DARK_BLUE,
                       fg=WHITE, font=("Times New Roman", 18),
                       anchor="w")
        lbl.grid(row=i, column=0, padx=30, pady=8, sticky="w")
        
        val = tk.Label(table, text=val_txt, bg=DARK_BLUE,
                       fg=WHITE, font=("Times New Roman", 18, "bold"),
                       anchor="e")
        val.grid(row=i, column=1, padx=30, pady=8, sticky="e")
    
    # Button row
    button_row = tk.Frame(container, bg=TOP_COLOR)  # Match top color
    button_row.pack(pady=20)
    
    def go_back():
        load_input(root, canvas)
    
    back_btn = tk.Button(button_row, text="Back to Input", command=go_back)
    style_button(back_btn)
    back_btn.grid(row=0, column=0, padx=15)
    
    def export():
        filename = export_to_pdf(results)
        messagebox.showinfo("PDF Saved", f"PDF exported as:\n{filename}")
    
    pdf_btn = tk.Button(button_row, text="Export to PDF", command=export)
    style_button(pdf_btn)
    pdf_btn.grid(row=0, column=1, padx=15)
    
    history_btn = tk.Button(button_row, text="View History", command=lambda: load_history(root, canvas))
    style_button(history_btn)
    history_btn.grid(row=0, column=2, padx=15)
    
    exit_btn = tk.Button(button_row, text="Exit", command=root.destroy)
    style_button(exit_btn)
    exit_btn.grid(row=0, column=3, padx=15)
    
    def place_widgets(event=None):
        canvas.coords(container_window, canvas.winfo_width() / 2, canvas.winfo_height() / 2)
    
    canvas.bind("<Configure>", place_widgets)
    place_widgets()  # Initial placement

# New: Load history screen with CRUD options
def load_history(root, old_canvas):
    old_canvas.destroy()
    
    canvas = create_gradient_canvas(root, TOP_COLOR, BOTTOM_COLOR)
    
    container = tk.Frame(root, bg=TOP_COLOR, relief="ridge", bd=5)
    container_window = canvas.create_window(0, 0, window=container, anchor="center")
    
    title = tk.Label(container, text="Cleanup History",
                     font=("Times New Roman", 32, "bold"), bg=TOP_COLOR, fg=WHITE)
    title.pack(pady=(20, 10))
    
    # Treeview for displaying cleanups
    tree = ttk.Treeview(container, columns=("ID", "Volunteers", "Bags", "Waste"), show="headings", height=10)
    tree.heading("ID", text="ID")
    tree.heading("Volunteers", text="Volunteers")
    tree.heading("Bags", text="Bags")
    tree.heading("Waste", text="Waste (kg)")
    tree.column("ID", width=50)
    tree.column("Volunteers", width=100)
    tree.column("Bags", width=100)
    tree.column("Waste", width=100)
    tree.pack(pady=10)
    
    # Populate tree with data
    cleanups = get_all_cleanups()
    for row in cleanups:
        tree.insert("", "end", values=row)
    
    # Button row
    button_row = tk.Frame(container, bg=TOP_COLOR)
    button_row.pack(pady=20)
    
    def view_details():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a cleanup to view.")
            return
        item = tree.item(selected[0])
        cleanup_id, volunteers, bags, waste = item["values"]
        results = calculate_impact(int(volunteers), int(bags))
        results["waste_kg"] = waste  # Use stored waste
        load_results(root, canvas, results)  # Reuse results screen
    
    view_btn = tk.Button(button_row, text="View Details", command=view_details)
    style_button(view_btn)
    view_btn.grid(row=0, column=0, padx=10)
    
    def edit_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a cleanup to edit.")
            return
        item = tree.item(selected[0])
        cleanup_id, volunteers, bags, waste = item["values"]
        load_edit(root, canvas, int(cleanup_id), int(volunteers), int(bags))
    
    edit_btn = tk.Button(button_row, text="Edit", command=edit_selected)
    style_button(edit_btn)
    edit_btn.grid(row=0, column=1, padx=10)
    
    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a cleanup to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this cleanup?")
        if confirm:
            item = tree.item(selected[0])
            cleanup_id = item["values"][0]
            delete_cleanup(cleanup_id)
            tree.delete(selected[0])
            messagebox.showinfo("Deleted", "Cleanup deleted successfully.")
    
    delete_btn = tk.Button(button_row, text="Delete", command=delete_selected)
    style_button(delete_btn)
    delete_btn.grid(row=0, column=2, padx=10)
    
    back_btn = tk.Button(button_row, text="Back", command=lambda: load_input(root, canvas))
    style_button(back_btn)
    back_btn.grid(row=0, column=3, padx=10)
    
    def place_widgets(event=None):
        canvas.coords(container_window, canvas.winfo_width() / 2, canvas.winfo_height() / 2)
    
    canvas.bind("<Configure>", place_widgets)
    place_widgets()

# New: Load edit screen (pre-filled input for update)
def load_edit(root, old_canvas, cleanup_id, volunteers, bags):
    old_canvas.destroy()
    
    canvas = create_gradient_canvas(root, TOP_COLOR, BOTTOM_COLOR)
    
    container = tk.Frame(root, bg=TOP_COLOR, relief="ridge", bd=5)
    container_window = canvas.create_window(0, 0, window=container, anchor="center")
    
    edit_title = tk.Label(container, text="Edit Cleanup",
                          font=("Times New Roman", 26, "bold"), bg=WHITE, fg=DARK_BLUE)
    edit_title.pack(pady=(20, 10))
    
    vol_label = tk.Label(container, text="Number of Volunteers:", bg=TOP_COLOR, fg=WHITE,
                         font=("Times New Roman", 16))
    vol_label.pack(pady=(10, 5))
    volunteers_entry = tk.Entry(container, font=("Times New Roman", 16))
    volunteers_entry.insert(0, str(volunteers))  # Pre-fill with existing value
    volunteers_entry.pack()
    
    bags_label = tk.Label(container, text="Trash Bags Collected:", bg=TOP_COLOR, fg=WHITE,
                          font=("Times New Roman", 16))
    bags_label.pack(pady=(10, 5))
    bags_entry = tk.Entry(container, font=("Times New Roman", 16))
    bags_entry.insert(0, str(bags))  # Pre-fill with existing value
    bags_entry.pack()
    
    # Button row
    button_row = tk.Frame(container, bg=TOP_COLOR)
    button_row.pack(pady=20)
    
    def save_changes():
        try:
            new_volunteers = int(volunteers_entry.get())
            new_bags = int(bags_entry.get())
            new_results = calculate_impact(new_volunteers, new_bags)
            update_cleanup(cleanup_id, new_volunteers, new_bags, new_results["waste_kg"])
            messagebox.showinfo("Updated", "Cleanup updated successfully!")
            load_results(root, canvas, new_results)  # Show updated results
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for volunteers and bags.")
    
    save_btn = tk.Button(button_row, text="Save Changes", command=save_changes)
    style_button(save_btn)
    save_btn.grid(row=0, column=0, padx=15)
    
    cancel_btn = tk.Button(button_row, text="Cancel", command=lambda: load_history(root, canvas))
    style_button(cancel_btn)
    cancel_btn.grid(row=0, column=1, padx=15)
    
    def place_widgets(event=None):
        canvas.coords(container_window, canvas.winfo_width() / 2, canvas.winfo_height() / 2)
    
    canvas.bind("<Configure>", place_widgets)
    place_widgets()  # Initial placement
