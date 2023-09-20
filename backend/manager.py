import paramiko
import docker


class manager:
    def __init__(self) -> None:
        super().__init__()

    def manager_SSH(self):
        # Just an example
        host = "YOUR_IP_ADDRESS"
        username = "YOUR_LIMITED_USER_ACCOUNT"
        password = "YOUR_PASSWORD"

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        _stdin, _stdout, _stderr = client.exec_command("df")
        print(_stdout.read().decode())
        client.close()

    def maneger_Docker(self, mode: str, remote_tls: bool = False):
        match mode:
            case "locate":
                client = docker.from_env()
                containers = client.containers.list()
                print(containers)
            case "remote":
                if remote_tls == True:
                    client = docker.DockerClient(base_url="tcp://127.0.0.1:2376")
                else:
                    client = docker.DockerClient(base_url="tcp://127.0.0.1:2375")
                print(client.containers.list())

    def manager_LocateShell(self):
        pass


class checker:
    def __init__(self) -> None:
        super().__init__()

    def check_Vol_2(self):
        pass

    def check_Vol_2_Libraries(self):
        pass

    def check_Vol_2_Plugins(self):
        pass

    def check_Vol_3(self):
        pass

    def check_Vol_3_Libraries(self):
        pass

    def check_Vol_3_Plugins(self):
        pass


core_manager = manager()
core_checker = checker()
