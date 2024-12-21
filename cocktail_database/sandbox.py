import streamlit as st

list_of_tables = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']

# Add CSS styles for the containers
container_style = """
    <style>
        .container1 {
            border: 2px solid #3498db;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 20px;
        }
        .container2 {
            /* Add styles for Container 2 if needed */
        }
    </style>
"""

# Display the CSS styles
st.markdown(container_style, unsafe_allow_html=True)

# Use the styled containers
with st.container() as container1:
    container1.markdown("<div class='container1'>", unsafe_allow_html=True)
    st.write("In Container 1")
    table_name = st.radio("Please Select Table", list_of_tables)
    container1.markdown("</div>", unsafe_allow_html=True)

with st.container() as container2:
    container2.markdown("<div class='container2'>", unsafe_allow_html=True)
    st.write("In Container 2")
    container2.markdown("</div>", unsafe_allow_html=True)
