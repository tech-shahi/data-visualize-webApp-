import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Print current directory for debugging
print("Current directory:", os.getcwd())

# Connect to SQLite database
db_file_path = 'feedback.db'  # Adjust the file path if necessary
print("Database file path:", db_file_path)
conn = sqlite3.connect(db_file_path)
c = conn.cursor()

# Create feedback table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS feedback
             (Name TEXT, Email TEXT, Message TEXT)''')
conn.commit()

# Function to save feedback data to SQLite database
def save_feedback_to_database(name, email, message):
    c.execute("INSERT INTO feedback (Name, Email, Message) VALUES (?, ?, ?)", (name, email, message))
    conn.commit()

# Function to retrieve feedback data from SQLite database
def get_feedback_data():
    c.execute("SELECT * FROM feedback")
    return c.fetchall()

working_dir = os.path.dirname(os.path.abspath(__file__))

# Custom sidebar
st.sidebar.title('Menu')
st.sidebar.markdown('---')
selected_menu = st.sidebar.radio('', ('📊 Data Visualizer', '🔍 About Us', '✉️ Contact Us'))

# Title with icon and tagline
st.title('📊 Data Visualizer')
st.markdown("*Empowering Data Insights*")

# Title
if selected_menu == '📊 Data Visualizer':
    # File uploader for CSV files
    uploaded_file = st.file_uploader("Drag and drop a CSV file here, or browse to upload", type="csv")

    if uploaded_file is not None:
        # Load the CSV data
        df = pd.read_csv(uploaded_file)

        col1, col2 = st.columns(2)

        columns = df.columns.tolist()

        with col1:
            st.write("")
            st.write(df.head())

        with col2:
            # Allow the user to select columns for plotting
            x_axis = st.selectbox('Select the X-axis', options=columns+["None"])
            y_axis = st.selectbox('Select the Y-axis', options=columns+["None"])

            plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
            # Allow the user to select the type of plot
            plot_type = st.selectbox('Select the type of plot', options=plot_list)

        # Generate the plot based on user selection
        if st.button('Generate Plot'):
            with st.spinner('Generating Plot...'):
                fig, ax = plt.subplots(figsize=(6, 4))

                if plot_type == 'Line Plot':
                    plt.plot(df[x_axis], df[y_axis])
                elif plot_type == 'Bar Chart':
                    sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
                elif plot_type == 'Scatter Plot':
                    plt.scatter(df[x_axis], df[y_axis])  # Use plt.scatter for scatter plot
                elif plot_type == 'Distribution Plot':
                    ax.hist(df[x_axis], bins=20, alpha=0.7, color='blue')  # Create a histogram
                    ax.set_xlabel(x_axis)
                    ax.set_ylabel(y_axis)
                    ax.set_title(f'Distribution Plot of {x_axis}')
                elif plot_type == 'Count Plot':
                    sns.countplot(x=df[x_axis], ax=ax)
                    y_axis = 'Count'

                # Adjust label sizes
                ax.tick_params(axis='x', labelsize=10)  # Adjust x-axis label size
                ax.tick_params(axis='y', labelsize=10)  # Adjust y-axis label size

                # Show the results
                st.pyplot(fig)

# About Us section
elif selected_menu == '🔍 About Us':
    st.title('About Us')
    st.write("Welcome to Data Visualizer, your go-to tool for exploring and visualizing data.")
    st.subheader('Our Mission')
    st.write("Our mission is to empower individuals and organizations to derive meaningful insights from their data.")
    st.subheader('Inspiration')
    st.write("Data Visualizer was inspired by the need for a user-friendly platform to visualize data effortlessly.")

# Contact Us section
elif selected_menu == '✉️ Contact Us':
    st.title('Contact Us')
    st.write("Have questions or feedback? Fill out the form below to get in touch.")
    name = st.text_input('Your Name')
    email = st.text_input('Your Email')
    message = st.text_area('Message')
    if st.button('Submit'):
        # Process the form submission
        save_feedback_to_database(name, email, message)
        st.success('Thank you for your message! We will get back to you shortly.')
