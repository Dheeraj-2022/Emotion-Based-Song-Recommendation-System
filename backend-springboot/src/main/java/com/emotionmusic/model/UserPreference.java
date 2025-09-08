package com.emotionmusic.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Entity
@Table(name = "user_preferences")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class UserPreference {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Column(name = "favorite_language")
    private String favoriteLanguage;

    @Column(name = "favorite_singer")
    private String favoriteSinger;

    @Column(name = "favorite_genre")
    private String favoriteGenre;
}
