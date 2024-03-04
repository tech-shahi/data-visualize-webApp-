import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Establish connection to SQLite database
conn = sqlite3.connect('feedback.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS feedback (
                Name TEXT,
                Email TEXT,
                Message TEXT
            )''')

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
        font-family: Arial, sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #4CAF50;
    }
    .sidebar .sidebar-content .block-container {
        color: white;
    }
    .sidebar .sidebar-content .block-container a {
        color: white;
    }
    .sidebar .sidebar-content .block-container a:hover {
        color: #f0f0f0;
    }
    .main .block-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
    }
    .footer {
        padding: 20px;
        text-align: center;
        color: #808080;
        background-color: #f0f0f0;
        border-top: 1px solid #ddd;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

working_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the folder where your CSV files are located
folder_path = f"{working_dir}/data"  # Update this to your folder path

# Function to load CSV data
@st.cache(allow_output_mutation=True)
def load_data(file):
    file_path = os.path.join(folder_path, file.name)
    df = pd.read_csv(file_path)
    return df

# Function to save feedback data to SQLite database
def save_feedback_to_db(name, email, message):
    c.execute("INSERT INTO feedback (Name, Email, Message) VALUES (?, ?, ?)", (name, email, message))
    conn.commit()

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
        df = load_data(uploaded_file)

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
        save_feedback_to_db(name, email, message)
        st.success('Thank you for your message! We will get back to you shortly.')

# Footer
st.markdown(
    """
    <div class="footer">
        © Copyrights - CreativeShahi 2024
    </div>
    """,
    unsafe_allow_html=True
)

# Close the SQLite database connection
conn.close()
