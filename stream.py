import streamlit as st
import json
import requests as re
import pandas as pd

st.markdown(
    """
    <div style="text-align: center; ">
        <h1 style="color: #ffffff; font-family: 'Helvetica Neue', sans-serif; font-size: 40px; text-transform: uppercase; ">
        <span style="background-color: #3399ff;  padding: 20px;">FinSecure</span>
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)


# Sidebar navigation
page = st.sidebar.selectbox("Select a page", ["Home","credit card fraud detection" ,"fake coin detector","bank account details"])

# Page content based on user selection
if page == "credit card fraud detection":
    st.title("credit card fraud detection")
    st.write("""
## About
Credit card fraud is a form of identity theft that involves an unauthorized taking of another's credit card information for the purpose of charging purchases to the account or removing funds from it.

**This Streamlit App utilizes a Machine Learning API in order to detect fraudulent credit card transactions based on the following criteria: hours, type of transaction, amount, balance before and after the transaction, etc.** 

        
""")
    st.markdown(
        """
        <hr style="border: 0.5px solid #ccc;">
        """,
        unsafe_allow_html=True
    )
    st.header('Input Features of The Transaction')

    sender_name = st.text_input("Input Sender ID")
    receiver_name = st.text_input("Input Receiver ID")
    step = st.slider("Number of Hours it took the Transaction to complete:", 0, 100, 50)
    types = st.radio("Enter Type of Transfer Made:", (0, 1, 2, 3, 4))
    x = {
            0: 'Cash in',
            1: 'Cash Out',
            2: 'Debit',
            3: 'Payment',
            4: 'Transfer'
        }.get(types, '')

    amount = st.number_input("Amount", 0, 110000, 5000)
    oldbalanceorg = st.number_input("sender Original Balance Before Transaction was made", 0, 110000, 5000)
    newbalanceorg = st.number_input("senders New Balance After Transaction was made", 0, 110000, 5000)
    oldbalancedest = st.number_input("Recepient Old Balance", 0, 110000, 5000)
    newbalancedest = st.number_input("Recepient New Balance", 0, 110000, 5000)
    isflaggedfraud = st.selectbox("Specify if this was flagged as Fraud by your System", (0, 1))

    if st.button("Detection Result"):
        values = {
            "step": step,
            "types": types,
            "amount": amount,
            "oldbalanceorig": oldbalanceorg,
            "newbalanceorig": newbalanceorg,
            "oldbalancedest": oldbalancedest,
            "newbalancedest": newbalancedest,
            "isflaggedfraud": isflaggedfraud
        }

        st.write(f"""### These are the transaction details:\n
            Sender ID: {sender_name}
            Receiver ID: {receiver_name}
            1. Number of Hours it took to complete: {step}\n
            2. Type of Transaction: {x}\n
            3. Amount Sent: {amount}\n
            4. Sender Previous Balance Before Transaction: {oldbalanceorg}\n
            5. Sender New Balance After Transaction: {newbalanceorg}\n
            6. Recepient Balance Before Transaction: {oldbalancedest}\n
            7. Recepient Balance After Transaction: {newbalancedest}\n
            8. System Flag Fraud Status: {isflaggedfraud}
                        """)

        # Update the URL to point to your Django backend
    backend_url = "http://localhost:8000/predict/"  # Replace with your Django backend URL
    res = re.post(backend_url, json=values)
    json_str = json.dumps(res.json())
    resp = json.loads(json_str)
        
    if sender_name=='' or receiver_name == '':
            st.write("Error! Please input Transaction ID or Names of Sender and Receiver!")
    else:
            st.write(f"""### The '{x}' transaction that took place between {sender_name} and {receiver_name} is {resp['result']}.""")


elif page == "fake coin detector":    
    st.title("fake coin detector")
    st.write("""\n\n
            **FinSecure introduces a groundbreaking 
            approach to counterfeit detection in the realm of digital currencies.**
             
             \n 
             **This Streamlit App utilizes a Deep Learning API in order to detect fraudulent in coins  based on the following criteria: upload image of coin** 
             \n
             \n
             """)
    st.write("Upload an image for fake coin detector.")

    uploaded_file = st.file_uploader("Choose an image of your coin...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        st.write("")
        st.write("Classifying...")

        # Add a button to trigger the classification
        if st.button("Classify Image"):
            # Create a dictionary with the image data
            image_data = {"image": uploaded_file.getvalue()}

            # Update the URL to point to your Django backend classify_image endpoint
            backend_url = "http://localhost:8000/classify_image/"  # Replace with your Django backend URL
            res = re.post(backend_url, files=image_data)
            json_str = json.dumps(res.json())
            resp = json.loads(json_str)

            st.write(f"Prediction: {resp['result']}")

elif page == "bank account details":    
    
    # Sample data for demonstration
    transaction_data = {
        'Date': ['2022-01-01', '2022-02-01', '2022-03-01'],
        'Description': ['Deposit', 'Withdrawal', 'Transfer'],
        'Amount': [1000, -500, -200],
    }

    # Sample personal details
    personal_details = {
        'Name': 'John Doe',
        'Mobile Number': '+1234567890',
        'Account Number': '123456789',
        # Add more details as needed
    }

    def display_personal_details():
        st.sidebar.title('Personal Details')
        for key, value in personal_details.items():
            st.sidebar.write(f'**{key}:** {value}')

    def display_transaction_table():
        st.title('Transaction Details')
        transaction_df = pd.DataFrame(transaction_data)
        st.table(transaction_df)

    # # Your existing Streamlit app code goes here

     # Add the new feature
    
    st.markdown(
        """
        <hr style="border: 0.5px solid #ccc;">
        """,
        unsafe_allow_html=True
    )
    
    if st.button('Show Personal Details and Transactions'):
         display_personal_details()
         display_transaction_table()
    # Add the new feature with centered button using custom CSS
    
elif page == "Home":
    st.title("welcome to **FinSecure**")
    st.write("""
             \n\n
             FinSecure employs sophisticated algorithms and machine learning techniques to meticulously analyze transaction patterns, flagging potentially fraudulent activities in real-time. Our state-of-the-art anomaly detection system ensures swift identification and prevention of unauthorized 
             transactions, minimizing the risk of financial losses and ensuring the integrity of your financial data.
             \n\n
             Leveraging Convolutional Neural Networks (CNN), FinSecure introduces a groundbreaking approach to counterfeit detection in the realm of digital currencies. Our CNN-based technology scrutinizes the minutest details, providing an extra layer of security against fake coins. Stay ahead of emerging threats and enjoy the peace of mind that your digital assets are genuine and secure
             """)
    st.markdown(
        """
        <hr style="border: 0.5px solid #ccc;">
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <h2>contributors</h2>
        <h4>- Ronak Verma </h4>
        <h4>- Akash Verma </h4>
        <h4>- Abhishek Singh Rajpurohit</h4>
        """,
        unsafe_allow_html=True
    )



# You can add more pages as needed

