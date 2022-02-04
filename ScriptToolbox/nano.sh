cd "$(dirname "$0")"
if [ -e ../main.py ]; then
    echo '123456' | sudo -S python3 ../main.py
else
    echo 'Main programme does not exist.'
fi