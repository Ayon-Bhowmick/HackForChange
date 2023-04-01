if [ "$1" = "--reqs"  || "$1" = "-r" ]; then
    pip install pipreqs
	pipreqs . --force
elif [ "$1" = "--install" || "$1" = "-i"]; then
    pip install -r requirements.txt
elif [ "$1" = "--start" || "$1" = "-s"]; then
    cd backend
    uvicorn main:api --reload
    cd ..
fi
