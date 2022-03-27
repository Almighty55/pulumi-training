# login to pulumi backend (this case it's local)
pulumi login --local

# install packages for virtual environment
venv\Scripts\pip install -r requirements.txt

# if the above fails try this
"C:\Users\Almighty\Documents\code\Scripts-n-Stuff\Python\Pulumi\AlmightyDev\AWS\ec2\venv\Scripts\python.exe" -m pip install --upgrade pip

# deploy the stack
pulumi up