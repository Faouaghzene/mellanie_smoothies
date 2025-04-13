
# Import python packages
import streamlit as st
import pandas as pd
import requests 
from snowflake.snowpark.functions import col 


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
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe,use_container_width=True)
#st.stop
pd_df = my_dataframe.to_pandas ()
#st.dataframe (pd_df)
#st.stop
ingredients_list = st.multiselect ('Choose top 5 fruit',my_dataframe,max_selections=5)
#st.write(ingredients_list)
if ingredients_list :
    
    ingredients_string=''
    for choose_fruit in ingredients_list :
        ingredients_string += choose_fruit +' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == choose_fruit, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', choose_fruit,' is ', search_on, '.')
        st.subheader (choose_fruit  +' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit"+search_on )
        sd = st.dataframe (fruityvice_response.json(),use_container_width=True)
        
        #st.write (ingredients_string)
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" +ingredients_string + """','""" +name_on_order + """')"""

        #st.write(my_insert_stmt)
        time_to_insert = st.button ("Submit Order")
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
 





