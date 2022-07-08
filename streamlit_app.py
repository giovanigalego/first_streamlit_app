import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("my parents new healthy dinner")

streamlit.header("Breakfast Favorites")
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)


def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")    

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        streamlit.write('Please select to get information.')
    else:
        back_from_funtion = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_funtion)
except URLErrors as e:
    streamlit.error()

streamlit.header("Fruit list contais")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()
        
if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)




def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute('insert into fruit_load_list values'+ new_fruit)
        return "thanks for adding"+ new_fruit

streamlit.stop()

add_my_fruit = streamlit.text_input('What fruit would like to add?')        
if streamlit.button('Add a fruit to the tlist'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_frunction = insert_row_snowflake
    streamlit.text(back_from_funtion)


fruit_add = streamlit.text_input('What fruit would you like to add?','Kiwi')
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_add)

streamlit.write('The user entered add ', fruit_add)

my_cur.execute("insert into fruit_load_list values('from streamlit')")
