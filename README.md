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
        <code>$ source venv/bin/activate</code><br>
        <code>(venv) $ _</code>
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
<p>For development try to use mysql. if you know how to set it up, a sqlite database will be made automatically, but this will likely cause problems later. So don't rely on it. For production we will use a mysql server from the school.</p>

<p>This project implements database migrations with flask-migrate.</p>

Create a migration with: <br>
<code>(venv) $ flask db migrate -m "migration name"</code>

upgrade migration with: <br>
<code>(venv) $ flask db upgrade</code>

downgrade migration with: <br>
<code>(venv) $ flask db downgrade</code>

<hr>
<h3>Related Flask Tutorials</h3>
<p><a href="https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world">The Flask Mega Tutorial</a> is a good start if anything here confuses you.</p>
<p><a href="http://exploreflask.com/en/latest/index.html">Explore Flask</a> is the best resourse for the design patterns we will be using. Check it out.</p>