import subprocess

setting = True

container_script = "sudo docker {} cam"
if setting:
    container_script.format("start")
else:
    container_script.format("stop")

print(container_script)

start_container = "sudo docker stop cam"
video_process = subprocess.Popen(
    start_container.split(), stdout=subprocess.PIPE
)
output, error = video_process.communicate()