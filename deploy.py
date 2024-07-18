import os
import tarfile
import io
from kubernetes import client, config
from kubernetes.stream import stream

def copy_file_to_pod(core_v1_api, namespace, pod_name, src_file, dest_path, container_name=None):
    # Read the local file content
    with open(src_file, 'rb') as f:
        file_content = f.read()

    # Create a tar archive with the file
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode='w') as tar:
        tarinfo = tarfile.TarInfo(name=os.path.basename(dest_path))
        tarinfo.size = len(file_content)
        tar.addfile(tarinfo, io.BytesIO(file_content))

    # Move the buffer position to the beginning
    tar_buffer.seek(0)

    # Create the command to extract the tar file
    command = ['tar', 'xvf', '-', '-C', '/']

    # Execute the command in the pod
    exec_stream = stream(
        core_v1_api.connect_get_namespaced_pod_exec,
        name=pod_name,
        namespace=namespace,
        command=command,
        container=container_name,
        stderr=True,
        stdin=True,
        stdout=False,
        tty=False,
        _preload_content=False
    )
    
    commands = []
    commands.append(tar_buffer.read())
    
    while exec_stream.is_open():
        exec_stream.update(timeout=1)
        if exec_stream.peek_stdout():
            print(f"STDOUT: {exec_stream.read_stdout()}")
        if exec_stream.peek_stderr():
            print(f"STDERR: {exec_stream.read_stderr()}")
        if commands:
            c = commands.pop(0)
            exec_stream.write_stdin(c.decode())
        else:
            break
    
    exec_stream.close()
        


if __name__ == "__main__":
    # Specify variables
    namespace = 'default'
    pod_name = ''
    src_file = 'user_program.py'
    dest_path = '/user_program.py'

    # Load kube config
    config.load_kube_config()
    # Initialize the Kubernetes API client
    core_v1_api = client.CoreV1Api()

    # Dynamically retrieve pod name
    pods = core_v1_api.list_namespaced_pod(namespace=namespace, label_selector="app=12345-environment")
    pod_name = [pod.metadata.name for pod in pods.items][0]

    copy_file_to_pod(core_v1_api, namespace, pod_name, src_file, dest_path)
