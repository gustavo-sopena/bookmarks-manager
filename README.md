# bookmarks-manager

This project is created for the Coding with Lewis Hackathon.

## Getting Started

At the time of writing, the project used Python version 3.12.4.

Create a virtual environment with Python. The name can be anything. In this case, it is “hackathon”.
```zsh
python -m venv hackathon
```

Activate the virtual environment by using the suitable activate script found in the folder created. The virtual environment can be deactivated by using the command: deactivate
```zsh
source ./hackathon/bin/activate
```

Next, install all of the required packages. These are needed to run the website.
```zsh
pip install -r requirements.txt
```

Execute the following command to get the database initialized.
```zsh
flask –app bookmarks_manager init_db
```

Execute the following command to get the website running.
```zsh
flask --app bookmarks_manager run
```
