import os

CURRENTDIR = os.path.dirname(os.path.abspath(__file__))
HTMLDIR = os.path.join(CURRENTDIR, "static", "html")

TRELLO_API_URL = "https://api.trello.com/1/"
BOARD_ID = "" # The ID of the board to track (find it in the URL of your board)

# TODO: Could build something into the app to guide the user through generating these values
API_KEY = "" # Your trello api key (from https://trello.com/1/appKey/generate)
USER_TOKEN = "" # See http://www.trello.org/help.html ("Getting a Token from a User")

NOT_DONE_LISTS = ("To Do", "Doing")
DONE_LISTS = ("Done")

DATABASE_URI = "sqlite:///%s" % os.path.join(CURRENTDIR, "spark.db")