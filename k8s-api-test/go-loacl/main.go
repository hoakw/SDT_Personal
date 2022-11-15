package main


import (
	"fmt"
	"context"
	//"reflect"
	
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	//"k8s.io/klog"

	v1 "k8s.io/api/core/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/tools/clientcmd"
        
)
type Pod struct {
	Name            string
	Uid             string
	NodeName        string
	RequestMilliCpu int64
	RequestMemory   int64
}

func getRunningPods(clientset *kubernetes.Clientset) []Pod {
	fmt.Println("Start KETI_getRunningPods...")
	pods, err := clientset.CoreV1().Pods("").List(context.TODO(), metav1.ListOptions{})

	if err != nil {
			fmt.Println("[ERROR] ",err)
	}
	
	runningPods := make([]Pod, 0)
	for _, pod := range pods.Items {
			if pod.Status.Phase == v1.PodRunning {
					var requestsMilliCpu, requestsMemory int64
					for _, ctn := range pod.Spec.Containers {
							requestsMilliCpu += ctn.Resources.Requests.Cpu().MilliValue()
							//requestsMilliCpu += ctn.Resources.Limits.Cpu().MilliValue()
							requestsMemory += ctn.Resources.Requests.Memory().Value() / 1024 / 1024
							//requestsMemory += ctn.Resources.Limits.Memory().Value() / 1024 / 1024
					}
					newPod := Pod{
							Name:            pod.Name,
							Uid:             pod.Namespace,
							NodeName:        pod.Spec.NodeName,
							RequestMilliCpu: requestsMilliCpu,
							RequestMemory:   requestsMemory,
					}
					runningPods = append(runningPods, newPod)
			}
	}
	// runningPods는 실행중인 Pod의 정보들을 담아서 저장한 곳
	return runningPods

}


func main() {
	master_config, _ :=  clientcmd.BuildConfigFromFlags("", "/home/june/.kube/config")
	clientset, _ := kubernetes.NewForConfig(master_config)
	pod_list := getRunningPods(clientset)
	fmt.Println(pod_list)
}