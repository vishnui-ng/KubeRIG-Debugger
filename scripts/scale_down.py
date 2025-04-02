"""
This script provides functionality to downscale Kubernetes deployments.
It restricts scaling operations to the 'sec' (Secondary RIG) environment.
"""

from utils.k8s_helpers import get_deployments, scale_deployment, get_current_context, validate_context, get_all_contexts

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

def downscale_deployments(context, deployments_to_downscale, replicas=1):
    """
    Downscale the replicas of the specified deployments to the given number.
    """
    for deployment in deployments_to_downscale:
        print(f"Scaling deployment: {deployment} to {replicas} replicas.")
        scale_deployment(context, deployment, replicas=replicas)

def main():
    # Select context
    context = select_context()
    if not context:
        print("No valid context selected. Exiting.")
        return

    # Restrict scaling operations to 'sec' environment
    if context != "sec":
        print(f"Error: Scaling operations are restricted to the 'sec' (Secondary RIG) environment.")
        return

    # Validate the context
    if not validate_context(context):
        print(f"Error: The context '{context}' is not valid or not present.")
        return

    print(f"Using context: {context}")
    print(f"Fetching deployments from context: {context}")
    deployments = get_deployments(context)

    if not deployments:
        print("No deployments found.")
        return

    print("\nAvailable deployments:")
    for i, deployment in enumerate(deployments, start=1):
        print(f"{i}. {deployment}")

    choices = input("\nEnter the numbers of the deployments to scale (comma-separated): ")
    try:
        selected_indices = [int(choice.strip()) - 1 for choice in choices.split(",")]
        selected_deployments = [deployments[i] for i in selected_indices if 0 <= i < len(deployments)]
    except (ValueError, IndexError):
        print("Invalid input. Please enter valid numbers.")
        return

    if not selected_deployments:
        print("No valid deployments selected.")
        return

    try:
        replicas = int(input("\nEnter the number of replicas to scale to (default is 1): ") or 1)
        if replicas < 0:
            raise ValueError("Number of replicas cannot be negative.")
    except ValueError as e:
        print(f"Invalid input for replicas: {e}")
        return

    print(f"\nSelected deployments to scale: {', '.join(selected_deployments)}")
    downscale_deployments(context, selected_deployments, replicas)

if __name__ == "__main__":
    main()