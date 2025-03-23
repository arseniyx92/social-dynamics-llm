package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

const (
	baseURL = "https://api.deepseek.com/v1"
)

type Agent struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type Request struct {
	SenderID   string `json:"sender_id"`
	ReceiverID string `json:"receiver_id"`
	Message    string `json:"message"`
}

type Opinion struct {
	AgentID string `json:"agent_id"`
	Opinion string `json:"opinion"`
}

type Response struct {
	AgentID  string `json:"agent_id"`
	Response string `json:"response"`
}

// CreateAgent создает нового агента
func CreateAgent(name string) (*Agent, error) {
	url := fmt.Sprintf("%s/agents", baseURL)
	agent := Agent{Name: name}

	jsonData, err := json.Marshal(agent)
	if err != nil {
		return nil, err
	}

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var newAgent Agent
	err = json.Unmarshal(body, &newAgent)
	if err != nil {
		return nil, err
	}

	return &newAgent, nil
}

// SendRequest отправляет запрос от одного агента другому
func SendRequest(senderID, receiverID, message string) error {
	url := fmt.Sprintf("%s/agents/%s/send", baseURL, senderID)
	request := Request{
		SenderID:   senderID,
		ReceiverID: receiverID,
		Message:    message,
	}

	jsonData, err := json.Marshal(request)
	if err != nil {
		return err
	}

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("failed to send request: %s", resp.Status)
	}

	return nil
}

// GetOpinion получает мнение агента
func GetOpinion(agentID string) (*Opinion, error) {
	url := fmt.Sprintf("%s/agents/%s/opinion", baseURL, agentID)

	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var opinion Opinion
	err = json.Unmarshal(body, &opinion)
	if err != nil {
		return nil, err
	}

	return &opinion, nil
}

// GetResponse получает ответ агента
func GetResponse(agentID string) (*Response, error) {
	url := fmt.Sprintf("%s/agents/%s/response", baseURL, agentID)

	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var response Response
	err = json.Unmarshal(body, &response)
	if err != nil {
		return nil, err
	}

	return &response, nil
}

func main() {
	// Пример использования функций

	// Создание нового агента
	agent, err := CreateAgent("Agent1")
	if err != nil {
		fmt.Println("Error creating agent:", err)
		return
	}
	fmt.Printf("Created agent: %+v\n", agent)

	// Отправка запроса другому агенту
	err = SendRequest(agent.ID, "receiver_agent_id", "Hello, how are you?")
	if err != nil {
		fmt.Println("Error sending request:", err)
		return
	}
	fmt.Println("Request sent successfully")

	// Получение мнения агента
	opinion, err := GetOpinion(agent.ID)
	if err != nil {
		fmt.Println("Error getting opinion:", err)
		return
	}
	fmt.Printf("Agent opinion: %+v\n", opinion)

	// Получение ответа агента
	response, err := GetResponse(agent.ID)
	if err != nil {
		fmt.Println("Error getting response:", err)
		return
	}
	fmt.Printf("Agent response: %+v\n", response)
}
