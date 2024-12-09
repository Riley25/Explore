import subprocess
import os

def launch_streamlit():
    """
    Launch the Streamlit app.
    Assumes the correct environment is already activated.
    """
    app_path = os.path.join("EXPLORE", "app.py")
    
    try:
        subprocess.run(["streamlit", "run", app_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error launching Streamlit: {e}")
    except FileNotFoundError:
        print("Streamlit is not installed or not available in the current environment.")

if __name__ == "__main__":
    launch_streamlit()


