# Toffle Customer Reply Generator

A Streamlit web application that helps generate professional customer service replies using the Groq API.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

3. Run the Streamlit application:
```bash
streamlit run app.py
```

## Features

- Select from different reply types (Order Status, Shipping, Returns, etc.)
- Input customer details and order information
- Dynamic form fields based on reply type
- AI-powered reply generation using Groq API
- Copy generated replies to clipboard

## Usage

1. Select the appropriate reply type from the dropdown menu
2. Fill in the required customer information
3. Add any additional details specific to the reply type
4. Click "Generate Reply" to create a professional response
5. Copy the generated reply using the "Copy to Clipboard" button

## Note

Make sure to keep your Groq API key secure and never commit it to version control. # ai_customer_reply_generator
