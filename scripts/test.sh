echo """this script will $(basename ${PWD%/*})allow to set gunicorn and nginx"""
#read -p "what is the name of the user you have created? " user_name
echo "Let's start from gunicorn:"
#echo $user_name
echo $(basename ${PWD%/*})

sed -i "s/USER/$user_name/" ./gunicorn/test.txt
sed -i "s/PROJECTDIR//" ./gunicorn/test.txt