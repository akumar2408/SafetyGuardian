package main

import (
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


// healthHandler provides a simple health check endpoint.
func healthHandler(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    w.Write([]byte("ok"))
}

func main() {
   

    
