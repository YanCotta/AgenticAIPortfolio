"""
Module for executing code in a sandboxed environment using Docker.
"""

import os
import subprocess
from autogen.coding import LocalCommandLineCodeExecutor
from MultiAgentFinancialAnalysis.logger import get_logger

logger = get_logger(__name__)

class DockerCodeExecutor(LocalCommandLineCodeExecutor):
    """
    Executes code in a Docker container to provide a sandboxed environment.
    """

    def __init__(self, *args, docker_image="python:3.9-slim", **kwargs):
        """
        Initializes the DockerCodeExecutor.

        Args:
            docker_image (str): The Docker image to use for execution.  Defaults to "python:3.9-slim".
            *args:  Positional arguments passed to the superclass.
            **kwargs: Keyword arguments passed to the superclass.
        """
        super().__init__(*args, **kwargs)
        self.docker_image = docker_image

    def execute_code(self, code, lang):
        """
        Executes the given code in a Docker container.

        Args:
            code (str): The code to execute.
            lang (str): The programming language of the code.

        Returns:
            tuple: A tuple containing the execution result and an error message (if any).
        """
        # Create a temporary file to store the code
        temp_file = os.path.join(self.work_dir, f"temp_code.{lang}")
        with open(temp_file, "w") as f:
            f.write(code)

        # Construct the Docker command
        docker_command = [
            "docker",
            "run",
            "--rm",  # Automatically remove the container after it exits
            "-v",
            f"{os.path.abspath(self.work_dir)}:/app",  # Mount the working directory
            "-w",
            "/app",  # Set the working directory inside the container
            self.docker_image,
            "python",
            temp_file,
        ]

        try:
            # Execute the Docker command
            process = subprocess.Popen(
                docker_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                cwd=self.work_dir,
            )
            result, error = process.communicate(timeout=self.timeout)

            # Log the execution result
            logger.info(f"Execution result: {result}")
            if error:
                logger.error(f"Execution error: {error}")

            return result, error
        except subprocess.TimeoutExpired:
            process.kill()
            error = "Timeout expired"
            logger.error(f"Execution timeout: {error}")
            return "", error
        except Exception as e:
            error = str(e)
            logger.error(f"Execution failed: {error}")
            return "", error
