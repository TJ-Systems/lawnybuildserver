"""Build Server Creation"""
#! /usr/bin/python2.7

#Copyright 2017 lawny.co

import argparse
import os
import time
from six.moves import input
import googleapiclient.discovery
from oauth2client.client import GoogleCredentials
CREDENTIALS = GoogleCredentials.get_application_default()

COMPUTE = googleapiclient.discovery.build('compute', 'v1')

 #[START list_instance_groups]
def list_instance_groups(compute, project, zone):
    """ list all the instance groups in project/zone """
    result = compute.instanceGroups().list(project=project, zone=zone).execute()
    return result['items']
# [END list_instance_groups]

# [START list_instances]
def list_instances(compute, project, zone):
    """ list all the instance in project/zone """
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items']
# [END list_instances]

# [START create_instance_group]
def create_instance_group(compute, project, zone, igname):
    """ Create the new instance group """
    network_response = compute.network().get(
        project=project, network='devops').execute()
    network = network_response['selflink']

    subnetwork_response = compute.subnetwork().get(
        project=project, region=zone, subnetwork='buildservers').execute()
    subnetwork = subnetwork_response['selfLink']

    config = {
        'description': 'Instance Group for build server',
        'name': igname,
        'network': network,
        'region': zone,
        'subnetwork': subnetwork
    }

    return compute.instanceGroups().insert(
        project=project,
        zone=zone,
        body=config).execute()
# [END create_instance_group]

# [START create_instance]
def create_instance(compute, project, zone, servername):
    """ Create the new instance """
    # Get the latest Debian Jessie image.
    image_response = compute.images().getFromFamily(
        project='debian-cloud', family='debian-8').execute()
    source_disk_image = image_response['selfLink']

    # Configure the machine
    machine_type = "zones/%s/machineTypes/n1-standard-1" % zone
    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), 'sscript.sh'), 'r').read()
    config = {
        'name': servername,
        'machineType': machine_type,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [{
                # Startup script is automatically executed by the
                # instance upon startup.
                'key': 'startup-script',
                'value': startup_script
            }]
        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()
# [END create_instance]

# [START wait_for_operation]
def wait_for_operation(compute, project, zone, operation):
    """ Check the status of the current operation """
    print 'Waiting for operation to finish...'
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print "done."
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)
# [END wait_for_operation]

# [START build the storage]
## create a google cloud storage bucket for file/artifact storage
# [END build the storage]

# [START artifact upload]
## Upload required artifacts to cloud storage
# [END artifact upload]

# [Build the instance]
def main(project, zone, igname, instance_name, wait=False):
    """ Execution of the steps """
    compute = googleapiclient.discovery.build('compute', 'v1')

    print 'Creating Instance Group...'

    operation = create_instance_group(compute, project, zone, igname)
    wait_for_operation(compute, project, zone, operation['name'])

    instancegroups = list_instance_groups(compute, project, zone)

    print 'Instance groups in project %s and zone %s:' % (project, zone)
    for instancegroup in instancegroups:
        print ' - ' + instancegroup['name']

    print 'Creating instance...'

    operation = create_instance(compute, project, zone, instance_name)
    wait_for_operation(compute, project, zone, operation['name'])

    instances = list_instances(compute, project, zone)

    print 'Instances in project %s and zone %s:' % (project, zone)
    for instance in instances:
        print ' - ' + instance['name']

    print """
Instance created.
"""
    if wait:
        input()

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    PARSER.add_argument('project_id', help='Your Google Cloud project ID.')
    PARSER.add_argument(
        '--zone',
        default='us-central1-f',
        help='Compute Engine zone to deploy to.')
    PARSER.add_argument(
        '--igname', default='demo-instance', help='Instance group name.')
    PARSER.add_argument(
        '--name', default='demo-instance', help='New instance name.')

    ARGS = PARSER.parse_args()

    main(ARGS.project_id, ARGS.zone, ARGS.igname, ARGS.name)
# [END run]
