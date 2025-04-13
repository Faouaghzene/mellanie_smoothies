# Import python packages
import streamlit as st

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
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)
