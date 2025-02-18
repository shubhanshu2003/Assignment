from flask import Flask
import datetime
import os
import subprocess

app = Flask(__name__)

@app.route('/htop')
def htop_view():
    now = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))  # IST
    name = "Your Full Name"  # Replace with your actual name
    username = os.getenv('USER', 'Unknown')  # More reliable than os.getlogin()
    server_time = now.strftime("%Y-%m-%d %H:%M:%S IST")

    try:
        top_output = subprocess.check_output(['top', '-b', '-n', '1']).decode()  # Batch mode, 1 iteration
    except FileNotFoundError:
        top_output = "top command not found. Please install it (sudo apt-get install procps)."
    except subprocess.CalledProcessError as e:
        top_output = f"Error executing top: {e}"
    except Exception as e:
        top_output = f"An unexpected error occurred: {e}"

    html = f"""
    <html>
    <head>
        <title>HTOP Data</title>
    </head>
    <body>
        <h1>HTOP Data</h1>
        <p>Name: {name}</p>
        <p>Username: {username}</p>
        <p>Server Time (IST): {server_time}</p>
        <pre>{top_output}</pre>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  
