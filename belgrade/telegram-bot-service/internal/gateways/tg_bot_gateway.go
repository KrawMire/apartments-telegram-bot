package gateways

import (
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"log"
	"telegram-bot-service/internal/adapters"
	"telegram-bot-service/pkg/tgformat"
)

type TgBotGateway struct {
	apartsAdapter *adapters.ApartmentsAdapter
	groupId       int64
	bot           *tgbotapi.BotAPI
}

func NewTgBotGateway(apartmentsAdapter *adapters.ApartmentsAdapter, groupId int64, botToken string) *TgBotGateway {
	bot, err := tgbotapi.NewBotAPI(botToken)
	if err != nil {
		log.Panic(err)
	}

	bot.Debug = false
	log.Printf("Authorized on account %s", bot.Self.UserName)

	return &TgBotGateway{
		apartsAdapter: apartmentsAdapter,
		groupId:       groupId,
		bot:           bot,
	}
}

func (g *TgBotGateway) SendApartments() {
	apartments, err := g.apartsAdapter.GetApartments()
	if err != nil {
		log.Printf("Error getting apartments: %v", err)
		return
	}

	for _, ap := range apartments {
		msgText := tgformat.BuildMessageFromApartment(ap)
		msg := tgbotapi.NewMessage(g.groupId, msgText)
		msg.ParseMode = "MarkdownV2"

		_, err = g.bot.Send(msg)
		if err != nil {
			log.Printf("Error sending message: %v", err)
		}
	}
}
