import subprocess

def run_shell_cmd(cmd: str):
    try:
        print(f"Running command: {cmd}\n")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        output = (result.stdout + result.stderr).strip()
        print(f"Output: {output}\n")
        return output
    except subprocess.CalledProcessError as e:
        print(f"Failed to run command. Exit Code {e.returncode}\n")
        raise