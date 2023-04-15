# Nots

This is a simple Flask web application that allows you to create notes with markdown support. The app also includes basic authentication to protect your notes with a username and password.

<p ALIGN="center"><img src="https://raw.githubusercontent.com/ayxkaddd/nots/main/static/favicon.ico" width="90" height="90"></p>

# Configuration

Before running the app, you'll need to fill in the values in config.py. Here are the variables you'll need to set:

- `profile`: A dictionary that contains the following keys:
    - `USERNAME`: The username that will be displayed on the index page
    - `ICON_PATH`: The path to your profile image
- `AUTH_USERNAME`: The username to use for authentication
- `AUTH_PASSWORD`: The password to use for authentication

You will also need to install dependencies by running 
```pip install -r requirements.txt```

# Usage 

Once you have filled in the configuration variables, you can run the app using the following command:

```python app.py```

This will start the Flask development server, and you can access the app by navigating to `http://localhost:5000` in your web browser.

On the index page, you can create a new note by clicking the "Add Note" button. You can also edit or delete existing notes by clicking the corresponding buttons next to each note.

When creating or editing a note, you can use markdown syntax to format your text. Your notes will be saved as `.md` files in the `notes` directory.

# Security

Note that the basic authentication provided by this app is not secure enough for production use. If you plan to deploy this app to a public server, you should use a more robust authentication mechanism, such as OAuth or JWT.

# Contributing

If you find a bug or have a feature request, feel free to open an issue or submit a pull request on GitHub.
