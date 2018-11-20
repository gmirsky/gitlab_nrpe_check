#GitLab NRPE Check Plugin

gitlab_nrpe_check.py

optional arguments:

 ** -h, --help**            show this help message and exit

  **-H HOST, --host HOST**  Hostname of the Gitlab server

  **-t TOKEN, --token TOKEN** User token for the Gitlab server

  **-x, --extended **       Add extended information. This will include the JSON sent back from the GitLab server.

**Note: ** token is deprecated by GitLab as of version 9.4 but this plugin supports it as input for compatibility. See the GitLab web page for more information about whitelisting your monitoring server:

[https://docs.gitlab.com/ee/user/admin_area/monitoring/health_check.html](https://docs.gitlab.com/ee/user/admin_area/monitoring/health_check.html "https://docs.gitlab.com/ee/user/admin_area/monitoring/health_check.html")

Place this script in /usr/lib64/nagios/plugins/gitlab_nrpe_check.py and make it executable:

```bash
chmod +x /usr/lib64/nagios/plugins/gitlab_nrpe_check.py
```

add

    command[gitlab_check]=/usr/lib64/nagios/plugins/gitlab_nrpe_check.py


Make sure to restart Nagios NRPE service:

    systemctl restart nrpe


Define new command in /etc/nagios/objects/commands.cfg

    define command{
            command_name    gitlab_check
            command_line    $USER1$/check_nrpe -H $HOSTADDRESS$ -c gitlab_check
            }
