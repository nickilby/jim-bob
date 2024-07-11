import requests
from urllib.parse import urljoin
from dotenv import load_dotenv
import os

# Specify the path to the .secrets file
load_dotenv('.secrets')

username = os.getenv('PROMETHEUS_USERNAME')
password = os.getenv('PROMETHEUS_PASSWORD')

print(f"username: {username}")
print(f"password: {password}")

class PrometheusQuery:
    """Methods for accessing the Prometheus server."""

    def __init__(self, url="https://prometheus.zengenti.io/", username=None, password=None):
        """
        Set up the configuration for the Prometheus server.

        Parameters:
        url (str): The base URL of the Prometheus server.
        username (str): The username for basic authentication (optional).
        password (str): The password for basic authentication (optional).
        """
        self.url = url
        self.username = username
        self.password = password

    def query_prometheus(self, query, timeout=10, verify_ssl=True):
        """
        Query the Prometheus server.

        Parameters:
        query (str): The PromQL query string.
        timeout (int): The timeout for the request in seconds. Default is 30 seconds.
        verify_ssl (bool): Whether to verify SSL certificates. Default is True.

        Returns:
        dict or None: The result of the query if successful, None otherwise.
        """
        # Construct the full URL for the query
        full_url = urljoin(self.url, "api/v1/query")
        
        # Define the parameters for the query
        params = {
            'query': query
        }

        try:
            # Send the request to the Prometheus server with a timeout and SSL verification
            response = requests.get(full_url, params=params, timeout=timeout, verify=verify_ssl, auth=(self.username, self.password) if self.username and self.password else None)
            
            # Print the full URL for debugging
            print(f"Request URL: {response.url}")
            
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                result = response.json()
                
                # Check if the query was successful
                if result['status'] == 'success':
                    return result['data']['result']
                else:
                    print(f"Query failed: {result.get('error', 'Unknown error')}")
            else:
                print(f"Request failed with status code {response.status_code}")
        
        except requests.exceptions.Timeout:
            print("The request timed out")
        except requests.exceptions.SSLError:
            print("SSL verification failed")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        
        return None

# Example usage
prometheus = PrometheusQuery(username=username, password=password)
query = "probe_http_duration_seconds"
data = prometheus.query_prometheus(query, timeout=30, verify_ssl=True)  # Enable SSL verification for production

# Print the result
print(data)
