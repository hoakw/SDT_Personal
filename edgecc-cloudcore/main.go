package main

import (
	"os"
	"fmt"
	"flag"
	"bytes"
	"net/http"
	"io/ioutil"
	"encoding/json"
)

var tests = map[string]*Msg{}

type Msg struct{
	Result string `json:"result"` 
}

type Cmd struct{
	Command string `json: "command"`
}

func main() {
	//parameter 
	cmd_context := flag.String("cmd", "nil", "nil")
	target_node := flag.String("node", "nil", "nil")
	flag.Parse()

	//Request - Post Method
	url := "http://192.168.1.20:9443"
	path := fmt.Sprintf("/%s/default/test", *target_node)
	cmd := Cmd{*cmd_context}
	cbytes, _ := json.Marshal(cmd)
	buff := bytes.NewBuffer(cbytes)
	resp, _ := http.Post(url+path, "application/json", buff)
	defer resp.Body.Close()

	respBody, _ := ioutil.ReadAll(resp.Body)
	fmt.Println("[Response] ", string(respBody))

	//Run Rest
	http.HandleFunc("/test", func(wr http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodGet:
			json.NewEncoder(wr).Encode(tests)
		case http.MethodPost:
			var tmp Msg
			json.NewDecoder(r.Body).Decode(&tmp)
			tests[tmp.Result] = &tmp
			json.NewEncoder(wr).Encode(tmp)
			fmt.Println("[Result] \n", tmp.Result)
			os.Exit(0)
		}

	})
	http.ListenAndServe(":8080", nil)

}