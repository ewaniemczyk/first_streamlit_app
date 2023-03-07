import streamlit #to run the code in streamlit
import pandas #to work on dataframes
import requests  #to send and get back requests-responses from streamlit
import snowflake.connector # to select/modify snowflake data

from  urllib.error import URLError # to control the flow

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


fruityvice_response=requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response.json())  ## function json() had to be added to remove error 200 -- it desplay now json

#take the json text and normalize it
fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
#output it screen as table
streamlit.dataframe(fruityvice_normalized)

#CREATE FUNCTION

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response=requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

#New Section to display Fruityvice API response
streamlit.header("View our fruit list! Add Your favourites!")
try:
  fruit_choice=streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please choose the fruit to get information')
  else:
    streamlit.write('The user entered', fruit_choice)
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
  streamlit.error()
  
 #first version of snowflake data  

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

#SECOND SNOWFLAKE VERSION WITH FUNCTION
streamlit.text("the fruit load list contains: ")

def get_fruit_load_list():
  with cnx.cursor() as my_cur:
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    cnx.close()
    return my_cur.fetchall()

#Add button  to load the fruit  - I had to commented as later the same button 'get fruit load list' is on the end
if streamlit.button('Get fruit list'):
  cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data=get_fruit_load_list()
  cnx.close()
  streamlit.dataframe(my_data)

#function to load snowflake
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values('" + new_fruit + "')")
    return ('thank You for adding'+new_fruit)
    
# Add button  to load the fruit into snowflake
add_my_fruit=streamlit.text_input('What fruit would You like to add')
if streamlit.button('Add a fruit to the list'):
  cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.text(insert_row_snowflake(add_my_fruit))
  cnx.close()
  streamlit.dataframe(get_fruit_load_list())
  
