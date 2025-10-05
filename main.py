#!/usr/bin/env python3
"""
Telecom Service Health Monitor & Auto-Recovery System
Simplified demo version for portfolio
"""

import argparse
import json
import socket
import time
from datetime import datetime
from typing import Dict, List, Optional
import requests


class HealthChecker:
    """Health checking engine supporting multiple protocols"""
    
    def check_http(self, service: Dict) -> Dict:
        """Check HTTP/HTTPS endpoint health"""
        try:
            start = time.time()
            response = requests.get(
                service['url'],
                timeout=service.get('timeout', 5)
            )
            duration = (time.time() - start) * 1000  # Convert to ms
            
            return {
                'healthy': response.status_code == 200,
                'status_code': response.status_code,
                'response_time_ms': round(duration, 2)
            }
        except requests.exceptions.RequestException as e:
            return {
                'healthy': False,
                'error': str(e),
                'response_time_ms': None
            }
    
    def check_tcp(self, service: Dict) -> Dict:
        """Check TCP port connectivity"""
        try:
            start = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(service.get('timeout', 5))
            
            result = sock.connect_ex((service['host'], service['port']))
            duration = (time.time() - start) * 1000
            
            sock.close()
            
            return {
                'healthy': result == 0,
                'connection_result': result,
                'response_time_ms': round(duration, 2)
            }
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e),
                'response_time_ms': None
            }
    
    def check_sip(self, service: Dict) -> Dict:
        """
        Check SIP endpoint health
        Simulates SIP OPTIONS request via UDP
        """
        try:
            start = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(service.get('timeout', 5))
            
            # Create SIP OPTIONS request
            sip_message = (
                f"OPTIONS sip:{service['host']}:{service['port']} SIP/2.0\r\n"
                f"Via: SIP/2.0/UDP monitor:5060;branch=z9hG4bK123456\r\n"
                f"From: <sip:monitor@localhost>;tag=123\r\n"
                f"To: <sip:{service['host']}>\r\n"
                f"Call-ID: health-check-{int(time.time())}\r\n"
                f"CSeq: 1 OPTIONS\r\n"
                f"Content-Length: 0\r\n\r\n"
            )
            
            # Send SIP message
            sock.sendto(sip_message.encode(), (service['host'], service['port']))
            
            # Try to receive response
            try:
                data, addr = sock.recvfrom(4096)
                duration = (time.time() - start) * 1000
                
                # Parse SIP response (simple check for 200 OK)
                healthy = b'SIP/2.0 200' in data or b'SIP/2.0 2' in data
                
                return {
                    'healthy': healthy,
                    'response': data.decode('utf-8', errors='ignore')[:100],
                    'response_time_ms': round(duration, 2)
                }
            except socket.timeout:
                # No response, but service might still be up
                # In real systems, this might indicate an issue
                return {
                    'healthy': False,
                    'error': 'SIP timeout - no response received',
                    'response_time_ms': None
                }
            finally:
                sock.close()
                
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e),
                'response_time_ms': None
            }


class RecoveryEngine:
    """Automatic recovery engine"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.recovery_attempts = {}
    
    def recover(self, service: Dict, check_result: Dict) -> bool:
        """
        Execute recovery action for failed service
        
        Returns True if recovery was attempted, False otherwise
        """
        service_name = service['name']
        recovery_config = service.get('recovery', {})
        action = recovery_config.get('action', 'alert')
        
        # Track recovery attempts
        if service_name not in self.recovery_attempts:
            self.recovery_attempts[service_name] = 0
        
        self.recovery_attempts[service_name] += 1
        
        print(f"\n{'='*60}")
        print(f"🔧 RECOVERY: {service_name}")
        print(f"{'='*60}")
        print(f"Action: {action}")
        print(f"Attempt: #{self.recovery_attempts[service_name]}")
        
        if action == 'failover':
            return self._execute_failover(service, recovery_config)
        elif action == 'restart':
            return self._execute_restart(service, recovery_config)
        elif action == 'alert':
            return self._execute_alert(service, recovery_config)
        else:
            print(f"⚠️  Unknown recovery action: {action}")
            return False
    
    def _execute_failover(self, service: Dict, config: Dict) -> bool:
        """Execute failover to backup endpoint"""
        target = config.get('target', 'unknown')
        print(f"Executing failover to: {target}")
        print("  [1/3] Marking primary endpoint as down...")
        time.sleep(0.5)
        print("  [2/3] Updating routing tables...")
        time.sleep(0.5)
        print("  [3/3] Verifying backup endpoint health...")
        time.sleep(0.5)
        print(f"✓ Failover to {target} completed successfully")
        return True
    
    def _execute_restart(self, service: Dict, config: Dict) -> bool:
        """Execute service restart"""
        command = config.get('command', 'systemctl restart service')
        print(f"Executing restart command: {command}")
        print("  [1/3] Stopping service...")
        time.sleep(0.5)
        print("  [2/3] Starting service...")
        time.sleep(0.5)
        print("  [3/3] Verifying service health...")
        time.sleep(0.5)
        print("✓ Service restart completed")
        return True
    
    def _execute_alert(self, service: Dict, config: Dict) -> bool:
        """Send alert notification"""
        message = config.get('message', f'{service["name"]} is down')
        print(f"Sending alert: {message}")
        print("  → Alert would be sent to PagerDuty/Slack")
        print("  → On-call engineer notified")
        return True


class TelecomMonitor:
    """Main monitoring orchestrator"""
    
    def __init__(self, config_path: str, auto_recover: bool = False, verbose: bool = False):
        self.config_path = config_path
        self.auto_recover = auto_recover
        self.verbose = verbose
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Initialize components
        self.health_checker = HealthChecker()
        self.recovery_engine = RecoveryEngine(verbose) if auto_recover else None
        
        # Statistics
        self.stats = {
            'total_checks': 0,
            'healthy_checks': 0,
            'unhealthy_checks': 0,
            'recoveries_attempted': 0,
            'recoveries_successful': 0
        }
    
    def log_incident(self, service_name: str, status: str, details: str):
        """Log incident to file"""
        timestamp = datetime.now().isoformat()
        incident = f"[{timestamp}] {service_name}: {status} - {details}\n"
        
        with open('incidents.log', 'a') as f:
            f.write(incident)
    
    def check_service(self, service: Dict) -> Dict:
        """Check a single service"""
        service_type = service['type']
        
        if service_type == 'http':
            result = self.health_checker.check_http(service)
        elif service_type == 'tcp':
            result = self.health_checker.check_tcp(service)
        elif service_type == 'sip':
            result = self.health_checker.check_sip(service)
        else:
            result = {'healthy': False, 'error': f'Unknown type: {service_type}'}
        
        result['service_name'] = service['name']
        result['service_type'] = service_type
        result['timestamp'] = datetime.now().isoformat()
        
        return result
    
    def display_result(self, service: Dict, result: Dict):
        """Display check result"""
        name = service['name']
        healthy = result.get('healthy', False)
        response_time = result.get('response_time_ms')
        
        status_symbol = "✓" if healthy else "✗"
        status_text = "HEALTHY" if healthy else "UNHEALTHY"
        status_color = "\033[92m" if healthy else "\033[91m"  # Green or Red
        reset_color = "\033[0m"
        
        output = f"{status_symbol} {status_color}{name}: {status_text}{reset_color}"
        
        if response_time:
            output += f" (response: {response_time}ms)"
        
        if not healthy and 'error' in result:
            output += f" - {result['error']}"
        
        print(output)
        
        # Log incident if unhealthy
        if not healthy:
            error_detail = result.get('error', 'Service check failed')
            self.log_incident(name, 'UNHEALTHY', error_detail)
    
    def run_check_cycle(self):
        """Run one complete check cycle"""
        print(f"\n{'='*60}")
        print(f"Health Check Cycle - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        results = []
        
        for service in self.config['services']:
            result = self.check_service(service)
            self.display_result(service, result)
            results.append((service, result))
            
            # Update stats
            self.stats['total_checks'] += 1
            if result.get('healthy'):
                self.stats['healthy_checks'] += 1
            else:
                self.stats['unhealthy_checks'] += 1
                
                # Attempt recovery if enabled
                if self.auto_recover and self.recovery_engine:
                    self.stats['recoveries_attempted'] += 1
                    if self.recovery_engine.recover(service, result):
                        self.stats['recoveries_successful'] += 1
        
        # Display summary
        healthy_count = sum(1 for _, r in results if r.get('healthy'))
        total_count = len(results)
        
        print(f"\n{'='*60}")
        print(f"Summary: {healthy_count}/{total_count} services healthy")
        if self.auto_recover:
            print(f"Recoveries attempted: {self.stats['recoveries_attempted']}")
        print(f"{'='*60}\n")
    
    def run(self):
        """Run the monitoring loop"""
        print("\n" + "="*60)
        print("🔧 Telecom Service Health Monitor & Auto-Recovery")
        print("="*60)
        print(f"Configuration: {self.config_path}")
        print(f"Services loaded: {len(self.config['services'])}")
        print(f"Auto-recovery: {'ENABLED' if self.auto_recover else 'DISABLED'}")
        print(f"Check interval: {self.config.get('check_interval', 30)} seconds")
        print("="*60 + "\n")
        
        try:
            while True:
                self.run_check_cycle()
                
                # Wait for next cycle
                interval = self.config.get('check_interval', 30)
                print(f"Waiting {interval} seconds until next check...\n")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\nShutting down gracefully...")
            print("\nFinal Statistics:")
            print(f"  Total checks: {self.stats['total_checks']}")
            print(f"  Healthy: {self.stats['healthy_checks']}")
            print(f"  Unhealthy: {self.stats['unhealthy_checks']}")
            if self.auto_recover:
                print(f"  Recovery attempts: {self.stats['recoveries_attempted']}")
                print(f"  Successful recoveries: {self.stats['recoveries_successful']}")
            print("\nIncidents logged to: incidents.log")
            print("\nGoodbye!")


def main():
    parser = argparse.ArgumentParser(
        description='Telecom Service Health Monitor & Auto-Recovery System'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config.json',
        help='Path to configuration file (default: config.json)'
    )
    parser.add_argument(
        '--auto-recover',
        action='store_true',
        help='Enable automatic recovery actions'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    monitor = TelecomMonitor(
        config_path=args.config,
        auto_recover=args.auto_recover,
        verbose=args.verbose
    )
    
    monitor.run()


if __name__ == '__main__':
    main()
