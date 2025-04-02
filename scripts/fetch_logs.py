"""
This script fetches logs from Kubernetes pods.
It allows the user to select deployments, fetch logs from their pods, and save
the logs to files in a user-specified directory.
"""

import os
from datetime import datetime
import pytz
from utils.k8s_helpers import get_deployments, get_pods, fetch_logs, get_current_context, validate_context, get_all_contexts

def select_context():
    """
    Display available contexts and allow the user to select one by number.
    """
    contexts = get_all_contexts()
    if not contexts:
        print("No Kubernetes contexts found.")
        return None

    print("\nAvailable Kubernetes contexts:")
    for i, context in enumerate(contexts, start=1):
        print(f"{i}. {context}")

    try:
        choice = int(input("\nSelect a context by number (default is current context or 'sec'): ") or 0)
        if choice == 0:
            return get_current_context() or "sec"
        if 1 <= choice <= len(contexts):
            return contexts[choice - 1]
        else:
            print("Invalid choice. Please select a valid number.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

def fetch_logs_for_deployments(context, base_output_dir="logs"):
    """
    Fetch logs for the selected deployments and save them to the specified directory.
    """
    print(f"Fetching deployments from context: {context}")
    deployments = get_deployments(context)

    if not deployments:
        print("No deployments found.")
        return

    print("\nAvailable deployments:")
    for i, deployment in enumerate(deployments, start=1):
        print(f"{i}. {deployment}")

    choices = input("\nEnter the numbers of the deployments to fetch logs from (comma-separated): ")
    try:
        selected_indices = [int(choice.strip()) - 1 for choice in choices.split(",")]
        selected_deployments = [deployments[i] for i in selected_indices if 0 <= i < len(deployments)]
    except (ValueError, IndexError):
        print("Invalid input. Please enter valid numbers.")
        return

    if not selected_deployments:
        print("No valid deployments selected.")
        return

    # Get current PST time
    pst_tz = pytz.timezone("America/Los_Angeles")
    current_time = datetime.now(pst_tz)
    current_date_str = current_time.strftime("%m%d%Y")  # MMDDYYYY
    current_time_str = current_time.strftime("%H%M")    # HHMM

    # Create base folder structure: context/date/time
    output_dir = os.path.join(base_output_dir, context, current_date_str, current_time_str)
    os.makedirs(output_dir, exist_ok=True)

    for deployment in selected_deployments:
        print(f"\nFetching pods for deployment: {deployment}")
        pods = get_pods(context, deployment)

        if not pods:
            print(f"No pods found for deployment: {deployment}")
            continue

        # If multiple pods, create a folder for the deployment
        if len(pods) > 1:
            deployment_dir = os.path.join(output_dir, deployment)
            os.makedirs(deployment_dir, exist_ok=True)
            for pod in pods:
                log_file = os.path.join(deployment_dir, f"{pod}.log")
                print(f"Fetching logs for pod: {pod} (container: {deployment})")
                fetch_logs(context, pod, log_file, container=deployment)
        else:
            # If only one pod, save the log directly in the output directory
            pod = pods[0]
            log_file = os.path.join(output_dir, f"{pod}.log")
            print(f"Fetching logs for pod: {pod} (container: {deployment})")
            fetch_logs(context, pod, log_file, container=deployment)

def main():
    # Select context
    context = select_context()
    if not context:
        print("No valid context selected. Exiting.")
        return

    # Validate the context
    if not validate_context(context):
        print(f"Error: The context '{context}' is not valid or not present.")
        return

    print(f"Using context: {context}")
    fetch_logs_for_deployments(context)

if __name__ == "__main__":
    main()