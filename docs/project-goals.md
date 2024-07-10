---
title: Goals
---
# Goals

Develop a web application that allows users to input a URL and receive a comprehensive health report based on a series of tests. The app will be accessible via a web frontend and will not rely on our internal infrastructure to function. Additionally, we aim to come up with a catchy and meaningful name for the app.

## Overview

The objective is to create a standalone app that evaluates the health of a given URL by performing various tests and presenting the results in a user-friendly manner. The app will not only check the URL but also delve into related infrastructure components if necessary. The primary features and tests could include:

- **DNS Resolution**: Verify that the domain name resolves correctly.
- **HTTP Response Codes**: Check the HTTP status codes returned by the server.
- **Returned Headers**: Analyze the headers returned by the server.
- **Upstream Provider Availability**: Assess the availability of upstream providers.
- **Disaster Recovery (DR) Scenario Status**: Check the status of DR scenarios.
- **VMware Host Resource Usage**: Monitor resource usage on VMware hosts.
- **Container Health**: Check the status of container deployments.
- **IIS Status**: Verify the status of IIS servers.
- **Query Prometheus Metrics**: Fetch and analyze metrics from Prometheus.
- **VIP Status/Location**: Determine the status and location of VIPs (Virtual IPs).
- **Database Responses**: Check the responsiveness of databases.

Given the complexity and scale of our infrastructure, this app aims to reduce the time to resolution for any issues that arise, enhancing our operational efficiency and reliability.

Basic Example

[http://up.zengenti.io:8000/](http://up.zengenti.io:8000/)
