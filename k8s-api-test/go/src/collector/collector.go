package collectors

import (
	"fmt"
	"time"
	"context"
	"reflect"
	 
	
	apiv1 "k8s.io/api/core/v1"
	appsv1 "k8s.io/api/apps/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/klog"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"

	//"k8s.io/client-go/tools/clientcmd"
	//"k8s.io/client-go/util/homedir"
	//"k8s.io/client-go/util/retry"
        
)

func New_collector() error {
	klog.Infof("[KETI] Start collector controller...")
	ns := "kube-system"
        for {
                err := collector_test(ns)
                if err != nil {
                        fmt.Println("[ERROR2] %v", err)
                }
                time.Sleep(time.Second * 10)
        }
        
	return nil
}
func collector_test(ns string) error {
        klog.Infof("[SDT] Test k8s API")
        config, err := rest.InClusterConfig()

        if err != nil {
                fmt.Println("[ERROR1] %v", err)
        }
        clientset, _ := kubernetes.NewForConfig(config)

		// deployment client 정의
        deploymentsClient := clientset.AppsV1().Deployments(apiv1.NamespaceDefault)

		// deployment spec 작성
        deployment := &appsv1.Deployment{
		ObjectMeta: metav1.ObjectMeta{
			Name: "deployment-test",
		},
		Spec: appsv1.DeploymentSpec{
			Replicas: int32Ptr(2),
			Selector: &metav1.LabelSelector{
				MatchLabels: map[string]string{
					"app": "deploy-test",
				},
			},
			Template: apiv1.PodTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{
					Labels: map[string]string{
						"app": "deploy-test",
					},
				},
				Spec: apiv1.PodSpec{
					Containers: []apiv1.Container{
						{
							Name:  "web",
							Image: "nginx:1.12",
							Ports: []apiv1.ContainerPort{
								{
									Name:          "http",
									Protocol:      apiv1.ProtocolTCP,
									ContainerPort: 80,
								},
							},
						},
					},
				},
			},
		},
	}

	// Create Deployment
	klog.Infof("Creating deployment...")
	result, err := deploymentsClient.Create(context.TODO(), deployment, metav1.CreateOptions{})
	if err != nil {
		panic(err)
	}
	klog.Infof("Created deployment : ", reflect.TypeOf(result))//.GetObjectMeta().GetName())
	klog.Infof("Created deployment Name : %s", result.ObjectMeta.GetName())
	klog.Infof("Created deployment Namespace : %s", result.ObjectMeta.GetName())
	klog.Infof("Created deployment DeploymentSpec : %s", result.Spec.Template.Labels)
	//klog.Infof("Created deployment deploymentstatus : %s", result.GetDeploymentStatus())

	time.Sleep(time.Second * 10)

	deploy_name := result.GetObjectMeta().GetName()
	klog.Infof("delete deployment... : ", deploy_name)

	deletePolicy := metav1.DeletePropagationForeground
	if err := deploymentsClient.Delete(context.TODO(), deploy_name, metav1.DeleteOptions{
		PropagationPolicy: &deletePolicy,
	}); err != nil {
		panic(err)
	}
	fmt.Println("Deleted deployment.")
	
        // Pod 생성하기
        

        // Pod List 불러오기
        /*        
        pods, err := clientset.CoreV1().Pods("").List(metav1.ListOptions{})
        for _, pod := range pods.Items {
                if pod.Status.Phase == v1.PodRunning {
                        for _, ctn := range pod.Spec.Containers {
                                fmt.Println("[SDT-Container Name] ", ctn.Name)
                        }
                }
        }
        */
        return err
}

func int32Ptr(i int32) *int32 { return &i }