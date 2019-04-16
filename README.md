
<h1>ToDo</h1>
<h3>Unit tests</h3>
<p>create a testing environment. create stubs. Check if inputs create outputs. create test for each unit test
</p>



<hr>
<h1>Syllahub</h1>
<p>Revamping the syllabus management system</p>

<hr>
<h3>Python</h3>
<p>I am using <a href="https://www.python.org/downloads/">python 3.7.2</a>. I think this is the most recent stable version. <strong>Make sure you are using the correct python command that is mapped to the correct python version.</strong></p>
<h5>Common python commands are:</h5>
<ul>
    <li>$ python</li>
    <li>$ python3</li>
    <li>$ py</li>
    <li>$ py3</li>
</ul>
<h5>Check python version for each command with: </h5>
<ul>
    <li>$ python -V</li>
    <li>$ python3 -V</li>
    <li>$ py -V</li>
    <li>$ py3 -V</li>
</ul>

<hr>
<h3>Flask Instalation Instructions</h3>
Once you clone the git repository, you must do a couple things to get this working on your local machine.
<ul>
    <li>
        cd to Syllahub directory
    </li>
    <li>
        Create Virtual Environment: <br>
        <code>$ python -m venv venv</code><br>
    </li>
    <li>
        Activate virtual environment: <br>
        For Windows: <code>$ venv/Source/activate</code><br>
        For Mac: <code>$ source venv/bin/activate</code><br>
        <code>(venv) $ _</code> <-- you should see this if enviroment is activated
    </li>
    <li>
        install all required packages from requirements.txt<br>
        <code>(venv) $ pip install -r requirements.txt</code><br>
        <strong>Note:</strong> if you change the packages you must update requirements.txt with: <br>
        <code>(venv) $ pip freeze > requirements.txt</code>
    </li>
    <li>
        Run local server with: <br>
        <code>$ flask run</code>
    </li>
</ul>

<hr>
<h3>Database</h3>
<p>You must set up your own mysql server on your local machines</p>

do not push the config file until I fix the flaskenv file loading<br>

We used the fillowing sql command to get the database info. Run this command from inside a mysql console.
<code>mysql > select * from information_schema.processlist;</code>

change the config variable SQLALCHEMY_DATABASE_URI <br>
"dialect[+driver]://user:password@host/dbname" <-- this is the standard format. fill in the correct info for your local database<br>

upgrade migration with: <br>
<code>(venv) $ flask db upgrade</code>

downgrade migration with: <br>
<code>(venv) $ flask db downgrade</code>

<p>This project implements database migrations with flask-migrate.</p>

Create a migration with: <br>
<code>(venv) $ flask db migrate -m "migration name"</code>
<hr>



<h3>HTTP RESTful Services</h3>
<a href="https://www.restapitutorial.com/lessons/httpmethods.html">GET and Post tutorial</a>
<p>We probably won't be using PUT, PATCH, and DELETE requests. But this is ideally how it should be done. This link also shows a good list of errors.</p>
<hr>


<h3>Related Flask Tutorials</h3>
<p><a href="https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world">The Flask Mega Tutorial</a> is a good start if anything here confuses you.</p>
<p><a href="http://exploreflask.com/en/latest/index.html">Explore Flask</a> is the best resourse for the design patterns we will be using. Check it out.</p>

