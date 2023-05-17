# AirScan 
# ![My Skills](https://skillicons.dev/icons?i=py,django,javascript,html,bootstrap,postgresql,docker,git,github)

Welcome to the AirScan! Airscan is an demo web application, that allows to read several types of data related to aviation.

## Application features:
- Scanning current flights above selected area.
- Overview of information related to current flights.
- Overview of information related to aircrafts.
- Overview of information related to airports.

## Features overview:
1. Project information
![1](https://github.com/marataj/AirScan/assets/96992545/835ccea7-9b9f-4fef-85e6-75b49b2ec544)
2. Scanning current flights above selected area
![2](https://github.com/marataj/AirScan/assets/96992545/908b5923-9aa1-4c3c-86f5-341ba2266e63)
![3](https://github.com/marataj/AirScan/assets/96992545/fa1725f6-1180-410e-a3b3-ccff586a4c5e)
![4](https://github.com/marataj/AirScan/assets/96992545/aeeeb0cd-2e05-44af-a445-ecaab7fd88a1)
3. Detailed flight information
![5](https://github.com/marataj/AirScan/assets/96992545/c0007c30-8cfb-4d60-ad7f-46062143852d)
![6](https://github.com/marataj/AirScan/assets/96992545/900f50b9-6ca0-4be4-bfae-d429ea11a950)
4. Detailed airports information
![7](https://github.com/marataj/AirScan/assets/96992545/20cc5c8c-ad70-481a-bb8e-677356584c7e)
5. Showing history of flights to/from selected airport
![8](https://github.com/marataj/AirScan/assets/96992545/f21a524b-a329-4ba2-a562-e0962bd22d11)
6. Showing airports on selected area
![9](https://github.com/marataj/AirScan/assets/96992545/9a1d2c51-e17d-42b3-9976-12a72597e8e2)
7. Searching for detailed information about aircrafts
![10](https://github.com/marataj/AirScan/assets/96992545/d30a20c2-8a9c-44d9-823e-ebcb1fb7d033)
![11](https://github.com/marataj/AirScan/assets/96992545/251ef92d-ca86-449d-a3b4-6adc4a89955a)
8. User authentication and favorites list
![12](https://github.com/marataj/AirScan/assets/96992545/afa393f5-a73b-4313-bee2-bc5600625fc0)


## How to start:
1. Start postgresql docker container based on Dockerfile (you can edit DB password and name in Dockerfile)
2. Build dev environment, using pip install -r requirements.txt
3. Sing up to OpenSky Network site
4. Complete django secret key, OpenSky Network credentials and DB settings in AirScan/.env file, which is the project config file.
5. Use python manage.py makemigrations ; ... migrate , to setup database
6. Use commands below to fill DB with initial data:
    - python manage.py fill_airplanes
    - python manage.py fill_airports_data
    - python manage.py fill_destinations
7. Use python manage.py runserver to run development server
## Data sources:
- ### [OpenSky Network](https://opensky-network.org/)
  ![opensky_logo](https://user-images.githubusercontent.com/96992545/236922599-f49264db-301b-4e11-b430-0599bf9d3a61.png)
  
  Flights data are provided from the OpenSky Network. The OpenSky Network provides REST API, that allows to retrieve multiple information related to aviation.

- ### [Planespotters](https://www.planespotters.net/)
  ![download](https://user-images.githubusercontent.com/96992545/236923198-099d0c60-fbcf-44a1-9801-6147648760e0.png)
  
  Photos of aircrafts are provided from the Planespotters application. The Planespotters provides REST API, that provides photos of aircrafts.

## Contributing :octocat:
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
