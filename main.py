# importing function. We can do this beacuse 'website' folder has an __init__
from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)