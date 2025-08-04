package main

import (
    "encoding/json"
    "net/http"
    "sync"
)

// User represents a user account.
type User struct {
    Username string `json:"username"`
    Password string `json:"password"`
}

var (
    users   = make(map[string]User)
    usersMu sync.Mutex
)

// registerHandler handles user registration requests.
func registerHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }
    var u User
    if err := json.NewDecoder(r.Body).Decode(&u); err != nil {
        http.Error(w, "Invalid request body", http.StatusBadRequest)
        return
    }
    usersMu.Lock()
    defer usersMu.Unlock()
    if _, exists := users[u.Username]; exists {
        http.Error(w, "User already exists", http.StatusBadRequest)
        return
    }
    users[u.Username] = u
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(map[string]string{"message": "User registered"})
}

// loginHandler handles user login requests.
func loginHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }
    var creds User
    if err := json.NewDecoder(r.Body).Decode(&creds); err != nil {
        http.Error(w, "Invalid request body", http.StatusBadRequest)
        return
    }
    usersMu.Lock()
    user, exists := users[creds.Username]
    usersMu.Unlock()
    if !exists || user.Password != creds.Password {
        http.Error(w, "Invalid credentials", http.StatusUnauthorized)
        return
    }
    json.NewEncoder(w).Encode(map[string]string{
        "message": "Login successful",
        "token":   "dummy-token",
    })
}
