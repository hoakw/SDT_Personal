package main

import (
	"fmt"
	"encoding/json"
	mqtt "github.com/eclipse/paho.mqtt.golang"
	"reflect"

	"os"
	"os/signal"
	"os/exec"
	"syscall"
)


var cli mqtt.Client

const (
	mqttUrl = "tcp://127.0.0.1:1883"
	topic = "test"
	return_topic = "default/test"
)

type cmdResult struct{
	Result string `json: "result"`
}

func connectToMqtt() mqtt.Client {
	fmt.Println("[JUNE] In connectToMqtt Function")
	opts := mqtt.NewClientOptions()
	opts.AddBroker(mqttUrl)

	cli = mqtt.NewClient(opts)

	token := cli.Connect()
	if token.Wait() && token.Error() != nil {
		fmt.Println(token.Error())
	}

	return cli
}


func main() {

	stopchan := make(chan os.Signal)
	signal.Notify(stopchan, syscall.SIGINT, syscall.SIGKILL)
	defer close(stopchan)

	cli = connectToMqtt()

	// Link to pseudo device counter
	fmt.Println("[JUNE] Start NewCounter Function")

	token := cli.Subscribe(topic, 0, func(client mqtt.Client, msg mqtt.Message) {
		m := map[string]interface{}{}
		err := json.Unmarshal(msg.Payload(), &m)
		fmt.Println("[JUNE] In Subscribe Function / ", msg.Topic(), "/", string(msg.Payload()))
		fmt.Println("[TEST]", reflect.TypeOf(m["Command"]))

		// cmd!!
		cmd := fmt.Sprintf("%s",m["Command"])
		cmd_run := exec.Command("sh", "-c", cmd)
		stdout, cmd_err := cmd_run.Output()

		// MQTT Pub
		result := cmdResult{string(stdout)}
		resultBody, _ := json.Marshal(result)
		pub_token := cli.Publish(return_topic, 0, false, resultBody)

		if pub_token.Wait() && pub_token.Error() != nil {
			fmt.Println(pub_token.Error())
		}

		fmt.Println("[CMD]", string(stdout))
		fmt.Println("[ERROR]", cmd_err)

		if err != nil {
			fmt.Printf("Unmarshal error: %v\n", err)
		}

	})
	fmt.Println(token)

	if token.Wait() && token.Error() != nil {
		fmt.Println(token.Error())
	}

	select {
	case <-stopchan:
		fmt.Printf("Interrupt, exit.\n")
		break
	}
}
