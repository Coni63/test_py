#!/usr/bin/env python3
"""
Network Connectivity Checker
Tests network access and authentication for various systems defined in YAML config.
"""

import yaml
import logging
import sys
from typing import Dict, List, Union, Optional
from pydantic import BaseModel, Field
import socket
import ssl
import time
from urllib.parse import urlparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Database connectors (install with: pip install cx_Oracle psycopg2-binary)
try:
    import cx_Oracle
    ORACLE_AVAILABLE = True
except ImportError:
    ORACLE_AVAILABLE = False

try:
    import psycopg2
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

# Kafka client (install with: pip install kafka-python)
try:
    from kafka import KafkaProducer, KafkaConsumer
    from kafka.errors import KafkaError
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


# Pydantic Models
class OracleConfig(BaseModel):
    name: str
    host: str
    port: int = 1521
    service_name: Optional[str] = None
    sid: Optional[str] = None
    username: str
    password: str
    timeout: int = 10

class PostgresConfig(BaseModel):
    name: str
    host: str
    port: int = 5432
    database: str
    username: str
    password: str
    timeout: int = 10

class WebServiceConfig(BaseModel):
    name: str
    url: str
    method: str = "GET"
    headers: Optional[Dict[str, str]] = None
    auth_username: Optional[str] = None
    auth_password: Optional[str] = None
    verify_ssl: bool = True
    timeout: int = 10
    expected_status: List[int] = Field(default_factory=lambda: [200])


class SystemsConfig(BaseModel):
    oracle: Optional[List[OracleConfig]] = None
    postgres: Optional[List[PostgresConfig]] = None
    webservices: Optional[List[WebServiceConfig]] = None
    kafka: Optional[List[KafkaConfig]] = None


# Checker Functions
def check_port_connectivity(host: str, port: int, timeout: int = 10) -> tuple[bool, str]:
    """Check if a port is reachable on a host."""
    try:
        sock = socket.create_connection((host, port), timeout)
        sock.close()
        return True, f"Port {port} is reachable"
    except socket.timeout:
        return False, f"Connection to {host}:{port} timed out"
    except socket.error as e:
        return False, f"Connection to {host}:{port} failed: {e}"

def check_oracle(config: OracleConfig) -> Dict[str, Union[bool, str]]:
    """Check Oracle database connectivity and authentication."""
    result = {
        "name": config.name,
        "network_ok": False,
        "auth_ok": False,
        "network_message": "",
        "auth_message": ""
    }
    
    logger.info(f"🔍 Checking Oracle: {config.name}")
    
    # Check network connectivity
    network_ok, network_msg = check_port_connectivity(config.host, config.port, config.timeout)
    result["network_ok"] = network_ok
    result["network_message"] = network_msg
    
    if not network_ok:
        logger.error(f"❌ {config.name} - Network: {network_msg}")
        return result
    
    logger.info(f"✅ {config.name} - Network: {network_msg}")
    
    # Check authentication
    if not ORACLE_AVAILABLE:
        result["auth_message"] = "cx_Oracle library not available"
        logger.warning(f"⚠️  {config.name} - Auth: cx_Oracle library not available")
        return result
    
    try:
        # Build connection string
        if config.service_name:
            dsn = cx_Oracle.makedsn(config.host, config.port, service_name=config.service_name)
        elif config.sid:
            dsn = cx_Oracle.makedsn(config.host, config.port, sid=config.sid)
        else:
            dsn = f"{config.host}:{config.port}"
        
        connection = cx_Oracle.connect(
            user=config.username,
            password=config.password,
            dsn=dsn,
            timeout=config.timeout
        )
        
        # Test with a simple query
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM DUAL")
        cursor.fetchone()
        cursor.close()
        connection.close()
        
        result["auth_ok"] = True
        result["auth_message"] = "Authentication successful"
        logger.info(f"✅ {config.name} - Auth: Authentication successful")
        
    except cx_Oracle.Error as e:
        result["auth_message"] = f"Oracle error: {e}"
        logger.error(f"❌ {config.name} - Auth: {e}")
    except Exception as e:
        result["auth_message"] = f"Unexpected error: {e}"
        logger.error(f"❌ {config.name} - Auth: {e}")
    
    return result

def check_postgres(config: PostgresConfig) -> Dict[str, Union[bool, str]]:
    """Check PostgreSQL database connectivity and authentication."""
    result = {
        "name": config.name,
        "network_ok": False,
        "auth_ok": False,
        "network_message": "",
        "auth_message": ""
    }
    
    logger.info(f"🔍 Checking PostgreSQL: {config.name}")
    
    # Check network connectivity
    network_ok, network_msg = check_port_connectivity(config.host, config.port, config.timeout)
    result["network_ok"] = network_ok
    result["network_message"] = network_msg
    
    if not network_ok:
        logger.error(f"❌ {config.name} - Network: {network_msg}")
        return result
    
    logger.info(f"✅ {config.name} - Network: {network_msg}")
    
    # Check authentication
    if not POSTGRES_AVAILABLE:
        result["auth_message"] = "psycopg2 library not available"
        logger.warning(f"⚠️  {config.name} - Auth: psycopg2 library not available")
        return result
    
    try:
        connection = psycopg2.connect(
            host=config.host,
            port=config.port,
            database=config.database,
            user=config.username,
            password=config.password,
            connect_timeout=config.timeout
        )
        
        # Test with a simple query
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        connection.close()
        
        result["auth_ok"] = True
        result["auth_message"] = "Authentication successful"
        logger.info(f"✅ {config.name} - Auth: Authentication successful")
        
    except psycopg2.OperationalError as e:
        result["auth_message"] = f"PostgreSQL error: {e}"
        logger.error(f"❌ {config.name} - Auth: {e}")
    except Exception as e:
        result["auth_message"] = f"Unexpected error: {e}"
        logger.error(f"❌ {config.name} - Auth: {e}")
    
    return result

def check_webservice(config: WebServiceConfig) -> Dict[str, Union[bool, str]]:
    """Check web service connectivity and authentication."""
    result = {
        "name": config.name,
        "network_ok": False,
        "auth_ok": False,
        "network_message": "",
        "auth_message": ""
    }
    
    logger.info(f"🔍 Checking Web Service: {config.name}")
    
    try:
        # Parse URL to check network connectivity first
        parsed_url = urlparse(config.url)
        host = parsed_url.hostname
        port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
        
        # Check network connectivity
        network_ok, network_msg = check_port_connectivity(host, port, config.timeout)
        result["network_ok"] = network_ok
        result["network_message"] = network_msg
        
        if not network_ok:
            logger.error(f"❌ {config.name} - Network: {network_msg}")
            return result
        
        logger.info(f"✅ {config.name} - Network: {network_msg}")
        
        # Prepare request
        session = requests.Session()
        
        # Setup retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        headers = config.headers or {}
        auth = None
        
        if config.auth_username and config.auth_password:
            auth = (config.auth_username, config.auth_password)
        
        # Make request
        response = session.request(
            method=config.method,
            url=config.url,
            headers=headers,
            auth=auth,
            verify=config.verify_ssl,
            timeout=config.timeout
        )
        
        # Check response
        if response.status_code in config.expected_status:
            result["auth_ok"] = True
            result["auth_message"] = f"Request successful (HTTP {response.status_code})"
            logger.info(f"✅ {config.name} - Auth: Request successful (HTTP {response.status_code})")
        else:
            result["auth_message"] = f"Unexpected status code: {response.status_code}"
            logger.error(f"❌ {config.name} - Auth: HTTP {response.status_code}")
        
    except requests.exceptions.Timeout:
        result["auth_message"] = "Request timed out"
        logger.error(f"❌ {config.name} - Auth: Request timed out")
    except requests.exceptions.ConnectionError as e:
        result["auth_message"] = f"Connection error: {e}"
        logger.error(f"❌ {config.name} - Auth: Connection error")
    except requests.exceptions.RequestException as e:
        result["auth_message"] = f"Request error: {e}"
        logger.error(f"❌ {config.name} - Auth: Request error: {e}")
    except Exception as e:
        result["auth_message"] = f"Unexpected error: {e}"
        logger.error(f"❌ {config.name} - Auth: Unexpected error: {e}")
    
    return result

def check_kafka(config: KafkaConfig) -> Dict[str, Union[bool, str]]:
    """Check Kafka connectivity and authentication."""
    result = {
        "name": config.name,
        "network_ok": False,
        "auth_ok": False,
        "network_message": "",
        "auth_message": ""
    }
    
    logger.info(f"🔍 Checking Kafka: {config.name}")
    
    if not KAFKA_AVAILABLE:
        result["network_message"] = "kafka-python library not available"
        result["auth_message"] = "kafka-python library not available"
        logger.warning(f"⚠️  {config.name} - kafka-python library not available")
        return result
    
    # Check network connectivity to all bootstrap servers
    network_results = []
    for server in config.bootstrap_servers:
        host, port = server.split(':')
        port = int(port)
        network_ok, network_msg = check_port_connectivity(host, port, config.timeout)
        network_results.append((network_ok, f"{server}: {network_msg}"))
    
    # At least one server should be reachable
    any_reachable = any(ok for ok, _ in network_results)
    result["network_ok"] = any_reachable
    result["network_message"] = "; ".join(msg for _, msg in network_results)
    
    if not any_reachable:
        logger.error(f"❌ {config.name} - Network: No bootstrap servers reachable")
        return result
    
    logger.info(f"✅ {config.name} - Network: At least one bootstrap server reachable")
    
    try:
        # Build Kafka configuration
        kafka_config = {
            'bootstrap_servers': config.bootstrap_servers,
            'request_timeout_ms': config.timeout * 1000,
            'api_version': (0, 10, 1),
        }
        
        if config.security_protocol != "PLAINTEXT":
            kafka_config['security_protocol'] = config.security_protocol
            
            if config.sasl_mechanism:
                kafka_config['sasl_mechanism'] = config.sasl_mechanism
            if config.sasl_username:
                kafka_config['sasl_plain_username'] = config.sasl_username
            if config.sasl_password:
                kafka_config['sasl_plain_password'] = config.sasl_password
            
            if config.ssl_cafile:
                kafka_config['ssl_cafile'] = config.ssl_cafile
            if config.ssl_certfile:
                kafka_config['ssl_certfile'] = config.ssl_certfile
            if config.ssl_keyfile:
                kafka_config['ssl_keyfile'] = config.ssl_keyfile
            if config.ssl_password:
                kafka_config['ssl_password'] = config.ssl_password
        
        # Test connection with a consumer (less intrusive than producer)
        consumer = KafkaConsumer(
            config.topic,
            **kafka_config,
            consumer_timeout_ms=config.timeout * 1000,
            auto_offset_reset='earliest',
            enable_auto_commit=False
        )
        
        # Check if we can get metadata (this validates authentication)
        metadata = consumer.list_consumer_groups()
        consumer.close()
        
        result["auth_ok"] = True
        result["auth_message"] = "Kafka connection and authentication successful"
        logger.info(f"✅ {config.name} - Auth: Connection successful")
        
    except KafkaError as e:
        result["auth_message"] = f"Kafka error: {e}"
        logger.error(f"❌ {config.name} - Auth: Kafka error: {e}")
    except Exception as e:
        result["auth_message"] = f"Unexpected error: {e}"
        logger.error(f"❌ {config.name} - Auth: Unexpected error: {e}")
    
    return result


def load_config(config_file: str) -> SystemsConfig:
    """Load and parse YAML configuration file."""
    try:
        with open(config_file, 'r') as f:
            config_data = yaml.safe_load(f)
        return SystemsConfig(**config_data)
    except FileNotFoundError:
        logger.error(f"Configuration file {config_file} not found")
        sys.exit(1)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        sys.exit(1)


def main():
    """Main function to run all connectivity checks."""
    if len(sys.argv) != 2:
        logger.error("Usage: python network_checker.py <config.yaml>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    config = load_config(config_file)
    
    results = []
    
    logger.info("🚀 Starting network connectivity checks...")
    logger.info(f"📋 Configuration loaded from: {config_file}")
    
    # Check Oracle databases
    if config.oracle:
        logger.info(f"\n📊 Checking {len(config.oracle)} Oracle database(s)...")
        for oracle_config in config.oracle:
            result = check_oracle(oracle_config)
            results.append(result)
    
    # Check PostgreSQL databases
    if config.postgres:
        logger.info(f"\n🐘 Checking {len(config.postgres)} PostgreSQL database(s)...")
        for postgres_config in config.postgres:
            result = check_postgres(postgres_config)
            results.append(result)
    
    # Check web services
    if config.webservices:
        logger.info(f"\n🌐 Checking {len(config.webservices)} web service(s)...")
        for ws_config in config.webservices:
            result = check_webservice(ws_config)
            results.append(result)
    
    # Check Kafka
    if config.kafka:
        logger.info(f "\n📡 Checking {len(config.kafka)} Kafka topic(s)...")
        for kafka_config in config.kafka:
            result = check_kafka(kafka_config)
            results.append(result)
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("📋 CONNECTIVITY CHECK SUMMARY")
    logger.info("="*50)
    
    total_checks = len(results)
    network_ok = sum(1 for r in results if r["network_ok"])
    auth_ok = sum(1 for r in results if r["auth_ok"])
    
    for result in results:
        network_status = "✅" if result["network_ok"] else "❌"
        auth_status = "✅" if result["auth_ok"] else "❌"
        logger.info(f"{result['name']}: Network {network_status} | Auth {auth_status}")
    
    logger.info(f"\nTotal checks: {total_checks}")
    logger.info(f"Network connectivity: {network_ok}/{total_checks}")
    logger.info(f"Authentication: {auth_ok}/{total_checks}")
    
    if network_ok == total_checks and auth_ok == total_checks:
        logger.info("🎉 All checks passed!")
        sys.exit(0)
    else:
        logger.error("💥 Some checks failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()