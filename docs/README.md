### Setting Up the Django Project
1. Install [Python version 3.7.4](https://www.python.org/downloads/release/python-374/) for your OS
   * After installing, validate that it was successful by running the command `python3 --version`
   * Also ensure that pip was installed alongside python by running the command `pip --version`

   *In Windows: If you type 'py' it will show you python version number and enter the python shell. type 'exit()' to leave.           
   *In Windows: Type 'py -m pip --version' in CMD Prompt to see pip verion number

2. Create a clone of our GitHub repository, which can be found [here](https://github.com/Bshuryan/WebAppraisal).
    1. Run the command `git clone https://github.com/Bshuryan/WebAppraisal` `<insert desination directory>`
       * Note: You must specify a project name, so I would recommend the desination directory be `some/directories/WebAppraisal`, which will create a new folder titled `WebAppraisal` under `some/directories/`
    
     2. An alternative method: you can download GitHub Desktop, select file in the top left --> clone directory.  From here you will see the GitHub projects attached to your account.  Clone the WebAppraisal Project.

3. Set up your virtual environment. (MAC)
   1. Run the command `virtualenv -p python3 venv`, which will create a new directory, `venv`
   2. Activate your virtual environment by running `source venv/bin/activate`
   3. Install Django using pip by running the command `pip install django==3.1.5`

4. Set up Virtual env in Windows.

   1. login to pycharm and Open cloned project from GitHub
   2. On the bottom of the pycharm window select Terminal
   3. Find where your python install is located, you will need to run the command in terminal from this directory. **You can do this by running this command in CMD Prompt "py -c "import os, sys; print(os.path.dirname(sys.executable))"
   4. change directorys in terminal to the file path given in the above cmd
   5. once in the correct directory run 'py -m venv C:\"YourFilePathOfGitHubProject"\venv     *It is important to remember the folder name after your GitHub Project File Path in order to create a folder and avoid installing in the root of your project
     *Running this correctly should get you a new folder in your pycharm client in the WebAppraisal project called "venv"
   6.  in pycharm, double click the shift key and type in "base" in the search box. Open up the base webApprasial.settings file, and press cntrl F to search for the "SECRET_KEY" variable. Replace the value to SECRET_KEY = 'secretkeyvalue' (secret key can be found in the discord)
   7. CD back to the path of the github project and activate your virtual enviorment with venv\scripts\activate in CMD prompt
   8. In the terminal, make sure your all the requirements are installed by running pip install -r requirements.txt
  **Note. Make sure you are installing the requirements inside your virtual environment. You should see (venv) in the terminal.
   
### Running Locally
(MAC)

1. While in your virtual environment and at the top level of the project directory, run the command `python manage.py runserver`
2. Visit http://127.0.0.1:8000/, which will direct you to the landing page for our webapp.

(WINDOWS)

1. while in CMD prompt and have you venv active type 'py manage.py runserver'
2. Visit http://127.0.0.1:8000/, which will direct you to the landing page for our webapp.

(USING DOCKER)
1. Download [the Docker desktop app](https://docs.docker.com/get-docker/). If you already own Docker, please ensure that you have the `docker-compose` command. If not, install [here](https://docs.docker.com/compose/install/).

      a. You must have Hyper-V enabled for this to work. Follow [this](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v) guide on how to do this.

      b. If you have Windows 10 home, you need to install the WSL2 feature for Windows. Follow [this](https://docs.docker.com/docker-for-windows/install-windows-home/) guide to set this up.

2. Create a file titled `.env` (do not specify a file type) under the top project directory (this should be named WebAppraisal but you may have named it something else)
    * Add the following lines to this file: 
    
        `SECRET_KEY=INSERT SECRET KEY HERE WITHOUT QUOTES`
    `DATABASE_URL=postgres://postgres:postgres@db:5432/postgres`
    
3. Run the following command from the top project directory: `docker-compose up --build`. If you see `Starting development server at http://0.0.0.0:8000/` you are able to run the webapp locally! However, you will need to apply the migrations to ensure you have the latest changes.
4. Run the following command from the project directory: `docker-compose run web python manage.py migrate` (note, if you ran the last command in a cmd prompt, you won't be able to type in your command. Open up another command prompt and run the command from the project directory)
5.  In your webrowser, go to localhost:8000 and it should take you to the login page. Open up the docker desktop app and you should now see "webappraisal" as a selection. Click on the dropdown, and hover over the "webappraisal_web_1" app. Click on the first button that is shown on the right, and it should take you to the WebAppraisal login page if successfull.

### Running in Production Environment
* We are quite there yet


### FAQ
Q: Why am I getting an error `"Set the SECRET_KEY environment variable"`?

A: You may be running the project locally for the first time. Follow these steps to resolve the issue:
1. Request the secret key from a project member.
2. If the request is granted, add the following line to the bottom of `venv/bin/activate` to add the environment variable
    `export SECRET_KEY="Insert Secret Key here"`
3. Deactivate your virtual environment by running `deactivate` while within your virtual environment
4. Re-activate your environment to apply your changes by running `source venv/bin/activate`
5. Retry running `python manage.py runserver`


Q: Why am I receiving an ImportError?

A: You may not have the package requirements. Open up the requirements.txt inside Pycharm. If a message says the requirements are not satisfied, click the "Install Requirements" option. Alternatviely, you can run running pip install -r requirements.txt to install all the libraries listed in the requirements.txt file.


Q: Why am I seeing errors when attempting to create a user for the first time with docker?

A: You may have to make migrations to the update the database schema. Run the command `docker-compose run web python manage.py migrate` and then `docker-compose up --build` and try again.


Q: How do I create my admin account?

A: In the Docker desktop app, click the dropdown for the webappraisal container. Hover over the "web_appraisal_web_1" and select the second button to the right of it (CLI). A command prompt should open up. From here, you can run "python manage.py createsuperuser". It should then prompt you for the information to make a superuser account. You can confirm that it has worked by going to localhost:8000/admin/ and entering in the credentials you created for the superuser.

Q: How do I run unit tests?

A: Run the following commands:

    1. docker-compose run web coverage run -m pytest
        * This will run the unit tests
    2. docker-compose run web coverage report // this is optional
        * Gives a summary of unit test coverage
    3. docker-compose run web coverage html // this is also optional
        * Creates the directory "htmlcov" at the project level - open up htmlcov/index.html for a detailed coverage report. This shows lines of code/branches covered or not covered by unit tests.
    