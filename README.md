# Mage

1. Clone the repository:
    ```
    git clone <repository_url>
    cd Status
    ```

2. Create a virtual environment and activate it:
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Run the application:
    ```
    python ./src/jim_bob/main.py
    ```

## Usage
Open your web browser and go to `http://127.0.0.1:8000`. Enter the URL you want to check
in the provided input box and click "Check".


#### Flow of tests
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
