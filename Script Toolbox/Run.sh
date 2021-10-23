rsync -av -e ssh --exclude={'.git','.vscode', '__pycache__', 'Instructions'} ../ lywal@192.168.1.133:~/Wheelchair
ssh -tt lywal@192.168.1.133 '~/Wheelchair/Script\ Toolbox/Nano.sh'