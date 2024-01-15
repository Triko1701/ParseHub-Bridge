import subprocess as sp

def run_shell_cmd(cmd: str) -> str:
    """
    Execute a shell command and return the combined standard output and standard error.

    Parameters:
    - cmd (str): The shell command to be executed.

    Returns:
    - str: The combined standard output and standard error of the executed command.

    Raises:
    - CalledProcessError: If the command exits with a non-zero status.

    Example:
    >>> run_shell_cmd("ls -l")
    'total 4\n-rw-r--r-- 1 user user 15 Jan 15 12:00 example.txt'
    """
    result = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE, text=True, shell=True)
    output = (result.stdout + result.stderr).strip()
    return output
