package config

type AppConfig struct {
	ApartmentsAdapterHost string
	TgBotGroupId          int64
	TgBotToken            string
}

func NewAppConfig() *AppConfig {
	return &AppConfig{
		ApartmentsAdapterHost: "http://localhost:5000",
		TgBotGroupId:          0,
		TgBotToken:            "",
	}
}
