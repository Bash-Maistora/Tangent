# Comment Tone Analyzer Api

This api follows restful architecture and provides two endpoints for crud operations:

## /comments
* GET request - For retrieval of all resources. Response is list of comments and status code 200 if successful.
* POST requests - To submit a new comment send a POST request with 'comment' as parameter and the actual comment as a value. Succesful response contains the new comment with tone if identified and status code 201. API returns 400 if comment is missing.

## /comments/{sku}
* GET - Returns comment with the specified sku if it exists else returns 404.
* PUT - Update the comment of the specific resource by submitting a new comment in the body. Returns the new comment and tone if it exists else returns 404.
* DELETE - Deletes the resources if it exists else returns 404.


## Setup
 1. Create and activate virtualenv with python 3.6
 2. Pip install -r requirements.txt
 3. Database creation and migration
    * python migration.py db init
    * python migration.py db migrate
    * python migration.py db upgrade
 4. Run tests with python test_api.py
 5. Run Server with flask run while in root dir

## Scalability
* The api can easily scale horizontally on multiple instances since it is stateless. They can all be located behind a load-balancer that would route requests between the servers, the database would be stored on separate instances(AWS RDS) to complitely decouple the architecture.
* To easily handle a large number of requests caching would be important. Solutions such as Redis and Memcache can help drastically decrease load on the servers.
* For even larger scale a NoSQL database can replace the SQL solution in order to increase the amount of concurrent writes that the database can handle.

## Restful Api
* Simple uniform interface
* The api is stateless as is required by the Representational State Transfer architecture. Each request contains the necessary state to be handled correctly by the server.
* Responses are cacheable
* Client server separation

## Architecture
Given the small scope of the project I made the decision to use Flask web framework as it is light and well suited to small api development and SQLite as a database since the project is not intended for production. The main api is isolated in its own folder that contains main api logic and models. The main folder contains the test file, migrations and run command. I used Application Factory in order to have instances with different settings specifically for testing.




