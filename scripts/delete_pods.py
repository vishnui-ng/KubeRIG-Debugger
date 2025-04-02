"""
This script provides functionality to delete Kubernetes pods interactively.
"""

import subprocess
from utils.k8s_helpers import get_deployments, get_pods, validate_context, select_context

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

def delete_pods_in_deployment(context, deployment):
    """
    Delete all pods under a specific deployment in the given Kubernetes context.
    """
    pods = get_pods(context, deployment)
    if not pods:
        print(f"No pods found for deployment: {deployment}")
        return

    print(f"\nDeleting all pods under deployment: {deployment}")
    for pod in pods:
        delete_pod(context, pod)

def main():
    # Select context
    context = select_context()
    if not context:
        print("No valid context selected. Exiting.")
        return

    # Restrict deletion operations to 'sec' environment
    if context != "sec":
        print(f"Error: Pod deletion operations are restricted to the 'sec' (Secondary RIG) environment.\nMoidfy code to allow deletion in other environments.")
        return

    # Validate the context
    if not validate_context(context):
        print(f"Error: The context '{context}' is not valid or not present.")
        return

    print(f"Using context: {context}")

    # Fetch deployments
    print("Fetching deployments in the selected context...")
    deployments = get_deployments(context)
    if not deployments:
        print("No deployments found in the selected context.")
        return

    print("\nAvailable deployments:")
    for i, deployment in enumerate(deployments, start=1):
        print(f"{i}. {deployment}")

    # Select multiple deployments
    try:
        deployment_choices = input("\nSelect deployments by numbers (comma-separated): ")
        selected_indices = [int(choice.strip()) - 1 for choice in deployment_choices.split(",")]
        selected_deployments = [deployments[i] for i in selected_indices if 0 <= i < len(deployments)]
    except (ValueError, IndexError):
        print("Invalid input. Please enter valid numbers.")
        return

    if not selected_deployments:
        print("No valid deployments selected.")
        return

    # Iterate over selected deployments
    for selected_deployment in selected_deployments:
        print(f"\nSelected deployment: {selected_deployment}")
        delete_choice = input("Do you want to delete all pods under this deployment? (yes/no/skip): ").strip().lower()

        if delete_choice == "skip":
            print(f"Skipping deployment: {selected_deployment}")
            continue
        elif delete_choice == "yes":
            # Delete all pods under the deployment
            delete_pods_in_deployment(context, selected_deployment)
        else:
            # Fetch pods under the deployment
            print(f"\nFetching pods under deployment: {selected_deployment}")
            pods = get_pods(context, selected_deployment)
            if not pods:
                print(f"No pods found for deployment: {selected_deployment}")
                continue

            print("\nAvailable pods:")
            for i, pod in enumerate(pods, start=1):
                print(f"{i}. {pod}")

            # Select multiple pods
            try:
                pod_choices = input("\nSelect pods to delete by numbers (comma-separated, or type 'skip' to skip): ")
                if pod_choices.strip().lower() == "skip":
                    print(f"Skipping pods for deployment: {selected_deployment}")
                    continue
                selected_pod_indices = [int(choice.strip()) - 1 for choice in pod_choices.split(",")]
                selected_pods = [pods[i] for i in selected_pod_indices if 0 <= i < len(pods)]
            except (ValueError, IndexError):
                print("Invalid input. Please enter valid numbers.")
                continue

            if not selected_pods:
                print("No valid pods selected.")
                continue

            # Confirm and delete selected pods
            print(f"\nSelected pods to delete: {', '.join(selected_pods)}")
            confirm = input("Are you sure you want to delete these pods? (yes/no/skip): ").strip().lower()
            if confirm == "skip":
                print(f"Skipping deletion of selected pods for deployment: {selected_deployment}")
                continue
            elif confirm == "yes":
                for pod in selected_pods:
                    delete_pod(context, pod)
            else:
                print("Operation canceled for these pods.")

if __name__ == "__main__":
    main()