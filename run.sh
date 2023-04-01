if [ "$1" = "--reqs"  || "$1" = "-r" ]; then
    cd backend
    pip install pipreqs
	pipreqs . --force
    cd ..
elif [ "$1" = "--install" || "$1" = "-i"]; then
    cd backend
    pip install -r requirements.txt
    cd ..
    cd mobile
    npm install
    cd ..
elif [ "$1" = "--start" || "$1" = "-s"]; then
    cd backend
    uvicorn main:api --reload
    cd ..
    cd mobile/forager
    npm start
    cd ..
fi
