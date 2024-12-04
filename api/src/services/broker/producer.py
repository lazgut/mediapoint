from aiokafka import AIOKafkaProducer
from core.config import settings
from loguru import logger


class KafkaProducerService:
    def __init__(self):
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_broker)
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send_message(self, topic: str, key: bytes, value: bytes):
        try:
            await self.producer.send_and_wait(topic, key=key, value=value)
        except Exception as e:
            logger.error(f"Ошибка при публикации в Kafka: {str(e)}")
            raise


kafka_producer_instance = KafkaProducerService()


async def get_kafka_producer_service() -> KafkaProducerService:
    return kafka_producer_instance
