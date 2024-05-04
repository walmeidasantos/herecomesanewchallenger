
#!/bin/bash

# Replace with the actual path to your Unix socket file
SOCKET_PATH=$GUNICORN_BIND

# Simple check: Try connecting to the socket
nc -z -U $SOCKET_PATH

# Exit code interpretation:
# - 0: Healthy (connection successful)
# - Other: Unhealthy (connection failed)
exit $?