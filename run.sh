if [ "$1" = "reqs" ]; then
    pip install pipreqs
	pipreqs . --force
elif [ "$1" = "install" ]; then
    
