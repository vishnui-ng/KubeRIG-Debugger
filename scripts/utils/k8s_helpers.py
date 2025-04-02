"""
This module provides utility functions for interacting with Kubernetes deployments, pods, and logs.
"""

import subprocess

def get_deployments(context="sec"):
    """
    Fetch all deployments in the specified Kubernetes context.
    """
    try:
        result = subprocess.run(
            ["kubectl", "--context", context, "get", "deployments", "-o", "jsonpath={.items[*].metadata.name}"],
            capture_output=True,
            text=True,
            check=True
        )
        deployments = result.stdout.strip().split()
        return deployments
    except subprocess.CalledProcessError as e:
        print(f"Error fetching deployments: {e.stderr}")
        return []

def scale_deployment(context, deployment, replicas):
    """
    Scale a specific deployment to the desired number of replicas.
    """
    try:
        subprocess.run(
            ["kubectl", "--context", context, "scale", "deployment", deployment, f"--replicas={replicas}"],
            check=True
        )
        print(f"Successfully scaled {deployment} to {replicas} replicas.")
    except subprocess.CalledProcessError as e:
        print(f"Error scaling deployment {deployment}: {e.stderr}")

def get_pods(context, deployment):
    """
    Fetch all pods for a specific deployment in the specified Kubernetes context.
    """
    try:
        result = subprocess.run(
            ["kubectl", "--context", context, "get", "pods", "-l", f"app={deployment}", "-o", "jsonpath={.items[*].metadata.name}"],
            capture_output=True,
            text=True,
            check=True
        )
        pods = result.stdout.strip().split()
        return pods
    except subprocess.CalledProcessError as e:
        print(f"Error fetching pods for deployment {deployment}: {e.stderr}")
        return []

def fetch_logs(context, pod, output_file, container=None):
    """
    Fetch logs for a specific pod and save them to a file.
    Optionally specify a container name to fetch logs from a specific container.
    """
    try:
        command = ["kubectl", "--context", context, "logs", pod]
        if container:
            command.extend(["-c", container])
        with open(output_file, "w") as file:
            subprocess.run(command, stdout=file, check=True)
        print(f"Logs for pod {pod} (container: {container}) saved to {output_file}.")
    except subprocess.CalledProcessError as e:
        print(f"Error fetching logs for pod {pod} (container: {container}): {e.stderr}")

def get_current_context():
    """
    Get the current Kubernetes context from the environment.
    """
    try:
        result = subprocess.run(
            ["kubectl", "config", "current-context"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def validate_context(context):
    """
    Validate if the given Kubernetes context exists.
    """
    try:
        result = subprocess.run(
            ["kubectl", "config", "get-contexts", "-o", "name"],
            capture_output=True,
            text=True,
            check=True
        )
        contexts = result.stdout.strip().split()
        return context in contexts
    except subprocess.CalledProcessError:
        return False

def get_all_contexts():
    """
    Get all available Kubernetes contexts.
    """
    try:
        result = subprocess.run(
            ["kubectl", "config", "get-contexts", "-o", "name"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split()
    except subprocess.CalledProcessError:
        return []

def delete_pod(context, pod_name):
    """
    Delete a specific pod in the given Kubernetes context.
    """
    try:
        subprocess.run(
            ["kubectl", "--context", context, "delete", "pod", pod_name],
            check=True
        )
        print(f"Successfully deleted pod {pod_name}.")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting pod {pod_name}: {e.stderr}")

def select_context(default_context="sec"):
    """
    Display available contexts and allow the user to select one by number.
    Default to the specified default_context if no input is provided.
    """
    contexts = get_all_contexts()
    if not contexts:
        print("No Kubernetes contexts found.")
        return None

    print("\nAvailable Kubernetes contexts:")
    for i, context in enumerate(contexts, start=1):
        print(f"{i}. {context}")
    print(f"0. Default to '{default_context}'")

    try:
        choice = int(input(f"\nSelect a context by number (default is '{default_context}'): ") or 0)
        if choice == 0:
            return default_context
        if 1 <= choice <= len(contexts):
            return contexts[choice - 1]
        else:
            print("Invalid choice.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None