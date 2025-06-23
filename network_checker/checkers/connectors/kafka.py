import logging
from typing import Optional
from pydantic import BaseModel
from checkers.exceptions import AccessError
from .abstract_connector import BaseConnector

from kafka import KafkaConsumer

logger = logging.getLogger("kafka-logger")

class KafkaConfig(BaseModel):
    name: str
    bootstrap_server: str
    topic: str
    security_protocol: str = "PLAINTEXT"
    sasl_mechanism: Optional[str] = None
    sasl_username: Optional[str] = None
    sasl_password: Optional[str] = None
    ssl_cafile: Optional[str] = None
    ssl_certfile: Optional[str] = None
    ssl_keyfile: Optional[str] = None
    ssl_password: Optional[str] = None
    timeout: int = 10



class KafkaConnector(BaseConnector):
    def check_network(self, config: KafkaConfig):
        """Check Kafka connectivity and authentication."""
        host, port = config.bootstrap_server.split(':')
        port = int(port)
        self.check_port_connectivity(host, port, config.timeout)

    def check_connection(self, config: KafkaConfig):
        try:
            # Build Kafka configuration
            kafka_config = {
                'bootstrap_servers': [config.bootstrap_server],
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
            _ = consumer.list_consumer_groups()
            consumer.close()
            
        except Exception as e:
            raise AccessError(f"❌ Kafka error: {e}")
