# aws-unixtime

Proof of concept for leveraging Ansible to deploy an AWS CloudFormation stack containing a Lambda via a custom resource.

The purpose of the Lambda is to take an input of a timezone in the state/province format, and the output of the stack will return the specific timezone variable information

## Setup

### AWS Credentials

First thing is to setup your aws config in `~/.aws/config`:

```ini
[default]
region={{ region }}
output=json
aws_access_key_id={{ your_access_key_id }}
aws_secret_access_key={{ your_secret_access_key }}
```

See documentation for more info: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

### Local Environment

```bash
git clone https://github.com/bwoolf1122/aws-unixtime.git
python3 -m venv venv/
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

Once your environnement is setup, you can now run the following commands:

### Deploy Stack

#### Variables

##### Default

```yaml
time_zone: "Europe/London"
time_zone_attrs: "*"
```

##### Valid

Valid `time_zone_attrs` can be supplied in a command seperated list:

```
*
abbreviation
client_ip
datetime
day_of_week
day_of_year
dst
dst_from
dst_offset
dst_until
raw_offset
timezone
unixtime
utc_datetime
utc_offset
week_number
```

### Deploy Command

```bash
ansible-playbook ansible-build.yml
```

Once this is run, `host_vars/localhost.yml` will be created with the stack and bucket name. NOTE: its best to leave this file be and let Ansible manage this

### Destroy Stack

The stack and bucket name will be read from `host_vars/localhost.yml`. __Once they have been destroyed, the local config information will be deleted__

```bash
ansible-playbook ansible-build.yml -e '{deploy: false, destroy: true}'
```
