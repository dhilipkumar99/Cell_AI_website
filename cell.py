import streamlit as st
from PIL import Image
import zipfile
import os
import base64
import pandas as pd
import csv
from io import StringIO
import datetime
import json
import shutil

# Set up page config
st.set_page_config(page_title="CellAI - Automated ROI Selection", layout="wide", page_icon="🤖")

# Convert an image file to a base64 string
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Function to handle unsubscribe requests
def handle_unsubscribe():
    st.title("Unsubscribe from Fluorocell.ai Email Communications")
    
    # Get email from query parameters - check multiple possible parameter names
    # Using the non-experimental API
    email = st.query_params.get("email", [""])[0]
    
    # If email is not in the query params directly, check if it's passed as part of the unsubscribe parameter
    if not email and "unsubscribe" in st.query_params:
        email = st.query_params.get("unsubscribe", [""])[0]
    
    # Create a form for unsubscribing
    with st.form("unsubscribe_form"):
        # Display the full email address above the form input
        if email:
            st.markdown(f"### Email address to unsubscribe: **{email}**")
            
            # Use a full-width text input that shows the complete email
            # Note: We're intentionally NOT using disabled=True as that can cause display issues
            email_input = st.text_input("Confirm Email Address", 
                                       value=email,
                                       key="email_field",
                                       help="Please confirm this is your email address")
        else:
            email_input = st.text_input("Your Email Address", placeholder="Enter your email address")
        
        reason = st.selectbox(
            "Reason for unsubscribing (optional)",
            [
                "Select a reason (optional)",
                "Too many emails",
                "Not relevant to my work",
                "I no longer need this service",
                "I didn't sign up for this",
                "Other"
            ]
        )
        
        if reason == "Other":
            other_reason = st.text_area("Please specify your reason", "")
        
        submitted = st.form_submit_button("Confirm Unsubscribe")
        
        if submitted and email_input:
            # Load existing unsubscribed users
            unsubscribed = load_unsubscribed_users()
            
            # Add the new unsubscribed email if it's not already in the list
            if email_input.lower() not in [e.lower() for e in unsubscribed]:
                add_unsubscribed_user(email_input, reason if reason != "Select a reason (optional)" else "No reason provided")
                st.success(f"You have been successfully unsubscribed from our email communications. You will no longer receive emails from fluorocell.ai.")
            else:
                st.info("Your email is already unsubscribed from our communications.")
            
            st.write("You may close this page now.")
        elif submitted:
            st.error("Please enter a valid email address.")

# Function to load unsubscribed users from session state or initialize it
def load_unsubscribed_users():
    if 'unsubscribed_users' not in st.session_state:
        # Try to load from a file if it exists
        try:
            # First try CSV in the primary location
            primary_csv_path = 'unsubscribed_users.csv'
            if os.path.exists(primary_csv_path):
                df = pd.read_csv(primary_csv_path)
                st.session_state.unsubscribed_users = df.to_dict('records')
                return [user['email'] for user in st.session_state.unsubscribed_users]
                
            # Check Mac-specific locations for email script file
            mac_paths = [
                os.path.expanduser('~/Documents/Python/unsubscribed_users.csv'),  # Python folder in Documents
                os.path.expanduser('~/unsubscribed_users.csv'),  # Home directory
                '/tmp/unsubscribed_users.csv'  # Temp directory
            ]
            
            for path in mac_paths:
                if os.path.exists(path):
                    df = pd.read_csv(path)
                    st.session_state.unsubscribed_users = df.to_dict('records')
                    # Sync to the primary location
                    os.makedirs(os.path.dirname(primary_csv_path) or '.', exist_ok=True)
                    df.to_csv(primary_csv_path, index=False)
                    return [user['email'] for user in st.session_state.unsubscribed_users]
                    
            # Try JSON backup as last resort
            json_paths = [
                'unsubscribed_users.json',
                os.path.expanduser('~/Documents/Python/unsubscribed_users.json'),
                os.path.expanduser('~/unsubscribed_users.json')
            ]
            
            for json_path in json_paths:
                if os.path.exists(json_path):
                    with open(json_path, 'r') as f:
                        st.session_state.unsubscribed_users = json.load(f)
                        # Sync to the primary location
                        df = pd.DataFrame(st.session_state.unsubscribed_users)
                        df.to_csv(primary_csv_path, index=False)
                        return [user['email'] for user in st.session_state.unsubscribed_users]
                        
            # If we get here, no files were found - initialize empty list
            st.session_state.unsubscribed_users = []
        except Exception as e:
            st.session_state['load_error'] = str(e)
            st.session_state.unsubscribed_users = []
    
    return [user['email'] for user in st.session_state.unsubscribed_users]

# Function to add a new unsubscribed user
def add_unsubscribed_user(email, reason=""):
    if 'unsubscribed_users' not in st.session_state:
        st.session_state.unsubscribed_users = []
    
    # Add the new user with timestamp
    st.session_state.unsubscribed_users.append({
        'email': email.lower().strip(),
        'reason': reason,
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Save to CSV
    save_unsubscribed_users()

# Function to save unsubscribed users to a CSV file
def save_unsubscribed_users():
    if 'unsubscribed_users' in st.session_state:
        # Create DataFrame from session state
        df = pd.DataFrame(st.session_state.unsubscribed_users)
        
        # Save to Streamlit's directory (primary location)
        primary_csv_path = 'unsubscribed_users.csv'
        df.to_csv(primary_csv_path, index=False)
        
        # Try to save to locations the email script can access
        try:
            # Mac-specific paths, especially for your setup
            mac_paths = [
                os.path.expanduser('~/Documents/Python/unsubscribed_users.csv'),  # Your Python folder
                os.path.expanduser('~/unsubscribed_users.csv'),  # Home directory
                '/tmp/unsubscribed_users.csv'  # Temp directory that might be accessible
            ]
            
            for path in mac_paths:
                try:
                    # Create directory if it doesn't exist
                    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
                    # Copy the file
                    df.to_csv(path, index=False)
                except Exception as e:
                    continue
                    
            # Export to JSON format as well (sometimes more reliable)
            json_data = json.dumps(st.session_state.unsubscribed_users)
            with open('unsubscribed_users.json', 'w') as f:
                f.write(json_data)
                
            # Also try to save JSON to your Python folder
            json_path = os.path.expanduser('~/Documents/Python/unsubscribed_users.json')
            try:
                os.makedirs(os.path.dirname(json_path) or '.', exist_ok=True)
                with open(json_path, 'w') as f:
                    f.write(json_data)
            except:
                pass
                
            # Return success
            return True
        except Exception as e:
            st.session_state['save_error'] = str(e)
            return False
    return False

# Function to display the admin page for managing unsubscriptions
def show_admin_page():
    st.title("Unsubscribe List Management")
    
    # Password protection
    password = st.text_input("Enter admin password", type="password")
    if password != "cellai2025":  # Simple password, consider more secure authentication in production
        st.warning("Please enter the correct password to access the admin panel")
        return
    
    # Load unsubscribed users
    if 'unsubscribed_users' not in st.session_state:
        load_unsubscribed_users()
    
    # Add option to check for file status and sync
    with st.expander("File Status & Sync Options", expanded=True):
        st.write("### File Status")
        
        # Show file paths and existence
        csv_exists = os.path.exists('unsubscribed_users.csv')
        json_exists = os.path.exists('unsubscribed_users.json')
        mac_csv_exists = os.path.exists(os.path.expanduser('~/Documents/Python/unsubscribed_users.csv'))
        
        st.write(f"CSV file in Streamlit directory: {'✅ Exists' if csv_exists else '❌ Not found'}")
        st.write(f"JSON backup in Streamlit directory: {'✅ Exists' if json_exists else '❌ Not found'}")
        st.write(f"CSV file in your Python folder: {'✅ Exists' if mac_csv_exists else '❌ Not found'}")
        
        # Error messages if any
        if 'load_error' in st.session_state:
            st.error(f"Last load error: {st.session_state['load_error']}")
        if 'save_error' in st.session_state:
            st.error(f"Last save error: {st.session_state['save_error']}")
        
        # Force save button
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Force Save Unsubscribe List"):
                success = save_unsubscribed_users()
                if success:
                    st.success("✅ Unsubscribe list saved to multiple locations")
                else:
                    st.error("❌ Error saving unsubscribe list")
        
        with col2:
            if st.button("Check for External Updates"):
                # Temporarily store current list
                current_emails = {u['email'].lower() for u in st.session_state.unsubscribed_users}
                
                # Force reload from files
                if 'unsubscribed_users' in st.session_state:
                    del st.session_state['unsubscribed_users']
                
                # Load from files
                new_emails = load_unsubscribed_users()
                
                # Compare
                added = len(new_emails) - len(current_emails)
                if added > 0:
                    st.success(f"✅ Found {added} new unsubscribed emails")
                else:
                    st.info("No new unsubscribes found")
        
        # Show manual sync instructions
        st.write("### Manual Sync Instructions")
        st.write("If automatic sync isn't working:")
        st.write("1. Download the unsubscribe list using the button below")
        st.write("2. Place the file in your Python folder at: ~/Documents/Python/")
        st.write("3. Make sure the filename is exactly: unsubscribed_users.csv")
    
    # Display the list
    if st.session_state.unsubscribed_users:
        df = pd.DataFrame(st.session_state.unsubscribed_users)
        st.write(f"Total unsubscribed users: {len(df)}")
        st.dataframe(df)
        
        # Export feature
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Unsubscribed List as CSV",
            data=csv,
            file_name="unsubscribed_users.csv",
            mime="text/csv"
        )
        
        # Clear list option
        if st.button("Clear Unsubscribe List"):
            if st.checkbox("I understand this will permanently delete all unsubscribe data"):
                st.session_state.unsubscribed_users = []
                save_unsubscribed_users()
                st.success("Unsubscribe list has been cleared")
                st.rerun()
    else:
        st.info("No unsubscribed users found")
    
    # Import feature
    st.subheader("Import Unsubscribed Users")
    uploaded_file = st.file_uploader("Upload a CSV file with email addresses", type="csv")
    if uploaded_file is not None:
        try:
            import_df = pd.read_csv(uploaded_file)
            if 'email' in import_df.columns:
                # Get existing emails
                existing_emails = [u['email'].lower() for u in st.session_state.unsubscribed_users]
                
                # Add new emails
                imported = 0
                for _, row in import_df.iterrows():
                    email = row['email'].lower().strip()
                    if email not in existing_emails and '@' in email:
                        reason = row.get('reason', "Imported") if 'reason' in import_df.columns else "Imported"
                        timestamp = row.get('timestamp', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) if 'timestamp' in import_df.columns else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        st.session_state.unsubscribed_users.append({
                            'email': email,
                            'reason': reason,
                            'timestamp': timestamp
                        })
                        imported += 1
                
                save_unsubscribed_users()
                st.success(f"Successfully imported {imported} new email addresses")
                st.rerun()
            else:
                st.error("CSV file must contain an 'email' column")
        except Exception as e:
            st.error(f"Error importing file: {e}")

#Check for route to display
def main():
    # Check if debug mode is enabled
def main():
    # Check if debug mode is enabled
    if "debug" in st.query_params:
        st.title("Debug Information")
        st.write(f"Current working directory: {os.getcwd()}")
        st.write("Files in current directory:")
        files = os.listdir(".")
        for file in files:
            st.write(f"- {file}")
        
        # CSV Management Section
        st.header("Unsubscribed Users Management")
        
        # Initialize or load CSV data
        csv_exists = os.path.exists("unsubscribed_users.csv")
        
        if csv_exists:
            df = pd.read_csv("unsubscribed_users.csv")
            
            # Store the dataframe in session state for editing
            if 'df_unsubscribed' not in st.session_state:
                st.session_state.df_unsubscribed = df.copy()
            
            # Display current data with options to edit
            st.subheader("Current Unsubscribed Users")
            
            # Create tabs for different operations
            tab1, tab2, tab3, tab4 = st.tabs(["View/Edit", "Delete Rows", "Add New Emails", "Upload/Append"])
            
            with tab1:
                # Editable dataframe
                edited_df = st.data_editor(
                    st.session_state.df_unsubscribed, 
                    use_container_width=True,
                    num_rows="dynamic",
                    key="editor"
                )
                
                if st.button("Save Changes", key="save_changes"):
                    try:
                        edited_df.to_csv("unsubscribed_users.csv", index=False)
                        st.session_state.df_unsubscribed = edited_df.copy()
                        st.success("Changes saved successfully!")
                        
                        # Try to save to the additional locations for email script compatibility
                        save_unsubscribed_users_to_all_locations(edited_df)
                    except Exception as e:
                        st.error(f"Error saving changes: {e}")
            
            with tab2:
                st.write("Select rows to delete:")
                
                if not st.session_state.df_unsubscribed.empty:
                    # Get emails for multiselect
                    all_emails = st.session_state.df_unsubscribed['email'].tolist()
                    
                    # Allow selection of multiple emails to delete
                    emails_to_delete = st.multiselect(
                        "Select emails to remove from unsubscribe list:",
                        options=all_emails
                    )
                    
                    if emails_to_delete and st.button("Delete Selected Emails"):
                        # Filter out the selected emails
                        st.session_state.df_unsubscribed = st.session_state.df_unsubscribed[
                            ~st.session_state.df_unsubscribed['email'].isin(emails_to_delete)
                        ]
                        
                        # Save the updated dataframe
                        try:
                            st.session_state.df_unsubscribed.to_csv("unsubscribed_users.csv", index=False)
                            st.success(f"Successfully removed {len(emails_to_delete)} email(s)!")
                            
                            # Try to save to the additional locations
                            save_unsubscribed_users_to_all_locations(st.session_state.df_unsubscribed)
                        except Exception as e:
                            st.error(f"Error saving changes: {e}")
                    
                    # Option to clear all unsubscribed users
                    if st.button("Clear All Unsubscribed Users", type="primary", use_container_width=True):
                        confirm = st.checkbox("I understand this will permanently delete all unsubscribe data")
                        
                        if confirm:
                            # Create empty DataFrame with just the headers
                            st.session_state.df_unsubscribed = pd.DataFrame(columns=st.session_state.df_unsubscribed.columns)
                            
                            # Save the empty dataframe
                            try:
                                st.session_state.df_unsubscribed.to_csv("unsubscribed_users.csv", index=False)
                                st.success("Unsubscribe list has been cleared!")
                                
                                # Try to save to the additional locations
                                save_unsubscribed_users_to_all_locations(st.session_state.df_unsubscribed)
                            except Exception as e:
                                st.error(f"Error clearing list: {e}")
                else:
                    st.info("No unsubscribed users in the list.")
            
            with tab3:
                st.write("Add new email addresses to the unsubscribe list:")
                
                # Input for a new email
                new_email = st.text_input("Enter email address to add:")
                
                # Button to add a single email
                if new_email and st.button("Add Email"):
                    if '@' in new_email:  # Basic validation
                        # Check if email already exists
                        if new_email.lower() in st.session_state.df_unsubscribed['email'].str.lower().values:
                            st.warning(f"Email {new_email} is already in the unsubscribe list.")
                        else:
                            # Get current timestamp
                            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            # Prepare new row with same columns as existing dataframe
                            new_row = pd.DataFrame({
                                'email': [new_email.lower().strip()],
                                'reason': ["Added via debug page"],
                                'timestamp': [timestamp]
                            })
                            
                            # Append to the dataframe
                            st.session_state.df_unsubscribed = pd.concat([st.session_state.df_unsubscribed, new_row], ignore_index=True)
                            
                            # Save updated dataframe
                            try:
                                st.session_state.df_unsubscribed.to_csv("unsubscribed_users.csv", index=False)
                                st.success(f"Successfully added {new_email} to unsubscribe list!")
                                
                                # Try to save to the additional locations
                                save_unsubscribed_users_to_all_locations(st.session_state.df_unsubscribed)
                            except Exception as e:
                                st.error(f"Error saving changes: {e}")
                    else:
                        st.error("Please enter a valid email address.")
                
                # Text area for bulk email addition
                bulk_emails = st.text_area("Or enter multiple emails (one per line):")
                
                if bulk_emails and st.button("Add All Emails"):
                    # Process the bulk emails
                    emails_list = [email.strip() for email in bulk_emails.split('\n') if email.strip()]
                    valid_emails = [email for email in emails_list if '@' in email]
                    
                    if valid_emails:
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Create DataFrame for new emails
                        new_rows = pd.DataFrame({
                            'email': [email.lower().strip() for email in valid_emails],
                            'reason': ["Bulk added via debug page"] * len(valid_emails),
                            'timestamp': [timestamp] * len(valid_emails)
                        })
                        
                        # Remove any duplicates with existing data
                        existing_emails = set(st.session_state.df_unsubscribed['email'].str.lower())
                        new_rows = new_rows[~new_rows['email'].str.lower().isin(existing_emails)]
                        
                        if not new_rows.empty:
                            # Append to the dataframe
                            st.session_state.df_unsubscribed = pd.concat([st.session_state.df_unsubscribed, new_rows], ignore_index=True)
                            
                            # Save updated dataframe
                            try:
                                st.session_state.df_unsubscribed.to_csv("unsubscribed_users.csv", index=False)
                                st.success(f"Successfully added {len(new_rows)} new email(s) to unsubscribe list!")
                                
                                # Try to save to the additional locations
                                save_unsubscribed_users_to_all_locations(st.session_state.df_unsubscribed)
                            except Exception as e:
                                st.error(f"Error saving changes: {e}")
                        else:
                            st.info("No new unique emails to add.")
                    else:
                        st.error("No valid email addresses found.")
            
            with tab4:
                st.write("Upload a CSV file with emails to append to the unsubscribe list:")
                
                uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
                
                if uploaded_file is not None:
                    try:
                        # Read the uploaded file
                        uploaded_df = pd.read_csv(uploaded_file)
                        
                        # Display the uploaded data
                        st.write("Uploaded data preview:")
                        st.dataframe(uploaded_df.head())
                        
                        # Determine which column contains emails
                        email_column = None
                        
                        # Check if 'email' column exists
                        if 'email' in uploaded_df.columns:
                            email_column = 'email'
                        else:
                            # Try to find a column that might contain emails
                            for col in uploaded_df.columns:
                                if uploaded_df[col].dtype == 'object' and uploaded_df[col].str.contains('@').any():
                                    email_column = col
                                    break
                        
                        if email_column:
                            st.write(f"Using column '{email_column}' for email addresses.")
                            
                            # Process button
                            if st.button("Process Upload & Append"):
                                # Extract valid emails
                                valid_emails = uploaded_df[email_column].dropna().astype(str)
                                valid_emails = valid_emails[valid_emails.str.contains('@')]
                                
                                if not valid_emails.empty:
                                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    
                                    # Create DataFrame for new emails
                                    new_rows = pd.DataFrame({
                                        'email': [email.lower().strip() for email in valid_emails],
                                        'reason': ["Imported via CSV upload"] * len(valid_emails),
                                        'timestamp': [timestamp] * len(valid_emails)
                                    })
                                    
                                    # Remove any duplicates with existing data
                                    existing_emails = set(st.session_state.df_unsubscribed['email'].str.lower())
                                    new_rows = new_rows[~new_rows['email'].str.lower().isin(existing_emails)]
                                    
                                    if not new_rows.empty:
                                        # Append to the dataframe
                                        st.session_state.df_unsubscribed = pd.concat([st.session_state.df_unsubscribed, new_rows], ignore_index=True)
                                        
                                        # Save updated dataframe
                                        try:
                                            st.session_state.df_unsubscribed.to_csv("unsubscribed_users.csv", index=False)
                                            st.success(f"Successfully imported {len(new_rows)} new email(s)!")
                                            
                                            # Try to save to the additional locations
                                            save_unsubscribed_users_to_all_locations(st.session_state.df_unsubscribed)
                                        except Exception as e:
                                            st.error(f"Error saving changes: {e}")
                                    else:
                                        st.info("No new unique emails to add.")
                                else:
                                    st.error("No valid email addresses found in the uploaded file.")
                        else:
                            st.error("Could not identify a column containing email addresses.")
                    except Exception as e:
                        st.error(f"Error processing CSV file: {e}")
        else:
            st.info("unsubscribed_users.csv not found. Creating a new file.")
            
            # Create a new DataFrame with required columns
            df = pd.DataFrame(columns=['email', 'reason', 'timestamp'])
            
            # Save it to create the file
            df.to_csv("unsubscribed_users.csv", index=False)
            
            # Add to session state
            st.session_state.df_unsubscribed = df.copy()
            
            # Reload the page to show the new file
            st.rerun()
        
        # Function to check and download files
        st.header("File Actions")
        if st.button("Download unsubscribed_users.csv"):
            if csv_exists:
                csv_data = st.session_state.df_unsubscribed.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="unsubscribed_users.csv",
                    mime="text/csv"
                )
            else:
                st.error("File does not exist")
        
        return
    
    # Get path from URL using the non-experimental API
    url_path = st.query_params.get("page", [""])[0]
    
    # Check if this is an unsubscribe request
    if "unsubscribe" in st.query_params:
        handle_unsubscribe()
        return
    
    # Also check for /unsubscribe in the URL path directly
    if url_path == "unsubscribe":
        handle_unsubscribe()
        return
    
    # If no special page is requested, display the main app
    # CSS for enhanced styling with increased spacing
    st.markdown(
        """
        <style>
        body {
            background-color: #f5f5f5;
            font-family: Arial, sans-serif;
        }
        # Rest of your CSS...
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Rest of your main function...

# Helper function to save unsubscribed users to all locations
def save_unsubscribed_users_to_all_locations(df):
    """Save the unsubscribed users DataFrame to all locations for the email script."""
    try:
        # Save to original location
        df.to_csv("unsubscribed_users.csv", index=False)
        
        # Additional locations from the email script
        mac_paths = [
            os.path.expanduser('~/Documents/Python/unsubscribed_users.csv'),
            os.path.expanduser('~/unsubscribed_users.csv'),
            '/tmp/unsubscribed_users.csv'
        ]
        
        for path in mac_paths:
            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
                # Copy the file
                df.to_csv(path, index=False)
            except Exception:
                continue
                
        # Export to JSON format as well
        json_data = df.to_json(orient='records')
        with open('unsubscribed_users.json', 'w') as f:
            f.write(json_data)
            
        # Also try to save JSON to Python folder
        json_path = os.path.expanduser('~/Documents/Python/unsubscribed_users.json')
        try:
            os.makedirs(os.path.dirname(json_path) or '.', exist_ok=True)
            with open(json_path, 'w') as f:
                f.write(json_data)
        except:
            pass
            
        return True
    except Exception as e:
        st.error(f"Error saving to multiple locations: {e}")
        return False
    
    # Get path from URL using the non-experimental API
    url_path = st.query_params.get("page", [""])[0]
    
    # Check if this is an unsubscribe request
    if "unsubscribe" in st.query_params:
        handle_unsubscribe()
        return
    
    # Also check for /unsubscribe in the URL path directly
    if url_path == "unsubscribe":
        handle_unsubscribe()
        return
    
    # Check if this is an admin panel request
    if url_path == "admin":
        show_admin_page()
        return
    
    # If no special page is requested, display the main app

    # CSS for enhanced styling with increased spacing
    st.markdown(
        """
        <style>
        body {
            background-color: #f5f5f5;
            font-family: Arial, sans-serif;
        }
        .navbar {
            position: sticky;
            top: 0;
            z-index: 1000;
            background-color: #333;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            color: white;
        }
        .navbar a {
            color: white;
            text-decoration: none;
            margin: 0 10px;
        }
        .navbar a:hover {
            text-decoration: underline;
        }
        .section {
            padding: 70px 20px;  /* Increased padding for more internal spacing */
            margin-bottom: 40px;  /* Added margin-bottom for spacing between sections */
        }
        .card {
            background-color: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 20px 0;
        }
        .hero {
            text-align: center;
            color: white;
            padding: 120px 20px;  /* Increased padding for a taller hero section */
            background-size: cover;
            background-position: center;
        }
        .hero h1 {
            font-size: 3em;
        }
        .footer {
            background-color: #333;
            color: white;
            padding: 30px;
            text-align: center;
            margin-top: 50px;  /* Added margin-top for spacing above footer */
        }
        .spacer {
            height: 40px;  /* Custom spacer class for additional control */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Navigation Bar
    st.markdown(
        """
        <div class="navbar">
            <a href="#">Home</a>
            <a href="#features">Features</a>
            <a href="#support">Support</a>
            <a href="#how-it-works">How It Works</a>
            <a href="#about">About Us</a>
            <a href="#pricing">Pricing</a>
            <a href="#contact">Contact</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Convert the hero image to base64
    try:
        hero_image_base64 = "data:image/jpeg;base64," + image_to_base64("hero_image.jpg")
    except:
        # Fallback if image can't be loaded
        hero_image_base64 = ""
        
    # Hero Section with embedded image
    if hero_image_base64:
        st.markdown(
            f"""
            <style>
            .hero {{
                text-align: center;
                color: white;
                padding: 120px 20px;
                background-image: url({hero_image_base64});
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            </style>
            <div class="hero">
                <h1>Welcome to CellAI</h1>
                <p>Empowering Biological Discovery with Automated ROI Selection</p>
                <p>CellAI harnesses the power of artificial intelligence to transform fluorescence microscopy analysis, delivering unparalleled speed, precision, and simplicity to researchers worldwide.</p>
                <button style="padding: 15px 30px; font-size: 18px; background-color: #ff6347; color: white; border: none; border-radius: 5px; cursor: pointer;">Get Started Today</button>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Fallback if image can't be loaded
        st.title("Welcome to CellAI")
        st.write("Empowering Biological Discovery with Automated ROI Selection")
        st.write("CellAI harnesses the power of artificial intelligence to transform fluorescence microscopy analysis, delivering unparalleled speed, precision, and simplicity to researchers worldwide.")
        st.button("Get Started Today")

    # Spacer after Hero
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

    # Introductory Section
    st.markdown(
        """
        <section class="section" style="background-color:#f7d9d9;">
            <div class="card">
                <h3>Revolutionizing Fluorescence Microscopy with CellAI</h3>
                <p>For researchers in biology and biomedical sciences, analyzing fluorescence microscopy images can be a daunting task. Hours spent manually annotating regions of interest (ROIs) in tools like ImageJ detract from the real work of scientific discovery. Enter CellAI—a game-changing solution that automates ROI selection with cutting-edge AI and machine learning technology.</p>
                <p>Our mission is simple: to save you time, improve your accuracy, and let you focus on what matters most—unlocking the secrets of cellular behavior. Whether you're studying protein localization, cell morphology, or dynamic processes in living cells, CellAI streamlines your workflow by identifying and mapping fluorescent regions of interest with unmatched efficiency. Say goodbye to tedious manual labeling and hello to a smarter, faster way to process your image datasets.</p>
                <p>Built by a team of experts in computer vision, machine learning, and biological research, CellAI integrates seamlessly with ImageJ, the gold standard in microscopy image analysis. Our service is tailored specifically for fluorescence microscopy data, ensuring that your unique research needs are met with precision and care.</p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    # Spacer after Intro
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

    # Features Section
    st.markdown("<a id='features'></a>", unsafe_allow_html=True)
    st.markdown("### Why Choose CellAI? Discover the Benefits")

    col1, col2 = st.columns([2, 3])
    with col1:
        try:
            st.image("draganddrop.png", caption="Save Time with Automation", use_container_width=True)
            st.image("micro_man.png", caption="Increase Precision in Analysis", use_container_width=True)
        except:
            st.write("Images not available")
            
    with col2:
        st.markdown(
            """
            <div class="card">
                <h4>A Smarter Approach to Image Segmentation</h4>
                <p>Fluorescence microscopy generates vast amounts of data, and manually selecting regions of interest can take hours—or even days—depending on the complexity of your dataset. CellAI changes that by leveraging state-of-the-art computer vision algorithms to automate the process. Our AI-powered segmentation tool identifies fluorescent regions with pinpoint accuracy, drawing ROI polygons that are ready to use in ImageJ. This not only speeds up your workflow but also ensures consistency across your analyses, eliminating the variability that comes with human annotation.</p>
                <p>But CellAI is more than just a time-saver. Our models are trained on diverse fluorescence microscopy datasets, enabling them to detect subtle variations in intensity and structure that might be missed by the human eye. Whether you're working with fixed cells, live-cell imaging, or multi-channel fluorescence, CellAI delivers reliable, reproducible results that enhance the quality of your research.</p>
                <p>We've designed CellAI with accessibility in mind. You don't need to be a computational expert to use it—just upload your images, and let our intuitive platform do the rest. From graduate students to seasoned principal investigators, CellAI empowers researchers at all levels to integrate advanced image analysis into their work without a steep learning curve.</p>
                <ul>
                    <li><strong>Save Time:</strong> Process entire datasets in minutes, not hours, with automated ROI selection tailored for fluorescence microscopy.</li>
                    <li><strong>Increase Precision:</strong> Achieve consistent, high-accuracy segmentation that captures even the finest details of your fluorescent images.</li>
                    <li><strong>User-Friendly:</strong> Enjoy a seamless interface designed for biologists, not just coders, with no advanced technical skills required.</li>
                    <li><strong>Scalable Solution:</strong> Handle small experiments or massive datasets with ease—CellAI grows with your research needs.</li>
                    <li><strong>Seamless Integration:</strong> Export ROIs directly into ImageJ for further analysis, fitting perfectly into your existing workflow.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Footer Section
    st.markdown("<a id='contact'></a>", unsafe_allow_html=True)
    st.markdown(
        """
        <footer class="footer">
            <p>CellAI is committed to accelerating scientific discovery through innovation.</p>
            <p>For support, inquiries, or partnership opportunities, reach out at <a href="mailto:cell.ai.solutions@gmail.com" style="color: lightblue;">cell.ai.solutions@gmail.com</a>.</p>
            <p>Stay connected with us on <a href="#" style="color: lightblue;">Twitter</a>, <a href="#" style="color: lightblue;">LinkedIn</a>, and <a href="#" style="color: lightblue;">GitHub</a> for updates, tips, and community resources.</p>
            <p><a href="?unsubscribe=true" style="color: lightblue;">Unsubscribe from emails</a></p>
            <p>© 2025 CellAI Solutions. All rights reserved.</p>
        </footer>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
