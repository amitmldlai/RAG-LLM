import subprocess
import os

cwd = os.getcwd()
venv_path = f'{cwd}/venv/Scripts/python'


def run_graphrag_index():
    """
    Runs the Graphrag index command to retrain the RAG model using a specified virtual environment.

    Returns:
        str: The output of the command.
    """
    # Define the command as a list
    command = [
        venv_path, '-m', 'graphrag', 'index',
        '--root', './'
    ]

    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    # Check for errors in the execution
    if result.returncode != 0:
        print(f"Error: {result.stderr}")  # Print error message if any
        return None

    return result.stdout  # Return the output of the command


def run_graphrag_query(query, method='local'):
    """
    Runs a Graphrag query using a specified virtual environment.

    Args:
        query (str): The query string to execute.
        method (str): The method type to use (default is 'local').

    Returns:
        str: The output of the command.
    """
    # Define the command as a list
    command = [
        venv_path, '-m',
        'graphrag',
        'query',
        '--root', '.',
        '--method', method,
        '--query', query
    ]

    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    # Check for errors in the execution
    if result.returncode != 0:
        print(f"Error: {result.stderr}")  # Print error message if any
        return None
    print(result.stdout.split('SUCCESS:')[1])
    return result.stdout.split('SUCCESS:')[1]  # Return the output of the command

