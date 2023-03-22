echo "now that we have taken care of the server part we can create the database"
echo "from here, i will leave you to the postgres database shell"
echo "refer to the readme and follow the instructions"
sudo -u postgres psql

echo "Welcome back! I hope the installation went well!"
echo "Don't forget to store the information you just used inside the .env file"
echo "you'll find the .env file inside the /base folder."
./django_starter.sh