# Parcelmasters

## Overview
This Courier App is a simple courier management system built with Django, designed to streamline the courier service process. It provides a comprehensive platform for managing deliveries, tracking packages, and optimizing routes for efficient logistics.

## Features
1. User Registration: Users can register their accounts in the system. During the registration process, users will be assigned a unique tracking number that can be used to track their deliveries.

2. Pricing Calculation: The system automatically calculates the pricing for each delivery based on the distance between the pickup and delivery locations. The pricing is determined using a predefined pricing model that takes into account the distance traveled.

3. Distance Calculation: The system utilizes a distance calculation algorithm to determine the distance between the pickup and delivery locations. This ensures accurate pricing and allows users to estimate delivery times.


## Technologies Used
- Django: Python web framework
- SQLite: Relational database management system
- JavaScript, HTML, CSS: Frontend development
- Bootstrap: CSS framework for responsive design


## Installation
1. Clone the repository: `git clone https://github.com/neo77-cyber/ Rocket-Speed-Express.git`
2. Navigate to the project directory: `cd parcelcourier`
3. Create a virtual environment: `pipenv shell`
5. Install dependencies: `pipenv install -r requirements.txt`
6. Set up environment variables: Configure the necessary environment variables (database credentials, API keys, etc.) in a `.env` file or your preferred method.
7. Apply database migrations: `python manage.py migrate`
8. Start the development server: `python manage.py runserver`
9. Access the app in your browser at `http://localhost:8000`

## Usage
- Explore the intuitive user interface to manage packages, track deliveries, and access additional features.


## Contributing
Contributions to the Courier App are welcome! If you encounter any issues or have suggestions for improvements, please submit an issue or a pull request to the GitHub repository.

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to modify and distribute this code as per the terms of the license.

## Contact
For any inquiries or questions, please contact the project maintainers:
- Enabulele Ikponmwosa: ikponmwosaenabs@gmail.com

