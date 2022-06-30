# importing function. We can do this beacuse 'website' folder has an __init__
from website import create_app, limiter


app = create_app()
limiter.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)