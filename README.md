# E-commerce Negotiation App

This is a Flask-based web application where users can browse products, negotiate prices with a chatbot (either text-based or voice-based), and complete their purchases. Users can also post reviews and view their order history.

## Features

1. **User Authentication**
    - Signup and Login functionalities for users.
    
2. **Browse Products**
    - Users can browse through the list of available products.

3. **Price Negotiation**
    - Users can negotiate product prices with a chatbot using either text or voice commands.

4. **Order Management**
    - Users can view their order history and complete purchases.

5. **Review System**
    - Users can post reviews for products, which are analyzed for sentiment (Positive, Negative, Neutral) using the VADER sentiment analysis tool.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/ecommerce-negotiate.git
    cd ecommerce-negotiate
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    - Create a MySQL database named `negotiate` and import the necessary tables. Use the following commands to create and import tables:

    ```sql
    CREATE DATABASE negotiate;
    USE negotiate;

    -- Create `users` table
    CREATE TABLE users (
        username VARCHAR(50) PRIMARY KEY,
        password VARCHAR(50),
        contact_no VARCHAR(15),
        emailid VARCHAR(50),
        address VARCHAR(100),
        gender VARCHAR(10)
    );

    -- Create `purchaseorder` table
    CREATE TABLE purchaseorder (
        username VARCHAR(50),
        product_id VARCHAR(50),
        product_name VARCHAR(100),
        amount FLOAT,
        transaction_date DATETIME
    );

    -- Create `reviews` table
    CREATE TABLE reviews (
        username VARCHAR(50),
        review TEXT,
        sentiment VARCHAR(10)
    );
    ```

5. **Add Dataset Files:**

    - Add your `Dataset/ecommerce.csv` and `Dataset/model.csv` files to the `Dataset` directory. Ensure they are formatted correctly according to your application's requirements.

6. **Run the application:**

    ```bash
    python app.py
    ```

    The application will be available at `http://127.0.0.1:5000`.

## Usage

1. **User Registration and Login:**

    - Navigate to the Signup page to create an account.
    - Login with your credentials to access the main user screen.

2. **Browse Products:**

    - Browse available products and choose to negotiate prices using either text or voice commands.

3. **Negotiate Prices:**

    - For text-based negotiation, enter the required text commands.
    - For voice-based negotiation, upload your voice commands.

4. **Complete Orders:**

    - Once satisfied with the negotiated price, complete the order.
    - View your order history on the `ViewOrders` page.

5. **Post Reviews:**

    - Post reviews for the products you purchased.
    - The sentiment of the reviews will be analyzed and displayed.

## Contributing

If you wish to contribute to the project, please fork the repository and create a pull request with your changes. Make sure to write clear commit messages and provide a detailed description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or feedback, please contact [bharadwazguthi@gmail.com](mailto:your-email@example.com).

