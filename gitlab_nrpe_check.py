#!/usr/bin/env python

import urllib2
import argparse
import json
import logging as log

# Nagios Exit Codes
# 0	OK
NAGIOS_OK_EXIT_CODE = 0
# 1	WARNING
# NAGIOS_WARNING_EXIT_CODE = 1
# 2	CRITICAL
NAGIOS_CRITICAL_EXIT_CODE = 2
# 3	UNKNOWN
NAGIOS_UNKNOWN_EXIT_CODE = 3


def get_jsonparsed_data(url):
    """
    Receive the content of url and return the object as JSON.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """

    try:
        URL_REQUEST = urllib2.Request(url)
        RESPONSE = urllib2.urlopen(URL_REQUEST)
    except urllib2.URLError as e:
        exit_gracefully(NAGIOS_UNKNOWN_EXIT_CODE,
                        e.reason)
    data = RESPONSE.read().decode("utf-8")
    return json.loads(data)


def exit_gracefully(exitcode, message=''):
    """ Exit gracefully with exit code and (optional) message

    Parameters
    ----------
    exitcode : int
    message  : str (optional)

    Returns
    -------
    exit

    """

    log.debug('Exiting with status {0}. Message: {1}'.format(exitcode,
                                                             message))

    if message:
        print(message)

    exit(exitcode)


def main():
    """ Main routine """

    parser = argparse.ArgumentParser(description='GitLab NRPE Check')
    #
    parser.add_argument('-H',
                        '--host',
                        help='Hostname of the Gitlab server',
                        required=True)

    parser.add_argument('-t',
                        '--token',
                        help='User token for the Gitlab server',
                        default='')

    parser.add_argument('-x',
                        '--extended',
                        help='Add extended information when possible',
                        action='store_true')

    args = parser.parse_args()

    base_url = 'http://{}'.format(args.host)

    # token is deprecated by GitLab but this plugin supports it as input
    # for compatibility.
    #
    # See GitLab web page for more information
    # https://docs.gitlab.com/ee/user/admin_area/monitoring/health_check.html
    #
    #
    # TOKEN = "FDUEDUV9gNe611ax431K"
    # curl http://gitlab.lancer-ins.com/-/readiness?token=FDUEDUV9gNe611ax431K

    TOKEN_PROVIDED = (args.token)

    EXTENDED = (args.extended)

    GITLAB_URL = base_url + "/-/readiness"

    if (TOKEN_PROVIDED != ''):
        GITLAB_URL = GITLAB_URL+"?token="+str(TOKEN_PROVIDED)

    MY_JSON = get_jsonparsed_data(GITLAB_URL)

    FORMATTED_JSON = (json.dumps(MY_JSON,
                      indent=4,
                      sort_keys=True))

    GITALY_CHECK = str(MY_JSON["gitaly_check"]
                       ["status"])

    if (GITALY_CHECK != "ok"):
        if EXTENDED:
            ERROR_MESSAGE = ("gitaly_check: " +
                             str(MY_JSON["gitaly_check"]
                                 ["status"] +
                                 "\n" +
                                 FORMATTED_JSON))
        else:
            ERROR_MESSAGE = ("gitaly_check: " +
                             str(MY_JSON["gitaly_check"]
                                 ["status"]))

        exit_gracefully(NAGIOS_CRITICAL_EXIT_CODE,
                        ERROR_MESSAGE)

    CACHE_CHECK = str(MY_JSON["cache_check"]
                      ["status"])

    if (CACHE_CHECK != "ok"):
        if EXTENDED:
            ERROR_MESSAGE = ("cache_check: " +
                             str(MY_JSON["cache_check"]
                                 ["status"] +
                                 "\n" +
                                 FORMATTED_JSON))
        else:
            ERROR_MESSAGE = ("cache_check: " +
                             str(MY_JSON["cache_check"]
                                 ["status"]))

        exit_gracefully(NAGIOS_CRITICAL_EXIT_CODE,
                        ERROR_MESSAGE)
    #
    DB_CHECK = str(MY_JSON["db_check"]
                   ["status"])

    if (DB_CHECK != "ok"):
        if EXTENDED:
            ERROR_MESSAGE = ("db_check: " +
                             str(MY_JSON["db_check"]
                                 ["status"] +
                                 "\n" +
                                 FORMATTED_JSON))
        else:
            ERROR_MESSAGE = ("db_check: " +
                             str(MY_JSON["db_check"]
                                 ["status"]))

        exit_gracefully(NAGIOS_CRITICAL_EXIT_CODE,
                        ERROR_MESSAGE)

    REDIS_CHECK = str(MY_JSON["redis_check"]
                      ["status"])

    if (REDIS_CHECK != "ok"):
        if EXTENDED:
            ERROR_MESSAGE = ("redis_check: " +
                             str(MY_JSON["redis_check"]
                                 ["status"] +
                                 "\n" +
                                 FORMATTED_JSON))
        else:
            ERROR_MESSAGE = ("redis_check: " +
                             str(MY_JSON["redis_check"]
                                 ["status"]))

        exit_gracefully(NAGIOS_CRITICAL_EXIT_CODE,
                        ERROR_MESSAGE)

    QUEUES_CHECK = str(MY_JSON["queues_check"]
                       ["status"])

    if (QUEUES_CHECK != "ok"):
        if EXTENDED:
            ERROR_MESSAGE = ("queues_check: " +
                             str(MY_JSON["queues_check"]
                                 ["status"] +
                                 "\n" +
                                 FORMATTED_JSON))
        else:
            ERROR_MESSAGE = ("queues_check: " +
                             str(MY_JSON["queues_check"]
                                 ["status"]))

        exit_gracefully(NAGIOS_CRITICAL_EXIT_CODE,
                        ERROR_MESSAGE)

    SHARED_STATE_CHECK = str(MY_JSON["shared_state_check"]
                             ["status"])

    if (SHARED_STATE_CHECK != "ok"):
        if EXTENDED:
            ERROR_MESSAGE = ("shared_state_check: " +
                             str(MY_JSON["shared_state_check"]
                                 ["status"] +
                                 "\n" +
                                 FORMATTED_JSON))
        else:
            ERROR_MESSAGE = ("shared_state_check: " +
                             str(MY_JSON["shared_state_check"]
                                 ["status"]))

        exit_gracefully(NAGIOS_CRITICAL_EXIT_CODE,
                        ERROR_MESSAGE)

    # All is good so exit with a zero return code
    if EXTENDED:
        ERROR_MESSAGE = ("all checks are ok" +
                         "\n" +
                         FORMATTED_JSON)
    else:
        ERROR_MESSAGE = ("all checks are ok")

    exit_gracefully(NAGIOS_OK_EXIT_CODE,
                    ERROR_MESSAGE)


if (__name__ == "__main__"):
    main()
