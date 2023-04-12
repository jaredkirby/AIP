import streamlit as st
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.llms import OpenAI
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate

st.set_page_config(
    page_icon=":camera:",
    layout="centered",
)

st.title("Additive Prompt Generator for Midjourney")
st.markdown(
    "#### This app will generate copy & paste prompt variations for Midjourney.")

col1, col2, col3 = st.sidebar.columns([1, 1, 2])
col1.image("https://em-content.zobj.net/thumbs/240/google/350/plus_2795.png",
           width=75)
col2.image("https://em-content.zobj.net/thumbs/240/google/350/camera-with-flash_1f4f8.png",
           width=75)
col3.write("")
with st.sidebar.expander("How this app works"):
    st.markdown('''
        - Each of the input fields will be used as a variable in the first LLM call prompt.
        - The prompt will be used to generate a table that breaks down the image into its elements.
        - The table will be filled with the user specified number of rows of data with variations created by LLM.
        - The table output from the first LLM call will be used as a variable input for the second LLM call prompt.
        - The second call will generate a comma-separated summary sentence for each row of the table. 
        - The sentences will be prepended with {framework} and appended with —ar {aspect_ratio}. 
        - The sentences will be formatted as a bulleted markdown list and displayed for the user.
        '''
                )

API_O = st.sidebar.text_input(":blue[Enter Your OPENAI API-KEY :]",
                              placeholder="Paste your OpenAI API key here (sk-...)", type="password")


# Define the prompt template with multiple input variables
table_template = """
Please create a table that breaks down a {framework} composition into the following key elements, where each of these key elements is a column: Composition, Camera Angle, Style, Room Type, Focal Point, Textures, Detail, Color Palette, Brand, Lighting, Location, Time of Day, Mood, Architecture.
Fill the table with {row_numbers} rows of data where:
composition = {composition}
camera_angle = {camera_angle}
style = {style}
room_type = {room_type}
focal_point = {focal_point}
textures = {textures}
detail = {detail}
color_palette = {color_palette}
brand = {brand}
lighting = {lighting}
location = {location}
time_of_day = {time_of_day}
mood = {mood}
architecture = {architecture}
"""
# 5 rows of data for a {framework} that is {adjective} and 5 rows of data for a {framework} that is {adjective}.
table_prompt = PromptTemplate(template=table_template, input_variables=["framework", "composition", "camera_angle", "style", "room_type",
                                                                        "focal_point", "textures", "detail", "color_palette", "brand", "lighting", "location", "time_of_day", "mood", "architecture", "row_numbers"])

line_template = """
Please write a comma-separated summary sentence for each row of the following table.
{table}
Prepend each sentence with {framework} and append each sentence with " —ar {aspect_ratio}".
Format: Bulleted markdown list with the title of "Suggested Prompts for Midjourney".
"""
line_prompt = PromptTemplate(template=line_template, input_variables=[
                             "table", "framework", "aspect_ratio"])

# Initialize the LLMs
if API_O:
    llm_7 = OpenAI(temperature=0.7,
                   openai_api_key=API_O, max_tokens=1000)
    llm_0 = OpenAI(temperature=0.0,
                   openai_api_key=API_O, max_tokens=1000)
    # Initialize LLMChain with the prompt and LLM
    table_chain = LLMChain(prompt=table_prompt, llm=llm_7,
                           output_key="table", verbose=True)
    line_chain = LLMChain(prompt=line_prompt, llm=llm_7,
                          output_key="lines", verbose=True)
    print(table_chain)
    print(line_chain)
    seq_chain = SequentialChain(
        chains=[table_chain, line_chain],
        input_variables=["framework", "composition", "camera_angle", "style", "room_type", "focal_point", "textures",
                         "detail", "color_palette", "brand", "lighting", "location", "time_of_day", "mood", "architecture", "aspect_ratio", "row_numbers"],
        output_variables=["lines"],
        verbose=True,
    )
else:
    st.markdown('''
    ```  
    Start Here: 
        - 1. Enter your OpenAI API key to use this app 🔐
        - 2. Select a suggestion or add a custom suggestion 📝 
        - 3. Select the number of prompt variations to generate 🔢
        - 4. Click the "Generate Prompts" button to generate prompts 🚀
    ''')
    st.sidebar.warning(
        'API key is required to try this app. The API key is not stored.')

# Create two columns
col1, col2 = st.columns(2)

# Add input fields to the columns
framework_options = ["Interior architecture photograph", "Landscape photograph",
                     "Street photography", "Macro photography", "Portrait photograph", "Custom"]
framework = col1.selectbox("Framework", framework_options, index=0)
if framework == "Custom":
    framework = col1.text_input("Enter custom framework")

composition_options = ["Rule of thirds", "Symmetrical",
                       "Diagonal lines", "Leading lines", "Frame within a frame", "Custom"]
composition = col1.selectbox("Composition", composition_options, index=0)
if composition == "Custom":
    composition = col1.text_input("Enter custom composition")

camera_angle_options = ["Eye level", "High angle",
                        "Low angle", "Bird's eye view", "Worm's eye view", "Custom"]
camera_angle = col1.selectbox("Camera Angle", camera_angle_options, index=0)
if camera_angle == "Custom":
    camera_angle = col1.text_input("Enter custom camera angle")

style_options = ["Minimalist", "Vintage",
                 "Modern", "Industrial", "Rustic", "Custom"]
style = col1.selectbox("Style", style_options, index=0)
if style == "Custom":
    style = col1.text_input("Enter custom style")

room_type_options = ["Living room", "Bedroom",
                     "Kitchen", "Bathroom", "Office", "Custom"]
room_type = col1.selectbox("Room Type", room_type_options, index=0)
if room_type == "Custom":
    room_type = col1.text_input("Enter custom room type")

focal_point_options = ["Furniture", "Window",
                       "Artwork", "Fireplace", "Accent wall", "Custom"]
focal_point = col1.selectbox("Focal Point", focal_point_options, index=0)
if focal_point == "Custom":
    focal_point = col1.text_input("Enter custom focal point")

textures_options = ["Wood", "Stone", "Metal", "Glass", "Fabric", "Custom"]
textures = col1.selectbox("Textures", textures_options, index=0)
if textures == "Custom":
    textures = col1.text_input("Enter custom textures")

detail_options = ["Architectural details", "Decorative items",
                  "Patterns", "Fixtures", "Flooring", "Custom"]
detail = col1.selectbox("Detail", detail_options, index=0)
if detail == "Custom":
    detail = col1.text_input("Enter custom detail")

color_palette_options = ["Monochrome", "Pastels", "Warm colors",
                         "Cool colors", "Complementary colors", "Custom"]
color_palette = col2.selectbox("Color Palette", color_palette_options, index=0)
if color_palette == "Custom":
    color_palette = col2.text_input("Enter custom color palette")

brand_options = ["IKEA", "Crate & Barrel", "West Elm",
                 "Restoration Hardware", "CB2", "Custom"]
brand = col2.selectbox("Brand", brand_options, index=0)
if brand == "Custom":
    brand = col2.text_input("Enter custom brand")

lighting_options = ["Natural light", "Ambient lighting",
                    "Accent lighting", "Task lighting", "Backlighting", "Custom"]
lighting = col2.selectbox("Lighting", lighting_options, index=0)
if lighting == "Custom":
    lighting = col2.text_input("Enter custom lighting")

location_options = ["Urban", "Suburban",
                    "Rural", "Coastal", "Mountainous", "Custom"]
location = col2.selectbox("Location", location_options, index=0)
if location == "Custom":
    location = col2.text_input("Enter custom location")

time_of_day_options = ["Sunrise", "Morning",
                       "Midday", "Sunset", "Night", "Custom"]
time_of_day = col2.selectbox("Time of Day", time_of_day_options, index=0)
if time_of_day == "Custom":
    time_of_day = col2.text_input("Enter custom time of day")

mood_options = ["Calm", "Inviting", "Dramatic", "Cozy", "Energetic", "Custom"]
mood = col2.selectbox("Mood", mood_options, index=0)
if mood == "Custom":
    mood = col2.text_input("Enter custom mood")

architecture_options = ["Modern", "Traditional",
                        "Victorian", "Art Deco", "Mid-century", "Custom"]
architecture = col2.selectbox("Architecture", architecture_options, index=0)
if architecture == "Custom":
    architecture = col2.text_input("Enter custom architecture")

aspect_ratio_options = ["16:9", "4:3", "1:1", "21:9", "3:2", "Custom"]
aspect_ratio = col2.selectbox("Aspect Ratio", aspect_ratio_options, index=0)
if aspect_ratio == "Custom":
    aspect_ratio = col2.text_input("Enter custom aspect ratio")


row_numbers = st.slider("Number of Prompts", 1, 10, 5)

st.sidebar.markdown('''
---
:camera: This application is build on the **Additive Prompting** ideas of [@nickfloats](https://twitter.com/nickfloats)

:robot_face: Application created by [@Kirby_](https://twitter.com/Kirby_) & GPT-4

:bird::link: Utilizing [@LangChainAI](https://twitter.com/LangChainAI)

:point_right: The code for this app is available on [GitHub](https://github.com/jaredkirby)

---
Built by **Jared Kirby** :wave:

[Twitter](https://twitter.com/Kirby_) | [GitHub](https://github.com/jaredkirby) | [LinkedIn](https://www.linkedin.com/in/jared-kirby/) | [Portfolio](https://www.jaredkirby.me)

    '''
                    )


if st.button("Generate"):
    with st.spinner("Generating output..."):
        output = seq_chain({"framework": framework, "composition": composition, "camera_angle": camera_angle, "style": style, "room_type": room_type, "focal_point": focal_point, "textures": textures, "detail": detail,
                            "color_palette": color_palette, "brand": brand, "lighting": lighting, "location": location, "time_of_day": time_of_day, "mood": mood, "architecture": architecture, "aspect_ratio": aspect_ratio, "row_numbers": row_numbers})

        st.markdown(output["lines"])
        print(output["lines"])


# Print the output
# print(output)
