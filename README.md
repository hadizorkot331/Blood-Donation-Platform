# Blood Donation Platform
#### This is a platform where patients can request blood and receive donations in the fastest and simplest way possible.

### Features

- Notifications. We utilize the Whatsapp API and the SMTP API to send out emails to eligible donors and spread the word on our Whatsapp group where messages are sent when new posts are added.
- Directions and Contact. Using the Google Places API, Google Place Details API, and Whatsapp API, users can get directions to the necessary hospital. Users can also contact the hospital by Phone or via their website, as well as contact the patient by Phone or via Whatsapp.
- All hospital coverage. Hospital data is collected from the Ministry of Public Health, ensuring that all hospitals of lebanon are covered and available.
- Anonymous Browsing. Users can browse the homepage without having to login or register.
- Full Mobile compatibility. Our website is designed to be used on all devices with ease in order to ensure that patients can request blood with ease from anywhere they might be.

### Setup
#### To run the site on your machine:
- Install the dependencies from requirements.txt
- Setup environment variables for `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `GOOGLE_API_KEY`, `SECRET_KEY`, `WHATSAPP_API_KEY`, and `HOST`. For obvious reasons, the API keys are not uploaded to github, therefore you will need to provide your own. The `SECRET_KEY` is the django secret key and `HOST` is the url that the site will be hosted on, in localhost case, you can use `127.0.0.1:8000`
- Run `python manage.py makemigrations` to make the migrations to the database.
- Run `python manage.py migrate` to apply the migrations.
- Run `python manage.py runserver` to run the server.

## Contact the devs
*_Backend_* : hadizorkot.hadi@gmail.com

*_Frontend_* : malekbahr55@gmail.com