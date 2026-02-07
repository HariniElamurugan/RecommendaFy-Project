from flask import Flask, request, render_template  # type: ignore
import pandas as pd # type: ignore
import random
from recommendafy.utils import truncate , content_based_recommendations
from flask_sqlalchemy import SQLAlchemy # type: ignore



app = Flask(__name__)

# Loading files
trending_products = pd.read_csv("data/trending_products.csv")
train_data = pd.read_csv("data/clean_data.csv")

# database configuration---------------------------------------
app.secret_key = "alskdjfwoeieiurlskdjfslkdjf"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/ecom"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define your model class for the 'signup' table
class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Define your model class for the 'signup' table
class Signin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


# routes ----------------------------------------------------


# List of predefined image URLs
random_image_urls = [
    "static/images/img_1.png",
    "static/images/img_2.png",
    "static/images/img_3.png",
    "static/images/img_4.png",
    "static/images/img_5.png",
    "static/images/img_6.png",
    "static/images/img_7.png",
    "static/images/img_8.png",
]

@app.route("/")
def index():
    # Create a list of random image URLs for each product
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
    price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
    return render_template('index.html',trending_products = trending_products.head(8),truncate = truncate,
                           random_product_image_urls = random_product_image_urls,
                           random_price = random.choice(price))


# routes main page
@app.route("/main")
def main():
    return render_template('main.html')


# route index page
@app.route("/index")
def indexredirect():
    # Create a list of random image URLs for each product
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
    price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
    return render_template('index.html', trending_products = trending_products.head(8), truncate=truncate,
                           random_product_image_urls = random_product_image_urls,
                           random_price = random.choice(price))

# Route for signup page..
@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_signup = Signup(username=username, email=email, password=password)
        db.session.add(new_signup)
        db.session.commit()

        # Create a list of random image URLs for each product
        random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
        price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
        return render_template('index.html', trending_products=trending_products.head(8), truncate=truncate,
                               random_product_image_urls=random_product_image_urls, random_price=random.choice(price),
                               signup_message='User signed up successfully!'
                               )
    
# Route for signin page..
@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username = request.form['signinUsername']
        password = request.form['signinPassword']
        new_signup = Signin(username=username,password=password)
        db.session.add(new_signup)
        db.session.commit()

        # Create a list of random image URLs for each product
        random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
        price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
        return render_template('index.html', trending_products=trending_products.head(8), truncate=truncate,
                               random_product_image_urls=random_product_image_urls, random_price=random.choice(price),
                               signup_message='User signed in successfully!'
                               )


# Route for recommendations..
@app.route("/recommendations", methods=['POST', 'GET'])
def recommendations():
    if request.method == 'POST':
        prod = request.form.get('prod')
        nbr = int(request.form.get('nbr'))
        content_based_rec = content_based_recommendations(train_data, prod, top_n=nbr)

        if content_based_rec.empty:
            message = "No recommendations available for this product."
            return render_template('main.html', message=message)
        else:
            # Create a list of random image URLs for each recommended product
            random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
            print(content_based_rec)
            print(random_product_image_urls)

            price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
            return render_template('main.html', content_based_rec=content_based_rec, truncate=truncate,
                                   random_product_image_urls=random_product_image_urls,
                                   random_price=random.choice(price))



if __name__ == '__main__':
    app.run(debug=True)