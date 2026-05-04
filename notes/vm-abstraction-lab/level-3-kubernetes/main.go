package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "os"
    "time"
)

type Response struct {
    Level     int       `json:"level"`
    Type      string    `json:"type"`
    Pod       string    `json:"pod"`
    Node      string    `json:"node"`
    Namespace string    `json:"namespace"`
    Timestamp time.Time `json:"timestamp"`
    Message   string    `json:"message"`
}

func main() {
    http.HandleFunc("/", handler)
    http.HandleFunc("/health", health)
    
    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }
    
    log.Printf("Level 3 Kubernetes service starting on port %s", port)
    log.Fatal(http.ListenAndServe(":"+port, nil))
}

func handler(w http.ResponseWriter, r *http.Request) {
    response := Response{
        Level:     3,
        Type:      "Kubernetes",
        Pod:       os.Getenv("HOSTNAME"),
        Node:      os.Getenv("NODE_NAME"),
        Namespace: os.Getenv("POD_NAMESPACE"),
        Timestamp: time.Now(),
        Message:   "Container orchestration at scale",
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func health(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    fmt.Fprintf(w, "OK")
}
