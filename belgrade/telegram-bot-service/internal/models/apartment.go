package models

type Apartment struct {
	Title       string   `json:"title"`
	Description string   `json:"description"`
	Link        string   `json:"link"`
	Placement   string   `json:"placement"`
	Price       string   `json:"price"`
	Owner       string   `json:"owner"`
	PublishDate string   `json:"date_published"`
	Features    []string `json:"features"`
}
