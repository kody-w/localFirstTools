import json
import os
import logging
import re
from datetime import datetime, timedelta, timezone

_USE_AZURE_STORAGE = os.environ.get('USE_AZURE_STORAGE', 'true').lower() == 'true'
if _USE_AZURE_STORAGE:
    try:
        from azure.storage.file import FileService
    except ImportError:
        logging.warning("Azure Storage File SDK not found.")
        _USE_AZURE_STORAGE = False
else:
    logging.info("USE_AZURE_STORAGE is false. Using local file system.")

def safe_json_loads(json_str):
    if not json_str: return {}
    try:
        if isinstance(json_str, (dict, list)): return json_str
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {}

class AzureFileStorageManager:
    def __init__(self):
        self.share_name = os.environ.get('AZURE_FILES_SHARE_NAME', 'local-share')
        self.shared_memory_path = "shared_memories"
        self.default_file_name = 'memory.json'
        self.current_guid = None
        self.local_base_path = os.environ.get('LOCAL_STORAGE_BASE_PATH', '/app/local_storage')

        if _USE_AZURE_STORAGE:
            storage_connection = os.environ.get('AzureWebJobsStorage', '')
            connection_parts = dict(part.split('=', 1) for part in storage_connection.split(';'))
            self.account_name = connection_parts.get('AccountName')
            self.account_key = connection_parts.get('AccountKey')
            self.file_service = FileService(account_name=self.account_name, account_key=self.account_key)
            self._ensure_azure_share_exists()
        else:
            self._ensure_local_share_exists()
        
        self.current_memory_path = os.path.join(self.share_name, self.shared_memory_path)

    def _ensure_azure_share_exists(self):
        try:
            self.file_service.create_share(self.share_name, fail_on_exist=False)
            self._ensure_directory_exists_azure(self.shared_memory_path)
            try:
                self.file_service.get_file_properties(self.share_name, self.shared_memory_path, self.default_file_name)
            except Exception:
                self.file_service.create_file_from_text(self.share_name, self.shared_memory_path, self.default_file_name, '{}')
        except Exception as e:
            logging.error(f"Error ensuring Azure share: {str(e)}")

    def _ensure_local_share_exists(self):
        try:
            os.makedirs(os.path.join(self.local_base_path, self.share_name, self.shared_memory_path), exist_ok=True)
            local_file = os.path.join(self.local_base_path, self.share_name, self.shared_memory_path, self.default_file_name)
            if not os.path.exists(local_file):
                with open(local_file, 'w') as f: f.write('{}')
        except Exception as e:
            logging.error(f"Error ensuring local share: {str(e)}")

    def set_memory_context(self, guid=None):
        if _USE_AZURE_STORAGE: return self._set_memory_context_azure(guid)
        else: return self._set_memory_context_local(guid)

    def _set_memory_context_azure(self, guid):
        if not guid:
            self.current_guid = None
            self.current_memory_path = self.shared_memory_path
            return True
        guid_dir = f"memory/{guid}"
        try:
            self.file_service.get_file_properties(self.share_name, guid_dir, "user_memory.json")
            self.current_guid = guid
            self.current_memory_path = guid_dir
            return True
        except Exception:
            self._ensure_directory_exists_azure(guid_dir)
            self.file_service.create_file_from_text(self.share_name, guid_dir, "user_memory.json", '{}')
            self.current_guid = guid
            self.current_memory_path = guid_dir
            return True

    def _set_memory_context_local(self, guid):
        if not guid:
            self.current_guid = None
            self.current_memory_path = os.path.join(self.share_name, self.shared_memory_path)
            return True
        guid_dir = f"memory/{guid}"
        local_dir = os.path.join(self.local_base_path, self.share_name, guid_dir)
        os.makedirs(local_dir, exist_ok=True)
        local_file = os.path.join(local_dir, "user_memory.json")
        if not os.path.exists(local_file):
            with open(local_file, 'w') as f: f.write('{}')
        self.current_guid = guid
        self.current_memory_path = os.path.join(self.share_name, guid_dir)
        return True

    def read_json(self):
        if _USE_AZURE_STORAGE: return self._read_json_azure()
        else: return self._read_json_local()

    def _read_json_azure(self):
        path = self.current_memory_path if self.current_guid else self.shared_memory_path
        file = "user_memory.json" if self.current_guid else self.default_file_name
        try:
            content = self.file_service.get_file_to_text(self.share_name, path, file)
            return safe_json_loads(content.content)
        except Exception: return {}

    def _read_json_local(self):
        local_path = os.path.join(self.local_base_path, self.current_memory_path, "user_memory.json" if self.current_guid else self.default_file_name)
        try:
            with open(local_path, 'r') as f: return safe_json_loads(f.read())
        except Exception: return {}

    def write_json(self, data):
        if _USE_AZURE_STORAGE: self._write_json_azure(data)
        else: self._write_json_local(data)

    def _write_json_azure(self, data):
        path = self.current_memory_path if self.current_guid else self.shared_memory_path
        file = "user_memory.json" if self.current_guid else self.default_file_name
        self.file_service.create_file_from_text(self.share_name, path, file, json.dumps(data, indent=4))

    def _write_json_local(self, data):
        local_path = os.path.join(self.local_base_path, self.current_memory_path, "user_memory.json" if self.current_guid else self.default_file_name)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'w') as f: f.write(json.dumps(data, indent=4))

    def ensure_directory_exists(self, directory_name):
        if _USE_AZURE_STORAGE: return self._ensure_directory_exists_azure(directory_name)
        else:
             local_dir = os.path.join(self.local_base_path, self.share_name, directory_name)
             os.makedirs(local_dir, exist_ok=True)
             return True

    def _ensure_directory_exists_azure(self, directory_name):
        if not directory_name: return False
        self.file_service.create_share(self.share_name, fail_on_exist=False)
        parts = directory_name.split('/')
        current = ""
        for part in parts:
            if part:
                current = f"{current}/{part}" if current else part
                self.file_service.create_directory(self.share_name, current, fail_on_exist=False)
        return True

    def write_file(self, directory, filename, content):
        if _USE_AZURE_STORAGE:
            self._ensure_directory_exists_azure(directory)
            self.file_service.create_file_from_text(self.share_name, directory, filename, str(content))
            return True
        else:
            path = os.path.join(self.local_base_path, self.share_name, directory, filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f: f.write(str(content))
            return True

    def read_file(self, directory, filename):
        if _USE_AZURE_STORAGE:
            try: return self.file_service.get_file_to_text(self.share_name, directory, filename).content
            except: return None
        else:
            path = os.path.join(self.local_base_path, self.share_name, directory, filename)
            try:
                with open(path, 'r') as f: return f.read()
            except: return None
    
    def list_files(self, directory_name):
        # Simplified list_files for local
        if not _USE_AZURE_STORAGE:
            local_dir = os.path.join(self.local_base_path, self.share_name, directory_name)
            files = []
            if os.path.exists(local_dir):
                for item in os.listdir(local_dir):
                    if os.path.isfile(os.path.join(local_dir, item)):
                         # Mock object to match Azure SDK structure
                        files.append(type('obj', (object,), {'name': item})())
            return files
        else:
             return list(self.file_service.list_directories_and_files(self.share_name, directory_name))
