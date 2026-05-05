# SwiftDeploy: Declarative Stack Automation

SwiftDeploy is a custom CLI tool designed to automate the lifecycle of a containerized web stack. Instead of manual configuration, SwiftDeploy uses a single manifest.yaml as the source of truth to programmatically generate Nginx configurations, Docker Compose files, and manage service promotions.

---

## Features

  - Declarative Manifest: Define your entire infrastructure in one YAML file.

  -  Template-Driven: Configs are generated using Jinja2 templates (no manual editing).

  -  Automated Validation: 5-point pre-flight check for manifest validity, ports, and Docker images.

  -  Canary Support: Seamlessly promote services to canary mode with rolling restarts.

  -  Chaos Engineering: Activate a chaos endpoint in canary mode to simulate latency and errors.

   ##  Project Structure
   ```
.
├── app/
│   ├── main.py           # Python/Flask API with Chaos logic
│   └── requirements.txt  # Project dependencies
├── templates/
│   ├── docker-compose.yml.j2 # Jinja2 template for Docker
│   └── nginx.conf.j2         # Jinja2 template for Nginx
├── swiftdeploy           # The CLI Automation Tool (Python)
├── manifest.yaml         # The Single Source of Truth
├── Dockerfile            # Multi-stage build (Image < 50MB)
└── README.md             # This file
```

## Subcommand Walkthrough

### 1. Initialization

Generates nginx.conf and docker-compose.yml based on the current manifest.
```
./swiftdeploy init
```

### 2. Validation

Runs 5 pre-flight checks to ensure the stack is ready for deployment.
```
./swiftdeploy validate
```

### 3. Deployment

Generates configs, validates the environment, and brings the stack up.
```
./swiftdeploy deploy
```

### 4. Promotion

Switches the deployment mode (e.g., from stable to canary) in the manifest and performs a rolling restart of the service.
```
./swiftdeploy promote canary
```

### 5. Teardown

Removes all containers, networks, and volumes. Use --clean to remove generated configs.
```
./swiftdeploy teardown --clean
```

## Chaos Engineering (Canary Only)

When in `canary` mode, you can simulate degraded behavior via the `/chaos` endpoint:

### Trigger Latency (2s delay):
```
curl -X POST http://localhost:8080/chaos \
     -H "Content-Type: application/json" \
     -d '{"mode": "slow", "duration": 2}'
```

### Recover System:
```
curl -X POST http://localhost:8080/chaos \
     -H "Content-Type: application/json" \
     -d '{"mode": "recover"}'
```
## Security & Best Practices
- Non-Root Execution: All containers run under a non-root user (UID 1001).

- Minimized Attack Surface: Using python:3.11-slim for a tiny footprint.

- Capability Dropping: Linux capabilities are dropped in the Compose file to limit container power.

- Reverse Proxy: The API service is never exposed directly; all traffic is routed through Nginx.
