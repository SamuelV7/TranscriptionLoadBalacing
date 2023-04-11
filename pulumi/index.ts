import * as pulumi from "@pulumi/pulumi";
import * as digitalocean from "@pulumi/digitalocean";

// Create a droplet digital ocean
const droplet = new digitalocean.Droplet("my-droplet", {
    image: "ubuntu-18-04-x64",
    region: "nyc3",
    size: "s-1vcpu-1gb",
})

const kubernetes = new digitalocean.KubernetesCluster("my-kubernetes", {
    region: "nyc3",
    version: "1.17.3-do.0",
    nodePool: {
        name: "default",
        size: "s-1vcpu-1gb",
        nodeCount: 1,
    },
});

// https in the kubernetes cluster
const kubernetesIngress = new digitalocean.KubernetesClusterIngress("my-kubernetes-ingress", {
    clusterId: kubernetes.id,
    ingress: {
        name: "example",
        rules: [{
            host: "example.com",
            http: {
                paths: [{
                    path: "/",
                    backend: {
                        serviceName: "example",
                        servicePort: 80,
                    },
                }],
            },
        }],
    },
});
