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

On your monitoring server you need to place this file also in the plugins3party directory. On my server it was /etc/lib64/nagios/plugins/plugins3party and make it executable just like you did on the target sever above.

Then add the following to /etc/nagios/nrpe.cfg

    command[gitlab_nrpe_check]=/usr/lib64/nagios/plugins/gitlab_nrpe_check.py -H <<<your server ip>>>

The above assumes that you whitelisted the server to itself. If not, then use the Gitlab token

    command[gitlab_nrpe_check]=/usr/lib64/nagios/plugins/gitlab_nrpe_check.py -H <<<your server ip>>> -t <<<your gitlab token>>>

Make sure to restart Nagios NRPE service:

    systemctl restart nrpe

Don't foreget to check the status of NRPE too!

    systemctl status nrpe

Define new command in your nagios/naemon commands.cfg file on your monitoring server.

    define command {
      command_name                   gitlab_nrpe_check
      command_line                   $USER1$/plugins3party/gitlab_nrpe_check.py -H $HOSTADDRESS$
    }

    define service {
      service_description            gitlab_nrpe_check
      host_name                      pv-git
      use                            generic-service
      check_command                  gitlab_nrpe_check
      contact_groups                 admins
    }
