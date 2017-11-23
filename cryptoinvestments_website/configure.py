from flask import Flask

app= Flask(__name__, static_folder="./static")
app.secret = "something_you_will_never_guess"
from app import views