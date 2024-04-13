package main

import (
	"telegram-bot-service/config"
	"telegram-bot-service/internal/adapters"
	"telegram-bot-service/internal/gateways"
	"time"
)

func main() {
	cfg := config.NewAppConfig()

	// dependency injection
	apartmentsAdapter := adapters.NewApartmentsAdapter(cfg.ApartmentsAdapterHost)
	tgGateway := gateways.NewTgBotGateway(
		apartmentsAdapter,
		cfg.TgBotGroupId,
		cfg.TgBotToken)

	go tgGateway.SendApartments()

	for range time.Tick(time.Minute * 30) {
		go tgGateway.SendApartments()
	}
}
