const k8s = require('@kubernetes/client-node');

// Get Confing
const kc = new k8s.KubeConfig();
kc.loadFromDefault();

const coreApi = kc.makeApiClient(k8s.CoreV1Api);
const appApi = kc.makeApiClient(k8s.AppsV1Api);

coreApi.listNamespacedPod('default')
    .then((res) => {
        res.body.items.forEach( (item) => {
            console.log(item.metadata.name);
        })
    });

var deployment_body = {
    metadata: {
        name: 'nginx-deployment',
        namespace: 'default',
        labels:{
            app: 'nginx'
        }
    },
    spec: {
        selector: {
            matchLabels: {
                app: 'nginx'
            }
        },
        replicas: 3,
        template: {
            metadata: {
                labels: {
                    app: 'nginx'
                }
            },
            spec: {
                containers: [
                    {
                        name: 'nginx',
                        image: 'nginx',
                        ports: [{
                            containerPort: 80
                        }],
                        resources: {
                            requests:{
                                "cpu": "250m",
                                "memory": "500Mi"
                            }
                        }
                    }
                ]
            }
        }
    }
};

var service_body = {
    metadata: {
        name: 'niginx-service',
        namespace: 'default'
    },
    spec: {
        ports: [
            {
                port: 8080,
                targetPort: 80,
                protocol: 'TCP',
                name: 'nginx-service'
            }
        ],
        selector: {
            app: 'nginx'
        }
    }
}
// appApi.createNamespacedDeployment('default', deployment_body).then(
//     (respones) => {
//         console.log('Creating' + deployment_body.metadata.name);
//     },
//     (err) => {
//         console.log('Error...');
//     }
// );

// coreApi.createNamespacedService('default', service_body).then(
//     (respones) => {
//         console.log('Creating' + service_body.metadata.name);
//     },
//     (err) => {
//         console.log('Error...');
//     }
// )


// appApi.deleteNamespacedDeployment(deployment_body.metadata.name, 'default').then(
//     (respones) => {
//         console.log('Deleted' + deployment_body.metadata.name);
//     },
//     (err) => {
//         console.log('Error...');
//     }    
// )
// coreApi.deleteNamespacedService(service_body.metadata.name, 'default').then(
//     (respones) => {
//         console.log('Deleted' + service_body.metadata.name);
//     },
//     (err) => {
//         console.log('Error...');
//     }   
// )


