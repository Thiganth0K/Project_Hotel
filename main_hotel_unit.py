import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
from datetime import datetime
import string
import random



def ordered_food():
    selected_items = []
    selected_items_dict = {}
    total_amount = 0 
    for var, item, quantity_entry in zip(vars, items_with_amount, quantity_entries):
        if var.get() == 1:
            quantity = quantity_entry.get()
            if quantity.strip() != '' and quantity.isdigit():
                selected_items.append(f' {item} ({quantity}) ')
                total_amount += float(items_with_amount[item].replace('rs:', '')) * int(quantity)
                selected_items_dict[item] = quantity
            else:
                messagebox.showwarning('Warning', 'Please enter a valid quantity for all selected items.')
                return

    if not selected_items:
        messagebox.showwarning('Warning', 'Please select at least one item.')
    else:
        order_confirmation = ('You Ordered:\n' + '\n'.join(selected_items) + '\n\nTotal Amount: ' + f'{total_amount:.2f}')
        result = messagebox.askokcancel('Order Confirmation', order_confirmation)
        if result:
            print("Order Placed")
            messagebox.showinfo("Order Info", "Order Placed")
            print(selected_items)
            print(selected_items_dict)

            ordered_time = datetime.now().strftime('%d-%m-%Y | %H:%M:%S')
            if result:
                #dict_to_excel(selected_items_dict, ordered_time,rating_value)

                # Add star rating feedback
                feedback_window = tk.Toplevel(root)
                feedback_window.title("Feedback")
                
                feedback_label = tk.Label(feedback_window, text="Please rate your experience:")
                feedback_label.pack()
                
                rating_frame = ttk.Frame(feedback_window)
                rating_frame.pack()
                
                rating_var = tk.DoubleVar()
                rating_var.set(5.0)  # Default rating
                rating_value=round(rating_var.get(),1)
                dict_to_excel(selected_items_dict,ordered_time,rating_value)

                rating_scale = ttk.Scale(rating_frame, from_=1, to=5, orient=tk.HORIZONTAL, variable=rating_var, style="Custom.Horizontal.TScale")
                rating_scale.pack(side=tk.LEFT)
                
                def update_rating_label(value):
                    rating_label.config(text=f"You rated: {value:.1f} stars")
                
                rating_scale.bind("<Motion>", lambda event: update_rating_label(rating_var.get()))
                
                rating_label = tk.Label(feedback_window, text="", font=("Arial", 12))
                rating_label.pack()
                
                increase_button = tk.Button(rating_frame, text="+", command=lambda: rating_var.set(min(rating_var.get() + 1, 5)))
                increase_button.pack(side=tk.LEFT, padx=5)
                
                decrease_button = tk.Button(rating_frame, text="-", command=lambda: rating_var.set(max(rating_var.get() - 1, 1)))
                decrease_button.pack(side=tk.LEFT, padx=5)
                
                submit_button = ttk.Button(feedback_window, text="Submit Rating",
                                           command=lambda: submit_feedback(round(rating_var.get(), 1), feedback_window,selected_items_dict))
                submit_button.pack()
                

        else:
            print("Order Cancelled")
            messagebox.showinfo("Order Info", "Order Cancelled")

def submit_feedback(rating, feedback_window,selected_items_dict):
    # Save the rating to a file or database
    messagebox.showinfo("Feedback Submitted", f"Thank you for your feedback! You rated us {rating} stars.")
    feedback_window.destroy()
    ordered_time=datetime.now().strftime('%d-%m-%Y | %H:%M:%S')
    dict_to_excel(selected_items_dict,ordered_time,rating)


def generate_token(length=6):
    letters_and_digits=string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range (length))



def dict_to_excel(data, ordered_time,rating=None):
    items_list = [(key, value) for key, value in data.items()]
    df = pd.DataFrame(items_list, columns=['Items', 'Quantity'])
    df['Ordered Time'] = ordered_time
    df['Rating']= rating if rating is not None else 'Not Rated'
    df['Token']=generate_token()
    excel_file = 'order_log.xlsx'
    df.to_excel(excel_file, index=False)
    print(f'DataFrame is exported successfully to {excel_file}')

# Define food items
items_with_amount = {'Chilli Parotta': 'rs:55',
                    'Kaima Parotta': 'rs:55',
                    'Ghee Podi Roast': 'rs:70',
                    'Full Meals': 'rs:80',
                    'Porichu Parotta(5 pieces)': 'rs:60',
                    'Tea': 'rs:10',
                    'Coffee': 'rs:10'
                    }

# Main window
root = tk.Tk()
root.title('Food Menu')

# Load background image
bg_image = Image.open("monsrow_logo.png")
bg_resized = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_resized)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Hotel details
hotel_label = tk.Label(root, text='Monsrow Hotel', font=("Arial", 16, "bold"), fg='navy')
hotel_label.place(x=200, y=30, anchor="center")

address_label = tk.Label(root, text="100, South Car Street,\nChidambaram-608001,\nContact no: 6383449503",
                         font=("Arial", 10, "normal"), fg='darkblue')
address_label.place(x=200, y=70, anchor="center")

# Menu label
menu_label = tk.Label(root, text='  MENU  ', font=("Courier New", 14, "bold"), fg='navy',bg='white')
menu_label.place(x=200, y=120, anchor="center")

# Checkboxes and quantity entries
vars = []
check_boxes = []
quantity_entries = []
for index, item in enumerate(items_with_amount.keys()):
    var = tk.IntVar()
    vars.append(var)
    check_box = tk.Checkbutton(root, text=f'{item} ({items_with_amount[item]})', variable=var, font=("Arial", 10),
                                fg='black', bg='lightyellow')
    check_box.place(x=20, y=150 + index * 40, anchor="w")
    check_boxes.append(check_box)

    quantity_label = tk.Label(root, text='Quantity:', justify='center', font=("Arial", 10), fg='black')
    quantity_label.place(x=300, y=150 + index * 40, anchor="e")

    quantity_entry = tk.Entry(root, justify='center', width=5, font=("Arial", 10))
    quantity_entry.place(x=330, y=150 + index * 40, anchor="w", height=20)
    quantity_entries.append(quantity_entry)

# Order button
order_button = tk.Button(root, text='Place Order', command=ordered_food, font=("Arial", 12, "bold"), fg='white',
                         bg='green', activebackground='darkgreen', activeforeground='black')
order_button.place(x=200, y=200 + len(items_with_amount) * 40, anchor="center")

# Customizing the style of the Scale widget
style = ttk.Style()
style.configure("Custom.Horizontal.TScale", troughcolor="lightblue", sliderlength=30)
style.map("Custom.Horizontal.TScale", background=[('active', 'yellow')])

# Tkinter event loop
root.mainloop()