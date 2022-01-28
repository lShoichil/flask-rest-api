cd ..
source prodenv/bin/activate
pip freeze > requirements.txt
git add .
git commit -m "deploy prod"
git push origin master
cd scripts && sh build.sh
