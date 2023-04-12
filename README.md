# Film Photography - Additive Prompt Generator for Midjourney

This is a Streamlit web application that generates creative prompts for film photography generation via Midjourney. The generated prompts are based on specific input parameters, such as subject, film type, color pallet, lens, and more.

## How it works

1.  Users input their preferences for various aspects of film photography.
2.  The application generates a table that breaks down the image into its key elements.
3.  The table is filled with variations created by the language model.
4.  A list of suggested prompts is generated from the table data.

## Features

- Customizable prompts based on user inputs
- Utilizes OpenAI's GPT-4 large language model
- Generates multiple prompt variations
- Easy-to-use interface built with Streamlit

## Requirements

- Python 3.7 or later
- Streamlit
- OpenAI API key

## Getting Started

1.  Clone this repository.
2.  Install the required packages using `pip install -r requirements.txt`.
3.  Run the application using `streamlit run app.py`.
4.  Open the application in your web browser.

## Usage

1.  Enter your OpenAI API key in the sidebar.
2.  Select or enter your preferences for various aspects of film photography.
3.  Choose the number of prompt variations to generate.
4.  Click the "Generate Prompts" button to generate prompts.
5.  The generated prompts will be displayed in a bulleted markdown list.

## Notes

- This application is built on the Additive Prompting ideas of [
