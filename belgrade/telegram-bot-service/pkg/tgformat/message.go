package tgformat

import (
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"strings"
	"telegram-bot-service/internal/models"
)

func BuildMessageFromApartment(apartment models.Apartment) string {
	strBuilder := strings.Builder{}

	strBuilder.WriteString("[" + tgbotapi.EscapeText("MarkdownV2", apartment.Title) + "](" + tgbotapi.EscapeText("MarkdownV2", apartment.Link) + ")\n")
	strBuilder.WriteString("_" + tgbotapi.EscapeText("MarkdownV2", apartment.Placement) + "_" + "\n\n")
	strBuilder.WriteString("_" + tgbotapi.EscapeText("MarkdownV2", apartment.Description) + "_" + "\n\n")
	strBuilder.WriteString("*" + tgbotapi.EscapeText("MarkdownV2", apartment.Price) + "*" + "\n")
	strBuilder.WriteString("*" + tgbotapi.EscapeText("MarkdownV2", apartment.Owner) + "*" + "\n\n")

	for _, feature := range apartment.Features {
		strBuilder.WriteString("\\- " + tgbotapi.EscapeText("MarkdownV2", feature) + "\n")
	}

	return strBuilder.String()
}
