package config

type AppConfig struct {
	RabbitMqHost  string
	RabbitMqQueue string
	TgBotGroupId  int64
	TgBotToken    string
}

func NewAppConfig() *AppConfig {
	return &AppConfig{
		RabbitMqHost:  "amqp://guest:guest@rabbitmq_service:5672/",
		RabbitMqQueue: "new_apartments",
		TgBotGroupId:  0,
		TgBotToken:    "",
	}
}
