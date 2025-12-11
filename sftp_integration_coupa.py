import paramiko
import os
import json

# --- Configuration ---
# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

SFTP_HOST = config['sftp']['host']
SFTP_PORT = config['sftp']['port']
SFTP_USER = config['sftp']['user']
PRIVATE_KEY_PATH = config['sftp']['private_key_path']
LOCAL_IMPORT_FILE = config['files']['local_import_file']
REMOTE_IMPORT_PATH = config['sftp']['remote_import_dir'] + LOCAL_IMPORT_FILE
REMOTE_EXPORT_DIR = config['sftp']['remote_export_dir']
LOCAL_DOWNLOAD_DIR = config['files']['local_download_dir']

def sftp_connect():
    """Establishes an SFTP connection using an SSH private key."""
    try:
        ssh_client = paramiko.SSHClient()
        # Automatically add the host key (use this cautiously, or manage known_hosts)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Load the private key
        k = paramiko.RSAKey.from_private_key_file(PRIVATE_KEY_PATH)
        
        # Connect
        ssh_client.connect(
            hostname=SFTP_HOST, 
            port=SFTP_PORT, 
            username=SFTP_USER, 
            pkey=k,
            timeout=30
        )
        sftp_client = ssh_client.open_sftp()
        print("Successfully connected to SFTP server.")
        return ssh_client, sftp_client
    except Exception as e:
        print(f"SFTP Connection Error: {e}")
        return None, None

def import_requisitions(sftp):
    """Uploads a requisition file to the Coupa Incoming directory."""
    try:
        print(f"Uploading {LOCAL_IMPORT_FILE} to {REMOTE_IMPORT_PATH}...")
        sftp.put(LOCAL_IMPORT_FILE, REMOTE_IMPORT_PATH)
        print("File uploaded successfully. Coupa will begin processing shortly.")
    except FileNotFoundError:
        print(f"Local file not found: {LOCAL_IMPORT_FILE}")
    except Exception as e:
        print(f"Upload Error: {e}")

def export_requisitions(sftp):
    """Downloads all files from the Coupa Outgoing directory."""
    try:
        files_to_download = sftp.listdir(REMOTE_EXPORT_DIR)
        print(f"Found {len(files_to_download)} files in {REMOTE_EXPORT_DIR}: {files_to_download}")
        
        if not os.path.exists(LOCAL_DOWNLOAD_DIR):
            os.makedirs(LOCAL_DOWNLOAD_DIR)

        for filename in files_to_download:
            if filename not in ['.', '..']:
                remote_path = os.path.join(REMOTE_EXPORT_DIR, filename).replace('\\', '/')
                local_path = os.path.join(LOCAL_DOWNLOAD_DIR, filename)
                
                print(f"Downloading {filename}...")
                sftp.get(remote_path, local_path)
                print(f"Downloaded to {local_path}. Deleting remote file...")
                
                # --- BEST PRACTICE: Delete file after successful download ---
                sftp.remove(remote_path)
                print(f"Remote file {filename} deleted.")
    except Exception as e:
        print(f"Export Error: {e}")

if __name__ == '__main__':
    ssh, sftp = sftp_connect()
    
    if sftp:
        # Example 1: Import Requisitions (Upload)
        # (Ensure your 'new_requisitions.csv' is correctly formatted in the local path)
        import_requisitions(sftp)
        
        # Example 2: Export Requisitions (Download)
        export_requisitions(sftp)
        
        # --- Clean up connections ---
        sftp.close()
        ssh.close()
        print("Connection closed.")