# README #

### DOCKER CONTAINER WILL NOT RUN UNTIL YOU SET REDIS_HOST, REDIS_PORT AND AT LEAST A SINGLE KEYWORD INTO ARTICLE_1_KEYWORDS IN .env FILE !!! ###
### Defaults to serving on port 81. ###

After running, simply point an RSS feed reader client to one of the xml paths of the host: (check the docker container log output to see all of your generated RSS feed XML files)

* http://snakeEaterHostname:81/general.xml 
* http://snakeEaterHostname:81/userDefinedCategory1.xml 
* http://snakeEaterHostname:81/userDefinedCategory2.xml


### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions