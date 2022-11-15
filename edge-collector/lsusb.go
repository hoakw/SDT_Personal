// Copyright 2013 Google Inc.  All rights reserved.
// Copyright 2016 the gousb Authors.  All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// lsusb lists attached USB devices.
package main

import (
	//"flag"
	"fmt"
	"log"

	"github.com/google/gousb"
	"github.com/google/gousb/usbid"
)


type usbInfo struct {
	Bus			int
	Device		int
	ID			string
	Describe	string
}


func main() {
	ctx := gousb.NewContext()
	defer ctx.Close()
	bus_map := make([]usbInfo, 0)
	devs, err := ctx.OpenDevices(func(desc *gousb.DeviceDesc) bool {
		newBus := usbInfo{
			Bus:		desc.Bus,
			Device:		desc.Address,
			ID:			fmt.Sprintf("%s:%s", desc.Vendor, desc.Product),
			Describe:	usbid.Describe(desc),
		}
		bus_map = append(bus_map, newBus)
		fmt.Printf("Bus %03d Device %03d: ID %s:%s %s\n", desc.Bus, desc.Address, desc.Vendor, desc.Product, usbid.Describe(desc))
		return false
	})

	defer func() {
		for _, d := range devs {
			d.Close()
		}
	}()
	if err != nil {
		log.Fatalf("list: %s", err)
	}

	fmt.Println(bus_map)
}


type Storage struct {
	Name		string
	Totalsize	string
	Used		string
	UsedPercent	string
	Mountpoint	string
}

type usbInfo struct {
	Bus			int
	Device		int
	Id			string
	Describe	string
}

type netInfo struct {
	Name			string
	Address			[]net.Addr
	Mtu 			int
	HardwareAddr	net.HardwareAddr
}

type serialInfo struct {
	Index		int
	Uart		string
	Port 		string
	Irq			int
	Tx 			int
	Rx			int

}