# TimBen Book Catalogue WebApp

## Description
This webapp is an implementation of a library book catalogue/shop. The webapp features a homepage, catalogue, register, login, and also provides the functionality to review books and also add them to a shopping cart. Our implementation requires that a user is logged in to perform a review and to access the 'shopping cart' or 'purchased books' pages. Each user object of the webapp contains the reiviews that a user has made, the current shopping cart instance and the list of books that a user has purchased. When logging out, the shopping cart is cleared and cannot be retrieved. The list of purchased books is saved and can be retrieved upon logging back in.

When the the webapp is set to either memory and/or TESTING *(see .env variables below)*, Any data not part of the provided json files in 'library/adapters/data' e.g. registered users, purchased books, shopping cart etc, will be lost upon stopping the app in the terminal it is running in. 

Another thing to note is that our implementation of prices and discounts are randomized, when TESTING is False and database mode is selected, these prices will be persistent. However if the webapp is set to memory and/or TESTING True, the webapp will randomize new prices and discounts upon execution.


## Python version
Please use Python version 3.6 or newer versions for development. Some of the depending libraries of our web application do not support Python versions below 3.6!


## Installation

**Installation via requirements.txt**
```shell
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```
when running this webapp please makesure you configure a virtual environment with the requirements.txt file installed as shown above. (this assumes that you have pip installed).

## Testing with the pytest unit tests

**Testing in memory mode**
Set the REPOSITORY env variable in the .env file to memory. *(see Choosing the environment variables below).*

From a terminal in the root folder of the project, run the command below
```
'python -m pytest tests'
``` 

**Testing in database mode**
Set the REPOSITORY env variable in the .env file to database. *(see Choosing the environment variables below).*

From a terminal in the root folder of the project, run the command below
```
'python -m pytest test_db'
``` 

## Execution of the web application

**Choosing the environment variables**
Use the .env file of the project directory to choose the webapp environment:

```
FLASK_ENV <- can be set to development or production

TESTING <- True or False

SQLALCHEMY_ECHO <- when set to True will output database behaviour in command line

REPOSITORY <- used to select a memory or database based repository.
```
*NOTE: When TESTING is set to True the database will refresh and remove all data upon executing the application*

**Running the Flask application**
From the project directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 
The application will run on a local server and the webapp can be viewed through any standard browser of your choice. Executing the above command will start the webapp on the server and output the address to access it.

**Common error with the local server and browser cacheing**
The web app local server can produce errors due to the cacheing of most common web browsers. The error occurs when the browser loads an instance of a previous user being logged upon starting the local server. However this produces a error as this user is not actually logged in. Due to this, the web app runs best in a private or incognito window that prevents previous sessions from interfering with new ones. Alternatively you can make sure that the home page only displys 'Welcome' and not 'Welcome, {user_name}' when starting the web app. If this is the case, simply just click the logout button in the navigation top bar.

## Data sources 
The data in the excerpt files were downloaded from (Comic & Graphic):
https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home

On this webpage, you can find more books and authors in the same file format as in our excerpt, for example for different book genres. 
These might be useful to extend your web application with more functionality.

We would like to acknowledge the authors of these papers for collecting the datasets by extracting them from Goodreads:

*Mengting Wan, Julian McAuley, "Item Recommendation on Monotonic Behavior Chains", in RecSys'18.*

*Mengting Wan, Rishabh Misra, Ndapa Nakashole, Julian McAuley, "Fine-Grained Spoiler Detection from Large-Scale Review Corpora", in ACL'19.*
#
