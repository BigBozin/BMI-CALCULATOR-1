import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import math
import time
import threading

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2a23e6")
        
        # Make window responsive
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Variables
        self.height_var = tk.DoubleVar(value=0.00)
        self.weight_var = tk.DoubleVar(value=0.00)
        self.bmi_var = tk.StringVar(value="BMI: --")
        self.category_var = tk.StringVar(value="Category: --")
        self.health_advice_var = tk.StringVar(value="Enter your details and click Calculate")
        
        # Animation control
        self.is_animating = False
        self.current_scale_weight = 0
        
        # Load your images
        self.load_images()
        self.create_widgets()
        
    def load_images(self):
        """Load your actual image files"""
        try:
            # Load and resize your images
            self.calc_img = self.load_and_resize_image("images/bmiICON3.png", 300, 200)
            self.chart_img = self.load_and_resize_image("images/BMI Chart African Boy-D2.jpg", 550, 200)
            self.title_img = self.load_and_resize_image("images/bmiCAL.png", 250, 80)
            
        except Exception as e:
            print(f"Error loading images: {e}")
            self.create_placeholder_images()
    
    def load_and_resize_image(self, filename, width, height):
        """Load and resize an image file"""
        try:
            image = Image.open(filename)
            image = image.resize((width, height), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Could not load {filename}: {e}")
            return self.create_placeholder_image(f"Image: {filename}", width, height, "#34495e")
    
    def create_placeholder_image(self, text, width, height, color):
        """Create placeholder image"""
        from PIL import Image, ImageDraw, ImageFont
        
        image = Image.new('RGB', (width, height), color)
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()
            
        draw.rectangle([0, 0, width-1, height-1], outline='#3498db', width=2)
        lines = text.split('\n')
        y_offset = height // 2 - len(lines) * 8
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, y_offset), line, fill='white', font=font)
            y_offset += 16
            
        return ImageTk.PhotoImage(image)
    
    def create_placeholder_images(self):
        """Create all placeholder images"""
        self.calc_img = self.create_placeholder_image("BMI\nCALCULATOR\nICON", 300, 250, "#3498db")
        self.chart_img = self.create_placeholder_image("BMI CATEGORIES", 350, 200, "#e74c3c")
        self.title_img = self.create_placeholder_image("BMI\nCALCULATOR", 250, 80, "#2980b9")

    def create_scale_canvas(self):
        """Create a dynamic scale canvas"""
        self.scale_canvas = tk.Canvas(self.right_column, width=180, height=250, 
                                    bg='#1a1a1a', highlightthickness=0)
        self.scale_canvas.pack(pady=10, fill=tk.BOTH, expand=True)
        self.draw_scale()

    def draw_scale(self, current_weight=0):
        """Draw the scale with current weight"""
        self.scale_canvas.delete("all")
        
        # Get canvas dimensions for responsive scaling
        canvas_width = self.scale_canvas.winfo_width()
        canvas_height = self.scale_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 180
            canvas_height = 250
        
        # Scale dimensions (responsive)
        scale_width = max(100, canvas_width - 60)
        scale_height = max(150, canvas_height - 80)
        scale_x = (canvas_width - scale_width) // 2
        scale_y = (canvas_height - scale_height) // 2
        
        # Draw scale background
        self.scale_canvas.create_rectangle(scale_x, scale_y, 
                                         scale_x + scale_width, 
                                         scale_y + scale_height, 
                                         fill='#333333', outline='#666666', width=2)
        
        # Draw scale markings (0 to 100 kg)
        for i in range(0, 101, 10):
            # Calculate position (0 at bottom, 100 at top)
            position_ratio = i / 100
            y_pos = scale_y + scale_height - (position_ratio * scale_height)
            
            # Draw main markings every 10kg
            self.scale_canvas.create_line(scale_x - 10, y_pos, scale_x, y_pos, 
                                        fill='white', width=2)
            self.scale_canvas.create_text(scale_x - 15, y_pos, text=str(i), 
                                        fill='white', font=('Arial', 8), anchor='e')
            
            # Draw minor markings every 5kg
            if i < 100:
                minor_y = y_pos - (scale_height * 0.05)
                self.scale_canvas.create_line(scale_x - 5, minor_y, scale_x, minor_y, 
                                            fill='white', width=1)
        
        # Draw needle based on current weight
        if 0 <= current_weight <= 100:
            position_ratio = current_weight / 100
            needle_y = scale_y + scale_height - (position_ratio * scale_height)
            
            # Draw needle
            self.scale_canvas.create_line(scale_x, needle_y, scale_x + scale_width, needle_y, 
                                        fill='#e74c3c', width=3)
            
            # Draw needle pointer
            self.scale_canvas.create_polygon(
                scale_x + scale_width, needle_y - 5,
                scale_x + scale_width + 8, needle_y,
                scale_x + scale_width, needle_y + 5,
                fill='#c0392b'
            )
        
        # Display current weight
        self.scale_canvas.create_text(scale_x + scale_width//2, scale_y + scale_height + 20,
                                    text=f"{current_weight} kg", 
                                    fill='#f39c12', font=('Arial', 12, 'bold'))

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="BMI CALCULATOR", 
                              font=('Arial', 20, 'bold'), foreground='white',
                              background="#c8d604")
        title_label.pack(pady=10)

        # Create three columns with responsive layout
        columns_frame = ttk.Frame(main_frame)
        columns_frame.pack(fill=tk.BOTH, expand=True)
        
        # Make columns responsive
        columns_frame.columnconfigure(0, weight=1)
        columns_frame.columnconfigure(1, weight=1)  
        columns_frame.columnconfigure(2, weight=1)
        columns_frame.rowconfigure(0, weight=1)

        # Left Column - Input Section with light border
        left_column = ttk.LabelFrame(columns_frame, text="Enter Your Details", padding="15")
        left_column.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        left_column.columnconfigure(0, weight=1)

        # Height input
        height_frame = ttk.Frame(left_column)
        height_frame.pack(fill=tk.X, pady=10)
        ttk.Label(height_frame, text="Height (meters):", font=('Arial', 12)).pack(side=tk.LEFT)
        
        height_entry = ttk.Entry(height_frame, textvariable=self.height_var, 
                               font=('Arial', 12), width=8, justify='center')
        height_entry.pack(side=tk.RIGHT, padx=10)
        height_entry.bind('<Return>', self.on_height_entry_change)

        # Weight input
        weight_frame = ttk.Frame(left_column)
        weight_frame.pack(fill=tk.X, pady=10)
        ttk.Label(weight_frame, text="Weight (kg):", font=('Arial', 12)).pack(side=tk.LEFT)
        
        weight_entry = ttk.Entry(weight_frame, textvariable=self.weight_var, 
                               font=('Arial', 12), width=8, justify='center')
        weight_entry.pack(side=tk.RIGHT, padx=10)
        weight_entry.bind('<Return>', self.on_weight_entry_change)

        # Calculate button
        self.calc_button = ttk.Button(left_column, text="CALCULATE BMI", 
                                    command=self.calculate_bmi, style='Accent.TButton')
        self.calc_button.pack(pady=10)

        # Loading label - CENTERED
        self.loading_var = tk.StringVar(value="")
        self.loading_label = ttk.Label(left_column, textvariable=self.loading_var,
                                     font=('Arial', 10), foreground='#f39c12',
                                     justify=tk.CENTER, anchor='center')
        # Ensure the label is centered within its container
        self.loading_label.pack(fill=tk.X, anchor='center')

        # Current values display with light border
        values_frame = ttk.LabelFrame(left_column, text="Current Values", padding="10")
        values_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(values_frame, text=f"Height: {self.height_var.get()} m", 
                 font=('Arial', 10)).pack(pady=5)
        ttk.Label(values_frame, text=f"Weight: {self.weight_var.get()} kg", 
                 font=('Arial', 10)).pack(pady=5)

        # Middle Column - Calculator Image with light border
        middle_column = ttk.LabelFrame(columns_frame, text="BMI Calculator", padding="0")
        middle_column.grid(row=0, column=1, sticky='nsew', padx=0, pady=0)
        middle_column.columnconfigure(0, weight=1)

        if hasattr(self, 'calc_img'):
            calc_label = ttk.Label(middle_column, image=self.calc_img)
            calc_label.pack(pady=0)

        # BMI Display in middle column
        bmi_display_frame = ttk.Frame(middle_column)
        bmi_display_frame.pack(pady=5, fill=tk.X)
        
        self.bmi_label = ttk.Label(bmi_display_frame, textvariable=self.bmi_var,
                                 font=('Arial', 24, 'bold'), foreground='#2980b9')
        self.bmi_label.pack()

        category_label = ttk.Label(bmi_display_frame, textvariable=self.category_var,
                                 font=('Arial', 14), foreground='#2c3e50')
        category_label.pack(pady=5)

        # Health advice
        health_frame = ttk.Frame(middle_column)
        health_frame.pack(pady=5, fill=tk.X, expand=True)
        
        health_label = ttk.Label(health_frame, textvariable=self.health_advice_var,
                               font=('Arial', 12), foreground='#27ae60', 
                               wraplength=650, justify=tk.CENTER)
        health_label.pack(fill=tk.BOTH, expand=True)

        # Right Column - Scale with light border
        self.right_column = ttk.LabelFrame(columns_frame, text="WEIGHT SCALE", padding="15")
        self.right_column.grid(row=0, column=2, sticky='nsew', padx=0, pady=0)
        self.right_column.columnconfigure(0, weight=1)
        self.right_column.rowconfigure(0, weight=1)

        # Create the scale canvas
        self.create_scale_canvas()

        # Scale info
        scale_info = ttk.Label(self.right_column, text="Scale: 0-100 kg", 
                             font=('Arial', 9), foreground="#1c0fcf")
        scale_info.pack(pady=0)

        # Bottom Section - BMI Chart with light border - CENTERED
        bottom_frame = ttk.LabelFrame(main_frame, text="BMI Categories Reference", padding="10")
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        bottom_frame.columnconfigure(0, weight=1)

        if hasattr(self, 'chart_img'):
            # Put the image inside a centered container so it stays centered
            chart_container = ttk.Frame(bottom_frame)
            chart_container.pack(fill=tk.BOTH, expand=True)
            chart_container.columnconfigure(0, weight=1)
            chart_container.rowconfigure(0, weight=1)

            chart_label = ttk.Label(chart_container, image=self.chart_img)
            # Use pack with expand and center anchor to keep image centered
            chart_label.pack(anchor='center', expand=True)
        else:
            # Text categories as fallback - CENTERED
            categories_frame = ttk.Frame(bottom_frame)
            categories_frame.pack(fill=tk.BOTH, expand=True)
            
            categories = [
                ("UNDERWEIGHT", "< 18.5", "#3498db"),
                ("NORMAL WEIGHT", "18.5 - 24.9", "#2ecc71"),
                ("OVERWEIGHT", "25 - 29.9", "#f39c12"),
                ("OBESE", "30.0 - 34.9", "#e74c3c"),
                ("EXTREMELY OBESE", "35.0+", "#c0392b")
            ]
            
            # Create a centered container for categories
            centered_container = ttk.Frame(categories_frame)
            centered_container.pack(expand=True)
            
            for i, (category, range_val, color) in enumerate(categories):
                cat_frame = ttk.Frame(centered_container)
                cat_frame.pack(side=tk.CENTER, padx=15)
                
                ttk.Label(cat_frame, text=category, font=('Arial', 10, 'bold'),
                         foreground=color, justify=tk.CENTER).pack(pady=5)
                ttk.Label(cat_frame, text=range_val, font=('Arial', 9), 
                         justify=tk.CENTER).pack()

        # Configure styles
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Arial', 12, 'bold'))

        # Bind resize event for responsive scaling
        self.root.bind('<Configure>', self.on_resize)

    def on_resize(self, event=None):
        """Handle window resize for responsive design"""
        if hasattr(self, 'scale_canvas'):
            # Redraw scale with new dimensions
            self.root.after(100, self.redraw_scale)

    def redraw_scale(self):
        """Redraw scale after resize"""
        current_weight = min(self.weight_var.get(), 100)
        self.draw_scale(current_weight)

    def on_height_entry_change(self, event=None):
        try:
            height = float(self.height_var.get())
            if 1.0 <= height <= 2.5:
                pass
            else:
                messagebox.showerror("Error", "Height must be between 1.0 and 2.5 meters")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for height")

    def on_weight_entry_change(self, event=None):
        try:
            weight = float(self.weight_var.get())
            if 0 <= weight <= 200:
                # Update scale immediately when weight is entered
                self.draw_scale(min(weight, 100))
            else:
                messagebox.showerror("Error", "Weight must be between 0 and 200 kg")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for weight")

    def calculate_bmi(self):
        """Calculate BMI with animations"""
        if self.is_animating:
            return
            
        try:
            height = self.height_var.get()
            weight = self.weight_var.get()
            
            if height <= 0 or weight <= 0:
                raise ValueError("Invalid values")
            
            # Calculate BMI
            bmi = weight / (height * height)
            
            # Start animations
            self.is_animating = True
            self.calc_button.config(state='disabled')
            self.animate_calculation(weight, bmi)
            
        except Exception as e:
            messagebox.showerror("Error", "Please enter valid height and weight values")

    def animate_calculation(self, target_weight, target_bmi):
        """Animate both scale and BMI value"""
        self.loading_var.set("Calculating...")
        
        # Start animation in separate thread
        thread = threading.Thread(target=self.combined_animation, 
                                args=(target_weight, target_bmi))
        thread.daemon = True
        thread.start()

    def combined_animation(self, target_weight, target_bmi):
        """Animate scale and BMI simultaneously"""
        # Scale animation (0 to target weight)
        scale_steps = 20
        scale_step_size = min(target_weight, 100) / scale_steps
        
        # BMI animation (0 to target BMI)
        bmi_steps = 20
        bmi_step_size = target_bmi / bmi_steps
        
        for step in range(max(scale_steps, bmi_steps) + 1):
            if not self.is_animating:
                break
                
            # Update scale
            if step <= scale_steps:
                current_scale_weight = step * scale_step_size
                self.root.after(0, lambda w=current_scale_weight: self.draw_scale(w))
            
            # Update BMI
            if step <= bmi_steps:
                current_bmi = step * bmi_step_size
                self.root.after(0, lambda b=current_bmi: self.update_bmi_display(b))
            
            # Update loading text
            progress = (step / max(scale_steps, bmi_steps)) * 100
            self.root.after(0, lambda: self.loading_var.set(f"Calculating... {int(progress)}%"))
            
            time.sleep(0.08)  # Animation speed
        
        # Final update
        self.root.after(0, self.finalize_calculation, target_bmi)

    def update_bmi_display(self, bmi_value):
        """Update BMI display during animation"""
        self.bmi_var.set(f"BMI: {bmi_value:.1f}")

    def finalize_calculation(self, final_bmi):
        """Finalize calculation after animation"""
        self.bmi_var.set(f"BMI: {final_bmi:.1f}")
        self.update_category(final_bmi)
        self.loading_var.set("Calculation Complete!")
        
        # Re-enable button after delay
        self.root.after(2000, lambda: self.calc_button.config(state='normal'))
        self.root.after(2000, lambda: self.loading_var.set(""))
        self.is_animating = False

    def update_category(self, bmi):
        """Update BMI category and health advice"""
        if bmi < 18.5:
            category = "Underweight"
            color = "#3498db"
            advice = "Consider consulting a healthcare provider for healthy weight gain strategies and nutrition guidance."
        elif 18.5 <= bmi < 25:
            category = "Normal Weight"
            color = "#2ecc71"
            advice = "Excellent! Maintain your healthy weight with balanced nutrition and regular physical activity."
        elif 25 <= bmi < 30:
            category = "Overweight"
            color = "#f39c12"
            advice = "Consider incorporating more physical activity and adopting balanced eating habits for optimal health."
        elif 30 <= bmi < 35:
            category = "Obese"
            color = "#e74c3c"
            advice = "Consult with a healthcare provider for personalized weight management and health improvement strategies."
        else:
            category = "Extremely Obese"
            color = "#c0392b"
            advice = "Please consult a healthcare provider for comprehensive weight management guidance and support."
        
        self.category_var.set(f"Category: {category}")
        self.health_advice_var.set(advice)
        self.bmi_label.configure(foreground=color)

def main():
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()