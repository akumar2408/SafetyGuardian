package main

import (
    "bytes"
    "io"
    "io/ioutil"
    "net/http"
)

// proxyRequest forwards a request body to the given URL and writes the response back.
func proxyRequest(w http.ResponseWriter, r *http.Request, url string) {
    body, err := ioutil.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "Failed to read request body", http.StatusBadRequest)
        return
    }
    resp, err := http.Post(url, "application/json", bytes.NewBuffer(body))
    if err != nil {
        http.Error(w, "Service unavailable", http.StatusServiceUnavailable)
        return
    }
    defer resp.Body.Close()
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(resp.StatusCode)
    io.Copy(w, resp.Body)
}

// qaHandler proxies question answering requests to the QA service.
func qaHandler(w http.ResponseWriter, r *http.Request) {
    proxyRequest(w, r, "http://qa:5003/qa")
}

// summarizeHandler proxies summarization requests to the QA service.
func summarizeHandler(w http.ResponseWriter, r *http.Request) {
    proxyRequest(w, r, "http://qa:5003/summarize")
}

// translateHandler proxies translation requests to the translation service.
func translateHandler(w http.ResponseWriter, r *http.Request) {
    proxyRequest(w, r, "http://translation:5004/translate")
}

// ttsHandler proxies text-to-speech requests to the translation service.
func ttsHandler(w http.ResponseWriter, r *http.Request) {
    proxyRequest(w, r, "http://translation:5004/tts")
}

// audioClassifyHandler proxies audio classification requests to the audio service.
func audioClassifyHandler(w http.ResponseWriter, r *http.Request) {
    proxyRequest(w, r, "http://audio:5002/classify_audio")
}

// detectHandler proxies object detection requests to the vision service.
func detectHandler(w http.ResponseWriter, r *http.Request) {
    proxyRequest(w, r, "http://vision:5001/detect")
}


func init() {
    http.HandleFunc("/health", healthHandler)
    http.HandleFunc("/api/register", registerHandler)
    http.HandleFunc("/api/login", loginHandler)
    http.HandleFunc("/api/detect", detectHandler)
    http.HandleFunc("/api/qa", qaHandler)
    http.HandleFunc("/api/summarize", summarizeHandler)
    http.HandleFunc("/api/translate", translateHandler)
    http.HandleFunc("/api/tts", ttsHandler)
    http.HandleFunc("/api/classify_audio", audioClassifyHandler)
}
