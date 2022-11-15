package main


import (
	"os"
	"fmt"
	"net"
	"flag"
	// "math/rand"
	"bufio"
	//"io"
	//"io/ioutil"
	// "context"
	// "sort"
	"strconv"
	"strings"
	// "reflect"
	"time"
	"context"

	human "github.com/dustin/go-humanize"
    "github.com/shirou/gopsutil/disk"
	"github.com/google/gousb"
	"github.com/google/gousb/usbid"
	// lsmod "github.com/Djarvur/go-lsmod"
	"github.com/influxdata/influxdb-client-go"
	"github.com/shirou/gopsutil/v3/process"

	// metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	// //"k8s.io/klog"
	// v1 "k8s.io/api/core/v1"
	// "k8s.io/client-go/kubernetes"
	// "k8s.io/client-go/tools/clientcmd"
	// metrics "k8s.io/metrics/pkg/client/clientset/versioned"

        
)

// type ContainerStatus struct{
// 	Name		string
// 	Cpu			int64
// 	Memory		int64
// }

// type PodStatus struct {
// 	Name		string
// 	Status		v1.PodPhase
// 	NodeName	string
// 	Container 	[]ContainerStatus
// }

// type Pod struct {
// 	Name            string
// 	Uid             string
// 	NodeName        string
// 	RequestMilliCpu int64
// 	RequestMemory   int64
// }

type Modules struct {
	Name		string
	Memory		uint64
	Used		uint64
	Depends		string
}

type procInfo struct {
	Id			string
	Cpu			float32
	Memory		float32
	Context		string	
}

type diskInfo struct {
	Name		string
	Totalsize	string
	Used		float64
	UsedPercent	string
	Mountpoint	string
}

type usbInfo struct {
	Bus			int
	Device		string
	Id			string
	Describe	string
}

type netInfo struct {
	Name			string
	Address			string
	Mtu 			int
	HardwareAddr	net.HardwareAddr
}

type serialInfo struct {
	Index		string
	Uart		string
	Port 		string
	Irq			int
	Tx 			int
	Rx			int

}

var prior_rx int
var prior_tx int

//getProc
func getProc() []procInfo {
	processes, _ := process.Processes()

	processes_cpu_mem := make([]procInfo, 0)
	for _, p := range processes {
		// p_name, _ := p.Name()
		p_cpu_percent, _ := p.CPUPercent()
		// p_cpu := fmt.Sprintf("%0.2f", float32(p_cpu_percent))
		p_mem_percent, _ := p.MemoryPercent()
		// p_mem := fmt.Sprintf("%0.2f", float32(p_mem_percent))
		p_name, _ := p.Name()
		p_id := fmt.Sprintf("%d", int(p.Pid))
		if p_cpu_percent < 0.3 {
			continue
		}
		newProc := procInfo{
			Id:			p_id,
			Cpu:		float32(p_cpu_percent),
			Memory:		float32(p_mem_percent),
			Context:	p_name,
		}

		processes_cpu_mem = append(processes_cpu_mem, newProc)
	}

	return processes_cpu_mem
}

//disk
func getDisk() []diskInfo{
	diskList := make([]diskInfo, 0)
    parts, _ := disk.Partitions(true)
    for _, p := range parts {
        device := p.Mountpoint
		s, _ := disk.Usage(device)
        if s == nil || s.Total == 0 {
            continue
        } else if strings.Contains(p.Mountpoint, "var/lib") {
			continue
		}

		disk_percent := fmt.Sprintf("%0.2f%%", s.UsedPercent)
		newDisk := diskInfo{
			Name:			p.Device,
			Totalsize:		human.Bytes(s.Total),
			Used:			float64(s.Used)/1024/1024/1024,
			UsedPercent:	disk_percent,
			Mountpoint:		p.Mountpoint,
		}

		diskList = append(diskList, newDisk)
        // fmt.Printf(formatter,
        //     p.Device,
        //     human.Bytes(s.Total),
        //     human.Bytes(s.Used),
        //     human.Bytes(s.Free),
        //     percent,
        //     p.Mountpoint,
        // )
    }
	
	return diskList
}

//usb
func getUsb() []usbInfo{
	ctx := gousb.NewContext()
	defer ctx.Close()
	bus_map := make([]usbInfo, 0)
	devs, err := ctx.OpenDevices(func(desc *gousb.DeviceDesc) bool {
		newBus := usbInfo{
			Bus:		int(desc.Bus),
			Device:		fmt.Sprintf("%d", int(desc.Address)),
			Id:			fmt.Sprintf("%s:%s", desc.Vendor, desc.Product),
			Describe:	usbid.Describe(desc),
		}
		bus_map = append(bus_map, newBus)
		return false
	})

	defer func() {
		for _, d := range devs {
			d.Close()
		}
	}()
	if err != nil {
		fmt.Println("[Error] ", err)
	}

	return bus_map
}

//serial
func getSerial() []serialInfo {
	data, err := os.Open("/proc/tty/driver/serial")
	if err != nil {
		fmt.Println(err)
	}
	defer data.Close()

	scan := bufio.NewScanner(data)

	serial_info := make([]serialInfo, 0)
	var tx int
	var rx int

	scan.Scan()
	for scan.Scan() {
		data_slice := strings.Split(strings.Replace(scan.Text(), ":", " ", -1), " ")
		if len(data_slice) < 9 {
			tx = -1
			rx = -1
		} else {
			tx, _ = strconv.Atoi(data_slice[9])
			rx, _ = strconv.Atoi(data_slice[11])
		}
		// index, _ := strconv.Atoi(data_slice[0])
		irq, _ := strconv.Atoi(data_slice[7])
		newSerial := serialInfo{
			Index:		data_slice[0],
			Uart:		data_slice[3],
			Port: 		data_slice[5],
			Irq:		irq,
			Tx:			tx,
			Rx:			rx,
		}
		serial_info = append(serial_info, newSerial)
	}

	return serial_info
}

func getNetwork() []netInfo{
	netw, err := net.Interfaces()
	if err != nil {
		os.Stderr.WriteString("Oops: " + err.Error() + "\n")
		os.Exit(1)
	}
	
	net_info := make([]netInfo, 0)
	var net_addrs string
	for _, inter := range netw {
		addrs,_ := inter.Addrs()
		if len(addrs) >= 2 {
			net_addrs = addrs[0].String()
		} else if len(addrs) == 0 {
			net_addrs = "notFound"
		} else if strings.Contains(addrs[0].String(), ":") {
			net_addrs = "notFound"
		}

		newNet := netInfo{
			Name:			inter.Name,
			HardwareAddr:	inter.HardwareAddr,
			Mtu:			inter.MTU,
			Address:		net_addrs,
		}
		net_info = append(net_info, newNet)
	}
	return net_info
}

// func getRunningPods(clientset *kubernetes.Clientset, mc *metrics.Clientset) []PodStatus {
// 	fmt.Println("Start KETI_getRunningPods...")
// 	pods, err := clientset.CoreV1().Pods("").List(context.TODO(), metav1.ListOptions{})

// 	if err != nil {
// 			fmt.Println("[ERROR] ",err)
// 	}
	
// 	runningPods := make([]PodStatus, 0)
// 	for _, pod := range pods.Items {

// 		metric_pod, _ := mc.MetricsV1beta1().PodMetricses(pod.Namespace).Get(context.TODO(), pod.Name, metav1.GetOptions{})
// 		Container_res := metric_pod.Containers
		
// 		containerInfo := make([]ContainerStatus, 0)
// 		for _, cont_res := range Container_res {
// 			newContainer := ContainerStatus{
// 				Name:		cont_res.Name,
// 				Cpu:		cont_res.Usage.Cpu().MilliValue(),
// 				Memory: 	cont_res.Usage.Memory().Value(),
// 			}	
// 			containerInfo = append(containerInfo, newContainer)
// 		}

// 		// Check Status
// 		newPod := PodStatus{
// 			Name:		pod.Name,
// 			Status:		pod.Status.Phase,
// 			NodeName:	pod.Spec.NodeName,
// 			Container:	containerInfo,
// 		}

// 		runningPods = append(runningPods, newPod)
// 	}
// 	// runningPods는 실행중인 Pod의 정보들을 담아서 저장한 곳
// 	return runningPods
// }

func insertData(client influxdb2.Client, data map[string]interface{}, nodeName string, nodeRule string){
	writeApi := client.WriteAPI("sdt", "test4")
	proc_data := data["process"].([]procInfo)
	disk_data := data["disk"].([]diskInfo)
	net_data := data["network"].([]netInfo)
	serial_data := data["serial"].([]serialInfo)
	usb_data := data["usb"].([]usbInfo)

	// Process
	for _, proc := range proc_data {
		proc_p := influxdb2.NewPoint(
			"edge_system",
			map[string]string{
				"hostname":		nodeName,
				"noderule":		nodeRule,
				"type":			"process",
				"name":			proc.Context,
				"id":			proc.Id,
			},
			map[string]interface{}{
				"cpu":			proc.Cpu,
				"mem":			proc.Memory,
			},
			time.Now())
		writeApi.WritePoint(proc_p)
	}

	// disk
	for _, disk_info := range disk_data {
		disk_p := influxdb2.NewPoint(
			"edge_system",
			map[string]string{
				"hostname": 	nodeName,
				"noderule": 	nodeRule,
				"type":			"disk",
				"name":			disk_info.Name,
				"mountpoint":	disk_info.Mountpoint,
				"usedpercent":	disk_info.UsedPercent,
				"totalsize":	disk_info.Totalsize,
			},
			map[string]interface{}{
				"used":			disk_info.Used,
			},
			time.Now())
		writeApi.WritePoint(disk_p)
	}
		// usb
	for _, usb_info := range usb_data {
		usb_p := influxdb2.NewPoint(
			"edge_system",
			map[string]string{
				"hostname": nodeName,
				"noderule": nodeRule,
				"type":		"usb",
				"id":		usb_info.Id,
				"device":	usb_info.Device,
				"describe":	usb_info.Describe,
			},
			map[string]interface{}{
				"bus": 		usb_info.Bus,
			},
			time.Now())
		writeApi.WritePoint(usb_p)
	}
	// network
	for _, net_info := range net_data {
		net_p := influxdb2.NewPoint(
			"edge_system",
			map[string]string{
				"hostname": nodeName,
				"noderule": nodeRule,
				"type":		"network",
				"name": 	net_info.Name,
			},
			map[string]interface{}{
				"address":		net_info.Address,
				"mtu":			net_info.Mtu,
				"hardwareaddr":	net_info.HardwareAddr,
			},
			time.Now())
		writeApi.WritePoint(net_p)
	}

	// serial
	for _, serial_info := range serial_data {
		serial_p := influxdb2.NewPoint(
			"edge_system",
			map[string]string{
				"hostname": nodeName,
				"noderule": nodeRule,
				"type":		"serial",
				"index": 	serial_info.Index,
				"uart": 	serial_info.Uart,
				"port": 	serial_info.Port,
			},
			map[string]interface{}{
				"tx":		serial_info.Tx,
				"rx":		serial_info.Rx,
			},
			time.Now())
		writeApi.WritePoint(serial_p)
	}

	writeApi.Flush()
}

func getData(client influxdb2.Client){
	queryApi := client.QueryAPI("sdt")
	query := `from(bucket:"test3")
				|> range(start: -2d) 
				|> last()
				|> filter(fn: (r) => r._measurement == "edge_system")
				|> filter(fn: (r) => r._field == "rx")
				|> filter(fn: (r) => r.index == "0")
	       `
	result, err := queryApi.Query(context.Background(), query)
	if err == nil {
		for result.Next() {
			fmt.Printf("%v : %v %v %v\n", result.Record().Time(), result.Record().ValueByKey("value"), result.Record().Field(), result.Record().Value())
		}

		if result.Err() != nil {
			fmt.Printf("query parsing error: %s\n", result.Err().Error())
		}
	} else {
		panic(err)
	}
}

func main() {
	hostname_params := flag.String("host", "nil", "nil") 
	rule_params := flag.String("rule", "nil", "nil")

	flag.Parse()

	fmt.Println("test")
	//Influx DB
	tokens := "NjySN6ZknNHRt8LwLVmv6mjdo4Ip4W_ZlJgyPSRQuvjQIMtKObBpCwUlOXXfdkPEE7LRQ9f-oAdLI_wTTPoZ1g=="
	client := influxdb2.NewClient("http://192.168.1.20:30626", tokens)

	for true {

		//processor
		proc_info := getProc()

		//disk
		// storage_formatter := "%-14s %7s %7s %4s %s \n"
		// fmt.Printf(storage_formatter, "Filesystem", "Size", "Used", "Use%", "Mount")
		disk_info := getDisk()
		// for _, storage_value := range disk_info{
		// 	fmt.Printf(storage_formatter, storage_value.Name, storage_value.Totalsize, storage_value.Used, storage_value.UsedPercent, storage_value.Mountpoint)
		// }

		//usb info
		usb_info := getUsb()
		// for _, usb_value := range usb_info{
		// 	fmt.Printf("Bus %03d Device %03d: ID %s %s\n", usb_value.Bus, usb_value.Device, usb_value.Id, usb_value.Describe)
		// }

		//serial info
		serial_info := getSerial()
		// for _, serial_value := range serial_info{
		// 	fmt.Printf("Index: %03d Uart: %10s Port: %10s Irq: %3d tx: %10d rx: %10d\n", serial_value.Index, serial_value.Uart, serial_value.Port, serial_value.Irq, serial_value.Tx, serial_value.Rx)
		// }

		//network info
		net_info := getNetwork()
		// for _, net_value := range net_info{
		// 	fmt.Printf("Name: %15s MTU: %06d HWaddr: %20s Addr: %s\n", net_value.Name, net_value.Mtu, net_value.HardwareAddr, net_value.Address)
		// }
		
		all_data := map[string]interface{}{
			"process":	proc_info,
			"disk":		disk_info,
			"usb":		usb_info,
			"serial":	serial_info,
			"network":	net_info,
		}

		// fmt.Println(all_data)
		// fmt.Println(*rule_params, *hostname_params)

		//insert
		// fmt.Println(*hostname_params, " / ", *rule_params)
		insertData(client, all_data, *hostname_params, *rule_params)

		// //read
		// getData(client)
		fmt.Println(time.Now())
		time.Sleep(3 * time.Second)
	}
	client.Close()

	// lsmod_info, lsmod_formatter := getModules()
	// for _, mod_value := range lsmod_info{
	// 	fmt.Printf(lsmod_formatter, mod_value.Name, mod_value.Memory, mod_value.Used, mod_value.Depends)
	// }

	// master_config, _ :=  clientcmd.BuildConfigFromFlags("", "/home/sdt/.kube/config")
	// clientset, _ := kubernetes.NewForConfig(master_config)
	// metric_c, _ := metrics.NewForConfig(master_config)
	// pod_list := getRunningPods(clientset, metric_c)
	// metric_test, _ := metric_c.MetricsV1beta1().NodeMetricses().List(context.TODO(), metav1.ListOptions{})


	// for _, pod := range pod_list {
	// 	fmt.Printf("[Node: %s] - Pod Name : %s / Pod Status : %s / Pod Resource utils : %s \n", pod.NodeName, pod.Name, pod.Status, pod.Container)
	// 	for _, pod_container := range pod.Container {
	// 		fmt.Printf(" - [Container] Name : %s / Cpu : %dm / Memory %dMi \n", pod_container.Name, pod_container.Cpu, pod_container.Memory / 1024 / 1024)
	// 	}
	// }

	// for _, nodes := range metric_test.Items {
	// 	fmt.Println(nodes.Name , ":  CPU = ", nodes.Usage.Cpu().MilliValue(), "m / Memory = ", nodes.Usage.Memory().Value() / 1024 / 1024, "Mi")
	// }
}