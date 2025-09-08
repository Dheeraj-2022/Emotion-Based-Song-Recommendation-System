package com.emotionmusic.controller;

import com.emotionmusic.model.UserPreference;
import com.emotionmusic.repository.UserPreferenceRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/preferences")
public class UserPreferenceController {
    @Autowired
    private UserPreferenceRepository preferenceRepository;

    @GetMapping("/{userId}")
    public ResponseEntity<?> getUserPreferences(@PathVariable Long userId) {
        return preferenceRepository.findByUserId(userId)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<?> savePreferences(@RequestBody UserPreference preference) {
        UserPreference saved = preferenceRepository.save(preference);
        return ResponseEntity.ok(saved);
    }
}