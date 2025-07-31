package main

import (
    "encoding/json"
    "io/ioutil"
    "log"
    "net/http"
)

// Request structure for detection endpoint. In a real system this
// might contain base64‑encoded images or URLs to media stored in
// object storage. For this skeleton, only an ImageURL field is
// included.
type detectRequest struct {
    ImageURL string `json:"image_url"`
}

// detectResponse contains a list of detected objects. A more
// sophisticated response could include bounding boxes and
// confidence scores.
type detectResponse struct {
    Detections []string `json:"detections"`
}

// detectHandler forwards the request to the vision service. In this
// skeleton implementation we return a hard coded response.
func detectHandler(w http.ResponseWriter, r *http.Request) {
    // Decode the request body
    var req detectRequest
    body, err := ioutil.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "cannot read body", http.StatusBadRequest)
        return
    }
    json.Unmarshal(body, &req)
    // TODO: call the Python vision service at http://vision:5001/detect
    // and return its result.
    resp := detectResponse{Detections: []string{"helmet", "vest"}}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

// healthHandler provides a simple health check endpoint.
func healthHandler(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    w.Write([]byte("ok"))
}

func main() {
    http.HandleFunc("/health", healthHandler)
    http.HandleFunc("/api/detect", detectHandler)
    log.Println("Gateway running on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatal(err)
    }
}
