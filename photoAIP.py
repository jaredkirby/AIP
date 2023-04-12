import streamlit as st
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.llms import OpenAI
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate

st.set_page_config(
    page_icon=":camera:",
    layout="centered",
)

st.title("Film Photography - Additive Prompt Generator for Midjourney")
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
table_template = '''
Please create a table with {row_numbers} rows that breaks down a {framework} composition into the following key elements, where each of these key elements is a column: 
Subject, Location, Clothing Type, Clothing Color, Shot Type, Color Pallet, Styling, Lighting, Ambiance, Film Type, Lens, Fine Tuning.
If a column data listed below is "none", then leave the cell blank.

Fill the first row of the table with data where:
Subject = {subject}
Location = {location}
Clothing Type = {clothing_type}
Clothing Color = {clothing_color}
Shot Type = {shot_type}
Color Pallet = {color_pallet}
Styling = {styling}
Lighting = {lighting}
Ambiance = {ambiance}
Film Type = {film_type}
Lens = {lens}
Fine Tuning = {fine_tuning}

Then use a variety of data for all subsequent rows, ensuring that it differs from the first and all other rows and aligns with the key elements listed above in a sensible way.
'''
table_prompt = PromptTemplate(template=table_template,
                              input_variables=["framework", "subject", "film_type", "lens", "lighting", "shot_type", "styling",
                                               "ambiance", "location", "fine_tuning", "clothing_type", "clothing_color", "row_numbers", "color_pallet"])
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
    seq_chain = SequentialChain(
        chains=[table_chain, line_chain],
        input_variables=["framework", "subject", "film_type", "lens", "lighting", "shot_type", "styling",
                         "ambiance", "location", "fine_tuning", "clothing_type", "clothing_color", "aspect_ratio", "row_numbers", "color_pallet"],
        output_variables=["lines"],
        verbose=True,
    )
    print(line_chain)
    print(table_chain)
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

# Film photography
framework = "Film photography photograph"

subject_options = ["Landscape", "Portrait", "Wildlife", "Street photography", "Architecture", "Product photography",
                   "Macro photography", "Wedding", "Sport", "Travel photography", "Fashion photography", "Food photography",
                   "Astrophotography", "Black and white photography", "Still life photography", "Documentary photography", "Custom"]
subject = col1.selectbox("Subject", subject_options, index=0)
if subject == "Custom":
    subject = col1.text_input("Enter custom subject")

film_type_options = ["Kodak Gold 400", "Porta 400", "Fujifilm Pro 160C", "Agfa Vista 400", "Ilford HP5 Plus",
                     "Kodak Tri-X 400", "Fujifilm Velvia 50", "Ilford Delta 3200", "Kodak Ektar 100", "Fuji Provia 100F",
                     "Lomography Color Negative 400", "CineStill 800T", "Kodak Portra 800", "Fujifilm Superia X-TRA 400",
                     "Ilford XP2 Super 400", "Kodak T-MAX 400", "Fujifilm Neopan 100 Acros" "Custom"]
film_type = col1.selectbox("Film Type", film_type_options, index=0)
if film_type == "Custom":
    film_type = col1.text_input("Enter custom film type")

color_pallet_options = ["Black and white", "Monochromatic", "Analogous", "Complementary", "Triadic", "Tetradic",
                        "Split Complementary", "Double Complementary", "Warm Colors", "Cool Colors", "Neutral Colors",
                        "Pastel Colors", "Bold Colors", "Earth Tones", "Jewel Tones", "Muted Tones", "Bright Colors",
                        "Primary Colors", "Secondary Colors", "Tertiary Colors", "Gradient Colors", "Rainbow Colors",
                        "Metallic Colors", "Vintage Colors", "Retro Colors", "Muted Pastels", "Saturated Colors",
                        "Desaturated Colors", "High-Contrast Colors", "Custom"]
color_pallet = col1.selectbox("Color Pallet", color_pallet_options, index=0)
if color_pallet == "Custom":
    color_pallet = col1.text_input("Enter custom color pallet")

lens_options = ["Canon FD 50mm f/1.4", "Nikon Nikkor-S 50mm f/1.4", "Leica Summicron-M 50mm f/2", "Minolta MC Rokkor-PG 50mm f/1.4",
                "Pentax Super-Takumar 50mm f/1.4", "Carl Zeiss Jena Tessar 50mm f/2.8", "Voigtlander Nokton 50mm f/1.5",
                "Olympus Zuiko 50mm f/1.8", "Yashica ML 50mm f/1.4", "Contax Planar 50mm f/1.4", "", "Custom"]
lens = col1.selectbox("Camera Lens", lens_options, index=0)
if lens == "Custom":
    lens = col1.text_input("Enter custom camera lens")

lighting_options = ["Natural light", "Back-lit", "Edge-lit", "Continuous lighting", "Flash photography", "Strobe lighting", "Softbox",
                    "Umbrella", "Ring light", "Beauty dish", "LED panels", "Reflector", "Gobo", "Snoot", "Barndoor", "Grid", "Honeycomb",
                    "Diffuser", "Custom"]
lighting = col1.selectbox("Lighting", lighting_options, index=0)
if lighting == "Custom":
    lighting = col1.text_input("Enter custom lighting")

shot_type_options = ["Close-up", "Low angle", "Birds-eye view", "High angle", "Wide shot", "Medium shot", "Full shot", "Extreme close-up",
                     "Over-the-shoulder shot", "Point-of-view shot", "Dutch angle", "Tilt shot", "Panning shot", "Zoom shot", "Tracking shot",
                     "Crane shot", "Handheld shot", "Static shot", "Long shot", "Two-shot", "Reverse shot", "Custom"]
shot_type = col1.selectbox("Shot Type", shot_type_options, index=0)
if shot_type == "Custom":
    shot_type = col1.text_input("Enter custom shot type")

styling_options = ["Street", "Warhol", "Anime", "Picasso", "Minimalism", "Abstract", "Surrealism", "Conceptual", "Documentary", "Landscape",
                   "Portrait", "Fashion", "Fine art", "Black and white", "Color", "Vintage", "Film noir", "Gothic", "High-key", "Low-key",
                   "HDR", "Bokeh", "Tilt-shift", "Long exposure", "Infrared", "Silhouette", "Custom"]
styling = col1.selectbox("Styling", styling_options, index=0)
if styling == "Custom":
    styling = col1.text_input("Enter custom styling")

ambiance_options = ["Mysty", "Smokey", "Dreamy", "Spooky", "Romantic", "Magical", "Serene", "Ethereal", "Whimsical", "Charming", "Enchanting",
                    "Nostalgic", "Melancholic", "Gritty", "Industrial", "Lively", "Vibrant", "Gloomy", "Mysterious", "Intimate", "Relaxing",
                    "Cheerful", "Energetic", "Peaceful", "Custom"]
ambiance = col2.selectbox("Ambiance", ambiance_options, index=0)
if ambiance == "Custom":
    ambiance = col1.text_input("Enter custom ambiance")

location_options = ["New York", "High Mountains", "Ancient Egypt", "Underwater", "International Space Station", "Seattle", "Paris",
                    "Tropical Island", "Rainforest", "Desert", "Small town", "Countryside", "Castle", "Amusement Park", "Factory",
                    "Library", "Museum", "College Campus", "Train Station", "Subway", "Zoo", "Airport", "Harbor", "Farm", "Shopping Mall", "Custom"]
location = col2.selectbox("Location", location_options, index=0)
if location == "Custom":
    location = col1.text_input("Enter custom location")

fine_tuning_options = ["Fine-grain", "4k", "Light Leaks", "Double Exposure", "Slow Shutter Speed", "High Depth of Field", "Shallow Depth of Field",
                       "Lens distortion", "Chromatic Aberration", "Vignetting", "High Clarity", "High Sharpness", "High Saturation", "Low Saturation",
                       "High Contrast", "Low Contrast", "Split Toning", "Custom"]
fine_tuning = col2.selectbox("Fine Tuning", fine_tuning_options, index=0)
if fine_tuning == "Custom":
    fine_tuning = col1.text_input("Enter custom fine tuning")

clothing_type_options = ["None", "Dress", "Top", "T-Shirt", "Blouse", "Sweater", "Cardigan", "Jacket", "Coat", "Jeans", "Trouser", "Legging", "Skirt", "Shorts",
                         "Swimsuit", "Sleepwear", "Robe", "Jumpsuit", "Bodysuit", "Suit", "Formalwear", "Sportswear", "Activewear",
                         "Hoodie", "Sweatshirt", "Vest", "Tank Top", "Crop Top", "Custom"]
clothing_type = col2.selectbox("Clothing Type", clothing_type_options, index=0)
if clothing_type == "Custom":
    clothing_type = col2.text_input("Enter custom clothing type")

clothing_color_options = ["None", "Black", "White", "Gray", "Navy", "Blue", "Red", "Burgundy", "Purple", "Pink", "Magenta", "Orange", "Yellow", "Green", "Teal",
                          "Turquoise", "Beige", "Brown", "Olive", "Mustard", "Gold", "Silver", "Metallic", "Pastel", "Neon", "Earth Tones", "Jewel Tones",
                          "Muted Tones", "Bright Colors", "Primary Colors", "Custom"]
clothing_color = col2.selectbox(
    "Clothing Color", clothing_color_options, index=0)
if clothing_color == "Custom":
    clothing_color = col2.text_input("Enter custom clothing color")

aspect_ratio_options = ["16:9", "4:3", "1:1", "21:9", "3:2", "Custom"]
aspect_ratio = col2.selectbox("Aspect Ratio", aspect_ratio_options, index=0)
if aspect_ratio == "Custom":
    aspect_ratio = col2.text_input("Enter custom aspect ratio")

row_numbers = st.slider("Number of Prompts", 1, 10, 5)

st.sidebar.markdown('''
---
:camera: This application is build on the **Additive Prompting** ideas of [@nickfloats](https://twitter.com/nickfloats)

:robot_face: Application created by [@Kirby_](https://twitter.com/Kirby_) & GPT-4

:bird::link: Utilizing [@LangChainAI](https://twitter.com/LangChainAI)")

:point_right: The code for this app is available on [GitHub](https://github.com/jaredkirby)

---
Built by **Jared Kirby** :wave:

[Twitter](https://twitter.com/Kirby_) | [GitHub](https://github.com/jaredkirby) | [LinkedIn](https://www.linkedin.com/in/jared-kirby/) | [Portfolio](https://www.jaredkirby.me)

    '''
                    )

if st.button("Generate"):
    with st.spinner("Generating output..."):
        output = seq_chain({"framework": framework, "subject": subject,  "lighting": lighting, "location": location, "aspect_ratio": aspect_ratio,
                            "row_numbers": row_numbers, "film_type": film_type, "lens": lens, "shot_type": shot_type, "styling": styling, "ambiance": ambiance,
                            "fine_tuning": fine_tuning, "clothing_type": clothing_type, "clothing_color": clothing_color, "color_pallet": color_pallet})

        st.markdown(output["lines"])
        print(output["lines"])
