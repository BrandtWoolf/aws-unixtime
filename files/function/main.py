# Author: Brandt Woolf
# Date: 2021-08-07
# Inspiration from: https://towardsdatascience.com/extending-cloudformation-using-lambda-backed-custom-resources-c99b98cc7304

import requests
import logging
from crhelper import CfnResource

logger = logging.getLogger(__name__)

helper = CfnResource(
  json_logging=False,
  log_level='DEBUG',
  boto_level='CRITICAL'
)

def HttpGet(url):
  logger.info(f"Sending request to {url}")
  r = requests.get(url)
  if r.ok:
    logger.info(f"Status: {r.status_code} for URL: {url}")
    return r.text
  else:
    logger.error(f"Status: {r.status_code} for URL: {url}")
    r.raise_for_status()

def validate_attrs(attrs):
  valid_attrs = ['*', 'abbreviation',' client_ip',' datetime',' day_of_week',' day_of_year',' dst',' dst_from',' dst_offset',' dst_until',' raw_offset',' timezone',' unixtime',' utc_datetime',' utc_offset',' week_number']
  attrs = attrs.split(',')
  for attr in attrs:
    if not attr in valid_attrs:
      raise ValueError(f"{attr} not in {valid_attrs}")
  return attrs

def handler(event, context):
  helper(event, context)

@helper.create
def create(event, context):
  # log entry point and rest resource properties
  logger.info("Resource Created")
  ResourceProperties = event['ResourceProperties']

  # gather the requested zone
  zone = ResourceProperties['zone']
  logger.info(f"zone: {zone}")

  #gather the request attributes
  attrs = ResourceProperties['gather_attr']
  logger.info(f"attrs: {attrs}")

  validated_attrs = validate_attrs(attrs)
  logger.info(f"valid attrs: {validated_attrs}")

  logger.info("zone and valid attr(s) collected")

  # get list of valid zones
  zones = HttpGet('http://worldtimeapi.org/api/timezone')

  # check if requested zone is valid
  if zone not in zones:
    # raise error if zone not in http://worldtimeapi.org/api/timezone
    logger.error(f"zone {zone} not in {zones}")
    raise ValueError(f"zone {zone} not in {zones}")

  # get timezone info
  r = HttpGet(f"http://worldtimeapi.org/api/timezone/{zone}.txt")

  # parse timezone info into dict
  timezone = {}
  # split on newline first
  for line in r.split('\n'):
    # split on colon to get key value pair
    l = line.split(":")
    # created and assign new key pair
    timezone[l[0].strip()] = l[1].strip()
  # check for * to return all attrs
  if '*' in validated_attrs:
    for key in timezone:
      helper.Data[key] = timezone[key]
  # return the attrs included in validated_attrs
  else:
    for attr in validated_attrs:
       helper.Data[attr] = timezone[attr]

@helper.update
def update(event, context):
  logger.info("Resource Updated")
  return "NewPhysicalResourceId"

@helper.delete
def delete(event, context):
  logger.info("Resource Deleted")
