# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)

session = get_active_session()
my_dataframe = (session.table("smoothies.public.fruit_options")
                .select(col('FRUIT_NAME')))
# st.dataframe(data=my_dataframe, use_container_width=True)

incredient_list = st.multiselect('Choose upto 5 ingredients:'
                                 , my_dataframe)

if incredient_list:
    # st.write(incredient_list)
    # st.text(incredient_list)
    
    incredient_string = ''
    for fruite_choosen in incredient_list:
        incredient_string += fruite_choosen + ' '

    # st.write(incredient_string)
    
    my_insert_stmt = f"""insert into smoothies.public.orders(ingredients)
                         values('{incredient_string}')"""
    
    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        