import subprocess
import os

def run():
    # Launch the Streamlit app.
    # Assumes the correct environment is already activated.
    
    #app_path = os.path.join("PYTHON_CODE", "app.py")
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    
    try:
        subprocess.run(["streamlit", "run", app_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error launching Streamlit: {e}")
    except FileNotFoundError:
        print("Streamlit is not installed or not available in the current environment.")