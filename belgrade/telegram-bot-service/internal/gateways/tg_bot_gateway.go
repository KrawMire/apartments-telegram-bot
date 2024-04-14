package gateways

import (
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"log"
	"telegram-bot-service/internal/models"
	"telegram-bot-service/pkg/tgformat"
)

type TgBotGateway struct {
	groupId int64
	bot     *tgbotapi.BotAPI
}

func NewTgBotGateway(groupId int64, botToken string) *TgBotGateway {
	bot, err := tgbotapi.NewBotAPI(botToken)
	if err != nil {
		log.Panic(err)
	}

	bot.Debug = false
	log.Printf("Authorized on account %s", bot.Self.UserName)

	return &TgBotGateway{
		groupId: groupId,
		bot:     bot,
	}
}

func (g *TgBotGateway) SendApartments(apartments []models.Apartment) {
	for _, ap := range apartments {
		msgText := tgformat.BuildMessageFromApartment(ap)
		msg := tgbotapi.NewMessage(g.groupId, msgText)
		msg.ParseMode = "MarkdownV2"

		_, err := g.bot.Send(msg)
		if err != nil {
			log.Printf("Error sending message: %v", err)
		}
	}
}
