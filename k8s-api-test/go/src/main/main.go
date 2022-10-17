package main

import (
//	"fmt"
//	"net"
	"status-controller/src/collector"
	"k8s.io/klog"
)

func main(){

	klog.Infof("[KETI] Start status controller...")
	err := collectors.New_collector()
	if err != nil {
		klog.Infof("[ERROR] %v", err)
	}

}
