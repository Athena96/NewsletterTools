import os
import webbrowser
import subprocess
import sys
from lib.newsletter import Newsletter
from dotenv import load_dotenv

'''
# Usage
python3 src/create.py <newsletter_number>

# Description
1. create the boilerplate HTML Newsletter file at the directory specicied in the .env file `newsletter_local_dir`
2. open the HTML file in VS code
3. open the HTML file in Chrome
'''

load_dotenv()

newsletter = Newsletter()

# create the HTML content
arguments = sys.argv

if len(arguments) < 2:
    raise Exception("\n\nPlease provide a newsletter number e.g.:\n\npython3 src/create.py 33\n\n")

number = f"{arguments[1]}"
html_content = f"""
<!DOCTYPE html>
<html>

<head>
    <style>
        /* body {{
            background-color: powderblue;
        }} */
        
        h1,
        h2,
        h3,
        h4,
        p,
        li {{
            font-family: "Helvetica Neue";
            margin: 15px 0;
        }}
        
        .center {{
            margin-left: 50px;
            margin-left: 50px;
            margin-right: 50px;
        }}
    </style>
</head>

<body>

    <h1 style="font-size:65px">The Jared Franzone Newsletter #{number}</h1>
    <p style="color:grey"><b>Friday {newsletter.month}/{newsletter.day}/{newsletter.year}</b> - Seattle, WA - <i>(sent on the last Friday of every
            month)</i><br /><a target="_blank " href="https://www.jaredfranzone.com/">jaredfranzone.com</a></p>
    <hr>
    </br>
    </br>
    <div class="center">


        <h1><a target="_blank " href="https://link.com">(emoji) Bullet Title</a></h1>
        <p>
                paragraph 1
        </p>

        <p>
                paragraph 2
        </p>



        <h1><a target="_blank " href="https://link.com">(emoji) Bullet Title</a></h1>
        <p>
                paragraph 1
        </p>

        <p>
                paragraph 2
        </p>




        <h1><a target="_blank " href="https://link.com">(emoji) Bullet Title</a></h1>
        <p>
                paragraph 1
        </p>

        <p>
                paragraph 2
        </p>

        <h3>Quote:</h3>

        <p>
            <i>"Creation is a better means of self expression than possession; it is through creating, not possessing, that life is revealed."</i> </br>- <b>Vida D. Scudder</i></b>
            <p>

                <p>

                </p>


                <p>
                </p><br />

                <hr />
                <h3>Also!</h3>
                <p>
                    Feel free to reply to this email (only I will get the reply) if you have any thoughts, questions, comments, or recommendations for me, I would love to hear from you, thanks for reading!
                </p>
                <p>
                </p><br />
    </div>
</body>

</html>
"""

# Write the HTML content to a file
newsletter_local_dir = os.getenv('newsletter_local_dir')
file_path = newsletter_local_dir + newsletter.filename + '.html'
with open(file_path, 'w') as file:
    file.write(html_content)

print(f"HTML file '{newsletter.filename}.html' created at '{file_path}'.")

# Open the file in VS Code
print(f"Opening the file in VS Code...")
subprocess.run(["code", file_path])

# Open the file in Chrome
print(f"Opening the file in Chrome...")
webbrowser.open(file_path)

# print option to delete the file
print(f"Created by accident? Delete the file with:")
print(f"rm {file_path}")

# Print next command to run:
print(f"Otherwise... here's the next command to run:\n\n")
print(f"python3 src/test.py")
