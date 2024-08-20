mport os
import streamlit as st
import anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("Claude_api_key")

# Initialize the Anthropic client with the API key
client = anthropic.Anthropic(api_key=api_key)

# Define the functions to generate content
def generate_game_environment(environment_description):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=150,
        temperature=0.7,
        system="You are an expert in world-building. Generate a detailed description of a game environment based on the input.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Create a detailed description of a game environment based on this input: {environment_description}"
                    }
                ]
            }
        ]
    )
    return message.content[0].text

def generate_protagonist(protagonist_description):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=150,
        temperature=0.7,
        system="You are an expert in character creation. Generate a detailed description of a game protagonist based on the input.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Create a detailed description of a game protagonist based on this input: {protagonist_description}"
                    }
                ]
            }
        ]
    )
    return message.content[0].text

def generate_antagonist(antagonist_description):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=150,
        temperature=0.7,
        system="You are an expert in villain creation. Generate a detailed description of a game antagonist based on the input.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Create a detailed description of a game antagonist based on this input: {antagonist_description}"
                    }
                ]
            }
        ]
    )
    return message.content[0].text

def generate_game_story(environment, protagonist, antagonist):
    story_prompt = (f"Create a detailed game story based on the following inputs:\n"
                    f"Game Environment: {environment}\n"
                    f"Protagonist: {protagonist}\n"
                    f"Antagonist: {antagonist}")
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=150,
        temperature=0.7,
        system="You are a master storyteller. Generate a detailed game story based on the inputs provided.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": story_prompt
                    }
                ]
            }
        ]
    )
    return message.content[0].text

# App Title
st.title("🎮 Safwan's GameMaker Studio")

# App Description
st.write("Welcome to Safwan's GameMaker Studio, a popular game development platform known for its ease of use and powerful features. Enter your ideas according to your taste and this will generate a script with a real scenario. Generate more ideas to compete with the big communities.")

# Sidebar Inputs
with st.sidebar:
    st.header("📝 Game Details")
    game_environment = st.text_input("🏞️ Game Environment", "Describe the setting of your game")
    protagonist = st.text_input("🦸‍♂️ Protagonist", "Describe the main character")
    antagonist = st.text_input("🦹‍♀️ Antagonist", "Describe the main villain or opposing force")
    if st.button("Generate Document"):
        # Generate content based on user input
        env_description = generate_game_environment(game_environment)
        protagonist_description = generate_protagonist(protagonist)
        antagonist_description = generate_antagonist(antagonist)
        game_story = generate_game_story(game_environment, protagonist, antagonist)
        
        # Store results in session state
        st.session_state.env_description = env_description
        st.session_state.protagonist_description = protagonist_description
        st.session_state.antagonist_description = antagonist_description
        st.session_state.game_story = game_story

# Layout with three columns
col1, col2, col3 = st.columns(3)

with col1:
    st.header("🌍 Game Environment")
    if 'env_description' in st.session_state:
        st.write(st.session_state.env_description)
    else:
        st.write(game_environment)
    st.markdown("---")

with col2:
    st.header("🦸‍♂️Protagonist")
    if 'protagonist_description' in st.session_state:
        st.write(st.session_state.protagonist_description)
        if st.button("Edit Protagonist Details", key="edit_protagonist"):
            new_protagonist_description = st.text_area("Edit Protagonist Description", st.session_state.protagonist_description)
            if st.button("Update Protagonist", key="update_protagonist"):
                st.session_state.protagonist_description = generate_protagonist(new_protagonist_description)
                st.experimental_rerun()
    else:
        st.write(protagonist)
    st.markdown("---")

with col3:
    st.header("🦹‍♀️ Antagonist")
    if 'antagonist_description' in st.session_state:
        st.write(st.session_state.antagonist_description)
        if st.button("Edit Antagonist Details", key="edit_antagonist"):
            new_antagonist_description = st.text_area("Edit Antagonist Description", st.session_state.antagonist_description)
            if st.button("Update Antagonist", key="update_antagonist"):
                st.session_state.antagonist_description = generate_antagonist(new_antagonist_description)
                st.experimental_rerun()
    else:
        st.write(antagonist)
    st.markdown("---")

# Combine and merge sections to generate a scenario and script
if 'env_description' in st.session_state and 'protagonist_description' in st.session_state and 'antagonist_description' in st.session_state:
    combined_content = (f"### Game Scenario\n\n"
                        f"**Environment:** {st.session_state.env_description}\n\n"
                        f"**Protagonist:** {st.session_state.protagonist_description}\n\n"
                        f"**Antagonist:** {st.session_state.antagonist_description}\n\n"
                        f"**Story:** {st.session_state.game_story}")
else:
    combined_content = "Your complete game scenario and script will be generated based on the inputs provided."

st.header("📜 Game Scenario & Script")
st.write(combined_content)
