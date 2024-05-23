import psycopg2
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tkmb

conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="2557", port="5432")

def create_table():
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS cars (
                    id SERIAL PRIMARY KEY,
                    manufacturer VARCHAR(255) NOT NULL,
                    model VARCHAR(255) NOT NULL,
                    horsepower INTEGER NOT NULL,
                    engine FLOAT NOT NULL);       
                    """)
    cur.close()
    conn.commit()


def insert_data_from_csv():
    with open("cars.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter=';')
        values =[]
        for row in reader:
            value = (row[0], row[1], row[2], row[3], row[4])
            values.append(value)

    query = "INSERT INTO cars (id, manufacturer, model, horsepower, engine) VALUES (%s, %s, %s, %s, %s)"
    cur = conn.cursor()
    cur.executemany(query, values)
    conn.commit()
    cur.close()




def get_last_id():
    cur = conn.cursor()
    cur.execute("SELECT id FROM cars ORDER BY id DESC LIMIT 1")
    return cur.fetchone()[0]
    cur.close()


def insert_new_car(manufacturer, model, horsepower, engine):
    try:
        cur = conn.cursor()
        id = get_last_id()
        values = (id+1, manufacturer, model, horsepower, engine)
        cur = conn.cursor()
        query = "INSERT INTO cars (id, manufacturer, model, horsepower, engine) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, values)
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)

app = tk.Tk()
app.geometry('800x500')
app.title('Cars Database')
label1 = tk.Label(app, text='Cars Database', font=('Helvetica', 20))
label1.pack(pady=30)


table = ttk.Treeview(app)
table['columns'] = ('id', 'manufacturer', 'model', 'horsepower', 'engine')
table['show'] = 'headings'
table.heading('id', text='ID')
table.heading('manufacturer', text='Manufacturer')
table.heading('model', text='Model')
table.heading('horsepower', text='Horsepower')
table.heading('engine', text='Engine')
table.pack(fill=tk.BOTH, expand=True, padx=20)


def get_data_from_db():
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars ORDER BY id DESC")
    for record in cur.fetchall():
        count=0
        table.insert(parent='', index=count, values=record)
        count+=1
get_data_from_db()

def open_new_window():
    app2 = tk.Tk()
    app2.geometry('800x500')
    app2.title('New window')
    label2 = tk.Label(app2, text='Spinboxes', font=('Helvetica', 20))
    label2.pack(pady=10)

    items = ('toyota', 'chrysler', 'ford', 'mazda')
    manufacturer_string = tk.StringVar(value=items[0])
    combo = ttk.Combobox(app2, textvariable = manufacturer_string)
    combo['values'] = items
    combo.pack(pady=10)

    combo.bind('<<ComboboxSelected>>', lambda event: print(combo.get()))


    app.destroy()

def delete_selected_item():
    selected_item = table.selection()
    if selected_item:
        item_id = selected_item[0]
        item_values = table.item(item_id, 'values')
        tkmb.showinfo("Deleted", "Selected item was deleted")
        print(item_values[0])
        table.delete(selected_item)
        cur = conn.cursor()
        cur.execute("DELETE FROM cars WHERE id = %s", (item_values[0]))
        conn.commit()
        cur.close()
    else:
        tkmb.showwarning("No selection", "Please select an item to delete.")





button_delete = tk.Button(app, text="delete", command=delete_selected_item)
button_delete.pack(side=tk.LEFT, padx=20)

button_delete = tk.Button(app, text="refresh", command=insert_data_from_csv)
button_delete.pack(side=tk.LEFT)

button_open = tk.Button(app, text='Open next window', background='#98FB98', width=25, font=('Helvetica', 10), command= open_new_window)
button_open.pack(side=tk.RIGHT, padx=20)






app.mainloop()




