if [ -e ~/Wheelchair/main.py ]; then
    echo '123456' | sudo -S python3 ~/Wheelchair/main.py
else
    echo 'main programme does not exist.'
fi