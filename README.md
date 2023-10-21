PlanetScale is a cloud-based edge database service provider that allows us to manage a remote MySQL database. Prisma is a TypeScript/JavaScript Object-Relational Mapper ORM) that has been shipped over with Python support and makes it easier to work with databases. To connect to PlanetScale with Prisma for Python, you can follow these step-by-step instructions: For better documentation on setting up the database on PlanetScale, follow this guide:
https://planetscale.com/docs/onboarding/create-a-database

## Setting up a PlanetScale Account (https://planetscale.com/docs/onboarding/create-an-account)

Login to PlanetScale using your GitHub account at https://auth.planetscale.com/sign-in
Verify your email address (if necessary I can’t remember if I had to)
You will need to connect a valid debit/credit card for details to complete account creation.

After that, create a new database, set it to ap-southeast-1 (Singapore) region and select the Hobby Tier, let them update you in case your database enters sleep after 7 days of inactivity. In the “connect to your database” screen, just click I’ll do this later.

Your dashboard should look something like this. Click the connect button and in the dropdown for Connect with, choose Prisma. Click New Password button and Create password. Copy over the connection string under the .env tab. You might need to generate a new password if your connection string has asterisks(\*) in it, as database passwords are only visible at creation.

Your final copy-pasted string should look something like
DATABASE_URL='mysql://<username>:\***\*\*\*\*\*\*\***@aws.connect.psdb.cloud/<database_name>?sslaccept=strict'
where the asterisks are replaced with a password and the correct username and database names are present too.

## Installing Prisma python package and Prisma VS Code extension (https://prisma-client-py.readthedocs.io/en/stable/getting_started/setup/)

We will be using VS Code for the Prisma extension (LSP & Formatter) and the built-in terminal to run CLI commands to connect your local Prisma schema to your PlanetScale database. I also recommend installing the Error Lens extension while you’re here.

Install Prisma extension on VS Code from the extensions marketplace.
Install Prisma using pip by running the command in the terminal (Ctrl + ` to activate in VS Code):
pip install prisma

## Initialize Prisma Client Configuration

(https://prisma-client-py.readthedocs.io/en/stable/getting_started/quickstart/):
I created a repository that you can refer to for the following steps.
https://github.com/matthewloh/prismaforpython
Create a new directory to store your Prisma configuration (e.g., `prisma/`).
Inside the `prisma/` directory, create a `schema.prisma` file that will hold your models, enums and overall schema between entities in your database. You will need to define your datasource and client generator. To use the Prisma client for Python, copy and paste as follows into your schema.prisma file:

```// in your schema.prisma

generator client {
	provider         	= "prisma-client-py"
	interface        	= "sync"
	recursive_type_depth = "-1"
}

datasource db {
	provider 	= "mysql"
	url      	= env("DATABASE_URL")
	relationMode = "prisma"
}

```

Environment Variables:

- Create a `.env` file in your project directory. Right click the root -> New File. IMPORTANT! Remember to add .env to your .gitignore of the root of your repository. Add your PlanetScale database connection details (DATABASE_URL) to this file:

```.env

DATABASE_URL='mysql://<username>:************@aws.connect.psdb.cloud/<database_name>?sslaccept=strict'

```

## Pushing Schema Changes to your PlanetScale and Generate Prisma Client:

In the repository, I made an example User model that essentially is a table in a database that has the fields id, email, and name. The Post model has a title and content and is linked to an author from the User table using the syntax:
<field_name> <field_type> <@modifiers>
In your terminal, run the following commands to update your PlanetScale schema to the defined models:

```in your terminal
	prisma db push
	prisma generate
```

Assuming no errors were raised, you should be able to view in your PlanetScale dashboard updates to the schema by going into Branches -> main.

Python Script to create a User and a Post
A main.py is already created in the repo that imports and uses the Prisma Client. You can use it to interact with your PlanetScale database. For example whenever you run a script:

```python
from prisma import Prisma

# Initialize the Prisma Client
prisma = Prisma()
# Running prisma.connect() is mandatory
prisma.connect()

	## refer to the main.py in the repository
```

When writing Python code using VS Code, the language server you’re using should provide you the code intellisense context and autocompletion of the data needed to insert a field into the table. Trigger this using Ctrl + Space. Hovering over the fields also provides type hints to ensure you do not mix up allowed types.

When working with multiple collaborators, you can also introspect the latest schema by running
prisma db pull

# Conclusion

That’s about it for now, to learn more about relation disambiguation, one-to-many, many-to-many relationship modelling, look for the documentation at
https://prisma-client-py.readthedocs.io/en/stable/reference/operations/

This YouTube tutorial also does a fantastic job at the modelling portion of Entities using Prisma, ignore the installation and setup process and instead focus on the schema sections. The usage should also be similar albeit in TypeScript.
https://youtu.be/RebA5J-rlwg?si=MsbwLX8QBT60uv24

At this point if you have any questions just contact me on discord my username is kabo\_
👍 Good luck and all the best!

https://docs.google.com/document/d/1TvCIbkcMeL4eZfZQitnYdhZxqaCUelaNdmwPIkSs8R8/edit