import streamlit as st
import os
import pyperclip
from groq import Groq

# CRITICAL: set_page_config MUST be the first Streamlit command
st.set_page_config(
    page_title="Customer Reply Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
body, .stApp {
    background-color: #262730;
    color: white;
}
textarea {
    background-color: #262730 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Work Sans', sans-serif;
    }
    
    .main {
        padding: 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        font-weight: 500;
    }
    .stTextArea>div>div>textarea {
        background-color: #f0f2f6;
        font-family: 'Work Sans', sans-serif;
    }
    .css-1d391kg {
        padding: 0;
    }
    h1 {
        color: inherit;
        padding: 0;
        margin: 0;
        margin-bottom: 3rem;
        font-weight: 600;
        text-align: center;
        font-size: 3.5rem;
    }
    h2 {
        color: #424242;
        padding: 0;
        margin: 0;
        font-weight: 600;
    }
    .stAlert {
        padding: 0.5rem;
        border-radius: 5px;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }
    div[data-testid="stVerticalBlock"] > div:last-child {
        margin-bottom: 0;
    }
    .stTextInput>div>div>input {
        font-family: 'Work Sans', sans-serif;
    }
    .stSelectbox>div>div>select {
        font-family: 'Work Sans', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- IMPORTANT: Set your Groq API Key ---
# (Your API key setup code remains here)
# For robust key management, prefer environment variables or Streamlit Secrets
try:
    # Try to get the API key from Streamlit secrets first, then environment variable
    api_key_value = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not api_key_value:
        st.error("GROQ_API_KEY is not set. Please add it to Streamlit secrets (on the cloud) or as an environment variable (locally).")
        client = None
    else:
        client = Groq(api_key=api_key_value)
except Exception as e:
    st.error(f"Failed to initialize Groq client. Error: {e}. Ensure GROQ_API_KEY is correctly set and the Groq library is functional.")
    client = None


# (generate_reply_with_groq function remains the same)
def generate_reply_with_groq(reply_type, customer_name, order_id, tracking_id=None, courier_website=None, other_comments=None):
    if not client:
        return "Error: Groq API client not initialized. Please ensure GROQ_API_KEY is set and the client was created successfully."

    system_prompt = "You are a helpful customer service assistant for Toffle. Your tone should be professional, empathetic, and polite. Use 'we' instead of 'I' when responding. Generate replies based on the user's input and keep them concise and to the point. Include any additional notes or context provided. End the reply with:\n\nWarm Regards,\nTeam Toffle"
    
    user_prompt_detail = ""
    if reply_type == 'Order Status Inquiry':
        user_prompt_detail = f"The query is about an 'Order Status Inquiry'. Customer Name: {customer_name}, Order ID: {order_id}."
        if tracking_id and courier_website:
            user_prompt_detail += f" The order has been shipped with Tracking ID: {tracking_id} and can be tracked at {courier_website}. Please provide a status update based on this."
        else:
            user_prompt_detail += " The order status is currently being checked. Please provide a general update and mention that tracking details will be shared if available or once shipped."
    elif reply_type == 'Order Delayed':
        user_prompt_detail = f"The query is about an 'Order Delayed' scenario. Customer Name: {customer_name}, Order ID: {order_id}. Please apologize and provide a believable, generic excuse for the delay."
        if tracking_id and courier_website:
            user_prompt_detail += f" The order has been shipped with Tracking ID: {tracking_id} and can be tracked at {courier_website}."
        else:
            user_prompt_detail += " The order has not been shipped yet."
    elif reply_type == 'Return Request - Fitting Issue':
        user_prompt_detail = f"The query is a 'Return Request - Fitting Issue'. Customer Name: {customer_name}, Order ID: {order_id}. Inform the customer they need to send the item back to F-213/C, First Floor, Old M B Road, Nai Basti, Lado Sarai, New Delhi, Delhi 110030, and explain what happens next (e.g., processing refund/store credit upon receipt)."
    elif reply_type == 'Exchange Request':
        user_prompt_detail = f"The query is an 'Exchange Request'. Customer Name: {customer_name}, Order ID: {order_id}. Explain that we will arrange a pickup and ask them for the new size or item they require."
    else: # Fallback for any other type
        user_prompt_detail = f"Generate a generic customer service reply for: Customer Name: {customer_name}, Order ID: {order_id} regarding: {reply_type}."

    user_prompt = f"Customer Name: {customer_name}\nOrder ID: {order_id}\nReply Type: {reply_type}\nDetails: {user_prompt_detail}"
    if other_comments:
        user_prompt += f"\nAdditional Notes: {other_comments}"
    user_prompt += "\n\nGenerate a professional and empathetic reply based on these details."

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                }
            ],
            model="llama3-70b-8192", # Or your preferred Groq model
            temperature=0.7,
            max_tokens=250,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error calling Groq API: {e}")
        return f"Sorry, I encountered an error trying to generate a reply from Groq. Details: {e}"


# Streamlit app UI
def main():
    st.title('Customer Reply Generator')
    
    # Main content columns
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### 📝 Input Details")
        with st.container():
            reply_type = st.selectbox(
                'Select Reply Type', 
                ['Order Status Inquiry', 'Order Delayed', 'Return Request - Fitting Issue', 'Exchange Request', 'Other Inquiry'], 
                key='reply_type_select'
            )

            customer_name = st.text_input('Customer Name', key='customer_name_input')
            order_id = st.text_input('Order ID', key='order_id_input')

            tracking_id = None
            courier_website = None

            # Conditional inputs
            if reply_type in ['Order Status Inquiry', 'Order Delayed']:
                tracking_id = st.text_input('Tracking ID (if shipped)', key='tracking_id_input')
                courier_website = st.text_input('Courier Website Link (if shipped)', key='courier_website_input')

            if reply_type == 'Return Request - Fitting Issue':
                st.info('Return Address: F-213/C, First Floor, Old M B Road, Nai Basti, Lado Sarai, New Delhi, Delhi 110030')
            
            if reply_type in ['Order Status Inquiry', 'Order Delayed', 'Other Inquiry', 'Exchange Request', 'Return Request - Fitting Issue']:
                other_comments = st.text_input('Custom Notes (optional)', key='other_comments')

            st.markdown("---")  # Add a horizontal line before the button
            
            if st.button('✨ Generate Reply', key='generate_button', use_container_width=True, type="primary"):
                if not client:
                    st.error("Groq API client not initialized or failed to initialize. Please ensure your GROQ_API_KEY is set as an environment variable and is correct.")
                elif not customer_name or not order_id:
                    st.error('Please enter both Customer Name and Order ID')
                else:
                    with st.spinner("🤖 Generating reply with Groq AI..."):
                        reply = generate_reply_with_groq(reply_type, customer_name, order_id, tracking_id, courier_website, other_comments)
                        st.session_state.generated_reply = reply

    with col2:
        st.markdown("### 📤 Generated Reply")
        if 'generated_reply' in st.session_state:
            st.text_area('', st.session_state.generated_reply, height=300, key='reply_output_area', help="Copy the text below to send to the customer.")
            
            if st.button('📋 Copy to Clipboard', key='copy_button', use_container_width=True, type="secondary"):
                pyperclip.copy(st.session_state.generated_reply)
                st.success("✅ Reply copied to clipboard successfully!")
        else:
            st.info("The AI-generated reply will appear here once you provide the details and click 'Generate Reply'.")

    # Footer
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Make sure to fill in all required fields
    - Use Custom Notes to add any specific details
    - Click the Copy button to easily copy the generated reply
    """)

if __name__ == '__main__':
    main()
