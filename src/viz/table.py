import pandas as pd
import inspect
import os

def generate_table(df: pd.DataFrame):
    with open(f'{os.path.dirname(os.path.realpath(__file__))}/table.css', 'r') as file:
        css = file.read().replace('\n', '')

    dir = os.path.dirname(os.path.abspath((inspect.stack()[1])[1]))

    text_file = open(f"{dir}/index.html", "w")
    text_file.write(f'<style>{css}</style>')
    text_file.write(df.to_html())
    text_file.close()