from aiokafka import AIOKafkaProducer
from core.config import settings
from loguru import logger


class KafkaProducerService:
    def __init__(self):
        self.producer = None

    async def start(self):
        logger.info("Initializing Kafka producer...")
        try:
            self.producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_broker)
            await self.producer.start()
            logger.info("Kafka producer started successfully.")
        except Exception as e:
            logger.error(f"Failed to start Kafka producer: {str(e)}")
            raise

    async def stop(self):
        if self.producer:
            logger.info("Stopping Kafka producer...")
            try:
                await self.producer.stop()
                logger.info("Kafka producer stopped successfully.")
            except Exception as e:
                logger.error(f"Failed to stop Kafka producer: {str(e)}")
                raise

    async def send_message(self, topic: str, key: bytes, value: bytes):
        logger.info(f"Sending message to Kafka topic '{topic}' with key '{key.decode()}'...")
        try:
            await self.producer.send_and_wait(topic, key=key, value=value)
            logger.info("Message sent to Kafka successfully.")
        except Exception as e:
            logger.error(f"Error sending message to Kafka: {str(e)}")
            raise


kafka_producer_instance = KafkaProducerService()


async def get_kafka_producer_service() -> KafkaProducerService:
    return kafka_producer_instance
