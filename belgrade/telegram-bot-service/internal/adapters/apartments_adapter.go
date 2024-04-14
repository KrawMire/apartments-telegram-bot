package adapters

import (
	"encoding/json"
	"net/http"
	"telegram-bot-service/internal/models"
	"time"
)

type ApartmentsAdapter struct {
	host string
}

func NewApartmentsAdapter(host string) *ApartmentsAdapter {
	return &ApartmentsAdapter{
		host: host,
	}
}

func (a *ApartmentsAdapter) GetApartments() ([]models.Apartment, error) {
	client := &http.Client{
		Timeout: time.Second * 90,
	}
	resp, err := client.Get(a.host + "/apartments-get")
	if err != nil {
		return nil, err
	}

	defer resp.Body.Close()
	var apartments []models.Apartment

	err = json.NewDecoder(resp.Body).Decode(&apartments)
	if err != nil {
		return nil, err
	}

	return apartments, nil
}
