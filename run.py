import subprocess
com_response = subprocess.run(["javac", "Solution.java"], capture_output=True, text=True)
print(com_response.stderr)
response = subprocess.run(["java", "Solution"],capture_output=True, text=True)