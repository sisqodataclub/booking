import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu


st.title("TERMS AND CONDITIONS")
import datetime

def shift_preferences():
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    shift_options = ['weekly', 'every 2 weeks', 'every 3 weeks', 'every 4 weeks']

    preferences_list = []

    selected_days = st.multiselect("Select Days you need your property cleaning", days)

    # Create lists to store data for each field
    day_list = []
    start_time_list = []
    end_time_list = []
    shift_prefs_list = []

    # Loop through each day of the week
    for day in selected_days:
        st.write(f"### {day}")

        # Create two columns to display the start and end time inputs side by side
        start_col, end_col = st.columns(2)

        # Add the start time input to the first column
        start_time = start_col.time_input(f'Start time for {day}:', value=datetime.time(hour=9, minute=0))
        start_time_list.append(start_time)

        # Add the end time input to the second column
        end_time = end_col.time_input(f'End time for {day}:', value=datetime.time(hour=17, minute=0))
        end_time_list.append(end_time)

        # Add a multiselect to choose the preferred shift(s) for the day
        shift_prefs = start_col.selectbox(f"Select preferred shift(s) for {day}:", shift_options)
        shift_prefs_list.append(shift_prefs)

        # Append the day to the day list
        day_list.append(day)

    # Create a DataFrame using the collected data
    preferences_df = pd.DataFrame({
        'Day': day_list,
        'Start Time': start_time_list,
        'End Time': end_time_list,
        'Shift Preferences': shift_prefs_list
    })

    return preferences_df

# Call the function to get the DataFrame
#preferences_df = shift_preferences()

# Call the function to get the preferences
#st.write(preferences_df)



selected3 = option_menu(None, ["ONE-OFF CLEANING", "REGULAR CLEANING",  "CARPET CLEANING ONLY"], 
        icons=['house', 'cloud-upload', "list-task"], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "15px"}, 
            "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "green"},
        }
    )




if selected3 == "REGULAR CLEANING":
    st.write('hi')
else:
    


    import streamlit as st

    # Define CSS styles for the fixed button
    button_style = """
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
        background-color: #FF5733;
        color: white;
        border: none;
        padding: 10px 20px;
        cursor: pointer;
        border-radius: 5px;
    """

    st.title("Fixed Button Example")

    # Display content
    st.write("This is the main content of your app.")

    # Display the fixed button using HTML and CSS
    st.write(
        f"""
        <button id="fixedButton" style='{button_style}'>Fixed Button</button>
        <script>
            document.getElementById('fixedButton').addEventListener('click', function() {{
                Streamlit.run("st.write('It\\\\'s working')")
            }});
        </script>
        """,
        unsafe_allow_html=True,
    )


    # Navigation menu
    # Navigation menu
    st.markdown(
        """
        <div style="
            display: flex;
            justify-content: space-around;
            align-items: center;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 60px;
            background-color: #333;
            font-size: 18px;
        ">
            <div style="color: white;">Option 1</div>
            <div style="color: white;">Option 2</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write('---')

    def popup_message(message):
        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: center;
                align-items: center;
                position: fixed;
                top: 8%;
                left: 200px; /* Adjust this value to position the pop-up message next to the sidebar */
                transform: translate(0, -50%);
                padding: 20px;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                z-index: 1000;
            ">
                {message}
            </div>
            """,
            unsafe_allow_html=True,
        )


    def popup_message10(button_label):
        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: center;
                align-items: center;
                position: fixed;
                top: 8%;
                left: 200px; /* Adjust this value to position the pop-up message next to the sidebar */
                transform: translate(0, -50%);
                padding: 20px;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                z-index: 1000;
            ">
                <div style="display: flex; align-items: center;">
                    <span style="margin-right: 10px;">{button_label}</span>
                    <span style="flex: 1;"><button style="width: 100%;">Click Me</button></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    # Your main content here
    st.title("Streamlit Sidebar Arrow with Text")
    st.write("This is the main content of your app.")


