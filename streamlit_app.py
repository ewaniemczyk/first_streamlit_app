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
import requests
fruityvice_response=requests.get_response("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response)
