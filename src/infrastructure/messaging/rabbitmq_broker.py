import json
import logging
import pika
from src.application.ports.message_broker import IMessageBroker
from src.domain.events.domain_events import DomainEvent
from src.infrastructure.config.settings import settings

logger = logging.getLogger(__name__)


class RabbitMQBroker(IMessageBroker):
    def __init__(self):
        self._connection = None
        self._channel = None
        self._connect()

    def _connect(self):
        try:
            params = pika.URLParameters(settings.RABBITMQ_URL)
            self._connection = pika.BlockingConnection(params)
            self._channel = self._connection.channel()
            # Declara as filas que vamos usar
            for queue in ["exam.performed", "report.issued", "result.available"]:
                self._channel.queue_declare(queue=queue, durable=True)
            logger.info("RabbitMQ conectado")
        except Exception as e:
            logger.error(f"Falha ao conectar RabbitMQ: {e}")

    def publish(self, queue: str, event: DomainEvent) -> None:
        try:
            if not self._channel or self._channel.is_closed:
                self._connect()

            body = json.dumps(event.to_dict())
            self._channel.basic_publish(
                exchange="",
                routing_key=queue,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # mensagem persistente
                    content_type="application/json",
                ),
            )
            logger.info(f"Evento publicado → [{queue}]: {body}")
        except Exception as e:
            logger.error(f"Erro ao publicar evento: {e}")

    def close(self):
        if self._connection and not self._connection.is_closed:
            self._connection.close()


class FakeBroker(IMessageBroker):
    """Broker em memória para testes e desenvolvimento sem RabbitMQ."""

    def publish(self, queue: str, event: DomainEvent) -> None:
        print(f"[EVENTO] [{queue}] {event.to_dict()}", flush=True)

    def close(self):
        pass
