[![Build Status](https://travis-ci.org/andela-gacheruevans/cp2-bucketlist.svg?branch=ft-implement-tests)](https://travis-ci.org/andela-gacheruevans/cp2-bucketlist)
[![Coverage Status](https://coveralls.io/repos/github/andela-gacheruevans/cp2-bucketlist/badge.svg?branch=ft-implement-tests)](https://coveralls.io/github/andela-gacheruevans/cp2-bucketlist?branch=develop)
# Bucketlist API

This application helps you log and catalog all the stuff you want to accomplish before you expire. 

##Task Description:
In this exercise I was required to create a Flask API for a bucket list service. Specification for the API is shown below.

| Endpoint                 				               | Functionality 						 |    
| -----------------------------------------------------|:-----------------------------------:|
| POST /auth/login         				               |  Logs a user in                     |
| POST /auth/register      				               |  Register a user                    |
| POST /bucketlists/       				               |  Create a new bucket list	         |
| GET /bucketlists/						               |  List all the created bucket lists	 | 
| GET /bucketlists/<bucketlists_id>		               |  Get single bucket list             |                     
| PUT /bucketlists/<bucketlists_id>                    |  Update this bucket list            |                       
| DELETE /bucketlists/<bucketlists_id>				   |  Delete this single bucket list     |                              
| POST /bucketlists/<bucketlists_id>/items/            |  Create a new item in bucket list   |                                
| PUT /bucketlists/<bucketlists_id>/items/<item_id>    |  Update a bucket list item          |                         
| DELETE /bucketlists/<bucketlists_id>/items/<item_id> |  Delete an item in a bucket list    |




