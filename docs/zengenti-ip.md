---
title: Confirm IP
---
# Confirmation of Zengenti IP

Query pap https://pap.zengenti.com/apidocs/#/environments/get_environments_ to get full list of environments

Then cycle through the list of environments https://pap.zengenti.com/environment/lbtower
wit x-extra-fields virtual_hosts to match the search URL


inspect the response check x-origin-server: and if it matches backend-coordinator output or record that the site = blocks
If the x-origin-server: = a response starting z- output or record the site is classic
