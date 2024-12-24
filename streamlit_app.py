import streamlit as st
import pandas as pd

# Set up page configuration
st.set_page_config(page_title="Team Projects Showcase", layout="wide")

# Add title
st.title("Team Projects Showcase")

# # Define project data using the provided format
# projects = [
#     {
#         "name": "💸 MoneyMentor",
#         "presentation": "https://moneymentor.streamlit.app/",
#         "app_link": "https://moneymentor.streamlit.app/",
#         "repo_link": "https://github.com/samkamau81/FinGPT_",
#         "short_description": "MoneyMentor is a project about money management and financial advice. MoneyMentor is a project about money management and financial advice. MoneyMentor is a project about money management and financial advice.",
#         "topic_tags": '["LangChain"]',
#         "tools": '["natural language processing", "computer vision"]',
#         "cohort_tag": "fall_2024",
#         "image": "https://via.placeholder.com/150?text=MoneyMentor",  # Placeholder image, replace with actual
#         "students": {
#             "Sam Kamau": "https://via.placeholder.com/150?text=Sam+Kamau",
#             "Alice Johnson": "https://via.placeholder.com/150?text=Alice+Johnson"
#         }
#     },
#     {
#         "name": "Adaptive Exercise Generator",
#         "presentation": "https://genai-exercise-generator-deza4qcucy8a9k4dzcwf9b.streamlit.app/",
#         "app_link": "https://genai-exercise-generator-deza4qcucy8a9k4dzcwf9b.streamlit.app/",
#         "repo_link": "https://github.com/sayyidka/genai-exercise-generator",
#         "short_description": "An AI-powered tool to generate personalized exercise routines.",
#         "topic_tags": '["LangChain"]',
#         "tools": '["AI", "machine learning", "fitness"]',
#         "cohort_tag": "fall_2024",
#         "image": "https://via.placeholder.com/150?text=Exercise+Generator",  # Placeholder image, replace with actual
#         "students": {
#             "Sayyid K": "https://via.placeholder.com/150?text=Sayyid+K",
#             "Jordan Lee": "https://via.placeholder.com/150?text=Jordan+Lee"
#         }
#     }
# ]

# Load the CSV data into a DataFrame
df = pd.read_csv("Project_Spreadsheet.csv")

# Convert the DataFrame to a list of dictionaries for easy access
projects = []
for _, row in df.iterrows():
    project = {
        "name": row["Project Name"],
        "presentation": row["Presentation Link"],
        "app_link": row["App Link"],
        "repo_link": row["Repo Link"],
        "short_description": row["Short Description"],
        "topic_tags": [tag.strip() for tag in row["Topic Tags"].split(',')],  # Convert string representation of list to actual list
        "tools": [tool.strip() for tool in row["Tools"].split(',')],  # Convert string representation of list to actual list
        "cohort_tag": row["Cohort Tag"],
        "image": row["Image URL"],
        "students": {}
    }

    # Parse the students and their links
    students = row["Students"].split(", ")
    for student in students:
        name, link = student.split(": ")
        project["students"][name] = link

    projects.append(project)

# print(projects)

# Create an expander panel for filtering options
with st.expander("Filter Projects"):
    # Create a multi-select dropdown for selecting multiple cohorts
    cohorts = list(set([project["cohort_tag"] for project in projects]))
    selected_cohorts = st.multiselect("Select Cohort(s)", cohorts, default=cohorts)

    # Create a multi-select dropdown for selecting multiple topics
    topics = list(set([tag for project in projects for tag in project["topic_tags"]]))
    selected_topics = st.multiselect("Select Topic(s)", topics, default=topics)

    # Create a multi-select dropdown for selecting multiple tools
    tools = list(set([tool for project in projects for tool in project["tools"]]))
    selected_tools = st.multiselect("Select Tool(s)", tools, default=tools)

# Filter the projects based on the selected cohorts, topics, and tools
filtered_projects = [
    project for project in projects
    if project["cohort_tag"] in selected_cohorts and
       any(tag in selected_topics for tag in project["topic_tags"]) and
       any(tool in selected_tools for tool in project["tools"])
]


# Create a grid layout to display the filtered projects
cols = st.columns(2)

# Loop through filtered projects and display in grid
for idx, project in enumerate(filtered_projects):
    col = cols[idx % 2]  # This ensures the layout wraps every 3 columns
    
    with col:
        # Display project thumbnail
        st.image(project["image"], width=150)
        
        # Project name
        st.subheader(project["name"])
        
        # Create a single row for the emojis with links
        st.markdown(
            f'''
            <div style="display: flex; justify-content: flex-start; gap: 10px;">
                <a href="{project["presentation"]}" target="_blank" style="font-size: 20px; text-decoration: none;">💡</a>
                <a href="{project["app_link"]}" target="_blank" style="font-size: 20px; text-decoration: none;">🔗</a>
                <a href="{project["repo_link"]}" target="_blank" style="font-size: 20px; text-decoration: none;">⚙️</a>
            </div>
            ''', unsafe_allow_html=True)
        
        # Short description
        st.write(project["short_description"])
        
        # Tags and tools as tiles
        tags = project['topic_tags']  # Convert string to list
        tools = project['tools']  # Convert string to list
        
        # Display tags as tiles
        # st.write("**Topic Tags**:")

        # Use Flexbox to display emojis in a row
        st.markdown(
            f'''
            <div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: flex-start;">
                {"".join([f'<span style="padding: 5px; background-color: #007bff; color: white; border-radius: 5px;">{tag}</span>' for tag in tags])}
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('')
        # Use Flexbox to display emojis in a row
        st.markdown(
            f'''
            <div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: flex-start;">
                {"".join([f'<span style="padding: 5px; background-color: #28a745; color: white; border-radius: 5px;">{tool}</span>' for tool in tools])}
            </div>
            ''', unsafe_allow_html=True)

        # Display students and their images in a row
        # st.write("**Students**:")
        st.write("")
        # Display students and their images with LinkedIn URL
        st.markdown(
            f'''
            <div style="display: flex; flex-wrap: wrap; gap: 15px; justify-content: flex-start;">
                {"".join([f'<div style="text-align: center; font-size: 14px;"><a href="{image_url}" target="_blank"><img src="gender-neutral-user.png" alt="{student}" style="width: 100px; border-radius: 50%;"></a><br><a href="{image_url}" target="_blank">{student}</a></div>' for student, image_url in project["students"].items()])}
            </div>
            ''', unsafe_allow_html=True)


        
        
        # # Display students and their images
        # st.write("**Students**:")
        # for student, image_url in project["students"].items():
        #     st.markdown(f"[{student}]({image_url})")

        st.write("---")

# # Optional footer
# st.markdown("""
# ## Contact Us
# For more information or inquiries, feel free to reach out to us at [team@example.com](mailto:team@example.com).
# """)
