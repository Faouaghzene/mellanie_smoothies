
# Import python packages
import streamlit as st
import requests 
from snowflake.snowpark.functions import col 

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# Write directly to the app
st.title(":cup_with_straw: Example Streamlit App :cup_with_straw:")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)
name_on_order =st.text_input ("Name on smoothie :")
st.write ('yous smoothie  is :',name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'))
st.dataframe(data=my_dataframe,use_container_width=True)


ingredients_list = st.multiselect ('Choose top 5 fruit',my_dataframe,max_selections=5)
#st.write(ingredients_list)
if ingredients_list :
    
    ingredients_string=''
    for choose_fruit in ingredients_list :
        ingredients_string += choose_fruit +' '

        #st.write (ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" +ingredients_string + """','""" +name_on_order + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button ("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

#st.write(smoothiefroot_response.json(),use_container_width=True)

sd = st.dataframe (smoothiefroot_response.json(),use_container_width=True)



