# The largest heading

## Executing The Code


### Steps To Follow
	
	> Creating Virtual Environement First
		
		For Windows:
		
		`	
			pip install virtualenv
			python venv -m venv
		`
		
		For Ubuntu:
		
		`
			pip install virtualenv
			python3 venv -m venv
		` 
		or 
		
		`
			python venv -m venv
		`
	
	> Activating Environment

		For Ubuntu User:
			> source venv/bin/activate
	
		For Windows User:
			.\venv\Scripts\activate

	> Installing the Requirements 
	
		`
			pip install - r requirements.txt
		`
	
	> loading Postman Collection in postman will be found 
	in:
	
		> assignment_task > postman_collection

	> Run The Project
		`
			python3 app.y
		`

## Working With Project:

	> First you will register the user by using the register api
	> next you will use login credentials to create jwt tokens for authentication
	> next you will use tokens in the headers of get,update and delete api.
	> as , the Response is encrypted, so, for decryption use the decript_massage.py file 
