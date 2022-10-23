import streamlit as st

# Initialization, two ways to access state
st.title('Initialization')
if 'location' not in st.session_state:
    st.session_state['location'] = 'China'

if 'price' not in st.session_state:
    st.session_state.price = 34

# Read state
st.title('Read State')
st.write(st.session_state)
st.write("Keys:")
for key in st.session_state.keys():
        st.write(key)

st.write("Values:")
for value in st.session_state.values():
        st.write(value)

st.write("Items:")
for item in st.session_state.items():
        st.write(item)

st.write(st.session_state.location)
st.write(st.session_state.price)

# Update state
st.title('Update State')
st.session_state['location'] = "Shanghai"
st.session_state.price = 100
st.write(st.session_state)

# Delete state
st.title('Delete State')
for key in st.session_state.keys():
        del st.session_state[key]
st.write(st.session_state)

# Widget with key will added to session state
st.title('Widget')
st.text_input("Your name", key="name")
st.write(st.session_state.name)

# Callback is called at first, then rerun all script
st.title('Callback')
def form_callback():
    st.write(st.session_state.my_slider)
    st.write(st.session_state.my_checkbox)

with st.form(key='my_form'):
    slider_input = st.slider('My slider', 0, 10, 5, key='my_slider')
    checkbox_input = st.checkbox('Yes or No', key='my_checkbox')
    submit_button = st.form_submit_button(label='Submit', on_click=form_callback)
st.write(st.session_state)