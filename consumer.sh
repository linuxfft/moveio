
#!/bin/bash
cd sync_docker
echo `pwd`
echo "HUEY CONSUMER"
echo "-------------"
echo "Stop the consumer using Ctrl+C"
PYTHONPATH=.:$PYTHONPATH

python -m huey.bin.huey_consumer sync_main.docker_huey -w 10 -k process


