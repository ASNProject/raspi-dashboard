import os
import platform
import subprocess
from pathlib import Path


class SystemManager:
    """
    System Manager

    Mengelola fitur sistem Linux seperti:
    - Auto Start Dashboard
    - Restart Dashboard
    - Shutdown
    - Reboot
    - Restart Service
    """

    SERVICE_NAME = "panzer-dashboard.service"

    SERVICE_PATH = f"/etc/systemd/system/{SERVICE_NAME}"

    # ==========================================================
    # SYSTEM
    # ==========================================================

    @staticmethod
    def is_linux():

        return platform.system() == "Linux"

    @staticmethod
    def is_windows():

        return platform.system() == "Windows"

    @staticmethod
    def is_raspberry_pi():

        if not SystemManager.is_linux():
            return False

        try:

            with open("/proc/device-tree/model") as f:

                return "Raspberry Pi" in f.read()

        except Exception:

            return False

    @staticmethod
    def is_orange_pi():

        if not SystemManager.is_linux():
            return False

        try:

            with open("/proc/device-tree/model") as f:

                return "Orange Pi" in f.read()

        except Exception:

            return False

    # ==========================================================
    # SERVICE
    # ==========================================================

    @classmethod
    def service_exists(cls):

        return os.path.exists(
            cls.SERVICE_PATH
        )

    @classmethod
    def is_autostart_enabled(cls):

        if not cls.is_linux():
            return False

        result = subprocess.run(
            [
                "systemctl",
                "is-enabled",
                cls.SERVICE_NAME,
            ],
            capture_output=True,
            text=True,
        )

        return result.stdout.strip() == "enabled"

    @classmethod
    def enable_autostart(
            cls,
            service_file,
    ):

        if not cls.is_linux():
            raise RuntimeError(
                "Auto Start hanya tersedia di Linux."
            )

        subprocess.run(
            [
                "sudo",
                "cp",
                service_file,
                cls.SERVICE_PATH,
            ],
            check=True,
        )

        subprocess.run(
            [
                "sudo",
                "systemctl",
                "daemon-reload",
            ],
            check=True,
        )

        subprocess.run(
            [
                "sudo",
                "systemctl",
                "enable",
                cls.SERVICE_NAME,
            ],
            check=True,
        )

    @classmethod
    def disable_autostart(cls):

        if not cls.is_linux():
            return

        subprocess.run(
            [
                "sudo",
                "systemctl",
                "disable",
                cls.SERVICE_NAME,
            ],
            check=False,
        )

        subprocess.run(
            [
                "sudo",
                "rm",
                "-f",
                cls.SERVICE_PATH,
            ],
            check=False,
        )

        subprocess.run(
            [
                "sudo",
                "systemctl",
                "daemon-reload",
            ],
            check=False,
        )

    # ==========================================================
    # SERVICE CONTROL
    # ==========================================================

    @classmethod
    def start_dashboard(cls):

        subprocess.run(
            [
                "sudo",
                "systemctl",
                "start",
                cls.SERVICE_NAME,
            ]
        )

    @classmethod
    def stop_dashboard(cls):

        subprocess.run(
            [
                "sudo",
                "systemctl",
                "stop",
                cls.SERVICE_NAME,
            ]
        )

    @classmethod
    def restart_dashboard(cls):

        subprocess.run(
            [
                "sudo",
                "systemctl",
                "restart",
                cls.SERVICE_NAME,
            ]
        )

    @classmethod
    def dashboard_status(cls):

        result = subprocess.run(
            [
                "systemctl",
                "status",
                cls.SERVICE_NAME,
                "--no-pager",
            ],
            capture_output=True,
            text=True,
        )

        return result.stdout

    # ==========================================================
    # POWER
    # ==========================================================

    @staticmethod
    def reboot():

        subprocess.run(
            [
                "sudo",
                "reboot",
            ]
        )

    @staticmethod
    def shutdown():

        subprocess.run(
            [
                "sudo",
                "shutdown",
                "-h",
                "now",
            ]
        )

    # ==========================================================
    # INFO
    # ==========================================================

    @staticmethod
    def hostname():

        return platform.node()

    @staticmethod
    def os_name():

        return platform.platform()

    @staticmethod
    def python_version():

        return platform.python_version()

    @staticmethod
    def architecture():

        return platform.machine()