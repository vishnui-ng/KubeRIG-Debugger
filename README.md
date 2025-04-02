# KubeRIG Debugger

This project provides three scripts for managing Kubernetes deployments:
1. **Downscale Deployments**: Scale down selected deployments to a specified number of replicas (restricted to the `sec` - Secondary RIG/environment).
2. **Fetch Logs**: Fetch logs from selected deployments and organize them in a structured folder hierarchy.
3. **Delete Pods**: Delete all pods under a deployment or specific pods interactively (restricted to the `sec` environment).

---

## Important Note

This project is designed for personal use in the `sec` (Secondary RIG) environment. The `sec` environment is often broken or does not log everything to JARVIS, making these scripts useful for debugging and testing. 

### Restrictions:
- **Scaling Operations**: The `scale_down.py` script is restricted to the `sec` environment. Users should not modify other environments (e.g., `dest`, `source`) unless absolutely necessary.
- **Log Retrieval**: The `fetch_logs.py` script can be used to pull logs from any environment.
- **Pod Deletion**: The `delete_pods.py` script is restricted to the `sec` environment.

---

## Project Structure

```
KubeRIG-Debugger/
│
├── scripts/
│   ├── scale_down.py
│   ├── fetch_logs.py
│   ├── delete_pods.py
│   └── utils/
│       └── k8s_helpers.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Requirements

- Python 3.x
- Access to a Kubernetes cluster
- `kubectl` installed and configured
- `pytz` library for timezone handling

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd KubeRIG-Debugger
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### 1. Downscale Deployments

This script allows you to scale down selected deployments to a specified number of replicas. **Scaling operations are restricted to the `sec` environment.**

Run the script:
```bash
python scripts/scale_down.py
```

Follow the interactive prompts:
- Select the Kubernetes context by number.
- Choose the deployments to scale down.
- Specify the number of replicas (default is 1).

---

### 2. Fetch Logs

This script fetches logs from selected deployments and organizes them in a structured folder hierarchy:
- **Context**: Folder for the Kubernetes context.
- **Date**: Folder for the current date in `MMDDYYYY` format.
- **Time**: Folder for the current time in `HHMM` format (PST).
- **Deployment**: Folder for deployments with multiple pods. Logs are saved as `<pod_name>.log`.

Run the script:
```bash
python scripts/fetch_logs.py
```

Follow the interactive prompts:
- Select the Kubernetes context by number.
- Choose the deployments to fetch logs from.
- Specify the directory to save logs (default is `logs`).

---

### 3. Delete Pods

This script allows you to delete all pods under a deployment or specific pods interactively. **Pod deletion operations are restricted to the `sec` environment.**

Run the script:
```bash
python scripts/delete_pods.py
```

Follow the interactive prompts:
- Select the Kubernetes context by number.
- Choose the deployments to delete pods from.
- Choose to delete all pods or specific pods.

---

## Example Folder Structure for Logs

For context `sec`, date `04012025`, and time `1430`:
```
logs/
└── sec/
    └── 04012025/
        └── 1430/
            ├── deployment-a/
            │   ├── pod-a1.log
            │   └── pod-a2.log
            ├── deployment-b/
            │   ├── pod-b1.log
            │   └── pod-b2.log
            └── pod-c1.log  # Single pod for deployment-c
```

---

## Adding Kubernetes Configurations for New Environments

To use this project with your Kubernetes environments, you need to configure your `~/.kube/config` file. Below are the steps to add a new environment:

### 1. Locate Your Kubernetes Configuration
- The Kubernetes configuration file is typically located at `/etc/kubernetes/admin.conf` on your Kubernetes master node.
- Copy this file to your local machine or directly append its contents to your `~/.kube/config` file.

### 2. Add the Configuration
- Open your `~/.kube/config` file.
- Append the contents of your Kubernetes configuration file (`admin.conf`) under the appropriate sections:
  - **clusters**: Add a new cluster entry with the `name` and `server` details.
  - **contexts**: Add a new context entry with the `name` and associated cluster and user.
  - **users**: Add a new user entry with the `name`, `client-certificate-data`, and `client-key-data`.

### 3. Naming Conventions
- Use meaningful names for clusters and contexts. For example:
  - Cluster names: `dest-cluster`, `sec-cluster`, `source-cluster`.
  - Context names: `dest`, `sec`, `source`.
- Ensure the `current-context` is set to the context you want to use by default.

### Example Configuration
Here is an example of how your `~/.kube/config` file should look after adding a new environment:

```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: REDACTED
    server: https://10.193.145.139:6443
  name: sec-cluster
contexts:
- context:
    cluster: sec-cluster
    user: sec-admin
  name: sec
current-context: sec
kind: Config
preferences: {}
users:
- name: sec-admin
  user:
    client-certificate-data: REDACTED
    client-key-data: REDACTED
```

---

## .gitignore

Ensure the following files and folders are ignored:
- `logs/`: The folder where logs are saved.
- Python cache files.

Add the following to `.gitignore`:
```
logs/
__pycache__/
*.pyc
*.pyo
```

---

## Troubleshooting

1. **kubectl not found**:
   Ensure `kubectl` is installed and configured correctly:
   ```bash
   kubectl version --client
   ```

2. **Permission issues**:
   Ensure you have the necessary permissions to access the Kubernetes cluster.

3. **Missing dependencies**:
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## Conclusion

**KubeRIG Debugger** provides three interactive scripts for managing Kubernetes deployments. The downscale script allows you to scale down deployments in the `sec` environment, the log-fetching script retrieves logs and organizes them in a structured folder hierarchy, and the pod deletion script allows you to delete pods interactively. Ensure you have the necessary permissions and kubeconfig set up to interact with your Kubernetes cluster.s