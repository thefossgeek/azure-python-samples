#!/usr/bin/env python
#===============================================================================
#
#            FILE:  get-azure-keyvault-secret.py
# 
#           USAGE:  ./get-azure-keyvault-secret.py --help
# 
#     DESCRIPTION:  This script will get a specified secret from a given key vault 
#                   using Azure Key Vault using REST API.
#   
#   EXAMPLE USAGE:   ./get-azure-keyvault-secret.py -t <tenant-id> \
#                   -c <client-id> -s <client-secret> -k <keyvault_name> \
#                   -n <secret_name> -v <secret_version>
#
#
#
#===============================================================================
import os
import sys
import argparse
import requests
import json

def get_access_token(tenant_id, client_id, client_secret):
	"""

	Get OAuth2 access  token for REST API call

	"""
	resource='https://vault.azure.net'
	if client_id and client_secret and tenant_id and resource:
		token_url="https://login.windows.net/{0}/oauth2/token".format(tenant_id)
		payload = {'client_id':client_id, 'client_secret':client_secret, 'resource':resource, 'grant_type':'client_credentials'}
		response=requests.post(token_url, data=payload).json()
		access_token=response['access_token']
	else:
		raise ValueError("Couldn't get the key vault properties")
		sys.exit(0)

	return access_token

	

def get_secret(secret_name, secret_version, keyvault_name, access_token):
	"""

	Get a specified secret from a given key vault.	

	"""
	endpoint = 'https://{0}.vault.azure.net/secrets/{1}/{2}?api-version=2016-10-01'.format(keyvault_name, secret_name, secret_version)
	
	headers = {"Authorization": 'Bearer ' + access_token}
	
	response = requests.get(endpoint,headers=headers).json()
	
	return response['value']

def get_args():
	"""
	This method defines what arguments it requires, and it will figure out how to parse those out of `sys.argv`. 
	The method also automatically generates help and usage messages and issues errors when users give the program invalid arguments.	
	"""
	parser = argparse.ArgumentParser(
									description='Python script to get Azure Key Vault Secret using REST API',
                                    formatter_class = argparse.RawTextHelpFormatter
									)
	parser.add_argument('-c', '--client_id',
                        help='Application ID or Client ID value used to authenticate to Key-Vault, this is mandatory argument and default None',
                        metavar='<client-id>',
                        action='store',
                        required=True,
                       	default=None)
	parser.add_argument('-k', '--keyvault_name',
                        help='Name of the Azure Key Vault, this is mandatory argument and default None',
                        metavar='<keyvault-name>',
                        action='store',
                        required=True,
                       	default=None)
	parser.add_argument('-n', '--secret_name',
                        help='The name of the secret, this is mandatory argument and default None',
                        metavar='<secret-name>',
                        action='store',
                        required=True,
                       	default=None)
	parser.add_argument('-v', '--secret_version',
                        help='The version of the secret, this is mandatory argument and default None',
                        metavar='<secret-version>',
                        action='store',
                        required=True,
                       	default=None)
	parser.add_argument('-s', '--client_secret',
                        help='Client Secret used to authenticate to Key Vault, this is mandatory argument and default None',
                        metavar='<client-secret>',
                        action='store',
                        required=True,
                       	default=None)
	parser.add_argument('-t', '--tenant_id',
                        help='Azure AD Tenant ID, default FIS, this is mandatory argument and default None',
                        metavar='<tenant-id>',
                        action='store',
                        required=True,
                       	default=None)

	args = parser.parse_args()
	return args


def main():
	"""

	The main function which parse all the command line parameter and invoke REST API function.

	"""
	
	args = get_args()

	client_id = args.client_id

	keyvault_name = args.keyvault_name

	secret_name = args.secret_name

	secret_version = args.secret_version

	client_secret = args.client_secret

	tenant_id = args.tenant_id
	
	access_token = get_access_token(tenant_id, client_id, client_secret)
	
	secret_value = get_secret(secret_name, secret_version, keyvault_name, access_token)

	print secret_value

if __name__ == "__main__":
	main()
