import re
import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from src.scrapper import service_run
from src.sender import find_sidebar, send_message
from src.utils import message, read_csv

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Temperature Converter')
        self.geometry('500x500')
        self.resizable(False, False)
        
        
class CsvConverter:
    @staticmethod
    def read_csv_from(f, format=True):
        print("Reading file %s" % f)
        global df
        df = read_csv(f)
        
        if format:
            return f'You have the following columns\n\t{list(df.columns)}'
        return list(df.columns)
    
    
class CsvFrame(ttk.Frame):
    def __init__(self, container, reader):
        super().__init__(container)

        self.reader = reader
        options = {'padx': 5, 'pady': 0}

        self.csv_label = ttk.Label(self, text="CSV file")
        self.csv_label.grid(column=0, row=0, sticky='w',  **options)
        
        self.csv_frame = tk.Frame(self)
        self.csv_frame.grid(column=1, row=0, columnspan=2, sticky='w', **options)
        self.csv = tk.Text(self.csv_frame, height=1, width=40) # height=20, width=20)
        self.csv.pack()

        self.convert_button = ttk.Button(self, text='Load')
        self.convert_button.grid(column=3, row=0, sticky='w', **options)
        self.convert_button.configure(command=self.read_csv)

        self.result_label = ttk.Label(self)
        self.result_label.grid(row=1, columnspan=3, **options)

        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    def read_csv(self, event=None):
        """  Handle button click event
        """
        try:
            global input_value
            input_value = self.csv.get(1.0, "end-1c")
            result = self.reader(input_value)
            self.result_label.config(text=result)
        except FileNotFoundError as error:
            self.reset()
            self.result_label.config(text='')
            showerror(title='Error', message=error)
        except ValueError as error:
            self.reset()
            self.result_label.config(text='')
            showerror(title='Error', message=error)

    def reset(self):
        self.csv.delete('1.0', 'end')
        self.result_label.text = ''
        
        
class ControlFrame(ttk.LabelFrame):
    def __init__(self, container):

        super().__init__(container)
        self['text'] = 'Message'
        options = {'padx': 5, 'pady': 0}
        self.df = None
        self.wsp = "https://web.whatsapp.com"
        
        self.message_frame = tk.Frame(self)
        self.message_frame.grid(column=0, row=0, columnspan=8, sticky='w', **options)
        self.message = tk.Text(self.message_frame, height=20, width=55)
        self.message.pack()
        
        # button
        self.convert_button = ttk.Button(self, text='Preview')
        self.convert_button.grid(column=0, row=1, sticky='w', **options)
        self.convert_button.configure(command=self.preview_message)
        
        # button
        self.convert_button = ttk.Button(self, text='Send')
        self.convert_button.grid(column=1, row=1, sticky='w', **options)
        self.convert_button.configure(command=self.send_message)

        self.grid(column=0, row=1, padx=5, pady=5, sticky='ew')

        self.frame = CsvFrame(
            container,
            CsvConverter.read_csv_from
        )

        
    def preview_message(self):
        if 'df' not in globals():
            showerror("Send Message", "Please, load the CSV file first")
            return

        self.df = df
        self.template = self.message.get(1.0, "end-1c")
        if self.template == '':
            showerror("Send Message", "The message is empty")
            return
          
        line = message(self.df.iloc[0], self.template, url=False)
        showinfo("Preview", line)
        
    def send_message(self):
        if self.df is None:
            showerror("Send Message", "Please, preview the message first")
            return
        
        if not self.template == self.message.get(1.0, "end-1c"):
            showerror("Send Message", "The message has changed!")
            return
          
        self.driver = service_run(os.getcwd())
        self.driver.get(self.wsp)
        find_sidebar(self.driver)
        logs = 0
        self.df['sent'] = 0
          
        for i, row in df.iterrows():
            line = message(row, self.template)
            link = f"{self.wsp}/send?phone=51{row.celular}&text={line}&source&data"
            flag = send_message(self.driver, link, row.celular)
            if flag:
                logs += 1
                self.df.loc[i, 'sent'] = 1

        self.driver.quit()
        self.output_path = re.search(r'(.*)\.csv', input_value).group(1)
        self.output_path = self.output_path + '_output.csv'
        self.df.to_csv(self.output_path, sep=',', index=False)
        showinfo("Results", f"Total sent: {logs}\nTotal skept: {len(df)-logs}\nTotal: {len(df)}")
        

    def change_frame(self):
        frame = self.frames[self.selected_value.get()]
        frame.reset()
        frame.tkraise()
        
if __name__ == '__main__':
    app = App()
    ControlFrame(app)
    app.mainloop()