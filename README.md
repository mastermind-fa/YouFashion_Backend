# YouFashion - Clothing Store Backend

## Overview

YouFashion is a Django Rest Framework-based backend for a clothing store. It provides essential functionalities such as user authentication, product management, cart and wishlist features, and a seamless payment experience using SSLCommerz.

## Features

- **User Authentication:**
  - User registration with email confirmation.
  - User login/logout functionality.
- **Product Management:**
  - Only admin users can add new products.
  - Update or delete product quantity.
- **Cart & Wishlist:**
  - Users can add products to their cart.
  - Users can add products to their wishlist.
- **Payments:**
  - SSLCommerz integration for secure payments.
- **Filtering & Sorting:**
  - Products can be filtered and sorted by price and popularity.

## Technologies Used

- **Backend:** Django Rest Framework
- **Database:** PostgreSQL
- **Authentication:** JWT Authentication
- **Payments:** SSLCommerz
- **Deployment:** Secure hosting platform

## Installation & Setup

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- PostgreSQL
- Virtual Environment (optional but recommended)

### Steps to Run the Project

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/mastermind-fa/YouFashion_Backend.git
   cd YouFashion_Backend
   ```
2. **Create & Activate Virtual Environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate  # For Windows
   ```
3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set Up Environment Variables:**
   - Create a `.env` file in the project root directory and add the following:
     ```sh
     SECRET_KEY=<your-generated-secret-key>
     DB_NAME=<your-database-name>
     DB_USER=<your-database-user>
     DB_PASSWORD=<your-database-password>
     DB_HOST=<your-database-host>
     DB_PORT=<your-database-port>
     EMAIL=<your-email>
     PASSWORD=<your-email-app-password>
     SUCCESS_URL=http://127.0.0.1:8000/order.html
     CANCEL_URL=http://127.0.0.1:8000/cart.html
     FAIL_URL=http://127.0.0.1:8000/cart.html
     ```
   - To generate a new Django secret key, run:
     ```sh
     python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
     ```
5. **Apply Migrations:**
   ```sh
   python manage.py migrate
   ```
6. **Create a Superuser (Admin):**
   ```sh
   python manage.py createsuperuser
   ```
7. **Run the Development Server:**
   ```sh
   python manage.py runserver
   ```

## API Endpoints

### Base URL: `http://127.0.0.1:8000/`

| Endpoint                                 | Method | Description                                  |
| ---------------------------------------- | ------ | -------------------------------------------- |
| `/customer/list/`                        | GET    | Fetch all customers                          |
| `/customer/login/`                       | POST   | User login (JSON format)                     |
| `/customer/logout/`                      | POST   | User logout                                  |
| `/customer/register/`                    | POST   | Register a new user                          |
| `/customer/details/<userID>/`            | GET    | Fetch user details                           |
| `/products/list/`                        | GET    | Get all products, filter by price/popularity |
| `/products/list/<id>/`                   | GET    | Get details of a single product              |
| `/products/reviews/list/?productID`      | GET    | Get all reviews of a product                 |
| `/products/reviews/`                     | POST   | Post a review                                |
| `/order/cart/`                           | POST   | Add product to cart                          |
| `/order/cart/`                           | GET    | Get cart data                                |
| `/order/cart/`                           | PUT    | Update cart quantity                         |
| `/order/cart/<productID>/`               | DELETE | Remove product from cart                     |
| `/products/wishlist/`                    | POST   | Add product to wishlist                      |
| `/products/wishlist/`                    | GET    | Get wishlist data                            |
| `/products/wishlist/remove/<productID>/` | DELETE | Remove product from wishlist                 |
| `/order/orders/`                         | GET    | Get previous orders of user                  |
| `/payment/sslcommerz/`                   | POST   | Process payment with SSLCommerz              |

## Contribution

Contributions are welcome! Feel free to fork the repo and submit a pull request.

## License

This project is licensed under the MIT License.

---

Developed by **Farhana Alam**
