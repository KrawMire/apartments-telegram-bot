package consumers

import (
	"encoding/json"
	amqp "github.com/rabbitmq/amqp091-go"
	"log"
	"telegram-bot-service/internal/gateways"
	"telegram-bot-service/internal/models"
	"time"
)

type ApartmentsConsumer struct {
	tgbGateway *gateways.TgBotGateway
	rMqHost    string
	queueName  string
}

func NewApartmentsConsumer(rabbitMqHost string, queueName string, tgGateway *gateways.TgBotGateway) *ApartmentsConsumer {
	return &ApartmentsConsumer{
		tgbGateway: tgGateway,
		rMqHost:    rabbitMqHost,
		queueName:  queueName,
	}
}

func (a *ApartmentsConsumer) WatchNewApartments() {
	conn := a.connect()
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		log.Fatal("Failed to open a channel")
	}
	defer ch.Close()

	q, err := ch.QueueDeclare(
		a.queueName,
		false,
		false,
		false,
		false,
		nil)
	if err != nil {
		log.Fatal("Failed to declare a queue")
	}

	msgs, err := ch.Consume(
		q.Name,
		"",
		true,
		false,
		false,
		false,
		nil)
	if err != nil {
		log.Fatal("Failed to register a consumer")
	}

	go a.handleNewApartments(msgs)
	log.Println("Listening for new apartments...")

	var forever chan struct{}
	<-forever
}

func (a *ApartmentsConsumer) connect() *amqp.Connection {
	for {
		conn, err := amqp.Dial(a.rMqHost)
		if err == nil {
			return conn
		}

		log.Println(err)
		log.Printf("Trying to reconnect to RabbitMQ at %s\n", a.rMqHost)
		time.Sleep(5 * time.Second)
	}
}

func (a *ApartmentsConsumer) handleNewApartments(msgs <-chan amqp.Delivery) {
	for d := range msgs {
		var apartments []models.Apartment

		err := json.Unmarshal(d.Body, &apartments)
		if err != nil {
			log.Printf("Cannot unmarshall JSON: %s\n", err)
			continue
		}

		log.Printf("Found %d new apartments. Sending... \n", len(apartments))

		a.tgbGateway.SendApartments(apartments)
		log.Println("Successfully processed apartments")
	}
}
