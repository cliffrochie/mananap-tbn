# mananap-tbn

<h3>Introduction</h3>
<p>This project is used in school events to utilize the technology and keep track of records digitally.</p>
<p>It is implemented as a RESTful API that is developed using Flask framework</p>

<h3>Major requirements</h3>
<ul>
  <li>Python 3.5+</li>
  <li>MySQL database</li>
</ul>

<br/>
<h3>Package requirements</h3>
<p>Here are the list of modules that have been used in this project</p>
<ul>
  <li><h4>poetry</h4> - to handle the modules/libraries/packages used in this sample task</li>
  <li><h4>flask</h4> - it is a micro web framework.</li>
  <li><h4>flask_cors</h4> - it is an extension tool that handles CORS</li>
  <li><h4>flask_sqlalchemy</h4> - it is an extension for Flask that adds support for SQLAlchemy ORM.</li>
  <li><h4>sqlalchemy</h4> - it is an ORM, the purpose of this module to this project is to use its exception module.</li>
  <li><h4>sqlalchemy_utils</h4> - a helper tool to handle database, table creation</li>
  <li><h4>faker</h4> - a helper tool that generates informative random strings that is useful to populate data to the database</li>
  <li><h4>PyJWT</h4> - to use json web token feature in auth.</li>
</ul>

<br/>
<h3>Helper tools/modules</h3>
<ul>
  <li><h4>black</h4> - It is a formatter that makes the code elegant.</li>
  <li><h4>mypy</h4> - It is a type checker that thecks the code statically and find potential bugs.</li>
  <li><h4>flake8</h4> - It is a helper tool that identifies the error and/or the violation codes </li>
  <li><h4>bandit</h4> - It is a tool that finds common security issues in Python.</li>
</ul>
<p>All of the package are installed via poetry.</p>

<h3>Usage</h3>
<p>To run this program, make sure you already installed the package requirements stated above.</p>
<p>To run the code, type <strong><code>poetry run python run.py</code></strong> when you are in the directory. 
Once the program starts, it will automatically created the database tables</p>
