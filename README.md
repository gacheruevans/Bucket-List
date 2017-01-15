[![Build Status](https://travis-ci.org/andela-gacheruevans/cp2-bucketlist.svg?branch=ft-implement-tests)](https://travis-ci.org/andela-gacheruevans/cp2-bucketlist)
[![Coverage Status](https://coveralls.io/repos/github/andela-gacheruevans/cp2-bucketlist/badge.svg?branch=ft-implement-tests)](https://coveralls.io/github/andela-gacheruevans/cp2-bucketlist?branch=develop)
# Bucketlist API

This application helps you log and catalog all the stuff you want to accomplish before you expire. 

##Task Description:
In this exercise I was required to create a Flask API for a bucket list service. Specification for the API is shown below.

| Endpoint                 				               		       | Functionality 						 |    
| -----------------------------------------------------------------|:-----------------------------------:|
| `POST /auth/login`         				                       |  Logs a user in                     |
| `POST /auth/register`      				                       |  Register a user                    |
| `POST /bucketlists`       				                       |  Create a new bucket list	         |
| `GET /bucketlists`						                       |  List all the created bucket lists	 | 
| `GET /bucketlists/**<bucketlists_id>**`		                   |  Get single bucket list             |                     
| `PUT /bucketlists/**<bucketlists_id>** `                         |  Update this bucket list            |                       
| `DELETE /bucketlists/**<bucketlists_id>**`				       |  Delete this single bucket list     |                              
| `POST /bucketlists/**<bucketlists_id>**/items`                   |  Create a new item in bucket list   |                                
| `PUT /bucketlists/**<bucketlists_id>**/items/**<item_id>**`      |  Update a bucket list item          |                         
| `DELETE /bucketlists/**<bucketlists_id>**/items/**<item_id>**`   |  Delete an item in a bucket list    |


##Installation
1. Create a working directory.

    mkdir Projects
    
2. Clone this repository.

    * via HTTPS

    	- https://github.com/andela-gacheruevans/cp2-bucketlist.git

    * via SSH

    	- git@github.com:andela-gacheruevans/cp2-bucketlist.git

3. Navigate to project directory.

		cd cp2-bucketlist  
    
4. Create a virtual environment.
    
    	mkvirtualenv **env** workon **env**

when selecting the virtual environment, you can pick any name that suits you for now you will be using **env**
    
5. Set up the environment requirements.
    
    	pip install -r requirements.txt


6. Initialize, migrate and update the database.
	
		python run.py db init
		python run.py db migrate
		python run.py db upgrade

7. Test the application by running the following command.
	
		tox

8. Test the application coverage by running the following command.
	
		coverage report --omit=run.py 
    
6. Run the server.
    
    	python run.py runserver

##Sample Api Use Case
Access the endpoints using your preferred client e.g Postman

- GET http://127.0.0.1:5000/api/v1/auth/login will give you the following message.
	body

		{
	  		"message": "Welcome to the BucketList API. Register a new user by 
	  		sending a POST request to /auth/register. 
	  		Login by sending a POST request to /auth/login to get started."
		}

- POST http://127.0.0.1:5000/api/v1/auth/register will prompt you to register a new user, providing username, email and password

	body
	
		{
			"username":"Evans",
			"email":"evans@evans.com",
			"password":"evans123"
		}

 	response

		{
		  	"message": "Evans created successfully"
		}

- POST http://127.0.0.1:5000/api/v1/auth/login will login user and generate a token.
	
		{
		 	"message": "Welcome Evans",
		  	"token": "Generated Token"
		}

- POST http://127.0.0.1:5000/api/v1/bucketlists create a new bucket list
	
	header

		Authorization : Generated Token 
	
	body

		{   
			"name":"January Activities"
		}

	response

		{
		  	"message": "January Activities created bucketlist successfully"
		}

- GET http://127.0.0.1:5000/api/v1/bucketlists displays all of the users bucket lists.

	header

		Authorization : Generated Token 

	response

		{
		  "bucketlists": [
		    {
		      "creator": "EVANS",
		      "date_created": "Sun, 15 Jan 2017 08:17:36 GMT",
		      "date_modified": null,
		      "id": 1,
		      "items": [],
		      "name": "January Activities"
		    }
		  ],
		  "next": "None",
		  "previous": "None",
		  "total pages": 1
		}

- POST http://127.0.0.1:5000/api/v1/bucketlists/id/items create a new item in a bucket list
	
	header

		Authorization : Generated Token 

	body

		{   
			"name":"buy a plot"
		}

	response

		{   
			"message": "buy a plot item created successfully"
		}
