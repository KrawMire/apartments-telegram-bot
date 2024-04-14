package main

import (
	"telegram-bot-service/config"
	"telegram-bot-service/internal/consumers"
	"telegram-bot-service/internal/gateways"
)

func main() {
	cfg := config.NewAppConfig()

	// dependency injection
	tgGateway := gateways.NewTgBotGateway(cfg.TgBotGroupId, cfg.TgBotToken)
	apartmentsAdapter := consumers.NewApartmentsConsumer(cfg.RabbitMqHost, cfg.RabbitMqQueue, tgGateway)

	apartmentsAdapter.WatchNewApartments()
}
