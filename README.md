# 🔧 Telecom Service Health Monitor & Auto-Recovery System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A lightweight automated health monitoring and self-healing system for telecom infrastructure. Monitors SIP endpoints, HTTP services, and TCP connections with automatic recovery capabilities.

## 🎯 Project Overview

This system demonstrates core infrastructure and systems engineering capabilities required for operating telecom services at scale - similar to systems used by VoIP providers like Amazon Connect.

**Key Capabilities:**
- Multi-protocol health checking (SIP, HTTP, TCP)
- Automatic service recovery (restart, failover)
- Real-time metrics and logging
- Incident tracking and history
- Chaos engineering for testing

## ✨ Features

### Health Monitoring
- **SIP Endpoint Checks**: Monitor SIP trunk availability
- **HTTP Health Checks**: Monitor REST APIs and web services  
- **TCP Port Checks**: Verify network connectivity
- **Configurable Intervals**: Set check frequency per service

### Auto-Recovery
- **Service Restart**: Automatically restart failed services
- **Failover**: Switch to backup endpoints
- **Exponential Backoff**: Smart retry with backoff
- **Circuit Breaker**: Prevent cascading failures

### Observability
- **Real-time Metrics**: Service status and health stats
- **Incident Logging**: Track all failures and recoveries
- **JSON Logs**: Structured logging for analysis

## 🏗️ Architecture

┌──────────────────────────────────────┐
│      Health Monitor                  │
│  ┌──────┐  ┌──────┐  ┌──────┐        │
│  │ SIP  │  │ HTTP │  │ TCP  │        │
│  └──┬───┘  └──┬───┘  └──┬───┘        │
│     └─────────┴─────────┘            │
│              │                       │
│      ┌───────▼────────┐              │
│      │ Health Engine  │              │
│      └───────┬────────┘              │ 
│              │                       │
│      ┌───────▼────────┐              │
│      │Recovery Engine │              │ 
│      └────────────────┘              │
└──────────────────────────────────────┘

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **HTTP Requests**: requests library
- **Async I/O**: asyncio
- **Configuration**: JSON
- **Logging**: Python logging with JSON output

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/sanikpatige/telecom-auto-recovery.git
cd telecom-auto-recovery
pip install -r requirements.txt
# config.json is included - edit with your endpoints
python monitor.py
python monitor.py --auto-recover
python monitor.py --auto-recover --verbose
python monitor.py --config my-services.json

🔧 Configuration

{
  "check_interval": 30,
  "services": [
    {
      "name": "sip-trunk-us-east",
      "type": "sip",
      "host": "sip.carrier1.com",
      "port": 5060,
      "timeout": 5,
      "recovery": {
        "action": "failover",
        "target": "sip-trunk-us-west"
      }
    },
    {
      "name": "api-gateway",
      "type": "http",
      "url": "https://api.example.com/health",
      "timeout": 3,
      "recovery": {
        "action": "alert",
        "message": "API Gateway is down"
      }
    },
    {
      "name": "database-primary",
      "type": "tcp",
      "host": "db.example.com",
      "port": 5432,
      "timeout": 2,
      "recovery": {
        "action": "failover",
        "target": "database-replica"
      }
    }
  ]
}

📊 Output Example

[2025-01-05 10:30:00] INFO: Starting Telecom Health Monitor
[2025-01-05 10:30:00] INFO: Loaded 3 services from config
[2025-01-05 10:30:00] INFO: Auto-recovery: ENABLED

[2025-01-05 10:30:05] ✓ sip-trunk-us-east: HEALTHY (response: 2.3ms)
[2025-01-05 10:30:05] ✓ api-gateway: HEALTHY (status: 200, response: 45ms)
[2025-01-05 10:30:05] ✗ database-primary: UNHEALTHY (connection timeout)

[2025-01-05 10:30:05] RECOVERY: Executing failover for database-primary
[2025-01-05 10:30:06] SUCCESS: Failover to database-replica completed

[2025-01-05 10:30:35] Health Check Summary:
  - Total Services: 3
  - Healthy: 3
  - Unhealthy: 0
  - Recoveries: 1

📁 Project Structure

telecom-auto-recovery/
├── monitor.py           # Main application
├── config.json          # Service configuration
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── LICENSE             # MIT License
└── incidents.log       # Incident history (auto-generated)

🎓 Skills Demonstrated
Systems Engineering
✅ Service Monitoring: Multi-protocol health checking
✅ Auto-Recovery: Self-healing system design
✅ Fault Tolerance: Failover and retry logic
✅ Observability: Structured logging and metrics
Telecom-Specific
✅ SIP Protocol: VoIP infrastructure monitoring
✅ Carrier Integration: Multi-carrier failover
✅ High Availability: Automatic failover mechanisms
Software Engineering
✅ Python: Clean, modular code
✅ Async Programming: Efficient I/O handling
✅ Configuration Management: JSON-based config
✅ Error Handling: Comprehensive exception management
✅ Logging: Production-grade logging

🔍 Technical Highlights

SIP Health Check
def check_sip(host, port, timeout):
    """
    Send SIP OPTIONS request to check endpoint health
    Simulates actual SIP handshake
    """
    # Create SIP OPTIONS message
    # Send via UDP socket
    # Parse SIP response
    # Return health status

Recovery Engine
def recover(service, action):
    """
    Execute recovery action based on failure type
    Supports: restart, failover, alert
    """
    if action == "failover":
        # Switch to backup endpoint
        # Update routing tables
        # Verify new endpoint health
    elif action == "restart":
        # Execute restart command
        # Wait for service startup
        # Verify service health

🧪 Testing Locally
The system includes simulated endpoints you can test immediately:

1. Run the monitor
python monitor.py --auto-recover --verbose
2. Watch it detect simulated failures
3. See automatic recovery in action
4. Check incidents.log for history

🚀 Real-World Applications
This system can monitor:

SIP trunks across multiple carriers
VoIP gateway endpoints
API gateways and microservices
Database connections
Load balancer health
Any TCP/HTTP service

🤝 Related to Amazon Connect SDE Role
Job RequirementProject FeatureVoice routing, SIP trunkingSIP endpoint health checksCarrier integrationsMulti-carrier failover logicReal-time systemsContinuous health monitoringTooling for engineersCLI tool with config managementDeploy and operate servicesAuto-recovery mechanismsIdentify and resolve issuesAutomatic incident detection
📈 Metrics Tracked

Service availability (up/down status)
Response times per service
Failure count and recovery attempts
Success rate of recoveries
Total incidents logged

🔮 Future Enhancements

 Prometheus metrics export
 Web dashboard for visualization
 Slack/PagerDuty integration
 Machine learning for predictive failures
 Kubernetes deployment
 Multi-region support with Terraform

📝 License
MIT License - see LICENSE file
👤 Author
Sanik Patige
GitHub: @sanikpatige







