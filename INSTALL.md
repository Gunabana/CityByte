## Quick Start

#### 1. Clone the repository:  

```
git clone https://github.com/rohitgeddam/CityByte.git
```


#### 2. Setup the virtual environment:

```
python -m venv venv
```


#### 3. Activate the virtual environment:  
On Mac/Linux: 
```
source venv/bin/activate
```
      
On Windows: 
```
venv\Scripts\activate
```
   

#### 4. Install required modules and libraries:  

```
pip install -r requirements.txt
```


#### 5a. Create .env file at ./CityByte using the below template.
   
```
GEODB_X_RAPID_API_KEY=""
GEODB_X_RAPID_API_HOST=""
AMADEUS_API_KEY=""
AMADEUS_API_SECRET_KEY=""
UNSPLASH_API_KEY=""
FOURSQUARE_API_KEY=""
WEATHER_BIT_X_RAPID_API_KEY=""
WEATHER_BIT_X_RAPID_API_HOST=""
```
Create an account in the below websites to Fetch API keys and use them in the above template.  
* [GeoDB Cities API](https://rapidapi.com/wirefreethought/api/geodb-cities/details)
* [Weather API](https://rapidapi.com/weatherbit/api/weather)
* [Amadeus API](https://developers.amadeus.com/)
* [Unsplash API](https://unsplash.com/developers)
* [Foursquare API](https://location.foursquare.com/developer/)  

#### 5b. Register your Google OAuth 2.0 Client IDs following the steps below.
1. Log in to https://console.cloud.google.com
2. Create a new Project
3. Navigate to APIs & Services
4. Select "Create Credential" > "OAuth client ID"
5. For the application type, choose "Web application" and enter a name for it
6. For authorized JavaScript origins, enter "http://localhost", "http://localhost:8000", and "http://127.0.0.1:8000"
7. For authorized redirect URIs, enter "http://localhost:8000/auth-receiver"
8. After this, you will be shown your Client ID and Client secret
9. Add `GOOGLE_OAUTH2_ID=""` and `GOOGLE_OAUTH2_SECRET=""` to the .env file with the Client ID and Client secret within their respective quotes
10. Add the Client ID to `data-client_id=""` in login.html
11. Follow <a href="https://developers.google.com/maps/get-started#create-project"> the guide </a> for registering for Google Maps API access. (While it does require credit
card registration, they will not let you exceed the free limit unless you prepay
or enable charges to your account; the free version allows $200 in credit each month)
12. Add `GOOGLE_API_KEY=""` to the .env file with the new API key

#### 6. Set-up REDIS
* Follow the instructions in [Getting Started](https://redis.io/docs/getting-started/) to Install Redis in your local environment.
* Start the Redis Server: Open a terminal and run the following command:
```
   redis-server
```
* Open another terminal to start the REDIS CLI:
```
   redis-cli
```

Now, you can run the application.
#### 7. Run the application:  
``` 
python manage.py migrate
python manage.py runserver
```

#### 8. Success!
The server starts at http://127.0.0.1:8000
