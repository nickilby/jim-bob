---
title: Tests
---
# Tests

1. **DNS Resolution**
   - Verify that the domain name resolves correctly.

2. **HTTP Response Codes**
   - Check the HTTP status codes returned by the server.

3. **Returned Headers**
   - Analyse the headers returned by the server.

4. **Zengenti Site Verification**
   - Verify if the site is hosted by Zengenti.

5. **Client/Environment/Project Discovery**
   - Identify the project and environment associated with the URL.

6. **Customer-Specific Tests**
   - Conduct tests on internal URLs associated with the customer project.
   - **Examples:**
     - External URL: [https://www.lse.ac.uk/](https://www.lse.ac.uk/)
     - Internal project URL: [https://live-else.cloud.contensis.com/](https://live-else.cloud.contensis.com/)
     - Internal server URLs:
       - [https://z-else-web1-live-else.cloud.contensis.com/](https://z-else-web1-live-else.cloud.contensis.com/)
       - [https://z-else-web2-live-else.cloud.contensis.com/](https://z-else-web2-live-else.cloud.contensis.com/)
   - Perform the same DNS and HTTP response code checks on


## Flow of tests

```mermaid
flowchart TD
    A[Required Tests] --> B[All Sites Global Tests]
    B --> C[Enter URL]
    C --> D[Website Response]
    D --> E[Status Code]
    D --> F[Latency]
    D --> G[DNS Response]
    D --> H[SSL True/False Days to expiry]
    D --> I[Cache TTL True/False]
    D --> J[Follow Redirects]

    D --> K[Based on Response]
    K --> L[Is URL a Zengenti URL based on DNS IP]

    L --> M[If Zengenti site perform extra tests]
    M --> N[JSON lookup information based on URL as the hostheader]
    N --> O[Return]
    O --> P[Customer Environment]
    O --> Q[Project]
    O --> R[Blocks]
    O --> S[App Server]
    O --> T[Web1/2]

    M --> U[Get live URL]
    M --> V[Get Web1/2 URL]
    V --> W[Perform Global tests on the 3 URLs]
    W --> B

    M --> X[Work out if the URL is a Redirect - Pass any info that we can]
    M --> Y[Work out if the URL is a Reverse Proxy - Pass any info that we can]
```