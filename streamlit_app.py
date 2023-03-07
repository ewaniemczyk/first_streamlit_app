import streamlit
import pandas

streamlit.title('My Parents New Healthy Dinner')
streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach, Rocket Smoothie')
streamlit.text('🐔 Hard Boild Free Range Eggs')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# changing dataframe index from first column with numbers into names of fruits.
my_fruit_list=my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruit_selected=streamlit.multiselect ("Pick your fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruit_to_show=my_fruit_list.loc[fruit_selected]

# Display the list
streamlit.dataframe(fruit_to_show)

#New Section to display Fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")

import requests
fruityvice_response=requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response.json())  ## function json() had to be added to remove error 200 -- it desplay now json

#take the json text and normalize it
fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
#output it screen as table
streamlit.dataframe(fruityvice_normalized)

#New Section to display Fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice=streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered', fruit_choice)
fruityvice_response=requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

streamlit.stop()

import snowflake.connector
my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur=my_cnx.cursor()
my_cur.execute("select current_user(), current_account(), current_region()")
my_data_row=my_cur.fetchone()
streamlit.text("Hello from Snowflake: " )
streamlit.text(my_data_row)

my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_row=my_cur.fetchall()
streamlit.text("the fruit load list contains: ")
streamlit.text(my_data_row)

streamlit.header("the fruit load list contains: ")
streamlit.dataframe(my_data_row)

#allow the user to add a fruit
add_my_fruit=streamlit.text_input('What fruit would You like to add?')
streamlit.write('Thanks for adding',add_my_fruit)

#INSERT NEW ROWS INTO SF
my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values('from streamlit')")
#
